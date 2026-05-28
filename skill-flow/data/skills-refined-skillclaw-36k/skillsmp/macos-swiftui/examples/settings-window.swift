// Settings Window Example (macOS 14+)
// Demonstrates Settings scene, TabView, and @AppStorage

import SwiftUI
import Observation

// MARK: - App Entry Point

@main
struct SettingsApp: App {
    @State private var appSettings = AppSettings()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(appSettings)
        }

        Settings {
            SettingsView()
                .environment(appSettings)
        }
    }
}

// MARK: - App Settings

@Observable
class AppSettings {
    // General
    @ObservationIgnored
    @AppStorage("defaultTab") var defaultTab: String = "general"

    @ObservationIgnored
    @AppStorage("launchAtLogin") var launchAtLogin: Bool = false

    @ObservationIgnored
    @AppStorage("checkForUpdatesAutomatically") var checkForUpdatesAutomatically: Bool = true

    // Appearance
    @ObservationIgnored
    @AppStorage("appearanceMode") var appearanceMode: String = "system"

    @ObservationIgnored
    @AppStorage("accentColor") var accentColor: String = "blue"

    @ObservationIgnored
    @AppStorage("sidebarIconSize") var sidebarIconSize: Double = 1.0

    @ObservationIgnored
    @AppStorage("showItemCount") var showItemCount: Bool = true

    // Editor
    @ObservationIgnored
    @AppStorage("fontSize") var fontSize: Double = 14.0

    @ObservationIgnored
    @AppStorage("fontFamily") var fontFamily: String = "SF Mono"

    @ObservationIgnored
    @AppStorage("lineHeight") var lineHeight: Double = 1.5

    @ObservationIgnored
    @AppStorage("showLineNumbers") var showLineNumbers: Bool = true

    @ObservationIgnored
    @AppStorage("wrapLines") var wrapLines: Bool = true

    @ObservationIgnored
    @AppStorage("tabWidth") var tabWidth: Int = 4

    // Keyboard
    @ObservationIgnored
    @AppStorage("useVimKeyBindings") var useVimKeyBindings: Bool = false

    @ObservationIgnored
    @AppStorage("enableAutoComplete") var enableAutoComplete: Bool = true

    // Advanced
    @ObservationIgnored
    @AppStorage("enableTelemetry") var enableTelemetry: Bool = false

    @ObservationIgnored
    @AppStorage("cacheSize") var cacheSize: Int = 100

    @ObservationIgnored
    @AppStorage("logLevel") var logLevel: String = "info"

    func resetToDefaults() {
        defaultTab = "general"
        launchAtLogin = false
        checkForUpdatesAutomatically = true
        appearanceMode = "system"
        accentColor = "blue"
        sidebarIconSize = 1.0
        showItemCount = true
        fontSize = 14.0
        fontFamily = "SF Mono"
        lineHeight = 1.5
        showLineNumbers = true
        wrapLines = true
        tabWidth = 4
        useVimKeyBindings = false
        enableAutoComplete = true
        enableTelemetry = false
        cacheSize = 100
        logLevel = "info"
    }
}

// MARK: - Main Content View

struct ContentView: View {
    @Environment(AppSettings.self) private var settings
    @Environment(\.openSettings) private var openSettings

    var body: some View {
        VStack(spacing: 20) {
            Text("Settings Demo App")
                .font(.largeTitle)

            Text("Font Size: \(Int(settings.fontSize))pt")
                .font(.system(size: settings.fontSize))

            Button("Open Settings...") {
                openSettings()
            }
            .keyboardShortcut(",", modifiers: .command)
        }
        .frame(width: 400, height: 300)
    }
}

// MARK: - Settings View

struct SettingsView: View {
    @Environment(AppSettings.self) private var settings

    var body: some View {
        TabView {
            GeneralSettingsTab()
                .tabItem {
                    Label("General", systemImage: "gear")
                }
                .tag("general")

            AppearanceSettingsTab()
                .tabItem {
                    Label("Appearance", systemImage: "paintbrush")
                }
                .tag("appearance")

            EditorSettingsTab()
                .tabItem {
                    Label("Editor", systemImage: "doc.text")
                }
                .tag("editor")

            KeyboardSettingsTab()
                .tabItem {
                    Label("Keyboard", systemImage: "keyboard")
                }
                .tag("keyboard")

            AdvancedSettingsTab()
                .tabItem {
                    Label("Advanced", systemImage: "gearshape.2")
                }
                .tag("advanced")
        }
        .frame(width: 550, height: 400)
    }
}

// MARK: - General Settings Tab

struct GeneralSettingsTab: View {
    @AppStorage("launchAtLogin") private var launchAtLogin = false
    @AppStorage("checkForUpdatesAutomatically") private var checkForUpdatesAutomatically = true
    @AppStorage("defaultTab") private var defaultTab = "general"

    var body: some View {
        Form {
            Section {
                Toggle("Launch at Login", isOn: $launchAtLogin)
                Toggle("Check for Updates Automatically", isOn: $checkForUpdatesAutomatically)
            }

            Section("Default Settings") {
                Picker("Default Tab", selection: $defaultTab) {
                    Text("General").tag("general")
                    Text("Appearance").tag("appearance")
                    Text("Editor").tag("editor")
                    Text("Keyboard").tag("keyboard")
                    Text("Advanced").tag("advanced")
                }
            }

            Section {
                HStack {
                    Spacer()
                    Button("Check for Updates Now") {
                        // Check for updates
                    }
                }
            }
        }
        .formStyle(.grouped)
        .padding()
    }
}

// MARK: - Appearance Settings Tab

struct AppearanceSettingsTab: View {
    @AppStorage("appearanceMode") private var appearanceMode = "system"
    @AppStorage("accentColor") private var accentColor = "blue"
    @AppStorage("sidebarIconSize") private var sidebarIconSize = 1.0
    @AppStorage("showItemCount") private var showItemCount = true

    var body: some View {
        Form {
            Section("Theme") {
                Picker("Appearance", selection: $appearanceMode) {
                    Text("System").tag("system")
                    Text("Light").tag("light")
                    Text("Dark").tag("dark")
                }
                .pickerStyle(.segmented)

                Picker("Accent Color", selection: $accentColor) {
                    ColorCircle(color: .blue, name: "Blue").tag("blue")
                    ColorCircle(color: .purple, name: "Purple").tag("purple")
                    ColorCircle(color: .pink, name: "Pink").tag("pink")
                    ColorCircle(color: .red, name: "Red").tag("red")
                    ColorCircle(color: .orange, name: "Orange").tag("orange")
                    ColorCircle(color: .yellow, name: "Yellow").tag("yellow")
                    ColorCircle(color: .green, name: "Green").tag("green")
                    ColorCircle(color: .gray, name: "Graphite").tag("graphite")
                }
            }

            Section("Sidebar") {
                Slider(value: $sidebarIconSize, in: 0.5...2.0, step: 0.25) {
                    Text("Icon Size")
                } minimumValueLabel: {
                    Text("S")
                } maximumValueLabel: {
                    Text("L")
                }

                Toggle("Show Item Count", isOn: $showItemCount)
            }

            Section {
                HStack {
                    Text("Preview")
                        .foregroundStyle(.secondary)

                    Spacer()

                    // Preview of sidebar item
                    Label {
                        HStack {
                            Text("Documents")
                            if showItemCount {
                                Text("12")
                                    .foregroundStyle(.secondary)
                            }
                        }
                    } icon: {
                        Image(systemName: "folder")
                            .font(.system(size: 16 * sidebarIconSize))
                    }
                    .padding(8)
                    .background(.quaternary)
                    .clipShape(RoundedRectangle(cornerRadius: 6))
                }
            }
        }
        .formStyle(.grouped)
        .padding()
    }
}

struct ColorCircle: View {
    let color: Color
    let name: String

    var body: some View {
        Label {
            Text(name)
        } icon: {
            Circle()
                .fill(color)
                .frame(width: 12, height: 12)
        }
    }
}

// MARK: - Editor Settings Tab

struct EditorSettingsTab: View {
    @AppStorage("fontSize") private var fontSize = 14.0
    @AppStorage("fontFamily") private var fontFamily = "SF Mono"
    @AppStorage("lineHeight") private var lineHeight = 1.5
    @AppStorage("showLineNumbers") private var showLineNumbers = true
    @AppStorage("wrapLines") private var wrapLines = true
    @AppStorage("tabWidth") private var tabWidth = 4

    let fontFamilies = ["SF Mono", "Menlo", "Monaco", "Courier New", "Source Code Pro"]

    var body: some View {
        Form {
            Section("Font") {
                Picker("Font Family", selection: $fontFamily) {
                    ForEach(fontFamilies, id: \.self) { font in
                        Text(font)
                            .font(.custom(font, size: 13))
                            .tag(font)
                    }
                }

                HStack {
                    Text("Font Size")
                    Spacer()
                    TextField("", value: $fontSize, format: .number)
                        .frame(width: 50)
                        .textFieldStyle(.roundedBorder)
                    Stepper("", value: $fontSize, in: 8...72, step: 1)
                        .labelsHidden()
                }

                HStack {
                    Text("Line Height")
                    Spacer()
                    Slider(value: $lineHeight, in: 1.0...3.0, step: 0.1)
                        .frame(width: 150)
                    Text(String(format: "%.1f", lineHeight))
                        .frame(width: 30)
                }
            }

            Section("Display") {
                Toggle("Show Line Numbers", isOn: $showLineNumbers)
                Toggle("Wrap Lines", isOn: $wrapLines)
            }

            Section("Indentation") {
                Picker("Tab Width", selection: $tabWidth) {
                    Text("2 spaces").tag(2)
                    Text("4 spaces").tag(4)
                    Text("8 spaces").tag(8)
                }
            }

            Section {
                // Preview
                VStack(alignment: .leading) {
                    Text("Preview")
                        .font(.caption)
                        .foregroundStyle(.secondary)

                    HStack(alignment: .top, spacing: 8) {
                        if showLineNumbers {
                            VStack(alignment: .trailing) {
                                ForEach(1...3, id: \.self) { num in
                                    Text("\(num)")
                                        .font(.custom(fontFamily, size: fontSize))
                                        .foregroundStyle(.secondary)
                                }
                            }
                        }

                        VStack(alignment: .leading, spacing: CGFloat(lineHeight * 4)) {
                            Text("func hello() {")
                            Text("    print(\"Hello, World!\")")
                            Text("}")
                        }
                        .font(.custom(fontFamily, size: fontSize))
                    }
                    .padding()
                    .background(.background)
                    .clipShape(RoundedRectangle(cornerRadius: 8))
                }
            }
        }
        .formStyle(.grouped)
        .padding()
    }
}

// MARK: - Keyboard Settings Tab

struct KeyboardSettingsTab: View {
    @AppStorage("useVimKeyBindings") private var useVimKeyBindings = false
    @AppStorage("enableAutoComplete") private var enableAutoComplete = true

    var body: some View {
        Form {
            Section("Key Bindings") {
                Toggle("Use Vim Key Bindings", isOn: $useVimKeyBindings)
            }

            Section("Auto Complete") {
                Toggle("Enable Auto Complete", isOn: $enableAutoComplete)
            }

            Section("Shortcuts") {
                Grid(alignment: .leading, horizontalSpacing: 16, verticalSpacing: 8) {
                    GridRow {
                        Text("Save")
                            .foregroundStyle(.secondary)
                        Text("\u{2318}S")
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(.quaternary)
                            .clipShape(RoundedRectangle(cornerRadius: 4))
                    }

                    GridRow {
                        Text("Open Settings")
                            .foregroundStyle(.secondary)
                        Text("\u{2318},")
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(.quaternary)
                            .clipShape(RoundedRectangle(cornerRadius: 4))
                    }

                    GridRow {
                        Text("Find")
                            .foregroundStyle(.secondary)
                        Text("\u{2318}F")
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(.quaternary)
                            .clipShape(RoundedRectangle(cornerRadius: 4))
                    }
                }
            }
        }
        .formStyle(.grouped)
        .padding()
    }
}

// MARK: - Advanced Settings Tab

struct AdvancedSettingsTab: View {
    @Environment(AppSettings.self) private var settings
    @AppStorage("enableTelemetry") private var enableTelemetry = false
    @AppStorage("cacheSize") private var cacheSize = 100
    @AppStorage("logLevel") private var logLevel = "info"
    @State private var showResetConfirmation = false

    var body: some View {
        Form {
            Section("Privacy") {
                Toggle("Send Anonymous Usage Data", isOn: $enableTelemetry)
                Text("Help improve the app by sending anonymous usage statistics.")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Section("Performance") {
                HStack {
                    Text("Cache Size (MB)")
                    Spacer()
                    TextField("", value: $cacheSize, format: .number)
                        .frame(width: 60)
                        .textFieldStyle(.roundedBorder)
                }

                Button("Clear Cache") {
                    // Clear cache
                }
            }

            Section("Debugging") {
                Picker("Log Level", selection: $logLevel) {
                    Text("Error").tag("error")
                    Text("Warning").tag("warning")
                    Text("Info").tag("info")
                    Text("Debug").tag("debug")
                    Text("Verbose").tag("verbose")
                }

                Button("Open Logs Folder") {
                    // Open logs folder
                }
            }

            Section {
                HStack {
                    Spacer()
                    Button("Reset All Settings", role: .destructive) {
                        showResetConfirmation = true
                    }
                    Spacer()
                }
            }
        }
        .formStyle(.grouped)
        .padding()
        .confirmationDialog(
            "Reset All Settings?",
            isPresented: $showResetConfirmation,
            titleVisibility: .visible
        ) {
            Button("Reset", role: .destructive) {
                settings.resetToDefaults()
            }
            Button("Cancel", role: .cancel) { }
        } message: {
            Text("This will reset all settings to their default values. This action cannot be undone.")
        }
    }
}

// MARK: - Preview

#Preview("Settings Window") {
    SettingsView()
        .environment(AppSettings())
}

#Preview("General Tab") {
    GeneralSettingsTab()
        .frame(width: 500)
}

#Preview("Appearance Tab") {
    AppearanceSettingsTab()
        .environment(AppSettings())
        .frame(width: 500)
}

#Preview("Editor Tab") {
    EditorSettingsTab()
        .frame(width: 500)
}
