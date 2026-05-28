// Basic macOS App Structure (macOS 14+)
// Demonstrates fundamental macOS SwiftUI app patterns

import SwiftUI
import Observation

// MARK: - App Entry Point

@main
struct BasicMacApp: App {
    @State private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(appState)
        }
        .defaultSize(width: 900, height: 600)
        .defaultPosition(.center)
        .commands {
            AppCommands()
        }

        Settings {
            SettingsView()
        }
    }
}

// MARK: - App State

@Observable
class AppState {
    var currentUser: User?
    var isAuthenticated: Bool { currentUser != nil }
    var sidebarItems: [SidebarItem] = SidebarItem.defaults

    func logout() {
        currentUser = nil
    }
}

// MARK: - Models

struct User: Identifiable, Codable {
    let id: UUID
    var name: String
    var email: String
}

struct SidebarItem: Identifiable, Hashable {
    let id: UUID
    let title: String
    let icon: String
    let category: Category

    enum Category: String, CaseIterable {
        case favorites = "Favorites"
        case library = "Library"
        case smart = "Smart Collections"
    }

    static let defaults: [SidebarItem] = [
        SidebarItem(id: UUID(), title: "All Items", icon: "square.grid.2x2", category: .favorites),
        SidebarItem(id: UUID(), title: "Recent", icon: "clock", category: .favorites),
        SidebarItem(id: UUID(), title: "Photos", icon: "photo", category: .library),
        SidebarItem(id: UUID(), title: "Videos", icon: "video", category: .library),
        SidebarItem(id: UUID(), title: "Documents", icon: "doc", category: .library),
    ]
}

// MARK: - Content View

struct ContentView: View {
    @Environment(AppState.self) private var appState
    @State private var selectedItem: SidebarItem?
    @State private var searchText = ""

    var body: some View {
        NavigationSplitView {
            SidebarView(selection: $selectedItem)
        } detail: {
            DetailView(selectedItem: selectedItem)
        }
        .searchable(text: $searchText, placement: .sidebar)
        .toolbar {
            ToolbarItemGroup(placement: .primaryAction) {
                Button(action: addItem) {
                    Label("Add", systemImage: "plus")
                }

                Button(action: refreshContent) {
                    Label("Refresh", systemImage: "arrow.clockwise")
                }
            }
        }
    }

    private func addItem() {
        // Add item action
    }

    private func refreshContent() {
        // Refresh content action
    }
}

// MARK: - Sidebar View

struct SidebarView: View {
    @Environment(AppState.self) private var appState
    @Binding var selection: SidebarItem?

    private var groupedItems: [SidebarItem.Category: [SidebarItem]] {
        Dictionary(grouping: appState.sidebarItems, by: \.category)
    }

    var body: some View {
        List(selection: $selection) {
            ForEach(SidebarItem.Category.allCases, id: \.self) { category in
                if let items = groupedItems[category] {
                    Section(category.rawValue) {
                        ForEach(items) { item in
                            Label(item.title, systemImage: item.icon)
                                .tag(item)
                        }
                    }
                }
            }
        }
        .listStyle(.sidebar)
        .navigationSplitViewColumnWidth(min: 180, ideal: 220, max: 280)
        .frame(minHeight: 300)
    }
}

// MARK: - Detail View

struct DetailView: View {
    let selectedItem: SidebarItem?

    var body: some View {
        Group {
            if let item = selectedItem {
                VStack {
                    Image(systemName: item.icon)
                        .font(.system(size: 64))
                        .foregroundStyle(.secondary)

                    Text(item.title)
                        .font(.title)

                    Text("Category: \(item.category.rawValue)")
                        .foregroundStyle(.secondary)
                }
            } else {
                ContentUnavailableView(
                    "No Selection",
                    systemImage: "sidebar.left",
                    description: Text("Select an item from the sidebar")
                )
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(.background)
    }
}

// MARK: - App Commands

struct AppCommands: Commands {
    var body: some Commands {
        CommandGroup(after: .newItem) {
            Button("New Folder") {
                // Create new folder
            }
            .keyboardShortcut("n", modifiers: [.command, .shift])
        }

        CommandMenu("View") {
            Button("Show Sidebar") {
                // Toggle sidebar
            }
            .keyboardShortcut("s", modifiers: [.command, .control])

            Divider()

            Button("Zoom In") {
                // Zoom in
            }
            .keyboardShortcut("+", modifiers: .command)

            Button("Zoom Out") {
                // Zoom out
            }
            .keyboardShortcut("-", modifiers: .command)
        }
    }
}

// MARK: - Settings View

struct SettingsView: View {
    var body: some View {
        TabView {
            GeneralSettingsTab()
                .tabItem {
                    Label("General", systemImage: "gear")
                }

            AppearanceSettingsTab()
                .tabItem {
                    Label("Appearance", systemImage: "paintbrush")
                }

            AccountSettingsTab()
                .tabItem {
                    Label("Account", systemImage: "person.crop.circle")
                }
        }
        .frame(width: 500, height: 350)
    }
}

struct GeneralSettingsTab: View {
    @AppStorage("launchAtLogin") private var launchAtLogin = false
    @AppStorage("checkForUpdates") private var checkForUpdates = true

    var body: some View {
        Form {
            Toggle("Launch at Login", isOn: $launchAtLogin)
            Toggle("Automatically Check for Updates", isOn: $checkForUpdates)
        }
        .formStyle(.grouped)
        .padding()
    }
}

struct AppearanceSettingsTab: View {
    @AppStorage("accentColorName") private var accentColorName = "blue"
    @AppStorage("sidebarIconSize") private var sidebarIconSize = 1.0

    var body: some View {
        Form {
            Picker("Accent Color", selection: $accentColorName) {
                Text("Blue").tag("blue")
                Text("Purple").tag("purple")
                Text("Pink").tag("pink")
                Text("Orange").tag("orange")
            }

            Slider(value: $sidebarIconSize, in: 0.5...2.0) {
                Text("Sidebar Icon Size")
            }
        }
        .formStyle(.grouped)
        .padding()
    }
}

struct AccountSettingsTab: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        Form {
            if let user = appState.currentUser {
                LabeledContent("Name", value: user.name)
                LabeledContent("Email", value: user.email)

                Button("Sign Out") {
                    appState.logout()
                }
            } else {
                Text("Not signed in")
                    .foregroundStyle(.secondary)

                Button("Sign In...") {
                    // Show sign in sheet
                }
            }
        }
        .formStyle(.grouped)
        .padding()
    }
}

// MARK: - Preview

#Preview("Main Window") {
    ContentView()
        .environment(AppState())
        .frame(width: 900, height: 600)
}

#Preview("Settings") {
    SettingsView()
        .environment(AppState())
}
