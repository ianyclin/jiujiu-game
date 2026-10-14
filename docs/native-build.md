# 原生打包（Capacitor 8）

遊戲本體仍是單檔 `index.html` + `assets/`，**原封不動**包進 app。`tools/make-www.mjs` 把它們複製到 `www/`（產物、不進版控；只少放一個商店用的 `icon-1024.png`），`cap sync` 再複製進 `ios/`、`android/`。網頁版（GitHub Pages）不受影響。

- `appId`：`io.github.ianyclin.jiujiumeteor`（**請確認**：Google Play 的套件名稱上架後永遠不能改；Apple 的 Bundle ID 也很難改。若你有自己的網域，改成反向網域，一次要改 `capacitor.config.json`、`android/app/build.gradle` 的 `namespace`／`applicationId`、`android/.../MainActivity.java` 的 package 與路徑、`strings.xml`、`ios/App/App.xcodeproj/project.pbxproj` 的 `PRODUCT_BUNDLE_IDENTIFIER`）。
- 外掛：**零**。只有 Capacitor 核心（`@capacitor/core`、`android`、`ios`）。沒有第三方 SDK，`NSPrivacyAccessedAPITypes` 為空。

## 指令

```bash
npm install
npm run sync                       # www/ → ios/、android/
python3 tools/make-app-icons.py    # 只有換了 icon-1024.png 才需要重跑

# Android（需要 JDK 21、Android SDK 36）
npm run android:apk                # android/app/build/outputs/apk/debug/app-debug.apk
npm run android:aab                # 上架用 AAB（要先設簽署，見下）
# iOS（需要 Mac + Xcode 26 以上）
npx cap open ios                   # 在 Xcode 選 Team、Product → Archive
```

改了 `index.html` 或 `assets/` 之後要 `npm run sync`，不然 app 裡還是舊的。

## 已處理

| 項目 | 做法 |
|---|---|
| App 名稱 | 桌面名稱短：英文「9×9 Meteor」、中日「九九流星隊」。iOS 用 `en／zh-Hant／ja.lproj/InfoPlist.strings`（已加進 pbxproj 的 `PBXVariantGroup` 與 `knownRegions`），Android 用 `values`（英文預設）、`values-zh`、`values-ja`。商店上的長名稱另外設（步驟 4） |
| 圖示 | `tools/make-app-icons.py` 從 `assets/icon/icon-1024.png` 產生：iOS 1024（不透明 RGB，App Store 不接受透明）；Android legacy 方形／圓形與 adaptive 前景（art 縮到 66%，可見範圍是中間 72/108）＋背景（夜空模糊） |
| 啟動畫面 | 夜空底色 `#08111f` ＋圖示置中，iOS storyboard 與 Android `Theme.SplashScreen` 都是，不閃白 |
| 直向鎖定 | iOS：iPhone、iPad 都只列 `Portrait`，iPad 加 `UIRequiresFullScreen`（不然 App Store 要求 iPad 支援四個方向）。Android：`screenOrientation="portrait"`。**注意**：Android 16（targetSdk 36）在 sw ≥ 600dp 的大螢幕（平板、折疊機展開）會忽略這個鎖定；遊戲橫向版面本來就能玩（CLAUDE.md 的平板規則），所以不處理 |
| 深色 | iOS `UIUserInterfaceStyle = Dark`、Android 視窗底色夜空色；`SystemBars.style = DARK`（淺色圖示）。遊戲刻意只做夜空一種主題，手機設成亮色模式時狀態列也不會變成黑字黑底 |
| 安全區 | 不改 `index.html`。iOS：`contentInset: never` → WKWebView 全螢幕，`viewport-fit=cover` 讓 `env(safe-area-inset-*)` 跟 Safari 加入主畫面一樣，`:root` 的 padding 處理一次。Android：Capacitor 8 的 SystemBars 預設 `insetsHandling: css`，舊 WebView（< 140）把 WebView 內縮、`env()` 回 0；新 WebView 照 `viewport-fit=cover` 滿版並給正確的 `env()`。兩種都不會讓遊戲被狀態列或手勢條蓋住，也不會算兩次（這是讀 Capacitor 原始碼與文件的結論，未在實機驗證） |
| 權限 | iOS：無。Android：**拿掉 `INTERNET`**（遊戲離線，Data safety 寫「不收集」更乾淨）；沒有任何其他權限 |
| 備份 | Android `allowBackup="false"`：孩子的紀錄不進 Google 備份，跟隱私權政策「只存本機」一致。iOS 的整機備份系統會帶走 app 資料，無法關，已寫進隱私權政策第 6 節 |
| 出口合規 | `ITSAppUsesNonExemptEncryption = false` |
| Privacy Manifest | `ios/App/App/PrivacyInfo.xcprivacy`：不追蹤、不收集、無 required-reason API |
| 版本 | `MARKETING_VERSION` 1.2、`versionName` 1.2（與關於頁一致；改版時三處一起改：`index.html` 的 `about.ver` ×3 語言、pbxproj、`build.gradle`） |

## localStorage 在 App 裡的保存

- 遊戲所有紀錄在 `localStorage`（`jiujiu-meteor-*`）。Capacitor 的 origin 是 iOS `capacitor://localhost`、Android `https://localhost`，**`capacitor.config.json` 的 `server.hostname`／`iosScheme`／`androidScheme` 已明確寫死，之後不可改**：儲存空間綁 origin，改了孩子的紀錄就看不到了。
- Android WebView 的 localStorage 在 app 私有資料夾，只有使用者主動清除 app 資料或解除安裝才會消失。
- iOS WKWebView 的資料在 `Library/WebKit`。「7 天不使用就清除」的 ITP 規則針對 Safari 瀏覽，不含 app 內的 WKWebView；但 Capacitor 官方文件仍提醒：系統在儲存空間吃緊時**理論上**可以清掉 WebView 儲存。
- **我刻意沒有加「鏡像到原生儲存」**（Capacitor Preferences 外掛，`save()` 同步寫一份、WebView 資料被清空時還原）。原因：(1) 沒有 Mac／實機，這個還原流程（偵測空資料 → 非同步取回 → 重載）無法在這裡測，在兒童 app 上放沒測過的資料還原有「蓋掉資料」的風險；(2) 要多一個外掛與 Privacy Manifest 的 UserDefaults 宣告；(3) 實務上很少發生。**建議**：先用 TestFlight／Play 內部測試觀察；若真有人回報紀錄不見，再做。需要時我可以做，要你決定。
- 紀錄匯出／匯入（家長關卡後手動備份）是另一個選項，同樣留待之後決定。

## 自動建 APK（GitHub Actions）

`.github/workflows/android-apk.yml`：推到 `main`、開或更新 PR（改到遊戲、`assets/`、`android/`、Capacitor 設定時），或在 GitHub 的 **Actions → Android APK → Run workflow** 手動按，都會自動建一個測試 APK。

- **下載**：Actions 頁面點進那次 run，最下面 **Artifacts** 的 `jiujiu-meteor-apk-<編號>`（zip，解開是 APK），保留 30 天。要登入 GitHub 才能下載。
- **版本號**：`versionCode` 用 run 編號（`CI_VERSION_CODE`），越新越大；`versionName` 仍是 1.2。
- **簽名固定**：`android/app/debug.keystore` 是進版控的**測試用** debug 金鑰（密碼 `android`）。每次建的 APK 簽名相同，手機上可以**直接覆蓋安裝，紀錄保留**。這把金鑰公開無妨，Google Play 不收 debug 簽署的檔案；上架用的 upload key 是另一把，絕不進版控。
  - 2026-10-14 之前我在對話裡傳的那個 APK 是用別的金鑰簽的，換成 CI 建的版本時要先解除安裝一次（**先用設定裡的「備份紀錄」備份**）。
- **建置後自動檢查**：套件名稱、版本、沒有 `INTERNET` 權限、APK 裡的 `index.html` 與 repo 逐位元相同；任何一項不對就失敗。
- 這是 debug 版：只給自己和測試者安裝。上架用的 AAB 要用你的 upload key 簽，見下節。

## 簽署與上架

- **iOS**：專案沒設 Team（`DEVELOPMENT_TEAM`），在 Xcode 的 Signing & Capabilities 選你的開發者帳號。Bundle ID 要先在 Apple Developer 後台註冊。第一次 Archive 前用 Xcode 26 開專案，確認 SPM（`CapApp-SPM`）解析成功。
- **Android**：用 Play App Signing。本機建 AAB 要有 upload key（**金鑰檔與密碼不要進版控**，`.gitignore` 已擋 `*.jks`、`*.keystore`、`keystore.properties`）。`android/app/build.gradle` 還沒設 `signingConfigs`，建 release 時再加，或用 Android Studio 的 Build → Generate Signed Bundle。

## 驗證狀況（誠實清單）

**已驗證（2026-10-14，在 Linux 上實際建置）**
- `gradle assembleDebug` 與 `gradle bundleRelease` 都成功：`app-debug.apk` 約 6.9 MB、`app-release.aab`（未簽署）約 5.8 MB。環境：JDK 21、Android SDK 36（platforms;android-36、build-tools;36.0.0）、Gradle 8.14.3。
- 用 `aapt2` 檢查成品：套件 `io.github.ianyclin.jiujiumeteor`、versionName 1.2、minSdk 24、targetSdk 36；**沒有 `INTERNET` 權限**（唯一的權限是 androidx 自己定義、只給本 app 的內部權限，不是使用者要同意的）；`allowBackup=false`、`screenOrientation=portrait`；桌面名稱英文「9×9 Meteor」、`zh`／`zh-TW`／`zh-HK`／`ja` 都是「九九流星隊」；APK 內的 `assets/public/index.html` 與 repo 的 `index.html` 逐位元相同，20 張寵物圖都在。
- 建置抓到並修掉兩個資源問題：`colors.xml` 註解裡的 `--`（XML 不允許），以及繁中地區（zh-TW、zh-HK）會落回英文名稱（加了 `values-zh-rTW`、`values-zh-rHK`）。

**沒驗證到**
1. **沒有在真的 Android 裝置或模擬器上跑過**：這個環境沒有 KVM，模擬器開不起來。所以 WebView 載入遊戲、觸控、音效、安全區（手勢導覽列、挖孔）、直向鎖定、`window.open`（粉專與隱私權政策連結，過家長關卡後是否開啟系統瀏覽器）都要在實機確認。debug APK 可直接傳到手機安裝測試。
2. **iOS 完全沒建置**（沒有 Mac）。`project.pbxproj` 的修改只用 `xcode` npm 套件解析確認格式與參照，沒有 Xcode 驗證。
3. 上架用的 AAB 要用你的 upload key 簽署（見上節）；這裡建的是未簽署版，debug APK 用 Android 的 debug 金鑰簽，**不能上架**，只能測試。
4. `./gradlew`（wrapper）在這個環境下載 Gradle 時連線被重置（proxy 的問題），所以我改用系統裝好的同版本 `gradle`。你自己的電腦用 `npm run android:apk` 即可。

## 在這個環境重現建置

```bash
# Android SDK（dl.google.com 要能連）
mkdir -p /opt/android-sdk/cmdline-tools && cd /opt/android-sdk/cmdline-tools
curl -LO https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip && unzip -q commandlinetools-*.zip && mv cmdline-tools latest
yes | latest/bin/sdkmanager --licenses && latest/bin/sdkmanager "platforms;android-36" "build-tools;36.0.0" "platform-tools"
export ANDROID_HOME=/opt/android-sdk
npm install && npm run sync && cd android && gradle assembleDebug --max-workers=2
```

Maven Central 偶爾回 429（瞬間請求太多），重跑即可。
