# 上架前獨立審查（2026-11-12）

> 審查者：Claude（獨立審查 session，只審查、沒有改遊戲程式）。對象：版本 1.4，`main` 的 commit `40ae955`。
> 怎麼審的：
> - 讀文件：`CLAUDE.md`、`docs/` 四份上架文件、`store/listing.json`、`ROADMAP.md`。
> - 讀程式與打包設定：`index.html`、`ios/`、`android/`、`capacitor.config.json`。
> - 讀外掛原始碼：`@capgo/native-purchases` 8.9.5 與 Capacitor 8.5.3 的 iOS 原始碼。
> - 實際玩：用 Playwright（Chromium）開本機 `index.html`。三種語言，六種尺寸：320×568、375×667、390×844、iPad 820×1180、1180×820、1024×1366。
> - 模擬購買：用假的 `window.Capacitor` 跑購買流程，iOS 與 Android 各一次。
> - 查規則：Apple 與 Google 的官方頁面，下面附網址。
>
> 標記說明：
> - **【實測】**：有用腳本重現或在畫面上看到。
> - **【讀程式】**：只看了程式碼。
> - **【推測】**：沒辦法驗證，例如要真的 iPhone 才知道。
> - 商店規則一律附官方網址。

---

## 結論先講

**沒有找到「一定會被退件」或「會讓遊戲壞掉」的問題。** 購買、恢復購買、家長關卡、隱私標示、Privacy Manifest、出口合規、版本號都對得上規則。壞存檔、儲存空間滿了、切到背景也都不會黑畫面。

但有 **3 件事要在送審前改或決定**：
1. **Kids 年齡層只能選一個**。文件寫「6–8 ＋ 9–11」，Apple 不允許，而且通過後不能改。
2. **家長關卡的「30 秒鎖」按「取消」就能繞過**。程式要修一行。
3. **審核備註要補「怎麼解家長關卡」與「試玩次數」**。Apple 10 月新增的 2.5.19、2.3.1(a) 要求功能寫清楚。

另外有 **1 件法律面的事要你決定**：美國德州等州的 App Store 年齡驗證法，Apple 建議開發者接 Declared Age Range API（見 A5）。

---

## A. 審核風險（會被退件或之後被要求補）

### A1. Kids 類別只能選「一個」年齡層，而且通過後不能改【已查官方原文】
- **問題**：`docs/store-listing.md:147` 寫「年齡層 6–8 ＋ 9–11」，`docs/launch-easy.md:107` 寫「年齡 6–8、9–11」。Apple 規定只能選一個。
- **官方原文**：
  - 類別頁：「Age-appropriate apps must be placed in **one** of three age bands based on their primary audience: 5 and under, 6–8, or 9–11.」（https://developer.apple.com/app-store/categories/ ，本次親自讀過）
  - 分級說明：「You can't change this selection once your app is approved」（https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating/ ）
- **建議**：選 **6–8**。商店說明寫的是「約二、三年級」，九九是小二、小三的課程，主要對象落在 6–8。9–11 的孩子還是搜得到、裝得了；年齡層只決定 Kids 分類頁把它放在哪一區。這是不能反悔的選擇，請你最後拍板。
- **Google 不受影響**：Google 的目標年齡可以複選（6–8、9–12），不用改。

### A2. 年齡分級問卷：有兩題容易答錯，答錯就進不了 Kids【已查官方原文】
- **Contests（競賽）**：Apple 的定義是「compete with one another for rankings, rewards」。答「Frequent」會變成 **13+**，13+ 就不能進 Kids。
  - 這個遊戲沒有線上排行、沒有和其他玩家比賽。幽靈競速是跟自己比，拔河是同一台裝置面對面玩。
  - 建議答「**無**」，最保守也只答「Infrequent」。
  - 來源：https://developer.apple.com/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions
- **Loot Boxes（戰利品箱）**：定義是「randomized virtual items **for purchase**」，指要花錢買的隨機獎勵。遊戲裡的寶箱不能用錢買，答「**無**」。
- **Cartoon or fantasy violence（卡通或奇幻暴力）**：答「Infrequent」會變 9+，9+ 還是可以進 Kids。打流星、拆炸彈打的不是角色，建議答「無」。
- **要多答的新題目**（`docs/store-checklist.md` 還沒寫到）：
  - In-App Controls（家長控制、年齡驗證）
  - 社群媒體：2026 年 9 月起送審必答（https://developer.apple.com/news/?id=tlur8uvi ）
  - Shared Location、Dating：2026-11-16 起新增，2027-01-12 前所有 app 都要答完（https://developer.apple.com/news/?id=yxkh08us ）
  - 以上全部答「無／沒有」。
- **預期結果**：4+。

### A3. 家長關卡的「連錯 3 次鎖 30 秒」可以用「取消」繞過【實測】
- **問題**：答錯兩次後按「取消」，再按「給大人看」，又有 3 次機會。這樣可以無限猜下去。
- **證據**：
  - `index.html:4122` 的 `$('#gate-close')… { gate = null; … }` 把整個關卡物件丟掉。
  - `index.html:3976` 每次打開關卡都把 `miss: 0` 重設。
  - 子代理用腳本連跑 5 輪「錯 2 次＋取消」，一次都沒被鎖。
- **為什麼要緊**：`CLAUDE.md` 寫了加這個鎖的原因是「亂按大約 30 秒就能猜中」。現在這個防護等於沒有。審核員不太可能測到這一點，但 1.3 要的是孩子進不去，這個漏洞正好讓孩子進得去。
- **建議**：把連錯次數改成和 `gateWait` 一樣的全域變數。按取消不歸零，答對或 30 秒鎖結束才歸零。只動幾行。

### A4. 審核備註要補幾句，避免 2.1／2.5.19 退件【已查官方原文】
- **規則**：
  - 2.3.1(a)：「All new features, functionality… must be described with specificity in the Notes for Review… (generic descriptions will be rejected)」
  - 2.5.19：「Don't include any hidden, dormant, or undocumented features… your app's functionality should be clear to end users and App Review.」
  - 兩條都在 https://developer.apple.com/app-store/review/guidelines/ ，2.5.19 是 2026-10-16 更新新增的（https://developer.apple.com/news/?id=92th7e5i ）。
- **現在的備註**（`docs/store-listing.md` 第三節）已經寫了試玩與家長關卡，建議再補：
  1. **怎麼解家長關卡**：寫出例子，例如「Parental gate: solve the arithmetic shown, e.g. 5 + 2 × 13 = 31 (multiplication first). Three wrong answers lock it for 30 seconds.」，審核員才不會卡在關卡前。
  2. **最快的測試路徑**：「Settings → For grown-ups → Unlock all games → solve the gate → purchase sheet (Sandbox)」。也寫明四個付費遊戲各有 3 局試玩，試玩用完會出現鎖卡。
  3. **遊戲裡的獎勵**：隱藏配件（徽章 40／50 個才出現）、傳說蛋、星塵換徽章，都是靠玩遊戲解鎖的內容，不能用錢買。
  4. **Restore Purchases 的位置**：在家長關卡後面的購買卡裡。
  5. 一句「This is an educational game for ages 6–8」（配合 A1）。
- 英文備註上限 4000 bytes，目前遠低於上限。

### A5. 美國州法：德州 SB2420 等「App Store 年齡驗證」【已查官方新聞，需要你決定；我不是律師】
- **內容**：
  - 2026-06-04 起，德州新的 Apple 帳號下載 app 與購買內購要家長同意，這部分 Apple 自己處理。
  - Apple 對開發者寫的是：「should use the Significant Change API」並「Review documentation and implement」Declared Age Range（https://developer.apple.com/news/?id=sg176nne ）。
  - 猶他（2026-05-06）、路易斯安那（2026-07-01）也會透過 Declared Age Range 分享年齡（https://developer.apple.com/news/?id=f5zj08ey ）。
  - Apple 的 Q&A：「In regions where legally required, you need to check the age… with the Declared Age Range API」（https://developer.apple.com/support/age-assurance ）
- **對這個 app 的影響**：
  - 這是**州法義務，不是審核條文**，送審被退的機率低。
  - 但要「照做」就得加原生程式（Declared Age Range 沒有官方 Capacitor 外掛），違反 `CLAUDE.md`「不再加外掛」。
- **三個選項**：
  - (a) 先上架，追蹤 Apple 後續要求再做。
  - (b) 第一版的銷售地區排除美國，最保守，但英文市場少一大塊。
  - (c) 寫一小段原生程式接 Declared Age Range。
- **我的建議**：(a)。遊戲不收資料、沒有帳號、購買由 Apple 處理家長同意，實際能被要求的事很少。重點是**之後若有「重大變更」**（例如加了雲端同步），要記得 Significant Change 這件事。這點建議問懂美國法的人。

### A6. 商店截圖：一張顯示了不可能的紀錄，付費遊戲也沒標出來【實測＋讀程式】
- **幽靈競速「最佳 2.2 秒」**：iPhone 與 iPad 截圖的主選單都寫「幽靈競速 最佳 2.2 秒」（英文 Best 2.2s）。20 題跑 2.2 秒是不可能的成績。
  - 原因：`tools/store-screenshots.cjs:49` 種的幽靈紀錄是「每題時間」，但遊戲存的是「累計時間」（`index.html:3908` 拿第 20 個數字當總時間）。
  - 影響：審核員不太會注意，家長可能會覺得奇怪。
  - 建議：把那一行改成累計值（例如每題約 2.5 秒，總時間約 50 秒），重截一次。
- **截圖沒標付費遊戲**【已查官方原文】：2.3.2：「make sure your app description, screenshots, and previews clearly indicate whether any featured items, levels… require additional purchases.」
  - 第 5 張是雙人拔河，屬於付費遊戲。截圖用的是網頁版，主選單卡片上沒有「免費試玩 3 次」的牌子。
  - 說明文字已經寫清楚哪些要買，所以風險**低～中**。
  - 建議用 App 模式（假 Capacitor）重截主選單，讓四張付費卡帶「免費試玩」牌子，或在拔河那張改用免費功能。
- **iPad 截圖必填**【已查官方原文】：專案支援 iPad，所以至少要一張 iPad 13" 截圖（https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications ）。截圖已經有了，`store-listing.md` 寫的「有支援 iPad 才需要」可以改成「必填」。
  - iPhone 必填的是 Dynamic Island 中尺寸（1206×2622），已經有；6.9" 是選填。
  - 2027 年 4 月起，用 iOS 27.1 SDK 建置還要多交 iPhone Duo 尺寸。

### A7. 最低功能（4.2「網頁包裝」）仍是主要的未知風險【已查官方原文；推測】
- 4.2 原文：「elevate it beyond a repackaged website」。4.7 管的是不在安裝檔裡的 HTML5 遊戲，這個 app 的 HTML 打包在安裝檔裡，不適用。
- 這個 app 完全離線、有即時合成的音樂、存檔、內購、多人，比一般網頁包裝扎實。審核員看不出它是網頁做的，**除非你在備註或說明裡提到「網頁版」**。
- **建議**：
  - 備註強調離線、本機存檔、StoreKit 內購、iPad 支援、即時合成音訊，**不要提 GitHub Pages 網頁版是免費的**。
  - 商店說明現在沒提網頁版，很好，維持不提。
  - 隱私權政策三語都提到「網頁版」（例如 `privacy/index.html:27`、`54`），遊戲的備份說明也提到「從網頁版搬到 app」。這是如實揭露資料怎麼處理，**應該保留**，不要為了審核拿掉。只是不要在審核備註裡主動強調「這是網頁包起來的」。

### A8. Privacy Manifest 與第三方 SDK 簽章【已查官方原文；推測】
- **Privacy Manifest**：`PrivacyInfo.xcprivacy` 宣告不追蹤、不收集，跟「Data Not Collected」一致。
  - Capacitor 8.5.3 自己附的 manifest 沒宣告 required-reason API，Capgo 外掛的 Swift 原始碼也沒用到 UserDefaults 之類的 API。目前的寫法看起來正確。
  - 上傳後如果 Apple 寄信說缺 reason（例如 `NSPrivacyAccessedAPICategoryUserDefaults` / `CA92.1`），再補上即可。上傳時會先收到 email，不會直接被退。
- **SDK 簽章**：Apple 的第三方 SDK 名單**有列 Capacitor 與 Cordova**（https://developer.apple.com/support/third-party-SDK-requirements/ ）。這個專案用 Swift Package 的 binary xcframework 引入它們，要有簽章。
  - 建議：第一次在 Xcode 或 CI 建置後，看 Capacitor xcframework 的 Signature 欄位。
- **App Privacy**：用 StoreKit 仍可填「Data Not Collected」。官方原文：「You are not responsible for disclosing data collected by Apple」（https://developer.apple.com/app-store/app-privacy-details/ ）。

### A9. 內購送審流程【已查官方原文】
- 第一個非消耗型內購**一定要和 App 版本放在同一次送審**（https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-in-app-purchase ）。`launch-easy.md` 第 12 步已寫，很好。
- 內購的審核截圖要「clearly shows the item」：建議截購買卡（家長關卡後那頁），**上傳後不能刪**。
- **恢復購買要不要放在家長關卡後面**：官方沒寫，查不到原文。放在後面最保守，維持現狀。
- **優惠碼**：Apple 2026-03-26 起不能再替內購建 Promo Code，改用 Offer Codes。這是二手資料，搜尋結果指向 Apple 官方新聞，原文我沒讀到。非消耗型可用，iOS 16.3 以上。`launch-easy.md`「上架以後」寫的就是 Offer Codes，正確。

---

## B. 程式問題（玩家可能卡住或遇到怪事）

### B1. 「購買前詢問」送出後還能再按購買【讀程式】
- **證據**：`index.html:4067`，外掛回 pending 時只顯示「付款還在處理中」，`iapBusy` 回到 false，購買鈕又可以按。
- **情境**：家長開了「購買前詢問」，孩子按了以後，家長手機收到請求。大人再按一次，會再送一個請求。
- **建議**：記一個「已送出、等核准」的狀態，這段期間購買鈕停用，只留恢復購買。
- **嚴重度**：低。TestFlight 測不到「購買前詢問」，上架後才看得到。

### B2. iOS 被來電打斷後，音樂可能不會自己回來【推測】
- **證據**：`index.html:1854` 只在 `actx.state === 'suspended'` 時才 `resume()`。iOS 被來電或 Siri 打斷時，狀態是 `'interrupted'`。
- **建議**：改成「不是 `running` 就 resume」。用 TestFlight 時接一通電話試試。

### B3. 匯入備份寫到一半失敗，可能刪掉別人的紀錄【讀程式，機率很低】
- **證據**：`index.html:4183` 先 `removeItem` 掉備份裡沒有的人，再逐一 `setItem`。中間如果因為儲存空間滿了丟例外，被刪的人就救不回來。
- **建議**：先寫完全部新資料，最後才刪舊的。

### B4. iPad 台前調度（Stage Manager）把視窗拉矮時，會出現關不掉的「請轉直」【推測】
- **證據**：`index.html:4332` 的條件是橫向、高度小於 500、觸控螢幕。iPad 的小視窗符合這三個條件，但把 iPad 轉直也不會消失。
- **建議**：多加一個條件，用螢幕本身的高度判斷（例如 `screen.height < 500`）。審核員有時會在 iPad 上測。

### B5. 試玩次數：刪掉重裝會重來；快速關閉可能少記一次【讀程式／實測但不確定】
- 試玩次數存在 localStorage（`jiujiu-meteor-unlock`），刪 App 重裝就重來。這是可以接受的設計，商店也不要求。
- 子代理在瀏覽器裡 1 秒內連續重新載入時，看過兩次試玩次數沒存到。間隔拉到 1.5 秒就正常，**很可能是測試環境的問題**，列出來給 TestFlight 時留意。

---

## C. 新玩家前 10 分鐘（390×844、繁中、全新安裝）【實測】

**做得好的**：
- 一進來自動問名字，有哥哥／姊姊等建議，不給「新增」，流程很清楚。
- 主選單五張卡加小標籤（全部都練、練速度…），不用捲動。
- 第一次玩流星不問模式直接開始。
- 答錯時流星亮出答案、要照著再打一次，紅字說明清楚。
- 結果卡有「這次答錯的題目，再看一眼」。
- 第一天的任務對新手合理（玩 1 局哪個大、開 3 個寶箱、拆 5 顆炸彈）。

**C1. 第一局唯一的引導只停留約 1 秒【實測＋讀程式】**
- **證據**：`index.html:2161` 用 `ftxt()` 顯示「打出答案，就能打下流星」，這是一個往上飄的浮字，壽命只有 1.15 秒（`index.html:2102`）。
- **情境**：小三孩子還沒讀完就消失了。這是新玩家唯一的操作提示。
- **建議**：改成停在鍵盤上方的固定提示（像錯題提示那樣），等孩子按下第一個數字才消失。

**C2. 寵物取名、餵食、照顧沒有實測到**
- 子代理的腳本沒走完挑蛋流程，所以「挑蛋 → 取名 → 第一次餵食」是**沒驗證**的路徑。建議 TestFlight 時讓孩子自己試。

**C3. 家長第一次看到的資訊**
- 關於頁寫了遊戲目的、五個遊戲各練什麼、隱私，很好。
- 但家長要找「怎麼買、多少錢」得進設定 → 家長區，第一次打開不會知道。這是**刻意設計**（購買不在孩子面前跳出來），符合 1.3，不建議改。

---

## D. 錯誤、邊界與排版【實測】

**測了沒問題的**：
- 三語言 × 六尺寸 × 21 個畫面，共 378 組，沒有：水平捲軸、露出 key 名稱、英日文漏翻（英日只有作者名「指數三寶飯」是中文，屬刻意保留）。
- 三語的 key 集合完全一致，`{參數}` 也一致。
- 6 種壞存檔都能正常進主選單、寵物、星圖、設定，沒有 JS 錯誤：`constructor`／`__proto__`、陣列、非 JSON、巨大數字等。
- localStorage 一律寫入失敗（模擬儲存空間滿了）也能照常玩。
- 多人：新增到 4 人、切換、改名、同名擋掉、刪人走家長關卡、localStorage 沒有殘留。
- 備份：匯出備份碼、前後多貼文字也能匯入、壞資料顯示「看不懂」、匯入後重新載入。
- 切到背景：流星立刻暫停，回來仍是暫停卡，分數不變。
- 五個遊戲各打一局，結果卡與「再玩一次」都正常。全程 0 個 JS 錯誤。

**小問題（美感）**：
- **D1.** 日文 320×568 的幽靈說明最後一個「う」單獨掉到下一行，違反「不留單一個字在下一行」的慣例。截圖：scratchpad `play/t2-320x568-ja-ghost.png`。
- **D2.** 320 寬時，名字長的玩家會讓設定卡標題「せってい（小星星星星）」「Settings (Alexandra)」變成兩行，備份卡標題同樣兩行。
- **D3.** 英文 320 寬的幽靈題號顯示成「Question 1·/ 20」，點和斜線擠在一起。
- **D4.** iPad 橫向（1180×820）的主選單只用了中間約 1/3 寬，字很小；星圖底部圖例貼底被切；寵物頁照顧區要捲才看得到。能玩，但 iPad 的審核員和家長會覺得「這是手機版放大」。平板直向比較好。
- **D5.** 改名成已存在的名字時，名字確實沒變，但子代理沒抓到提示文字。請你在手機上試一次有沒有 toast。
- 寵物頁點心鈕的「♥最愛」標籤，掃描器報「溢出」。我看過截圖，是刻意騎在邊框上的設計，**不是問題**。

---

## E. 效能與耗電

- **E1. 主選單也每一幀整張重畫【讀程式；推測影響】**
  - `frame()`（`index.html:4337` 起）每幀都畫完整的星空、月亮、小鎮。在主選單、寵物頁、星圖，每幀還要量一次元素位置（`getBoundingClientRect`）。
  - iPhone Pro 是 120Hz 螢幕，孩子停在主選單或寵物頁看寵物走路時，也一直全速重畫，會耗電、發熱。
  - 建議：非遊戲畫面降到每秒 30 幀，位置只在 resize 或捲動時量。
  - 實測（無 GPU 的 Chromium）主選單與流星都穩定 60fps、沒有長任務，所以**不會卡**，只是耗電。
- **背景**：切到背景時主迴圈停止、Web Audio `suspend`，回來 `resume`（`index.html:4326`），正確。
- **音樂**：全部即時合成，沒有音檔，App 很小。

---

## F. 商店文案與資料

- **F1. 「新功能（What's New）」還寫 1.3**（`store/listing.json:8`、`22`、`36`）。第一版上架沒有這一欄，不影響送審。之後更新前要改成 1.4 或下一版的內容。
- **F2. 中文關鍵字重複了名稱裡的字**：「九九乘法」「乘法表」「遊戲」已經在名稱或副標題裡，Apple 會自己索引。`docs/store-listing.md` 自己也寫了「不要重複」。拿掉可以空出約 12 字，換成「九九表」「乘法練習」「數學遊戲」「國小數學」「小二」「小三」。
- **F3.** 英文關鍵字有「kids」。Apple 2.3.8 說「For Kids」這類字只留給 Kids 類別用；我們在 Kids 類別，所以沒問題。
- **F4. Google（之後）**：Data safety 對付款程式庫的「記錄元件」要不要申報，官方仍不明確。
  - 官方原文：用 Google Play 結帳時「you don't need to declare… financial transactions」，但「Libraries and SDKs」傳出裝置的資料要申報（https://support.google.com/googleplay/android-developer/answer/10787469 ）。
  - 維持 checklist 的結論：上架前問 Play 支援。
  - Google Families 政策沒有明文要求購買前要有家長關卡，付款由 Google Play 驗證；但禁止「overly aggressive commercial tactics」（https://support.google.com/googleplay/android-developer/answer/9893335 ）。現在的鎖卡文字符合。
- **F5. Google 開發者名稱**：checklist 寫「個人帳號同樣用本名」，不精確。
  - 顯示名稱「can be different from your legal name」，可以寫「指數三寶飯」。
  - 但法定姓名、國家，有營利時連完整地址，都會另外公開（https://support.google.com/googleplay/android-developer/answer/13628312 ）。
- **F6. repo 根目錄的 12 張 `shot24-*.png`／`shot25-*.png`** 是舊的測試截圖，會被 GitHub Pages 公開（`…/jiujiu-game/shot25-menu.png` 打得開）。不會進 App（`tools/make-www.mjs` 只複製 `index.html` 與 `assets/`），建議之後清掉。

---

## G. 好不好玩、商業化、行銷（建議，不是問題）

1. **核心設計很強**：
   - 錯題加權、重測、星圖、不給壓力。
   - 「孩子只覺得在玩，背後在補弱點」很少有 app 做得這麼細。
   - 家長最在意的「沒有廣告、不收資料、不催買」也做到了。
   - 這些是商店頁最大的賣點，第一張截圖可以考慮加一行標語（例如「錯題自動多練」），不用另外做行銷圖。
2. **試玩 3 局、US$2.99 很合理**。台灣 App Store 的價格會自動換算（約新台幣 90～100 元），家長的接受度應該不錯。
   - 可以觀察：多少人玩完試玩、多少人打開購買卡。但遊戲不收資料，**只能從 App Store Connect 的銷售數字看**。這是刻意的取捨。
3. **免費部分已經很完整**：流星、星圖、寵物、任務都免費，孩子可以一直玩。付費的四個遊戲裡，雙人拔河（親子對戰）最能打動家長。商店說明可以考慮把它往前放，或在截圖裡突出「跟爸媽比」。
4. **上架初期的宣傳**：
   - 粉專「指數三寶飯」本身就是管道。可以用 Offer Codes 送給老師、家長社團試用。
   - 台灣的國小老師社群、家長社團（例如「小學家長」類社團）對「無廣告、不收資料」很買單。
   - 之後上 Google Play 可以申請 **Teacher Approved**。官方寫「can opt in… cannot guarantee」，可以申請但不保證會通過。
5. **之後可以考慮的玩法**（ROADMAP 已有的「抓錯」「找朋友」）：「找朋友」是除法的前置，可以當下一版主打，也是之後「更新內容」的好理由。
6. **Android 收不收費**：如果 Android 完全免費，就不用公開地址，也不用設定付款資料。可以先免費上架累積評價，等 iOS 的銷售數字出來再決定。不過 Google 規定**已經以免費提供的 app 不能改成付費下載**，但可以之後加內購，所以這條路仍然通。

---

## H. 建議的處理順序

| 順序 | 事項 | 誰做 | 對應 |
|---|---|---|---|
| 1 | 決定 Kids 年齡層（建議 6–8），改 `docs/store-listing.md`、`launch-easy.md` | 你決定、上架 session 改文件 | A1 |
| 2 | 修家長關卡「取消」繞過 30 秒鎖 | 主開發 session | A3 |
| 3 | 補審核備註（關卡解法、測試路徑、試玩、隱藏配件） | 上架 session | A4 |
| 4 | 修截圖腳本的幽靈紀錄，App 模式重截主選單 | 上架 session | A6 |
| 5 | 分級問卷：Contests、Loot Boxes、暴力都答「無」，新題目都答「沒有」 | 你填表時照做 | A2 |
| 6 | 第一局提示改成固定、按鍵才消失 | 主開發 session | C1 |
| 7 | TestFlight 實機：購買、恢復、重裝自動解鎖、接電話後的音樂、Stage Manager、讓孩子自己挑蛋取名 | 你 | B1、B2、B4、C2 |
| 8 | 決定德州等州法怎麼處理（建議先上架、追蹤） | 你 | A5 |
| 9 | 其他小問題（日文孤字、320 寬標題兩行、iPad 橫向、耗電、備份寫入順序） | 之後的版本 | B3、D、E1 |

---

## 附：測試腳本與截圖
- 都在本次 session 的 scratchpad，**沒有進 repo**，session 結束後就不在了。
- 內容：Playwright 試玩、假 Capacitor 購買、壞存檔、文字 key 比對。
- 需要重跑時，請新的 session 照本文件的「實測」描述再做一次。
