// 產生「加入主畫面」的圖示：用 Playwright 把一段 SVG 畫成 1024px PNG，再縮成各尺寸。
// 用法：node tools/make-icon.js（需要 playwright 與 python3 + Pillow）。改設計就改下面的 SVG。
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const root = path.resolve(__dirname, '..');
const stars = [[120,160,6],[300,90,4],[860,140,5],[930,420,4],[90,540,4],[200,880,5],[700,930,4],[880,760,6],[520,130,3],[420,960,3],[980,640,3],[60,340,3]];
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <radialGradient id="sky" cx="50%" cy="38%" r="75%"><stop offset="0" stop-color="#1b3358"/><stop offset=".6" stop-color="#0e1d33"/><stop offset="1" stop-color="#07101e"/></radialGradient>
    <linearGradient id="tail" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset=".55" stop-color="#ffd23f" stop-opacity=".85"/><stop offset="1" stop-color="#ffae57"/></linearGradient>
    <radialGradient id="rock" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#b98a68"/><stop offset="1" stop-color="#5b4a5f"/></radialGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="22"/></filter>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>
  <rect width="1024" height="1024" fill="url(#sky)"/>
  ${stars.map(([x,y,r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" opacity=".9"/>`).join('')}
  <circle cx="880" cy="220" r="150" fill="#ffd23f" opacity=".22" filter="url(#glow)"/><circle cx="880" cy="220" r="46" fill="#fff1cf"/><circle cx="866" cy="208" r="9" fill="#e9d7b0"/><circle cx="896" cy="232" r="7" fill="#e9d7b0"/>
  <path d="M150 150 L715 470" stroke="url(#tail)" stroke-width="70" stroke-linecap="round" opacity=".95"/>
  <path d="M190 112 L700 430" stroke="#fff" stroke-width="14" stroke-linecap="round" opacity=".55"/>
  <circle cx="755" cy="500" r="120" fill="#ffae57" opacity=".45" filter="url(#soft)"/>
  <circle cx="755" cy="500" r="100" fill="url(#rock)" stroke="#ffd9a8" stroke-width="12"/>
  <circle cx="720" cy="470" r="18" fill="#3f3148" opacity=".8"/><circle cx="790" cy="530" r="24" fill="#3f3148" opacity=".8"/><circle cx="765" cy="450" r="10" fill="#3f3148" opacity=".7"/>
  <text x="512" y="880" text-anchor="middle" font-family="'Chiron GoRound TC'" font-weight="900" font-size="420" fill="#ffd23f" stroke="#a87a00" stroke-width="10" paint-order="stroke" style="letter-spacing:-.04em">九九</text>
  <text x="512" y="880" text-anchor="middle" font-family="'Chiron GoRound TC'" font-weight="900" font-size="420" fill="#ffd23f" style="letter-spacing:-.04em">九九</text>
</svg>`;
const html = `<!doctype html><meta charset="utf-8"><style>@font-face{font-family:'Chiron GoRound TC';font-weight:900;src:url(file://${root}/assets/fonts/chiron-900.woff2) format('woff2')}html,body{margin:0;background:#000}</style>${svg}`;
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1024, height: 1024 } });
  await pg.setContent(html); await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(300);
  const out = path.join(root, 'assets', 'icon', 'icon-1024.png');
  await pg.screenshot({ path: out, clip: { x: 0, y: 0, width: 1024, height: 1024 } });
  await b.close(); console.log('wrote', out);
})();
