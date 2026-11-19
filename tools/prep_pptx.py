"""Prepare a PPTX for conversion.

usage: python3 prep_pptx.py deck.pptx cache_dir
writes:
  cache_dir/clean.pptx     ink removed, hidden slides still hidden (the converter's input)
  cache_dir/all.pptx       ink removed, every slide visible (for the reference render)
  cache_dir/ref/s-NN.png   one 1920x1080 reference image per slide, used to crop drawn diagrams
needs: python-pptx, LibreOffice (soffice), poppler (pdftoppm)
"""
import os, shutil, subprocess, sys, glob
from pptx import Presentation

src, cache = sys.argv[1], sys.argv[2]
os.makedirs(cache, exist_ok=True)


def strip_ink(prs, unhide):
    removed = 0
    for s in prs.slides:
        if unhide and s._element.get('show') == '0':
            del s._element.attrib['show']
        tree = s.shapes._spTree
        for el in list(tree.iter()):
            if el.tag.endswith('}contentPart'):  # PowerPoint ink
                node = el
                while node.getparent() is not None and node.getparent() is not tree:
                    node = node.getparent()
                if node.getparent() is tree:
                    tree.remove(node)
                    removed += 1
    return removed


p = Presentation(src)
n = strip_ink(p, unhide=False)
p.save(os.path.join(cache, 'clean.pptx'))
p = Presentation(src)
strip_ink(p, unhide=True)
p.save(os.path.join(cache, 'all.pptx'))
print(f'removed {n} ink objects')

subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', cache, os.path.join(cache, 'all.pptx')],
               check=True, capture_output=True, timeout=900)
ref = os.path.join(cache, 'ref')
shutil.rmtree(ref, ignore_errors=True)
os.makedirs(ref)
subprocess.run(['pdftoppm', '-r', '144', '-png', os.path.join(cache, 'all.pdf'), os.path.join(ref, 's')], check=True)
print(f'rendered {len(glob.glob(os.path.join(ref, "*.png")))} reference slides')
