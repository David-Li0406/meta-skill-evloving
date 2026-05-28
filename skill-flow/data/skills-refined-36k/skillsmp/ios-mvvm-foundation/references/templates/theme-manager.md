# Theme Manager Template

> Theme system setup với MVVM integration.

---

## 🎯 Overview

Complete theme manager template bao gồm:
- Domain entities (Theme, ColorPalette, Typography)
- ThemeService protocol và implementation
- MVVM integration (AppViewModel)
- SwiftUI Environment integration
- Theme persistence (UserDefaults)

---

## 📚 Full Documentation

Xem chi tiết tại [theme-system.md](../theme-system.md) cho:
- Architecture overview
- Implementation details
- SwiftUI integration
- Seasonal themes
- Best practices

---

## 🚀 Quick Start

### 1. Theme Entity

```swift
struct Theme: Identifiable, Equatable {
    let id: String
    let name: String
    let colors: ColorPalette
    let typography: Typography
}

struct ColorPalette: Equatable {
    let primary: Color
    let secondary: Color
    let background: Color
    let surface: Color
    let textPrimary: Color
    let textSecondary: Color
    let error: Color
}

struct Typography: Equatable {
    let h1: Font
    let h2: Font
    let body: Font
    let caption: Font
}
```

### 2. Environment Key

```swift
struct ThemeKey: EnvironmentKey {
    static let defaultValue: Theme = .defaultLight
}

extension EnvironmentValues {
    var theme: Theme {
        get { self[ThemeKey.self] }
        set { self[ThemeKey.self] = newValue }
    }
}
```

### 3. View Usage

```swift
struct MyView: View {
    @Environment(\.theme) var theme
    
    var body: some View {
        Text("Hello")
            .font(theme.typography.h1)
            .foregroundColor(theme.colors.textPrimary)
            .background(theme.colors.background)
    }
}
```

### 4. Theme Switching (AppViewModel)

```swift
class AppViewModel: ObservableObject {
    @Published var currentTheme: Theme = .defaultLight
    
    private let themeService: ThemeServiceProtocol
    
    func switchTheme(to themeId: String) {
        if let theme = themeService.getTheme(by: themeId) {
            currentTheme = theme
            themeService.saveSelectedTheme(themeId)
        }
    }
}
```

### 5. App Entry Point

```swift
@main
struct MyApp: App {
    @StateObject private var appViewModel = AppViewModel()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.theme, appViewModel.currentTheme)
        }
    }
}
```

---

## 📋 Checklist

- [ ] Theme entity với ColorPalette và Typography
- [ ] ThemeKey cho SwiftUI Environment
- [ ] ThemeService cho theme management
- [ ] AppViewModel cho theme switching
- [ ] Theme persistence trong UserDefaults
- [ ] Default themes (light/dark)
