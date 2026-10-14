# 商店文案與截圖

> 本檔由 `tools/make-listing.py` 從 `store/listing.json` 產生，**要改文案請改 JSON 再重跑**。英文、日文是 Claude 寫的，**上架前請母語者看過**。
> 字數都是「字元數」；Apple 與 Google 的上限（名稱 30、副標 30、Apple 宣傳文字 170、Google 簡短說明 80、關鍵字 100、完整說明 4000）已用腳本檢查過。上限以後台當下顯示為準。

## 一、各語言文案

兩家商店共用同一份完整說明（description）。Apple 的「名稱」與 Google 的「應用程式名稱」相同。

### 繁體中文（zh-Hant／台灣）

| 欄位 | 字數／上限 | 內容 |
|---|---|---|
| 名稱（Apple Name／Google 標題） | 5／30 | 九九流星隊 |
| 副標題（Apple Subtitle） | 13／30 | 打流星練九九，錯題自動多練 |
| 宣傳文字（Apple Promotional Text） | 42／170 | 打下流星、點亮星圖，把九九乘法練到又快又不會錯。沒有廣告、不用網路、不收集任何資料。 |
| 簡短說明（Google Short description） | 35／80 | 打下流星、點亮星圖，把九九乘法練到又快又不會錯。沒有廣告，也不用網路。 |
| 關鍵字（Apple Keywords） | 44／100 | 九九乘法,乘法表,背九九,小學,國小,數學,二年級,三年級,練習,遊戲,學習,教育,速算 |
| 新功能（What's New） | 21／4000 | 第一版：五種玩法、星圖、每日任務、養寵物。 |

**完整說明**（654／4000）

```text
九九流星隊是給小學生（約二、三年級）練九九乘法的遊戲。目標不是「學會」，而是把「都會，但偶爾會背錯」練到又快又不會錯。

【五種玩法】
● 流星防衛戰：算出答案就發射雷射，打下往小鎮掉的流星。每 5 波有錯題魔王，還有寶箱和追蹤飛彈。
● 幽靈競速：20 題計時賽，追過上次的自己。
● 雙人拔河：面對面搶答，可以跟大人比，也能跟機器人比。
● 哪個大？哪個小？：三個算式，點出答案最大（或最小）的那個。
● 炸彈拆除：引線燒完前，點掉炸彈上那個數的倍數。

【越玩越熟】
● 答錯的題目會悄悄更常出現，隔一陣子再考一次。孩子只覺得在玩遊戲。
● 星圖：每一題都有一顆星，答得又快又對就亮起來，一眼看出哪裡還不熟。
● 每日任務、徽章、養寵物：用答對的題目換星塵餵寵物（毛毛、小龍、呱呱，還有一顆傳說蛋），再換上配件。
● 沒有「寵物餓了」，也不會倒扣，不逼孩子。

【給家長】
● 沒有廣告、沒有內購、不用登入，不收集任何個人資料。
● 完全離線，不用網路也能玩。遊戲紀錄只存在這台裝置上，我們看不到。
● 換新手機或平板時，大人可以在設定用「備份紀錄」把紀錄搬過去（備份檔或備份碼，存在你自己選的地方，遊戲不會上傳）。
● 最多 4 位孩子，各有自己的紀錄。設定裡可以選要練哪幾個乘法表（1 到 12）。
● 要連到外部網頁之前，需要大人回答一題。
● 介面有繁體中文、English、日本語。

隱私權政策：https://ianyclin.github.io/jiujiu-game/privacy/
```

### English（en-US）

| 欄位 | 字數／上限 | 內容 |
|---|---|---|
| 名稱（Apple Name／Google 標題） | 16／30 | 9×9 Meteor Squad |
| 副標題（Apple Subtitle） | 24／30 | Times tables meteor game |
| 宣傳文字（Apple Promotional Text） | 125／170 | Shoot down meteors, light up the star map, and get your times tables fast and right. No ads, works offline, collects no data. |
| 簡短說明（Google Short description） | 74／80 | Shoot down meteors and light up the star map. Master times tables. No ads. |
| 關鍵字（Apple Keywords） | 96／100 | multiplication,times table,math,kids,practice,grade 2,grade 3,learn,facts,school,education,drill |
| 新功能（What's New） | 69／4000 | First release: five games, star map, daily quests and a pet to raise. |

**完整說明**（1974／4000）

```text
9×9 Meteor Squad is a times-tables practice game for kids in about 2nd to 3rd grade. The goal isn't just "learning" the facts. It's turning "I know it, but I sometimes slip" into fast and correct, even when it feels rushed.

FIVE GAMES
● Meteor Defense: type the answer to fire a laser and shoot down meteors falling on the little town. Every 5 waves a boss made of the facts you miss, plus treasure chests and homing missiles.
● Ghost Race: 20 questions against the clock. Beat your own last run.
● Tug of War: face-to-face for two players. Play a grown-up, or play the robot.
● Bigger or Smaller: three problems. Tap the one with the biggest (or smallest) answer.
● Bomb Defusal: before the fuse burns out, tap every multiple of the number on the bomb.

THE MORE THEY PLAY, THE BETTER THEY KNOW IT
● Facts a child misses quietly show up more often, and come back for another try a little later. To the child, it just feels like playing.
● Star Map: every fact has a star. It lights up when the answer is fast and right, so you can see at a glance what still needs work.
● Daily quests, badges and a pet to raise: answers earn stardust to feed the pet (Fuzzy, Draki or Croaky, plus a legendary egg) and unlock outfits.
● No "your pet is hungry" and no penalties. Nothing pressures the child.

FOR PARENTS
● No ads, no in-app purchases, no sign-in, and no personal data collected.
● Works fully offline. Progress is saved only on this device, and we can't see it.
● Getting a new phone or tablet? A grown-up can use "Back up records" in Settings to move progress over with a backup file or code. You keep it wherever you like; the game never uploads it.
● Up to 4 kids, each with their own progress. In Settings you can pick which times tables to practice (1 to 12).
● A grown-up has to answer a question before any link opens outside the game.
● Available in English, Traditional Chinese and Japanese.

Privacy policy: https://ianyclin.github.io/jiujiu-game/privacy/en.html
```

### 日本語（ja）

| 欄位 | 字數／上限 | 內容 |
|---|---|---|
| 名稱（Apple Name／Google 標題） | 5／30 | 九九流星隊 |
| 副標題（Apple Subtitle） | 12／30 | 九九をゲームでれんしゅう |
| 宣傳文字（Apple Promotional Text） | 64／170 | 流星をうって、星マップをひからせよう。九九を「はやく、まちがえずに」言えるように。広告なし、オフラインOK、データは集めません。 |
| 簡短說明（Google Short description） | 42／80 | 流星をうって星マップを光らせよう。九九を楽しくれんしゅう。広告なし・オフラインOK。 |
| 關鍵字（Apple Keywords） | 40／100 | 九九,かけ算,算数,小学生,2年生,3年生,練習,暗記,ゲーム,学習,知育,計算 |
| 新功能（What's New） | 37／4000 | はじめてのリリース：5つの遊び、星マップ、デイリーミッション、ペット育成。 |

**完整說明**（972／4000）

```text
九九流星隊は、小学生（2〜3年生くらい）が九九をれんしゅうするゲームです。ねらいは「おぼえる」ことだけではなく、「わかっているのに、ときどきまちがえる」を、はやく、まちがえずに答えられるまで練習することです。

【5つの遊び】
● 流星ぼうえいせん：答えを入力するとレーザーが発射され、町に落ちてくる流星をうち落とします。5ウェーブごとに、まちがえやすい問題のボスが登場。宝箱や追いかけミサイルもあります。
● ゴーストレース：20問のタイムレース。前回の自分を追いこそう。
● ふたりでつなひき：向かい合って早押し。大人とも、ロボットとも対戦できます。
● どっちが大きい？小さい？：3つの式から、答えがいちばん大きい（小さい）ものを選びます。
● ばくだんかいたい：導火線がもえきる前に、ばくだんの数の倍数をタップします。

【遊ぶほど身につく】
● まちがえた問題は、こっそりよく出るようになり、少しあとでもう一度出ます。子どもには、ただ遊んでいるように感じられます。
● 星マップ：すべての問題に星が1つ。はやく正しく答えられると光るので、どこが苦手か一目でわかります。
● デイリーミッション、バッジ、ペット育成：正解すると星のこなが貯まり、ペット（モフモフ、リュウ、ケロケロ、そして伝説のたまご）にあげたり、きせかえを楽しんだりできます。
● 「おなかがすいた」も、ペナルティもありません。子どもをせかしません。

【保護者の方へ】
● 広告なし、アプリ内課金なし、ログイン不要。個人情報は一切集めません。
● 完全オフラインで遊べます。記録はこの端末の中にだけ保存され、私たちには見えません。
● 機種変更のときは、大人の方が設定の「きろくのバックアップ」から記録を移せます（バックアップファイルまたはコード。保存先はご自身で選び、ゲームがアップロードすることはありません）。
● 最大4人まで、それぞれの記録を保存できます。設定で練習する段（1〜12）を選べます。
● ゲームの外のページを開く前に、大人の方が問題に答える必要があります。
● 画面は日本語・繁体字中国語・英語に対応しています。

プライバシーポリシー：https://ianyclin.github.io/jiujiu-game/privacy/ja.html
```

> 關鍵字不要重複名稱與副標題裡已有的字（Apple 會自己索引）；不要放競品或商標名稱。
> 說明中沒有宣稱成效（如「保證進步」），也沒有宣稱「手繪」（寵物與配件插畫是 AI 生成，見 `CLAUDE.md`）。

## 二、類別與分級（建議）

| 項目 | 建議 |
|---|---|
| Apple 主要類別／次要類別 | 教育（Education）／遊戲（Games → Educational） |
| Apple Kids 類別 | 勾選，年齡層 **6–8 ＋ 9–11**（不勾 5 歲以下） |
| Apple 年齡分級問卷 | 全部「無」（無暴力、無使用者產生內容、無動態消息、無不受限網頁存取、無賭博、無購買）→ 預期 4+ |
| Google 類別 | 教育（Education）；Families：目標年齡 6–8、9–12 |
| Google 內容分級（IARC） | 全部「否」；預期全年齡 |
| 價格 | 免費、無內購、無廣告（Play Console「包含廣告」選「否」） |
| 版權欄（Apple Copyright） | `© 2026 指數三寶飯` |

## 三、隱私問卷（照實填）

| 商店欄位 | 填法 | 依據 |
|---|---|---|
| Apple App Privacy | **Data Not Collected**（不收集資料）；不追蹤 | 沒有 SDK、沒有網路請求；`PrivacyInfo.xcprivacy` 一致 |
| Apple Privacy Policy URL | `https://ianyclin.github.io/jiujiu-game/privacy/`（各語言版可填 `…/privacy/en.html`、`…/privacy/ja.html`） | merge 後要先在瀏覽器確認打得開 |
| Apple Support URL | `https://ianyclin.github.io/jiujiu-game/support/`（三語支援頁，內含聯絡 email 與常見問題；在 #48 的分支） | merge 後先在瀏覽器確認打得開 |
| 聯絡 email（Apple／Google 開發者資料） | `gigigagagogogege@gmail.com` | 會公開顯示 |
| Google Data safety | 「此應用程式不會收集或分享任何使用者資料」。因為沒有收集，傳輸加密與刪除要求兩欄不適用 | Android 已拿掉 `INTERNET` 權限 |
| Google 廣告 ID 宣告 | 不使用 | — |
| Google「目標對象與內容」 | 勾選兒童年齡層；回答「含有廣告：否」 | — |
| App Review Notes（給 Apple） | 見下 | — |

**App Review Notes 建議內容（英文）**：

```text
9×9 Meteor Squad is an offline times-tables practice game for children. It has no accounts, no ads, no in-app purchases, no third-party SDKs and makes no network requests. All progress is stored on the device only.
The only links that leave the app are the author's Facebook page and the privacy policy. Both are behind a parental gate (a grown-up must answer a math question first), as required for the Kids Category.
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

