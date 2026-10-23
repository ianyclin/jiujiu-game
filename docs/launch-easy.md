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
- 到 `developer.apple.com` 用你的 Apple ID 註冊，選「**個人**」，付 US$99／年。
- Apple ID 要先開「雙重認證」。
- 個人帳號在商店上會顯示你的**本名**（不是地址）。
- 做完會怎樣：能登入 App Store Connect（`appstoreconnect.apple.com`）。

**5. 簽「付費 App 協議」**
- App Store Connect → 商務（Business）→ 協議 → 付費 App（Paid Apps）→ 填銀行、稅務（照實填）。
- App 免費下載也要簽，因為裡面有賣東西。
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
- 說明：`jiujiu meteor`；Bundle ID 選「明確」（Explicit），填 `io.github.ianyclin.jiujiumeteor`（**一個字都不能錯，上架後不能改**）。
- 下面的功能清單不用勾（App 內購買本來就開著）→ 繼續 → 註冊。
- 做完會怎樣：識別碼清單裡多一行 `io.github.ianyclin.jiujiumeteor`。

**8. 建立 App**
- App Store Connect → App → ＋ → 新 App。
  - 平台：iOS
  - 名稱：`九九流星隊：九九乘法表練習`
  - 主要語言：繁體中文
  - 套件 ID：選剛剛那個 `io.github.ianyclin.jiujiumeteor`
  - SKU：`jiujiu-meteor`（自己看的代號，隨便填）
- 進去以後 → **價格與銷售地區**：
  - 價格：**免費**。
  - 地區：先全部勾，再**取消下面這些**：
    - **中國大陸**（有內購的遊戲要先拿政府的遊戲版號，沒有會被下架）
    - **歐盟 27 國**：奧地利、比利時、保加利亞、克羅埃西亞、賽普勒斯、捷克、丹麥、愛沙尼亞、芬蘭、法國、德國、希臘、匈牙利、愛爾蘭、義大利、拉脫維亞、立陶宛、盧森堡、馬爾他、荷蘭、波蘭、葡萄牙、羅馬尼亞、斯洛伐克、斯洛維尼亞、西班牙、瑞典
  - 挪威、冰島、列支敦斯登、瑞士、英國**不是**歐盟，留著。
- 做完會怎樣：App 清單裡多一個「九九流星隊」。取消勾選完，銷售地區應該是全部地區少 28 個。

**9. 建立商品**
- 在這個 App 裡 → App 內購買項目 → ＋ → 選「**非消耗型**」。
  - 參考名稱：`解鎖全部遊戲`（自己看的）
  - 產品 ID：`unlock_all`（**一個字都不能錯，建立後不能改**）
- 進去以後：
  - 價格：US$2.99（其他國家讓它自動換算）
  - 銷售地區：跟 App 一樣，取消中國大陸與歐盟 27 國
  - 在地化：繁中、英文、日文各一個名稱與說明：
    - 中：「解鎖全部遊戲」／「幽靈競速、雙人拔河、哪個大？哪個小？、炸彈拆除，買一次就能一直玩」
    - 英：「Unlock All Games」／「Ghost Race, Tug of War, Biggest? Smallest? and Bomb Squad. Buy once, play forever.」
    - 日：「すべてのゲームを解除」／「ゴーストレース、つなひきバトル、どれが大きい？、ばくだんかいじょ。一度の購入でずっと遊べます。」
  - 審核用截圖：先空著，第 11 步之後我幫你截。
  - **家人共享：打開**（已決定；打開後不能關）。
- 做完會怎樣：商品狀態是「缺少元數據」或「準備送出」。都正常。

**10. 打包上傳 → 跟我說**
- iPhone 版要在 Mac 上打包。兩種做法，選一種跟我說：
  - **你有 Mac**：裝 Xcode，我一步一步帶你按。
  - **你沒有 Mac**：我可以設定 GitHub 幫我們用它的 Mac 打包上傳（不用另外花錢）。你只要在 App Store Connect 建一把「API 金鑰」給它，我會教你怎麼建、怎麼放（金鑰不要貼給我或貼在對話裡）。
- 做完會怎樣：App Store Connect → TestFlight 裡看得到一個版本。

**11. 用 TestFlight 自己先玩**
- 在 iPhone 裝 TestFlight（App Store 搜尋），App Store Connect → TestFlight → 加自己和家人。
- 在 TestFlight 裡買東西**不會扣錢**，放心按。
- 試：買一次、刪掉重裝會不會自己解鎖、「恢復購買」。
- （家人共享在 TestFlight 測不到，上架後才看得到。）

**12. 填資料、送審**
- 照 `docs/store-listing.md` 填：名稱、副標、說明、關鍵字、截圖（`store/screenshots/apple-*`）、支援網址、隱私權政策網址。
- 類別勾 **Kids**，年齡 6–8、9–11。
- App 隱私：選「**不收集資料**」。
- 審核備註：複製 `docs/store-listing.md` 裡的英文那段。
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

1. 商品代號是 `unlock_all`，Bundle ID 是 `io.github.ianyclin.jiujiumeteor`，一個字都不能錯。
2. Apple 的銷售地區要取消中國大陸和歐盟 27 國。
3. 卡住就截圖給我。
