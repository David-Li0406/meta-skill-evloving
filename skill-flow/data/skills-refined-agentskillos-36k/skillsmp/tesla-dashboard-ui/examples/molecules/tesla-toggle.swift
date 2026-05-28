// Tesla Dashboard UI - Toggle
// Tesla風トグルスイッチ
// アクセシビリティ完全対応

import SwiftUI

// MARK: - Tesla Toggle

/// Tesla風トグルスイッチ
/// カスタムデザインとアニメーション付き
struct TeslaToggle: View {
    // MARK: - Properties

    @Binding var isOn: Bool
    var label: String
    var icon: TeslaIcon? = nil
    var onLabel: String? = nil
    var offLabel: String? = nil

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @Environment(\.isEnabled) private var isEnabled

    // MARK: - Constants

    private let trackWidth: CGFloat = 51
    private let trackHeight: CGFloat = 31
    private let thumbSize: CGFloat = 27
    private let thumbPadding: CGFloat = 2

    // MARK: - Body

    var body: some View {
        HStack(spacing: 16) {
            // Label Section
            HStack(spacing: 8) {
                if let icon {
                    TeslaIconView(
                        icon: icon,
                        size: 20,
                        color: labelColor
                    )
                }

                Text(label)
                    .font(TeslaTypography.titleMedium)
                    .foregroundStyle(labelColor)
            }

            Spacer()

            // Status Label
            if let statusLabel = isOn ? onLabel : offLabel {
                Text(statusLabel)
                    .font(TeslaTypography.labelMedium)
                    .foregroundStyle(TeslaColors.textSecondary)
            }

            // Toggle
            toggleSwitch
        }
        .contentShape(Rectangle())
        .onTapGesture {
            guard isEnabled else { return }
            withAnimation(reduceMotion ? .none : TeslaAnimation.quick) {
                isOn.toggle()
            }
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel(label)
        .accessibilityValue(isOn ? "オン" : "オフ")
        .accessibilityAddTraits(.isButton)
        .accessibilityHint("ダブルタップで切り替え")
    }

    // MARK: - Toggle Switch

    private var toggleSwitch: some View {
        ZStack(alignment: isOn ? .trailing : .leading) {
            // Track
            RoundedRectangle(cornerRadius: trackHeight / 2)
                .fill(trackColor)
                .frame(width: trackWidth, height: trackHeight)

            // Thumb
            Circle()
                .fill(Color.white)
                .frame(width: thumbSize, height: thumbSize)
                .shadow(color: .black.opacity(0.15), radius: 4, y: 2)
                .padding(thumbPadding)
        }
        .animation(reduceMotion ? .none : TeslaAnimation.quick, value: isOn)
    }

    // MARK: - Computed Properties

    private var labelColor: Color {
        isEnabled ? TeslaColors.textPrimary : TeslaColors.textDisabled
    }

    private var trackColor: Color {
        if !isEnabled {
            return TeslaColors.glassBackground
        }
        return isOn ? TeslaColors.statusGreen : TeslaColors.glassBackground
    }
}

// MARK: - Tesla Toggle Style

/// Toggle用のカスタムスタイル（標準Toggle向け）
struct TeslaToggleStyle: ToggleStyle {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    func makeBody(configuration: Configuration) -> some View {
        HStack {
            configuration.label
                .font(TeslaTypography.titleMedium)
                .foregroundStyle(TeslaColors.textPrimary)

            Spacer()

            ZStack(alignment: configuration.isOn ? .trailing : .leading) {
                RoundedRectangle(cornerRadius: 15.5)
                    .fill(configuration.isOn ? TeslaColors.statusGreen : TeslaColors.glassBackground)
                    .frame(width: 51, height: 31)

                Circle()
                    .fill(Color.white)
                    .frame(width: 27, height: 27)
                    .shadow(color: .black.opacity(0.15), radius: 4, y: 2)
                    .padding(2)
            }
            .animation(reduceMotion ? .none : TeslaAnimation.quick, value: configuration.isOn)
            .onTapGesture {
                configuration.isOn.toggle()
            }
        }
    }
}

extension ToggleStyle where Self == TeslaToggleStyle {
    /// Tesla風トグルスタイル
    static var tesla: TeslaToggleStyle { TeslaToggleStyle() }
}

// MARK: - Convenience Initializers

extension TeslaToggle {
    /// 基本的な初期化
    /// - Parameters:
    ///   - label: ラベルテキスト
    ///   - isOn: オン/オフ状態
    init(_ label: String, isOn: Binding<Bool>) {
        self.label = label
        self._isOn = isOn
    }

    /// アイコン付きの初期化
    /// - Parameters:
    ///   - label: ラベルテキスト
    ///   - icon: アイコン
    ///   - isOn: オン/オフ状態
    init(_ label: String, icon: TeslaIcon, isOn: Binding<Bool>) {
        self.label = label
        self.icon = icon
        self._isOn = isOn
    }
}

// MARK: - Preview

#Preview("Tesla Toggle") {
    struct TogglePreview: View {
        @State private var isClimateOn = true
        @State private var isSeatHeaterOn = false
        @State private var isDefrostOn = false
        @State private var isAutoModeOn = true

        var body: some View {
            VStack(spacing: 24) {
                // Basic Toggles
                VStack(alignment: .leading, spacing: 16) {
                    Text("Basic Toggles")
                        .font(TeslaTypography.headlineSmall)
                        .foregroundStyle(TeslaColors.textPrimary)

                    VStack(spacing: 16) {
                        TeslaToggle("空調", icon: .climate, isOn: $isClimateOn)

                        TeslaToggle(
                            isOn: $isSeatHeaterOn,
                            label: "シートヒーター",
                            icon: .seatHeater,
                            onLabel: "ON",
                            offLabel: "OFF"
                        )

                        TeslaToggle("デフロスター", icon: .defrost, isOn: $isDefrostOn)
                    }
                    .padding(16)
                    .teslaCard()
                }

                Divider()
                    .background(TeslaColors.glassBorder)

                // Standard Toggle with Tesla Style
                VStack(alignment: .leading, spacing: 16) {
                    Text("Standard Toggle Style")
                        .font(TeslaTypography.headlineSmall)
                        .foregroundStyle(TeslaColors.textPrimary)

                    Toggle("オートモード", isOn: $isAutoModeOn)
                        .toggleStyle(.tesla)
                        .padding(16)
                        .teslaCard()
                }

                Divider()
                    .background(TeslaColors.glassBorder)

                // Disabled Toggle
                VStack(alignment: .leading, spacing: 16) {
                    Text("Disabled")
                        .font(TeslaTypography.headlineSmall)
                        .foregroundStyle(TeslaColors.textPrimary)

                    TeslaToggle("無効なトグル", icon: .settings, isOn: .constant(false))
                        .disabled(true)
                        .padding(16)
                        .teslaCard()
                }

                Spacer()
            }
            .padding(24)
            .background(TeslaColors.background)
        }
    }

    return TogglePreview()
}
