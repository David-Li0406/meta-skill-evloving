// Tesla Dashboard UI - Icon Button
// ガラスモーフィズム効果のアイコンボタン
// アクセシビリティ完全対応

import SwiftUI

// MARK: - Tesla Icon Button

/// Tesla風アイコンボタン
/// ガラスモーフィズム効果と押下時のスケールアニメーション付き
struct TeslaIconButton: View {
    // MARK: - Properties

    let icon: TeslaIcon
    let label: String
    var isSelected: Bool = false
    var isDisabled: Bool = false
    var size: TeslaIconButtonSize = .medium
    let action: () -> Void

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    // MARK: - Body

    var body: some View {
        Button(action: action) {
            VStack(spacing: size.labelSpacing) {
                // Icon Container
                ZStack {
                    // Background
                    Circle()
                        .fill(backgroundColor)
                        .frame(width: size.circleSize, height: size.circleSize)

                    // Border (when not selected)
                    if !isSelected {
                        Circle()
                            .stroke(TeslaColors.glassBorder, lineWidth: 1)
                            .frame(width: size.circleSize, height: size.circleSize)
                    }

                    // Icon
                    TeslaIconView(
                        icon: icon,
                        size: size.iconSize,
                        color: iconColor
                    )
                }

                // Label
                Text(label)
                    .font(size.labelFont)
                    .foregroundStyle(labelColor)
                    .lineLimit(1)
            }
        }
        .buttonStyle(TeslaIconButtonStyle(reduceMotion: reduceMotion))
        .disabled(isDisabled)
        .accessibilityLabel(label)
        .accessibilityHint(isSelected ? "選択済み" : "ダブルタップで選択")
        .accessibilityAddTraits(isSelected ? .isSelected : [])
    }

    // MARK: - Computed Properties

    private var backgroundColor: Color {
        if isDisabled {
            return TeslaColors.glassBackground.opacity(0.5)
        }
        return isSelected ? TeslaColors.accent : TeslaColors.glassBackground
    }

    private var iconColor: Color {
        if isDisabled {
            return TeslaColors.textDisabled
        }
        return isSelected ? .white : TeslaColors.textSecondary
    }

    private var labelColor: Color {
        if isDisabled {
            return TeslaColors.textDisabled
        }
        return isSelected ? TeslaColors.accent : TeslaColors.textSecondary
    }
}

// MARK: - Button Size

/// アイコンボタンのサイズ
enum TeslaIconButtonSize {
    case small
    case medium
    case large

    var circleSize: CGFloat {
        switch self {
        case .small: return 44
        case .medium: return 56
        case .large: return 72
        }
    }

    var iconSize: CGFloat {
        switch self {
        case .small: return 18
        case .medium: return 24
        case .large: return 32
        }
    }

    var labelSpacing: CGFloat {
        switch self {
        case .small: return 4
        case .medium: return 8
        case .large: return 12
        }
    }

    var labelFont: Font {
        switch self {
        case .small: return TeslaTypography.labelSmall
        case .medium: return TeslaTypography.labelSmall
        case .large: return TeslaTypography.labelMedium
        }
    }
}

// MARK: - Button Style

/// Tesla風ボタンスタイル
struct TeslaIconButtonStyle: ButtonStyle {
    let reduceMotion: Bool

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.92 : 1.0)
            .animation(
                reduceMotion ? .none : TeslaAnimation.quick,
                value: configuration.isPressed
            )
    }
}

// MARK: - Convenience Initializers

extension TeslaIconButton {
    /// 基本的な初期化
    /// - Parameters:
    ///   - icon: 表示するアイコン
    ///   - label: ラベルテキスト
    ///   - action: タップ時のアクション
    init(
        icon: TeslaIcon,
        label: String,
        action: @escaping () -> Void
    ) {
        self.icon = icon
        self.label = label
        self.isSelected = false
        self.isDisabled = false
        self.size = .medium
        self.action = action
    }

    /// 選択状態を指定して初期化
    /// - Parameters:
    ///   - icon: 表示するアイコン
    ///   - label: ラベルテキスト
    ///   - isSelected: 選択状態
    ///   - action: タップ時のアクション
    init(
        icon: TeslaIcon,
        label: String,
        isSelected: Bool,
        action: @escaping () -> Void
    ) {
        self.icon = icon
        self.label = label
        self.isSelected = isSelected
        self.isDisabled = false
        self.size = .medium
        self.action = action
    }
}

// MARK: - Preview

#Preview("Tesla Icon Button") {
    struct IconButtonPreview: View {
        @State private var selectedIndex: Int? = 0

        let items: [(icon: TeslaIcon, label: String)] = [
            (.lock, "ロック"),
            (.climate, "空調"),
            (.light, "ライト"),
            (.trunk, "トランク"),
            (.seatHeater, "シート"),
            (.camera, "カメラ")
        ]

        var body: some View {
            VStack(spacing: 32) {
                // Size Variants
                VStack(alignment: .leading, spacing: 16) {
                    Text("Sizes")
                        .font(TeslaTypography.headlineSmall)
                        .foregroundStyle(TeslaColors.textPrimary)

                    HStack(spacing: 24) {
                        TeslaIconButton(
                            icon: .lock,
                            label: "Small",
                            isSelected: false,
                            isDisabled: false,
                            size: .small
                        ) {}

                        TeslaIconButton(
                            icon: .lock,
                            label: "Medium",
                            isSelected: false,
                            isDisabled: false,
                            size: .medium
                        ) {}

                        TeslaIconButton(
                            icon: .lock,
                            label: "Large",
                            isSelected: false,
                            isDisabled: false,
                            size: .large
                        ) {}
                    }
                }

                Divider()
                    .background(TeslaColors.glassBorder)

                // States
                VStack(alignment: .leading, spacing: 16) {
                    Text("States")
                        .font(TeslaTypography.headlineSmall)
                        .foregroundStyle(TeslaColors.textPrimary)

                    HStack(spacing: 24) {
                        TeslaIconButton(
                            icon: .lock,
                            label: "Default",
                            isSelected: false,
                            isDisabled: false,
                            size: .medium
                        ) {}

                        TeslaIconButton(
                            icon: .lock,
                            label: "Selected",
                            isSelected: true,
                            isDisabled: false,
                            size: .medium
                        ) {}

                        TeslaIconButton(
                            icon: .lock,
                            label: "Disabled",
                            isSelected: false,
                            isDisabled: true,
                            size: .medium
                        ) {}
                    }
                }

                Divider()
                    .background(TeslaColors.glassBorder)

                // Interactive Example
                VStack(alignment: .leading, spacing: 16) {
                    Text("Quick Actions")
                        .font(TeslaTypography.headlineSmall)
                        .foregroundStyle(TeslaColors.textPrimary)

                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 16) {
                            ForEach(items.indices, id: \.self) { index in
                                TeslaIconButton(
                                    icon: items[index].icon,
                                    label: items[index].label,
                                    isSelected: selectedIndex == index
                                ) {
                                    withAnimation(TeslaAnimation.quick) {
                                        if selectedIndex == index {
                                            selectedIndex = nil
                                        } else {
                                            selectedIndex = index
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            .padding(24)
            .background(TeslaColors.background)
        }
    }

    return IconButtonPreview()
}
