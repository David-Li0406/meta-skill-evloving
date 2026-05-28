# 位置情報権限パターン

iOS 17+での位置情報権限リクエストとInfo.plist設定の詳細ガイド。

## Info.plist設定

### 必須キー

#### NSLocationWhenInUseUsageDescription

アプリ使用中の位置情報アクセス理由を説明。

```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>現在地を地図上に表示し、周辺のスポットを検索するために位置情報を使用します。</string>
```

#### NSLocationAlwaysAndWhenInUseUsageDescription

バックグラウンドでの位置情報アクセスが必要な場合。

```xml
<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>目的地への到着を通知するために、バックグラウンドでも位置情報を使用します。</string>
```

#### NSLocationAlwaysUsageDescription（iOS 10以前の互換性）

```xml
<key>NSLocationAlwaysUsageDescription</key>
<string>バックグラウンドでのナビゲーションのために位置情報を使用します。</string>
```

### バックグラウンド位置情報

バックグラウンドで位置情報を取得する場合、UIBackgroundModesも設定が必要。

```xml
<key>UIBackgroundModes</key>
<array>
    <string>location</string>
</array>
```

### 説明文のベストプラクティス

**良い例:**
- 「現在地周辺のレストランを検索するために位置情報を使用します」
- 「地図上であなたの位置を表示し、目的地への経路を案内するために位置情報を使用します」

**悪い例:**
- 「位置情報が必要です」（具体的な理由がない）
- 「Location access required」（日本語アプリで英語）

## CLAuthorizationStatus

### ステータス一覧

| Status | 値 | 説明 |
|--------|---|------|
| `.notDetermined` | 0 | まだ権限を求めていない |
| `.restricted` | 1 | ペアレンタルコントロール等で制限 |
| `.denied` | 2 | ユーザーが拒否した |
| `.authorizedAlways` | 3 | 常時許可 |
| `.authorizedWhenInUse` | 4 | 使用中のみ許可 |

### ステータス確認

```swift
let status = CLLocationManager().authorizationStatus

switch status {
case .notDetermined:
    // 権限をリクエスト
    locationManager.requestWhenInUseAuthorization()
case .restricted:
    // 機能を無効化
    showLocationDisabledMessage()
case .denied:
    // 設定アプリへ誘導
    showSettingsPrompt()
case .authorizedWhenInUse, .authorizedAlways:
    // 位置情報を使用可能
    startLocationServices()
@unknown default:
    break
}
```

## 権限リクエストフロー

### When In Use 権限

```swift
@MainActor
@Observable
final class LocationManager: NSObject, CLLocationManagerDelegate {
    var authorizationStatus: CLAuthorizationStatus = .notDetermined

    private let manager = CLLocationManager()

    override init() {
        super.init()
        manager.delegate = self
        authorizationStatus = manager.authorizationStatus
    }

    func requestWhenInUseAuthorization() {
        manager.requestWhenInUseAuthorization()
    }

    nonisolated func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        Task { @MainActor in
            authorizationStatus = manager.authorizationStatus
        }
    }
}
```

### Always 権限

Always権限は、まずWhenInUse権限を取得してから段階的にリクエスト。

```swift
func requestAlwaysAuthorization() {
    guard authorizationStatus == .authorizedWhenInUse else {
        // まずWhenInUse権限を取得
        manager.requestWhenInUseAuthorization()
        return
    }

    // WhenInUse取得済みの場合、Alwaysをリクエスト
    manager.requestAlwaysAuthorization()
}
```

### async/await パターン (iOS 17+)

```swift
func requestAuthorization() async -> CLAuthorizationStatus {
    let status = manager.authorizationStatus

    if status == .notDetermined {
        manager.requestWhenInUseAuthorization()

        // 権限変更を待機
        return await withCheckedContinuation { continuation in
            authorizationContinuation = continuation
        }
    }

    return status
}

// デリゲートメソッド内で
nonisolated func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
    Task { @MainActor in
        authorizationStatus = manager.authorizationStatus

        if let continuation = authorizationContinuation {
            continuation.resume(returning: manager.authorizationStatus)
            authorizationContinuation = nil
        }
    }
}
```

## Pre-Permission UI

権限リクエスト前に説明画面を表示するパターン。

### なぜ必要か

- ユーザーに位置情報使用の目的を説明
- 許可率を向上させる
- App Store審査で好印象

### 実装例

```swift
struct LocationPermissionView: View {
    @State private var locationManager = LocationManager()
    @Binding var isPresented: Bool

    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "location.fill")
                .font(.system(size: 60))
                .foregroundStyle(.blue)

            Text("位置情報へのアクセス")
                .font(.title)
                .fontWeight(.bold)

            Text("周辺のスポットを検索したり、現在地から目的地への経路を表示するために、位置情報へのアクセスが必要です。")
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)

            Button("許可する") {
                locationManager.requestWhenInUseAuthorization()
                isPresented = false
            }
            .buttonStyle(.borderedProminent)

            Button("後で") {
                isPresented = false
            }
            .buttonStyle(.bordered)
        }
        .padding()
    }
}
```

## 設定アプリへの誘導

権限が拒否された場合、設定アプリへユーザーを誘導。

```swift
struct LocationDeniedView: View {
    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "location.slash")
                .font(.system(size: 48))
                .foregroundStyle(.secondary)

            Text("位置情報がオフです")
                .font(.headline)

            Text("設定アプリで位置情報を有効にしてください。")
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)

            Button("設定を開く") {
                openSettings()
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }

    private func openSettings() {
        guard let url = URL(string: UIApplication.openSettingsURLString) else { return }
        UIApplication.shared.open(url)
    }
}
```

## Precise vs Reduced Location

iOS 14+では、ユーザーが「おおよその位置情報」を選択可能。

### 精度レベルの確認

```swift
let accuracyAuthorization = manager.accuracyAuthorization

switch accuracyAuthorization {
case .fullAccuracy:
    // 正確な位置情報が利用可能
    useFullLocationFeatures()
case .reducedAccuracy:
    // おおよその位置情報のみ
    useReducedLocationFeatures()
@unknown default:
    break
}
```

### 一時的な正確な位置情報のリクエスト

```swift
func requestTemporaryFullAccuracy(purposeKey: String) {
    manager.requestTemporaryFullAccuracyAuthorization(
        withPurposeKey: purposeKey
    ) { error in
        if let error {
            print("Error: \(error.localizedDescription)")
        }
    }
}
```

Info.plistに目的を記載:

```xml
<key>NSLocationTemporaryUsageDescriptionDictionary</key>
<dict>
    <key>NavigationPurpose</key>
    <string>正確なナビゲーションのために、一時的に正確な位置情報が必要です。</string>
    <key>SearchPurpose</key>
    <string>より正確な検索結果を表示するために、正確な位置情報が必要です。</string>
</dict>
```

## App Store審査ポイント

### 位置情報使用の正当性

- 位置情報を使用する明確な理由が必要
- 使用目的と説明文が一致していること
- 不要な「Always」権限を求めないこと

### 拒否される可能性のあるケース

- 位置情報が機能に必須でないのに必須として扱う
- 説明文が曖昧または不十分
- Always権限を求めるが、バックグラウンド機能がない

### 推奨事項

1. 最小限の権限を求める（WhenInUseで十分なら Alwaysは求めない）
2. 位置情報なしでも基本機能は使えるようにする
3. 権限が拒否されても graceful degradation を実装
4. 説明文は具体的かつユーザーメリットを明示

## 権限フロー図

```
アプリ起動
    │
    ▼
┌─────────────────────┐
│ 権限ステータス確認    │
│ manager.authorizationStatus │
└─────────┬───────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
notDetermined  authorized/denied
    │           │
    ▼           ▼
Pre-Permission UI   機能実行
    │           または
    ▼           設定誘導
システム権限ダイアログ
    │
    ▼
権限変更通知
locationManagerDidChangeAuthorization
    │
    ▼
ステータスに応じた処理
```

## テスト方法

### シミュレータでの権限テスト

1. シミュレータの設定アプリで位置情報権限を変更
2. `Debug` > `Location` で位置をシミュレート
3. 権限を「なし」「使用中のみ」「常に」で切り替えてテスト

### 実機でのテスト

1. 設定 > プライバシーとセキュリティ > 位置情報サービス
2. アプリの権限を変更
3. 各権限状態での動作を確認

### ユニットテスト

```swift
// CLLocationManagerをモック化
protocol LocationManagerProtocol {
    var authorizationStatus: CLAuthorizationStatus { get }
    func requestWhenInUseAuthorization()
}

class MockLocationManager: LocationManagerProtocol {
    var authorizationStatus: CLAuthorizationStatus = .notDetermined

    func requestWhenInUseAuthorization() {
        authorizationStatus = .authorizedWhenInUse
    }
}
```
