# Settings/Preferences Reference (macOS 14+)

Comprehensive guide to implementing Settings windows and user preferences in macOS SwiftUI applications.

## Settings Scene

### Basic Settings Window

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        Settings {
            SettingsView()
        }
    }
}
```

The Settings scene:
- Opens via app menu (AppName > Settings...) or ⌘,
- Is a single-instance window
- Follows macOS Settings UI conventions

## TabView for Settings

### Standard Tabbed Settings

```swift
struct SettingsView: View {
    var body: some View {
        TabView {
            GeneralSettingsTab()
                .tabItem {
                    Label("General", systemImage: "gear")
                }

            AccountSettingsTab()
                .tabItem {
                    Label("Account", systemImage: "person.crop.circle")
                }

            AdvancedSettingsTab()
                .tabItem {
                    Label("Advanced", systemImage: "gearshape.2")
                }
        }
        .frame(width: 500, height: 350)
    }
}
```

### Tab with Badge

```swift
TabView {
    UpdatesTab()
        .tabItem {
            Label("Updates", systemImage: "arrow.down.circle")
        }
        .badge(3) // Shows update count
}
```

## @AppStorage

### Basic Usage

```swift
struct GeneralSettingsTab: View {
    @AppStorage("launchAtLogin") private var launchAtLogin = false
    @AppStorage("checkForUpdates") private var checkForUpdates = true
    @AppStorage("defaultFolder") private var defaultFolder = "~/Documents"

    var body: some View {
        Form {
            Toggle("Launch at Login", isOn: $launchAtLogin)
            Toggle("Check for Updates", isOn: $checkForUpdates)
            TextField("Default Folder", text: $defaultFolder)
        }
    }
}
```

### Supported Types

```swift
// Bool
@AppStorage("isEnabled") var isEnabled = false

// Int
@AppStorage("fontSize") var fontSize = 14

// Double
@AppStorage("volume") var volume = 0.5

// String
@AppStorage("username") var username = ""

// URL (stored as string)
@AppStorage("lastOpenedURL") var lastOpenedURL: URL?

// Data (use with caution for small data)
@AppStorage("customData") var customData: Data?

// RawRepresentable (enums)
@AppStorage("theme") var theme: Theme = .system
```

### Custom Suite

```swift
// Use a specific UserDefaults suite
@AppStorage("setting", store: UserDefaults(suiteName: "com.example.shared"))
private var setting = false
```

### Enum with RawRepresentable

```swift
enum Theme: String, CaseIterable {
    case system = "system"
    case light = "light"
    case dark = "dark"
}

struct AppearanceSettings: View {
    @AppStorage("theme") private var theme: Theme = .system

    var body: some View {
        Picker("Theme", selection: $theme) {
            ForEach(Theme.allCases, id: \.self) { theme in
                Text(theme.rawValue.capitalized)
            }
        }
    }
}
```

## Form Styles

### Grouped Form (Recommended for Settings)

```swift
struct GeneralSettingsTab: View {
    @AppStorage("autoSave") private var autoSave = true
    @AppStorage("autoSaveInterval") private var autoSaveInterval = 5

    var body: some View {
        Form {
            Section("Saving") {
                Toggle("Auto Save", isOn: $autoSave)

                if autoSave {
                    Picker("Interval", selection: $autoSaveInterval) {
                        Text("1 minute").tag(1)
                        Text("5 minutes").tag(5)
                        Text("10 minutes").tag(10)
                    }
                }
            }

            Section("Privacy") {
                Toggle("Send Analytics", isOn: .constant(false))
            }
        }
        .formStyle(.grouped)
        .padding()
    }
}
```

### Columns Form

```swift
Form {
    TextField("Name", text: $name)
    TextField("Email", text: $email)
    DatePicker("Birthday", selection: $birthday)
}
.formStyle(.columns)
```

## LabeledContent

For displaying read-only information:

```swift
Form {
    Section("Account") {
        LabeledContent("Name", value: user.name)
        LabeledContent("Email", value: user.email)
        LabeledContent("Plan", value: user.plan.displayName)
        LabeledContent("Member Since") {
            Text(user.joinDate.formatted())
        }
    }
}
```

## Common Settings Patterns

### Slider with Value Display

```swift
struct FontSettings: View {
    @AppStorage("fontSize") private var fontSize = 14.0

    var body: some View {
        Form {
            HStack {
                Slider(value: $fontSize, in: 10...24, step: 1) {
                    Text("Font Size")
                }

                Text("\(Int(fontSize)) pt")
                    .frame(width: 50)
                    .monospacedDigit()
            }
        }
    }
}
```

### Path/Folder Selection

```swift
struct LocationSettings: View {
    @AppStorage("downloadFolder") private var downloadFolder = ""

    var body: some View {
        Form {
            HStack {
                TextField("Download Folder", text: $downloadFolder)
                    .textFieldStyle(.roundedBorder)

                Button("Choose...") {
                    selectFolder()
                }
            }
        }
    }

    private func selectFolder() {
        let panel = NSOpenPanel()
        panel.canChooseFiles = false
        panel.canChooseDirectories = true
        panel.allowsMultipleSelection = false

        if panel.runModal() == .OK {
            downloadFolder = panel.url?.path ?? ""
        }
    }
}
```

### Keyboard Shortcut Configuration

```swift
struct ShortcutSettings: View {
    @AppStorage("shortcutEnabled") private var shortcutEnabled = true

    var body: some View {
        Form {
            Section("Global Shortcuts") {
                Toggle("Enable Shortcuts", isOn: $shortcutEnabled)

                if shortcutEnabled {
                    HStack {
                        Text("Show Window")
                        Spacer()
                        Text("⌥ Space")
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(.quaternary)
                            .clipShape(RoundedRectangle(cornerRadius: 4))
                    }
                }
            }
        }
    }
}
```

### Color Selection

```swift
struct AppearanceSettings: View {
    @AppStorage("accentColor") private var accentColor = "blue"

    let colors = ["blue", "purple", "pink", "red", "orange", "yellow", "green"]

    var body: some View {
        Form {
            Picker("Accent Color", selection: $accentColor) {
                ForEach(colors, id: \.self) { color in
                    HStack {
                        Circle()
                            .fill(Color(color))
                            .frame(width: 12, height: 12)
                        Text(color.capitalized)
                    }
                    .tag(color)
                }
            }
        }
    }
}
```

## Settings Window Sizing

```swift
struct SettingsView: View {
    var body: some View {
        TabView {
            GeneralTab()
                .tabItem { Label("General", systemImage: "gear") }

            AdvancedTab()
                .tabItem { Label("Advanced", systemImage: "gearshape.2") }
        }
        .frame(width: 500, height: 350)
        // Or use minimum constraints
        .frame(minWidth: 400, minHeight: 300)
    }
}
```

## iCloud Sync with NSUbiquitousKeyValueStore

```swift
class SettingsStore: ObservableObject {
    private let ubiquitousStore = NSUbiquitousKeyValueStore.default

    @Published var theme: String {
        didSet {
            ubiquitousStore.set(theme, forKey: "theme")
            ubiquitousStore.synchronize()
        }
    }

    init() {
        theme = ubiquitousStore.string(forKey: "theme") ?? "system"

        NotificationCenter.default.addObserver(
            self,
            selector: #selector(ubiquitousStoreDidChange),
            name: NSUbiquitousKeyValueStore.didChangeExternallyNotification,
            object: ubiquitousStore
        )
    }

    @objc private func ubiquitousStoreDidChange(_ notification: Notification) {
        theme = ubiquitousStore.string(forKey: "theme") ?? "system"
    }
}
```

## Reset to Defaults

```swift
struct AdvancedSettingsTab: View {
    @State private var showResetConfirmation = false

    var body: some View {
        Form {
            Section {
                Button("Reset All Settings", role: .destructive) {
                    showResetConfirmation = true
                }
            }
        }
        .confirmationDialog(
            "Reset All Settings?",
            isPresented: $showResetConfirmation,
            titleVisibility: .visible
        ) {
            Button("Reset", role: .destructive) {
                resetToDefaults()
            }
            Button("Cancel", role: .cancel) { }
        } message: {
            Text("This will reset all settings to their default values.")
        }
    }

    private func resetToDefaults() {
        let defaults = UserDefaults.standard
        let dictionary = defaults.dictionaryRepresentation()

        dictionary.keys.forEach { key in
            defaults.removeObject(forKey: key)
        }
    }
}
```

## @Observable Settings Class

For complex settings with computed properties:

```swift
@Observable
class AppSettings {
    @ObservationIgnored
    @AppStorage("fontSize") var fontSize = 14.0

    @ObservationIgnored
    @AppStorage("fontFamily") var fontFamily = "SF Mono"

    var font: Font {
        .custom(fontFamily, size: fontSize)
    }

    @ObservationIgnored
    @AppStorage("theme") var theme: Theme = .system

    func resetToDefaults() {
        fontSize = 14.0
        fontFamily = "SF Mono"
        theme = .system
    }
}
```

## Best Practices

1. **Use @AppStorage for Simple Values** - Ideal for basic preferences
2. **Group Related Settings** - Use Sections and TabView
3. **Provide Sensible Defaults** - Always specify default values
4. **Follow macOS Conventions** - Use standard UI patterns
5. **Support Reset** - Allow users to restore defaults
6. **Consider iCloud Sync** - For cross-device preferences
7. **Validate Input** - Ensure settings values are valid
8. **Size Appropriately** - Don't make settings windows too large or small

## Common Tab Icons

| Tab | System Image |
|-----|--------------|
| General | gear |
| Appearance | paintbrush |
| Account | person.crop.circle |
| Notifications | bell |
| Privacy | hand.raised |
| Security | lock |
| Advanced | gearshape.2 |
| Updates | arrow.down.circle |
| Shortcuts | keyboard |
| Sync | arrow.triangle.2.circlepath |
