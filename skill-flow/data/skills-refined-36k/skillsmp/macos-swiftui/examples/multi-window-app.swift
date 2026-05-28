// Multi-Window macOS App (macOS 14+)
// Demonstrates multiple windows, openWindow, and window state management

import SwiftUI
import Observation

// MARK: - App Entry Point

@main
struct MultiWindowApp: App {
    @State private var appState = AppState()

    var body: some Scene {
        // Main window - can have multiple instances
        WindowGroup {
            MainWindowView()
                .environment(appState)
        }
        .defaultSize(width: 800, height: 600)
        .commands {
            WindowCommands(appState: appState)
        }

        // Inspector window - single instance
        Window("Inspector", id: "inspector") {
            InspectorWindowView()
                .environment(appState)
        }
        .defaultSize(width: 300, height: 500)
        .defaultPosition(.topTrailing)
        .windowResizability(.contentSize)

        // Activity Monitor window - value-based
        WindowGroup("Activity", for: Activity.ID.self) { $activityId in
            if let activityId {
                ActivityDetailView(activityId: activityId)
                    .environment(appState)
            }
        }
        .defaultSize(width: 400, height: 300)

        // Auxiliary window group with custom ID
        WindowGroup(id: "new-item") {
            NewItemWindowView()
                .environment(appState)
        }
        .defaultSize(width: 500, height: 400)
        .windowResizability(.contentMinSize)

        Settings {
            SettingsView()
        }
    }
}

// MARK: - App State

@Observable
class AppState {
    var items: [Item] = Item.sampleData
    var selectedItemId: Item.ID?
    var activities: [Activity] = Activity.sampleData
    var inspectorVisible = false

    var selectedItem: Item? {
        items.first { $0.id == selectedItemId }
    }

    func addItem(_ item: Item) {
        items.append(item)
    }

    func deleteItem(id: Item.ID) {
        items.removeAll { $0.id == id }
        if selectedItemId == id {
            selectedItemId = nil
        }
    }
}

// MARK: - Models

struct Item: Identifiable, Hashable {
    let id: UUID
    var name: String
    var description: String
    var createdAt: Date

    static let sampleData: [Item] = [
        Item(id: UUID(), name: "Project Alpha", description: "Main project", createdAt: .now),
        Item(id: UUID(), name: "Project Beta", description: "Secondary project", createdAt: .now.addingTimeInterval(-86400)),
        Item(id: UUID(), name: "Project Gamma", description: "Research project", createdAt: .now.addingTimeInterval(-172800)),
    ]
}

struct Activity: Identifiable, Hashable {
    let id: UUID
    var name: String
    var progress: Double
    var status: Status

    enum Status: String, CaseIterable {
        case pending = "Pending"
        case running = "Running"
        case completed = "Completed"
        case failed = "Failed"
    }

    static let sampleData: [Activity] = [
        Activity(id: UUID(), name: "Build", progress: 0.75, status: .running),
        Activity(id: UUID(), name: "Test", progress: 1.0, status: .completed),
        Activity(id: UUID(), name: "Deploy", progress: 0.0, status: .pending),
    ]
}

// MARK: - Main Window View

struct MainWindowView: View {
    @Environment(AppState.self) private var appState
    @Environment(\.openWindow) private var openWindow

    var body: some View {
        @Bindable var state = appState

        NavigationSplitView {
            List(appState.items, selection: $state.selectedItemId) { item in
                ItemRow(item: item)
                    .tag(item.id)
            }
            .navigationSplitViewColumnWidth(min: 200, ideal: 250)
            .toolbar {
                ToolbarItem {
                    Button {
                        openWindow(id: "new-item")
                    } label: {
                        Label("Add", systemImage: "plus")
                    }
                }
            }
        } detail: {
            if let item = appState.selectedItem {
                ItemDetailView(item: item)
            } else {
                ContentUnavailableView(
                    "No Selection",
                    systemImage: "doc",
                    description: Text("Select an item from the sidebar")
                )
            }
        }
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button {
                    openWindow(id: "inspector")
                } label: {
                    Label("Inspector", systemImage: "info.circle")
                }
            }
        }
    }
}

struct ItemRow: View {
    let item: Item

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(item.name)
                .font(.headline)

            Text(item.description)
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .padding(.vertical, 4)
    }
}

struct ItemDetailView: View {
    let item: Item

    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "folder.fill")
                .font(.system(size: 64))
                .foregroundStyle(.blue)

            Text(item.name)
                .font(.title)

            Text(item.description)
                .foregroundStyle(.secondary)

            Text("Created: \(item.createdAt.formatted())")
                .font(.caption)
                .foregroundStyle(.tertiary)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .navigationTitle(item.name)
    }
}

// MARK: - Inspector Window

struct InspectorWindowView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Inspector")
                .font(.title2)
                .fontWeight(.semibold)

            Divider()

            if let item = appState.selectedItem {
                Form {
                    LabeledContent("Name", value: item.name)
                    LabeledContent("Description", value: item.description)
                    LabeledContent("Created", value: item.createdAt.formatted())
                    LabeledContent("ID", value: item.id.uuidString)
                }
            } else {
                ContentUnavailableView(
                    "No Selection",
                    systemImage: "info.circle",
                    description: Text("Select an item to inspect")
                )
            }

            Spacer()
        }
        .padding()
        .frame(minWidth: 250, minHeight: 300)
    }
}

// MARK: - Activity Detail Window

struct ActivityDetailView: View {
    @Environment(AppState.self) private var appState
    let activityId: Activity.ID

    private var activity: Activity? {
        appState.activities.first { $0.id == activityId }
    }

    var body: some View {
        VStack(spacing: 20) {
            if let activity {
                Image(systemName: statusIcon(for: activity.status))
                    .font(.system(size: 48))
                    .foregroundStyle(statusColor(for: activity.status))

                Text(activity.name)
                    .font(.title)

                ProgressView(value: activity.progress) {
                    Text("\(Int(activity.progress * 100))%")
                }
                .progressViewStyle(.linear)
                .frame(maxWidth: 200)

                Text(activity.status.rawValue)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)
                    .background(statusColor(for: activity.status).opacity(0.2))
                    .clipShape(Capsule())
            } else {
                Text("Activity not found")
                    .foregroundStyle(.secondary)
            }
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    private func statusIcon(for status: Activity.Status) -> String {
        switch status {
        case .pending: return "clock"
        case .running: return "play.circle"
        case .completed: return "checkmark.circle"
        case .failed: return "xmark.circle"
        }
    }

    private func statusColor(for status: Activity.Status) -> Color {
        switch status {
        case .pending: return .gray
        case .running: return .blue
        case .completed: return .green
        case .failed: return .red
        }
    }
}

// MARK: - New Item Window

struct NewItemWindowView: View {
    @Environment(AppState.self) private var appState
    @Environment(\.dismiss) private var dismiss

    @State private var name = ""
    @State private var description = ""

    var body: some View {
        VStack(spacing: 20) {
            Text("New Item")
                .font(.title)

            Form {
                TextField("Name", text: $name)
                TextField("Description", text: $description, axis: .vertical)
                    .lineLimit(3...6)
            }
            .formStyle(.grouped)

            HStack {
                Button("Cancel") {
                    dismiss()
                }
                .keyboardShortcut(.escape)

                Spacer()

                Button("Create") {
                    let item = Item(
                        id: UUID(),
                        name: name,
                        description: description,
                        createdAt: .now
                    )
                    appState.addItem(item)
                    dismiss()
                }
                .keyboardShortcut(.return)
                .disabled(name.isEmpty)
            }
            .padding()
        }
        .padding()
        .frame(minWidth: 400, minHeight: 300)
    }
}

// MARK: - Window Commands

struct WindowCommands: Commands {
    let appState: AppState
    @Environment(\.openWindow) private var openWindow

    var body: some Commands {
        CommandGroup(after: .newItem) {
            Button("New Item...") {
                openWindow(id: "new-item")
            }
            .keyboardShortcut("n", modifiers: [.command, .shift])
        }

        CommandMenu("Window") {
            Button("Show Inspector") {
                openWindow(id: "inspector")
            }
            .keyboardShortcut("i", modifiers: [.command, .option])

            Divider()

            ForEach(appState.activities) { activity in
                Button("Show \(activity.name)") {
                    openWindow(value: activity.id)
                }
            }
        }
    }
}

// MARK: - Settings View

struct SettingsView: View {
    @AppStorage("defaultWindowPosition") private var defaultWindowPosition = "center"

    var body: some View {
        Form {
            Picker("Default Window Position", selection: $defaultWindowPosition) {
                Text("Center").tag("center")
                Text("Top Left").tag("topLeading")
                Text("Top Right").tag("topTrailing")
            }
        }
        .formStyle(.grouped)
        .padding()
        .frame(width: 400, height: 200)
    }
}

// MARK: - Preview

#Preview("Main Window") {
    MainWindowView()
        .environment(AppState())
        .frame(width: 800, height: 600)
}

#Preview("Inspector") {
    InspectorWindowView()
        .environment(AppState())
        .frame(width: 300, height: 400)
}

#Preview("New Item") {
    NewItemWindowView()
        .environment(AppState())
}
