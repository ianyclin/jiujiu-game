#!/usr/bin/env python3
"""把 Google Fonts 倉庫的字型切成遊戲用的子集（woff2），放進 assets/fonts。
用法：python3 tools/make-fonts.py <來源目錄>
來源目錄要有 ChironGoRoundTC[wght].ttf（可變字型）與 LilitaOne-Regular.ttf，
下載自 https://github.com/google/fonts/tree/main/ofl/chirongoroundtc 與 ofl/lilitaone。
需要 pip install fonttools brotli。改了 index.html 的文字之後要重跑一次（新字才會有）。
"""
import sys, os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset
src = sys.argv[1]; root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); out = os.path.join(root, 'assets', 'fonts'); os.makedirs(out, exist_ok=True)
html = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
chars = set(html)
chars |= set('0123456789+−×÷=？?！!，。、：；「」（）〈〉《》…・·★☆♥✓✕～~%/-–—′″℃ 　')
chars |= set(chr(c) for c in range(0x20, 0x7f)) | set(chr(c) for c in range(0xff01, 0xff5f))
text = ''.join(sorted(c for c in chars if c >= ' ' and c not in '  '))
print('chars', len(text), 'cjk', sum(1 for c in text if '一' <= c <= '鿿'))
def sub(path, dst, text):
    o = subset.Options(); o.flavor = 'woff2'; o.layout_features = ['*']; o.name_IDs = ['*']; o.notdef_outline = True; o.hinting = False; o.desubroutinize = True
    f = TTFont(path); ss = subset.Subsetter(o); ss.populate(text=text); ss.subset(f); f.flavor = 'woff2'; f.save(dst); print(dst, os.path.getsize(dst))
vf = TTFont(os.path.join(src, 'ChironGoRoundTC[wght].ttf'))
for w in (400, 700, 900):
    inst = instancer.instantiateVariableFont(vf, {'wght': w}, inplace=False, updateFontNames=False)
    tmp = os.path.join(out, f'chiron-{w}.tmp.ttf'); inst.save(tmp); sub(tmp, os.path.join(out, f'chiron-{w}.woff2'), text); os.remove(tmp)
sub(os.path.join(src, 'LilitaOne-Regular.ttf'), os.path.join(out, 'lilita.woff2'), ''.join(chr(c) for c in range(0x20, 0x7f)) + '×−＋？！：・…')
