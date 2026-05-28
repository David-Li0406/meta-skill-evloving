# Theme System

> Dynamic theme system với MVVM integration và Liquid Glass support (iOS 26+)

---

## 🎯 Architecture

| Component | Role |
|-----------|------|
| `AppViewModel` | Store theme ID (`@Published`) |
| `ThemeService` | Load/save themes |
| `@Environment(\.theme)` | Access theme trong View |

---

## ⚠️ Critical Rules

1. **Theme ID** trong `AppViewModel @Published` - single source of truth
2. **Theme object** access via `@Environment(\.theme)`
3. **Animation state** vẫn ở `@State` (không liên quan theme)
4. **Default theme** luôn available (fallback)

---

## 📦 Implementation

### AppViewModel

```swift
class AppViewModel: ObservableObject {
    @Published var currentThemeId: String = "default_light"  // Chỉ ID!
    @Published var availableThemes: [String] = []
    @Published var isLoadingTheme = false
    
    private let themeService: ThemeServiceProtocol
    
    init(themeService: ThemeServiceProtocol = Resolver.resolve()) {
        self.themeService = themeService
    }
    
    func loadSavedTheme() async {
        currentThemeId = await themeService.loadSavedTheme()
    }
    
    func selectTheme(id: String) async {
        isLoadingTheme = true
        defer { isLoadingTheme = false }
        
        currentThemeId = id
        await themeService.saveTheme(id: id)
    }
    
    func loadAvailableThemes() async {
        availableThemes = await themeService.getAvailableThemes()
    }
}
```

### Theme Provider (App Level)

```swift
@main
struct MyApp: App {
    @StateObject private var appViewModel = AppViewModel()
    @StateObject private var themeService = ThemeService()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(
                    \.theme,
                    themeService.getTheme(id: appViewModel.currentThemeId) ?? .defaultLight
                )
                .environmentObject(appViewModel)
                .task {
                    await appViewModel.loadSavedTheme()
                    await appViewModel.loadAvailableThemes()
                }
        }
    }
}
```

### Feature View (Consumer)

```swift
struct LoginView: View {
    @StateObject private var viewModel: LoginViewModel = .live()
    @Environment(\.theme) var theme
    
    // Animation vẫn ở @State
    @State private var buttonScale: CGFloat = 1.0
    
    var body: some View {
        VStack(spacing: theme.spacing.lg) {
            Text("Đăng nhập")
                .font(theme.typography.h1)
                .foregroundColor(theme.colors.textPrimary)
            
            TextField("Email", text: $email)
                .textFieldStyle(.roundedBorder)
            
            Button("Đăng nhập") {
                Task { await viewModel.login() }
            }
            .buttonStyle(.glass)  // iOS 26+
            .scaleEffect(buttonScale)
        }
        .padding(theme.spacing.lg)
        .background(theme.colors.background)
    }
}
```

---

## 🎨 Theme Structure

```swift
struct Theme {
    let id: String
    let name: String
    let colors: Colors
    let typography: Typography
    let spacing: Spacing
    
    struct Colors {
        let primary: Color
        let secondary: Color
        let background: Color
        let surface: Color
        let textPrimary: Color
        let textSecondary: Color
        let error: Color
        let success: Color
    }
    
    struct Typography {
        let h1: Font
        let h2: Font
        let body: Font
        let caption: Font
    }
    
    struct Spacing {
        let xs: CGFloat  // 4
        let sm: CGFloat  // 8
        let md: CGFloat  // 16
        let lg: CGFloat  // 24
        let xl: CGFloat  // 32
    }
}

// Default themes
extension Theme {
    static let defaultLight = Theme(
        id: "default_light",
        name: "Light",
        colors: Colors(
            primary: .blue,
            secondary: .purple,
            background: .white,
            surface: Color(.systemGray6),
            textPrimary: .primary,
            textSecondary: .secondary,
            error: .red,
            success: .green
        ),
        typography: Typography(
            h1: .largeTitle.bold(),
            h2: .title.bold(),
            body: .body,
            caption: .caption
        ),
        spacing: Spacing(xs: 4, sm: 8, md: 16, lg: 24, xl: 32)
    )
    
    static let defaultDark = Theme(
        id: "default_dark",
        name: "Dark",
        colors: Colors(
            primary: .blue,
            secondary: .purple,
            background: .black,
            surface: Color(.systemGray5),
            textPrimary: .white,
            textSecondary: .gray,
            error: .red,
            success: .green
        ),
        typography: Typography(
            h1: .largeTitle.bold(),
            h2: .title.bold(),
            body: .body,
            caption: .caption
        ),
        spacing: Spacing(xs: 4, sm: 8, md: 16, lg: 24, xl: 32)
    )
}
```

---

## 🌍 Environment Key

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

---

## 🔄 Theme Switching

```swift
struct SettingsView: View {
    @EnvironmentObject var appViewModel: AppViewModel
    @Environment(\.theme) var theme
    
    var body: some View {
        List {
            Section("Giao diện") {
                ForEach(appViewModel.availableThemes, id: \.self) { themeId in
                    Button {
                        Task { await appViewModel.selectTheme(id: themeId) }
                    } label: {
                        HStack {
                            Text(themeId)
                            Spacer()
                            if appViewModel.currentThemeId == themeId {
                                Image(systemName: "checkmark")
                            }
                        }
                    }
                }
            }
        }
    }
}
```

---

## 🔗 Related

- [liquid-glass.md](liquid-glass.md) - iOS 26+ Liquid Glass
- [presentation-patterns.md](presentation-patterns.md) - View patterns

