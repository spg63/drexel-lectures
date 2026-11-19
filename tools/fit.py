"""Measure every slide in a headless browser and set `zoom` only where content overflows.

usage: python3 fit.py deck_dir   (run after convert.py; rewrites deck_dir/slides.md in place)
"""
import json, os, re, subprocess, sys, time, math, signal

DECK = sys.argv[1]
SRC = os.path.join(DECK, 'slides.md')
MEAS = os.path.join(DECK, '_measure.md')
TOOLS = os.path.dirname(os.path.abspath(__file__))
PORT = 3031
MIN_ZOOM = 0.6

text = open(SRC).read()
# pieces[i] ends with slide i's frontmatter; pieces[i+1] starts with its body
pieces = re.split(r'(?m)^(?=<!-- source:)', text)


def strip_keys(piece, keys):
    return re.sub(r'(?m)^(%s): .*\n' % '|'.join(keys), '', piece)


def set_zoom(piece, z):
    piece = re.sub(r'---\n---\n\n$', '---\n\n', strip_keys(piece, ['zoom']))
    if z is None:
        return piece
    keyed = re.search(r'---\n((?:[A-Za-z]\w*: [^\n]*\n)+)---\n\n$', piece)
    if keyed:
        return piece[:keyed.end(1)] + f'zoom: {z}\n---\n\n'
    return re.sub(r'---\n\n$', f'---\nzoom: {z}\n---\n\n', piece)


def measure(pieces_for_run, count):
    open(MEAS, 'w').write(''.join(pieces_for_run))
    srv = subprocess.Popen(['npx', 'slidev', os.path.basename(MEAS), '--port', str(PORT)], cwd=DECK,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    try:
        time.sleep(10)
        res = subprocess.run(['node', os.path.join(TOOLS, 'measure.mjs'), f'http://localhost:{PORT}/#', str(count)],
                             cwd=DECK, capture_output=True, text=True, timeout=900)
        return json.loads(res.stdout)
    finally:
        os.killpg(srv.pid, signal.SIGTERM)
        time.sleep(1)


# pass 1: measure everything unzoomed and unhidden
base = [strip_keys(p, ['zoom', 'hide']) for p in pieces]
base = [set_zoom(p, None) for p in base]
n = len(pieces) - 1
results = measure(base, n)
zooms = {}
for r in results:
    if not r or r.get('height') is None:
        continue
    ratio = max(r['height'] / r['canvasH'], r['width'] / r['canvasW'])
    if ratio > 1.01:
        zooms[r['n']] = max(MIN_ZOOM, math.floor(100 / ratio) / 100)

# write zooms into the real file (hidden flags preserved)
out = list(pieces)
for i in range(1, n + 1):
    out[i - 1] = set_zoom(out[i - 1], zooms.get(i))
open(SRC, 'w').write(''.join(out))
os.remove(MEAS)
tight = {k: v for k, v in zooms.items() if v <= MIN_ZOOM}
print(f'{len(zooms)} slides zoomed; floor hit (still overflowing, needs a split or edit): {sorted(tight)}')
print(json.dumps({k: v for k, v in sorted(zooms.items())}))
