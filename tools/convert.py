"""PPTX -> Slidev markdown converter (first pass; editorial pass follows by hand).

usage: python3 convert.py deck.pptx ref_png_dir out_deck_dir [--title T] [--kicker K]
  ref_png_dir: LibreOffice render of the deck with hidden slides unhidden, one PNG per slide
  (tools/prep_pptx.py makes both; `npm run convert` runs the whole pipeline)
"""
import sys, os, re, hashlib, subprocess, glob, colorsys, io, argparse
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER
from PIL import Image

A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('ref'); ap.add_argument('out')
ap.add_argument('--title', default='Lecture'); ap.add_argument('--kicker', default='')
A_ = ap.parse_args()
SRC, REF, OUT, TITLE, KICKER = A_.src, A_.ref, A_.out, A_.title, A_.kicker
IMG = os.path.join(OUT, 'public', 'img')
os.makedirs(IMG, exist_ok=True)

prs = Presentation(SRC)
SW, SH = prs.slide_width, prs.slide_height
refs = sorted(glob.glob(os.path.join(REF, '*.png')))
TITLE_TYPES = {PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE}
COMPLEX = {MSO_SHAPE_TYPE.GROUP, MSO_SHAPE_TYPE.AUTO_SHAPE, MSO_SHAPE_TYPE.LINE,
           MSO_SHAPE_TYPE.FREEFORM, MSO_SHAPE_TYPE.TABLE, MSO_SHAPE_TYPE.CHART}


# ---------- text ----------
def color_class(hexv):
    if not hexv:
        return None
    r, g, b = (int(hexv[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.25 or l < 0.12 or l > 0.92:
        return None
    h *= 360
    if h < 25 or h >= 330:
        return 'dx-red'
    if 80 <= h < 170:
        return 'dx-green'
    if 170 <= h < 255:
        return 'dx-blue'
    if 255 <= h < 330:
        return 'dx-purple'
    return 'dx-red'  # oranges read as emphasis


PUA = {0xF0E0: '→', 0xF0AE: '→', 0xF0E8: '⇨', 0xF0DF: '←', 0xF04A: '☺', 0xF04C: '☹', 0xF0FC: '✓',
       0xF0FB: '✗', 0xF0B9: '≠', 0xF0A3: '≤', 0xF0B3: '≥', 0xF0B4: '×', 0xF0CE: '∈', 0xF0C6: '∅',
       0xF0D9: '∧', 0xF0DA: '∨', 0xF0D8: '¬', 0xF0A5: '∞', 0xF0B1: '±'}
UNMAPPED = set()


def fix_pua(t):
    out = []
    for ch in t:
        o = ord(ch)
        if 0xF000 <= o <= 0xF0FF:
            if o in PUA:
                out.append(PUA[o])
            else:
                UNMAPPED.add(hex(o))
                out.append('�')
        else:
            out.append(ch)
    return ''.join(out)


def esc(t):
    t = fix_pua(t)
    t = t.replace('\\', '\\\\').replace('$', '\\$').replace('<', '&lt;').replace('>', '&gt;')
    t = t.replace('→', '→').replace('\v', '<br>')
    return t


def run_fmt(r):
    rPr = r._r.find(A + 'rPr')
    f = r.font
    base = int(rPr.get('baseline')) if rPr is not None and rPr.get('baseline') not in (None, '0') else 0
    cls = None
    try:
        if f.color and f.color.type is not None and f.color.rgb is not None:
            cls = color_class(str(f.color.rgb))
    except Exception:
        pass
    link = r.hyperlink.address if r.hyperlink and r.hyperlink.address else None
    return (bool(f.bold), bool(f.italic), bool(f.underline), cls, link, (base > 0) - (base < 0))


def wrap(text, fmt):
    b, i, u, cls, link, base = fmt
    t = esc(text)
    lead = re.match(r'^\s*', t).group(0)
    trail = re.search(r'\s*$', t).group(0)
    core = t.strip()
    if not core:
        return t
    if base:
        core = f"<sup>{core}</sup>" if base > 0 else f"<sub>{core}</sub>"
    html = base != 0
    if i:
        core = f"<em>{core}</em>" if html else f"*{core}*"
    if b:
        core = f"<strong>{core}</strong>" if html or i else f"**{core}**"
    if u:
        core = f"<u>{core}</u>"
    if cls:
        core = f'<span class="{cls}">{core}</span>'
    if link:
        core = f"[{core}]({link})"
    return lead + core + trail


def segments_md(segs):
    # merge identical formatting
    merged = []
    for text, fmt in segs:
        if merged and merged[-1][1] == fmt and fmt is not None:
            merged[-1] = (merged[-1][0] + text, fmt)
        else:
            merged.append((text, fmt))
    out, k = [], 0
    while k < len(merged):
        text, fmt = merged[k]
        if fmt is None:
            out.append(text)
            k += 1
            continue
        # italic single letter (+ subscript) -> KaTeX
        if fmt[1] and re.fullmatch(r'\s*[A-Za-z]\s*', text) and not fmt[4]:
            tex, k2 = text.strip(), k + 1
            while k2 < len(merged) and merged[k2][1] and merged[k2][1][5] != 0 and re.fullmatch(r'[\w+\-]+', merged[k2][0].strip()):
                tex += ('_{' if merged[k2][1][5] < 0 else '^{') + merged[k2][0].strip() + '}'
                k2 += 1
            lead = ' ' if text[:1].isspace() else ''
            trail = ' ' if text[-1:].isspace() else ''
            m = f'${tex}$'
            out.append(lead + (f'<span class="{fmt[3]}">{m}</span>' if fmt[3] else m) + trail)
            k = k2
            continue
        out.append(wrap(text, fmt))
        k += 1
    return ''.join(out)


def para_md(p):
    from pptx.text.text import _Run
    segs = []
    for child in p._p:
        tag = child.tag.split('}')[1]
        if tag == 'r':
            r = _Run(child, p)
            if r.text:
                segs.append((r.text, run_fmt(r)))
        elif tag == 'br':
            segs.append(('<br>', None))
        elif tag == 'fld':
            segs.append((esc(''.join(child.itertext())), None))
        elif 'AlternateContent' in child.tag or tag == 'oMathPara':
            math = ''.join(t for t in child.itertext())
            segs.append((f'<span class="todo-math">{esc(math)}</span>', None))
    return segments_md(segs).strip()


def bullet_kind(p, default):
    pPr = p._p.find(A + 'pPr')
    if pPr is not None:
        if pPr.find(A + 'buNone') is not None:
            return 'none'
        if pPr.find(A + 'buAutoNum') is not None:
            return 'num'
        if pPr.find(A + 'buChar') is not None or pPr.find(A + 'buBlip') is not None:
            return 'bullet'
    return default


def text_block(sh, default_bullet):
    paras = []
    for p in sh.text_frame.paragraphs:
        md = para_md(p)
        if not md:
            continue
        cur = {'level': p.level, 'md': md, 'kind': bullet_kind(p, default_bullet)}
        prev = paras[-1] if paras else None
        if (prev and prev['kind'] == 'none' and cur['kind'] == 'none'
                and not re.search(r'[.!?:)]\**$', prev['md']) and re.match(r'[a-z(~0-9]', cur['md'])):
            prev['md'] += ' ' + cur['md']  # manual line wrap in the original
            continue
        paras.append(cur)
    return paras


def render_paras(paras, start_counts=None):
    """paragraph dicts -> markdown lines. start_counts lets a continued list keep numbering."""
    lines, counters = [], dict(start_counts or {})
    prev_list_level = -1
    for p in paras:
        if p['kind'] == 'none':
            if lines and prev_list_level >= 0:
                lines.append('')
            lines.append(p['md'])
            lines.append('')
            prev_list_level = -1
            continue
        lvl = min(p['level'], prev_list_level + 1)
        for k in list(counters):
            if k > lvl:
                del counters[k]
        indent = '   ' * lvl
        if p['kind'] == 'num':
            counters[lvl] = counters.get(lvl, 0) + 1
            lines.append(f"{indent}{counters[lvl]}. {p['md']}")
        else:
            counters.pop(lvl, None)
            lines.append(f"{indent}- {p['md']}")
        prev_list_level = lvl
    return lines, counters


# ---------- images ----------
_wmf_queue = []


def save_blob(blob, ext, name, crop=None):
    if ext in ('wmf', 'emf'):
        raw = os.path.join(OUT, '.cache', 'wmf', name + '.' + ext)
        os.makedirs(os.path.dirname(raw), exist_ok=True)
        open(raw, 'wb').write(blob)
        _wmf_queue.append((raw, name, crop))
        return f'/img/{name}.png'
    im = Image.open(io.BytesIO(blob))
    if crop:
        im = apply_crop(im, crop)
    ext = 'jpg' if ext in ('jpg', 'jpeg') else 'png'
    if ext == 'jpg':
        im.convert('RGB').save(os.path.join(IMG, f'{name}.jpg'), quality=88)
    else:
        im.save(os.path.join(IMG, f'{name}.png'))
    return f'/img/{name}.{ext}'


def apply_crop(im, crop):
    l, t, r, b = crop
    w, h = im.size
    box = (int(w * l), int(h * t), int(w * (1 - r)), int(h * (1 - b)))
    if box[2] - box[0] > 4 and box[3] - box[1] > 4:
        im = im.crop(box)
    return im


def flush_wmf():
    if not _wmf_queue:
        return
    rawdir = os.path.dirname(_wmf_queue[0][0])
    subprocess.run(['soffice', '--headless', '--convert-to', 'svg', '--outdir', rawdir]
                   + [q[0] for q in _wmf_queue], capture_output=True, timeout=600)
    for raw, name, crop in _wmf_queue:
        svg = os.path.splitext(raw)[0] + '.svg'
        png = os.path.join(IMG, name + '.png')
        subprocess.run(['rsvg-convert', '-w', '2000', svg, '-o', png], check=True)
        subprocess.run(['convert', png, '-trim', '+repage', png], check=True)
        if crop and any(crop):
            apply_crop(Image.open(png), crop).save(png)


def crop_ref(idx, box, name):
    im = Image.open(refs[idx - 1])
    W, H = im.size
    l, t, r, b = box
    pad = 10
    px = (max(0, int(l / SW * W) - pad), max(0, int(t / SH * H) - pad),
          min(W, int(r / SW * W) + pad), min(H, int(b / SH * H) + pad))
    im.crop(px).save(os.path.join(IMG, name + '.png'))
    return f'/img/{name}.png'


# ---------- slide model ----------
def bbox(sh):
    return (sh.left or 0, sh.top or 0, (sh.left or 0) + (sh.width or 0), (sh.top or 0) + (sh.height or 0))


def union(boxes):
    return (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))


def inside(b, region, slack=0.15):
    w, h = b[2] - b[0], b[3] - b[1]
    ix = max(0, min(b[2], region[2]) - max(b[0], region[0]))
    iy = max(0, min(b[3], region[3]) - max(b[1], region[1]))
    return w > 0 and h > 0 and (ix * iy) / (w * h) > 1 - slack


def is_pic(sh):
    return sh.shape_type == MSO_SHAPE_TYPE.PICTURE or (sh.is_placeholder and sh._element.tag.endswith('}pic'))


def model(idx, slide):
    m = {'idx': idx, 'hidden': slide._element.get('show') == '0', 'title': '', 'blocks': [],
         'pics': [], 'complex': [], 'notes': '', 'subtitle': [], 'title_box': None, 'altboxes': []}
    # shapes wrapped in mc:AlternateContent (OMML equations) are invisible to python-pptx
    for el in slide.shapes._spTree:
        if el.tag.endswith('}AlternateContent'):
            xf = el.find('.//' + A + 'xfrm')
            off = xf.find(A + 'off') if xf is not None else None
            ext = xf.find(A + 'ext') if xf is not None else None
            if off is not None and ext is not None:
                x, y = int(off.get('x')), int(off.get('y'))
                m['altboxes'].append((x, y, x + int(ext.get('cx')), y + int(ext.get('cy'))))
    for sh in slide.shapes:
        ph = sh.placeholder_format.type if sh.is_placeholder else None
        if ph in TITLE_TYPES and sh.has_text_frame:
            m['title'] = ' '.join(para_md(p) for p in sh.text_frame.paragraphs if p.text.strip())
            m['title_box'] = bbox(sh)
            continue
        if (sh.shape_type == MSO_SHAPE_TYPE.TEXT_BOX and sh.has_text_frame
                and 0 < len(sh.text_frame.text.strip()) <= 12):
            m.setdefault('labels', []).append(sh)  # maybe a diagram label; decided below
            continue
        if is_pic(sh):
            m['pics'].append(sh)
        elif sh.shape_type in COMPLEX and not (sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE and sh.has_text_frame
                                                and len(sh.text_frame.text) > 120):
            m['complex'].append(sh)
        elif sh.has_text_frame and sh.text_frame.text.strip():
            default = 'bullet' if (sh.is_placeholder and ph in (PP_PLACEHOLDER.BODY, PP_PLACEHOLDER.OBJECT, None)
                                   and sh.shape_type == MSO_SHAPE_TYPE.PLACEHOLDER) else 'none'
            if ph == PP_PLACEHOLDER.SUBTITLE:
                default = 'none'
            m['blocks'].append({'box': bbox(sh), 'paras': text_block(sh, default)})
    graphic = [bbox(x) for x in m['pics'] + m['complex']]
    for sh in m.pop('labels', []):
        if any(near(bbox(sh), g, 0.015) for g in graphic):
            m['complex'].append(sh)
        else:
            m['blocks'].append({'box': bbox(sh), 'paras': text_block(sh, 'none')})
    if slide.has_notes_slide:
        tf = slide.notes_slide.notes_text_frame
        m['notes'] = tf.text.strip() if tf is not None else ''
    m['blocks'].sort(key=lambda b: (b['box'][1], b['box'][0]))
    return m


def pic_sig(sh):
    return hashlib.md5(sh.image.blob).hexdigest()[:10] + str(bbox(sh))


def signature(m):
    return (m['title'], tuple(sorted(pic_sig(p) for p in m['pics'])), len(m['complex']), len(m['blocks']), m['hidden'])


def is_prefix(a, b):
    if len(a['blocks']) != len(b['blocks']):
        return False
    grew = False
    for x, y in zip(a['blocks'], b['blocks']):
        px, py = [p['md'] for p in x['paras']], [p['md'] for p in y['paras']]
        if py[:len(px)] != px:
            return False
        grew |= len(py) > len(px)
    return grew


# ---------- emit ----------
def overlap_frac(b, region):
    w, h = b[2] - b[0], b[3] - b[1]
    ix = max(0, min(b[2], region[2]) - max(b[0], region[0]))
    iy = max(0, min(b[3], region[3]) - max(b[1], region[1]))
    return (ix * iy) / (w * h) if w > 0 and h > 0 else 0


def near(a, b, gap=0.03):
    g = gap * SW
    return not (a[2] + g < b[0] or b[2] + g < a[0] or a[3] + g < b[1] or b[3] + g < a[1])


def place_figures(m, name):
    """Return list of (box, src). Drawn shapes, labels and touching pictures become one crop
    from the reference render; free-standing pictures keep their original files."""
    figs = []
    pics = list(m['pics'])
    cluster = [bbox(s) for s in m['complex']]
    if not cluster:
        # pictures that touch each other form a composite (trees of maps, etc.)
        pb = [bbox(p) for p in pics]
        for i in range(len(pb)):
            for j in range(i + 1, len(pb)):
                if near(pb[i], pb[j], 0.01):
                    cluster = [pb[i], pb[j]]
                    break
            if cluster:
                break
    if cluster:
        changed = True
        while changed:
            changed = False
            for p in pics:
                b = bbox(p)
                if b not in cluster and near(b, union(cluster), 0.02):
                    cluster.append(b)
                    changed = True
        region = list(union(cluster))
        if m['title_box']:
            region[1] = max(region[1], m['title_box'][3])
        region = tuple(region)
        absorbed = [b for b in m['blocks'] if overlap_frac(b['box'], region) > 0.85
                    and sum(len(p['md']) for p in b['paras']) < 40]  # only short labels melt into figures
        for b in absorbed:
            m['blocks'].remove(b)
        # body text that only partly overlaps the drawing: trim the crop so the text isn't duplicated
        region = list(region)
        for b in m['blocks']:
            bb = b['box']
            if overlap_frac(bb, tuple(region)) > 0 and (min(bb[2], region[2]) - max(bb[0], region[0])) > 0.4 * (region[2] - region[0]):
                if (bb[1] + bb[3]) / 2 < (region[1] + region[3]) / 2:
                    # text sits above the drawing; estimate where its text actually ends
                    lines = sum(1 + len(re.sub(r'<[^>]+>', '', p['md'])) // 95 for p in b['paras'])
                    text_bottom = bb[1] + min(bb[3] - bb[1], int(lines * 0.055 * SH))
                    new = (region[0], max(region[1], text_bottom), region[2], region[3])
                else:
                    new = (region[0], region[1], region[2], min(region[3], bb[1]))
                if new[3] - new[1] > 0.25 * (region[3] - region[1]):
                    region = list(new)
        region = tuple(region)
        pics = [p for p in pics if overlap_frac(bbox(p), region) < 0.5]
        figs.append((region, crop_ref(m['idx'], region, f'{name}-fig')))
    for k, p in enumerate(pics):
        crop = (p.crop_left, p.crop_top, p.crop_right, p.crop_bottom)
        figs.append((bbox(p), save_blob(p.image.blob, p.image.ext, f'{name}-{k}', crop if any(crop) else None)))
    for k, b in enumerate(m['altboxes']):
        figs.append((b, crop_ref(m['idx'], b, f'{name}-math{k}')))
    return figs


def img_tag(src, box, mode):
    w = (box[2] - box[0]) / SW
    h = (box[3] - box[1]) / SH
    if mode == 'split':
        return f'<img src="{src}" class="fig" style="max-height:{min(400, int(h * 552 * 1.15))}px" />'
    return f'<img src="{src}" class="fig" style="width:{int(w * 980 * 0.95)}px;max-height:{int(min(h, 0.62) * 552)}px" />'


def text_lines(m, reveal=None):
    """reveal: list per block of [n_initial, n_after_click1, ...] paragraph counts."""
    out = []
    for bi, b in enumerate(m['blocks']):
        paras = b['paras']
        if not reveal:
            lines, _ = render_paras(paras)
            out += lines
        else:
            steps = reveal[bi]
            lines, counters = render_paras(paras[:steps[0]])
            out += lines
            for s0, s1 in zip(steps, steps[1:]):
                if s1 == s0:
                    continue
                more, counters = render_paras(paras[s0:s1], counters)
                out += ['', '<div v-click>', ''] + more + ['', '</div>']
        out.append('')
    return out


def text_chars(m):
    return sum(len(re.sub(r'<[^>]+>', '', p['md'])) + 30 * p['level'] for b in m['blocks'] for p in b['paras'])


def emit(m, reveal=None, merged=()):
    idx = m['idx']
    name = f's{idx:02d}'
    fm = {}
    if m['hidden']:
        fm['hide'] = 'true'
    body = []
    figs = place_figures(m, name)
    chars = text_chars(m)
    title = m['title'] or ''
    if idx == 1:
        fm['layout'] = 'cover'
        fm['kicker'] = KICKER
        sub = [p['md'] for b in m['blocks'] for p in b['paras']]
        plain = re.sub(r'<(?!br)[^>]+>|\*\*', '', title)
        parts = [t.strip() for t in re.split(r'<br>', plain) if t.strip()]
        if len(parts) == 1:  # "Artificial intelligenceCONSTRAINT REASONING" style run-together titles
            mm = re.match(r'(.*?[a-z])([A-Z][A-Z ]+)$', parts[0])
            parts = [mm.group(1), mm.group(2)] if mm else parts
        cap = lambda x: x if not x.isupper() and not x.islower() else x.title()
        body = [f"# {cap(parts[-1])}", '', cap(parts[0]) if len(parts) > 1 else '', '']
        body += ['<small>' + ' · '.join(sub) + '</small>']
        return fm, body
    head = [f"# {title}", ''] if title else []
    if not figs:
        body = head + text_lines(m, reveal)
    else:
        fu = union([f[0] for f in figs])
        side = fu[0] > 0.36 * SW or fu[2] < 0.62 * SW
        if m['blocks'] and side and chars > 0:
            fm['layout'] = 'split'
            if fu[2] < 0.58 * SW:
                fm['flip'] = 'true'
            figmd = [img_tag(src, box, 'split') for box, src in figs]
            fig_side = lambda b: ((b['box'][0] + b['box'][2]) / 2 < 0.5 * SW) == bool(fm.get('flip'))
            caps = [b for b in m['blocks'] if fig_side(b) and len(m['blocks']) > 1]
            main = [b for b in m['blocks'] if b not in caps]
            rmain = [reveal[m['blocks'].index(b)] for b in main] if reveal else None
            capmd = ['', '<div class="caption">', ''] + text_lines(dict(m, blocks=caps)) + ['</div>'] if caps else []
            body = head + ['::left::', ''] + text_lines(dict(m, blocks=main), rmain) + ['::right::', ''] + figmd + capmd
        else:
            above = [b for b in m['blocks'] if b['box'][1] < fu[1]]
            figmd = ['<div class="figs">'] + [img_tag(src, box, 'flow') for box, src in figs] + ['</div>', '']
            m2_above = dict(m, blocks=above)
            m2_below = dict(m, blocks=[b for b in m['blocks'] if b not in above])
            r_above = [reveal[m['blocks'].index(b)] for b in above] if reveal else None
            r_below = [reveal[m['blocks'].index(b)] for b in m2_below['blocks']] if reveal else None
            body = head + text_lines(m2_above, r_above) + figmd + text_lines(m2_below, r_below)
    # density -> zoom (first guess; verified by render)
    cap = 520 if fm.get('layout') == 'split' else 900
    if figs and fm.get('layout') != 'split':
        cap = 420
    if chars > cap:
        fm['zoom'] = f"{max(0.62, round((cap / chars) ** 0.5, 2))}"
    return fm, body


def notes_md(texts):
    seen, out = set(), []
    for t in texts:
        for line in t.splitlines():
            line = line.strip()
            if line and line not in seen:
                seen.add(line)
                out.append(esc(line).replace('--', '&#8209;&#8209;'))
    return '\n\n'.join(out)


models = [model(i, s) for i, s in enumerate(prs.slides, 1)]

# merge runs of "build" slides (same title/figures, text grows by appending)
groups, cur = [], [models[0]]
for m in models[1:]:
    last = cur[-1]
    if signature(m) == signature(last) and is_prefix(last, m):
        cur.append(m)
    else:
        groups.append(cur)
        cur = [m]
groups.append(cur)

chunks, report = [], []
for g in groups:
    final = g[-1]
    reveal = None
    if len(g) > 1:
        reveal = [[len(s['blocks'][bi]['paras']) for s in g] for bi in range(len(final['blocks']))]
        report.append(f"merged slides {g[0]['idx']}-{final['idx']} into one with {len(g) - 1} clicks")
    ov = os.path.join(OUT, 'overrides', f"s{g[0]['idx']:02d}.md")
    if os.path.exists(ov):
        emit(final, reveal)  # still extract this slide's images; the override can reference them
        txt = open(ov).read().strip()
        mm = re.match(r'^---\n(.*?)\n---\n(.*)$', txt, re.S)
        fmtxt, md = (mm.group(1), mm.group(2).strip()) if mm else ('', txt)
        if final['hidden'] and 'hide:' not in fmtxt:
            fmtxt = ('hide: true\n' + fmtxt).strip()
        chunks.append((fmtxt, f"<!-- source: slide {g[0]['idx']} (override) -->\n\n" + md))
        report.append(f"slide {g[0]['idx']}: override")
        continue
    fm, body = emit(final, reveal)
    if final['altboxes']:
        report.append(f"slide {final['idx']}: OMML math cropped as image; write an override")
    src_note = f"<!-- source: slide {g[0]['idx']}" + (f"-{final['idx']}" if len(g) > 1 else '') + ' -->'
    notes = notes_md([s['notes'] for s in g])
    fmtxt = '\n'.join(f'{k}: {v}' for k, v in fm.items())
    md = '\n'.join(body).strip()
    md = re.sub(r'\n{3,}', '\n\n', md)
    chunks.append((fmtxt, src_note + '\n\n' + md + ('\n\n<!--\n' + notes + '\n-->' if notes else '')))
flush_wmf()
import shutil
for f in glob.glob(os.path.join(OUT, 'overrides', 'img', '*')):
    shutil.copy(f, IMG)  # hand-made assets used by overrides

head = f"""---
theme: drexel
title: "{TITLE}"
aspectRatio: 16/9
canvasWidth: 980
"""
out = []
for i, (fmtxt, md) in enumerate(chunks):
    if i == 0:
        out.append(head + fmtxt + '\n---\n\n' + md)
    else:
        out.append(('---\n' + fmtxt + '\n---\n\n' if fmtxt else '---\n\n') + md)
open(os.path.join(OUT, 'slides.md'), 'w').write('\n\n'.join(out) + '\n')
print('unmapped symbol chars:', UNMAPPED or 'none')
print(f"{len(models)} source slides -> {len(chunks)} Slidev slides")
print('\n'.join(report))
