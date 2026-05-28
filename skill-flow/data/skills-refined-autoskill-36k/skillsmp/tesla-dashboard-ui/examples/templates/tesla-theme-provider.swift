// Tesla Dashboard UI - Theme Provider
// @Observable + Environment によるテーマプロバイダー
// iOS 17+ の Observation フレームワークを活用

import SwiftUI
import Observation

// MARK: - Tesla Theme

/// Tesla Dashboard UI のテーマ設定
/// @Observable により、テーマの変更が自動的にUIに反映される
@Observable
final class TeslaTheme {

    // MARK: - Properties

    /// カラースキーム
    var colors: TeslaColorScheme

    /// タイポグラフィスキーム
    var typography: TeslaTypographyScheme

    /// アニメーションスキーム
    var animation: TeslaAnimationScheme

    // MARK: - Initialization

    /// テーマを初期化
    /// - Parameters:
    ///   - colors: カラースキーム（デフォルト: ダーク）
    ///   - typography: タイポグラフィスキーム（デフォルト: default）
    ///   - animation: アニメーションスキーム（デフォルト: default）
    init(
        colors: TeslaColorScheme = .dark,
        typography: TeslaTypographyScheme = .default,
        animation: TeslaAnimationScheme = .default
    ) {
        self.colors = colors
        self.typography = typography
        self.animation = animation
    }

    // MARK: - Convenience Accessors

    /// 背景色
    var background: Color { colors.background }

    /// サーフェス色
    var surface: Color { colors.surface }

    /// アクセント色
    var accent: Color { colors.accent }

    /// プライマリテキスト色
    var textPrimary: Color { colors.textPrimary }

    /// セカンダリテキスト色
    var textSecondary: Color { colors.textSecondary }

    // MARK: - Animation Helpers

    /// 標準アニメーションを取得（Reduce Motion対応）
    /// - Parameter reduceMotion: Reduce Motionが有効か
    /// - Returns: 適切なアニメーション
    func standardAnimation(reduceMotion: Bool) -> Animation {
        reduceMotion ? .linear(duration: 0) : animation.standard
    }
}

// MARK: - Environment Key

/// TeslaTheme の EnvironmentKey
struct TeslaThemeKey: EnvironmentKey {
    static let defaultValue = TeslaTheme()
}

extension EnvironmentValues {
    /// Tesla Theme を Environment から取得・設定
    var teslaTheme: TeslaTheme {
        get { self[TeslaThemeKey.self] }
        set { self[TeslaThemeKey.self] = newValue }
    }
}

// MARK: - Theme Provider View

/// テーマを提供するコンテナビュー
struct TeslaThemeProvider<Content: View>: View {
    @State private var theme: TeslaTheme
    let content: () -> Content

    /// テーマプロバイダーを初期化
    /// - Parameters:
    ///   - theme: 使用するテーマ（デフォルト: 新規作成）
    ///   - content: コンテンツビュー
    init(
        theme: TeslaTheme = TeslaTheme(),
        @ViewBuilder content: @escaping () -> Content
    ) {
        self._theme = State(initialValue: theme)
        self.content = content
    }

    var body: some View {
        content()
            .environment(\.teslaTheme, theme)
            .preferredColorScheme(.dark)
    }
}

// MARK: - Themed View Protocol

/// Tesla Theme を使用するビューのプロトコル
protocol TeslaThemedView: View {
    var theme: TeslaTheme { get }
}

// MARK: - Theme Modifier

/// Tesla Theme を適用する ViewModifier
struct TeslaThemeModifier: ViewModifier {
    @Environment(\.teslaTheme) private var theme

    func body(content: Content) -> some View {
        content
            .background(theme.background)
            .foregroundStyle(theme.textPrimary)
    }
}

extension View {
    /// Tesla Theme の基本スタイルを適用
    func teslaThemed() -> some View {
        modifier(TeslaThemeModifier())
    }
}

// MARK: - Card Style Modifier

/// Tesla風カードスタイルを適用する ViewModifier
struct TeslaCardModifier: ViewModifier {
    @Environment(\.teslaTheme) private var theme
    let padding: CGFloat
    let cornerRadius: CGFloat

    func body(content: Content) -> some View {
        content
            .padding(padding)
            .background(theme.surface)
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
    }
}

extension View {
    /// Tesla風カードスタイルを適用
    /// - Parameters:
    ///   - padding: 内側の余白（デフォルト: 16）
    ///   - cornerRadius: 角丸半径（デフォルト: 16）
    func teslaCard(padding: CGFloat = 16, cornerRadius: CGFloat = 16) -> some View {
        modifier(TeslaCardModifier(padding: padding, cornerRadius: cornerRadius))
    }
}

// MARK: - Surface Style Modifier

/// 浮き上がったサーフェススタイルを適用する ViewModifier
struct TeslaSurfaceModifier: ViewModifier {
    @Environment(\.teslaTheme) private var theme
    let elevated: Bool
    let cornerRadius: CGFloat

    func body(content: Content) -> some View {
        content
            .background(elevated ? theme.colors.surfaceElevated : theme.surface)
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
    }
}

extension View {
    /// Tesla サーフェススタイルを適用
    /// - Parameters:
    ///   - elevated: 浮き上がったスタイルを使用するか（デフォルト: false）
    ///   - cornerRadius: 角丸半径（デフォルト: 16）
    func teslaSurface(elevated: Bool = false, cornerRadius: CGFloat = 16) -> some View {
        modifier(TeslaSurfaceModifier(elevated: elevated, cornerRadius: cornerRadius))
    }
}

// MARK: - Preview

#Preview("Tesla Theme Provider") {
    TeslaThemeProvider {
        VStack(spacing: 24) {
            // Header
            Text("Tesla Dashboard")
                .font(TeslaTypography.headlineLarge)
                .foregroundStyle(TeslaColors.textPrimary)

            // Cards
            VStack(spacing: 16) {
                // Standard Card
                VStack(alignment: .leading, spacing: 8) {
                    Text("Vehicle Status")
                        .font(TeslaTypography.titleMedium)
                    Text("All systems operational")
                        .font(TeslaTypography.bodyMedium)
                        .foregroundStyle(TeslaColors.textSecondary)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .teslaCard()

                // Glassmorphism Card
                VStack(alignment: .leading, spacing: 8) {
                    Text("Battery")
                        .font(TeslaTypography.titleMedium)
                    HStack {
                        Text("85%")
                            .font(TeslaTypography.displaySmall)
                            .foregroundStyle(TeslaColors.statusGreen)
                        Spacer()
                        Text("340 km")
                            .font(TeslaTypography.titleLarge)
                            .foregroundStyle(TeslaColors.textSecondary)
                    }
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(16)
                .teslaGlassmorphism()

                // Elevated Surface
                HStack {
                    Image(systemName: "location.fill")
                        .foregroundStyle(TeslaColors.accent)
                    Text("Navigation")
                        .font(TeslaTypography.titleMedium)
                    Spacer()
                    Image(systemName: "chevron.right")
                        .foregroundStyle(TeslaColors.textTertiary)
                }
                .padding(16)
                .teslaSurface(elevated: true)
            }

            Spacer()
        }
        .padding(24)
        .teslaThemed()
    }
}

// MARK: - App Integration Example

/*
 // アプリへの統合例

 @main
 struct TeslaDashboardApp: App {
     @State private var theme = TeslaTheme()

     var body: some Scene {
         WindowGroup {
             TeslaMainDashboard()
                 .environment(\.teslaTheme, theme)
                 .preferredColorScheme(.dark)
         }
         .modelContainer(for: [
             TeslaSettings.self,
             TeslaFavoriteLocation.self,
             TeslaTripHistory.self,
             TeslaEnergyStats.self
         ])
     }
 }

 // または TeslaThemeProvider を使用

 @main
 struct TeslaDashboardApp: App {
     var body: some Scene {
         WindowGroup {
             TeslaThemeProvider {
                 TeslaMainDashboard()
             }
         }
         .modelContainer(for: [
             TeslaSettings.self,
             TeslaFavoriteLocation.self,
             TeslaTripHistory.self,
             TeslaEnergyStats.self
         ])
     }
 }
 */
