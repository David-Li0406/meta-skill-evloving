# Permission Patterns

iOS音声認識に必要な権限設定とリクエストパターン。

## Info.plist Configuration

### Required Keys

```xml
<!-- マイクアクセス（必須） -->
<key>NSMicrophoneUsageDescription</key>
<string>音声入力機能を使用するためにマイクへのアクセスが必要です。</string>

<!-- 音声認識（必須） -->
<key>NSSpeechRecognitionUsageDescription</key>
<string>音声をテキストに変換するために音声認識を使用します。</string>
```

### Optional Keys

```xml
<!-- バックグラウンドオーディオ（必要な場合のみ） -->
<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
</array>
```

## Authorization Flow

### iOS 17+ Async/Await Pattern

```swift
@MainActor
final class PermissionManager {

    enum PermissionStatus {
        case authorized
        case denied
        case restricted
        case notDetermined
    }

    func checkAndRequestPermissions() async -> PermissionStatus {
        // 1. 現在のステータスを確認
        let currentStatus = SFSpeechRecognizer.authorizationStatus()

        switch currentStatus {
        case .authorized:
            return await checkMicrophonePermission()
        case .denied:
            return .denied
        case .restricted:
            return .restricted
        case .notDetermined:
            return await requestSpeechPermission()
        @unknown default:
            return .denied
        }
    }

    private func requestSpeechPermission() async -> PermissionStatus {
        let status = await withCheckedContinuation { continuation in
            SFSpeechRecognizer.requestAuthorization { status in
                continuation.resume(returning: status)
            }
        }

        switch status {
        case .authorized:
            return await checkMicrophonePermission()
        case .denied:
            return .denied
        case .restricted:
            return .restricted
        case .notDetermined:
            return .notDetermined
        @unknown default:
            return .denied
        }
    }

    private func checkMicrophonePermission() async -> PermissionStatus {
        let granted = await AVAudioApplication.requestRecordPermission()
        return granted ? .authorized : .denied
    }
}
```

### SwiftUI Integration

```swift
@MainActor
@Observable
final class SpeechPermissionViewModel {
    var permissionStatus: PermissionManager.PermissionStatus = .notDetermined
    var showPermissionDeniedAlert = false

    private let permissionManager = PermissionManager()

    func requestPermission() async {
        permissionStatus = await permissionManager.checkAndRequestPermissions()

        if permissionStatus == .denied {
            showPermissionDeniedAlert = true
        }
    }
}

struct ContentView: View {
    @State private var viewModel = SpeechPermissionViewModel()

    var body: some View {
        VStack {
            switch viewModel.permissionStatus {
            case .authorized:
                DictationView()
            case .denied:
                PermissionDeniedView()
            case .restricted:
                Text("音声認識は制限されています")
            case .notDetermined:
                Button("音声入力を有効にする") {
                    Task { await viewModel.requestPermission() }
                }
            }
        }
        .alert("権限が必要です", isPresented: $viewModel.showPermissionDeniedAlert) {
            Button("設定を開く") { openSettings() }
            Button("キャンセル", role: .cancel) { }
        } message: {
            Text("音声入力を使用するには、設定アプリでマイクと音声認識の権限を許可してください。")
        }
    }

    private func openSettings() {
        if let url = URL(string: UIApplication.openSettingsURLString) {
            UIApplication.shared.open(url)
        }
    }
}
```

## Authorization States

### SFSpeechRecognizerAuthorizationStatus

| State | Description | 対応 |
|-------|-------------|------|
| `.authorized` | ユーザーが許可 | 機能を有効化 |
| `.denied` | ユーザーが拒否 | 設定アプリへ誘導 |
| `.restricted` | ペアレンタルコントロール等で制限 | 機能を無効化、説明を表示 |
| `.notDetermined` | まだ選択されていない | 権限リクエストを実行 |

### AVAudioSession RecordPermission

| State | Description |
|-------|-------------|
| `granted` | マイク使用許可 |
| `denied` | マイク使用拒否 |
| `undetermined` | 未決定 |

## Handling Denied Permissions

### 設定アプリへのディープリンク

```swift
func openAppSettings() {
    guard let settingsURL = URL(string: UIApplication.openSettingsURLString),
          UIApplication.shared.canOpenURL(settingsURL) else {
        return
    }
    UIApplication.shared.open(settingsURL)
}
```

### ユーザーフレンドリーなUI

```swift
struct PermissionDeniedView: View {
    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "mic.slash")
                .font(.system(size: 60))
                .foregroundStyle(.secondary)

            Text("マイクの権限が必要です")
                .font(.headline)

            Text("音声入力を使用するには、設定アプリでマイクへのアクセスを許可してください。")
                .font(.subheadline)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)

            Button(action: openAppSettings) {
                Label("設定を開く", systemImage: "gear")
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }

    private func openAppSettings() {
        if let url = URL(string: UIApplication.openSettingsURLString) {
            UIApplication.shared.open(url)
        }
    }
}
```

## Best Practices

### 権限リクエストのタイミング

1. **遅延リクエスト**: アプリ起動直後ではなく、機能使用時にリクエスト
2. **コンテキスト提供**: リクエスト前に使用目的を説明
3. **段階的リクエスト**: まず音声認識、次にマイクの順でリクエスト

### Pre-Permission UI

```swift
struct PrePermissionView: View {
    let onContinue: () -> Void

    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "mic.circle.fill")
                .font(.system(size: 80))
                .foregroundStyle(.blue)

            Text("音声入力を使用")
                .font(.title2)
                .fontWeight(.semibold)

            Text("テキストを話すだけで入力できます。マイクと音声認識の権限が必要です。")
                .font(.body)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)

            Button("続ける") {
                onContinue()
            }
            .buttonStyle(.borderedProminent)
        }
        .padding(32)
    }
}
```

## App Store Review Considerations

### プライバシーポリシー要件

音声認識を使用するアプリは以下を明記すべき：

1. 収集する音声データの種類
2. データの使用目的
3. データの保存期間
4. 第三者との共有有無

### App Store Reviewガイドライン

- **5.1.1 Data Collection and Storage**: ユーザーデータの収集には明確な同意が必要
- **5.1.2 Data Use and Sharing**: データ使用目的を明確に説明

### Info.plist説明文のベストプラクティス

**悪い例:**
```xml
<string>マイクを使用します</string>
```

**良い例:**
```xml
<string>音声入力機能を使用するためにマイクへのアクセスが必要です。音声データはテキスト変換のみに使用され、サーバーには保存されません。</string>
```

## Testing Permissions

### シミュレータでの制限

- シミュレータでは音声認識が動作しない
- 権限ダイアログは表示されるが、実際の認識はできない
- 実機テストが必須

### 権限リセット方法

**デバイスで:**
1. 設定 > 一般 > リセット > 位置情報とプライバシーをリセット

**または:**
1. アプリをアンインストール
2. 再インストール

### 自動テスト

```swift
import XCTest

class PermissionTests: XCTestCase {
    func testPermissionStatusHandling() async {
        let manager = PermissionManager()

        // 各ステータスに対するUI更新をテスト
        // 注: 実際の権限状態はモックが必要
    }
}
```
