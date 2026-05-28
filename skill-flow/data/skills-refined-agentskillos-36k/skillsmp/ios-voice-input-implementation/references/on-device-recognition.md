# On-Device Recognition

iOS 17+でのオンデバイス音声認識の詳細設定とフォールバック戦略。

## Overview

オンデバイス認識はネットワーク不要でプライバシー保護に優れる。iOS 13で導入され、iOS 17+で大幅に改善。

### メリット

- **プライバシー**: 音声データがデバイス外に送信されない
- **オフライン対応**: ネットワーク接続不要
- **低レイテンシ**: ネットワーク往復時間なし
- **コスト**: サーバー側の処理コストなし

### デメリット

- **対応言語**: サーバー認識より対応言語が少ない
- **精度**: 特定のケースでサーバー認識より劣る可能性
- **デバイス負荷**: CPU/メモリを消費

## Configuration

### オンデバイス認識の有効化

```swift
let request = SFSpeechAudioBufferRecognitionRequest()

// オンデバイス認識が利用可能か確認
if speechRecognizer.supportsOnDeviceRecognition {
    // オンデバイス認識を強制（ネットワーク使用しない）
    request.requiresOnDeviceRecognition = true
}
```

### 可用性チェック

```swift
func isOnDeviceRecognitionAvailable(for locale: Locale) -> Bool {
    guard let recognizer = SFSpeechRecognizer(locale: locale) else {
        return false
    }
    return recognizer.supportsOnDeviceRecognition
}
```

## Supported Languages

iOS 17+でオンデバイス認識に対応する主要言語：

| Language | Locale ID | Notes |
|----------|-----------|-------|
| 日本語 | ja-JP | 完全対応 |
| 英語（米国） | en-US | 完全対応 |
| 英語（英国） | en-GB | 完全対応 |
| 中国語（簡体字） | zh-CN | 完全対応 |
| 中国語（繁体字） | zh-TW | 完全対応 |
| スペイン語 | es-ES | 完全対応 |
| フランス語 | fr-FR | 完全対応 |
| ドイツ語 | de-DE | 完全対応 |
| イタリア語 | it-IT | 完全対応 |
| 韓国語 | ko-KR | 完全対応 |
| ポルトガル語 | pt-BR | 完全対応 |

**言語サポート確認:**

```swift
func checkOnDeviceSupportForLanguage(_ languageCode: String) {
    let locale = Locale(identifier: languageCode)
    guard let recognizer = SFSpeechRecognizer(locale: locale) else {
        print("\(languageCode): SFSpeechRecognizer作成不可")
        return
    }

    if recognizer.supportsOnDeviceRecognition {
        print("\(languageCode): オンデバイス認識対応")
    } else {
        print("\(languageCode): サーバー認識のみ")
    }
}
```

## Fallback Strategy

### オンライン/オフライン自動切り替え

```swift
@MainActor
@Observable
final class AdaptiveSpeechRecognizer {
    private let speechRecognizer: SFSpeechRecognizer?
    private var useOnDeviceRecognition = false

    init(locale: Locale = Locale(identifier: "ja-JP")) {
        speechRecognizer = SFSpeechRecognizer(locale: locale)
        updateRecognitionMode()
    }

    private func updateRecognitionMode() {
        guard let recognizer = speechRecognizer else { return }

        // オンデバイス認識が利用可能ならデフォルトで使用
        useOnDeviceRecognition = recognizer.supportsOnDeviceRecognition
    }

    func createRequest() -> SFSpeechAudioBufferRecognitionRequest {
        let request = SFSpeechAudioBufferRecognitionRequest()
        request.shouldReportPartialResults = true

        if useOnDeviceRecognition {
            request.requiresOnDeviceRecognition = true
        }

        return request
    }

    /// ネットワーク状態に応じてモードを切り替え
    func setPreferOnDevice(_ prefer: Bool) {
        guard let recognizer = speechRecognizer else { return }

        if prefer && recognizer.supportsOnDeviceRecognition {
            useOnDeviceRecognition = true
        } else {
            useOnDeviceRecognition = false
        }
    }
}
```

### ネットワーク監視との連携

```swift
import Network

@MainActor
@Observable
final class NetworkAwareSpeechRecognizer {
    private let pathMonitor = NWPathMonitor()
    private var isNetworkAvailable = true
    private let speechRecognizer: SFSpeechRecognizer?

    init(locale: Locale = Locale(identifier: "ja-JP")) {
        speechRecognizer = SFSpeechRecognizer(locale: locale)
        startNetworkMonitoring()
    }

    private func startNetworkMonitoring() {
        pathMonitor.pathUpdateHandler = { [weak self] path in
            Task { @MainActor in
                self?.isNetworkAvailable = (path.status == .satisfied)
            }
        }
        pathMonitor.start(queue: DispatchQueue.global(qos: .utility))
    }

    func createRequest() -> SFSpeechAudioBufferRecognitionRequest {
        let request = SFSpeechAudioBufferRecognitionRequest()
        request.shouldReportPartialResults = true

        // ネットワーク不可またはオンデバイス優先設定時
        if !isNetworkAvailable || shouldPreferOnDevice() {
            if speechRecognizer?.supportsOnDeviceRecognition == true {
                request.requiresOnDeviceRecognition = true
            }
        }

        return request
    }

    private func shouldPreferOnDevice() -> Bool {
        // ユーザー設定やバッテリー状態などで判断
        return UserDefaults.standard.bool(forKey: "preferOnDeviceRecognition")
    }

    deinit {
        pathMonitor.cancel()
    }
}
```

## Error Handling

### オンデバイス認識固有のエラー

```swift
func handleRecognitionError(_ error: Error) {
    let nsError = error as NSError

    switch (nsError.domain, nsError.code) {
    case ("kAFAssistantErrorDomain", 216):
        // ネットワークエラー - オンデバイスにフォールバック
        retryWithOnDeviceRecognition()

    case (SFSpeechRecognizerError.errorDomain, SFSpeechRecognizerError.noOnDeviceRecognition.rawValue):
        // オンデバイス認識非対応 - サーバー認識を使用
        retryWithServerRecognition()

    default:
        // その他のエラー
        handleGenericError(error)
    }
}

private func retryWithOnDeviceRecognition() {
    guard speechRecognizer?.supportsOnDeviceRecognition == true else {
        showOfflineUnavailableMessage()
        return
    }

    let request = SFSpeechAudioBufferRecognitionRequest()
    request.requiresOnDeviceRecognition = true
    // 認識を再開
}

private func retryWithServerRecognition() {
    let request = SFSpeechAudioBufferRecognitionRequest()
    request.requiresOnDeviceRecognition = false
    // 認識を再開
}
```

## Performance Considerations

### メモリ使用量

オンデバイス認識はモデルをメモリにロードするため、以下に注意：

```swift
// 認識終了後は適切にクリーンアップ
func cleanup() {
    recognitionTask?.cancel()
    recognitionTask = nil
    recognitionRequest?.endAudio()
    recognitionRequest = nil
    audioEngine.stop()
    audioEngine.inputNode.removeTap(onBus: 0)
}
```

### バッテリー消費

長時間の継続認識はバッテリーを消費：

```swift
// タイムアウトを設定
func startRecordingWithTimeout(seconds: TimeInterval) async throws {
    try await startRecording()

    // 指定秒後に自動停止
    Task {
        try await Task.sleep(for: .seconds(seconds))
        await stopRecording()
    }
}
```

### CPU使用率

認識処理はCPU集約的：

```swift
// QoSを適切に設定
let recognitionQueue = OperationQueue()
recognitionQueue.qualityOfService = .userInitiated
speechRecognizer?.queue = recognitionQueue
```

## User Settings Integration

### 設定画面の実装

```swift
struct SpeechSettingsView: View {
    @AppStorage("preferOnDeviceRecognition") private var preferOnDevice = false

    var body: some View {
        Form {
            Section("音声認識") {
                Toggle("オフライン認識を優先", isOn: $preferOnDevice)

                if preferOnDevice {
                    Text("ネットワーク不要で音声認識を行います。一部の言語では精度が低下する可能性があります。")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }

            Section("サポート状況") {
                HStack {
                    Text("日本語オンデバイス認識")
                    Spacer()
                    if isJapaneseOnDeviceSupported() {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundStyle(.green)
                    } else {
                        Image(systemName: "xmark.circle.fill")
                            .foregroundStyle(.red)
                    }
                }
            }
        }
    }

    private func isJapaneseOnDeviceSupported() -> Bool {
        let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "ja-JP"))
        return recognizer?.supportsOnDeviceRecognition ?? false
    }
}
```

## Testing On-Device Recognition

### 機内モードテスト

1. 機内モードを有効化
2. Wi-Fi/モバイルデータをオフ
3. `requiresOnDeviceRecognition = true` で認識実行
4. 正常に認識されることを確認

### 対応言語テスト

```swift
func testOnDeviceSupportedLanguages() {
    let testLocales = ["ja-JP", "en-US", "zh-CN", "ko-KR"]

    for localeID in testLocales {
        let locale = Locale(identifier: localeID)
        let recognizer = SFSpeechRecognizer(locale: locale)

        print("\(localeID): \(recognizer?.supportsOnDeviceRecognition == true ? "対応" : "非対応")")
    }
}
```
