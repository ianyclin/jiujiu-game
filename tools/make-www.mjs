#!/usr/bin/env node
// 把遊戲本體複製到 www/（Capacitor 的 webDir）。index.html 與 assets 原封不動，不改、不壓縮、不加任何檔。
// 用法：node tools/make-www.mjs（或 npm run www）。www/ 是產物，不進版控。
import { cpSync, rmSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const out = join(root, 'www');
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });

for (const f of ['index.html', 'manifest.json']) cpSync(join(root, f), join(out, f));
// 1024 圖示只給商店用（App Store 圖示在 ios/ 裡），遊戲頁面用不到，不放進 app
cpSync(join(root, 'assets'), join(out, 'assets'), {
  recursive: true,
  filter: src => !src.endsWith('icon-1024.png'),
});

for (const f of ['index.html', 'assets/fonts', 'assets/pets', 'assets/gear']) {
  if (!existsSync(join(out, f))) { console.error('缺少 ' + f); process.exit(1); }
}
console.log('www/ 完成');
