// Tesla Dashboard UI - Typography
// Tesla風大きめタイポグラフィスケール（Display 57pt〜）
// 車載ダッシュボード向けの高視認性を実現

import SwiftUI

// MARK: - Tesla Typography

/// Tesla Dashboard UI のタイポグラフィスケール
/// 車載ダッシュボード向けの大きめサイズで高視認性を実現
enum TeslaTypography {

    // MARK: - Display (速度・数値表示用)

    /// Display Large - 57pt Regular (速度表示)
    static let displayLarge = Font.system(size: 57, weight: .regular, design: .default)

    /// Display Medium - 45pt Regular (バッテリー残量)
    static let displayMedium = Font.system(size: 45, weight: .regular, design: .default)

    /// Display Small - 36pt Regular (航続距離)
    static let displaySmall = Font.system(size: 36, weight: .regular, design: .default)

    // MARK: - Headline (セクション見出し)

    /// Headline Large - 32pt Semibold
    static let headlineLarge = Font.system(size: 32, weight: .semibold, design: .default)

    /// Headline Medium - 28pt Semibold
    static let headlineMedium = Font.system(size: 28, weight: .semibold, design: .default)

    /// Headline Small - 24pt Semibold
    static let headlineSmall = Font.system(size: 24, weight: .semibold, design: .default)

    // MARK: - Title (サブセクション)

    /// Title Large - 22pt Medium
    static let titleLarge = Font.system(size: 22, weight: .medium, design: .default)

    /// Title Medium - 18pt Medium
    static let titleMedium = Font.system(size: 18, weight: .medium, design: .default)

    /// Title Small - 14pt Medium
    static let titleSmall = Font.system(size: 14, weight: .medium, design: .default)

    // MARK: - Body (本文)

    /// Body Large - 16pt Regular
    static let bodyLarge = Font.system(size: 16, weight: .regular, design: .default)

    /// Body Medium - 14pt Regular
    static let bodyMedium = Font.system(size: 14, weight: .regular, design: .default)

    /// Body Small - 12pt Regular
    static let bodySmall = Font.system(size: 12, weight: .regular, design: .default)

    // MARK: - Label (ボタン・ラベル)

    /// Label Large - 14pt Medium
    static let labelLarge = Font.system(size: 14, weight: .medium, design: .default)

    /// Label Medium - 12pt Medium
    static let labelMedium = Font.system(size: 12, weight: .medium, design: .default)

    /// Label Small - 10pt Medium
    static let labelSmall = Font.system(size: 10, weight: .medium, design: .default)

    // MARK: - Monospaced (数値表示)

    /// Monospaced Large - 57pt Regular Monospaced (速度表示)
    static let monospacedLarge = Font.system(size: 57, weight: .regular, design: .monospaced)

    /// Monospaced Medium - 36pt Regular Monospaced
    static let monospacedMedium = Font.system(size: 36, weight: .regular, design: .monospaced)

    /// Monospaced Small - 18pt Regular Monospaced
    static let monospacedSmall = Font.system(size: 18, weight: .regular, design: .monospaced)
}

// MARK: - Typography Scheme

/// テーマで使用するタイポグラフィスキーム
struct TeslaTypographyScheme: Sendable {
    let displayLarge: Font
    let displayMedium: Font
    let displaySmall: Font
    let headlineLarge: Font
    let headlineMedium: Font
    let headlineSmall: Font
    let titleLarge: Font
    let titleMedium: Font
    let titleSmall: Font
    let bodyLarge: Font
    let bodyMedium: Font
    let bodySmall: Font
    let labelLarge: Font
    let labelMedium: Font
    let labelSmall: Font

    /// デフォルトスキーム
    static let `default` = TeslaTypographyScheme(
        displayLarge: TeslaTypography.displayLarge,
        displayMedium: TeslaTypography.displayMedium,
        displaySmall: TeslaTypography.displaySmall,
        headlineLarge: TeslaTypography.headlineLarge,
        headlineMedium: TeslaTypography.headlineMedium,
        headlineSmall: TeslaTypography.headlineSmall,
        titleLarge: TeslaTypography.titleLarge,
        titleMedium: TeslaTypography.titleMedium,
        titleSmall: TeslaTypography.titleSmall,
        bodyLarge: TeslaTypography.bodyLarge,
        bodyMedium: TeslaTypography.bodyMedium,
        bodySmall: TeslaTypography.bodySmall,
        labelLarge: TeslaTypography.labelLarge,
        labelMedium: TeslaTypography.labelMedium,
        labelSmall: TeslaTypography.labelSmall
    )
}

// MARK: - Typography Modifiers

/// Dynamic Type対応のViewModifier
struct TeslaDynamicTypeModifier: ViewModifier {
    let font: Font
    let maxSize: DynamicTypeSize

    func body(content: Content) -> some View {
        content
            .font(font)
            .dynamicTypeSize(...maxSize)
    }
}

extension View {
    /// Tesla Typographyを適用（Dynamic Type制限付き）
    /// - Parameters:
    ///   - font: 適用するフォント
    ///   - maxSize: 最大Dynamic Typeサイズ（デフォルト: xxxLarge）
    func teslaFont(_ font: Font, maxSize: DynamicTypeSize = .xxxLarge) -> some View {
        modifier(TeslaDynamicTypeModifier(font: font, maxSize: maxSize))
    }
}

// MARK: - Text Style Extensions

extension Text {
    /// Display Large スタイルを適用
    func teslaDisplayLarge() -> Text {
        self.font(TeslaTypography.displayLarge)
    }

    /// Display Medium スタイルを適用
    func teslaDisplayMedium() -> Text {
        self.font(TeslaTypography.displayMedium)
    }

    /// Display Small スタイルを適用
    func teslaDisplaySmall() -> Text {
        self.font(TeslaTypography.displaySmall)
    }

    /// Headline Large スタイルを適用
    func teslaHeadlineLarge() -> Text {
        self.font(TeslaTypography.headlineLarge)
    }

    /// Headline Medium スタイルを適用
    func teslaHeadlineMedium() -> Text {
        self.font(TeslaTypography.headlineMedium)
    }

    /// Title Large スタイルを適用
    func teslaTitleLarge() -> Text {
        self.font(TeslaTypography.titleLarge)
    }

    /// Title Medium スタイルを適用
    func teslaTitleMedium() -> Text {
        self.font(TeslaTypography.titleMedium)
    }

    /// Body Large スタイルを適用
    func teslaBodyLarge() -> Text {
        self.font(TeslaTypography.bodyLarge)
    }

    /// Body Medium スタイルを適用
    func teslaBodyMedium() -> Text {
        self.font(TeslaTypography.bodyMedium)
    }

    /// Label Large スタイルを適用
    func teslaLabelLarge() -> Text {
        self.font(TeslaTypography.labelLarge)
    }

    /// Label Small スタイルを適用
    func teslaLabelSmall() -> Text {
        self.font(TeslaTypography.labelSmall)
    }
}

// MARK: - Preview

#Preview("Tesla Typography") {
    ScrollView {
        VStack(alignment: .leading, spacing: 24) {
            // Display
            VStack(alignment: .leading, spacing: 8) {
                Text("Display")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textSecondary)

                Text("120")
                    .font(TeslaTypography.displayLarge)
                    .foregroundStyle(TeslaColors.textPrimary)
                + Text(" km/h")
                    .font(TeslaTypography.titleMedium)
                    .foregroundStyle(TeslaColors.textSecondary)

                Text("85%")
                    .font(TeslaTypography.displayMedium)
                    .foregroundStyle(TeslaColors.statusGreen)

                Text("340 km")
                    .font(TeslaTypography.displaySmall)
                    .foregroundStyle(TeslaColors.textPrimary)
            }

            Divider()
                .background(TeslaColors.glassBorder)

            // Headline
            VStack(alignment: .leading, spacing: 8) {
                Text("Headline")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textSecondary)

                Text("Navigation")
                    .font(TeslaTypography.headlineLarge)
                    .foregroundStyle(TeslaColors.textPrimary)

                Text("Climate Control")
                    .font(TeslaTypography.headlineMedium)
                    .foregroundStyle(TeslaColors.textPrimary)

                Text("Quick Actions")
                    .font(TeslaTypography.headlineSmall)
                    .foregroundStyle(TeslaColors.textPrimary)
            }

            Divider()
                .background(TeslaColors.glassBorder)

            // Title
            VStack(alignment: .leading, spacing: 8) {
                Text("Title")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textSecondary)

                Text("Vehicle Status")
                    .font(TeslaTypography.titleLarge)
                    .foregroundStyle(TeslaColors.textPrimary)

                Text("Battery Information")
                    .font(TeslaTypography.titleMedium)
                    .foregroundStyle(TeslaColors.textPrimary)

                Text("Drive Mode")
                    .font(TeslaTypography.titleSmall)
                    .foregroundStyle(TeslaColors.textPrimary)
            }

            Divider()
                .background(TeslaColors.glassBorder)

            // Body
            VStack(alignment: .leading, spacing: 8) {
                Text("Body")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textSecondary)

                Text("Your Tesla is currently parked and charging.")
                    .font(TeslaTypography.bodyLarge)
                    .foregroundStyle(TeslaColors.textPrimary)

                Text("Estimated time to full charge: 2 hours 30 minutes")
                    .font(TeslaTypography.bodyMedium)
                    .foregroundStyle(TeslaColors.textSecondary)

                Text("Last updated: 5 minutes ago")
                    .font(TeslaTypography.bodySmall)
                    .foregroundStyle(TeslaColors.textTertiary)
            }

            Divider()
                .background(TeslaColors.glassBorder)

            // Label
            VStack(alignment: .leading, spacing: 8) {
                Text("Label")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textSecondary)

                HStack(spacing: 16) {
                    Text("LOCK")
                        .font(TeslaTypography.labelLarge)
                        .foregroundStyle(TeslaColors.textPrimary)

                    Text("CLIMATE")
                        .font(TeslaTypography.labelMedium)
                        .foregroundStyle(TeslaColors.textPrimary)

                    Text("SETTINGS")
                        .font(TeslaTypography.labelSmall)
                        .foregroundStyle(TeslaColors.textSecondary)
                }
            }
        }
        .padding(24)
    }
    .background(TeslaColors.background)
}
