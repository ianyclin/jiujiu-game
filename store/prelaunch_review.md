# 上架前獨立審查（2026-11-12，兩輪合併版）

> 審查者：Claude（獨立審查 session，只審查、沒有改遊戲程式）。對象：版本 1.4，`main` 的 commit `40ae955`。
>
> **做了兩輪**，第二輪的子代理沒有拿到第一輪的結論，各自獨立審：
> - 第一輪：文件、程式、試玩、官方規則。
> - 第二輪：整份 JS 讀完加模擬、完整玩到魔王與寵物全流程、破壞性測試、逐國法規。
>
> 2026-11-12 另加 **K 節「設計建議」**：不是上架必要，是「遊戲本身還能怎麼更好」。
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
15. **讀不到商品時，購買鈕看起來還是可以按**（2026-11-12 TestFlight 實機看到）：`index.html:4026` 有把 `#buy-go` 設成 `disabled`，但外觀還是亮黃色，按了沒反應，大人會以為壞掉。停用時改成灰色或半透明，或乾脆藏起來，只留「現在讀不到商店的商品，請稍後再試」。
16. **遊戲說明在 iPhone 上換行很亂、太長**（2026-11-12 Ian 在 TestFlight 實機回報，附三張截圖）：同一段裡有的行到右邊、有的行只到三分之二就換行。
    - 原因【推測，要在 iPhone 實機確認】：`index.html:524` 的 `.rules li{text-wrap:pretty}`。Safari 的 `pretty` 會重排整段讓各行長度接近，中文段落就被提早換行；Chromium 只調整最後幾行，所以電腦上測不出來。先改成一般換行（`text-wrap:wrap`）在 iPhone 看一次，確認是不是這個原因。
    - **Ian 想要的方向：分成精簡版和完整版。** 建議做法（細節由主開發 session 定、做完給 Ian 看）：說明卡標題列下面放兩顆切換鈕「簡單版／完整版」，預設簡單版；簡單版每個遊戲 2～3 句，只講怎麼玩、怎麼贏；完整版就是現在的內容。不建議叫「小朋友／大人」：完整版是細的規則，不是給家長的資訊（給家長的在設定 →「關於」），孩子也可能想看完整版。切換結果記在 `DB.set`（每個人各自的）。三語都要寫，重跑 `tools/make-fonts.py`，320×568 三語檢查。
17. **第一次取名的卡片加一列語言切換**（2026-11-13 Ian 決定）：語言現在跟著手機語言自動選（`langAuto()`，`index.html:1555`），手機設成英文的台灣家庭打開會是英文，要到「設定」第一列才改得到。
    - 只加在**全新安裝自動跳出的那張取名卡**（`#o-name` 的「誰在玩」取名流程，`WHO.asked` 那次）上面，一列小按鈕：中文／English／日本語，沿用設定頁 `#set-lang` 的按鈕與 `langName`，點了立刻 `setLang()`、整張卡換語言，並存進目前玩家的 `DB.set.lang`。
    - 之後從主選單「誰在玩」打開的取名、改名都**不顯示**；主選單**不加**語言鈕（孩子會好奇去按，換成看不懂的語言就回不來）。
    - 標籤沿用 `set.lang`（一律帶「Language」字樣）。320×568 三語檢查卡片不會多捲；改了文字重跑 `tools/make-fonts.py`。

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

7a. **關鍵字加上加減**（Ian 2026-11-12 提出：1.4 起有 20 以內加減，說明已寫但關鍵字沒有）：在拿掉重複字之後，中文加「加減法、20以內加減、進位、退位、湊十」，英文加「addition,subtraction,math facts」，日文加「たし算,ひき算,くり上がり,くり下がり」；跑 `tools/make-listing.py` 確認不超過 100 字。名稱、副標、完整說明不改（說明三語已有加減那段）。

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
8a. 五張截圖裡換一張成**加減**：流星防衛戰選「加減」、答錯後出現湊十／雙倍算法的畫面（或主選單副標顯示練加減），讓家長看得出不只練乘法。
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

### J3. 給「上架 session」：Bundle ID／套件名稱改成 `com.sanbaofang.jiujiu`（2026-11-12 Ian 決定）

**新名字**：`com.sanbaofang.jiujiu`（iOS Bundle ID 與 Android applicationId 都用這個）。舊的 `io.github.ianyclin.jiujiumeteor` 全部換掉。Ian 擁有 `sanbaofang.com`，但這件事**不需要任何 DNS／Cloudflare 設定**，網站也不搬。Ian 會自己在 Apple Developer 登記這個 Bundle ID（`docs/launch-easy.md` 第 7 步）。

**要改的地方**（`git grep -n "io.github.ianyclin"` 應該只剩文件裡說明「舊名字」的句子）：
1. `capacitor.config.json:2` 的 `appId`。**只改 `appId`**；同檔的 `server.hostname`／`scheme` **絕對不能改**（`CLAUDE.md`：改了 origin，localStorage 就看不到舊紀錄）。
2. `ios/App/App.xcodeproj/project.pbxproj:337`、`358` 的 `PRODUCT_BUNDLE_IDENTIFIER`（Debug、Release 兩處）。
3. `android/app/build.gradle:4` 的 `namespace` 與 `:7` 的 `applicationId`。
4. `android/app/src/main/java/io/github/ianyclin/jiujiumeteor/MainActivity.java`：搬到 `android/app/src/main/java/com/sanbaofang/jiujiu/MainActivity.java`，第一行改成 `package com.sanbaofang.jiujiu;`，刪掉舊的空資料夾。
5. `android/app/src/main/res/values/strings.xml:6`、`:7` 的 `package_name` 與 `custom_url_scheme`。
6. **`.github/workflows/android-apk.yml:83` 權限白名單**裡的 `io.github.ianyclin.jiujiumeteor.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION` → `com.sanbaofang.jiujiu.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`。**漏改 CI 會失敗**（這個權限名稱跟著套件名稱）。
7. 文件：`docs/launch-easy.md:59`、`61`、`68`、`157`；`docs/native-build.md:5`、`79`；`docs/store-checklist.md:75`、`163`（決定紀錄改成「2026-11-12 改為 `com.sanbaofang.jiujiu`」並寫原因：名字跟著自己的網域、不綁 GitHub 帳號）；`CLAUDE.md` 若有提到也一併改。

**不用改的**：商品代號 `unlock_all`、`capacitor.config.json` 的 hostname／scheme、存檔的 localStorage key、GitHub Pages 網址（隱私權政策、支援頁、網頁版都不動）。

**對已經裝了測試 APK 的 Android 手機**：新 APK 是另一個 App，不會覆蓋舊的，兩個並排、紀錄各自獨立。請在 `docs/launch-easy.md` 第 1 步與 Release 說明（workflow 的 release body）加一句：「2026-11 起 App 換了內部名稱，新版會變成另一個 App。舊 App 的紀錄請先用『設定 → 家長區 → 備份紀錄』匯出，再到新 App 匯入；搬好再刪舊的。」網頁版不受影響。

**驗證**：
- `npm run sync` 成功。
- push 後 Android Actions 綠燈，用 `aapt2 dump badging` 確認套件是 `com.sanbaofang.jiujiu`、權限白名單通過。
- iOS 那邊等 macOS 打包時，確認上傳到 App Store Connect 的 Bundle ID 是 `com.sanbaofang.jiujiu`，跟 Apple 後台登記的一致。
- commit 訊息用繁體中文，例如「Bundle ID／套件名稱改為 com.sanbaofang.jiujiu」。

---

## K. 設計建議（2026-11-12 加；**不是上架必要**，要不要做、何時做由 Ian 決定）

> 這一節回答「遊戲本身還有沒有建議」。**不要跟 J 的交辦混在一起做**：J 是上架要修的，K 是讓遊戲更好的，沒有 Ian 點頭不要動工。
>
> **怎麼來的**：八個角度（孩子的手感、學習科學、家長與老師、長期留存、無障礙、同類 App 與商店呈現、音效與視覺、五個遊戲的平衡）各自提建議，共 42 條。每一條再交給另一個子代理去推翻：遊戲是不是已經有了、有沒有違反 `CLAUDE.md` 的原則、證據重跑一次對不對。
> - 35 條查證完成：29 條**改小之後**值得做，6 條不建議做。沒有一條是照原提案通過的，下面寫的都是查證後縮小的版本。
> - 7 條的查證中途中斷（用量額度用完）。我自己對過程式碼行號、用算術核對，但沒有重跑模擬，下面標 **【未重跑】**。
>
> **所有數字都來自機器人和模擬，不是真的孩子。** 機器人一次只想一題、不會累、不會先偷看下一顆；孩子多快、多常按錯都是假設值。`ROADMAP.md` 也寫「參數先凍結，看孩子玩的狀況再調」。所以第一步是 K0 的觀察，不是改程式。模擬腳本放在審查 session 的暫存區，沒有進版控；要重現得重寫。

### K0. 先花 10 分鐘看孩子玩（不用改程式）

最好找一個「會背但還不快」的孩子，不要只看已經很熟的。

| 看什麼 | 記什麼 | 出現這種情況，就值得做 |
|---|---|---|
| 流星防衛戰 3 局 | 每局死在第幾波、玩了多久 | 多半死在第 2～4 波、兩三分鐘內結束 → K1 |
| 第 5 波的魔王 | 有沒有看過、有沒有打倒過 | 幾乎沒打倒過 → K1a、K1b |
| 幽靈競速第一局 | 有沒有贏新手幽靈 | 輸了 → K2 第 4 項 |
| 跟機器人拔河 5 局 | 贏幾局、一局多久 | 常超過 3 分鐘 → K2 第 6 項；幾乎全贏或全輸 → K4 的機器人階梯 |

### K1. 最重要的一條：流星防衛戰對「還不夠快」的孩子太難

三個角度（手感、無障礙、平衡）各自獨立發現同一件事。【子代理實測與模擬，查證者另寫機器人重跑；我用算術核對】

- **現象**：流星的落下時間、生成間隔、同時幾顆只看第幾波，不看孩子多快（`index.html:2169-2171`）。
  - 想 1.5 秒的機器人：打到第 9～11 波。
  - 想 3.0 秒、完全不會錯（＝遊戲自己的亮星門檻 `FLUENT_MS`）：每一局都停在第 4 波，約 160～170 秒，**見不到第 5 波的魔王**。
  - 想 3.5 秒、錯 12%：中位數第 2 波、91 秒、只答 18 題，79% 的局死在第 2 波以內。
  - 想 4.5 秒：第 2 波、約 90 秒。
  - **想 2.4～2.6 秒的孩子，兩組機器人結論差很多**（一組停在第 3 波，一組打到第 6～8 波），差在打字速度與答錯率怎麼假設。3 秒以上的三組結論一致。
- **為什麼**（算術）：第 2 波同時最多 3 顆、每顆 11 秒落地。想 3.5 秒加按兩個鍵，大約 4.5 秒一題，三顆輪一圈要 13.5 秒，比 11 秒長，所以再努力也會有流星落地。這不是「不會」，是速度跟不上，而速度正是孩子來這裡要練的。
- **為什麼重要**：流星是 App 版**唯一免費**的遊戲，也是每個新玩家的第一個遊戲。寶箱、魔王、飛彈這些主打內容，照模擬只有已經熟的孩子玩得到；而遊戲的對象正是「會但還不快」的孩子。拔河機器人已經會配合孩子的速度（`cpuBase()`，`index.html:2811`），流星沒有。
- **建議做法**（查證後的版本；原提案的參數會把最高分弄壞）：
  1. 開局時算一個節奏係數 `pace = clamp(1 + 0.6 ×（平均想答案時間 ÷ 2.2 秒 − 1), 1, 1.5)`，存在 `M.pace`，只乘在落下時間與生成間隔上，同時顆數不動。題庫照 `cpuBase()` 的取法，至少 5 筆紀錄才用。快的孩子 `pace = 1`，**完全不變**；孩子變快後自動回到原速。不做成設定開關。
  2. 還沒有紀錄的第一局：第 1 波照原速，第 2 波起用第 1 波量到的時間來算。不要預設放慢，不然快的孩子第一局分數虛高、之後破不了自己。
  3. `help.meteor` 三語加一句，照機器人那句的講法，例如「流星掉下來的速度，會配合你平常算題的速度」。重跑 `tools/make-fonts.py`，更新 `CLAUDE.md` 的流星規則。
- **同一套機器人試過這個版本**：快的不變；想 3.5 秒、錯 12% 的孩子，死在第 2 波以內從 79% 降到 29%，一局從 91 秒變 173 秒、18 題變 32 題；想 4.5 秒的到第 4 波、25% 見到魔王。分數仍然是越快越高（想 4.5／3.0／1.5 秒：2,090／4,330／10,895 分）。
- **代價**：最高分不再是完全同一把尺（慢的時候活得比較久）。上面的係數已經壓到「分數仍然越快越高」，但要真人驗證。

跟 K1 有關的三件事，建議一起評估：

- **K1a. 第一隻魔王對慢的孩子幾乎打不倒**【未重跑；程式與算術核對過】：第 5 波魔王 6 滴血（`index.html:2202`），約 25 秒落地（落下時間 × 2.6，`:2152`），要**一次答對**才扣血，題目又是孩子最弱的題。等於連對 6 題、每題含打字約 4 秒內。想 3 秒以上的孩子來不及，2.5 秒左右在邊緣。單一組模擬：普通孩子打倒率 2%，血量改 4 是 43%。建議 `hp = 3 + floor(wave/5)`（第 5 波 4 滴、第 10 波 5 滴），`help.meteor` 三語的「打中 6 下以上」同步改。
- **K1b. 每日任務會抽到做不到的任務**【未重跑；程式核對過】：`hardQuests()`（`index.html:3672`）只要流星最高分 ≥ 200，就開放「打倒魔王」「到第 4 波」「連擊 15」。孩子幾局內就會超過 200 分，但魔王打不倒的話，抽到那天就拿不到徽章（要三項全完成）。照抽法算，App 免費版可抽的任務少，約三成的日子會抽到魔王任務。建議改成「自己做到過才抽」：打倒過魔王才抽魔王任務；波數、連擊的目標跟著自己的最高紀錄。存檔要多兩個欄位（最高波數、最高連擊），在 `cleanRest` 補消毒，舊存檔當 0。
- **K1c. 掉心後這一波退一級**：快的孩子有明顯的斷崖（前面幾分鐘零威脅，然後十幾秒三顆心掉光）。做了 K1 之後還有的話，再考慮「掉一顆心，這一波的難度級數退一級，下一波恢復」。只把生成間隔放慢不夠（瓶頸是同時顆數 × 每題秒數 > 落地時間）。「老手縮短暖身」不建議做：前段大量答題本來就是這個遊戲的目的。

### K2. 工作量小、值得做的

| # | 做什麼 | 為什麼 | 查證 |
|---|---|---|---|
| 1 | 炸彈、哪個大：還沒全對過時，顯示「最多拆 N 顆／最多對 N 題」 | 這兩個遊戲唯一的紀錄是「全對的最快時間」。每格點錯 5% 時約三成的局全拆，10% 時約一成；沒全對過的孩子，卡片和結果卡的紀錄永遠是「—」 | 真的遊戲各跑 32 局 |
| 2 | 流星結果卡：破紀錄時標題用「新紀錄！」；差不到兩成時寫「只差 N 分就破紀錄」 | 現在破紀錄的標題仍是「小鎮撐不住了！」，另外三個遊戲的標題都會跟著成績換 | 三語實測 |
| 3 | 幽靈競速：真的追過幽靈那一下給回饋 | 賣點是追過自己，但追過的瞬間跟一般答對完全一樣 | 實測 |
| 4 | 幽靈競速第一局：新手幽靈配合孩子的速度 | 新手幽靈每題 3.6 秒含打字，大約要想得比 2.8 秒快才贏得了。還不熟的孩子第一局幾乎一定輸，而 App 版這是三次試玩的第一次 | 【未重跑】算術成立 |
| 5 | 炸彈加減版的引線固定 40 秒（乘法維持 25 秒） | 加減版 12 格都是算式，要一格一格算。逐格算的機器人每格 2.1 秒時只拆成 39% | 模擬；每格幾秒是假設 |
| 6 | 拔河對機器人：開局 120 秒後一拉 6 格 | 對機器人常拖到 2～3 分鐘、答 30～50 題，最慢一成的局超過 200～350 秒 | 重跑模擬成立；只砍掉特別長的局 |
| 7 | 星圖：「容易錯」框線加粗、「熟悉中」改虛線 | 紅綠色盲的孩子看這兩種是同一個顏色（色差從 34.6 掉到 5.6） | 色盲模擬實測，小格子不壓數字 |
| 8 | 徽章滿 50 個後不再顯示「星塵換徽章」 | 配件最高門檻是 50，之後換了什麼都不會解鎖，白花 ★300 | 實測 |
| 9 | 錯題本「全部清空」：走簡單的家長關卡，或直接拿掉這顆鈕 | 孩子兩下就能清掉，家長看到的弱點清單跟著消失（題目本身之後還是會再出） | 讀程式 |
| 10 | 星圖底部「清除所有紀錄」搬到設定的家長區 | 已有家長關卡，但跟刪除玩家同一個理由：紅色鈕太顯眼、孩子會試按 | 子代理順帶提的；我核對過位置 |
| 11 | 星圖全亮時慶祝一次，說明框換成「81 顆星全部點亮了！」 | 現在全亮的當下什麼都沒發生 | 實測 |
| 12 | 星圖：點同一格或空白處回到摘要；加一句「3 秒內想出答案算熟」 | 點過格子後摘要回不來；家長不知道秒數怎麼看 | 實測 |
| 13 | 卡片出現時加 0.18 秒進場動畫（兩行 CSS） | 現在所有卡片都是瞬間出現 | 注入 CSS 實測 |
| 14 | 破紀錄專用音效 | 破紀錄、每一波開始、魔王登場現在是同一個聲音 | 讀程式＋離線量音量；**要 Ian 用耳朵聽過再合併** |
| 15 | iPad 外接鍵盤：結果卡按 Enter＝再玩一次，暫停卡按 Enter＝繼續 | 現在 Enter 沒反應，Tab 要按 13 下才到按鈕 | 實測 |

給主開發 session 的細節（編號同上）。凡是新增介面文字：三語都加、重跑 `tools/make-fonts.py`、英日文要短到 320 寬不多一行；規則有變就同步 `help.*` 與 `CLAUDE.md`。

1. `BEST0`（`index.html:1597`）最後面加 `bombN: 0, cmpN: 0`；`cleanRest` 夾在 0～5／0～10；舊存檔已有全拆／全對時間的直接當滿。**只在還沒有全對時間時顯示**，有了之後一切照舊。破顆數紀錄只換 note 文字（寫「新紀錄！最多拆 3 顆」，不寫「比上次多」），不放彩帶：彩帶留給全對破時間紀錄。新字串不比現有 `best.bomb`／`best.cmp` 長。
2. 只動 `gameOver()`（`index.html:2514-2519`），標準與一擊即死共用。標題用現成的 `r.new`，note 新增兩個 key。第一次玩（舊紀錄是 0）不寫「比之前多」。
3. `updateGhost()` 在幽靈題數超過自己時記一個「落後過」的旗標；`ghostKey()` 答對後若從落後變領先就觸發一次（一聲 `SFX.ding`、`#g-you` 放大發光約 0.5 秒、`#g-prog` 換成「追過幽靈了！」）。平手不算、最後一題不算。**不做**「被追過」的回饋和「領先 N 題」字樣。
4. `index.html:2706`：沒有最佳紀錄時每題用 `max(3600, cpuBase() × 1.6)` 毫秒；`g.first` 三語的「每題 3.6 秒」改成帶參數。
5. 秒數存在每顆炸彈的 round 上，`index.html:3190-3192` 改讀它。最快紀錄量的是實際時間，不受影響。不做「依熟練度自動調引線」：模擬裡公式調不準，等真人資料。
6. `vForce()`（`index.html:2822-2826`）在機器人模式且開局 120 秒後回 6；新增 `v.slip6` 三語（例如「最後一拉！」）；繩子多一個樣式，`openVersusReset()` 要清掉。**雙人對戰不動**（兩個真人沒有追趕機制，120 秒後會變成誰先答對誰贏）。模擬裡孩子勝率會從 96%／83% 降到 90%／74%，但這兩個勝率本身就不確定，見 K4。
7. `.cell.weak`（`index.html:297`）加 `border-width:2px`、框色調亮；`.cell.learn`（`:296`）加 `border-style:dashed`；圖例 `:787-788` 同步。不加圓點。不用改文字。
8. `renderGear()`（`index.html:3352-3354`）在徽章數 ≥ `GEAR` 最高門檻時不畫 `#badge-buy`；門檻用 `GEAR` 算，不要寫死 50。
9. `index.html:3820-3825`。用 `openGate(fn, why, false)`（簡單題）；單題的「清除」照舊留給孩子。
10. `#map-reset`（`index.html:3652`）。
11. `starsNow() === starsMax()` 第一次成立時，沿用三項任務全完成那套 toast＋彩帶＋音效；旗標放 `DB.bests[bestKey()]`；之後星星暗掉不收回、不提示。加減星圖比照（64 格）。
12. 格子的 click（`index.html:3637-3651`）點到已選的同一格或格子外時呼叫 `mapInfoDefault()`。
13. `@keyframes cardIn{from{opacity:0;transform:scale(.94)}}` 與 `.overlay:not([hidden])>.card{animation:cardIn .18s cubic-bezier(.2,.9,.3,1.2)}`。不加在 `.screen` 上（跟拔河的開始卡會疊成三層），暗幕不淡入（設定、關於、備份互換時會閃）。
14. `index.html:3876` 的 `SFX.fan()` 換成新的 `SFX.record()`，音量在 `milestone(2)`～`(3)` 之間。不做「結束音」（輸的時候容易被聽成失敗音）。
15. `index.html:4214` 那串 keydown。條件：`e.target` 不是按鈕、卡片已出現 1.5 秒以上、只收 Enter。不動焦點。

### K3. 商店頁（併進 J2，跟已排定的文案修改、重截一起做）

1. **宣傳文字**（Apple 唯一不用點「更多」就看得到的文字，隨時可改、不用送審）三語加「一次購買、不是訂閱」和「錯題自動多練、星圖看得出哪裡還不熟」。不寫價錢。英文已用 125／170 字，要改寫才放得下。
2. 【給家長】的免費清單補上「錯題本」（現在漏了；實測沒解鎖也打得開）。【越玩越熟】加一點介紹錯題本。
3. 加一點：「沒有排行榜，最快紀錄只跟上次的自己比。星圖的星星看的是多久想出答案，不算打字時間。」**不要寫**「沒有計時」「零壓力」「不跟別的孩子比」：幽靈有計時、拔河就是對戰，寫了不實。
4. 日文：「設定で練習する段（1〜12）を選べます」從家長區第 6 點往上移成獨立一點；第一段明講這是「覚えたあとの仕上げ用」（日本同類 App 多半是教讀音的，定位要先講清楚）。繁中版同樣把「可以選乘法表」往上移。措辭交給母語者定。
5. J2 第 7a 項補充：英文關鍵字直接加 addition、subtraction 會超過 100 字，要先刪 game、multiply、education（改完 95 字）。不要加「一年級」「flash cards」：介面是寫給小三的，也不是字卡 App（Apple 2.3.7 要求關鍵字如實）。
6. J2 第 8a 項補充：加減那張建議「加第六張」，不要換掉現有的；最省事是加減星圖。
7. **截圖加一行標語、把玩法放第一張**【要 Ian 決定】：Apple 官方說明寫搜尋結果會露出前一到三張截圖，現在第一張是主選單。但 `docs/store-checklist.md:78` 的決定是「第一版用原圖、不加標語」。要改的話跟 A10 的重截一起做，只截一次；合成圖要確認字型真的載到、標語的字在字型子集裡。
8. **無障礙標籤**（Apple 的 Accessibility Nutrition Labels，目前自願填，Apple 說日後會變必填）：`docs/store-checklist.md` 加一節逐項寫現況。第一版只勾 Reduced Motion；VoiceOver 不勾（遊戲本體是畫布）；Sufficient Contrast、Dark Interface 先不勾。

### K4. 方向對，但等上架後有真人資料再決定

- **久沒碰的星星題優先複習**：現在星星亮了就不再特別安排。查證後效果比想像小（星星題本來平均兩三天會再出現一次）。要做就用窄版：只在星星題之間重新分配，不稀釋弱題；星星不變暗、畫面不顯示。放長假回來的孩子最可能受益。會多存「最後答對的日期」，要檢查隱私權政策。
- **家長的學習摘要**（每個乘法表一條進度、複製文字貼給老師、一次看所有孩子）：沒有家長提過這個需求。先做 K2 第 12 項，有人問再做。
- **家長區「鎖住練習設定」**：沒有證據孩子會偷改範圍，等有家長回報再做。
- **星圖播放「新亮的星星」**：每格一輩子只播一次。
- **音樂**：遊戲曲 7.6 秒一輪，五個遊戲共用同一首。**請 Ian 自己戴耳機連玩 5 分鐘**，真的膩了再加 B 段；寫程式的一方聽不到成品。
- **VoiceOver**：只可能先支援幽靈競速，而且要實機測過才能合併。
- **拔河機器人改成「輸了放慢、贏了加快」**【未重跑】：兩組模擬對普通孩子的勝率差很多（一組 96%、一組 52%，差在有沒有算打字和答錯的時間），所以現在的公式準不準只能看真人。K0 若觀察到幾乎全贏或全輸，就改成這種會自己校正的階梯（跟幽靈「連輸就放慢」同一個想法）。很快的孩子一定全贏這點是確定的：機器人最快 2.2 秒一題（`index.html:2815`）。
- **熟練的孩子任務太容易**【未重跑】：答對 30 題一分鐘就過。影響小。
- **乘法答錯時提示「你會 8 × 7，7 × 8 也一樣」**：只在對調那題已經是星星時給。先看真實存檔裡這種題有幾題，幾乎沒有就不用做。

### K5. 查過、不建議做的

| 提案 | 為什麼不做 |
|---|---|
| 今天打錯的題，隔天保證再考一次 | 提案的模擬算錯了。重算後，現有的加權已經讓大約八到九成的錯題隔天再出現，缺口只有一到兩成 |
| 打錯 a × b，把 b × a 也排進重測 | 會把真正打錯的題擠出重測名額。研究說的是「練 a × b 會帶動 b × a」，照原題重測就已經練到 |
| 「訪客」模式 | 未滿 4 人時新增一個名字就解決。放在孩子會開的名單裡，誤按後整場練習都不記錄，跟遊戲的核心相反 |
| 寵物第二隻起養久一點 | 空窗是「徽章 30 個」決定的，不是星塵；同一種蛋本來就能再養 |
| 中文加注音開關 | 實測注音字型寬 1.5 倍，主選單卡片撐破 320 寬；注音符號只有約 4px 高，看不清；「長大、音樂、重新」這類多音字預設讀音是錯的，孩子看得到的字約三成要人工校對 |
| 主音量限幅器、看算法時壓低音樂 | 量測顯示現在沒有破音；照提案的設定做反而有機率破音 |

### K6. 看過覺得已經做對、不用動的

- **學習設計**：以打答案為主軸、選擇題（哪個大、炸彈）只輕量記不點星、不計時施壓、答錯後隔 6～12 題重測一次。學習科學那個角度查了文獻，說這些方向都有研究支持（Ophuis-Cox 2023 小二乘法的提取練習、van Galen & Reitsma 2011 乘法交換律的遷移，這兩篇查證者有再讀過摘要；其餘【二手】，我沒有逐篇核對）。
- **定價與定位**：US$2.99 一次買斷落在同類 App 的區間內；「都會但偶爾背錯」的定位，同類 App 沒有人這樣講。
- **手感**：流星答對的回饋、炸彈爆炸後的說明（「2 × 9 = 18，差了 1」）、幽靈輸了下一局自動放慢、哪個大的節奏。
- **無障礙**：沒有只靠聲音傳達的資訊；減少動態處理完整；寶箱稀有度不只靠顏色；觸控目標夠大。
- **留存**：連續天數斷了不罰也不提醒；換徽章 ★300 的定價合理；難度在第 12 波左右封頂，高手仍有空間。

---

## L. Ian 的待辦（2026-11-12 起，做完就打勾）

### 優惠碼（`unlock_all`）
遊戲已經有「使用優惠碼」按鈕（購買卡，家長關卡後面；`index.html:4082`），兌換後會自動解鎖。**碼要自己在 App Store Connect 建**：App → 內購 → `unlock_all` → Offer Codes → Create Offer。建好不能改，要改就另建一個。依據：[Create offer codes for In-App Purchases](https://developer.apple.com/help/app-store-connect/manage-in-app-purchases/create-offer-codes-for-in-app-purchases/)【官方】。

- [ ] **TestFlight 時**：建一批**沙盒碼**（10～10,000 個，App 還沒上架也能建），用沙盒測試帳號在 iPhone 實測「購買卡 → 使用優惠碼 → 輸入 → 自動解鎖」。順便確認 iOS 16.3 以前會提示改去 App Store 帳號頁兌換。
- [ ] **上架、內購審核通過後**：建一個**免費**的優惠活動（Free Offer）。
  - 送親友、老師、粉專活動：用**自訂碼**（自己取名，例如 `JIUJIU2026`），設兌換次數上限與到期日（最長 6 個月）。
  - 要一人一碼：用**一次性碼**（一批 500～25,000 個，一定要設到期日）。
  - 資格可限定「從沒買過」的人；地區跟 App 一樣（不含中國大陸、歐盟、越南）。
  - 一個 App 同時最多 10 個有效活動；每季最多 100 萬個碼。
- [ ] Android 上架時：Google Play 的優惠碼另外在 Play Console 建；遊戲裡沒有輸入框，要在 Play 付款畫面選「兌換代碼」，回到遊戲會自己檢查（3 天內要確認，遊戲已處理）。
