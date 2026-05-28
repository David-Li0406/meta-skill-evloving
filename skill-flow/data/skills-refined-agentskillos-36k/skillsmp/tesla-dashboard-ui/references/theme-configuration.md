# Theme Configuration / テーマ設定

Tesla Dashboard UIのテーマシステムと設定方法について解説します。

## Overview / 概要

`@Observable` + `Environment` パターンを使用したテーマプロバイダーシステムです。

## Theme Provider / テーマプロバイダー

### 基本構造

```swift
@Observable
final class TeslaTheme {
    var colors: TeslaColorScheme = .dark
    var typography: TeslaTypographyScheme = .default
    var animation: TeslaAnimationScheme = .default
}
```

### Environment Key

```swift
struct TeslaThemeKey: EnvironmentKey {
    static let defaultValue = TeslaTheme()
}

extension EnvironmentValues {
    var teslaTheme: TeslaTheme {
        get { self[TeslaThemeKey.self] }
        set { self[TeslaThemeKey.self] = newValue }
    }
}
```

### 使用方法

```swift
// アプリのルートで設定
@main
struct TeslaDashboardApp: App {
    var body: some Scene {
        WindowGroup {
            TeslaMainDashboard()
                .teslaTheme()  // テーマを適用
        }
    }
}

// コンポーネント内でアクセス
struct TeslaIconButton: View {
    @Environment(\.teslaTheme) private var theme

    var body: some View {
        // theme.colors, theme.typography を使用
    }
}
```

## Color Scheme / カラースキーム

### TeslaColorScheme

```swift
struct TeslaColorScheme {
    let background: Color
    let surface: Color
    let surfaceElevated: Color
    let accent: Color
    let textPrimary: Color
    let textSecondary: Color
    let textTertiary: Color
    let textDisabled: Color
    let statusGreen: Color
    let statusOrange: Color
    let statusRed: Color
    let glassBackground: Color
    let glassBorder: Color
}
```

### ダークテーマ（デフォルト）

```swift
extension TeslaColorScheme {
    static let dark = TeslaColorScheme(
        background: Color(hex: "#141416"),
        surface: Color(hex: "#1E1E22"),
        surfaceElevated: Color(hex: "#28282C"),
        accent: Color(hex: "#3399FF"),
        textPrimary: Color(hex: "#FFFFFF"),
        textSecondary: Color(hex: "#B3B3B3"),
        textTertiary: Color(hex: "#666666"),
        textDisabled: Color(hex: "#4D4D4D"),
        statusGreen: Color(hex: "#4DD966"),
        statusOrange: Color(hex: "#FF9933"),
        statusRed: Color(hex: "#F24D4D"),
        glassBackground: Color.white.opacity(0.08),
        glassBorder: Color.white.opacity(0.12)
    )
}
```

## Typography Scheme / タイポグラフィスキーム

### TeslaTypographyScheme

```swift
struct TeslaTypographyScheme {
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
    let labelLarge: Font
    let labelMedium: Font
    let labelSmall: Font
}
```

### デフォルトスキーム

```swift
extension TeslaTypographyScheme {
    static let `default` = TeslaTypographyScheme(
        displayLarge: .system(size: 57, weight: .bold),
        displayMedium: .system(size: 45, weight: .bold),
        displaySmall: .system(size: 36, weight: .bold),
        headlineLarge: .system(size: 32, weight: .semibold),
        headlineMedium: .system(size: 28, weight: .semibold),
        headlineSmall: .system(size: 24, weight: .semibold),
        titleLarge: .system(size: 22, weight: .semibold),
        titleMedium: .system(size: 16, weight: .medium),
        titleSmall: .system(size: 14, weight: .medium),
        bodyLarge: .system(size: 16, weight: .regular),
        bodyMedium: .system(size: 14, weight: .regular),
        labelLarge: .system(size: 14, weight: .medium),
        labelMedium: .system(size: 12, weight: .medium),
        labelSmall: .system(size: 11, weight: .medium)
    )
}
```

## Animation Scheme / アニメーションスキーム

### TeslaAnimationScheme

```swift
struct TeslaAnimationScheme {
    let standard: Animation
    let quick: Animation
    let slow: Animation
    let bouncy: Animation
}
```

### デフォルトスキーム

```swift
extension TeslaAnimationScheme {
    static let `default` = TeslaAnimationScheme(
        standard: .spring(response: 0.35, dampingFraction: 0.8),
        quick: .spring(response: 0.25, dampingFraction: 0.85),
        slow: .spring(response: 0.5, dampingFraction: 0.75),
        bouncy: .spring(response: 0.4, dampingFraction: 0.6)
    )
}
```

## View Modifiers / ビューモディファイア

### .teslaTheme()

テーマプロバイダーを適用：

```swift
ContentView()
    .teslaTheme()
```

### .teslaCard()

カードスタイルを適用：

```swift
VStack { ... }
    .teslaCard()

// 実装
func teslaCard() -> some View {
    self
        .padding(16)
        .background(TeslaColors.surface)
        .clipShape(RoundedRectangle(cornerRadius: 16))
}
```

### .teslaGlassmorphism()

ガラスモーフィズム効果を適用：

```swift
VStack { ... }
    .teslaGlassmorphism()

// 実装
func teslaGlassmorphism() -> some View {
    self
        .background(.ultraThinMaterial)
        .background(TeslaColors.glassBackground)
        .clipShape(RoundedRectangle(cornerRadius: 16))
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(TeslaColors.glassBorder, lineWidth: 1)
        )
}
```

### .teslaSurface()

サーフェススタイルを適用：

```swift
VStack { ... }
    .teslaSurface()
```

### .teslaPulse()

パルスアニメーションを適用（充電中など）：

```swift
Image(systemName: "bolt.fill")
    .teslaPulse()
```

## Customization / カスタマイズ

### カスタムカラースキーム

```swift
extension TeslaColorScheme {
    static let custom = TeslaColorScheme(
        background: Color(hex: "#0A0A0C"),
        surface: Color(hex: "#161618"),
        // ... 他のカラーを定義
    )
}

// 使用
TeslaMainDashboard()
    .environment(\.teslaTheme, {
        let theme = TeslaTheme()
        theme.colors = .custom
        return theme
    }())
```

### Dynamic Type対応

```swift
extension TeslaTypographyScheme {
    static func scaled(for category: ContentSizeCategory) -> TeslaTypographyScheme {
        let scaleFactor = scaleFactor(for: category)
        return TeslaTypographyScheme(
            displayLarge: .system(size: 57 * scaleFactor, weight: .bold),
            // ...
        )
    }
}
```

## Best Practices / ベストプラクティス

### 1. 直接カラー使用を避ける

```swift
// ✅ Good
.foregroundStyle(TeslaColors.textPrimary)

// ❌ Bad
.foregroundStyle(Color.white)
```

### 2. テーマをEnvironmentから取得

```swift
// ✅ Good
@Environment(\.teslaTheme) private var theme

var body: some View {
    Text("Hello")
        .font(theme.typography.titleMedium)
}

// ❌ Bad（直接参照）
Text("Hello")
    .font(TeslaTypography.titleMedium)
```

### 3. Reduce Motion対応

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion

withAnimation(reduceMotion ? .none : TeslaAnimation.quick) {
    // ...
}
```

## Related Documents / 関連ドキュメント

- [Design System](./design-system.md)
- [Animation Guidelines](./animation-guidelines.md)
- [Accessibility Guide](./accessibility-guide.md)
