// App Store「標題和搜尋結果」素材：把 store/creative/header.html 轉成 5244 × 2950 的 PNG（不透明）。
// 用法：node tools/make-header.cjs   → store/creative/header-5244x2950.png
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 5244, height: 2950 }, deviceScaleFactor: 1 })).newPage();
  await p.goto('file://' + path.resolve(__dirname, '../store/creative/header.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  await p.screenshot({ path: path.resolve(__dirname, '../store/creative/header-5244x2950.png'), omitBackground: false });
  await b.close();
})();
