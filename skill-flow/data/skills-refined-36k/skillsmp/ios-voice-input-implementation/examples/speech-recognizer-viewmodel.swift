// speech-recognizer-viewmodel.swift
// 音声認識ViewModelの完全な実装例
// iOS 17+ / SwiftUI

import Speech
import AVFoundation
import Observation

@MainActor
@Observable
final class SpeechRecognizerViewModel {

    // MARK: - Published Properties

    /// 認識されたテキスト
    var transcribedText = ""

    /// 録音中かどうか
    var isRecording = false

    /// エラーメッセージ
    var errorMessage: String?

    /// 権限ステータス
    var authorizationStatus: SFSpeechRecognizerAuthorizationStatus = .notDetermined

    // MARK: - Private Properties

    private var audioEngine: AVAudioEngine?
    private var recognitionTask: SFSpeechRecognitionTask?
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private let speechRecognizer: SFSpeechRecognizer?

    // MARK: - Initialization

    init(locale: Locale = Locale(identifier: "ja-JP")) {
        speechRecognizer = SFSpeechRecognizer(locale: locale)
        speechRecognizer?.delegate = self
    }

    deinit {
        cleanup()
    }

    // MARK: - Public Methods

    /// 権限をリクエスト
    func requestAuthorization() async {
        authorizationStatus = await withCheckedContinuation { continuation in
            SFSpeechRecognizer.requestAuthorization { status in
                continuation.resume(returning: status)
            }
        }
    }

    /// 録音を開始
    func startRecording() async throws {
        guard authorizationStatus == .authorized else {
            throw SpeechRecognizerError.unauthorized
        }

        guard let speechRecognizer = speechRecognizer, speechRecognizer.isAvailable else {
            throw SpeechRecognizerError.recognizerUnavailable
        }

        // 既存のタスクをクリーンアップ
        cleanup()

        // オーディオセッションを設定
        try configureAudioSession()

        // オーディオエンジンを初期化
        audioEngine = AVAudioEngine()
        guard let audioEngine = audioEngine else {
            throw SpeechRecognizerError.audioEngineError
        }

        // 認識リクエストを作成
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        guard let recognitionRequest = recognitionRequest else {
            throw SpeechRecognizerError.requestCreationFailed
        }

        // 設定
        recognitionRequest.shouldReportPartialResults = true
        recognitionRequest.taskHint = .dictation

        // オンデバイス認識が利用可能なら使用
        if speechRecognizer.supportsOnDeviceRecognition {
            recognitionRequest.requiresOnDeviceRecognition = true
        }

        // 認識タスクを開始
        recognitionTask = speechRecognizer.recognitionTask(with: recognitionRequest) { [weak self] result, error in
            Task { @MainActor in
                self?.handleRecognitionResult(result: result, error: error)
            }
        }

        // オーディオ入力タップを設定
        let inputNode = audioEngine.inputNode
        let recordingFormat = inputNode.outputFormat(forBus: 0)

        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { [weak self] buffer, _ in
            self?.recognitionRequest?.append(buffer)
        }

        // オーディオエンジンを開始
        audioEngine.prepare()
        try audioEngine.start()

        isRecording = true
        errorMessage = nil
    }

    /// 録音を停止
    func stopRecording() {
        isRecording = false

        audioEngine?.stop()
        audioEngine?.inputNode.removeTap(onBus: 0)

        recognitionRequest?.endAudio()
        recognitionTask?.finish()
    }

    /// 録音をトグル
    func toggleRecording() async {
        if isRecording {
            stopRecording()
        } else {
            do {
                try await startRecording()
            } catch {
                handleError(error)
            }
        }
    }

    /// テキストをクリア
    func clearText() {
        transcribedText = ""
    }

    // MARK: - Private Methods

    private func configureAudioSession() throws {
        let audioSession = AVAudioSession.sharedInstance()
        try audioSession.setCategory(.playAndRecord, mode: .measurement, options: [.duckOthers, .defaultToSpeaker])
        try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
    }

    private func handleRecognitionResult(result: SFSpeechRecognitionResult?, error: Error?) {
        if let error = error {
            handleError(error)
            return
        }

        guard let result = result else { return }

        transcribedText = result.bestTranscription.formattedString

        if result.isFinal {
            stopRecording()
        }
    }

    private func handleError(_ error: Error) {
        let nsError = error as NSError

        switch nsError.domain {
        case "kAFAssistantErrorDomain":
            switch nsError.code {
            case 203:
                errorMessage = "音声が検出されませんでした"
            case 216:
                errorMessage = "ネットワークエラーが発生しました"
            case 1100:
                // キャンセル - エラーとして扱わない
                return
            default:
                errorMessage = "認識エラー: \(nsError.localizedDescription)"
            }
        default:
            errorMessage = error.localizedDescription
        }

        stopRecording()
    }

    private func cleanup() {
        recognitionTask?.cancel()
        recognitionTask = nil

        recognitionRequest?.endAudio()
        recognitionRequest = nil

        audioEngine?.stop()
        audioEngine?.inputNode.removeTap(onBus: 0)
        audioEngine = nil

        try? AVAudioSession.sharedInstance().setActive(false)
    }
}

// MARK: - SFSpeechRecognizerDelegate

extension SpeechRecognizerViewModel: SFSpeechRecognizerDelegate {
    nonisolated func speechRecognizer(_ speechRecognizer: SFSpeechRecognizer, availabilityDidChange available: Bool) {
        Task { @MainActor in
            if !available && isRecording {
                stopRecording()
                errorMessage = "音声認識が一時的に利用できません"
            }
        }
    }
}

// MARK: - Error Types

enum SpeechRecognizerError: LocalizedError {
    case unauthorized
    case recognizerUnavailable
    case audioEngineError
    case requestCreationFailed

    var errorDescription: String? {
        switch self {
        case .unauthorized:
            return "音声認識の権限がありません"
        case .recognizerUnavailable:
            return "音声認識が利用できません"
        case .audioEngineError:
            return "オーディオエンジンの初期化に失敗しました"
        case .requestCreationFailed:
            return "認識リクエストの作成に失敗しました"
        }
    }
}
