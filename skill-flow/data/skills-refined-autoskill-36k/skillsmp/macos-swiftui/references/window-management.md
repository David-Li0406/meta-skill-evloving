# Window Management Reference (macOS 14+)

Comprehensive guide to window management in macOS SwiftUI applications.

## Scene Types

### WindowGroup

Creates a window that can have multiple instances. Each instance shares the same view hierarchy but has independent state.

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

**Key Characteristics**:
- Users can create multiple windows via File > New Window
- Each window is independent
- Window state is not shared between instances
- Appears in Window menu

### Window (Single Instance)

Creates a single-instance window. Attempting to open it again brings the existing window to front.

```swift
@main
struct MyApp: App {
    var body: some Scene {
        Window("Preferences", id: "preferences") {
            PreferencesView()
        }
    }
}
```

**Key Characteristics**:
- Only one instance can exist
- Great for inspectors, palettes, auxiliary windows
- Requires explicit ID for programmatic opening

### WindowGroup with ID

Creates a window group with a specific identifier for programmatic control.

```swift
WindowGroup(id: "editor") {
    EditorView()
}
```

### WindowGroup with Value

Creates windows that are associated with specific data values.

```swift
WindowGroup(for: Document.ID.self) { $documentId in
    if let documentId {
        DocumentView(documentId: documentId)
    }
}
```

## Window Modifiers

### Default Size

```swift
WindowGroup {
    ContentView()
}
.defaultSize(width: 800, height: 600)

// Using CGSize
.defaultSize(CGSize(width: 800, height: 600))
```

### Default Position

```swift
.defaultPosition(.center)
.defaultPosition(.topLeading)
.defaultPosition(.topTrailing)
.defaultPosition(.bottomLeading)
.defaultPosition(.bottomTrailing)

// Custom position
.defaultPosition(UnitPoint(x: 0.5, y: 0.3))
```

### Window Resizability

```swift
// Content-based sizing (window adjusts to content)
.windowResizability(.contentSize)

// Minimum content size
.windowResizability(.contentMinSize)

// Free resizing (default)
.windowResizability(.automatic)
```

### Window Style

```swift
// Standard titlebar
.windowStyle(.automatic)

// Hidden titlebar
.windowStyle(.hiddenTitleBar)

// Titlebar with accessory views
.windowStyle(.titleBar)
```

### Window Toolbar Style

```swift
.windowToolbarStyle(.automatic)
.windowToolbarStyle(.unified)
.windowToolbarStyle(.unifiedCompact)
.windowToolbarStyle(.expanded)
```

## Opening Windows Programmatically

### Using Environment

```swift
struct ContentView: View {
    @Environment(\.openWindow) private var openWindow

    var body: some View {
        Button("Open Inspector") {
            // Open by ID
            openWindow(id: "inspector")

            // Open with value
            openWindow(value: document.id)
        }
    }
}
```

### Opening URL

```swift
struct ContentView: View {
    @Environment(\.openURL) private var openURL

    var body: some View {
        Button("Open in Browser") {
            openURL(URL(string: "https://example.com")!)
        }
    }
}
```

## Closing Windows

### Using Environment

```swift
struct DetailView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        Button("Close") {
            dismiss()
        }
    }
}
```

### Window Close Confirmation

```swift
struct DocumentView: View {
    @State private var hasUnsavedChanges = false

    var body: some View {
        TextEditor(text: $text)
            .interactiveDismissDisabled(hasUnsavedChanges)
    }
}
```

## Window State Persistence

### Using SceneStorage

```swift
struct ContentView: View {
    @SceneStorage("selectedTab") private var selectedTab = "home"
    @SceneStorage("sidebarWidth") private var sidebarWidth: CGFloat = 200

    var body: some View {
        // State is restored per window
    }
}
```

### Window Position and Size Persistence

```swift
WindowGroup {
    ContentView()
}
.defaultSize(width: 800, height: 600)
// macOS automatically persists window frame
```

## Multi-Window Patterns

### Main + Auxiliary Windows

```swift
@main
struct MyApp: App {
    var body: some Scene {
        // Main window
        WindowGroup {
            MainView()
        }

        // Inspector (single instance)
        Window("Inspector", id: "inspector") {
            InspectorView()
        }
        .defaultSize(width: 300, height: 400)

        // Activity monitor (value-based)
        WindowGroup("Activity", for: Activity.ID.self) { $activityId in
            ActivityView(activityId: activityId)
        }
    }
}
```

### Sharing State Between Windows

```swift
@Observable
class SharedState {
    var selectedDocument: Document?
    var preferences: Preferences
}

@main
struct MyApp: App {
    @State private var sharedState = SharedState()

    var body: some Scene {
        WindowGroup {
            MainView()
                .environment(sharedState)
        }

        Window("Inspector", id: "inspector") {
            InspectorView()
                .environment(sharedState)
        }
    }
}
```

## Window Level and Behavior

### Floating Windows

For windows that should float above others (like inspectors):

```swift
// Using NSWindow (via AppKit integration)
extension NSWindow {
    static func configureAsPanel(_ window: NSWindow) {
        window.level = .floating
        window.collectionBehavior = [.moveToActiveSpace, .fullScreenAuxiliary]
    }
}
```

### Full Screen Support

```swift
struct ContentView: View {
    @Environment(\.supportsMultipleWindows) private var supportsMultipleWindows

    var body: some View {
        content
    }
}
```

## MenuBarExtra (Status Bar Apps)

### Menu-Based

```swift
@main
struct StatusBarApp: App {
    var body: some Scene {
        MenuBarExtra("My App", systemImage: "star") {
            Button("Action 1") { }
            Button("Action 2") { }
            Divider()
            Button("Quit") {
                NSApplication.shared.terminate(nil)
            }
        }
    }
}
```

### Window-Based

```swift
@main
struct StatusBarApp: App {
    var body: some Scene {
        MenuBarExtra("My App", systemImage: "star") {
            StatusBarPanelView()
        }
        .menuBarExtraStyle(.window)
    }
}
```

## Best Practices

1. **Use WindowGroup for main content** - Allows users to create multiple windows
2. **Use Window for single-instance UI** - Inspectors, preferences, palettes
3. **Always set default sizes** - Provides better initial experience
4. **Use meaningful window IDs** - Makes programmatic opening clearer
5. **Share state via Environment** - Use @Observable for shared state
6. **Persist window-specific state with SceneStorage** - Preserves user customization
7. **Consider window restoration** - macOS restores windows on app launch
