# 用法：python3 tools/make-icon.py <來源 PNG（正方形、不透明、1024 以上）>
# 從一張插畫切出加入主畫面要的各種尺寸：1024（留存）、512、192、180（apple-touch）與 maskable-512
# maskable：Android 會用圓形／圓角遮罩裁掉邊緣，所以整張圖縮到 78% 放在同色系的漸層底上，字才不會被切到
import sys, os
from PIL import Image
src = sys.argv[1]; root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); out = os.path.join(root, 'assets', 'icon'); os.makedirs(out, exist_ok=True)
im = Image.open(src).convert('RGB'); assert im.size[0] == im.size[1], '要正方形'
big = im.resize((1024, 1024), Image.LANCZOS); big.save(os.path.join(out, 'icon-1024.png'), optimize=True)
for n in (512, 192, 180): big.resize((n, n), Image.LANCZOS).save(os.path.join(out, f'icon-{n}.png'), optimize=True)
# maskable：底是圖上半夜空拉開模糊後的版本（邊緣顏色自然接上、不會有黃字糊成一團），中間貼 78% 的圖，邊緣用圓角羽化
from PIL import ImageFilter, ImageDraw
bg = big.crop((0, 0, 1024, 440)).resize((512, 512), Image.LANCZOS).filter(ImageFilter.GaussianBlur(24))   # 只取上面的夜空（沒有字）拉成底，模糊後是柔和的藍色漸層
inner = big.resize((400, 400), Image.LANCZOS)
mask = Image.new('L', (400, 400), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, 399, 399), radius=70, fill=255); mask = mask.filter(ImageFilter.GaussianBlur(3))
bg.paste(inner, (56, 56), mask); bg.save(os.path.join(out, 'maskable-512.png'), optimize=True)
print('ok', os.listdir(out))
