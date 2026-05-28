// dictation-view.swift
// ディクテーション画面の完全サンプル
// iOS 17+ / SwiftUI

import SwiftUI
import Speech

/// ディクテーション画面
struct DictationView: View {

    // MARK: - Properties

    @State private var viewModel = SpeechRecognizerViewModel()
    @State private var showSettings = false
    @State private var showClearConfirmation = false

    // MARK: - Body

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // テキスト表示エリア
                textDisplayArea

                Divider()

                // コントロールエリア
                controlArea
            }
            .navigationTitle("音声入力")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        showSettings = true
                    } label: {
                        Image(systemName: "gear")
                    }
                }
            }
            .sheet(isPresented: $showSettings) {
                SettingsView()
            }
            .task {
                await viewModel.requestAuthorization()
            }
            .alert("テキストを消去", isPresented: $showClearConfirmation) {
                Button("消去", role: .destructive) {
                    viewModel.clearText()
                }
                Button("キャンセル", role: .cancel) { }
            } message: {
                Text("入力されたテキストをすべて消去しますか？")
            }
        }
    }

    // MARK: - Subviews

    private var textDisplayArea: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                if viewModel.transcribedText.isEmpty {
                    placeholderText
                } else {
                    transcribedText
                }

                if let errorMessage = viewModel.errorMessage {
                    errorBanner(message: errorMessage)
                }
            }
            .padding()
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .frame(maxHeight: .infinity)
        .background(Color(.systemGroupedBackground))
    }

    private var placeholderText: some View {
        VStack(spacing: 12) {
            Image(systemName: "text.bubble")
                .font(.system(size: 48))
                .foregroundStyle(.tertiary)

            Text("マイクボタンをタップして\n音声入力を開始してください")
                .font(.subheadline)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 60)
    }

    private var transcribedText: some View {
        Text(viewModel.transcribedText)
            .font(.body)
            .textSelection(.enabled)
            .frame(maxWidth: .infinity, alignment: .leading)
    }

    private func errorBanner(message: String) -> some View {
        HStack {
            Image(systemName: "exclamationmark.triangle.fill")
                .foregroundStyle(.orange)

            Text(message)
                .font(.caption)
        }
        .padding()
        .frame(maxWidth: .infinity)
        .background(Color.orange.opacity(0.1))
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }

    private var controlArea: some View {
        VStack(spacing: 16) {
            // 録音ボタン
            recordButton

            // ステータス表示
            statusText

            // アクションボタン
            actionButtons
        }
        .padding()
        .background(Color(.systemBackground))
    }

    private var recordButton: some View {
        Button(action: handleRecordButtonTap) {
            ZStack {
                Circle()
                    .fill(viewModel.isRecording ? Color.red : Color.blue)
                    .frame(width: 80, height: 80)
                    .shadow(color: (viewModel.isRecording ? Color.red : Color.blue).opacity(0.3), radius: 10)

                Image(systemName: viewModel.isRecording ? "stop.fill" : "mic.fill")
                    .font(.system(size: 32))
                    .foregroundStyle(.white)

                // 録音中のアニメーション
                if viewModel.isRecording {
                    Circle()
                        .stroke(Color.red.opacity(0.5), lineWidth: 3)
                        .frame(width: 90, height: 90)
                        .scaleEffect(1.2)
                        .opacity(0.0)
                        .animation(
                            .easeOut(duration: 1.0).repeatForever(autoreverses: false),
                            value: viewModel.isRecording
                        )
                }
            }
        }
        .buttonStyle(.plain)
        .disabled(viewModel.authorizationStatus != .authorized)
        .accessibilityLabel(viewModel.isRecording ? "録音を停止" : "録音を開始")
    }

    private var statusText: some View {
        Group {
            switch viewModel.authorizationStatus {
            case .authorized:
                if viewModel.isRecording {
                    HStack(spacing: 4) {
                        Circle()
                            .fill(Color.red)
                            .frame(width: 8, height: 8)
                        Text("録音中...")
                    }
                    .foregroundStyle(.red)
                } else {
                    Text("タップして音声入力を開始")
                        .foregroundStyle(.secondary)
                }

            case .denied, .restricted:
                Button {
                    openSettings()
                } label: {
                    Label("設定で権限を許可してください", systemImage: "exclamationmark.triangle")
                        .foregroundStyle(.orange)
                }

            case .notDetermined:
                Text("権限を確認中...")
                    .foregroundStyle(.secondary)

            @unknown default:
                EmptyView()
            }
        }
        .font(.caption)
    }

    private var actionButtons: some View {
        HStack(spacing: 24) {
            // コピーボタン
            Button {
                UIPasteboard.general.string = viewModel.transcribedText
            } label: {
                Label("コピー", systemImage: "doc.on.doc")
            }
            .disabled(viewModel.transcribedText.isEmpty)

            // 共有ボタン
            ShareLink(item: viewModel.transcribedText) {
                Label("共有", systemImage: "square.and.arrow.up")
            }
            .disabled(viewModel.transcribedText.isEmpty)

            // クリアボタン
            Button(role: .destructive) {
                showClearConfirmation = true
            } label: {
                Label("クリア", systemImage: "trash")
            }
            .disabled(viewModel.transcribedText.isEmpty)
        }
        .font(.caption)
    }

    // MARK: - Actions

    private func handleRecordButtonTap() {
        Task {
            await viewModel.toggleRecording()
        }
    }

    private func openSettings() {
        if let url = URL(string: UIApplication.openSettingsURLString) {
            UIApplication.shared.open(url)
        }
    }
}

// MARK: - Settings View

struct SettingsView: View {
    @Environment(\.dismiss) private var dismiss
    @AppStorage("preferOnDeviceRecognition") private var preferOnDevice = false

    var body: some View {
        NavigationStack {
            Form {
                Section("音声認識") {
                    Toggle("オフライン認識を優先", isOn: $preferOnDevice)

                    if preferOnDevice {
                        Text("ネットワーク不要で音声認識を行います。一部のケースでは精度が低下する可能性があります。")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                }

                Section("デバイス情報") {
                    HStack {
                        Text("日本語オンデバイス認識")
                        Spacer()
                        if isJapaneseOnDeviceSupported() {
                            Label("対応", systemImage: "checkmark.circle.fill")
                                .foregroundStyle(.green)
                        } else {
                            Label("非対応", systemImage: "xmark.circle.fill")
                                .foregroundStyle(.red)
                        }
                    }
                }

                Section {
                    Button("プライバシーポリシー") {
                        // プライバシーポリシーへのリンク
                    }

                    Button("利用規約") {
                        // 利用規約へのリンク
                    }
                }
            }
            .navigationTitle("設定")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("完了") {
                        dismiss()
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

// MARK: - Preview

#Preview("Dictation View") {
    DictationView()
}

#Preview("Settings") {
    SettingsView()
}
