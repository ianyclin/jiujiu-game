"""把稀有配件圖（左右各一樣、白底）切成兩張透明 PNG：assets/gear/wings.png、assets/gear/bubble.png。

用法：python3 tools/cut-rare.py <來源圖.png>
泡泡裡面的淡色會改成半透明，遊戲裡才看得出寵物在泡泡裡。印出寬高比給 GEAR 表的 ar。
"""
import sys, os, json
import numpy as np
from PIL import Image
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'gear') + '/'

# 直接重用 cut-gear 的去背（不執行它的主程式）
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cut-gear.py'), encoding='utf-8').read()
ns = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cut-gear.py')}; exec(src[:src.index('img = remove_bg(')], ns); remove_bg = ns['remove_bg']

img = remove_bg(Image.open(sys.argv[1]))
al = np.asarray(img)[:, :, 3] > 0
cnt = al.sum(axis=0); mid = img.width // 2
# 在中間附近找最空的一欄當切點
lo, hi = int(img.width * 0.35), int(img.width * 0.65)
cut = lo + int(np.argmin(cnt[lo:hi]))
meta = {}
for gid, box in (('wings', (0, 0, cut, img.height)), ('bubble', (cut, 0, img.width, img.height))):
    sub = img.crop(box); sub = sub.crop(sub.getbbox())
    if gid == 'bubble':   # 泡泡：淡色區域半透明，邊框、星星、反光保留
        a = np.asarray(sub).copy(); rgb = a[:, :, :3].astype(int)
        pale = (rgb.min(axis=2) >= 170) & (rgb.max(axis=2) - rgb.min(axis=2) <= 60)
        a[:, :, 3] = np.where(pale & (a[:, :, 3] > 0), np.minimum(a[:, :, 3], 110), a[:, :, 3])
        sub = Image.fromarray(a, 'RGBA')
    k = 512 / max(sub.size); sub = sub.resize((round(sub.width * k), round(sub.height * k)), Image.LANCZOS)
    sub.quantize(256).save(f'{OUT}{gid}.png', optimize=True)
    meta[gid] = round(sub.width / sub.height, 3); print(gid, sub.size)
print(json.dumps(meta))
