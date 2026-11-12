# 上架前獨立審查（2026-11-12，兩輪合併版）

> 審查者：Claude（獨立審查 session，只審查、沒有改遊戲程式）。對象：版本 1.4，`main` 的 commit `40ae955`。
>
> **做了兩輪**，第二輪的子代理沒有拿到第一輪的結論，各自獨立審：
> - 第一輪（Opus 5.5 主審，試玩用 Sonnet）：文件、程式、試玩、官方規則。
> - 第二輪（Fable 5.2）：整份 JS 讀完加模擬、完整玩到魔王與寵物全流程、破壞性測試、逐國法規。
>
> 怎麼審的：
> - 讀文件與設定：`CLAUDE.md`、`docs/`、`store/listing.json`、`ios/`、`android/`、`capacitor.config.json`。
> - 讀外掛原始碼：`@capgo/native-purchases` 8.9.5、Capacitor 8.5.3（iOS 與 Android）。
> - 實際玩：Playwright（Chromium）開本機 `index.html`，三種語言，手機 320×568 到 390×844、iPad 直橫向與分割畫面寬度。
> - 模擬購買：假的 `window.Capacitor`，iOS 與 Android。
> - 查規則：Apple、Google 與政府的官方頁面，下面附網址。
>
> 標記：
> - **【實測】**：用腳本重現或在截圖上看到。
> - **【讀程式】**：只看了程式碼。
> - **【推測】**：沒辦法驗證，例如要真的 iPhone。
> - **【官方】**：讀到官方原文；**【二手】**：只有搜尋摘錄或非官方來源。
> - 🆕 是第二輪才發現的。

---

## 結論先講

**兩輪都沒有找到程式上「會壞掉、會算錯錢」的 bug。** 學習演算法、購買、恢復購買、存檔、備份、名字塞惡意程式碼，都實跑驗證過。

**但第二輪在「商店設定與文案」找到 3 個會被退件或下架的問題**，都不用改遊戲邏輯：

| # | 問題 | 嚴重度 |
|---|---|---|
| 1 | 🆕 **越南**要政府的遊戲許可，銷售地區要再排除越南 | 高 |
| 2 | 🆕 **Apple 版不能出現「Google Play」**（商店說明三語＋App 內關於頁） | 高 |
| 3 | 🆕 **付費協議、銀行、稅表全部生效後才能送審**，不然審核員買不了 | 高 |
| 4 | **Kids 年齡層只能選一個**，通過後不能改，也不能退出 Kids | 高（要你決定） |
| 5 | **家長關卡的 30 秒鎖按「取消」就能繞過** | 中（要修程式） |
| 6 | **審核備註要補**：關卡怎麼解、測試路徑、內購排除哪些地區 | 中 |

---

## A. 會被退件、下架，或要你決定的事

### A1. 🆕 越南：遊戲要有政府許可【官方，我親自讀過】
- **原文**：「The Vietnamese Ministry of Information and Communications (MIC) requires games to be licensed to remain available on the App Store in Vietnam.」（https://developer.apple.com/news/?id=06h4gf33 ）
- **影響**：次要類別選 Games、文案自稱遊戲，就落在這條。外國個人拿不到許可（需要當地公司，這句是二手）。
- **建議**：App 與 `unlock_all` 的銷售地區都**再取消越南**。`docs/launch-easy.md` 第 8、9 步與「記住三件事」要改，少 29 個地區，不是 28 個。
- **更省事的做法**：介面只有中、英、日，第一版改用「白名單」，只勾台灣、日本、美國、加拿大、英國、澳洲、紐西蘭、香港、澳門、新加坡、馬來西亞等。巴西、印尼這些規定不明的國家自然不在內。
- **其他國家**（第二輪查的）：
  - 南韓：分級編號只有 19 禁或賭博、性、暴力內容才必填；賣家資訊只針對住在韓國的開發者。**可留**。【官方】
  - 巴西：2026 年新的兒少數位法有域外效力、禁止兒童遊戲的戰利品箱。【二手】對外國小開發者的義務查不到官方說法。保守可排除。
  - 印尼：遊戲分級 2026 年起強制。【二手】Apple 沒有印尼欄位。保守可排除。
  - 日本：特定商取引法對「透過 App Store 賣內購的外國個人」要不要標示，查不到官方見解。**可留**，但建議問懂日本法的人。
  - 英國、魁北克、土耳其、印度、俄羅斯：沒讀到官方頁面，不下結論。

### A2. 🆕 Apple 版不能提到「Google Play」【官方，我親自讀過】
- **原文（2.3.10）**：「don't include names, icons, or imagery of other mobile platforms or alternative app marketplaces **in your app or metadata**」（https://developer.apple.com/app-store/review/guidelines/ ）
- **哪裡有**：
  - `store/listing.json` 三語的完整說明：「付款由 App Store／Google Play 處理」。
  - App 內關於頁 `about.buyL`（`index.html:1243`、`1393`、`1542`）：同一句，iPhone 上也會顯示。
  - `buy.codeAnd`（`index.html:1239` 等）有「Google Play」，但只在 Android 顯示，不影響 iOS。
- **建議**：
  - 商店說明拆成 Apple 版與 Google 版，Apple 版只寫「付款由 App Store 處理」。
  - 關於頁那句改成依平台顯示（iOS 只寫 App Store），或改成不點名的「付款由商店處理」。
- **不用改的**：隱私權政策與支援頁是網頁，不是 App 的 metadata，如實寫兩個商店沒有問題。

### A3. 🆕 付費協議、銀行、稅表要全部生效才送審【官方，我親自讀過】
- **原文**：「Paid In-App Purchases won't function in review until this agreement is active.」（https://developer.apple.com/help/app-review/before-submitting-for-review/configure-in-app-purchases ）
- **影響**：沒生效時，App 的購買卡會顯示「現在讀不到商店的商品」、購買鈕按不下去【實測】。審核員看到這個畫面就是 2.1(b) 退件。
- **建議的順序**：
  1. 協議顯示「有效」、銀行與稅表都完成。論壇說填完後約 2 小時商品才載得到【二手】。
  2. 在 TestFlight 打開購買卡，**確認看得到價錢**（例如「購買 NT$90」）。
  3. 這時才送審，而且 `unlock_all` 要跟版本放在同一次送審（已寫在 `launch-easy.md`）。
- **同一頁還寫**：內購不需要先通過審核就能在審核環境運作；如果內購有排除地區，要在審核備註寫明。

### A4. Kids 類別：只能選一個年齡層，而且進去就出不來【官方，我親自讀過】
- **原文**：
  - 「must be placed in **one** of three age bands… 5 and under, 6–8, or 9–11」（https://developer.apple.com/app-store/categories/ ）
  - 「You can't change this selection once your app is approved by App Review. The app and all subsequent updates will need to follow the Kids category guidelines」（https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating/ ）
- **文件寫錯的地方**：`docs/store-listing.md:147`、`docs/launch-easy.md:107`、`docs/store-checklist.md` 的決定紀錄都寫「6–8 ＋ 9–11」。
- **建議**：
  - 年齡層選 **6–8**（主要對象是小二、小三）。
  - 🆕 進 Kids 是**永久的**。代價是之後每一版都要守 Kids 規則：不能加第三方分析、連網功能要很小心。這個 app 現在完全符合，而且你本來就不打算做這些，所以我建議照原計畫進 Kids。但如果你將來可能想加雲端同步或統計，現在就只放 Education、分級 4+，不進 Kids。
- **Google 不受影響**：目標年齡可以複選。

### A5. 家長關卡的「連錯 3 次鎖 30 秒」按「取消」就能繞過【實測，兩輪都重現】
- **證據**：`index.html:3976` 每次打開都 `miss: 0`；`index.html:4122` 取消只做 `gate = null`。
- **實測**：第二輪連跑 8 輪「錯 2 次＋取消」共 16 次錯，一次都沒被鎖。簡單題的答案只有 136 種。
- **為什麼要緊**：購買和外部連結都靠這一關，Kids 1.3 要的就是孩子進不去。
- **改法**：錯誤次數改成跟 `gateWait` 一樣放在外面，取消不歸零，答對或鎖過後才歸零。

### A6. 審核備註要補的內容【官方】
- **規則**：2.3.1(a)「must be described with specificity in the Notes for Review… (generic descriptions will be rejected)」；2.5.19「Don't include any hidden, dormant, or undocumented features」（2026-10-16 新增，https://developer.apple.com/news/?id=92th7e5i ）。
- **建議補上**：
  1. **家長關卡怎麼解**：「Parental gate: solve the arithmetic shown, e.g. 5 + 2 × 13 = 31 (multiply first). Three wrong answers lock it for 30 seconds.」
  2. **到購買畫面的最短路徑**（第二輪實測，全新安裝 4 個動作）：關掉取名卡（✕）→ Settings → For grown-ups → Unlock all games → 解一題 → 購買卡。
  3. 🆕 **內購排除的地區**：「The in-app purchase is not sold in China mainland, the EU, or Vietnam, matching the app's availability.」（A3 那頁要求寫）
  4. 四個付費遊戲各有 3 局試玩；隱藏配件、傳說蛋、星塵換徽章都是玩出來的，不能用錢買。
  5. Restore Purchases 與 Offer Code 兌換在購買卡裡。

### A7. 年齡分級問卷：有幾題容易答錯【官方】
- **Contests（競賽）**：答「Frequent」會變 13+，就進不了 Kids。遊戲沒有線上排行、沒有跟別的玩家比，答「**無**」。
- **Loot Boxes**：定義是「randomized virtual items **for purchase**」。遊戲的寶箱不能買，答「**無**」。（答有的話，在巴西會變 18+。）
- **Cartoon or fantasy violence**：建議答「無」；答 Infrequent 是 9+，仍可進 Kids。
- **新題目**都答沒有：In-App Controls、社群媒體（2026 年 9 月起必答）、Shared Location 與 Dating（2026-11-16 起）。
- 🆕 `docs/store-listing.md` 寫「問到 App 內購買就照實回答有」，但 Apple 的分級問卷**沒有內購這一題**，這句要拿掉。
- 來源：https://developer.apple.com/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions

### A8. 美國州法（德州、猶他、路易斯安那）【官方；要你決定；我不是律師】
- **現況**：德州 SB2420 的禁制令被撤銷，**2026-06-04 起生效中**（https://developer.apple.com/news/?id=sg176nne ）。猶他 2026-05-06、路易斯安那 2026-07-01（https://developer.apple.com/news/?id=f5zj08ey ）。
- **Apple 做的**：新帳號確認年齡、未成年人下載與內購要家長同意。
- **Apple 對開發者說的**：「In regions where legally required, you need to check the age… with the Declared Age Range API… consult your legal counsel」（https://developer.apple.com/support/age-assurance ）。沒說不做會退件，也沒說兒童 app 可以豁免。
- **對這個 app**：把所有人都當兒童、不收資料、沒有分齡內容，實務風險低。程式已處理的「付款處理中」剛好對應家長同意的流程。
- **建議**：第一版不接這些 API（要加原生程式，違反「不再加外掛」），在文件記一筆「重大改版（新增內購、連網、收資料）前要重新評估」。
- **COPPA**：管的是向兒童收集個資的業者；不收集就沒有同意與通知義務。風險低。

### A9. 🆕 台灣：遊戲軟體分級【官方條文；實務不明】
- **條文**：《遊戲軟體分級管理辦法》第 10 條第 2 項，上市前要把分級級別登錄到主管機關的資料庫；條文沒有寫教育類或 App 商店可以豁免（https://law.moj.gov.tw/LawClass/LawAll.aspx?PCODE=J0030086 ）。
- **不確定的地方**：個人做的教育 app 實務上會不會被要求，查不到官方說法。
- **建議**：上架前到數位產業署的分級查詢網自評登錄（應該是普遍級），或寫信問。成本很低。

### A10. 商店截圖【實測＋官方】
- **幽靈競速「最佳 2.2 秒」**：截圖的主選單這樣寫，但 20 題不可能 2.2 秒。`tools/store-screenshots.cjs:49` 種的是每題時間，遊戲存的是累計時間（`index.html:3908`）。改成累計值再重截。
- **付費遊戲沒標出來**：2.3.2 要求截圖看得出哪些要另外買。截圖用的是網頁版，沒有「免費試玩 3 次」牌子。建議用 App 模式重截主選單。風險低到中（說明文字有寫清楚）。
- **必填尺寸**：iPhone 1206×2622（已有）、iPad 13" 2064×2752（已有，因為支援 iPad 所以必填）。6.9" 是選填。2027 年 4 月起還要 iPhone Duo 尺寸。
- 來源：https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications

### A11. 最低功能（4.2「網頁包裝」）【官方；推測】
- 仍是最主要的未知風險。App 完全離線、有即時合成音樂、存檔、內購、多人，比一般網頁包裝扎實。
- 審核備註強調這些，**不要主動提「網頁版免費」**。隱私權政策提到網頁版是如實揭露，保留。

### A12. Privacy Manifest、SDK 簽章、App 隱私【官方；推測】
- `PrivacyInfo.xcprivacy` 宣告不追蹤、不收集，跟「Data Not Collected」一致。Capacitor 與外掛都沒用到要申報理由的 API。上傳後如果 Apple 寄信說缺，再補。
- Apple 的第三方 SDK 名單有列 Capacitor（https://developer.apple.com/support/third-party-SDK-requirements/ ）。專案用 binary 形式引入，第一次建置後看一下簽章欄位。
- 用 StoreKit 仍可填「Data Not Collected」：「You are not responsible for disclosing data collected by Apple」（https://developer.apple.com/app-store/app-privacy-details/ ）。

---

## B. 🆕 第一次用 GitHub 打包 iPhone 版，最可能卡住的地方【讀程式，沒有 Mac 可驗證】

給上架 session 參考：

1. **缺檔**：`ios/.gitignore` 排除了 `App/App/public`、`capacitor.config.json`；`www/` 不進版控；`Package.swift` 指到 `node_modules/@capgo/native-purchases`。**一定要先跑 `npm ci && npm run sync`**。
2. **簽章**：`project.pbxproj` 沒有 `DEVELOPMENT_TEAM`，只有自動簽章。CI 要帶 Team ID 與 API 金鑰（`-allowProvisioningUpdates`）。不要在命令列全域加 `PROVISIONING_PROFILE_SPECIFIER`，Swift Package 的 target 會報錯。
3. **流水號寫死**：`project.pbxproj:328` 是 `CURRENT_PROJECT_VERSION = 1`，第二次上傳會被拒。CI 帶 `CURRENT_PROJECT_VERSION=$GITHUB_RUN_NUMBER`。
4. **Xcode 版本**：外掛的 `Package.swift` 會偵測 Xcode 的 StoreKit 版本決定編譯旗標。CI 用 runner 預設的最新 Xcode，或明確設 `DEVELOPER_DIR`。現在最低要 Xcode 26（iOS 26 SDK）。
5. **沒有 shared scheme**：`xcodebuild -scheme App` 多半能自動產生；失敗就在 Xcode 勾 Shared 再進版控。
6. **API 金鑰**【官方＋二手】：帳號持有人要先在 App Store Connect 按「Request Access」。雲端簽章建議用 Admin 角色的 Team key（論壇回報，官方沒寫）。
7. **TestFlight**【官方】：內部測試 100 人免審；外部測試要過 Beta 審核。TestFlight 的內購是沙盒，不扣款。

**已核對沒問題的**：
- App 圖示 1024 沒有透明通道。
- Info.plist、AppDelegate、SceneDelegate 跟 Capacitor 8.5.3 範本一致。
- `ITSAppUsesNonExemptEncryption` 是 false。
- 桌面名稱四個語系都有。
- iPad 四個方向都支援。
- 最低 iOS 15。
- 版本號四處都是 1.4。

---

## C. 程式問題

### 會影響 iPhone 首發的

**C1. 🆕 魔王剛進場時壓到分數與血條，飛彈提示被發射鈕蓋住【實測，我看過截圖】**
- 390×844、第 5 波有飛彈時：魔王從上面掉下來，蓋住 HUD 的分數；血條被題目框蓋住只露兩端；「有飛彈！按「發射」」最後一個字被發射鈕壓到。
- 每次魔王經過這段都會發生，只是幾秒。

**C2. 🆕 買完以後，購買卡唯一的按鈕還寫「之後再說」【實測】**
- 卡上寫「已經解鎖了，謝謝你的支持！」，下面是「之後再說」（Not now／あとで）。每個付費的家長都會看到。解鎖後改成「好」。

**C3. 🆕 320 寬的購買卡，「之後再說」被切在卡片外【實測，我看過截圖】**
- 320×568 三語都要在卡內捲動才看得到；375 寬就放得下。
- 會遇到的裝置：iPhone SE 第一代，還有 **iPad 分割畫面最窄那一格**（審核員可能會試）。

**C4. 「購買前詢問」送出後還能再按購買【讀程式】**
- `index.html:4067`，顯示「處理中」後購買鈕又能按，家長會收到好幾個請求。

**C5. 🆕 商店回空商品時不會自己重試【實測】**
- 要關掉購買卡再開才會重問。建議 2～3 秒後自動再問一次，網路慢時審核員才不會看到按不下去的鈕。

**C6. iOS 被來電打斷後音樂可能不回來【推測】**
- `index.html:1854` 只處理 `'suspended'`，iOS 被打斷是 `'interrupted'`。改成「不是 running 就 resume」。

**C7. 🆕 支援頁沒提 iPhone 靜音鍵【已查】**
- 遊戲聲音跟著側邊靜音鍵，家長會以為壞了。支援頁三語各加一句「沒聲音請先檢查靜音鍵與音量」。

**C8. iPad 台前調度把視窗拉矮，會出現關不掉的「請轉直」【推測】**
- `index.html:4332` 的條件（橫向、高度 < 500、觸控）在 iPad 小視窗也成立。

### 只影響 Android（上架 Android 前要修）

**C9. 🆕 小螢幕 Android 手機打名字時，被「請把手機轉直」蓋住【模擬重現；沒有實機】**
- **原因**：Capacitor 8 在鍵盤彈出時把網頁畫面縮掉鍵盤的高度。360×640 的手機剩約 360×316，寬大於高，`index.html:202` 的條件就判成橫拿。
- **實測**：360×640、384×640、320×568 都出現；360×740 以上正常。
- **情境**：舊款、平價的 Android 手機（常是給孩子的舊機），第一次打開自動跳取名，孩子只看到「請轉直」，怎麼轉都沒用。
- **改法**：CSS 與 `rotMQ` 兩處都加 `and (min-aspect-ratio: 3/2)`。
- iPhone 不受影響（鍵盤不會縮網頁高度）。

**C10. 🆕 付款中按 Home 再回來，購買鈕可能卡死【讀程式】**
- `index.html:4113` 回前景時會查一次購買紀錄；Android 外掛每次呼叫都先關掉舊連線，進行中的購買就永遠不回來。付款成功沒事（會解鎖），付款失敗就三顆鈕停用到重開 App。
- **改法**：回前景那行加 `&& !iapBusy`，購買加 90 秒逾時。

### 機率很低

- **C11.** 匯入備份寫到一半失敗（儲存空間滿），可能留下新舊混合（`index.html:4183`）。先全部準備好再開始刪寫。
- **C12.** 試玩次數存在 localStorage，刪 App 重裝會重來。可接受。

---

## D. 體驗與設計（第二輪玩完整流程看到的）

**D1. 第一局唯一的引導只停約 1 秒【實測＋讀程式】**
- `index.html:2161` 的「打出答案，就能打下流星」是往上飄的浮字，壽命 1.15 秒（`index.html:2102`）。改成固定在鍵盤上方，按下第一個數字才消失。

**D2. 🆕 試玩一進去就扣，倒數中退出也算一局【實測】**
- 點幽靈競速 → 倒數時按「主選單」，重複 3 次，第 4 次就鎖了，一題都沒答。
- 符合規格（每局開始 +1），但孩子誤點、審核員隨手點就會燒光試玩。建議改成「答了第 1 題」或「倒數結束」才算。

**D3. 🆕 任務全完成寫「明天再來」【實測】**
- 三語都有（See you tomorrow／また明日ね）。`CLAUDE.md` 在換徽章那段明寫「不寫明天再來，不催孩子回來」，這裡不一致。Kids 類別也比較在意這種字眼。

**D4. 🆕 鎖卡的主要按鈕（黃色、在上面）是「給大人看」【實測】**
- 文字沒有催買，符合規格。只是視覺重點在通往購買的那顆。建議對調，讓「好」當主要按鈕，對 Kids 審核更保守。
- 另外標題「試玩用完囉」與內文「試玩結束了」重複。

**D5. 🆕 星圖說「沒有特別容易錯的題目」，錯題本同時列了 5 題【實測】**
- 只練加減時看到。兩邊門檻不同，家長會覺得矛盾。

**D6. 🆕 說明文字與實際不符【讀程式】**
- `help.wrong` 寫「把那題的紀錄歸零」，實際是降到「熟悉中」，要再答對一次才亮星。

---

## E. 排版【實測】

**沒問題的**：三語 × 手機三種尺寸 × 24 個畫面、iPad 直橫向與分割畫面，沒有水平捲軸、沒有露出 key、沒有漏翻。繁中沒有簡體字或中國用語。

**小問題**（除了 C3）：
- 320×568 的 App 模式主選單要捲動（中 11px、英 23px、日 26px），英日第二排按鈕被切一半。
- 320 寬：難題家長關卡的英日文取消鈕切一半；鎖卡中文標題斷在「試／玩」中間；設定頁英日標題兩行。
- iPad 分割畫面 320×1024：月亮壓到標題（英文蓋住 Meteors 的 s）。
- 「50 連擊！無人能擋」折成兩行，「能擋」落單。
- 寶箱浮字（「追蹤飛彈 +1」）在高處會蓋住愛心與分數。
- 設定的乘法表方格在 320 寬是 33×44，不到 44px。
- 幽靈結果卡寫「最高紀錄 4.6 秒」，時間應該是「最快紀錄」。
- toast 會蓋住幽靈競速「你」那一道 2～3 秒。
- 日文 320×568 幽靈說明最後的「う」單獨一行。
- iPad 橫向主選單只用中間三分之一，字小。

---

## F. 英文、日文最值得改的句子（第二輪挑的；仍建議請母語者看）

| 語言 | key | 現在 | 建議 |
|---|---|---|---|
| en | `how.sub` | Think plus: 8 + 7 = 15 | Think addition: … |
| en | `c.n.same`／`c.n.behind` | All right! … | All correct! …（會被讀成 Alright） |
| en | `bomb.desc` | Tap every answer in the table… | Tap every answer from the bomb's times table… |
| en | `bomb.tag` | Find facts | Find multiples |
| en | `stage.3` | Grown-up | Adult 或 Big（跟家長區的 grown-up 撞名） |
| en | `b.fuse` | Still hidden: … | You missed: … |
| ja | `v.slip2` | つながすべる！ | ロープがすべる！（平假名連著難斷句） |
| ja | `how.near` | …、あと 1 で 15 | …、1 をたして 15（原句會讀成「還差 1」） |
| ja | `c.big`／`c.small` | いちばん大きい？ | いちばん大きいのは？ |
| ja | `map.weak` | いちばんまちがえる問題 | よくまちがえる問題 |

---

## G. 確認沒問題的（兩輪實跑）

**學習演算法**【實測，第二輪】
- 11 種設定各跑 2000～6000 題（只勾 2、只勾 12、標準、只練加減、都練、全錯）：沒有永遠不出的題、沒有壞掉的權重、沒有無窮迴圈。
- 4094 種乘法表組合跑炸彈、哪個大、魔王出題，零錯誤。
- 546 個字串 key 三語一致。

**計時**【實測】
- 幽靈切背景 3 秒，計時只多 3 毫秒；答錯停 3 秒時計時不動；流星切背景自動暫停。
- 同一幀按 20 鍵、連點暫停 30 次、結果卡瞬間狂點：狀態都乾淨。遊戲中跨日正常。

**安全**【實測，兩位子代理各自驗證】
- 玩家名字、寵物名字、備份的每個欄位塞惡意程式碼（`<img onerror>`、`<svg onload>` 等），從畫面輸入、備份匯入、直接改存檔三條路都試：**沒有任何程式被執行**。
- 6 種壞存檔、儲存空間滿，都不會黑畫面。

**內購**【實測＋對照外掛原始碼】
- 方法名、參數、回傳值、錯誤訊息都對得上 8.9.5。
- 11 種情境（成功、取消、處理中、商品回空、已擁有、家人共享、恢復購買沒紀錄、離線）結果都正確。
- 離線時不會把買過的人鎖回去。
- 孩子看得到的畫面（鎖卡、提醒卡、試玩提示）沒有價錢、沒有催買字眼。
- 提醒卡只在流星第 3、第 10 局回主選單各跳一次。

**完整流程**【實測】
- 流星打到魔王並打倒；一擊即死；連擊橫幅；飛彈。
- 幽靈贏與輸（輸了幽靈會放慢）。
- 拔河贏、輸、繩子變滑（44.6 秒與 89.3 秒）、真人雙邊同時按、大人加難。
- 哪個大全對；炸彈全拆與引線燒完。
- 寵物從挑蛋到究極、放回家、請回來、刪除。
- 加減與都練；乘法表範圍切換後紀錄分開存。
- 錯題本清除；每日任務全完成。

---

## H. 商業與其他

- 🆕 **小型企業計畫（抽成 15%）要自己申請**，不是自動的：「simply complete a few steps to enroll」。簽完付費協議就去申請。【官方】
- 🆕 **台灣商店的標準抽成** 2026-10-31 起由 30% 降為 26%（https://developer.apple.com/news/?id=w9mxlhek ）。【官方】
- 🆕 **稅表**：所有開發者都要填美國稅表，非美國人會導到 W-8BEN。台灣個人要不要辦營業登記，請問國稅局。【官方＋未查到】
- **Offer Codes**：非消耗型可用；每批最少 500 組、效期最長 6 個月；App 內兌換要 iOS 16.3 以上。【官方】
- **家人共享**：開了不能關。【官方】文件正確。
- **「新功能」欄**（`store/listing.json:8`、`22`、`36`）還寫 1.3。第一版用不到，之後更新前要改。
- **關鍵字**：中文「九九乘法、乘法表、遊戲」、英文 `game`、日文「ゲーム」跟名稱或副標重複，浪費字數。
- **Google（之後）**：
  - 現在一律要 API 36，延期已過（專案已是 36）。
  - Families 政策禁止用情緒操弄催內購；純兒童 app 不能有未核准的 SDK（Play Billing 是 Google 自家的，建議跟 Play 支援確認）。
  - 開發者名稱可以自訂，但法定姓名會另外公開，有營利時還有完整地址。
  - 2026-09-30 起開發者驗證在巴西、印尼、新加坡、泰國生效，2027 年全球。
- **repo 根目錄 12 張 `shot24-*`、`shot25-*.png`** 會被 GitHub Pages 公開，建議清掉。
- **文件過期**：`docs/native-build.md:38`、`64`、`79` 還寫 1.3、1.2；第 46 行說匯出匯入「留待之後決定」，其實已做。

**商業化與遊戲性的看法**：
1. 定價模式（免費＋一次買斷）對兒童教育類是對的；瓶頸是被看到，不是價格。
2. 免費內容很夠玩，轉換率可能偏低。可以不違規地做兩件事：試玩還沒用完時，每日任務照抽付費遊戲；商店截圖把「親子對戰」（雙人拔河）往前放，因為付錢的是家長。
3. 最有效的宣傳是老師：用 Offer Codes 送給國小老師、安親班。
4. 日本市場值得認真看，但日文一定要請母語者看過。
5. 流星防衛戰撐起大部分遊戲時間，長期會膩；可以偶爾出現特殊波（只出某個表的「特訓波」）。
6. 長期目標偏遠（傳說蛋至少 30 天），徽章 4 到 20 之間的獎勵間隔拉得開，中段容易流失。

---

## I. 建議的處理順序

**送審前一定要做**

| 順序 | 事項 | 誰做 | 對應 |
|---|---|---|---|
| 1 | 銷售地區再排除越南（或改白名單），改 `launch-easy.md` | 你決定、上架 session | A1 |
| 2 | Apple 版說明與 App 關於頁拿掉「Google Play」 | 上架 session＋主開發 session | A2 |
| 3 | 協議、銀行、稅表生效後，在 TestFlight 確認購買卡看得到價錢，才送審 | 你 | A3 |
| 4 | 決定進不進 Kids、年齡層選一個（建議進、選 6–8），改三份文件 | 你決定 | A4 |
| 5 | 修家長關卡「取消」繞過 | 主開發 session | A5 |
| 6 | 補審核備註 | 上架 session | A6 |
| 7 | 分級問卷照 A7 填 | 你 | A7 |
| 8 | 修截圖腳本、App 模式重截 | 上架 session | A10 |

**送審前建議做**

| 順序 | 事項 | 對應 |
|---|---|---|
| 9 | 買完後按鈕改「好」、320 寬購買卡放得下、空商品自動重試 | C2、C3、C5 |
| 10 | 第一局提示固定顯示；試玩改成答了第 1 題才算 | D1、D2 |
| 11 | 「明天再來」拿掉；鎖卡按鈕對調 | D3、D4 |
| 12 | 魔王進場的重疊 | C1 |
| 13 | 支援頁加靜音鍵說明 | C7 |
| 14 | 申請小型企業計畫；台灣遊戲分級登錄 | H、A9 |

**TestFlight 實機要試的**
- 購買、恢復、刪掉重裝後自動解鎖。
- 接電話後的音樂（C6）。
- iPad 台前調度、分割畫面（C8、C3）。
- 取名時鍵盤收起後畫面有沒有復位。
- 系統分享面板存備份檔。
- 讓孩子自己玩第一局。

**Android 上架前**：C9、C10。

**之後的版本**：E 的排版小問題、F 的英日文、耗電（主選單也全速重畫，建議非遊戲畫面降到每秒 30 幀）。

---

## 附：兩輪都沒測到的

- 真的 iPhone、iPad、Android 手機（只有瀏覽器模擬）。
- Xcode 建置、真實商店購買、家人共享、購買前詢問。
- 聲音（測試環境沒有聲音）。
- 系統分享面板、剪貼簿在 App 裡的行為。
- iPhone Duo 尺寸、減少動態模式。
- 100 連擊、傳說蛋實際解鎖、隱藏配件現身。

測試腳本與截圖在這次 session 的暫存區，**沒有進 repo**，session 結束後就不在了。

---

## J. 交辦清單（2026-11-12 整理，直接複製給對應的 session）

> 下面第 1、2 點 Ian 已在 2026-11-12 確認；第 3 點是建議，Ian 若決定不同，請照他說的改：
> 1. App 與 `unlock_all` 的銷售地區**再排除越南**（共排除中國大陸、歐盟 27 國、越南）。
> 2. **進 Kids 類別、年齡層只選 6–8**（核准後不能改、不能退出）。
> 3. 美國州法第一版不接 Declared Age Range；台灣遊戲分級由 Ian 自己去登錄。
>
> 依據都在 `store/prelaunch_review.md`（分支 `claude/prelaunch-review`），括號是節次。

### J1. 給「主開發 session」（改遊戲程式，`index.html`）

照 `CLAUDE.md` 的慣例做：介面文字三語都改、改了文字重跑 `tools/make-fonts.py`、改規則同步遊戲說明、最後 `npm run sync`。每項做完用 Playwright 驗證。

**送審前一定要改**
1. **家長關卡連錯 3 次鎖 30 秒可用「取消」繞過**（A5）：`index.html:3976` 每次開卡 `miss: 0`、`index.html:4122` 取消只做 `gate = null`。把錯誤次數改成跟 `gateWait` 一樣的模組變數，取消不歸零，答對或鎖滿 30 秒才歸零。驗證：錯 2 次＋取消重複幾輪，第 3 次錯就要鎖。
2. **iOS 不能出現「Google Play」**（A2，Apple 2.3.10）：關於頁 `about.buyL`（三語，`index.html:1243`、`1393`、`1542`）的「付款由 App Store／Google Play 處理」改成依平台顯示（iOS 只寫 App Store、Android 只寫 Google Play、網頁版兩個都寫或都不寫）。全文再搜一次 `Google`，確認 iOS 上看得到的地方都沒有。

**送審前建議改**
3. **買完後購買卡按鈕還寫「之後再說」**（C2）：解鎖後改成「好」（三語）。
4. **320 寬購買卡的「之後再說」被切在卡外**（C3）：320×568 三語都要不用捲就看得到全部按鈕（iPad 分割畫面最窄一格也是這個寬度）。
5. **商店回空商品時不會重試**（C5）：`iapNoProd` 時 2～3 秒後自動再問一次 `getProducts`。
6. **「購買前詢問」送出後還能再按購買**（C4，`index.html:4067`）：記一個待核准狀態，期間購買鈕停用、只留恢復購買。
7. **第一局的引導只停 1.15 秒**（D1，`index.html:2161`、`2102`）：改成固定在鍵盤上方，按下第一個數字才消失。
8. **試玩一進去就扣**（D2）：倒數中退出也算一局。改成倒數結束（或答了第 1 題）才 `UL.trial[m]++`，toast 也跟著移。
9. **任務全完成寫「明天再來」**（D3，三語）：拿掉，跟 `CLAUDE.md`「不催孩子回來」一致。
10. **鎖卡主次按鈕**（D4）：「好」當主要（黃色、上面），「給大人看」次要；標題與內文別重複「試玩用完／結束」。
11. **魔王進場時蓋住分數與血條、飛彈提示被發射鈕壓到**（C1）。
12. **iOS 被來電打斷後音樂可能不回來**（C6，`index.html:1854`）：`actx.state !== 'running'` 就 `resume()`。
13. **iPad 台前調度的「請轉直」**（C8，`index.html:202`、`4332`）與 **Android 鍵盤把畫面擠矮誤判橫向**（C9）：CSS 與 `rotMQ` 兩處都加 `and (min-aspect-ratio: 3/2)`。
14. `help.wrong` 說「歸零」但實際是降到熟悉中（D6），改說明。

**之後的版本（不擋送審）**
- Android 付款中回前景卡死（C10）：回前景檢查加 `&& !iapBusy`、購買加 90 秒逾時。
- 匯入備份寫入順序（C11）、E 節排版小問題、F 節英日文、非遊戲畫面降到 30fps。

改完後請：更新版本（若要改號，照 `CLAUDE.md`「發版要改」那幾處）、`npm run sync`、告訴上架 session 要重截截圖。

### J2. 給「上架 session」（文件、商店資料、打包）

**文件要改**（A1、A4、A7、H）
1. `docs/launch-easy.md`：
   - 第 8、9 步與「記住三件事」：銷售地區再取消**越南**（少 29 個）。
   - 第 12 步：Kids 年齡層**只選 6–8**，加註「核准後不能改、不能退出 Kids」。
   - 第 5 步：付費協議之外，**銀行、稅表（W-8BEN）也要完成**；全部生效後才送審（官方：協議沒生效，審核時內購不會動）。加一步「申請小型企業計畫（15%）」。
   - 第 10 步：API 金鑰要先由帳號持有人按 Request Access；建議 Admin 角色的 Team key。
   - 第 11 步加：TestFlight 打開購買卡**確認看得到價錢**，看到才可以送審。
2. `docs/store-listing.md`：
   - 第二節 Kids 年齡層改「6–8（只能選一個）」；分級問卷那列刪掉「問到 App 內購買就照實回答有」（Apple 問卷沒有這題），改寫 A7 的答法：Contests、Loot Boxes、暴力都答「無」，In-App Controls、社群、Shared Location、Dating 都答沒有。
   - 截圖表：必填是 iPhone 1206×2622 與 iPad 13"；6.9" 選填；2027 年 4 月起要 iPhone Duo。
   - 審核備註換成下面第 4 點的版本。
3. `docs/store-checklist.md`：同步上面幾點；Google API 36 的延期已過；抽成要自己申請小型企業計畫、台灣商店標準抽成 2026-10-31 起 26%；補「美國州法」「越南許可」「台灣遊戲分級」三條決定紀錄。`docs/native-build.md` 的 1.3／1.2 改 1.4，第 46 行備份已完成。

**商店文案**（`store/listing.json` → `python3 tools/make-listing.py`）
4. **Apple 版說明不能有「Google Play」**（2.3.10）：拆成 Apple 版與 Google 版（或在 JSON 加 `description_apple`），Apple 版只寫「付款由 App Store 處理」，三語。
5. `whatsNew` 三語從 1.3 改成 1.4 的內容（第一版不會用到，但先改好）。
6. 關鍵字拿掉跟名稱、副標重複的字（中文「九九乘法、乘法表、遊戲」、英文 `game`、日文「ゲーム」），換成新詞。

**審核備註**（英文，A6）——在現有版本上補：
```text
Parental gate: solve the arithmetic shown, e.g. 5 + 2 × 13 = 31 (multiply first). Three wrong answers lock it for 30 seconds.
Fastest path to the purchase screen on a fresh install: close the name card (✕) → Settings → For grown-ups → Unlock all games → solve the gate → purchase card (price, Buy, Restore Purchase, Use a promo code).
Each of the four paid games can also be tried 3 times; after that a card appears with "Show a grown-up", which leads to the same gate.
The in-app purchase is not sold in China mainland, the EU or Vietnam, matching the app's availability.
Hidden outfits (unlocked at 40 and 50 badges), the legendary egg and trading stardust for a badge are gameplay rewards earned by playing; none can be bought.
```
（不要提網頁版免費，A11。）

**截圖**（A10）
7. `tools/store-screenshots.cjs:49`：幽靈紀錄改成**累計**時間（例如每題約 2.5 秒、第 20 個約 50 秒），現在主選單顯示「最佳 2.2 秒」。
8. 用 App 模式（注入假 `window.Capacitor`）截主選單，讓四張付費卡帶「免費試玩」牌子（2.3.2）。等主開發 session 改完再一起重截全部。

**iOS 打包（GitHub Actions macOS）**（B 節）
9. 先 `npm ci && npm run sync`（`ios/App/App/public`、`capacitor.config.json` 不在版控）。
10. 簽章：帶 Team ID 與 API 金鑰、`-allowProvisioningUpdates`；不要全域加 `PROVISIONING_PROFILE_SPECIFIER`。
11. `CURRENT_PROJECT_VERSION=$GITHUB_RUN_NUMBER`（`project.pbxproj:328` 寫死 1）。
12. 用 runner 預設的最新 Xcode（至少 Xcode 26），或明確設 `DEVELOPER_DIR`。
13. 第一次建置後看 Capacitor xcframework 的簽章欄位（A12）。

**其他**
14. repo 根目錄 12 張 `shot24-*`、`shot25-*.png` 移掉（GitHub Pages 會公開）。
15. 支援頁 `support/` 三語加一句「沒有聲音請先檢查 iPhone 側邊的靜音鍵與音量」（C7）。
