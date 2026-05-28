# 位置情報権限パターン (macOS)

macOSでの位置情報権限リクエストと設定の詳細ガイド。

## Info.plist設定

### 必須キー

```xml
<key>NSLocationUsageDescription</key>
<string>現在地を地図上に表示し、周辺のスポットを検索するために位置情報を使用します。</string>
```

### 説明文のベストプラクティス

**良い例:**
- 「現在地周辺のレストランを検索するために位置情報を使用します」
- 「地図上であなたの位置を表示し、目的地への経路を案内するために位置情報を使用します」
- 「最寄りの店舗を表示するために位置情報を使用します」

**悪い例:**
- 「位置情報が必要です」（具体的な理由がない）
- 「Location access required」（日本語アプリで英語）
- 「アプリの機能向上のため」（曖昧すぎる）

## CLAuthorizationStatus (macOS)

### ステータス一覧

| Status | 値 | macOSでの意味 |
|--------|---|--------------|
| `.notDetermined` | 0 | まだ権限を求めていない |
| `.restricted` | 1 | ペアレンタルコントロール等で制限 |
| `.denied` | 2 | ユーザーが拒否した |
| `.authorized` | 3 | 許可された（macOS主要） |
| `.authorizedAlways` | 3 | 常時許可（.authorizedと同値） |

**重要:** macOSでは`.authorizedWhenInUse`は利用不可。

### ステータス確認

```swift
let status = manager.authorizationStatus

switch status {
case .notDetermined:
    // 権限をリクエスト
    manager.requestWhenInUseAuthorization()
case .restricted:
    // 機能を無効化
    showLocationDisabledMessage()
case .denied:
    // システム環境設定へ誘導
    openLocationSettings()
case .authorized, .authorizedAlways:
    // 位置情報を使用可能
    startLocationServices()
@unknown default:
    break
}
```

## 権限リクエストフロー

### 基本実装

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

    func requestAuthorization() {
        manager.requestWhenInUseAuthorization()
    }

    nonisolated func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        Task { @MainActor in
            authorizationStatus = manager.authorizationStatus
        }
    }
}
```

### async/await パターン

```swift
private var authorizationContinuation: CheckedContinuation<CLAuthorizationStatus, Never>?

func requestAuthorization() async -> CLAuthorizationStatus {
    let status = manager.authorizationStatus

    if status == .notDetermined {
        manager.requestWhenInUseAuthorization()

        return await withCheckedContinuation { continuation in
            authorizationContinuation = continuation
        }
    }

    return status
}

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

権限リクエスト前に説明画面を表示。

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
                .frame(maxWidth: 400)

            Button("許可する") {
                locationManager.requestAuthorization()
                isPresented = false
            }
            .buttonStyle(.borderedProminent)
            .controlSize(.large)

            Button("後で") {
                isPresented = false
            }
            .buttonStyle(.bordered)
        }
        .padding(32)
    }
}
```

## システム環境設定への誘導

権限が拒否された場合。

### 実装

```swift
func openLocationSettings() {
    if let url = URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy_LocationServices") {
        NSWorkspace.shared.open(url)
    }
}
```

### UI例

```swift
struct LocationDeniedView: View {
    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "location.slash")
                .font(.system(size: 60))
                .foregroundStyle(.secondary)

            Text("位置情報がオフです")
                .font(.title2)
                .fontWeight(.bold)

            Text("この機能を使用するには、システム環境設定で位置情報を有効にしてください。")
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)
                .frame(maxWidth: 400)

            Button("システム環境設定を開く") {
                openLocationSettings()
            }
            .buttonStyle(.borderedProminent)

            Text("「プライバシーとセキュリティ」>「位置情報サービス」でこのアプリを許可してください")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .padding()
    }

    private func openLocationSettings() {
        if let url = URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy_LocationServices") {
            NSWorkspace.shared.open(url)
        }
    }
}
```

## 精度設定

macOSではフル精度のみがサポートされています（iOS 14+のReduced Accuracyはなし）。

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
    ▼           システム環境設定誘導
システム権限ダイアログ
    │
    ▼
権限変更通知
locationManagerDidChangeAuthorization
    │
    ▼
ステータスに応じた処理
```

## App Store審査ポイント

### 位置情報使用の正当性

- 位置情報を使用する明確な理由が必要
- 使用目的と説明文が一致していること

### 拒否される可能性のあるケース

- 位置情報が機能に必須でないのに必須として扱う
- 説明文が曖昧または不十分
- 位置情報を不要な目的で収集

### 推奨事項

1. 最小限の権限を求める
2. 位置情報なしでも基本機能は使えるようにする
3. 権限が拒否されても graceful degradation を実装
4. 説明文は具体的かつユーザーメリットを明示

## テスト方法

### シミュレータでの権限テスト

1. メニュー > Features > Location でシミュレート
2. 権限ダイアログはアプリ初回起動時に表示

### 実機でのテスト

1. システム環境設定 > プライバシーとセキュリティ > 位置情報サービス
2. アプリの権限を変更
3. 各権限状態での動作を確認

### 権限リセット

```bash
# アプリの権限をリセット（ターミナル）
tccutil reset LocationServices com.your.bundle.id
```
