#!/usr/bin/env python3
"""讀 store/listing.json（商店文案的唯一來源），檢查各商店的字數上限，輸出 docs/store-listing.md。
用法：python3 tools/make-listing.py（超過上限會報錯並結束）。改文案只改 listing.json，不要直接改產出的 md。"""
import json, os, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(root, 'store', 'listing.json'), encoding='utf-8'))
LIM = {'name': 30, 'subtitle': 30, 'promo': 170, 'short': 80, 'keywords': 100, 'whatsNew': 4000, 'description': 4000}
NAMES = {'zh-Hant': '繁體中文（zh-Hant／台灣）', 'en': 'English（en-US）', 'ja': '日本語（ja）'}
bad = []
for lang, d in L.items():
    for k, m in LIM.items():
        if len(d[k]) > m: bad.append(f'{lang}.{k}: {len(d[k])} > {m}')
if bad: sys.exit('超過字數上限：\n' + '\n'.join(bad))

o = []
w = o.append
w('''# 商店文案與截圖

> 本檔由 `tools/make-listing.py` 從 `store/listing.json` 產生，**要改文案請改 JSON 再重跑**。英文、日文是 Claude 寫的，**上架前請母語者看過**。
> 字數都是「字元數」；Apple 與 Google 的上限（名稱 30、副標 30、Apple 宣傳文字 170、Google 簡短說明 80、關鍵字 100、完整說明 4000）已用腳本檢查過。上限以後台當下顯示為準。

## 一、各語言文案

兩家商店共用同一份完整說明（description）。Apple 的「名稱」與 Google 的「應用程式名稱」相同。
''')
for lang, d in L.items():
    w(f'### {NAMES[lang]}\n')
    w('| 欄位 | 字數／上限 | 內容 |\n|---|---|---|')
    rows = [('名稱（Apple Name／Google 標題）', 'name'), ('副標題（Apple Subtitle）', 'subtitle'), ('宣傳文字（Apple Promotional Text）', 'promo'),
            ('簡短說明（Google Short description）', 'short'), ('關鍵字（Apple Keywords）', 'keywords'), ('新功能（What\'s New）', 'whatsNew')]
    for label, k in rows:
        w(f'| {label} | {len(d[k])}／{LIM[k]} | {d[k]} |')
    w(f'\n**完整說明**（{len(d["description"])}／{LIM["description"]}）\n')
    w('```text\n' + d['description'] + '\n```\n')
w('''> 關鍵字不要重複名稱與副標題裡已有的字（Apple 會自己索引）；不要放競品或商標名稱。
> 說明中沒有宣稱成效（如「保證進步」），也沒有宣稱「手繪」（寵物與配件插畫是 AI 生成，見 `CLAUDE.md`）。

## 二、類別與分級（建議）

| 項目 | 建議 |
|---|---|
| Apple 主要類別／次要類別 | 教育（Education）／遊戲（Games → Educational） |
| Apple Kids 類別 | 勾選，年齡層 **6–8 ＋ 9–11**（不勾 5 歲以下） |
| Apple 年齡分級問卷 | 照實填：暴力、使用者產生內容、動態消息、不受限網頁存取、賭博都「無」；問到 App 內購買就照實回答「有」（一次性解鎖）→ 預期 4+ |
| Google 類別 | 教育（Education）；Families：目標年齡 6–8、9–12 |
| Google 內容分級（IARC） | 「數位購買」答「是」（有 `unlock_all` 內購），其他全部「否」；預期全年齡 |
| 價格 | App 本身**免費**＋一個**非消耗型**內購 `unlock_all`（建議 US$2.99，解鎖幽靈競速、雙人拔河、哪個大、炸彈拆除）；無廣告（Play Console「包含廣告」選「否」）。Apple 要在商品設定打開「家人共享」 |
| 版權欄（Apple Copyright） | `© 2026 指數三寶飯` |

## 三、隱私問卷（照實填）

| 商店欄位 | 填法 | 依據 |
|---|---|---|
| Apple App Privacy | **Data Not Collected**（不收集資料）；不追蹤 | 遊戲本身沒有網路請求；購買走 StoreKit，Apple 的說明頁寫「You are not responsible for disclosing data collected by Apple」，付款資料在 app 外輸入、開發者拿不到也不算收集；`PrivacyInfo.xcprivacy` 一致 |
| Apple Privacy Policy URL | `https://ianyclin.github.io/jiujiu-game/privacy/`（各語言版可填 `…/privacy/en.html`、`…/privacy/ja.html`） | merge 後要先在瀏覽器確認打得開 |
| Apple Support URL | `https://ianyclin.github.io/jiujiu-game/support/`（三語支援頁，內含聯絡 email 與常見問題；在 #48 的分支） | merge 後先在瀏覽器確認打得開 |
| 聯絡 email（Apple／Google 開發者資料） | `gigigagagogogege@gmail.com` | 會公開顯示 |
| Google Data safety | 預計填「此應用程式不會收集或分享任何使用者資料」，**但上架前要在 Play Console 的說明再確認一次**：Google 付款程式庫（billing 9.1.0）會帶進 Google 自己的記錄元件（`datatransport`，也是 `INTERNET`／`ACCESS_NETWORK_STATE` 權限的來源），Google 的說明把付款程式庫列為「財務資訊」的例子，但沒有講清楚只用它解鎖、不存購買紀錄的 app 要不要申報；查不到官方答案就問 Play 支援 | 遊戲程式本身不連網；我們沒有伺服器、收不到購買紀錄 |
| Google 廣告 ID 宣告 | 不使用 | — |
| 「備份紀錄」功能 | 不改變上面的答案：備份檔／備份碼由大人自己存放，遊戲不上傳、我們收不到，所以仍是「不收集」 | 隱私權政策已寫明 |
| Google「目標對象與內容」 | 勾選兒童年齡層；回答「含有廣告：否」 | — |
| App Review Notes（給 Apple） | 見下 | — |

**App Review Notes 建議內容（英文）**：

```text
9×9 Meteor Squad is an offline times-tables practice game for children. It has no accounts, no ads, no analytics or advertising SDKs, and the game itself makes no network requests. All progress is stored on the device only.
In-app purchase: Meteor Defense, the Star Map, the pet and daily missions are free. The other four games (Ghost Race, Tug of War, Biggest? Smallest?, Bomb Squad) can each be played 3 times for free; after that, tapping one shows a card asking the child to get a grown-up. One non-consumable purchase (unlock_all) unlocks all four. The purchase screen, Restore Purchase and promo code redemption are only reachable after a parental gate (a math question), either from that card or from Settings > For grown-ups > Unlock all games.
The only links that leave the app are the author's Facebook page and the privacy policy. Both are behind the same parental gate, as required for the Kids Category.
Stardust (the in-game currency used to feed the pet, buy it treats and trade for badges) is earned only by answering questions and cannot be bought; the only in-app purchase is unlock_all.
No login is needed. To see the pet and star map screens quickly, tap "Star Map" or "Pet" on the main menu.
```

## 四、截圖與圖形

腳本：`node tools/store-screenshots.cjs`（需 `npm i --no-save playwright` 與系統 Chromium；`--feature` 產生 Google 主圖）。用真的遊戲（`index.html` 不改），種一份「玩了幾週」的存檔，固定亂數；流星那張由機器人打題目，每次略有不同。五張順序：**1 主選單、2 流星防衛戰、3 星圖、4 寵物、5 雙人拔河**（對機器人）。三種語言各一套，輸出在 `store/screenshots/<裝置>/<語言>/`，JPEG（沒有透明度，Apple 不收有透明的圖）。

| 資料夾 | 像素 | 用在 | 備註 |
|---|---|---|---|
| `apple-iphone-6.9` | 1320 × 2868 | App Store iPhone 6.9" | 最大的 iPhone 尺寸，Apple 會縮給小的 |
| `apple-iphone-6.3` | 1206 × 2622 | App Store iPhone（Dynamic Island） | Apple 說明頁列的必填尺寸之一 |
| `apple-ipad-13` | 2064 × 2752 | App Store iPad 13" | 專案有支援 iPad 才需要 |
| `google-phone` | 1080 × 2160 | Play 手機截圖 | 2:1，Play 長短邊比上限 |
| `google-tablet-10` | 1600 × 2560 | Play 10 吋平板截圖 | 選填，有平板排名／推薦才需要 |
| `google-feature` | 1024 × 500 | Play 主圖（Feature graphic） | 必填；用圖示加標語畫的，**請你看過** |

- Apple 規格出處是 App Store Connect 說明頁（本次已讀）：iPhone Dynamic Island 1179×2556／1206×2622、iPad 13" 2064×2752／2048×2732，每種尺寸 1–10 張。若 Face ID 大螢幕那一欄仍被要求，補 1284×2778（`tools/store-screenshots.cjs` 的 `DEVICES` 加一行）。
- Google 的規格我查不到官方頁（網路被擋），數字來自搜尋結果與既有知識（手機截圖 2–8 張、短邊 ≥ 320、長邊 ≤ 3840 且比例不超過 2:1；主圖 1024×500；圖示 512×512 → 用 `assets/icon/icon-512.png`），**請在 Play Console 上傳時確認**。
- 截圖是遊戲原圖，沒有裝置外框與行銷標語。需要的話再另外設計。

''')
open(os.path.join(root, 'docs', 'store-listing.md'), 'w', encoding='utf-8').write('\n'.join(o))
print('ok')
