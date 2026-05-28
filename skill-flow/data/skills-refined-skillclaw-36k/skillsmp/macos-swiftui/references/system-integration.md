# System Integration Reference (macOS 14+)

Comprehensive guide to integrating macOS system features in SwiftUI applications.

## Notifications

### Requesting Permission

```swift
import UserNotifications

func requestNotificationPermission() async -> Bool {
    let center = UNUserNotificationCenter.current()
    do {
        let granted = try await center.requestAuthorization(options: [.alert, .sound, .badge])
        return granted
    } catch {
        print("Error requesting notification permission: \(error)")
        return false
    }
}
```

### Sending Notifications

```swift
func sendNotification(title: String, body: String, identifier: String? = nil) {
    let content = UNMutableNotificationContent()
    content.title = title
    content.body = body
    content.sound = .default

    let request = UNNotificationRequest(
        identifier: identifier ?? UUID().uuidString,
        content: content,
        trigger: nil // Deliver immediately
    )

    UNUserNotificationCenter.current().add(request)
}
```

### Scheduled Notifications

```swift
func scheduleNotification(title: String, body: String, date: Date) {
    let content = UNMutableNotificationContent()
    content.title = title
    content.body = body

    let components = Calendar.current.dateComponents(
        [.year, .month, .day, .hour, .minute],
        from: date
    )
    let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: false)

    let request = UNNotificationRequest(
        identifier: UUID().uuidString,
        content: content,
        trigger: trigger
    )

    UNUserNotificationCenter.current().add(request)
}
```

### Notification Delegate

```swift
class NotificationDelegate: NSObject, UNUserNotificationCenterDelegate {
    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification
    ) async -> UNNotificationPresentationOptions {
        // Show notification even when app is in foreground
        return [.banner, .sound]
    }

    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse
    ) async {
        // Handle notification tap
        let identifier = response.notification.request.identifier
        // Navigate to relevant content
    }
}
```

## MenuBarExtra (Status Bar Apps)

### Menu-Based

```swift
@main
struct StatusBarApp: App {
    var body: some Scene {
        MenuBarExtra("My App", systemImage: "star.fill") {
            Button("Show Dashboard") {
                // Show main window
            }
            .keyboardShortcut("d", modifiers: .command)

            Button("Check for Updates") {
                // Check updates
            }

            Divider()

            Button("Preferences...") {
                // Open preferences
            }
            .keyboardShortcut(",", modifiers: .command)

            Divider()

            Button("Quit") {
                NSApplication.shared.terminate(nil)
            }
            .keyboardShortcut("q", modifiers: .command)
        }
    }
}
```

### Window-Based

```swift
@main
struct StatusBarApp: App {
    var body: some Scene {
        MenuBarExtra("My App", systemImage: "star.fill") {
            StatusPanelView()
                .frame(width: 300, height: 400)
        }
        .menuBarExtraStyle(.window)
    }
}

struct StatusPanelView: View {
    var body: some View {
        VStack {
            // Panel content
        }
        .padding()
    }
}
```

### Dynamic Menu Bar Icon

```swift
@main
struct StatusBarApp: App {
    @State private var isConnected = false

    var body: some Scene {
        MenuBarExtra {
            // Menu content
        } label: {
            Image(systemName: isConnected ? "wifi" : "wifi.slash")
        }
    }
}
```

## NSWorkspace Integration

### Open URLs and Files

```swift
import AppKit

// Open URL in default browser
func openURL(_ url: URL) {
    NSWorkspace.shared.open(url)
}

// Open file with default app
func openFile(_ path: String) {
    NSWorkspace.shared.openFile(path)
}

// Open file with specific app
func openFile(_ path: String, withApp appPath: String) {
    NSWorkspace.shared.openFile(path, withApplication: appPath)
}

// Reveal in Finder
func revealInFinder(_ url: URL) {
    NSWorkspace.shared.activateFileViewerSelecting([url])
}
```

### Get Running Applications

```swift
func getRunningApplications() -> [NSRunningApplication] {
    NSWorkspace.shared.runningApplications
}

func isAppRunning(bundleIdentifier: String) -> Bool {
    NSWorkspace.shared.runningApplications.contains {
        $0.bundleIdentifier == bundleIdentifier
    }
}
```

### Launch Applications

```swift
func launchApp(bundleIdentifier: String) {
    NSWorkspace.shared.launchApplication(
        withBundleIdentifier: bundleIdentifier,
        options: [],
        additionalEventParamDescriptor: nil,
        launchIdentifier: nil
    )
}
```

### System Events

```swift
class WorkspaceObserver {
    private var observer: NSObjectProtocol?

    init() {
        observer = NSWorkspace.shared.notificationCenter.addObserver(
            forName: NSWorkspace.didWakeNotification,
            object: nil,
            queue: .main
        ) { _ in
            print("System woke from sleep")
        }
    }

    deinit {
        if let observer {
            NSWorkspace.shared.notificationCenter.removeObserver(observer)
        }
    }
}
```

## Widgets (WidgetKit)

### Widget Configuration

```swift
import WidgetKit
import SwiftUI

struct MyWidget: Widget {
    let kind: String = "MyWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            MyWidgetView(entry: entry)
        }
        .configurationDisplayName("My Widget")
        .description("Shows important information.")
        .supportedFamilies([.systemSmall, .systemMedium, .systemLarge])
    }
}

struct Provider: TimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(date: Date(), data: "Placeholder")
    }

    func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> ()) {
        completion(SimpleEntry(date: Date(), data: "Snapshot"))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<SimpleEntry>) -> ()) {
        let entry = SimpleEntry(date: Date(), data: "Timeline")
        let timeline = Timeline(entries: [entry], policy: .after(Date().addingTimeInterval(3600)))
        completion(timeline)
    }
}
```

### Widget View

```swift
struct MyWidgetView: View {
    var entry: Provider.Entry
    @Environment(\.widgetFamily) var family

    var body: some View {
        switch family {
        case .systemSmall:
            SmallWidgetView(entry: entry)
        case .systemMedium:
            MediumWidgetView(entry: entry)
        case .systemLarge:
            LargeWidgetView(entry: entry)
        default:
            Text("Unsupported")
        }
    }
}
```

## Spotlight Integration

### Core Spotlight Indexing

```swift
import CoreSpotlight
import MobileCoreServices

func indexItem(_ item: Item) {
    let attributeSet = CSSearchableItemAttributeSet(contentType: .content)
    attributeSet.title = item.name
    attributeSet.contentDescription = item.description
    attributeSet.keywords = item.tags

    let searchableItem = CSSearchableItem(
        uniqueIdentifier: item.id.uuidString,
        domainIdentifier: "com.example.items",
        attributeSet: attributeSet
    )

    CSSearchableIndex.default().indexSearchableItems([searchableItem]) { error in
        if let error {
            print("Indexing error: \(error)")
        }
    }
}

func removeFromIndex(_ itemId: String) {
    CSSearchableIndex.default().deleteSearchableItems(withIdentifiers: [itemId])
}

func removeAllFromIndex() {
    CSSearchableIndex.default().deleteAllSearchableItems()
}
```

### Handling Spotlight Results

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .onContinueUserActivity(CSSearchableItemActionType) { activity in
                    if let identifier = activity.userInfo?[CSSearchableItemActivityIdentifier] as? String {
                        // Navigate to item with identifier
                    }
                }
        }
    }
}
```

## Services Menu

### Providing Services

In Info.plist:

```xml
<key>NSServices</key>
<array>
    <dict>
        <key>NSMessage</key>
        <string>processText:</string>
        <key>NSMenuItem</key>
        <dict>
            <key>default</key>
            <string>Process with My App</string>
        </dict>
        <key>NSSendTypes</key>
        <array>
            <string>public.utf8-plain-text</string>
        </array>
    </dict>
</array>
```

### Service Implementation

```swift
class ServiceProvider: NSObject {
    @objc func processText(_ pasteboard: NSPasteboard, userData: String?, error: AutoreleasingUnsafeMutablePointer<NSString?>) {
        guard let text = pasteboard.string(forType: .string) else { return }
        // Process the text
    }
}

// In AppDelegate
NSApp.servicesProvider = ServiceProvider()
```

## Quick Look Preview

```swift
import QuickLookUI

struct QuickLookView: NSViewRepresentable {
    let url: URL

    func makeNSView(context: Context) -> QLPreviewView {
        let view = QLPreviewView()
        view.previewItem = url as QLPreviewItem
        return view
    }

    func updateNSView(_ nsView: QLPreviewView, context: Context) {
        nsView.previewItem = url as QLPreviewItem
    }
}
```

## Share Extensions

### Using NSSharingServicePicker

```swift
struct ShareButton: View {
    let items: [Any]

    var body: some View {
        Button {
            showShareMenu()
        } label: {
            Label("Share", systemImage: "square.and.arrow.up")
        }
    }

    private func showShareMenu() {
        let picker = NSSharingServicePicker(items: items)
        if let window = NSApp.keyWindow {
            picker.show(relativeTo: .zero, of: window.contentView!, preferredEdge: .minY)
        }
    }
}
```

## Best Practices

1. **Request permissions appropriately** - Only when needed, explain why
2. **Handle notification permissions** - Check status before sending
3. **Use appropriate notification timing** - Don't spam users
4. **Keep widgets lightweight** - They have limited resources
5. **Index relevant content only** - Don't pollute Spotlight
6. **Update indexes when content changes** - Keep data current
7. **Test services menu integration** - Ensure proper data handling
8. **Consider system preferences** - Respect Do Not Disturb, etc.
