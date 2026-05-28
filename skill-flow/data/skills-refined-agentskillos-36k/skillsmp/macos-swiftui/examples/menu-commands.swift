// Menu and Commands Example (macOS 14+)
// Demonstrates Commands, KeyboardShortcut, and @FocusedValue

import SwiftUI
import Observation

// MARK: - App Entry Point

@main
struct MenuCommandsApp: App {
    @State private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(appState)
        }
        .commands {
            // Replace standard commands
            CommandGroup(replacing: .newItem) {
                NewItemCommands(appState: appState)
            }

            // Add after existing groups
            CommandGroup(after: .pasteboard) {
                PasteSpecialCommands()
            }

            // Custom command menus
            EditModeCommands(appState: appState)
            ViewCommands(appState: appState)
            ItemCommands()
        }
    }
}

// MARK: - App State

@Observable
class AppState {
    var items: [Item] = Item.sampleData
    var selectedItemIds: Set<Item.ID> = []
    var viewMode: ViewMode = .grid
    var sortOrder: SortOrder = .name
    var isEditing = false
    var showSidebar = true

    enum ViewMode: String, CaseIterable {
        case list = "List"
        case grid = "Grid"
        case columns = "Columns"

        var icon: String {
            switch self {
            case .list: return "list.bullet"
            case .grid: return "square.grid.2x2"
            case .columns: return "rectangle.split.3x1"
            }
        }
    }

    enum SortOrder: String, CaseIterable {
        case name = "Name"
        case date = "Date"
        case size = "Size"
        case kind = "Kind"
    }

    var selectedItems: [Item] {
        items.filter { selectedItemIds.contains($0.id) }
    }

    func duplicateSelectedItems() {
        let duplicates = selectedItems.map { item in
            Item(id: UUID(), name: "\(item.name) copy", kind: item.kind, createdAt: .now)
        }
        items.append(contentsOf: duplicates)
    }

    func deleteSelectedItems() {
        items.removeAll { selectedItemIds.contains($0.id) }
        selectedItemIds.removeAll()
    }
}

// MARK: - Models

struct Item: Identifiable, Hashable {
    let id: UUID
    var name: String
    var kind: Kind
    var createdAt: Date

    enum Kind: String, CaseIterable {
        case document = "Document"
        case folder = "Folder"
        case image = "Image"
        case video = "Video"

        var icon: String {
            switch self {
            case .document: return "doc"
            case .folder: return "folder"
            case .image: return "photo"
            case .video: return "video"
            }
        }
    }

    static let sampleData: [Item] = [
        Item(id: UUID(), name: "Project Plan", kind: .document, createdAt: .now),
        Item(id: UUID(), name: "Assets", kind: .folder, createdAt: .now),
        Item(id: UUID(), name: "Screenshot", kind: .image, createdAt: .now),
        Item(id: UUID(), name: "Demo Video", kind: .video, createdAt: .now),
    ]
}

// MARK: - New Item Commands

struct NewItemCommands: View {
    let appState: AppState
    @Environment(\.openWindow) private var openWindow

    var body: some View {
        Button("New Document") {
            appState.items.append(Item(id: UUID(), name: "Untitled", kind: .document, createdAt: .now))
        }
        .keyboardShortcut("n", modifiers: .command)

        Button("New Folder") {
            appState.items.append(Item(id: UUID(), name: "New Folder", kind: .folder, createdAt: .now))
        }
        .keyboardShortcut("n", modifiers: [.command, .shift])

        Divider()

        Menu("New From Template") {
            Button("Blank Document") { }
            Button("Report") { }
            Button("Presentation") { }
        }
    }
}

// MARK: - Paste Special Commands

struct PasteSpecialCommands: View {
    var body: some View {
        Divider()

        Button("Paste and Match Style") {
            // Paste with style matching
        }
        .keyboardShortcut("v", modifiers: [.command, .option, .shift])

        Button("Paste as Plain Text") {
            // Paste as plain text
        }
    }
}

// MARK: - Edit Mode Commands

struct EditModeCommands: Commands {
    let appState: AppState

    var body: some Commands {
        CommandGroup(after: .undoRedo) {
            Divider()

            Toggle("Edit Mode", isOn: Binding(
                get: { appState.isEditing },
                set: { appState.isEditing = $0 }
            ))
            .keyboardShortcut("e", modifiers: .command)
        }
    }
}

// MARK: - View Commands

struct ViewCommands: Commands {
    let appState: AppState

    var body: some Commands {
        CommandMenu("View") {
            // View mode picker
            Picker("View Mode", selection: Binding(
                get: { appState.viewMode },
                set: { appState.viewMode = $0 }
            )) {
                ForEach(AppState.ViewMode.allCases, id: \.self) { mode in
                    Label(mode.rawValue, systemImage: mode.icon)
                        .tag(mode)
                }
            }
            .pickerStyle(.inline)

            Divider()

            // Sort order
            Menu("Sort By") {
                Picker("Sort Order", selection: Binding(
                    get: { appState.sortOrder },
                    set: { appState.sortOrder = $0 }
                )) {
                    ForEach(AppState.SortOrder.allCases, id: \.self) { order in
                        Text(order.rawValue).tag(order)
                    }
                }
            }

            Divider()

            Toggle("Show Sidebar", isOn: Binding(
                get: { appState.showSidebar },
                set: { appState.showSidebar = $0 }
            ))
            .keyboardShortcut("s", modifiers: [.command, .control])

            Divider()

            Button("Enter Full Screen") {
                // Toggle full screen
            }
            .keyboardShortcut("f", modifiers: [.command, .control])
        }
    }
}

// MARK: - Item Commands (Using FocusedValue)

struct ItemCommands: Commands {
    @FocusedValue(\.selectedItems) private var selectedItems

    var body: some Commands {
        CommandMenu("Item") {
            Button("Get Info") {
                // Show info
            }
            .keyboardShortcut("i", modifiers: .command)
            .disabled(selectedItems?.isEmpty ?? true)

            Button("Rename") {
                // Rename item
            }
            .keyboardShortcut(.return, modifiers: [])
            .disabled((selectedItems?.count ?? 0) != 1)

            Divider()

            Button("Duplicate") {
                // Duplicate - handled by FocusedBinding
            }
            .keyboardShortcut("d", modifiers: .command)
            .disabled(selectedItems?.isEmpty ?? true)

            Button("Move to Trash") {
                // Move to trash - handled by FocusedBinding
            }
            .keyboardShortcut(.delete, modifiers: .command)
            .disabled(selectedItems?.isEmpty ?? true)

            Divider()

            Button("Share...") {
                // Share
            }
            .disabled(selectedItems?.isEmpty ?? true)

            Menu("Move To") {
                Button("Desktop") { }
                Button("Documents") { }
                Button("Downloads") { }
                Divider()
                Button("Choose...") { }
            }
            .disabled(selectedItems?.isEmpty ?? true)
        }
    }
}

// MARK: - Focused Values

struct SelectedItemsKey: FocusedValueKey {
    typealias Value = [Item]
}

struct DuplicateActionKey: FocusedValueKey {
    typealias Value = () -> Void
}

struct DeleteActionKey: FocusedValueKey {
    typealias Value = () -> Void
}

extension FocusedValues {
    var selectedItems: [Item]? {
        get { self[SelectedItemsKey.self] }
        set { self[SelectedItemsKey.self] = newValue }
    }

    var duplicateAction: (() -> Void)? {
        get { self[DuplicateActionKey.self] }
        set { self[DuplicateActionKey.self] = newValue }
    }

    var deleteAction: (() -> Void)? {
        get { self[DeleteActionKey.self] }
        set { self[DeleteActionKey.self] = newValue }
    }
}

// MARK: - Content View

struct ContentView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        @Bindable var state = appState

        NavigationSplitView {
            if appState.showSidebar {
                SidebarView()
            }
        } detail: {
            ItemGridView()
        }
        .focusedSceneValue(\.selectedItems, appState.selectedItems)
        .focusedSceneValue(\.duplicateAction) {
            appState.duplicateSelectedItems()
        }
        .focusedSceneValue(\.deleteAction) {
            appState.deleteSelectedItems()
        }
    }
}

// MARK: - Sidebar View

struct SidebarView: View {
    var body: some View {
        List {
            Section("Favorites") {
                Label("All Items", systemImage: "square.grid.2x2")
                Label("Recent", systemImage: "clock")
                Label("Shared", systemImage: "person.2")
            }

            Section("Folders") {
                Label("Documents", systemImage: "folder")
                Label("Images", systemImage: "photo.on.rectangle")
                Label("Videos", systemImage: "video")
            }
        }
        .listStyle(.sidebar)
        .navigationSplitViewColumnWidth(min: 180, ideal: 200)
    }
}

// MARK: - Item Grid View

struct ItemGridView: View {
    @Environment(AppState.self) private var appState

    private let columns = [
        GridItem(.adaptive(minimum: 120, maximum: 150), spacing: 16)
    ]

    var body: some View {
        @Bindable var state = appState

        ScrollView {
            LazyVGrid(columns: columns, spacing: 16) {
                ForEach(appState.items) { item in
                    ItemCell(
                        item: item,
                        isSelected: appState.selectedItemIds.contains(item.id),
                        isEditing: appState.isEditing
                    )
                    .onTapGesture {
                        if NSEvent.modifierFlags.contains(.command) {
                            if appState.selectedItemIds.contains(item.id) {
                                appState.selectedItemIds.remove(item.id)
                            } else {
                                appState.selectedItemIds.insert(item.id)
                            }
                        } else {
                            appState.selectedItemIds = [item.id]
                        }
                    }
                }
            }
            .padding()
        }
        .toolbar {
            ToolbarItem(placement: .automatic) {
                Picker("View", selection: $state.viewMode) {
                    ForEach(AppState.ViewMode.allCases, id: \.self) { mode in
                        Label(mode.rawValue, systemImage: mode.icon)
                    }
                }
                .pickerStyle(.segmented)
            }
        }
    }
}

// MARK: - Item Cell

struct ItemCell: View {
    let item: Item
    let isSelected: Bool
    let isEditing: Bool

    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: item.kind.icon)
                .font(.system(size: 48))
                .foregroundStyle(isSelected ? .white : .blue)
                .frame(width: 80, height: 80)
                .background(isSelected ? Color.accentColor : Color.clear)
                .clipShape(RoundedRectangle(cornerRadius: 8))

            Text(item.name)
                .lineLimit(2)
                .multilineTextAlignment(.center)
                .font(.caption)
        }
        .padding(8)
        .background(isSelected ? Color.accentColor.opacity(0.2) : Color.clear)
        .clipShape(RoundedRectangle(cornerRadius: 8))
        .overlay {
            if isEditing {
                RoundedRectangle(cornerRadius: 8)
                    .stroke(Color.accentColor, lineWidth: 2)
            }
        }
    }
}

// MARK: - Preview

#Preview {
    ContentView()
        .environment(AppState())
        .frame(width: 800, height: 600)
}
