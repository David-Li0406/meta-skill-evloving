# Troubleshooting

iOS音声認識の一般的な問題と解決策。

## Common Error Codes

### kAFAssistantErrorDomain

| Code | Description | 原因 | 解決策 |
|------|-------------|------|--------|
| 203 | No speech detected | 音声が検出されない | マイク入力を確認、ユーザーに発話を促す |
| 209 | Retry | 一時的なエラー | 自動リトライ |
| 216 | Network error | ネットワーク接続不可 | オンデバイス認識にフォールバック |
| 301 | Recognition timeout | 認識がタイムアウト | タイムアウト値を調整 |
| 1100 | Request cancelled | リクエストがキャンセルされた | 意図的でなければ再開 |
| 1101 | No match | 認識結果なし | ユーザーに再入力を促す |
| 1107 | Connection error | 接続エラー | ネットワーク確認、リトライ |
| 1110 | Audio format error | オーディオフォーマット不正 | AudioSession再設定 |

### SFSpeechRecognizerError

| Error | Description | 解決策 |
|-------|-------------|--------|
| `.unknown` | 不明なエラー | ログ収集、リトライ |
| `.audioInterrupted` | オーディオ中断 | AudioSession再設定、リトライ |
| `.unauthorized` | 権限なし | 権限リクエスト |
| `.unavailable` | 利用不可 | 後で再試行 |
| `.noOnDeviceRecognition` | オンデバイス非対応 | サーバー認識にフォールバック |

## Error Handling Implementation

```swift
func handleError(_ error: Error) {
    let nsError = error as NSError

    switch nsError.domain {
    case "kAFAssistantErrorDomain":
        handleAssistantError(code: nsError.code)
    case SFSpeechRecognizerError.errorDomain:
        handleSpeechRecognizerError(error)
    default:
        handleUnknownError(error)
    }
}

private func handleAssistantError(code: Int) {
    switch code {
    case 203:
        // 音声が検出されない
        showMessage("音声が検出されませんでした。もう一度お話しください。")
        restartRecognition()

    case 216:
        // ネットワークエラー
        if canUseOnDeviceRecognition() {
            switchToOnDeviceRecognition()
        } else {
            showMessage("ネットワーク接続を確認してください。")
        }

    case 301:
        // タイムアウト
        showMessage("認識がタイムアウトしました。")
        restartRecognition()

    case 1100:
        // キャンセル - 通常は意図的なので何もしない
        break

    case 1110:
        // オーディオフォーマットエラー
        reconfigureAudioSession()
        restartRecognition()

    default:
        showMessage("エラーが発生しました。もう一度お試しください。")
    }
}
```

## Simulator Limitations

### 音声認識はシミュレータで動作しない

シミュレータでの制限事項：

- **SFSpeechRecognizer**: 認識処理が実行されない
- **AVAudioEngine**: マイク入力が取得できない
- **権限ダイアログ**: 表示されるが実際の権限は付与されない

### シミュレータでのテスト方法

```swift
#if targetEnvironment(simulator)
class MockSpeechRecognizer {
    func simulateRecognition(text: String, delay: TimeInterval = 1.0) async -> String {
        try? await Task.sleep(for: .seconds(delay))
        return text
    }
}
#endif
```

### 実機テストの必須項目

1. 権限リクエストフロー
2. 実際の音声認識精度
3. バックグラウンド/フォアグラウンド遷移
4. 長時間使用時の安定性
5. 様々なノイズ環境

## Audio Session Conflicts

### 他アプリとの競合

```swift
// 通知を監視
NotificationCenter.default.addObserver(
    forName: AVAudioSession.interruptionNotification,
    object: nil,
    queue: .main
) { notification in
    guard let userInfo = notification.userInfo,
          let typeValue = userInfo[AVAudioSessionInterruptionTypeKey] as? UInt,
          let type = AVAudioSession.InterruptionType(rawValue: typeValue) else {
        return
    }

    switch type {
    case .began:
        // 中断開始 - 認識を一時停止
        pauseRecognition()

    case .ended:
        // 中断終了 - 認識を再開
        if let optionsValue = userInfo[AVAudioSessionInterruptionOptionKey] as? UInt,
           AVAudioSession.InterruptionOptions(rawValue: optionsValue).contains(.shouldResume) {
            resumeRecognition()
        }

    @unknown default:
        break
    }
}
```

### ルート変更の処理

```swift
// Bluetoothヘッドセット接続/切断など
NotificationCenter.default.addObserver(
    forName: AVAudioSession.routeChangeNotification,
    object: nil,
    queue: .main
) { notification in
    guard let userInfo = notification.userInfo,
          let reasonValue = userInfo[AVAudioSessionRouteChangeReasonKey] as? UInt,
          let reason = AVAudioSession.RouteChangeReason(rawValue: reasonValue) else {
        return
    }

    switch reason {
    case .newDeviceAvailable:
        // 新しいデバイスが接続された
        reconfigureAudioSession()

    case .oldDeviceUnavailable:
        // デバイスが切断された
        reconfigureAudioSession()

    default:
        break
    }
}
```

## Debugging Tips

### Console.appでのログ確認

1. Macでconsole.appを開く
2. デバイスを選択
3. フィルタに `Speech` または `Audio` を入力
4. 認識実行時のログを確認

### 詳細ログの有効化

```swift
#if DEBUG
func logRecognitionResult(_ result: SFSpeechRecognitionResult?) {
    guard let result = result else {
        print("[Speech] No result")
        return
    }

    print("[Speech] isFinal: \(result.isFinal)")
    print("[Speech] bestTranscription: \(result.bestTranscription.formattedString)")

    for (index, segment) in result.bestTranscription.segments.enumerated() {
        print("[Speech] Segment \(index): '\(segment.substring)' confidence: \(segment.confidence)")
    }
}

func logError(_ error: Error) {
    let nsError = error as NSError
    print("[Speech] Error domain: \(nsError.domain)")
    print("[Speech] Error code: \(nsError.code)")
    print("[Speech] Error description: \(nsError.localizedDescription)")
    print("[Speech] Error userInfo: \(nsError.userInfo)")
}
#endif
```

### 認識状態の監視

```swift
func logTaskState(_ task: SFSpeechRecognitionTask?) {
    guard let task = task else {
        print("[Speech] Task is nil")
        return
    }

    switch task.state {
    case .starting:
        print("[Speech] Task starting")
    case .running:
        print("[Speech] Task running")
    case .finishing:
        print("[Speech] Task finishing")
    case .canceling:
        print("[Speech] Task canceling")
    case .completed:
        print("[Speech] Task completed")
    @unknown default:
        print("[Speech] Task unknown state")
    }
}
```

## Common Issues and Solutions

### 問題: 認識が開始されない

**チェックリスト:**
1. Info.plistの権限設定を確認
2. `SFSpeechRecognizer.authorizationStatus()` を確認
3. `AVAudioSession.recordPermission` を確認
4. `speechRecognizer.isAvailable` を確認
5. `audioEngine.isRunning` を確認

### 問題: 認識結果が返ってこない

**チェックリスト:**
1. `recognitionRequest.shouldReportPartialResults = true` を確認
2. `audioEngine.inputNode` のtapが正しく設定されているか
3. オーディオフォーマットが正しいか
4. `recognitionTask` がnilでないか

```swift
// デバッグ用チェック
func validateSetup() -> Bool {
    guard let recognizer = speechRecognizer else {
        print("ERROR: speechRecognizer is nil")
        return false
    }

    guard recognizer.isAvailable else {
        print("ERROR: recognizer is not available")
        return false
    }

    guard audioEngine.inputNode.inputFormat(forBus: 0).sampleRate > 0 else {
        print("ERROR: Invalid audio format")
        return false
    }

    return true
}
```

### 問題: 認識精度が低い

**改善策:**
1. `taskHint` を適切に設定（`.dictation` など）
2. `contextualStrings` で期待される単語を設定
3. ノイズが少ない環境でテスト
4. マイクの品質を確認

```swift
// コンテキスト文字列の設定
request.contextualStrings = ["東京", "大阪", "名古屋"]  // 認識される可能性が高い単語
```

### 問題: メモリリーク

**対策:**

```swift
// 適切なクリーンアップ
func cleanup() {
    recognitionTask?.cancel()
    recognitionTask = nil

    recognitionRequest?.endAudio()
    recognitionRequest = nil

    audioEngine.stop()
    audioEngine.inputNode.removeTap(onBus: 0)

    try? AVAudioSession.sharedInstance().setActive(false)
}

// deinitでのクリーンアップ
deinit {
    cleanup()
    NotificationCenter.default.removeObserver(self)
}
```

## Performance Profiling

### Instrumentsでの計測

1. Xcode > Product > Profile
2. "Time Profiler" を選択
3. 音声認識を実行
4. CPU使用率を確認

### メモリ使用量の監視

```swift
func logMemoryUsage() {
    var info = mach_task_basic_info()
    var count = mach_msg_type_number_t(MemoryLayout<mach_task_basic_info>.size)/4

    let result = withUnsafeMutablePointer(to: &info) {
        $0.withMemoryRebound(to: integer_t.self, capacity: 1) {
            task_info(mach_task_self_, task_flavor_t(MACH_TASK_BASIC_INFO), $0, &count)
        }
    }

    if result == KERN_SUCCESS {
        let usedMB = Double(info.resident_size) / 1024.0 / 1024.0
        print("[Memory] Used: \(String(format: "%.2f", usedMB)) MB")
    }
}
```
