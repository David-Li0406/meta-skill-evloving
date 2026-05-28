# Speech Framework API Reference

iOS 17+ Speech Framework の詳細APIリファレンス。

## SFSpeechRecognizer

音声認識エンジンの主要クラス。

### Initialization

```swift
// デフォルトロケール（デバイス設定に依存）
let recognizer = SFSpeechRecognizer()

// 特定ロケール指定
let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "ja-JP"))
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `isAvailable` | `Bool` | 認識エンジンが利用可能か |
| `locale` | `Locale` | 認識対象言語 |
| `supportsOnDeviceRecognition` | `Bool` | オンデバイス認識対応か |
| `delegate` | `SFSpeechRecognizerDelegate?` | 可用性変化通知用デリゲート |
| `defaultTaskHint` | `SFSpeechRecognitionTaskHint` | デフォルトタスクヒント |
| `queue` | `OperationQueue` | コールバック実行キュー |

### Methods

#### requestAuthorization

```swift
class func requestAuthorization(_ handler: @escaping (SFSpeechRecognizerAuthorizationStatus) -> Void)
```

ユーザーに音声認識権限をリクエスト。初回呼び出し時にシステムダイアログ表示。

#### recognitionTask(with:resultHandler:)

```swift
func recognitionTask(
    with request: SFSpeechRecognitionRequest,
    resultHandler: @escaping (SFSpeechRecognitionResult?, Error?) -> Void
) -> SFSpeechRecognitionTask
```

音声認識タスクを開始。結果はresultHandlerで非同期に返される。

**使用例:**

```swift
let task = recognizer.recognitionTask(with: request) { result, error in
    if let result = result {
        let transcription = result.bestTranscription.formattedString
        let isFinal = result.isFinal
    }
    if let error = error {
        // エラー処理
    }
}
```

### SFSpeechRecognizerDelegate

```swift
protocol SFSpeechRecognizerDelegate {
    func speechRecognizer(_ speechRecognizer: SFSpeechRecognizer, availabilityDidChange available: Bool)
}
```

ネットワーク状態変化やシステムリソースによる可用性変化を監視。

## SFSpeechRecognitionRequest

音声認識リクエストの基底クラス。

### Subclasses

- `SFSpeechAudioBufferRecognitionRequest` - リアルタイムオーディオバッファ用
- `SFSpeechURLRecognitionRequest` - 録音済みファイル用

### Common Properties

| Property | Type | Description |
|----------|------|-------------|
| `shouldReportPartialResults` | `Bool` | 途中結果を報告するか（デフォルト: true） |
| `requiresOnDeviceRecognition` | `Bool` | オンデバイス認識を強制するか |
| `taskHint` | `SFSpeechRecognitionTaskHint` | 認識タスクのヒント |
| `contextualStrings` | `[String]` | 認識精度向上のためのコンテキスト文字列 |
| `addsPunctuation` | `Bool` | 句読点を自動追加するか（iOS 16+） |

### SFSpeechRecognitionTaskHint

```swift
enum SFSpeechRecognitionTaskHint {
    case unspecified    // 指定なし
    case dictation      // ディクテーション（長文入力）
    case search         // 検索クエリ（短いフレーズ）
    case confirmation   // 確認（はい/いいえ）
}
```

**ディクテーション用途では `.dictation` を指定:**

```swift
request.taskHint = .dictation
```

## SFSpeechAudioBufferRecognitionRequest

リアルタイム音声認識用リクエスト。AVAudioEngineと組み合わせて使用。

### Methods

#### append(_:)

```swift
func append(_ audioPCMBuffer: AVAudioPCMBuffer)
```

オーディオバッファを認識エンジンに追加。

**使用例:**

```swift
let inputNode = audioEngine.inputNode
let recordingFormat = inputNode.outputFormat(forBus: 0)

inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, _ in
    request.append(buffer)
}
```

#### endAudio()

```swift
func endAudio()
```

オーディオ入力の終了を通知。最終結果が返される。

## SFSpeechRecognitionResult

音声認識結果を格納。

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `bestTranscription` | `SFTranscription` | 最も可能性の高い文字起こし |
| `transcriptions` | `[SFTranscription]` | 候補一覧（信頼度順） |
| `isFinal` | `Bool` | 最終結果かどうか |
| `speechRecognitionMetadata` | `SFSpeechRecognitionMetadata?` | メタデータ（iOS 14+） |

### SFTranscription

```swift
struct SFTranscription {
    var formattedString: String      // フォーマット済み文字列
    var segments: [SFTranscriptionSegment]  // セグメント一覧
}
```

### SFTranscriptionSegment

各単語/フレーズの詳細情報。

```swift
struct SFTranscriptionSegment {
    var substring: String           // 認識された文字列
    var substringRange: NSRange     // 元文字列での範囲
    var timestamp: TimeInterval     // 発話開始時刻
    var duration: TimeInterval      // 発話時間
    var confidence: Float           // 信頼度 (0.0-1.0)
    var alternativeSubstrings: [String]  // 代替候補
}
```

**信頼度に基づく処理例:**

```swift
for segment in transcription.segments {
    if segment.confidence < 0.5 {
        // 低信頼度セグメントをハイライト表示
    }
}
```

## SFSpeechRecognitionTask

実行中の認識タスクを管理。

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `state` | `SFSpeechRecognitionTaskState` | 現在の状態 |
| `isFinishing` | `Bool` | 終了処理中か |
| `error` | `Error?` | 発生したエラー |

### SFSpeechRecognitionTaskState

```swift
enum SFSpeechRecognitionTaskState {
    case starting     // 開始中
    case running      // 実行中
    case finishing    // 終了処理中
    case canceling    // キャンセル中
    case completed    // 完了
}
```

### Methods

#### cancel()

タスクを即座にキャンセル。部分結果は破棄される。

```swift
task.cancel()
```

#### finish()

オーディオ入力を終了し、最終結果を取得。

```swift
task.finish()
```

## Error Types

### SFSpeechRecognizerError

```swift
enum SFSpeechRecognizerError: Int, Error {
    case unknown = 0
    case audioInterrupted = 1
    case unauthorized = 2
    case unavailable = 3
    case noOnDeviceRecognition = 4
}
```

### 一般的なエラーコード

| Code | Domain | Description |
|------|--------|-------------|
| 203 | kAFAssistantErrorDomain | 音声が検出されない |
| 216 | kAFAssistantErrorDomain | ネットワークエラー |
| 301 | kAFAssistantErrorDomain | 認識がタイムアウト |
| 1100 | kAFAssistantErrorDomain | リクエストキャンセル |
| 1110 | kAFAssistantErrorDomain | オーディオフォーマット不正 |

## AVAudioEngine Integration

### Basic Setup

```swift
let audioEngine = AVAudioEngine()
let inputNode = audioEngine.inputNode
let recordingFormat = inputNode.outputFormat(forBus: 0)

// Tap installation
inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, time in
    recognitionRequest.append(buffer)
}

// Engine start
audioEngine.prepare()
try audioEngine.start()
```

### Cleanup

```swift
func stopRecording() {
    audioEngine.stop()
    audioEngine.inputNode.removeTap(onBus: 0)
    recognitionRequest?.endAudio()
    recognitionTask?.cancel()
}
```

## Memory Management

### Task Lifecycle

1. `recognitionTask(with:resultHandler:)` でタスク作成
2. オーディオバッファを `append()` で追加
3. `endAudio()` または `finish()` で終了
4. `resultHandler` で `isFinal == true` の結果を受信
5. タスクは自動的に解放される

### Avoiding Memory Leaks

```swift
// Weakなselfキャプチャでクロージャからのリーク防止
recognitionTask = recognizer.recognitionTask(with: request) { [weak self] result, error in
    guard let self = self else { return }
    // 処理
}
```

### Audio Engine Cleanup

```swift
deinit {
    audioEngine.stop()
    audioEngine.inputNode.removeTap(onBus: 0)
}
```

## Rate Limits and Quotas

Apple は音声認識APIにレート制限を設けている：

- **デバイス単位**: 1日あたりの認識リクエスト数に制限あり
- **アプリ単位**: 同時認識セッション数に制限あり
- **詳細な数値**: Apple非公開（変更される可能性）

**ベストプラクティス:**
- 不要な認識リクエストを避ける
- ユーザーアクションに基づいて認識を開始
- 長時間の継続認識は避け、適切に区切る
