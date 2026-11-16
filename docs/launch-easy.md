# 上架步驟（簡單版）

照順序做，一次做一步。每一步後面寫了「做完會怎樣」，看到就代表成功。卡住了就截圖給我。
詳細版（規則出處、為什麼這樣做）在 `docs/store-checklist.md`。

> 後台的按鈕名稱常常改，這裡寫的是大概的位置；找不到就截圖問我。

**順序**：先做 iPhone（第二關），Android（第三關）等決定好要不要收費再做。

---

## 第一關：不用花錢，先試

**1. 用 Android 手機試玩**
- 手機打開這個網址，下載後安裝：
  `https://github.com/ianyclin/jiujiu-game/releases/download/android-latest/jiujiu-meteor.apk`
- 手機會說「不明來源」，按允許。
- 玩看看：流星、幽靈（試玩 3 次後會出現鎖）、設定、備份紀錄。
- 這個版本**還不能真的買**（商店裡還沒有商品），按「購買」失敗是正常的。
- **2026-11 起 App 換了內部名稱**（`com.sanbaofang.jiujiu`），新版會變成**另一個 App**，不會覆蓋舊的。舊 App 的紀錄請先用「設定 → 家長區 → 備份紀錄」匯出，再到新 App 匯入；搬好再刪舊的。網頁版不受影響。
- 做完會怎樣：遊戲正常開、能玩、有聲音。

**2. 確認兩個網頁打得開**
- `https://ianyclin.github.io/jiujiu-game/privacy/`（隱私權政策）
- `https://ianyclin.github.io/jiujiu-game/support/`（支援頁）
- 做完會怎樣：兩頁都看得到字。

**3. 請朋友看英文、日文**
- 找會英文、日文的朋友看：遊戲畫面（設定裡可以換語言）、`store/listing.json` 的商店介紹。
- 有要改的，直接跟我說哪裡要改成什麼。

---

## 第二關：Apple App Store（每年 US$99）

**4. 註冊 Apple Developer**
- 事前：Apple ID 先開「雙重認證」（iPhone：設定 → 你的名字 → 登入與安全性）；準備信用卡（US$99／年）、身分證或護照。
- 在 Mac 開 `developer.apple.com/programs/enroll/` → Start Your Enrollment → 登入 → 選**網頁**註冊（不用 Apple Developer app）。
- Entity Type 選「**Individual / Sole Proprietor**」（個人）；公司要 D-U-N-S 編號，要等好幾週。
- 姓名要跟證件、信用卡一致（護照有英文就填英文）；這個名字會顯示在商店的「開發者」欄位（不是地址）。
- 付 US$99 → 收到「Thank you for purchasing」→ 等 Apple 開通 1～3 天，收到「Welcome to the Apple Developer Program」。
- 卡住：「enrollment could not be completed」多半是姓名對不上；被要求上傳證件就照做再等一兩天。
- 做完會怎樣：能登入 App Store Connect（`appstoreconnect.apple.com`）。

**5. 簽「付費 App 協議」、填銀行與稅表**
- App Store Connect → 商務（Business）→ 協議 → 付費 App（Paid Apps）→ View and Agree to Terms → Agree（按了不能撤回）。
- 同一行接著填**銀行帳戶**與**稅表**（照實填）。美國稅表每個人都要填，不是美國人會導到 **W-8BEN**。台灣個人要不要辦營業登記，請問國稅局。
- App 免費下載也要簽，因為裡面有賣東西。
- **協議、銀行、稅表三樣都顯示「有效」才可以送審**：Apple 說協議沒生效時，審核環境裡的內購不會動；審核員看到「讀不到商品」就會退件。
- 簽好後順便申請**小型企業計畫**（App Store Small Business Program，抽成 15%）：要自己申請，不是自動的。
- 做完會怎樣：協議狀態變成「有效」（可能要等一兩天）。

**6. 回答歐盟的問題（數位服務法）**
- 同一頁（商務 → 協議）往下捲到「合規（Compliance）」→ 數位服務法（Digital Services Act）→ 完成。
- 選「**這不是交易者帳號**」（This is not a trader account）→ 完成。不用填地址。
- 為什麼可以這樣選：我們**不在歐盟 27 國上架**（第 8 步會取消勾選）。Apple 說只在歐盟以外上架的人不算歐盟的交易者。
- 如果選「是交易者」，歐盟的商店頁會公開你的地址、電話、email。
- 做完會怎樣：「數位服務法」那一行顯示已完成。

**7. 登記 App 的身分證（Bundle ID）**
- `developer.apple.com` → Account → 憑證、識別碼與描述檔（Certificates, Identifiers & Profiles）→ 識別碼（Identifiers）→ ＋。
- 選 **App IDs** → **App** → 繼續。
- 說明：`jiujiu meteor`；Bundle ID 選「明確」（Explicit），填 `com.sanbaofang.jiujiu`（**一個字都不能錯，上架後不能改**）。
- 下面的功能清單不用勾（App 內購買本來就開著）→ 繼續 → 註冊。
- 做完會怎樣：識別碼清單裡多一行 `com.sanbaofang.jiujiu`。

**8. 建立 App**
- App Store Connect → App → ＋ → 新 App。
  - 平台：iOS
  - 名稱：`九九流星隊：九九乘法表練習`
  - 主要語言：繁體中文
  - 套件 ID：選剛剛那個 `com.sanbaofang.jiujiu`
  - SKU：`jiujiu-meteor`（自己看的代號，隨便填）
- 進去以後 → **價格與銷售地區**：
  - 價格：**免費**。
  - 地區：先全部勾，再**取消下面這些**：
    - **中國大陸**（有內購的遊戲要先拿政府的遊戲版號，沒有會被下架）
    - **歐盟 27 國**：奧地利、比利時、保加利亞、克羅埃西亞、賽普勒斯、捷克、丹麥、愛沙尼亞、芬蘭、法國、德國、希臘、匈牙利、愛爾蘭、義大利、拉脫維亞、立陶宛、盧森堡、馬爾他、荷蘭、波蘭、葡萄牙、羅馬尼亞、斯洛伐克、斯洛維尼亞、西班牙、瑞典
    - **越南**（越南政府要求 App Store 上的遊戲要有許可，外國個人拿不到）
  - 挪威、冰島、列支敦斯登、瑞士、英國**不是**歐盟，留著。
- 做完會怎樣：App 清單裡多一個「九九流星隊」。取消勾選完，銷售地區應該是全部地區少 29 個。

**9. 建立商品**
- 在這個 App 裡 → App 內購買項目 → ＋ → 選「**非消耗型**」。
  - 參考名稱：`解鎖全部遊戲`（自己看的）
  - 產品 ID：`unlock_all`（**一個字都不能錯，建立後不能改**）
- 進去以後：
  - 價格：US$2.99（其他國家讓它自動換算）
  - 銷售地區：跟 App 一樣，取消中國大陸、歐盟 27 國與越南
  - 在地化：繁中、英文、日文各一個名稱與說明：
    - 中：「解鎖全部遊戲」／「幽靈競速、雙人拔河、哪個大？哪個小？、炸彈拆除，買一次就能一直玩」
    - 英：「Unlock All Games」／「Ghost Race, Tug of War, Biggest? Smallest? and Bomb Squad. Buy once, play forever.」
    - 日：「すべてのゲームを解除」／「ゴーストレース、つなひきバトル、どれが大きい？、ばくだんかいじょ。一度の購入でずっと遊べます。」
  - 審核用截圖：先空著，第 11 步之後我幫你截。
  - **家人共享：打開**（已決定；打開後不能關）。
- 做完會怎樣：商品狀態是「缺少元數據」或「準備送出」。都正常。

**10. 在 Mac 上用 Xcode 打包上傳**
- 第一版在你自己的 Mac 打包（2026-11-12 決定）；GitHub 自動打包之後再做。
- 要先做完**第 7、8 步**（Bundle ID 登記好、App Store Connect 裡建好 App），不然上傳會失敗。
- 照下面的「**附錄：在 Mac 上用 Xcode 打包上傳**」一步一步做。
- 做完會怎樣：App Store Connect → TestFlight 裡看得到一個版本，你的 iPhone 的 TestFlight 收得到。

**11. 用 TestFlight 自己先玩**
- 在 iPhone 裝 TestFlight（App Store 搜尋），App Store Connect → TestFlight → 加自己和家人。
- 在 TestFlight 裡買東西**不會扣錢**，放心按。
- **先確認看得到價錢**：設定 → 家長區 → 解鎖全部遊戲 → 解一題 → 購買卡的按鈕要寫價錢（例如「購買 NT$90」）。如果寫「現在讀不到商店的商品」、按鈕是灰的，代表第 5 步還沒全部生效或商品還沒設定好，**這時不能送審**（填完後商品可能要幾個小時才讀得到）。
- 試：買一次、刪掉重裝會不會自己解鎖、「恢復購買」。
- （家人共享在 TestFlight 測不到，上架後才看得到。）

**12. 填資料、送審**
- 照 `docs/store-listing.md` 填：名稱、副標、說明、關鍵字、截圖（`store/screenshots/apple-*`）、支援網址、隱私權政策網址。
- 類別勾 **Kids**，年齡層**只能選一個**：選 **6–8**。⚠️ 審核通過後**不能改、也不能退出 Kids**，之後每一版都要守 Kids 規則（不能加廣告、第三方分析）。
- 年齡分級問卷：照 `docs/store-listing.md` 第二節填，全部答「無／沒有」。特別注意 **Contests（競賽）答無**（答「經常」會變 13+，進不了 Kids）、**Loot Boxes 答無**（遊戲的寶箱不能用錢買）。
- App 隱私：選「**不收集資料**」。
- 說明（Description）：複製 `docs/store-listing.md` 裡標「**Apple 版**」的那段（Apple 版沒有提到 Google Play，Apple 規定不能提別的商店）。
- 審核備註：複製 `docs/store-listing.md` 裡的英文那段（已經寫了家長關卡怎麼解、怎麼走到購買畫面、哪些地區不賣）。
- **送審時要把 `unlock_all` 一起勾進去**（第一個商品一定要跟 App 一起送）。
- 做完會怎樣：狀態變成「等待審核」，通常幾天內有結果。被退件就把信貼給我。

---

## 第三關：Google Play（之後再做）

> 還沒決定 Android 要不要收費。Google 規定**有在賺錢的個人帳號要公開完整地址**（不能用郵政信箱）。
> 如果 Android 版完全免費、沒有內購，就不用公開地址；決定好跟我說，我再改程式和這一段。

**13. 註冊開發者帳號**
- 到 Google Play Console（`play.google.com/console`）註冊，選「**個人**」。
- 要付 US$25、上傳身分證件驗證，可能要等幾天。

**14. 建立 App**
- 名稱：`九九流星隊：九九乘法表練習`；類型：**應用程式**；**免費**。
- （Google Play 在中國大陸本來就沒有開放，不用另外排除。）

**15. 做正式的安裝檔（AAB）→ 跟我說**
- 上架要的檔案跟試玩的 APK 不一樣，要用一把「上傳金鑰」簽名。我來帶你做。

**16. 上傳到「封閉測試」，找 12 個人測 14 天**
- 測試 → 封閉測試 → 建立版本 → 上傳 AAB，填 12 個人的 Gmail（他們要用 Android 手機）。
- 把「加入測試」連結傳給他們，每個人都要按「加入」再從 Play 商店安裝。
- 12 個人要**連續 14 天**都留著這個測試。

**17. 填商店資料**
- 照 `docs/store-listing.md` 複製貼上；截圖在 `store/screenshots/google-phone/`，圖示 `assets/icon/icon-512.png`，主圖 `store/screenshots/google-feature/`。
- 目標年齡：6–8、9–12；有沒有廣告：**沒有**。
- 「資料安全性」那一頁先截圖給我，我們一起確認再填。

**18. 申請正式版**
- 14 天到了，Play Console 會出現「申請正式版」→ 回答幾個問題 → 送出。

（如果 Android 也要收費：還要設定收款（付款資料）、建立 `unlock_all` 商品、把測試的人加到「授權測試」，到時我再補。）

---

## 上架以後：送朋友優惠碼

- **Apple**：App 內購買項目 → `unlock_all` → 優惠代碼（Offer Codes）。朋友在遊戲「設定 → 家長區 → 解鎖全部遊戲 → 使用優惠碼」輸入。
- **Google**（如果有收費）：營利 → 促銷代碼 → 建立。朋友在付款方式那裡選「兌換代碼」輸入。

---

## 你只需要記住三件事

1. 商品代號是 `unlock_all`，Bundle ID 是 `com.sanbaofang.jiujiu`，一個字都不能錯。
2. Apple 的銷售地區要取消中國大陸、歐盟 27 國和越南。
3. 卡住就截圖給我。

---

## 附錄：在 Mac 上用 Xcode 打包上傳

給第 10 步用。從零開始，大概 1 小時（第一次比較久）。每一段後面寫了「做完會怎樣」，看到就代表成功；看到紅字或跟這裡寫的不一樣，就截圖給我。

> 「終端機」：按 ⌘ + 空白鍵，打 `終端機`（或 `Terminal`），按 Enter。下面灰底的指令，**一次複製一行**貼進去、按 Enter，等它跑完（出現新的一行、可以再打字）再貼下一行。

### A. 第一次才要做：準備工具

**A1. 確認 Xcode 已經裝好、打開過一次**
- 第一次打開 Xcode 會問要不要裝元件，**iOS** 要勾。
- 做完會怎樣：看得到「Welcome to Xcode」視窗（可以關掉）。

**A2. 在 Xcode 登入你的開發者帳號**
- Xcode 選單 **Xcode → Settings（設定）→ Accounts（帳號）→ 左下 ＋ → Apple ID** → 登入（跟 App Store Connect 同一個帳號）。
- 做完會怎樣：清單裡出現你的 Apple ID，右邊 Team 寫 **YEN CHU LIN**，角色是 Account Holder（帳號持有人）。

**A3. 裝 Node.js（打包要用的小工具）**
- 打開 `https://nodejs.org` → 下載 **LTS** 版（標著 LTS 的那個按鈕，macOS 安裝檔 `.pkg`）→ 打開 → 一直按「繼續」裝完。版本要 **22 以上**。
- 打開終端機，貼：
  ```
  node -v
  ```
- 做完會怎樣：出現 `v22.…` 或更大的數字（例如 `v24.11.0`）。

**A4. 把專案下載到 Mac（git clone）**
- 在終端機一行一行貼：
  ```
  mkdir -p ~/Projects
  cd ~/Projects
  git clone https://github.com/ianyclin/jiujiu-game.git
  ```
- 如果跳出「需要安裝命令列開發者工具」：按「安裝」，裝完再貼一次最後一行。
- 做完會怎樣：家目錄的 `Projects` 資料夾裡多一個 `jiujiu-game`。**Ian 的 Mac 已經在 `~/Projects/jiujiu-game`（2026-11-12 下載），不用再做這步。**

### B. 每次打包都要做

**B1. 拿最新的版本、準備好檔案**
- 在終端機一行一行貼：
  ```
  cd ~/Projects/jiujiu-game
  git stash
  git switch main
  git pull
  npm ci
  npm run sync
  grep -c help-ver ios/App/App/public/index.html
  ```
  - `git stash`：把上次在 Xcode 選 Team 時改到的東西先收起來，不然 `git pull` 會卡住。收起來沒關係，B3 重選 Team 就好。
  - `git switch main`：一律用 main（上架 session 合併好的版本）打包，不要用其他分支。
  - 最後一行是檢查用：出現 **1 以上的數字**才代表 App 裡是最新的遊戲；是 0 就代表 `npm run sync` 沒跑到，截圖給我。
  - `git pull`：拿 GitHub 上最新的遊戲。顯示 `Already up to date.` 也是正常的。
  - `npm ci`：裝打包用的套件（第一次要一兩分鐘）。最後出現 `added … packages` 就是好了；有 `warn` 黃字沒關係，有 `ERR!` 紅字就截圖給我。
  - `npm run sync`：把遊戲複製進 iPhone 專案。最後出現 `Sync finished` 就是好了。
- **一定要跑 `npm run sync`**，不然 App 裡是空的或是舊的遊戲。

**B2. 用 Xcode 打開 iPhone 專案**
- 貼：
  ```
  npx cap open ios
  ```
- 做完會怎樣：Xcode 打開一個叫 **App** 的專案。第一次打開，左下或上面會寫「Resolving Packages」（下載套件），等它跑完再往下做（幾分鐘）。

**B3. 選 Team、確認 Bundle ID（B1 用了 `git stash`，所以每次都要重選 Team）**
- 左邊最上面點藍色的 **App**（專案圖示）→ 中間 **TARGETS** 底下點 **App** → 上面分頁點 **Signing & Capabilities**。
- **Automatically manage signing**（自動管理簽名）：**打勾**。
- **Team**：選 **YEN CHU LIN**。如果有兩個，選**沒有寫「(Personal Team)」**的那個（Personal Team 是免費帳號，不能上架）。
- **Bundle Identifier**：要是 `com.sanbaofang.jiujiu`，**一個字都不能錯**。不是的話**不要自己改**，截圖給我。
- 做完會怎樣：下面「Signing Certificate」那幾行沒有紅字。出現紅字（例如找不到 Bundle ID）就截圖給我：多半是第 7 步還沒做。
- 不用按「+ Capability」加東西（App 內購買本來就開著）。

**B4. 確認版本號與 build 號**
- 同一個畫面，上面分頁改點 **General** → **Identity** 那一區：
  - **Version**（版本號）：`1.4`。這是商店上給大家看的版本，要跟遊戲「關於」頁寫的一樣，**不要自己改**；發新版時我會在專案裡一起改好。
  - **Build**（build 號）：第一次上傳是 `1`。
- **build 號的規則**：同一個版本號每上傳一次，build 號就要**比上次大**（1 → 2 → 3）。上傳失敗、要重傳，或修了東西再傳一次，都要先把 Build 改大一號（直接在這個欄位改）。改了以後跟我說改成幾，我把專案裡的也改成一樣，下次 `git pull` 才不會打架。
- 換新版本號（例如 1.5）時 build 號可以從 1 重新開始。

**B5. 打包（Archive）**
- Xcode 視窗最上面中間，▶ 按鈕右邊有一個選裝置的地方，點它，選 **Any iOS Device (arm64)**（「任何 iOS 裝置」）。**不能選模擬器**（iPhone 17 這種寫 Simulator 的），選了模擬器 Archive 會是灰的。
- 選單 **Product → Archive**。
- 等它跑（幾分鐘，上面進度條跑完）。
- 做完會怎樣：自動跳出 **Organizer** 視窗，清單最上面是剛剛那一包（App 1.4 (1)）。
- 中途失敗（上面出現紅色 ✕）：點左邊紅色的錯誤，整個視窗截圖給我。

**B6. 上傳到 App Store Connect（Distribute App）**
- 在 Organizer 選剛剛那一包 → 右邊按 **Distribute App**。
- 選上傳到 App Store Connect 的那個選項（叫 **App Store Connect** 或 **TestFlight & App Store**，看你的 Xcode 版本）→ Next。
  - 如果有 **TestFlight Internal Only**（只給內部測試）：**不要選**，這種版本之後不能拿去送審。
- 後面幾頁照預設一直按 **Next**／**Upload**（簽名選「自動」Automatically manage signing）。
- 做完會怎樣：最後一頁寫 **Upload Successful**（或「已上傳」）。
- 卡住、出現英文錯誤：整個視窗截圖給我，**不要一直重按**（重傳要先把 build 號改大，見 B4）。

**B7. 等 Apple 處理**
- 上傳完 App Store Connect 要「處理」一下，通常十幾分鐘到一兩個小時，會寄信說處理好了。
- App Store Connect → App → 九九流星隊 → **TestFlight** 分頁，看得到 `1.4 (1)`。
- 如果它問「出口合規」（加密）：專案已經設定好「沒有用加密」，正常不會問；真的問了，截圖給我。

### C. 把自己加成內部測試員（第一次才要做）

**C1. 建一個內部測試群組**
- App Store Connect → App → 九九流星隊 → **TestFlight** 分頁。
- 左邊 **內部測試**（Internal Testing）旁邊的 **＋** → 名字打 `自己人` → 勾 **啟用自動發佈**（Enable automatic distribution：之後每次上傳都會自動送給群組裡的人）→ **建立**（Create）。

**C2. 把自己加進去**
- 左邊點剛建的 `自己人` → 右邊 **邀請測試員**（Invite Testers）→ 勾你自己 → **新增**（Add）。
- 家人要一起測的話：他們要先是 App Store Connect 的使用者（使用者和存取權限 → ＋ 邀請），才能加成內部測試員；不想這麼麻煩就先只加自己。

**C3. 第一次上傳的那一包，手動加進群組**
- 如果群組是在上傳之後才建的：點 `自己人` → **新增建置版本**（Add Builds）→ 選 `1.4 (1)` → 下一步 → 「要測試的內容」打 `第一版` → 新增。

**C4. 在 iPhone 上裝**
- iPhone 到 App Store 搜尋 **TestFlight**，裝起來。
- 你的 email 會收到邀請信，點「View in TestFlight」或在 TestFlight 裡直接看到九九流星隊 → **安裝**。
- 做完會怎樣：iPhone 桌面多一個九九流星隊（圖示旁邊有一個小橘點，代表是測試版）。接著做第 11 步。

### 之後改版要做什麼
只要做 **B1 → B4（Build 改大一號）→ B5 → B6**。A 和 C 只有第一次要做。
