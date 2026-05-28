// voice-text-field.swift
// 音声入力対応TextFieldコンポーネント
// iOS 17+ / SwiftUI

import SwiftUI
import Speech

/// 音声入力ボタン付きのTextField
struct VoiceTextField: View {

    // MARK: - Properties

    @Binding var text: String
    let placeholder: String
    let axis: Axis

    @State private var viewModel = SpeechRecognizerViewModel()
    @State private var showPermissionAlert = false

    // MARK: - Initialization

    init(
        _ placeholder: String = "",
        text: Binding<String>,
        axis: Axis = .horizontal
    ) {
        self.placeholder = placeholder
        self._text = text
        self.axis = axis
    }

    // MARK: - Body

    var body: some View {
        HStack(alignment: .bottom, spacing: 8) {
            TextField(placeholder, text: $text, axis: axis)
                .textFieldStyle(.roundedBorder)

            voiceButton
        }
        .onChange(of: viewModel.transcribedText) { _, newValue in
            if !newValue.isEmpty {
                text = newValue
            }
        }
        .alert("権限が必要です", isPresented: $showPermissionAlert) {
            Button("設定を開く") {
                openSettings()
            }
            Button("キャンセル", role: .cancel) { }
        } message: {
            Text("音声入力を使用するには、設定アプリでマイクと音声認識の権限を許可してください。")
        }
        .task {
            await viewModel.requestAuthorization()
        }
    }

    // MARK: - Subviews

    private var voiceButton: some View {
        Button(action: handleVoiceButtonTap) {
            ZStack {
                Circle()
                    .fill(viewModel.isRecording ? Color.red.opacity(0.2) : Color.blue.opacity(0.1))
                    .frame(width: 44, height: 44)

                Image(systemName: viewModel.isRecording ? "mic.fill" : "mic")
                    .font(.system(size: 20))
                    .foregroundStyle(viewModel.isRecording ? .red : .blue)

                if viewModel.isRecording {
                    Circle()
                        .stroke(Color.red, lineWidth: 2)
                        .frame(width: 44, height: 44)
                        .scaleEffect(1.2)
                        .opacity(0.5)
                        .animation(
                            .easeInOut(duration: 0.8).repeatForever(autoreverses: true),
                            value: viewModel.isRecording
                        )
                }
            }
        }
        .buttonStyle(.plain)
        .accessibilityLabel(viewModel.isRecording ? "録音を停止" : "音声入力を開始")
    }

    // MARK: - Actions

    private func handleVoiceButtonTap() {
        switch viewModel.authorizationStatus {
        case .authorized:
            Task {
                await viewModel.toggleRecording()
            }
        case .denied, .restricted:
            showPermissionAlert = true
        case .notDetermined:
            Task {
                await viewModel.requestAuthorization()
                if viewModel.authorizationStatus == .authorized {
                    await viewModel.toggleRecording()
                }
            }
        @unknown default:
            break
        }
    }

    private func openSettings() {
        if let url = URL(string: UIApplication.openSettingsURLString) {
            UIApplication.shared.open(url)
        }
    }
}

// MARK: - Preview

#Preview {
    struct PreviewWrapper: View {
        @State private var text = ""

        var body: some View {
            VStack(spacing: 20) {
                VoiceTextField("テキストを入力...", text: $text)

                Text("入力されたテキスト:")
                    .font(.caption)
                    .foregroundStyle(.secondary)

                Text(text.isEmpty ? "なし" : text)
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(Color.gray.opacity(0.1))
                    .clipShape(RoundedRectangle(cornerRadius: 8))
            }
            .padding()
        }
    }

    return PreviewWrapper()
}

// MARK: - Compact Voice Button

/// コンパクトな音声入力ボタン（単体で使用可能）
struct VoiceInputButton: View {

    @Binding var text: String
    @State private var viewModel = SpeechRecognizerViewModel()
    @State private var showPermissionAlert = false

    var body: some View {
        Button(action: handleTap) {
            Image(systemName: viewModel.isRecording ? "mic.fill" : "mic")
                .font(.title2)
                .foregroundStyle(viewModel.isRecording ? .red : .primary)
                .padding(12)
                .background(
                    Circle()
                        .fill(viewModel.isRecording ? Color.red.opacity(0.2) : Color.gray.opacity(0.1))
                )
        }
        .onChange(of: viewModel.transcribedText) { _, newValue in
            if !newValue.isEmpty {
                text = newValue
            }
        }
        .alert("権限が必要です", isPresented: $showPermissionAlert) {
            Button("設定を開く") {
                if let url = URL(string: UIApplication.openSettingsURLString) {
                    UIApplication.shared.open(url)
                }
            }
            Button("キャンセル", role: .cancel) { }
        } message: {
            Text("音声入力を使用するには、設定でマイクと音声認識を許可してください。")
        }
        .task {
            await viewModel.requestAuthorization()
        }
    }

    private func handleTap() {
        if viewModel.authorizationStatus == .authorized {
            Task { await viewModel.toggleRecording() }
        } else if viewModel.authorizationStatus == .notDetermined {
            Task {
                await viewModel.requestAuthorization()
                if viewModel.authorizationStatus == .authorized {
                    await viewModel.toggleRecording()
                }
            }
        } else {
            showPermissionAlert = true
        }
    }
}
