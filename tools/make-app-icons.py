#!/usr/bin/env python3
"""從 assets/icon/icon-1024.png 產生原生 app 要用的圖示與啟動畫面（ios/、android/ 底下）。
用法：python3 tools/make-app-icons.py（icon-1024.png 要先用 tools/make-icon.py 產生）
- iOS：AppIcon 1024（App Store 不接受透明，轉成不透明 RGB）、啟動畫面（夜空底色＋圖示置中）
- Android：legacy 方形與圓形圖示、adaptive 圖示的前景與背景（可見範圍是中間 72/108，所以圖縮到 66%）、啟動畫面圖示
需要 pip install pillow。"""
import os
from PIL import Image, ImageDraw, ImageFilter

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = Image.open(os.path.join(root, 'assets', 'icon', 'icon-1024.png')).convert('RGB')
NIGHT = (8, 17, 31)   # 與 index.html 的 --ink（#08111f）一致

def save(img, *parts):
    p = os.path.join(root, *parts); os.makedirs(os.path.dirname(p), exist_ok=True); img.save(p, optimize=True); print(p, img.size, img.mode)

# --- iOS ---
save(src, 'ios', 'App', 'App', 'Assets.xcassets', 'AppIcon.appiconset', 'AppIcon-512@2x.png')   # RGB、無 alpha
# 啟動畫面：純夜空底色＋圖示置中（scaleAspectFill，所以只有中間是圖；一張圖三個倍率共用）
splash = Image.new('RGB', (1366, 1366), NIGHT)
logo = src.resize((360, 360), Image.LANCZOS)
m = Image.new('L', (360, 360), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 359, 359), radius=76, fill=255)
splash.paste(logo, ((1366 - 360) // 2, (1366 - 360) // 2), m)
sd = os.path.join('ios', 'App', 'App', 'Assets.xcassets', 'Splash.imageset')
for old in os.listdir(os.path.join(root, sd)):
    if old.endswith('.png'): os.remove(os.path.join(root, sd, old))
save(splash, sd, 'splash.png')
open(os.path.join(root, sd, 'Contents.json'), 'w').write('''{
  "images" : [
    { "idiom" : "universal", "filename" : "splash.png", "scale" : "1x" },
    { "idiom" : "universal", "filename" : "splash.png", "scale" : "2x" },
    { "idiom" : "universal", "filename" : "splash.png", "scale" : "3x" }
  ],
  "info" : { "version" : 1, "author" : "xcode" }
}
''')

# --- Android ---
res = os.path.join('android', 'app', 'src', 'main', 'res')
sky = src.crop((0, 0, 1024, 440)).resize((1024, 1024), Image.LANCZOS).filter(ImageFilter.GaussianBlur(48))   # 同 make-icon.py 的 maskable：只取上面的夜空，模糊成底
def rounded(img, radius_frac):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, img.size[0] - 1, img.size[1] - 1), radius=int(img.size[0] * radius_frac), fill=255)
    out = img.convert('RGBA'); out.putalpha(m.filter(ImageFilter.GaussianBlur(1))); return out
DENS = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}
for d, k in DENS.items():
    legacy = int(48 * k); full = int(108 * k)
    save(rounded(src.resize((legacy, legacy), Image.LANCZOS), 0.18), res, f'mipmap-{d}', 'ic_launcher.png')
    c = Image.new('L', (legacy * 4, legacy * 4), 0); ImageDraw.Draw(c).ellipse((0, 0, legacy * 4 - 1, legacy * 4 - 1), fill=255)
    rd = src.resize((legacy, legacy), Image.LANCZOS).convert('RGBA'); rd.putalpha(c.resize((legacy, legacy), Image.LANCZOS))
    save(rd, res, f'mipmap-{d}', 'ic_launcher_round.png')
    save(sky.resize((full, full), Image.LANCZOS), res, f'mipmap-{d}', 'ic_launcher_background.png')
    fg = Image.new('RGBA', (full, full), (0, 0, 0, 0)); inner = int(full * 0.66)
    fg.paste(rounded(src.resize((inner, inner), Image.LANCZOS), 0.16), ((full - inner) // 2, (full - inner) // 2))
    save(fg, res, f'mipmap-{d}', 'ic_launcher_foreground.png')
