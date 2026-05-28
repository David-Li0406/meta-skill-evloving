// NavigationSplitView Example (macOS 14+)
// Demonstrates 2/3 column layouts, sidebar patterns, and Inspector

import SwiftUI
import Observation

// MARK: - App Entry Point

@main
struct NavigationApp: App {
    @State private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(appState)
        }
        .defaultSize(width: 1000, height: 700)
        .commands {
            NavigationCommands(appState: appState)
        }
    }
}

// MARK: - App State

@Observable
class AppState {
    var categories: [Category] = Category.sampleData
    var selectedCategoryId: Category.ID?
    var selectedItemId: Item.ID?
    var showInspector = false
    var sidebarVisibility: NavigationSplitViewVisibility = .all

    var selectedCategory: Category? {
        categories.first { $0.id == selectedCategoryId }
    }

    var selectedItem: Item? {
        selectedCategory?.items.first { $0.id == selectedItemId }
    }
}

// MARK: - Models

struct Category: Identifiable, Hashable {
    let id: UUID
    var name: String
    var icon: String
    var items: [Item]

    static let sampleData: [Category] = [
        Category(
            id: UUID(),
            name: "Documents",
            icon: "doc.fill",
            items: [
                Item(id: UUID(), name: "Project Proposal", type: .document, size: 245_000, modifiedAt: .now),
                Item(id: UUID(), name: "Meeting Notes", type: .document, size: 12_000, modifiedAt: .now.addingTimeInterval(-3600)),
                Item(id: UUID(), name: "Requirements", type: .document, size: 78_000, modifiedAt: .now.addingTimeInterval(-7200)),
            ]
        ),
        Category(
            id: UUID(),
            name: "Images",
            icon: "photo.fill",
            items: [
                Item(id: UUID(), name: "Screenshot 1", type: .image, size: 1_200_000, modifiedAt: .now),
                Item(id: UUID(), name: "Logo", type: .image, size: 450_000, modifiedAt: .now.addingTimeInterval(-86400)),
            ]
        ),
        Category(
            id: UUID(),
            name: "Archives",
            icon: "archivebox.fill",
            items: [
                Item(id: UUID(), name: "Backup 2024", type: .archive, size: 52_000_000, modifiedAt: .now.addingTimeInterval(-604800)),
            ]
        ),
    ]
}

struct Item: Identifiable, Hashable {
    let id: UUID
    var name: String
    var type: ItemType
    var size: Int
    var modifiedAt: Date

    enum ItemType: String {
        case document = "Document"
        case image = "Image"
        case video = "Video"
        case archive = "Archive"

        var icon: String {
            switch self {
            case .document: return "doc"
            case .image: return "photo"
            case .video: return "video"
            case .archive: return "archivebox"
            }
        }
    }

    var formattedSize: String {
        ByteCountFormatter.string(fromByteCount: Int64(size), countStyle: .file)
    }
}

// MARK: - Content View (Three Column)

struct ContentView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        @Bindable var state = appState

        NavigationSplitView(columnVisibility: $state.sidebarVisibility) {
            // Sidebar (Column 1)
            SidebarView()
        } content: {
            // Content (Column 2)
            ContentListView()
        } detail: {
            // Detail (Column 3)
            DetailView()
        }
        .navigationSplitViewStyle(.balanced)
        .inspector(isPresented: $state.showInspector) {
            InspectorView()
                .inspectorColumnWidth(min: 200, ideal: 280, max: 350)
        }
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button {
                    appState.showInspector.toggle()
                } label: {
                    Label("Inspector", systemImage: "info.circle")
                }
            }
        }
    }
}

// MARK: - Sidebar View

struct SidebarView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        @Bindable var state = appState

        List(selection: $state.selectedCategoryId) {
            Section("Collections") {
                ForEach(appState.categories) { category in
                    Label {
                        HStack {
                            Text(category.name)
                            Spacer()
                            Text("\(category.items.count)")
                                .foregroundStyle(.secondary)
                                .font(.caption)
                        }
                    } icon: {
                        Image(systemName: category.icon)
                    }
                    .tag(category.id)
                }
            }

            Section("Smart Folders") {
                Label("Recent", systemImage: "clock")
                Label("Large Files", systemImage: "externaldrive")
                Label("Shared", systemImage: "person.2")
            }
        }
        .listStyle(.sidebar)
        .navigationSplitViewColumnWidth(min: 180, ideal: 220, max: 300)
        .toolbar {
            ToolbarItem {
                Button {
                    // Add category
                } label: {
                    Label("Add", systemImage: "plus")
                }
            }
        }
    }
}

// MARK: - Content List View

struct ContentListView: View {
    @Environment(AppState.self) private var appState
    @State private var sortOrder = [KeyPathComparator(\Item.name)]

    var body: some View {
        @Bindable var state = appState

        Group {
            if let category = appState.selectedCategory {
                Table(category.items, selection: $state.selectedItemId, sortOrder: $sortOrder) {
                    TableColumn("Name", value: \.name) { item in
                        Label(item.name, systemImage: item.type.icon)
                    }
                    .width(min: 150, ideal: 200)

                    TableColumn("Type", value: \.type.rawValue)
                        .width(80)

                    TableColumn("Size") { item in
                        Text(item.formattedSize)
                    }
                    .width(80)

                    TableColumn("Modified", value: \.modifiedAt) { item in
                        Text(item.modifiedAt.formatted(date: .abbreviated, time: .shortened))
                    }
                    .width(min: 120)
                }
                .onChange(of: sortOrder) { _, newOrder in
                    // Sort items
                }
                .navigationTitle(category.name)
            } else {
                ContentUnavailableView(
                    "No Collection Selected",
                    systemImage: "folder",
                    description: Text("Select a collection from the sidebar")
                )
            }
        }
        .navigationSplitViewColumnWidth(min: 250, ideal: 350)
    }
}

// MARK: - Detail View

struct DetailView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        Group {
            if let item = appState.selectedItem {
                ItemDetailContent(item: item)
            } else {
                ContentUnavailableView(
                    "No Item Selected",
                    systemImage: "doc",
                    description: Text("Select an item to view its details")
                )
            }
        }
        .frame(minWidth: 300)
    }
}

struct ItemDetailContent: View {
    let item: Item

    var body: some View {
        ScrollView {
            VStack(spacing: 24) {
                // Icon
                Image(systemName: item.type.icon)
                    .font(.system(size: 72))
                    .foregroundStyle(.blue)
                    .frame(width: 120, height: 120)
                    .background(.blue.opacity(0.1))
                    .clipShape(RoundedRectangle(cornerRadius: 16))

                // Name
                Text(item.name)
                    .font(.title)
                    .fontWeight(.semibold)

                // Info grid
                Grid(alignment: .leading, horizontalSpacing: 24, verticalSpacing: 12) {
                    GridRow {
                        Text("Type")
                            .foregroundStyle(.secondary)
                        Text(item.type.rawValue)
                    }

                    GridRow {
                        Text("Size")
                            .foregroundStyle(.secondary)
                        Text(item.formattedSize)
                    }

                    GridRow {
                        Text("Modified")
                            .foregroundStyle(.secondary)
                        Text(item.modifiedAt.formatted())
                    }
                }
                .padding()
                .background(.background)
                .clipShape(RoundedRectangle(cornerRadius: 8))

                Spacer()
            }
            .padding()
        }
        .navigationTitle(item.name)
    }
}

// MARK: - Inspector View

struct InspectorView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        Form {
            if let item = appState.selectedItem {
                Section("File Info") {
                    LabeledContent("Name", value: item.name)
                    LabeledContent("Type", value: item.type.rawValue)
                    LabeledContent("Size", value: item.formattedSize)
                }

                Section("Dates") {
                    LabeledContent("Modified", value: item.modifiedAt.formatted())
                }

                Section("Actions") {
                    Button("Open") {
                        // Open item
                    }
                    Button("Share...") {
                        // Share item
                    }
                    Button("Move to Trash", role: .destructive) {
                        // Delete item
                    }
                }
            } else {
                Text("No item selected")
                    .foregroundStyle(.secondary)
            }
        }
        .formStyle(.grouped)
    }
}

// MARK: - Navigation Commands

struct NavigationCommands: Commands {
    let appState: AppState

    var body: some Commands {
        CommandGroup(after: .sidebar) {
            Divider()

            Button("Show Inspector") {
                appState.showInspector.toggle()
            }
            .keyboardShortcut("i", modifiers: [.command, .option])

            Divider()

            Button("Show All Columns") {
                appState.sidebarVisibility = .all
            }
            .keyboardShortcut("1", modifiers: [.command, .control])

            Button("Hide Sidebar") {
                appState.sidebarVisibility = .detailOnly
            }
            .keyboardShortcut("2", modifiers: [.command, .control])
        }
    }
}

// MARK: - Two Column Layout Example

struct TwoColumnView: View {
    @State private var selectedId: UUID?

    let items = [
        (UUID(), "Item 1"),
        (UUID(), "Item 2"),
        (UUID(), "Item 3"),
    ]

    var body: some View {
        NavigationSplitView {
            List(items, id: \.0, selection: $selectedId) { item in
                Text(item.1)
                    .tag(item.0)
            }
            .navigationSplitViewColumnWidth(200)
        } detail: {
            if let id = selectedId,
               let item = items.first(where: { $0.0 == id }) {
                Text("Selected: \(item.1)")
            } else {
                Text("Select an item")
            }
        }
    }
}

// MARK: - Collapsible Sidebar Example

struct CollapsibleSidebarView: View {
    @State private var columnVisibility: NavigationSplitViewVisibility = .all

    var body: some View {
        NavigationSplitView(columnVisibility: $columnVisibility) {
            List {
                Text("Sidebar Item 1")
                Text("Sidebar Item 2")
            }
            .navigationSplitViewColumnWidth(200)
        } detail: {
            VStack {
                Text("Main Content")

                Button("Toggle Sidebar") {
                    withAnimation {
                        columnVisibility = columnVisibility == .all ? .detailOnly : .all
                    }
                }
            }
        }
        .navigationSplitViewStyle(.prominentDetail)
    }
}

// MARK: - Preview

#Preview("Three Column") {
    ContentView()
        .environment(AppState())
        .frame(width: 1000, height: 700)
}

#Preview("Two Column") {
    TwoColumnView()
        .frame(width: 600, height: 400)
}

#Preview("Collapsible Sidebar") {
    CollapsibleSidebarView()
        .frame(width: 600, height: 400)
}
