# Xcode Configuration Guide

Swift 6 Strict Concurrency を有効化するための Xcode 設定ガイド。

## Build Settings

### Strict Concurrency Checking

**設定名:** `SWIFT_STRICT_CONCURRENCY`

**場所:** Build Settings → Swift Compiler - Language → Strict Concurrency Checking

| 値 | 説明 |
|----|------|
| `minimal` | 最小限の警告（デフォルト） |
| `targeted` | `@Sendable` を明示した部分のみチェック |
| `complete` | 完全なデータ競合チェック（Swift 6 相当） |

### xcconfig での設定

```xcconfig
// Debug.xcconfig
SWIFT_STRICT_CONCURRENCY = complete

// Release.xcconfig
SWIFT_STRICT_CONCURRENCY = complete
```

### ターゲット別の設定

特定のターゲットのみ有効化する場合：

1. Project Navigator でプロジェクトを選択
2. 対象のターゲットを選択
3. Build Settings → Strict Concurrency Checking を設定

## Package.swift

### Swift Package Manager での設定

```swift
// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "MyPackage",
    platforms: [
        .iOS(.v17),
        .macOS(.v14)
    ],
    targets: [
        .target(
            name: "MyTarget",
            swiftSettings: [
                // Swift 5.x で Strict Concurrency を有効化
                .enableUpcomingFeature("StrictConcurrency")
            ]
        )
    ]
)
```

### Swift 6 言語モードの設定

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "MyPackage",
    platforms: [
        .iOS(.v17),
        .macOS(.v14)
    ],
    targets: [
        .target(
            name: "MyTarget",
            swiftSettings: [
                // Swift 6 言語モード
                .swiftLanguageMode(.v6)
            ]
        )
    ]
)
```

### 段階的な設定

```swift
let package = Package(
    name: "MyPackage",
    targets: [
        // メインターゲット: 完全な Strict Concurrency
        .target(
            name: "MyApp",
            swiftSettings: [
                .swiftLanguageMode(.v6)
            ]
        ),
        // レガシーモジュール: targeted モード
        .target(
            name: "LegacyModule",
            swiftSettings: [
                .enableUpcomingFeature("StrictConcurrency")
            ]
        ),
        // テスト: 完全な Strict Concurrency
        .testTarget(
            name: "MyAppTests",
            dependencies: ["MyApp"],
            swiftSettings: [
                .swiftLanguageMode(.v6)
            ]
        )
    ]
)
```

## Xcode プロジェクト設定

### 新規プロジェクトの推奨設定

1. **iOS/macOS の最小バージョン:**
   - iOS 17.0 以上
   - macOS 14.0 以上

2. **Swift バージョン:**
   - Swift 5.9 以上（推奨: 6.0）

3. **Strict Concurrency:**
   - 新規プロジェクト: `complete`
   - 既存プロジェクト: `targeted` から開始

### Build Settings の検索

1. Build Settings タブを開く
2. 検索バーに「concurrency」と入力
3. 「Strict Concurrency Checking」を見つける

### All / Combined / Levels の切り替え

- **All:** すべての設定を表示
- **Combined:** プロジェクトとターゲットの設定をマージして表示
- **Levels:** 各レベルの設定を個別に表示

## コマンドラインでの設定

### swift build

```bash
# Strict Concurrency を有効化
swift build -Xswiftc -strict-concurrency=complete

# Swift 6 モード
swift build -Xswiftc -swift-version -Xswiftc 6
```

### xcodebuild

```bash
xcodebuild \
    -project MyProject.xcodeproj \
    -scheme MyScheme \
    -configuration Debug \
    SWIFT_STRICT_CONCURRENCY=complete \
    build
```

## CI/CD での設定

### GitHub Actions

```yaml
name: Build and Test

on: [push, pull_request]

jobs:
  build:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4

      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_15.4.app

      - name: Build
        run: |
          xcodebuild \
            -project MyProject.xcodeproj \
            -scheme MyScheme \
            -destination 'platform=iOS Simulator,name=iPhone 15' \
            SWIFT_STRICT_CONCURRENCY=complete \
            build

      - name: Test
        run: |
          xcodebuild \
            -project MyProject.xcodeproj \
            -scheme MyScheme \
            -destination 'platform=iOS Simulator,name=iPhone 15' \
            test
```

### Fastlane

```ruby
# Fastfile
lane :build do
  gym(
    project: "MyProject.xcodeproj",
    scheme: "MyScheme",
    xcargs: "SWIFT_STRICT_CONCURRENCY=complete"
  )
end

lane :test do
  scan(
    project: "MyProject.xcodeproj",
    scheme: "MyScheme",
    xcargs: "SWIFT_STRICT_CONCURRENCY=complete"
  )
end
```

## トラブルシューティング

### 設定が反映されない場合

1. **クリーンビルド:**
   - Product → Clean Build Folder (⌘⇧K)
   - DerivedData を削除

2. **キャッシュのクリア:**
   ```bash
   rm -rf ~/Library/Developer/Xcode/DerivedData
   ```

3. **Xcode の再起動**

### 特定のファイルで警告を無視

```swift
// 一時的に特定のファイルで警告を抑制（非推奨）
// Build Settings → Other Swift Flags に追加
// -Xfrontend -disable-actor-data-race-checks
```

### サードパーティライブラリの警告

サードパーティライブラリからの警告を抑制するには、そのライブラリのターゲット設定を変更するか、`@preconcurrency import` を使用：

```swift
@preconcurrency import ThirdPartyLibrary
```

## チェックリスト

- [ ] `SWIFT_STRICT_CONCURRENCY` が正しく設定されている
- [ ] すべてのターゲットで一貫した設定になっている
- [ ] CI/CD でも同じ設定が適用されている
- [ ] クリーンビルドで警告が表示されることを確認
- [ ] サードパーティライブラリの警告に対処済み
