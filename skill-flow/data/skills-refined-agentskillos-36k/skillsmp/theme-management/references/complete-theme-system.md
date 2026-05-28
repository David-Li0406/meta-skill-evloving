# Complete Theme System Reference

<!-- Loading Trigger: Load this reference when implementing multi-theme support, custom color palettes, white-label theming, theme animations, or advanced accessibility color systems for iOS/tvOS applications -->

## Complete Theme Architecture

```swift
import SwiftUI
import Combine

// MARK: - Theme Protocol

protocol Theme: Equatable {
    var name: String { get }

    // Colors
    var colors: ThemeColors { get }

    // Typography
    var typography: ThemeTypography { get }

    // Spacing
    var spacing: ThemeSpacing { get }

    // Shapes
    var shapes: ThemeShapes { get }

    // Shadows
    var shadows: ThemeShadows { get }

    // Animation
    var animations: ThemeAnimations { get }
}

// MARK: - Theme Colors

struct ThemeColors: Equatable {
    // Primary palette
    let primary: Color
    let primaryVariant: Color
    let onPrimary: Color

    // Secondary palette
    let secondary: Color
    let secondaryVariant: Color
    let onSecondary: Color

    // Surface colors
    let background: Color
    let surface: Color
    let surfaceVariant: Color
    let onBackground: Color
    let onSurface: Color

    // Feedback colors
    let error: Color
    let onError: Color
    let warning: Color
    let onWarning: Color
    let success: Color
    let onSuccess: Color
    let info: Color
    let onInfo: Color

    // Text colors
    let textPrimary: Color
    let textSecondary: Color
    let textTertiary: Color
    let textDisabled: Color

    // Border colors
    let border: Color
    let borderFocused: Color
    let divider: Color

    // Interactive states
    let ripple: Color
    let highlight: Color
    let disabled: Color
}

// MARK: - Theme Typography

struct ThemeTypography: Equatable {
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

    let caption: Font
    let overline: Font

    static let `default` = ThemeTypography(
        displayLarge: .system(size: 57, weight: .regular),
        displayMedium: .system(size: 45, weight: .regular),
        displaySmall: .system(size: 36, weight: .regular),
        headlineLarge: .system(size: 32, weight: .semibold),
        headlineMedium: .system(size: 28, weight: .semibold),
        headlineSmall: .system(size: 24, weight: .semibold),
        titleLarge: .system(size: 22, weight: .medium),
        titleMedium: .system(size: 16, weight: .medium),
        titleSmall: .system(size: 14, weight: .medium),
        bodyLarge: .system(size: 16, weight: .regular),
        bodyMedium: .system(size: 14, weight: .regular),
        bodySmall: .system(size: 12, weight: .regular),
        labelLarge: .system(size: 14, weight: .medium),
        labelMedium: .system(size: 12, weight: .medium),
        labelSmall: .system(size: 11, weight: .medium),
        caption: .system(size: 12, weight: .regular),
        overline: .system(size: 10, weight: .medium)
    )
}

// MARK: - Theme Spacing

struct ThemeSpacing: Equatable {
    let xxs: CGFloat   // 2
    let xs: CGFloat    // 4
    let sm: CGFloat    // 8
    let md: CGFloat    // 16
    let lg: CGFloat    // 24
    let xl: CGFloat    // 32
    let xxl: CGFloat   // 48
    let xxxl: CGFloat  // 64

    static let `default` = ThemeSpacing(
        xxs: 2, xs: 4, sm: 8, md: 16, lg: 24, xl: 32, xxl: 48, xxxl: 64
    )
}

// MARK: - Theme Shapes

struct ThemeShapes: Equatable {
    let cornerRadiusSmall: CGFloat
    let cornerRadiusMedium: CGFloat
    let cornerRadiusLarge: CGFloat
    let cornerRadiusXLarge: CGFloat

    static let `default` = ThemeShapes(
        cornerRadiusSmall: 4,
        cornerRadiusMedium: 8,
        cornerRadiusLarge: 12,
        cornerRadiusXLarge: 16
    )
}

// MARK: - Theme Shadows

struct ThemeShadows: Equatable {
    let small: ShadowStyle
    let medium: ShadowStyle
    let large: ShadowStyle

    struct ShadowStyle: Equatable {
        let color: Color
        let radius: CGFloat
        let x: CGFloat
        let y: CGFloat
    }

    static let `default` = ThemeShadows(
        small: ShadowStyle(color: .black.opacity(0.1), radius: 4, x: 0, y: 2),
        medium: ShadowStyle(color: .black.opacity(0.15), radius: 8, x: 0, y: 4),
        large: ShadowStyle(color: .black.opacity(0.2), radius: 16, x: 0, y: 8)
    )
}

// MARK: - Theme Animations

struct ThemeAnimations: Equatable {
    let fast: Animation
    let normal: Animation
    let slow: Animation
    let spring: Animation

    static let `default` = ThemeAnimations(
        fast: .easeInOut(duration: 0.15),
        normal: .easeInOut(duration: 0.25),
        slow: .easeInOut(duration: 0.4),
        spring: .spring(response: 0.4, dampingFraction: 0.7)
    )
}
```

## Built-in Themes

```swift
// MARK: - Light Theme

struct LightTheme: Theme {
    let name = "Light"

    let colors = ThemeColors(
        primary: Color(hex: "#007AFF"),
        primaryVariant: Color(hex: "#0056B3"),
        onPrimary: .white,

        secondary: Color(hex: "#5856D6"),
        secondaryVariant: Color(hex: "#3634A3"),
        onSecondary: .white,

        background: Color(hex: "#F2F2F7"),
        surface: .white,
        surfaceVariant: Color(hex: "#F5F5F5"),
        onBackground: Color(hex: "#1C1C1E"),
        onSurface: Color(hex: "#1C1C1E"),

        error: Color(hex: "#FF3B30"),
        onError: .white,
        warning: Color(hex: "#FF9500"),
        onWarning: .white,
        success: Color(hex: "#34C759"),
        onSuccess: .white,
        info: Color(hex: "#007AFF"),
        onInfo: .white,

        textPrimary: Color(hex: "#1C1C1E"),
        textSecondary: Color(hex: "#3C3C43").opacity(0.6),
        textTertiary: Color(hex: "#3C3C43").opacity(0.3),
        textDisabled: Color(hex: "#3C3C43").opacity(0.2),

        border: Color(hex: "#C6C6C8"),
        borderFocused: Color(hex: "#007AFF"),
        divider: Color(hex: "#C6C6C8").opacity(0.5),

        ripple: Color.black.opacity(0.1),
        highlight: Color(hex: "#007AFF").opacity(0.1),
        disabled: Color(hex: "#D1D1D6")
    )

    let typography = ThemeTypography.default
    let spacing = ThemeSpacing.default
    let shapes = ThemeShapes.default
    let shadows = ThemeShadows.default
    let animations = ThemeAnimations.default
}

// MARK: - Dark Theme

struct DarkTheme: Theme {
    let name = "Dark"

    let colors = ThemeColors(
        primary: Color(hex: "#0A84FF"),
        primaryVariant: Color(hex: "#5AC8FA"),
        onPrimary: .white,

        secondary: Color(hex: "#5E5CE6"),
        secondaryVariant: Color(hex: "#BF5AF2"),
        onSecondary: .white,

        background: Color(hex: "#000000"),
        surface: Color(hex: "#1C1C1E"),
        surfaceVariant: Color(hex: "#2C2C2E"),
        onBackground: .white,
        onSurface: .white,

        error: Color(hex: "#FF453A"),
        onError: .white,
        warning: Color(hex: "#FF9F0A"),
        onWarning: .black,
        success: Color(hex: "#30D158"),
        onSuccess: .black,
        info: Color(hex: "#0A84FF"),
        onInfo: .white,

        textPrimary: .white,
        textSecondary: Color(hex: "#EBEBF5").opacity(0.6),
        textTertiary: Color(hex: "#EBEBF5").opacity(0.3),
        textDisabled: Color(hex: "#EBEBF5").opacity(0.2),

        border: Color(hex: "#38383A"),
        borderFocused: Color(hex: "#0A84FF"),
        divider: Color(hex: "#38383A"),

        ripple: Color.white.opacity(0.1),
        highlight: Color(hex: "#0A84FF").opacity(0.2),
        disabled: Color(hex: "#3A3A3C")
    )

    let typography = ThemeTypography.default
    let spacing = ThemeSpacing.default
    let shapes = ThemeShapes.default
    let shadows = ThemeShadows(
        small: .init(color: .black.opacity(0.3), radius: 4, x: 0, y: 2),
        medium: .init(color: .black.opacity(0.4), radius: 8, x: 0, y: 4),
        large: .init(color: .black.opacity(0.5), radius: 16, x: 0, y: 8)
    )
    let animations = ThemeAnimations.default
}

// MARK: - High Contrast Theme (Accessibility)

struct HighContrastLightTheme: Theme {
    let name = "High Contrast Light"

    let colors = ThemeColors(
        primary: Color(hex: "#0040DD"),
        primaryVariant: Color(hex: "#002080"),
        onPrimary: .white,

        secondary: Color(hex: "#4B0082"),
        secondaryVariant: Color(hex: "#2E0052"),
        onSecondary: .white,

        background: .white,
        surface: .white,
        surfaceVariant: Color(hex: "#F0F0F0"),
        onBackground: .black,
        onSurface: .black,

        error: Color(hex: "#C00000"),
        onError: .white,
        warning: Color(hex: "#8B4513"),
        onWarning: .white,
        success: Color(hex: "#006400"),
        onSuccess: .white,
        info: Color(hex: "#00008B"),
        onInfo: .white,

        textPrimary: .black,
        textSecondary: Color(hex: "#1A1A1A"),
        textTertiary: Color(hex: "#333333"),
        textDisabled: Color(hex: "#666666"),

        border: .black,
        borderFocused: Color(hex: "#0040DD"),
        divider: Color(hex: "#333333"),

        ripple: Color.black.opacity(0.2),
        highlight: Color(hex: "#0040DD").opacity(0.2),
        disabled: Color(hex: "#808080")
    )

    let typography = ThemeTypography.default
    let spacing = ThemeSpacing.default
    let shapes = ThemeShapes.default
    let shadows = ThemeShadows.default
    let animations = ThemeAnimations.default
}
```

## Theme Manager

```swift
import SwiftUI
import Combine

// MARK: - Theme Type Enum

enum ThemeType: String, CaseIterable, Identifiable {
    case system
    case light
    case dark
    case highContrastLight
    case highContrastDark

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .system: return "System"
        case .light: return "Light"
        case .dark: return "Dark"
        case .highContrastLight: return "High Contrast Light"
        case .highContrastDark: return "High Contrast Dark"
        }
    }

    var icon: String {
        switch self {
        case .system: return "circle.lefthalf.filled"
        case .light: return "sun.max.fill"
        case .dark: return "moon.fill"
        case .highContrastLight: return "sun.max.circle.fill"
        case .highContrastDark: return "moon.circle.fill"
        }
    }
}

// MARK: - Theme Manager

@MainActor
final class ThemeManager: ObservableObject {

    static let shared = ThemeManager()

    // MARK: - Published Properties

    @Published private(set) var currentTheme: any Theme
    @Published var selectedThemeType: ThemeType {
        didSet {
            UserDefaults.standard.set(selectedThemeType.rawValue, forKey: "selectedTheme")
            updateTheme()
        }
    }

    // MARK: - Private Properties

    private var colorSchemeObserver: AnyCancellable?
    private var systemColorScheme: ColorScheme = .light

    // MARK: - Initialization

    private init() {
        // Load saved theme preference
        let savedTheme = UserDefaults.standard.string(forKey: "selectedTheme") ?? ThemeType.system.rawValue
        self.selectedThemeType = ThemeType(rawValue: savedTheme) ?? .system
        self.currentTheme = LightTheme()

        updateTheme()
        observeSystemColorScheme()
    }

    // MARK: - Theme Resolution

    private func updateTheme() {
        let resolvedTheme: any Theme

        switch selectedThemeType {
        case .system:
            resolvedTheme = systemColorScheme == .dark ? DarkTheme() : LightTheme()
        case .light:
            resolvedTheme = LightTheme()
        case .dark:
            resolvedTheme = DarkTheme()
        case .highContrastLight:
            resolvedTheme = HighContrastLightTheme()
        case .highContrastDark:
            resolvedTheme = HighContrastDarkTheme()
        }

        withAnimation(.easeInOut(duration: 0.3)) {
            currentTheme = resolvedTheme
        }

        applyToUIKit()
    }

    // MARK: - System Color Scheme Observation

    private func observeSystemColorScheme() {
        // Monitor system appearance changes
        NotificationCenter.default.publisher(for: UIApplication.didBecomeActiveNotification)
            .sink { [weak self] _ in
                self?.checkSystemColorScheme()
            }
            .store(in: &cancellables)
    }

    private var cancellables = Set<AnyCancellable>()

    private func checkSystemColorScheme() {
        let newScheme: ColorScheme = UITraitCollection.current.userInterfaceStyle == .dark ? .dark : .light

        if newScheme != systemColorScheme {
            systemColorScheme = newScheme
            if selectedThemeType == .system {
                updateTheme()
            }
        }
    }

    func updateSystemColorScheme(_ colorScheme: ColorScheme) {
        if systemColorScheme != colorScheme {
            systemColorScheme = colorScheme
            if selectedThemeType == .system {
                updateTheme()
            }
        }
    }

    // MARK: - UIKit Application

    private func applyToUIKit() {
        // Apply theme to all windows
        for scene in UIApplication.shared.connectedScenes {
            guard let windowScene = scene as? UIWindowScene else { continue }

            for window in windowScene.windows {
                // Set interface style
                window.overrideUserInterfaceStyle = uiKitInterfaceStyle

                // Apply tint color
                window.tintColor = UIColor(currentTheme.colors.primary)
            }
        }

        // Update UINavigationBar appearance
        let navBarAppearance = UINavigationBarAppearance()
        navBarAppearance.configureWithOpaqueBackground()
        navBarAppearance.backgroundColor = UIColor(currentTheme.colors.surface)
        navBarAppearance.titleTextAttributes = [
            .foregroundColor: UIColor(currentTheme.colors.textPrimary)
        ]
        navBarAppearance.largeTitleTextAttributes = [
            .foregroundColor: UIColor(currentTheme.colors.textPrimary)
        ]

        UINavigationBar.appearance().standardAppearance = navBarAppearance
        UINavigationBar.appearance().scrollEdgeAppearance = navBarAppearance

        // Update UITabBar appearance
        let tabBarAppearance = UITabBarAppearance()
        tabBarAppearance.configureWithOpaqueBackground()
        tabBarAppearance.backgroundColor = UIColor(currentTheme.colors.surface)

        UITabBar.appearance().standardAppearance = tabBarAppearance
        UITabBar.appearance().scrollEdgeAppearance = tabBarAppearance
    }

    private var uiKitInterfaceStyle: UIUserInterfaceStyle {
        switch selectedThemeType {
        case .system:
            return .unspecified
        case .light, .highContrastLight:
            return .light
        case .dark, .highContrastDark:
            return .dark
        }
    }
}

// MARK: - High Contrast Dark Theme

struct HighContrastDarkTheme: Theme {
    let name = "High Contrast Dark"

    let colors = ThemeColors(
        primary: Color(hex: "#4DA6FF"),
        primaryVariant: Color(hex: "#80BFFF"),
        onPrimary: .black,

        secondary: Color(hex: "#A78BFA"),
        secondaryVariant: Color(hex: "#C4B5FD"),
        onSecondary: .black,

        background: .black,
        surface: Color(hex: "#0A0A0A"),
        surfaceVariant: Color(hex: "#141414"),
        onBackground: .white,
        onSurface: .white,

        error: Color(hex: "#FF6B6B"),
        onError: .black,
        warning: Color(hex: "#FFD93D"),
        onWarning: .black,
        success: Color(hex: "#6BCB77"),
        onSuccess: .black,
        info: Color(hex: "#4DA6FF"),
        onInfo: .black,

        textPrimary: .white,
        textSecondary: Color(hex: "#E0E0E0"),
        textTertiary: Color(hex: "#BDBDBD"),
        textDisabled: Color(hex: "#757575"),

        border: .white,
        borderFocused: Color(hex: "#4DA6FF"),
        divider: Color(hex: "#E0E0E0"),

        ripple: Color.white.opacity(0.2),
        highlight: Color(hex: "#4DA6FF").opacity(0.3),
        disabled: Color(hex: "#424242")
    )

    let typography = ThemeTypography.default
    let spacing = ThemeSpacing.default
    let shapes = ThemeShapes.default
    let shadows = ThemeShadows(
        small: .init(color: .white.opacity(0.1), radius: 4, x: 0, y: 2),
        medium: .init(color: .white.opacity(0.15), radius: 8, x: 0, y: 4),
        large: .init(color: .white.opacity(0.2), radius: 16, x: 0, y: 8)
    )
    let animations = ThemeAnimations.default
}
```

## Environment Integration

```swift
import SwiftUI

// MARK: - Theme Environment Key

private struct ThemeKey: EnvironmentKey {
    static let defaultValue: any Theme = LightTheme()
}

extension EnvironmentValues {
    var theme: any Theme {
        get { self[ThemeKey.self] }
        set { self[ThemeKey.self] = newValue }
    }
}

// MARK: - View Extension for Theme

extension View {
    func themed() -> some View {
        modifier(ThemedViewModifier())
    }
}

struct ThemedViewModifier: ViewModifier {
    @ObservedObject private var themeManager = ThemeManager.shared
    @Environment(\.colorScheme) private var colorScheme

    func body(content: Content) -> some View {
        content
            .environment(\.theme, themeManager.currentTheme)
            .onChange(of: colorScheme) { newScheme in
                themeManager.updateSystemColorScheme(newScheme)
            }
    }
}

// MARK: - Themed View Protocol

protocol ThemedView: View {
    associatedtype ThemedContent: View
    @ViewBuilder func themedBody(theme: any Theme) -> ThemedContent
}

extension ThemedView {
    var body: some View {
        ThemedBodyView(themedView: self)
    }
}

private struct ThemedBodyView<T: ThemedView>: View {
    let themedView: T
    @Environment(\.theme) private var theme

    var body: some View {
        themedView.themedBody(theme: theme)
    }
}

// MARK: - Usage Example

struct ExampleThemedView: ThemedView {
    func themedBody(theme: any Theme) -> some View {
        VStack(spacing: theme.spacing.md) {
            Text("Themed Title")
                .font(theme.typography.headlineMedium)
                .foregroundColor(theme.colors.textPrimary)

            Text("Themed body text")
                .font(theme.typography.bodyMedium)
                .foregroundColor(theme.colors.textSecondary)
        }
        .padding(theme.spacing.lg)
        .background(theme.colors.surface)
        .cornerRadius(theme.shapes.cornerRadiusMedium)
    }
}
```

## Themed Components

```swift
import SwiftUI

// MARK: - Themed Button Styles

struct ThemedPrimaryButtonStyle: ButtonStyle {
    @Environment(\.theme) private var theme
    @Environment(\.isEnabled) private var isEnabled

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(theme.typography.labelLarge)
            .foregroundColor(isEnabled ? theme.colors.onPrimary : theme.colors.textDisabled)
            .padding(.horizontal, theme.spacing.lg)
            .padding(.vertical, theme.spacing.sm)
            .background(
                RoundedRectangle(cornerRadius: theme.shapes.cornerRadiusMedium)
                    .fill(isEnabled ? theme.colors.primary : theme.colors.disabled)
            )
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .animation(theme.animations.fast, value: configuration.isPressed)
    }
}

struct ThemedSecondaryButtonStyle: ButtonStyle {
    @Environment(\.theme) private var theme
    @Environment(\.isEnabled) private var isEnabled

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(theme.typography.labelLarge)
            .foregroundColor(isEnabled ? theme.colors.primary : theme.colors.textDisabled)
            .padding(.horizontal, theme.spacing.lg)
            .padding(.vertical, theme.spacing.sm)
            .background(
                RoundedRectangle(cornerRadius: theme.shapes.cornerRadiusMedium)
                    .stroke(isEnabled ? theme.colors.primary : theme.colors.disabled, lineWidth: 1)
            )
            .scaleEffect(configuration.isPressed ? 0.98 : 1.0)
            .animation(theme.animations.fast, value: configuration.isPressed)
    }
}

// MARK: - Themed Text Field

struct ThemedTextField: View {
    let title: String
    @Binding var text: String
    var placeholder: String = ""
    var errorMessage: String?

    @Environment(\.theme) private var theme
    @FocusState private var isFocused: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: theme.spacing.xs) {
            Text(title)
                .font(theme.typography.labelMedium)
                .foregroundColor(theme.colors.textSecondary)

            TextField(placeholder, text: $text)
                .font(theme.typography.bodyMedium)
                .foregroundColor(theme.colors.textPrimary)
                .padding(theme.spacing.sm)
                .background(
                    RoundedRectangle(cornerRadius: theme.shapes.cornerRadiusSmall)
                        .fill(theme.colors.surfaceVariant)
                )
                .overlay(
                    RoundedRectangle(cornerRadius: theme.shapes.cornerRadiusSmall)
                        .stroke(borderColor, lineWidth: 1)
                )
                .focused($isFocused)

            if let error = errorMessage {
                Text(error)
                    .font(theme.typography.caption)
                    .foregroundColor(theme.colors.error)
            }
        }
    }

    private var borderColor: Color {
        if errorMessage != nil {
            return theme.colors.error
        } else if isFocused {
            return theme.colors.borderFocused
        } else {
            return theme.colors.border
        }
    }
}

// MARK: - Themed Card

struct ThemedCard<Content: View>: View {
    @Environment(\.theme) private var theme
    let content: Content

    init(@ViewBuilder content: () -> Content) {
        self.content = content()
    }

    var body: some View {
        content
            .padding(theme.spacing.md)
            .background(theme.colors.surface)
            .cornerRadius(theme.shapes.cornerRadiusMedium)
            .shadow(
                color: theme.shadows.medium.color,
                radius: theme.shadows.medium.radius,
                x: theme.shadows.medium.x,
                y: theme.shadows.medium.y
            )
    }
}

// MARK: - Themed Divider

struct ThemedDivider: View {
    @Environment(\.theme) private var theme
    var padding: CGFloat?

    var body: some View {
        Rectangle()
            .fill(theme.colors.divider)
            .frame(height: 1)
            .padding(.horizontal, padding ?? 0)
    }
}

// MARK: - Themed Badge

struct ThemedBadge: View {
    @Environment(\.theme) private var theme
    let text: String
    let style: BadgeStyle

    enum BadgeStyle {
        case primary, secondary, success, warning, error, info
    }

    var body: some View {
        Text(text)
            .font(theme.typography.labelSmall)
            .foregroundColor(foregroundColor)
            .padding(.horizontal, theme.spacing.sm)
            .padding(.vertical, theme.spacing.xxs)
            .background(
                Capsule()
                    .fill(backgroundColor)
            )
    }

    private var backgroundColor: Color {
        switch style {
        case .primary: return theme.colors.primary
        case .secondary: return theme.colors.secondary
        case .success: return theme.colors.success
        case .warning: return theme.colors.warning
        case .error: return theme.colors.error
        case .info: return theme.colors.info
        }
    }

    private var foregroundColor: Color {
        switch style {
        case .primary: return theme.colors.onPrimary
        case .secondary: return theme.colors.onSecondary
        case .success: return theme.colors.onSuccess
        case .warning: return theme.colors.onWarning
        case .error: return theme.colors.onError
        case .info: return theme.colors.onInfo
        }
    }
}
```

## Accessibility Contrast Validation

```swift
import SwiftUI

// MARK: - WCAG Contrast Levels

enum WCAGLevel {
    case aa        // 4.5:1 for normal text, 3:1 for large text
    case aaa       // 7:1 for normal text, 4.5:1 for large text

    var normalTextRatio: Double {
        switch self {
        case .aa: return 4.5
        case .aaa: return 7.0
        }
    }

    var largeTextRatio: Double {
        switch self {
        case .aa: return 3.0
        case .aaa: return 4.5
        }
    }
}

// MARK: - Color Extension for Contrast

extension Color {

    /// Calculate contrast ratio against another color
    func contrastRatio(against background: Color) -> Double {
        let fgLuminance = relativeLuminance
        let bgLuminance = background.relativeLuminance

        let lighter = max(fgLuminance, bgLuminance)
        let darker = min(fgLuminance, bgLuminance)

        return (lighter + 0.05) / (darker + 0.05)
    }

    /// Check if contrast meets WCAG level for normal text
    func meetsContrastRequirement(
        against background: Color,
        level: WCAGLevel = .aa,
        isLargeText: Bool = false
    ) -> Bool {
        let ratio = contrastRatio(against: background)
        let requiredRatio = isLargeText ? level.largeTextRatio : level.normalTextRatio
        return ratio >= requiredRatio
    }

    /// Get relative luminance (WCAG formula)
    var relativeLuminance: Double {
        let uiColor = UIColor(self)
        var red: CGFloat = 0
        var green: CGFloat = 0
        var blue: CGFloat = 0
        var alpha: CGFloat = 0

        uiColor.getRed(&red, green: &green, blue: &blue, alpha: &alpha)

        func linearize(_ value: CGFloat) -> Double {
            let v = Double(value)
            return v <= 0.03928 ? v / 12.92 : pow((v + 0.055) / 1.055, 2.4)
        }

        return 0.2126 * linearize(red) + 0.7152 * linearize(green) + 0.0722 * linearize(blue)
    }

    /// Suggest a color adjustment for better contrast
    func adjustedForContrast(
        against background: Color,
        level: WCAGLevel = .aa
    ) -> Color {
        var currentColor = self
        let requiredRatio = level.normalTextRatio
        var currentRatio = currentColor.contrastRatio(against: background)

        // Determine if we should lighten or darken
        let bgLuminance = background.relativeLuminance
        let shouldLighten = bgLuminance < 0.5

        var iterations = 0
        while currentRatio < requiredRatio && iterations < 20 {
            currentColor = shouldLighten ? currentColor.lighter(by: 0.05) : currentColor.darker(by: 0.05)
            currentRatio = currentColor.contrastRatio(against: background)
            iterations += 1
        }

        return currentColor
    }

    /// Lighten color by percentage
    func lighter(by percentage: Double) -> Color {
        adjust(by: abs(percentage))
    }

    /// Darken color by percentage
    func darker(by percentage: Double) -> Color {
        adjust(by: -abs(percentage))
    }

    private func adjust(by percentage: Double) -> Color {
        let uiColor = UIColor(self)
        var hue: CGFloat = 0
        var saturation: CGFloat = 0
        var brightness: CGFloat = 0
        var alpha: CGFloat = 0

        uiColor.getHue(&hue, saturation: &saturation, brightness: &brightness, alpha: &alpha)

        let newBrightness = max(0, min(1, brightness + CGFloat(percentage)))

        return Color(UIColor(hue: hue, saturation: saturation, brightness: newBrightness, alpha: alpha))
    }
}

// MARK: - Theme Contrast Validator

struct ThemeContrastValidator {
    let theme: any Theme

    struct ValidationResult {
        let colorPair: String
        let foreground: Color
        let background: Color
        let ratio: Double
        let meetsAA: Bool
        let meetsAAA: Bool
    }

    func validateAllColors() -> [ValidationResult] {
        var results: [ValidationResult] = []

        // Validate text colors against backgrounds
        let textPairs: [(String, Color, Color)] = [
            ("Text Primary on Background", theme.colors.textPrimary, theme.colors.background),
            ("Text Primary on Surface", theme.colors.textPrimary, theme.colors.surface),
            ("Text Secondary on Background", theme.colors.textSecondary, theme.colors.background),
            ("Text Secondary on Surface", theme.colors.textSecondary, theme.colors.surface),
            ("On Primary", theme.colors.onPrimary, theme.colors.primary),
            ("On Secondary", theme.colors.onSecondary, theme.colors.secondary),
            ("On Error", theme.colors.onError, theme.colors.error),
            ("On Success", theme.colors.onSuccess, theme.colors.success),
            ("On Warning", theme.colors.onWarning, theme.colors.warning),
        ]

        for (name, foreground, background) in textPairs {
            let ratio = foreground.contrastRatio(against: background)
            results.append(ValidationResult(
                colorPair: name,
                foreground: foreground,
                background: background,
                ratio: ratio,
                meetsAA: ratio >= WCAGLevel.aa.normalTextRatio,
                meetsAAA: ratio >= WCAGLevel.aaa.normalTextRatio
            ))
        }

        return results
    }

    func printValidationReport() {
        let results = validateAllColors()

        print("Theme Contrast Validation Report: \(theme.name)")
        print(String(repeating: "=", count: 60))

        for result in results {
            let aaStatus = result.meetsAA ? "PASS" : "FAIL"
            let aaaStatus = result.meetsAAA ? "PASS" : "FAIL"
            print("\(result.colorPair)")
            print("  Ratio: \(String(format: "%.2f", result.ratio)):1")
            print("  AA: \(aaStatus), AAA: \(aaaStatus)")
        }

        let failingAA = results.filter { !$0.meetsAA }
        if !failingAA.isEmpty {
            print("\nWARNING: \(failingAA.count) color pairs fail WCAG AA requirements")
        }
    }
}
```

## Theme Switching Animation

```swift
import SwiftUI

// MARK: - Animated Theme Switcher

struct AnimatedThemeSwitcher: View {
    @ObservedObject private var themeManager = ThemeManager.shared
    @State private var isAnimating = false

    var body: some View {
        Menu {
            ForEach(ThemeType.allCases) { themeType in
                Button {
                    switchTheme(to: themeType)
                } label: {
                    HStack {
                        Image(systemName: themeType.icon)
                        Text(themeType.displayName)
                        if themeManager.selectedThemeType == themeType {
                            Image(systemName: "checkmark")
                        }
                    }
                }
            }
        } label: {
            Image(systemName: themeManager.selectedThemeType.icon)
                .font(.title2)
                .rotationEffect(.degrees(isAnimating ? 360 : 0))
        }
    }

    private func switchTheme(to themeType: ThemeType) {
        withAnimation(.spring(response: 0.5, dampingFraction: 0.7)) {
            isAnimating = true
        }

        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
            themeManager.selectedThemeType = themeType
        }

        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
            isAnimating = false
        }
    }
}

// MARK: - Crossfade Theme Transition

struct CrossfadeThemeModifier: ViewModifier {
    @Environment(\.theme) private var theme
    @State private var opacity: Double = 1

    func body(content: Content) -> some View {
        content
            .opacity(opacity)
            .onChange(of: theme.name) { _ in
                withAnimation(.easeInOut(duration: 0.15)) {
                    opacity = 0.8
                }
                withAnimation(.easeInOut(duration: 0.15).delay(0.15)) {
                    opacity = 1
                }
            }
    }
}

extension View {
    func crossfadeOnThemeChange() -> some View {
        modifier(CrossfadeThemeModifier())
    }
}
```

## Color Utilities

```swift
import SwiftUI

// MARK: - Hex Color Extension

extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)

        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }

        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }

    var hexString: String {
        let uiColor = UIColor(self)
        var red: CGFloat = 0
        var green: CGFloat = 0
        var blue: CGFloat = 0
        var alpha: CGFloat = 0

        uiColor.getRed(&red, green: &green, blue: &blue, alpha: &alpha)

        return String(
            format: "#%02X%02X%02X",
            Int(red * 255),
            Int(green * 255),
            Int(blue * 255)
        )
    }
}

// MARK: - Dynamic Color

extension Color {
    static func dynamic(light: Color, dark: Color) -> Color {
        Color(UIColor { traits in
            traits.userInterfaceStyle == .dark ? UIColor(dark) : UIColor(light)
        })
    }
}
```
