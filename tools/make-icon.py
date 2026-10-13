# 用法：python3 tools/make-icon.py <來源 PNG（正方形、不透明、1024 以上）>
# 從一張插畫切出加入主畫面要的各種尺寸：1024（留存）、512、192、180（apple-touch）與 maskable-512
# maskable：Android 會用圓形／圓角遮罩裁掉邊緣，所以整張圖縮到 78% 放在同色系的漸層底上，字才不會被切到
import sys, os
from PIL import Image
src = sys.argv[1]; root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); out = os.path.join(root, 'assets', 'icon'); os.makedirs(out, exist_ok=True)
im = Image.open(src).convert('RGB'); assert im.size[0] == im.size[1], '要正方形'
big = im.resize((1024, 1024), Image.LANCZOS); big.save(os.path.join(out, 'icon-1024.png'), optimize=True)
for n in (512, 192, 180): big.resize((n, n), Image.LANCZOS).save(os.path.join(out, f'icon-{n}.png'), optimize=True)
# maskable：上下各取圖的邊緣顏色做漸層底
top, bot = im.getpixel((im.size[0] // 2, 2)), im.getpixel((im.size[0] // 2, im.size[1] - 3))
m = Image.new('RGB', (512, 512))
px = m.load()
for y in range(512):
    t = y / 511; c = tuple(round(top[i] * (1 - t) + bot[i] * t) for i in range(3))
    for x in range(512): px[x, y] = c
inner = big.resize((400, 400), Image.LANCZOS); m.paste(inner, (56, 56)); m.save(os.path.join(out, 'maskable-512.png'), optimize=True)
print('ok', os.listdir(out))
