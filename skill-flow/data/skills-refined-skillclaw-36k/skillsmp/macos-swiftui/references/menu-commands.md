# Menu Commands Reference (macOS 14+)

Comprehensive guide to implementing menus and keyboard shortcuts in macOS SwiftUI applications.

## Commands Overview

The `Commands` protocol allows you to define menu items that appear in the app's menu bar.

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .commands {
            MyCommands()
        }
    }
}

struct MyCommands: Commands {
    var body: some Commands {
        // Menu definitions
    }
}
```

## Standard Command Groups

### Replacing Standard Commands

```swift
struct MyCommands: Commands {
    var body: some Commands {
        // Replace New Item commands
        CommandGroup(replacing: .newItem) {
            Button("New Document") { }
                .keyboardShortcut("n", modifiers: .command)
        }

        // Replace Save Item commands
        CommandGroup(replacing: .saveItem) {
            Button("Save") { }
                .keyboardShortcut("s", modifiers: .command)
            Button("Save As...") { }
                .keyboardShortcut("s", modifiers: [.command, .shift])
        }
    }
}
```

### Available Replacement Groups

| Group | Description |
|-------|-------------|
| `.appInfo` | About menu item |
| `.appSettings` | Settings/Preferences |
| `.appVisibility` | Hide/Show app |
| `.appTermination` | Quit |
| `.newItem` | New document/window |
| `.saveItem` | Save commands |
| `.importExport` | Import/Export |
| `.printItem` | Print commands |
| `.undoRedo` | Undo/Redo |
| `.pasteboard` | Cut/Copy/Paste |
| `.textEditing` | Text editing commands |
| `.textFormatting` | Text formatting |
| `.toolbar` | Toolbar commands |
| `.sidebar` | Sidebar toggle |
| `.windowSize` | Window size commands |
| `.windowList` | Window list |
| `.windowArrangement` | Window arrangement |
| `.singleWindowList` | Single window list |
| `.help` | Help menu |

### Adding Before/After Standard Commands

```swift
struct MyCommands: Commands {
    var body: some Commands {
        // Add after New Item
        CommandGroup(after: .newItem) {
            Button("New From Template...") { }
                .keyboardShortcut("n", modifiers: [.command, .option])
        }

        // Add before Undo/Redo
        CommandGroup(before: .undoRedo) {
            Button("Custom Action") { }
        }
    }
}
```

## Custom Command Menus

```swift
struct MyCommands: Commands {
    var body: some Commands {
        CommandMenu("Tools") {
            Button("Run Script") { }
                .keyboardShortcut("r", modifiers: .command)

            Button("Build") { }
                .keyboardShortcut("b", modifiers: .command)

            Divider()

            Menu("Transform") {
                Button("Uppercase") { }
                Button("Lowercase") { }
                Button("Capitalize") { }
            }
        }
    }
}
```

## Keyboard Shortcuts

### Basic Shortcuts

```swift
Button("Save") {
    save()
}
.keyboardShortcut("s", modifiers: .command)
```

### Modifier Combinations

```swift
// Command + Shift + S
.keyboardShortcut("s", modifiers: [.command, .shift])

// Command + Option + S
.keyboardShortcut("s", modifiers: [.command, .option])

// Command + Control + S
.keyboardShortcut("s", modifiers: [.command, .control])
```

### Special Keys

```swift
// Return/Enter
.keyboardShortcut(.return)

// Escape
.keyboardShortcut(.escape)

// Delete
.keyboardShortcut(.delete)

// Tab
.keyboardShortcut(.tab)

// Space
.keyboardShortcut(.space)

// Arrow keys
.keyboardShortcut(.upArrow)
.keyboardShortcut(.downArrow)
.keyboardShortcut(.leftArrow)
.keyboardShortcut(.rightArrow)
```

### Default Actions

```swift
// Primary action (Return)
.keyboardShortcut(.defaultAction)

// Cancel action (Escape)
.keyboardShortcut(.cancelAction)
```

## FocusedValue and FocusedBinding

### Defining Focused Values

```swift
// Define the key
struct SelectedDocumentKey: FocusedValueKey {
    typealias Value = Document
}

extension FocusedValues {
    var selectedDocument: Document? {
        get { self[SelectedDocumentKey.self] }
        set { self[SelectedDocumentKey.self] = newValue }
    }
}
```

### Publishing Focused Values

```swift
struct DocumentView: View {
    let document: Document

    var body: some View {
        TextEditor(text: $document.text)
            .focusedValue(\.selectedDocument, document)
    }
}
```

### Using in Commands

```swift
struct DocumentCommands: Commands {
    @FocusedValue(\.selectedDocument) private var document

    var body: some Commands {
        CommandMenu("Document") {
            Button("Export...") {
                document?.export()
            }
            .disabled(document == nil)
        }
    }
}
```

### FocusedBinding for Two-Way Binding

```swift
struct TextKey: FocusedValueKey {
    typealias Value = Binding<String>
}

extension FocusedValues {
    var text: Binding<String>? {
        get { self[TextKey.self] }
        set { self[TextKey.self] = newValue }
    }
}

// In view
.focusedSceneValue(\.text, $document.text)

// In commands
struct EditCommands: Commands {
    @FocusedBinding(\.text) private var text

    var body: some Commands {
        CommandGroup(after: .pasteboard) {
            Button("Clear") {
                text = ""
            }
            .disabled(text == nil)
        }
    }
}
```

## Conditional Commands

### Disabling Commands

```swift
struct MyCommands: Commands {
    @FocusedValue(\.selectedItem) private var item

    var body: some Commands {
        CommandMenu("Item") {
            Button("Delete") {
                item?.delete()
            }
            .disabled(item == nil)
        }
    }
}
```

### Dynamic Commands

```swift
struct ViewCommands: Commands {
    @Binding var viewMode: ViewMode

    var body: some Commands {
        CommandMenu("View") {
            Picker("Mode", selection: $viewMode) {
                Text("List").tag(ViewMode.list)
                Text("Grid").tag(ViewMode.grid)
                Text("Columns").tag(ViewMode.columns)
            }
            .pickerStyle(.inline)
        }
    }
}
```

## Toggle Commands

```swift
struct ViewCommands: Commands {
    @Binding var showSidebar: Bool
    @Binding var showInspector: Bool

    var body: some Commands {
        CommandMenu("View") {
            Toggle("Show Sidebar", isOn: $showSidebar)
                .keyboardShortcut("s", modifiers: [.command, .control])

            Toggle("Show Inspector", isOn: $showInspector)
                .keyboardShortcut("i", modifiers: [.command, .option])
        }
    }
}
```

## Submenus

```swift
struct FormatCommands: Commands {
    var body: some Commands {
        CommandMenu("Format") {
            Menu("Font") {
                Button("Bold") { }
                    .keyboardShortcut("b", modifiers: .command)
                Button("Italic") { }
                    .keyboardShortcut("i", modifiers: .command)
                Button("Underline") { }
                    .keyboardShortcut("u", modifiers: .command)
            }

            Menu("Text") {
                Button("Align Left") { }
                Button("Center") { }
                Button("Align Right") { }
                Divider()
                Button("Justify") { }
            }
        }
    }
}
```

## Context Menus

```swift
struct ItemView: View {
    let item: Item

    var body: some View {
        Text(item.name)
            .contextMenu {
                Button("Open") {
                    item.open()
                }

                Button("Rename") {
                    item.rename()
                }

                Divider()

                Button("Delete", role: .destructive) {
                    item.delete()
                }
            }
    }
}
```

## Menu Bar Item (MenuBarExtra)

```swift
@main
struct MyApp: App {
    var body: some Scene {
        MenuBarExtra("Status", systemImage: "star") {
            Button("Show Main Window") {
                // Action
            }
            .keyboardShortcut("1", modifiers: .command)

            Divider()

            Menu("Recent Items") {
                Button("Item 1") { }
                Button("Item 2") { }
            }

            Divider()

            Button("Quit") {
                NSApplication.shared.terminate(nil)
            }
            .keyboardShortcut("q", modifiers: .command)
        }
    }
}
```

## Best Practices

1. **Follow Platform Conventions** - Use standard shortcuts (⌘S for Save, ⌘Q for Quit)
2. **Group Related Commands** - Use dividers and submenus for organization
3. **Provide Keyboard Shortcuts** - For frequently used commands
4. **Disable When Inappropriate** - Use `.disabled()` when actions can't be performed
5. **Use FocusedValue** - For window-specific command behavior
6. **Keep Menus Organized** - Don't overcrowd menus
7. **Use Descriptive Labels** - Commands should be self-explanatory

## Common Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New | ⌘N |
| Open | ⌘O |
| Save | ⌘S |
| Save As | ⇧⌘S |
| Close | ⌘W |
| Quit | ⌘Q |
| Undo | ⌘Z |
| Redo | ⇧⌘Z |
| Cut | ⌘X |
| Copy | ⌘C |
| Paste | ⌘V |
| Select All | ⌘A |
| Find | ⌘F |
| Preferences | ⌘, |
