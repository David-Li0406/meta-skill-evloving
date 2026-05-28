---
name: macos-swiftui
description: |
  This skill should be used when the user asks to "build macOS app",
  "create macOS window", "implement NavigationSplitView", "add menu commands",
  "create Settings window", "implement document-based app", "use WindowGroup",
  "add toolbar", "implement sidebar", "multi-window app",
  "macOS アプリを作成", "macOS で実装", "メニューを追加",
  "設定画面を作成", "マルチウィンドウ", "サイドバーを実装",
  "ドキュメントベースアプリ", "ツールバーを追加".
  Provides macOS 14+ (Sonoma) development guidance with SwiftUI,
  window management, menu integration, and macOS-specific patterns.
version: 1.0.0
---

# macOS SwiftUI Development

Comprehensive macOS app development skill for macOS 14+ (Sonoma) with SwiftUI and modern Swift practices.

## Overview

**Target Platform**: macOS 14+ (Sonoma) / Swift 5.9+

**Core Technologies**:
- UI Framework: SwiftUI (primary), AppKit (when needed)
- Window Management: WindowGroup, Window, MenuBarExtra
- Navigation: NavigationSplitView, NavigationStack
- Data: SwiftData (recommended), Core Data
- Document: FileDocument, DocumentGroup

## Quick Start

### New Project Setup

To create a new macOS project:

1. Open Xcode and select "Create New Project"
2. Choose "App" template under macOS
3. Select SwiftUI for Interface
4. Set minimum deployment target to macOS 14.0
5. Enable Swift strict concurrency checking in Build Settings

### Basic App Structure

```swift
import SwiftUI

@main
struct MyMacApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .commands {
            // Custom menu commands
        }

        Settings {
            SettingsView()
        }
    }
}
```

### Existing Project Analysis

To analyze an existing project structure:

```bash
bash scripts/macos-project-analyzer.sh /path/to/project
```

## Window Management

### WindowGroup (Multi-Instance Windows)

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .defaultSize(width: 800, height: 600)
        .defaultPosition(.center)
    }
}
```

### Window (Single Instance)

```swift
@main
struct MyApp: App {
    var body: some Scene {
        Window("Inspector", id: "inspector") {
            InspectorView()
        }
        .defaultSize(width: 300, height: 400)
        .windowResizability(.contentSize)
    }
}
```

### Opening Windows Programmatically

```swift
struct ContentView: View {
    @Environment(\.openWindow) private var openWindow

    var body: some View {
        Button("Open Inspector") {
            openWindow(id: "inspector")
        }
    }
}
```

For detailed window patterns, see [references/window-management.md](references/window-management.md).

## Menu Bar Integration

### Custom Commands

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .commands {
            CommandGroup(after: .newItem) {
                Button("New Document") {
                    // Action
                }
                .keyboardShortcut("n", modifiers: [.command, .shift])
            }

            CommandMenu("Custom") {
                Button("Action 1") { }
                    .keyboardShortcut("1", modifiers: .command)
                Divider()
                Button("Action 2") { }
            }
        }
    }
}
```

### FocusedValue for Window-Specific State

```swift
struct FocusedDocumentKey: FocusedValueKey {
    typealias Value = Binding<Document>
}

extension FocusedValues {
    var document: Binding<Document>? {
        get { self[FocusedDocumentKey.self] }
        set { self[FocusedDocumentKey.self] = newValue }
    }
}

// In View
.focusedSceneValue(\.document, $document)
```

For detailed menu patterns, see [references/menu-commands.md](references/menu-commands.md).

## Navigation Patterns

### NavigationSplitView (Two/Three Column)

```swift
struct ContentView: View {
    @State private var selectedCategory: Category?
    @State private var selectedItem: Item?

    var body: some View {
        NavigationSplitView {
            // Sidebar
            List(categories, selection: $selectedCategory) { category in
                Label(category.name, systemImage: category.icon)
            }
            .navigationSplitViewColumnWidth(min: 180, ideal: 200, max: 250)
        } content: {
            // Content
            if let category = selectedCategory {
                List(category.items, selection: $selectedItem) { item in
                    Text(item.name)
                }
            }
        } detail: {
            // Detail
            if let item = selectedItem {
                ItemDetailView(item: item)
            } else {
                ContentUnavailableView("Select an Item", systemImage: "doc")
            }
        }
        .navigationSplitViewStyle(.balanced)
    }
}
```

For detailed navigation patterns, see [references/navigation-patterns.md](references/navigation-patterns.md).

## Settings/Preferences

### Settings Scene

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

struct SettingsView: View {
    var body: some View {
        TabView {
            GeneralSettingsView()
                .tabItem {
                    Label("General", systemImage: "gear")
                }

            AdvancedSettingsView()
                .tabItem {
                    Label("Advanced", systemImage: "gearshape.2")
                }
        }
        .frame(width: 450, height: 300)
    }
}
```

### @AppStorage for User Defaults

```swift
struct GeneralSettingsView: View {
    @AppStorage("showSidebar") private var showSidebar = true
    @AppStorage("fontSize") private var fontSize = 14.0

    var body: some View {
        Form {
            Toggle("Show Sidebar", isOn: $showSidebar)
            Slider(value: $fontSize, in: 10...24, step: 1) {
                Text("Font Size: \(Int(fontSize))")
            }
        }
        .formStyle(.grouped)
        .padding()
    }
}
```

For detailed settings patterns, see [references/settings-preferences.md](references/settings-preferences.md).

## Document-Based Apps

### FileDocument Implementation

```swift
struct TextDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.plainText] }

    var text: String

    init(text: String = "") {
        self.text = text
    }

    init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents,
              let string = String(data: data, encoding: .utf8) else {
            throw CocoaError(.fileReadCorruptFile)
        }
        text = string
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        let data = text.data(using: .utf8)!
        return FileWrapper(regularFileWithContents: data)
    }
}

@main
struct TextEditorApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: TextDocument()) { file in
            TextEditorView(document: file.$document)
        }
    }
}
```

For detailed document patterns, see [references/document-based-apps.md](references/document-based-apps.md).

## Toolbar

### Toolbar Items

```swift
struct ContentView: View {
    @State private var searchText = ""

    var body: some View {
        NavigationSplitView {
            Sidebar()
        } detail: {
            DetailView()
        }
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button(action: addItem) {
                    Label("Add", systemImage: "plus")
                }
            }

            ToolbarItem(placement: .navigation) {
                Button(action: toggleSidebar) {
                    Label("Sidebar", systemImage: "sidebar.left")
                }
            }
        }
        .searchable(text: $searchText, placement: .toolbar)
    }
}
```

### ToolbarItemGroup

```swift
.toolbar {
    ToolbarItemGroup(placement: .primaryAction) {
        Button { } label: {
            Label("Bold", systemImage: "bold")
        }
        Button { } label: {
            Label("Italic", systemImage: "italic")
        }
    }
}
```

## System Integration

### Notifications

```swift
import UserNotifications

func requestNotificationPermission() async -> Bool {
    let center = UNUserNotificationCenter.current()
    do {
        return try await center.requestAuthorization(options: [.alert, .sound, .badge])
    } catch {
        return false
    }
}

func sendNotification(title: String, body: String) {
    let content = UNMutableNotificationContent()
    content.title = title
    content.body = body
    content.sound = .default

    let request = UNNotificationRequest(
        identifier: UUID().uuidString,
        content: content,
        trigger: nil
    )

    UNUserNotificationCenter.current().add(request)
}
```

### Menu Bar Extra (Status Bar Apps)

```swift
@main
struct MyApp: App {
    var body: some Scene {
        MenuBarExtra("My App", systemImage: "star") {
            MenuBarView()
        }
        .menuBarExtraStyle(.window)
    }
}
```

For detailed system integration patterns, see [references/system-integration.md](references/system-integration.md).

## Drag & Drop / Pasteboard

### Transferable Protocol

```swift
struct MyItem: Transferable, Codable {
    var id: UUID
    var name: String

    static var transferRepresentation: some TransferRepresentation {
        CodableRepresentation(contentType: .myItem)
        ProxyRepresentation(exporting: \.name)
    }
}

extension UTType {
    static var myItem = UTType(exportedAs: "com.example.myitem")
}
```

### Draggable and DropDestination

```swift
struct ItemView: View {
    let item: MyItem

    var body: some View {
        Text(item.name)
            .draggable(item)
    }
}

struct DropZoneView: View {
    @State private var items: [MyItem] = []

    var body: some View {
        VStack {
            ForEach(items) { item in
                Text(item.name)
            }
        }
        .dropDestination(for: MyItem.self) { items, location in
            self.items.append(contentsOf: items)
            return true
        }
    }
}
```

For detailed drag & drop patterns, see [references/drag-drop-pasteboard.md](references/drag-drop-pasteboard.md).

## macOS-Specific UI Components

### Table View

```swift
struct TableExample: View {
    @State private var items: [Item] = []
    @State private var selection: Set<Item.ID> = []
    @State private var sortOrder = [KeyPathComparator(\Item.name)]

    var body: some View {
        Table(items, selection: $selection, sortOrder: $sortOrder) {
            TableColumn("Name", value: \.name)
            TableColumn("Date", value: \.date) { item in
                Text(item.date.formatted())
            }
            TableColumn("Size", value: \.size) { item in
                Text("\(item.size) KB")
            }
        }
        .onChange(of: sortOrder) { _, newOrder in
            items.sort(using: newOrder)
        }
    }
}
```

### Popover

```swift
struct PopoverExample: View {
    @State private var showPopover = false

    var body: some View {
        Button("Show Info") {
            showPopover = true
        }
        .popover(isPresented: $showPopover, arrowEdge: .bottom) {
            VStack {
                Text("Information")
                    .font(.headline)
                Text("Details go here")
            }
            .padding()
            .frame(width: 200)
        }
    }
}
```

## AppKit Integration

### NSViewRepresentable

```swift
import AppKit
import SwiftUI

struct NSTextViewWrapper: NSViewRepresentable {
    @Binding var text: String

    func makeNSView(context: Context) -> NSScrollView {
        let scrollView = NSTextView.scrollableTextView()
        let textView = scrollView.documentView as! NSTextView
        textView.delegate = context.coordinator
        textView.string = text
        return scrollView
    }

    func updateNSView(_ scrollView: NSScrollView, context: Context) {
        let textView = scrollView.documentView as! NSTextView
        if textView.string != text {
            textView.string = text
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, NSTextViewDelegate {
        var parent: NSTextViewWrapper

        init(_ parent: NSTextViewWrapper) {
            self.parent = parent
        }

        func textDidChange(_ notification: Notification) {
            guard let textView = notification.object as? NSTextView else { return }
            parent.text = textView.string
        }
    }
}
```

## Code Quality Checklist

Before submitting code, verify:

- [ ] All public APIs have documentation comments
- [ ] ViewModels use `@MainActor` for UI updates
- [ ] Windows have appropriate default sizes and positions
- [ ] Menu commands have keyboard shortcuts where appropriate
- [ ] Settings are properly persisted with @AppStorage
- [ ] Document apps handle errors gracefully
- [ ] Drag & drop uses Transferable protocol correctly
- [ ] No force unwrapping (`!`) without safety checks
- [ ] Memory management: no retain cycles in closures
- [ ] App works correctly in sandboxed environment

## Additional Resources

### Reference Files

- **[references/window-management.md](references/window-management.md)** - Window management patterns
- **[references/menu-commands.md](references/menu-commands.md)** - Menu and keyboard shortcuts
- **[references/settings-preferences.md](references/settings-preferences.md)** - Settings implementation
- **[references/document-based-apps.md](references/document-based-apps.md)** - FileDocument patterns
- **[references/navigation-patterns.md](references/navigation-patterns.md)** - NavigationSplitView details
- **[references/system-integration.md](references/system-integration.md)** - Notifications, Widgets, Spotlight
- **[references/drag-drop-pasteboard.md](references/drag-drop-pasteboard.md)** - Transferable protocol
- **[references/troubleshooting.md](references/troubleshooting.md)** - Sandbox, signing, notarization

### Example Files

- **[examples/basic-macos-app.swift](examples/basic-macos-app.swift)** - Basic macOS app structure
- **[examples/multi-window-app.swift](examples/multi-window-app.swift)** - Multi-window application
- **[examples/document-based-app.swift](examples/document-based-app.swift)** - Document-based app
- **[examples/menu-commands.swift](examples/menu-commands.swift)** - Menu and commands implementation
- **[examples/navigation-splitview.swift](examples/navigation-splitview.swift)** - NavigationSplitView patterns
- **[examples/settings-window.swift](examples/settings-window.swift)** - Settings window implementation

### Utility Scripts

- **[scripts/macos-project-analyzer.sh](scripts/macos-project-analyzer.sh)** - Analyze macOS project structure
