# Navigation Patterns Reference (macOS 14+)

Comprehensive guide to navigation patterns in macOS SwiftUI applications.

## NavigationSplitView

### Two-Column Layout

```swift
struct TwoColumnView: View {
    @State private var selectedItem: Item?

    var body: some View {
        NavigationSplitView {
            // Sidebar
            List(items, selection: $selectedItem) { item in
                Text(item.name)
                    .tag(item)
            }
            .navigationSplitViewColumnWidth(min: 180, ideal: 200, max: 250)
        } detail: {
            // Detail
            if let item = selectedItem {
                ItemDetailView(item: item)
            } else {
                ContentUnavailableView(
                    "No Selection",
                    systemImage: "doc",
                    description: Text("Select an item")
                )
            }
        }
    }
}
```

### Three-Column Layout

```swift
struct ThreeColumnView: View {
    @State private var selectedCategory: Category?
    @State private var selectedItem: Item?

    var body: some View {
        NavigationSplitView {
            // Sidebar (Column 1)
            List(categories, selection: $selectedCategory) { category in
                Label(category.name, systemImage: category.icon)
                    .tag(category)
            }
        } content: {
            // Content (Column 2)
            if let category = selectedCategory {
                List(category.items, selection: $selectedItem) { item in
                    Text(item.name)
                        .tag(item)
                }
            } else {
                ContentUnavailableView("Select a Category", systemImage: "folder")
            }
        } detail: {
            // Detail (Column 3)
            if let item = selectedItem {
                ItemDetailView(item: item)
            } else {
                ContentUnavailableView("Select an Item", systemImage: "doc")
            }
        }
    }
}
```

## Column Visibility

### Controlling Column Visibility

```swift
struct ContentView: View {
    @State private var columnVisibility: NavigationSplitViewVisibility = .all

    var body: some View {
        NavigationSplitView(columnVisibility: $columnVisibility) {
            SidebarView()
        } content: {
            ContentListView()
        } detail: {
            DetailView()
        }
    }
}
```

### Visibility Options

```swift
// Show all columns
columnVisibility = .all

// Show content and detail (hide sidebar)
columnVisibility = .doubleColumn

// Show only detail
columnVisibility = .detailOnly

// Automatic based on available space
columnVisibility = .automatic
```

### Toggle Sidebar

```swift
struct ContentView: View {
    @State private var columnVisibility: NavigationSplitViewVisibility = .all

    var body: some View {
        NavigationSplitView(columnVisibility: $columnVisibility) {
            SidebarView()
        } detail: {
            DetailView()
                .toolbar {
                    ToolbarItem(placement: .navigation) {
                        Button {
                            withAnimation {
                                columnVisibility = columnVisibility == .all
                                    ? .detailOnly
                                    : .all
                            }
                        } label: {
                            Label("Sidebar", systemImage: "sidebar.left")
                        }
                    }
                }
        }
    }
}
```

## NavigationSplitView Styles

```swift
NavigationSplitView {
    SidebarView()
} detail: {
    DetailView()
}
// Balanced column widths
.navigationSplitViewStyle(.balanced)

// Prominent detail (sidebar is secondary)
.navigationSplitViewStyle(.prominentDetail)

// Automatic (default)
.navigationSplitViewStyle(.automatic)
```

## Column Width

### Setting Column Width

```swift
NavigationSplitView {
    SidebarView()
        .navigationSplitViewColumnWidth(200)
} content: {
    ContentListView()
        .navigationSplitViewColumnWidth(min: 200, ideal: 300, max: 400)
} detail: {
    DetailView()
}
```

## NavigationStack

For hierarchical navigation within a column:

```swift
struct SidebarView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List {
                NavigationLink("Item 1", value: Item.one)
                NavigationLink("Item 2", value: Item.two)
            }
            .navigationDestination(for: Item.self) { item in
                ItemView(item: item)
            }
        }
    }
}
```

### Programmatic Navigation

```swift
@Observable
class Router {
    var path = NavigationPath()

    func navigate(to item: Item) {
        path.append(item)
    }

    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }

    func popToRoot() {
        path.removeLast(path.count)
    }
}

struct ContentView: View {
    @State private var router = Router()

    var body: some View {
        NavigationStack(path: $router.path) {
            HomeView()
                .environment(router)
        }
    }
}
```

## Inspector

### Adding Inspector Panel

```swift
struct ContentView: View {
    @State private var showInspector = false
    @State private var selectedItem: Item?

    var body: some View {
        NavigationSplitView {
            SidebarView(selection: $selectedItem)
        } detail: {
            DetailView(item: selectedItem)
        }
        .inspector(isPresented: $showInspector) {
            InspectorView(item: selectedItem)
                .inspectorColumnWidth(min: 200, ideal: 280, max: 350)
        }
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button {
                    showInspector.toggle()
                } label: {
                    Label("Inspector", systemImage: "info.circle")
                }
            }
        }
    }
}
```

## Sidebar Patterns

### Grouped Sidebar

```swift
struct SidebarView: View {
    @Binding var selection: Item.ID?

    var body: some View {
        List(selection: $selection) {
            Section("Favorites") {
                Label("All", systemImage: "tray.full")
                    .tag(Item.ID.all)
                Label("Recent", systemImage: "clock")
                    .tag(Item.ID.recent)
            }

            Section("Library") {
                ForEach(libraryItems) { item in
                    Label(item.name, systemImage: item.icon)
                        .tag(item.id)
                }
            }

            Section("Smart Folders") {
                ForEach(smartFolders) { folder in
                    Label(folder.name, systemImage: "folder.badge.gearshape")
                        .tag(folder.id)
                }
            }
        }
        .listStyle(.sidebar)
    }
}
```

### Sidebar with Badges

```swift
List {
    Label {
        HStack {
            Text("Inbox")
            Spacer()
            Text("12")
                .foregroundStyle(.secondary)
                .font(.caption)
        }
    } icon: {
        Image(systemName: "tray")
    }
}
```

### Collapsible Sections

```swift
struct SidebarView: View {
    @State private var expandedSections: Set<String> = ["favorites"]

    var body: some View {
        List {
            DisclosureGroup(
                isExpanded: Binding(
                    get: { expandedSections.contains("favorites") },
                    set: { isExpanded in
                        if isExpanded {
                            expandedSections.insert("favorites")
                        } else {
                            expandedSections.remove("favorites")
                        }
                    }
                )
            ) {
                // Items
            } label: {
                Text("Favorites")
            }
        }
    }
}
```

## Table for Lists

### Basic Table

```swift
struct ItemListView: View {
    let items: [Item]
    @State private var selection: Set<Item.ID> = []
    @State private var sortOrder = [KeyPathComparator(\Item.name)]

    var body: some View {
        Table(items, selection: $selection, sortOrder: $sortOrder) {
            TableColumn("Name", value: \.name)
                .width(min: 100, ideal: 150)

            TableColumn("Type", value: \.type.rawValue)
                .width(80)

            TableColumn("Size") { item in
                Text(item.formattedSize)
            }
            .width(60)

            TableColumn("Date", value: \.date) { item in
                Text(item.date.formatted())
            }
        }
        .onChange(of: sortOrder) { _, newOrder in
            items.sort(using: newOrder)
        }
    }
}
```

### Table with Context Menu

```swift
Table(items, selection: $selection) {
    // Columns...
}
.contextMenu(forSelectionType: Item.ID.self) { items in
    Button("Open") {
        // Open selected items
    }
    Button("Delete", role: .destructive) {
        // Delete selected items
    }
} primaryAction: { items in
    // Double-click action
    openItems(items)
}
```

## Navigation Title

```swift
struct ContentView: View {
    var body: some View {
        NavigationSplitView {
            SidebarView()
                .navigationTitle("Library")
        } detail: {
            DetailView()
                .navigationTitle("Details")
                .navigationSubtitle("3 items selected")
        }
    }
}
```

## Toolbar Integration

```swift
struct ContentView: View {
    var body: some View {
        NavigationSplitView {
            SidebarView()
                .toolbar {
                    ToolbarItem {
                        Button("Add", systemImage: "plus") { }
                    }
                }
        } detail: {
            DetailView()
                .toolbar {
                    ToolbarItemGroup(placement: .primaryAction) {
                        Button("Share", systemImage: "square.and.arrow.up") { }
                        Button("Delete", systemImage: "trash") { }
                    }
                }
        }
    }
}
```

## Empty State

```swift
struct DetailView: View {
    let selectedItem: Item?

    var body: some View {
        Group {
            if let item = selectedItem {
                ItemContent(item: item)
            } else {
                ContentUnavailableView {
                    Label("No Selection", systemImage: "doc")
                } description: {
                    Text("Select an item from the sidebar to view its details.")
                } actions: {
                    Button("Create New") {
                        // Create new item
                    }
                }
            }
        }
    }
}
```

## Best Practices

1. **Use NavigationSplitView for macOS** - Better than NavigationStack for desktop apps
2. **Three columns for complex apps** - Source list, content, detail
3. **Two columns for simpler apps** - Sidebar and detail
4. **Persist selection state** - Use @SceneStorage for window-specific state
5. **Support keyboard navigation** - Lists should be keyboard navigable
6. **Provide empty states** - Use ContentUnavailableView
7. **Responsive column widths** - Set min/ideal/max for flexibility
8. **Consider column visibility** - Allow users to show/hide columns
