// Tesla Dashboard UI - Color Palette
// ダークテーマ専用のカラーパレット定義
// Glassmorphism: blur 30, opacity 0.16

import SwiftUI

// MARK: - Tesla Colors

/// Tesla Dashboard UI のカラーパレット
/// ダークテーマ専用で、高コントラスト・高視認性を実現
enum TeslaColors {

    // MARK: - Background Colors

    /// メイン背景色 (#141416)
    static let background = Color(red: 0.078, green: 0.078, blue: 0.086)

    /// カード・パネル背景色 (#1E1E22)
    static let surface = Color(red: 0.118, green: 0.118, blue: 0.133)

    /// 浮き上がった要素の背景色 (#28282C)
    static let surfaceElevated = Color(red: 0.157, green: 0.157, blue: 0.173)

    // MARK: - Accent Colors

    /// Tesla Blue - 主要アクション色 (#3399FF)
    static let accent = Color(red: 0.2, green: 0.6, blue: 1.0)

    /// 正常ステータス・充電完了 (#4DD966)
    static let statusGreen = Color(red: 0.302, green: 0.851, blue: 0.400)

    /// 注意喚起・後進 (#FF9933)
    static let statusOrange = Color(red: 1.0, green: 0.6, blue: 0.2)

    /// エラー・緊急 (#F24D4D)
    static let statusRed = Color(red: 0.949, green: 0.302, blue: 0.302)

    // MARK: - Text Colors

    /// メインテキスト (#FFFFFF)
    static let textPrimary = Color.white

    /// サブテキスト (#B3B3B3)
    static let textSecondary = Color(white: 0.7)

    /// 補助テキスト (#808080)
    static let textTertiary = Color(white: 0.5)

    /// 無効テキスト (#4D4D4D)
    static let textDisabled = Color(white: 0.3)

    // MARK: - Glassmorphism

    /// ガラスモーフィズム背景 (#FFFFFF with 8% opacity)
    static let glassBackground = Color.white.opacity(0.08)

    /// ガラスモーフィズム背景（強調） (#FFFFFF with 16% opacity)
    static let glassBackgroundElevated = Color.white.opacity(0.16)

    /// ガラスモーフィズム境界線 (#FFFFFF with 12% opacity)
    static let glassBorder = Color.white.opacity(0.12)

    // MARK: - Semantic Colors

    /// 駐車中ステータス
    static let statusParked = statusGreen

    /// 走行中ステータス
    static let statusDriving = accent

    /// 後進ステータス
    static let statusReverse = statusOrange

    /// 充電中ステータス
    static let statusCharging = statusGreen

    /// ドア開放警告
    static let doorOpen = statusOrange

    /// ドア閉鎖
    static let doorClosed = statusGreen
}

// MARK: - Color Scheme

/// テーマで使用するカラースキーム
struct TeslaColorScheme: Sendable {
    let background: Color
    let surface: Color
    let surfaceElevated: Color
    let accent: Color
    let statusGreen: Color
    let statusOrange: Color
    let statusRed: Color
    let textPrimary: Color
    let textSecondary: Color
    let textTertiary: Color
    let glassBackground: Color
    let glassBorder: Color

    /// ダークテーマ（デフォルト）
    static let dark = TeslaColorScheme(
        background: TeslaColors.background,
        surface: TeslaColors.surface,
        surfaceElevated: TeslaColors.surfaceElevated,
        accent: TeslaColors.accent,
        statusGreen: TeslaColors.statusGreen,
        statusOrange: TeslaColors.statusOrange,
        statusRed: TeslaColors.statusRed,
        textPrimary: TeslaColors.textPrimary,
        textSecondary: TeslaColors.textSecondary,
        textTertiary: TeslaColors.textTertiary,
        glassBackground: TeslaColors.glassBackground,
        glassBorder: TeslaColors.glassBorder
    )
}

// MARK: - Glassmorphism Modifier

/// ガラスモーフィズム効果を適用するViewModifier
struct TeslaGlassmorphismModifier: ViewModifier {
    var blurRadius: CGFloat = 30
    var opacity: CGFloat = 0.16
    var cornerRadius: CGFloat = 16
    var showBorder: Bool = true

    func body(content: Content) -> some View {
        content
            .background(.ultraThinMaterial)
            .background(Color.white.opacity(opacity))
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
            .overlay {
                if showBorder {
                    RoundedRectangle(cornerRadius: cornerRadius)
                        .stroke(TeslaColors.glassBorder, lineWidth: 1)
                }
            }
    }
}

extension View {
    /// ガラスモーフィズム効果を適用
    /// - Parameters:
    ///   - blurRadius: ブラー半径（デフォルト: 30）
    ///   - opacity: 背景の不透明度（デフォルト: 0.16）
    ///   - cornerRadius: 角丸半径（デフォルト: 16）
    ///   - showBorder: 境界線を表示するか（デフォルト: true）
    func teslaGlassmorphism(
        blurRadius: CGFloat = 30,
        opacity: CGFloat = 0.16,
        cornerRadius: CGFloat = 16,
        showBorder: Bool = true
    ) -> some View {
        modifier(TeslaGlassmorphismModifier(
            blurRadius: blurRadius,
            opacity: opacity,
            cornerRadius: cornerRadius,
            showBorder: showBorder
        ))
    }
}

// MARK: - Preview

#Preview("Tesla Colors") {
    ScrollView {
        VStack(spacing: 24) {
            // Background Colors
            VStack(alignment: .leading, spacing: 12) {
                Text("Background Colors")
                    .font(.headline)
                    .foregroundStyle(TeslaColors.textPrimary)

                HStack(spacing: 12) {
                    ColorSwatch(color: TeslaColors.background, name: "Background")
                    ColorSwatch(color: TeslaColors.surface, name: "Surface")
                    ColorSwatch(color: TeslaColors.surfaceElevated, name: "Elevated")
                }
            }

            // Accent Colors
            VStack(alignment: .leading, spacing: 12) {
                Text("Accent Colors")
                    .font(.headline)
                    .foregroundStyle(TeslaColors.textPrimary)

                HStack(spacing: 12) {
                    ColorSwatch(color: TeslaColors.accent, name: "Accent")
                    ColorSwatch(color: TeslaColors.statusGreen, name: "Green")
                    ColorSwatch(color: TeslaColors.statusOrange, name: "Orange")
                    ColorSwatch(color: TeslaColors.statusRed, name: "Red")
                }
            }

            // Text Colors
            VStack(alignment: .leading, spacing: 12) {
                Text("Text Colors")
                    .font(.headline)
                    .foregroundStyle(TeslaColors.textPrimary)

                HStack(spacing: 12) {
                    ColorSwatch(color: TeslaColors.textPrimary, name: "Primary")
                    ColorSwatch(color: TeslaColors.textSecondary, name: "Secondary")
                    ColorSwatch(color: TeslaColors.textTertiary, name: "Tertiary")
                }
            }

            // Glassmorphism
            VStack(alignment: .leading, spacing: 12) {
                Text("Glassmorphism")
                    .font(.headline)
                    .foregroundStyle(TeslaColors.textPrimary)

                HStack {
                    Text("Glassmorphism Effect")
                        .foregroundStyle(TeslaColors.textPrimary)
                        .padding()
                        .teslaGlassmorphism()
                }
            }
        }
        .padding(24)
    }
    .background(TeslaColors.background)
}

// Helper view for preview
private struct ColorSwatch: View {
    let color: Color
    let name: String

    var body: some View {
        VStack(spacing: 8) {
            RoundedRectangle(cornerRadius: 8)
                .fill(color)
                .frame(width: 60, height: 60)
                .overlay {
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(TeslaColors.glassBorder, lineWidth: 1)
                }

            Text(name)
                .font(.caption2)
                .foregroundStyle(TeslaColors.textSecondary)
        }
    }
}
