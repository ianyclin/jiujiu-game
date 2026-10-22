#!/usr/bin/env node
// 商店截圖：用 Playwright 開真的遊戲（index.html 原封不動），種一份好看的存檔，依各商店的尺寸截出五張：
// 主選單、流星防衛戰、星圖、寵物、拔河。三種語言各一套。輸出 store/screenshots/<裝置>/<語言>/<n>-<名>.jpg
// （JPEG：Apple 不收有透明度的圖，JPEG 沒有 alpha；檔案也小。）
//
// 用法：
//   npm i --no-save playwright      （只要 node 模組；瀏覽器用系統的 Chromium：CHROMIUM_PATH，預設 /opt/pw-browsers/chromium）
//   node tools/store-screenshots.cjs [--device apple-iphone-6.9,...] [--lang zh-Hant,en,ja] [--shot menu,meteor,map,pet,versus]
//   node tools/store-screenshots.cjs --feature      只做 Google Play 的 1024×500 主圖
// 流星那張靠「機器人」打題目（讀 #m-answer 的算式、按數字鍵），所以每次畫面不會一模一樣；其他張是固定的。
const fs = require('fs'), path = require('path'), http = require('http');
const { chromium } = require('playwright');
const root = path.join(__dirname, '..');

// 各商店要的尺寸（像素 = CSS 寬高 × scale）。Apple：iPhone 6.9"／6.3"（Dynamic Island）、iPad 13"；Google：手機、10 吋平板
// 規格出處：docs/store-listing.md「截圖規格」。Apple 官方頁（App Store Connect 說明）列的是 1179×2556／1206×2622 與 2064×2752／2048×2732，
// 6.9" 的 1320×2868 是最大的 iPhone 尺寸，兩種都做，上傳時 Apple 會把大的縮給小的。
const DEVICES = {
  'apple-iphone-6.9': { w: 440, h: 956, s: 3, mobile: true },     // 1320×2868
  'apple-iphone-6.3': { w: 402, h: 874, s: 3, mobile: true },     // 1206×2622
  'apple-ipad-13':    { w: 1032, h: 1376, s: 2, mobile: false },  // 2064×2752
  'google-phone':     { w: 360, h: 720, s: 3, mobile: true },     // 1080×2160（長邊不超過短邊 2 倍）
  'google-tablet-10': { w: 800, h: 1280, s: 2, mobile: false },   // 1600×2560
};
const LANGS = {
  'zh-Hant': { who: '小星', pet: '糰糰' },
  en:        { who: 'Star', pet: 'Mochi' },
  ja:        { who: 'ほし', pet: 'もち' },
};
const SHOTS = ['menu', 'meteor', 'map', 'pet', 'versus'];

const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i < 0 ? d : (process.argv[i + 1] || '').split(','); };
const devices = arg('device', Object.keys(DEVICES)), langs = arg('lang', Object.keys(LANGS)), shots = arg('shot', SHOTS);
const outRoot = path.join(root, 'store', 'screenshots');

// 種存檔：一個玩了幾個禮拜的孩子——大部分星星亮了、幾題還在練、寵物是成體、戴了幾樣配件
function seed(lang) {
  const hard = new Set(['6x7', '7x6', '6x8', '8x6', '7x8', '8x7', '7x9', '9x7', '8x9', '9x8', '6x9', '9x6', '7x7', '8x8']);
  const weak = new Set(['7x8', '8x7', '6x8', '8x6', '7x9', '9x7']);
  const fresh = new Set(['9x9', '8x9', '9x8', '6x9', '9x6', '4x9', '3x9']);
  const facts = {};
  for (let a = 1; a <= 9; a++) for (let b = 1; b <= 9; b++) {
    const k = a + 'x' + b, h = (a * 7 + b * 13) % 10;
    if (weak.has(k)) facts[k] = { n: 5, err: 0.55, t: 5200, w: 3 };
    else if (fresh.has(k)) continue;
    else if (hard.has(k) || h === 3) facts[k] = { n: 3, err: 0.2, t: 3900, w: 1 };
    else facts[k] = { n: 4 + h, err: 0.02, t: 1500 + h * 130 };
  }
  const ghost = Array.from({ length: 20 }, (_, i) => 2100 + ((i * 337) % 900));
  return {
    who: { cur: '', list: [{ id: '', name: LANGS[lang].who }], asked: true },
    save: {
      facts, retest: [],
      bests: { std: { meteor: 1840, sudden: 920, ghost, cmpT: 27800, bomb: 58200, ghostLoss: 0 } },
      set: { what: 'mul', sound: false, music: false, sudden: false, seqLabel: true, tables: [1, 2, 3, 4, 5, 6, 7, 8, 9], lang },
      daily: { date: '', tasks: [], badges: 15, streak: 4, lastDone: '', starBase: 40, ans: 38, wrong: 3, log: {} },
      pet: { kind: 'cute', name: LANGS[lang].pet, dust: 126, fed: 380, wear: { head: 'star', face: 'glasses', neck: 'bowtie', side: 'balloon', back: '' }, released: [], sent: 0 },
    },
  };
}

function serve() {   // 小型靜態伺服器：不用 file://（字型與 localStorage 在 file:// 行為不同）
  const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.woff2': 'font/woff2', '.css': 'text/css', '.jpg': 'image/jpeg' };
  const srv = http.createServer((req, res) => {
    const f = path.join(root, decodeURIComponent(req.url.split('?')[0]).replace(/\/$/, '/index.html'));
    if (!f.startsWith(root) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
  });
  return new Promise(r => srv.listen(0, '127.0.0.1', () => r(srv)));
}

async function newPage(browser, dev, lang, base) {
  const ctx = await browser.newContext({ viewport: { width: dev.w, height: dev.h }, deviceScaleFactor: dev.s, isMobile: dev.mobile, hasTouch: true, reducedMotion: 'no-preference' });
  const page = await ctx.newPage(); const sd = seed(lang);
  page.on('pageerror', e => console.error('  [pageerror]', e.message));
  await page.addInitScript(([sd]) => {
    localStorage.setItem('jiujiu-meteor-who', JSON.stringify(sd.who));
    const d = new Date(); const day = n => { const x = new Date(d); x.setDate(x.getDate() - n); return `${x.getFullYear()}-${String(x.getMonth() + 1).padStart(2, '0')}-${String(x.getDate()).padStart(2, '0')}`; };
    sd.save.daily.log = { [day(1)]: { s: 44, t: 2600, r: 'std', a: 41 }, [day(2)]: { s: 42, t: 2700, r: 'std', a: 35 }, [day(4)]: { s: 40, t: 2800, r: 'std', a: 30 }, [day(8)]: { s: 31, t: 3300, r: 'std', a: 22 } };
    localStorage.setItem('jiujiu-meteor-v1', JSON.stringify(sd.save));
    let s = 20261013; Math.random = () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };   // 固定亂數：流星位置、星空、走動的寵物每次一樣
  }, [sd]);
  await page.goto(base + '/index.html'); await page.waitForTimeout(1200);
  await page.evaluate(() => document.fonts && document.fonts.ready);
  return { ctx, page };
}

const out = (dev, lang, n, name) => { const d = path.join(outRoot, dev, lang); fs.mkdirSync(d, { recursive: true }); return path.join(d, `${n}-${name}.jpg`); };
const snap = (page, f) => page.screenshot({ path: f, type: 'jpeg', quality: 88 });

// 機器人：讀目前瞄準的題目（#m-answer 顯示「a × b = 」），按出答案；回傳打了幾題
async function meteorBot(page, until) {
  let n = 0;
  for (let i = 0; i < 1200 && !(await until()); i++) {
    const t = await page.textContent('#m-answer').catch(() => '');
    const m = /^\s*(\d+)\s*×\s*(\d+)\s*=\s*$/.exec(t || '');
    if (m) { const a = String(+m[1] * +m[2]); for (const ch of a) { await page.keyboard.press(ch); await page.waitForTimeout(90); } n++; await page.waitForTimeout(350); }
    else await page.waitForTimeout(200);
  }
  return n;
}

async function shotMenu(page, f) { await page.waitForTimeout(1500); await snap(page, f); }
async function shotMeteor(page, f) {
  // 數畫面上有幾顆流星：流星的算式是用 canvas fillText 畫的，記下最近 60ms 內畫過的不同算式
  await page.evaluate(() => {
    window.__mt = {}; const ft = CanvasRenderingContext2D.prototype.fillText;
    CanvasRenderingContext2D.prototype.fillText = function (t) { if (/×/.test(String(t))) window.__mt[String(t)] = performance.now(); return ft.apply(this, arguments); };
  });
  const onScreen = () => page.evaluate(() => Object.values(window.__mt).filter(t => performance.now() - t < 60).length);
  await page.click('#go-meteor'); await page.click('[data-sd="0"]');
  await page.waitForTimeout(3600);   // 倒數
  const combo = async () => { const c = await page.textContent('#m-combo').catch(() => ''); return +(/(\d+)/.exec(c || '') || [0, 0])[1]; };
  await meteorBot(page, async () => (await combo()) >= 6 && (await onScreen()) >= 2);   // 不停手：連擊夠高、畫面上同時有 2 顆以上就截
  const t = await page.textContent('#m-answer'); const m = /(\d+)\s*×\s*(\d+)/.exec(t || '');
  if (m) { const a = String(+m[1] * +m[2]); await page.keyboard.press(a[0]); await page.waitForTimeout(150); }   // 打到一半，畫面有「正在作答」的感覺
  await snap(page, f);
}
async function shotMap(page, f) { await page.click('#go-map'); await page.waitForTimeout(800); await snap(page, f); }
async function shotPet(page, f) { await page.click('#go-pet'); await page.waitForTimeout(1200); await snap(page, f); }
async function shotVersus(page, f) {
  await page.click('#go-versus'); await page.waitForTimeout(500); await page.click('#v-start'); await page.waitForTimeout(3600);
  // 小隊長（下方）連答幾題把繩子往下拉，機器人偶爾也答
  for (let i = 0; i < 4; i++) {
    for (let tries = 0; tries < 20; tries++) {
      const t = await page.textContent('#v-bot [data-q]');
      const m = /(\d+)\s*×\s*(\d+)/.exec(t || '');
      if (m && !/\?/.test(t.replace(/=.*/, ''))) {
        for (const ch of String(+m[1] * +m[2])) { await page.click(`#v-bot [data-pad] .key >> text="${ch}"`, { timeout: 2000 }).catch(() => {}); await page.waitForTimeout(120); }
        break;
      }
      await page.waitForTimeout(250);
    }
    await page.waitForTimeout(700);
  }
  await snap(page, f);
}
const SHOTFN = { menu: shotMenu, meteor: shotMeteor, map: shotMap, pet: shotPet, versus: shotVersus };

async function feature(browser, base) {
  const L = JSON.parse(fs.readFileSync(path.join(root, 'store', 'listing.json'), 'utf8'));
  for (const lang of Object.keys(LANGS)) {
    const ctx = await browser.newContext({ viewport: { width: 1024, height: 500 }, deviceScaleFactor: 1 }); const page = await ctx.newPage();
    const g = L[lang].graphic;
    const html = `<!doctype html><html lang="${lang === 'zh-Hant' ? 'zh-Hant-TW' : lang}"><head><meta charset="utf-8"><style>
      @font-face{font-family:'Chiron GoRound TC';font-weight:900;src:url(/assets/fonts/chiron-900.woff2) format('woff2')}
      @font-face{font-family:'Chiron GoRound TC';font-weight:700;src:url(/assets/fonts/chiron-700.woff2) format('woff2')}
      @font-face{font-family:'Zen Maru Gothic';font-weight:900;src:url(/assets/fonts/zenmaru-900.woff2) format('woff2')}
      @font-face{font-family:'Zen Maru Gothic';font-weight:700;src:url(/assets/fonts/zenmaru-700.woff2) format('woff2')}
      @font-face{font-family:'Lilita One';src:url(/assets/fonts/lilita.woff2) format('woff2')}
      html,body{margin:0;width:1024px;height:500px;overflow:hidden}
      body{background:radial-gradient(120% 140% at 80% 0%,#1d3d78 0%,#11223a 45%,#08111f 100%);font-family:${lang === 'ja' ? "'Zen Maru Gothic'" : "'Chiron GoRound TC'"},system-ui,sans-serif;color:#f2f6fb;position:relative}
      .star{position:absolute;width:3px;height:3px;border-radius:50%;background:#fff;opacity:.8}
      .icon{position:absolute;left:64px;top:90px;width:320px;height:320px;border-radius:70px;box-shadow:0 18px 50px rgba(0,0,0,.55),0 0 0 4px rgba(255,210,63,.35)}
      .t{position:absolute;left:430px;right:40px;top:110px}
      h1{margin:0;font-size:${lang === 'en' ? 78 : 104}px;line-height:1.05;font-weight:900;color:#ffd23f;text-shadow:0 5px 0 #a87a00,0 10px 24px rgba(0,0,0,.5);letter-spacing:2px}
      p{margin:26px 0 0;font-size:${lang === 'en' ? 36 : 40}px;line-height:1.35;font-weight:700;color:#cfe8ff;text-wrap:balance}
      .badge{position:absolute;right:40px;bottom:30px;font-size:22px;font-weight:700;color:#5ff2d0;border:2px solid rgba(95,242,208,.5);border-radius:999px;padding:6px 18px;background:rgba(8,17,31,.5)}
    </style></head><body>
      ${Array.from({ length: 46 }, (_, i) => `<i class="star" style="left:${(i * 197) % 1024}px;top:${(i * 83) % 500}px;opacity:${0.3 + (i % 5) * 0.15}"></i>`).join('')}
      <img class="icon" src="/assets/icon/icon-512.png">
      <div class="t"><h1>${g.title}</h1><p>${g.tagline}</p></div>
      <div class="badge">${g.badge}</div>
    </body></html>`;
    const f = path.join(outRoot, 'google-feature', lang); fs.mkdirSync(f, { recursive: true });
    await page.setContent(html.replace(/url\(\//g, `url(${base}/`).replace('src="/', `src="${base}/`));
    await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(400);
    await page.screenshot({ path: path.join(f, 'feature-1024x500.jpg'), type: 'jpeg', quality: 88 });
    await ctx.close(); console.log('feature', lang);
  }
}

(async () => {
  const srv = await serve(); const base = 'http://127.0.0.1:' + srv.address().port;
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  try {
    if (process.argv.includes('--feature')) { await feature(browser, base); return; }
    for (const dn of devices) for (const lang of langs) for (const name of shots) {
      const { ctx, page } = await newPage(browser, DEVICES[dn], lang, base);
      const n = SHOTS.indexOf(name) + 1;
      try { await SHOTFN[name](page, out(dn, lang, n, name)); console.log(dn, lang, name); }
      catch (e) { console.error('FAIL', dn, lang, name, e.message); process.exitCode = 1; }
      await ctx.close();
    }
  } finally { await browser.close(); srv.close(); }
})();
