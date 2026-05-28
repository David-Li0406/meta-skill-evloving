# Troubleshooting Reference (macOS 14+)

Common issues and solutions for macOS SwiftUI app development.

## App Sandbox

### Understanding Sandbox

macOS apps distributed through the App Store must be sandboxed. The sandbox restricts:
- File system access (limited to app container and user-selected files)
- Network access (requires entitlement)
- Hardware access (camera, microphone, etc.)
- Inter-process communication

### Enabling Sandbox

In your app's entitlements file:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
</dict>
</plist>
```

### Common Sandbox Entitlements

```xml
<!-- Network access -->
<key>com.apple.security.network.client</key>
<true/>
<key>com.apple.security.network.server</key>
<true/>

<!-- File access -->
<key>com.apple.security.files.user-selected.read-only</key>
<true/>
<key>com.apple.security.files.user-selected.read-write</key>
<true/>
<key>com.apple.security.files.downloads.read-write</key>
<true/>

<!-- Hardware -->
<key>com.apple.security.device.camera</key>
<true/>
<key>com.apple.security.device.microphone</key>
<true/>
<key>com.apple.security.device.bluetooth</key>
<true/>

<!-- Other -->
<key>com.apple.security.print</key>
<true/>
<key>com.apple.security.personal-information.location</key>
<true/>
```

### Accessing Files Outside Sandbox

Use Security-Scoped Bookmarks:

```swift
func saveBookmark(for url: URL) throws -> Data {
    try url.bookmarkData(
        options: .withSecurityScope,
        includingResourceValuesForKeys: nil,
        relativeTo: nil
    )
}

func resolveBookmark(_ data: Data) throws -> URL {
    var isStale = false
    let url = try URL(
        resolvingBookmarkData: data,
        options: .withSecurityScope,
        relativeTo: nil,
        bookmarkDataIsStale: &isStale
    )

    if isStale {
        // Bookmark needs to be recreated
    }

    return url
}

// Usage
func accessSecuredResource(_ url: URL) {
    guard url.startAccessingSecurityScopedResource() else {
        print("Failed to access resource")
        return
    }

    defer {
        url.stopAccessingSecurityScopedResource()
    }

    // Read/write file
}
```

## Code Signing

### Signing Requirements

All macOS apps need to be signed:
- **Development**: Automatic signing with development certificate
- **Distribution**: Requires Developer ID or App Store certificate

### Checking Signature

```bash
# Check if app is signed
codesign -v /path/to/MyApp.app

# Display signature details
codesign -dv --verbose=4 /path/to/MyApp.app

# Verify deep signature (all nested code)
codesign --verify --deep --strict /path/to/MyApp.app
```

### Common Signing Issues

**"Code signature invalid"**
- Rebuild the app
- Check that all frameworks are signed
- Verify entitlements are correct

**"Resource envelope is obsolete"**
- Re-sign the app with `--force` flag

```bash
codesign --force --deep --sign "Developer ID Application: Your Name" /path/to/MyApp.app
```

## Notarization

### Requirements

Apps distributed outside the App Store must be notarized by Apple.

### Notarization Process

1. Archive and export your app
2. Submit for notarization
3. Staple the notarization ticket

```bash
# Submit for notarization
xcrun notarytool submit MyApp.zip \
    --apple-id "your@email.com" \
    --team-id "TEAM_ID" \
    --password "@keychain:AC_PASSWORD" \
    --wait

# Check status
xcrun notarytool log <submission-id> \
    --apple-id "your@email.com" \
    --team-id "TEAM_ID" \
    --password "@keychain:AC_PASSWORD"

# Staple the ticket
xcrun stapler staple MyApp.app
```

### Common Notarization Issues

**"The binary uses an SDK older than the 10.9 SDK"**
- Update minimum deployment target
- Rebuild with latest Xcode

**"The signature does not include a secure timestamp"**
- Re-sign with `--timestamp` flag

**"The executable requests the com.apple.security.get-task-allow entitlement"**
- This entitlement is only for development
- Use different entitlements for release builds

## Hardened Runtime

### Enabling Hardened Runtime

Required for notarization. Enable in Xcode:
1. Select your target
2. Go to Signing & Capabilities
3. Enable "Hardened Runtime"

### Hardened Runtime Entitlements

```xml
<!-- Allow JIT compilation (for JavaScript engines, etc.) -->
<key>com.apple.security.cs.allow-jit</key>
<true/>

<!-- Allow unsigned executable memory -->
<key>com.apple.security.cs.allow-unsigned-executable-memory</key>
<true/>

<!-- Allow DYLD environment variables -->
<key>com.apple.security.cs.allow-dyld-environment-variables</key>
<true/>

<!-- Disable library validation -->
<key>com.apple.security.cs.disable-library-validation</key>
<true/>

<!-- Debugging (development only) -->
<key>com.apple.security.get-task-allow</key>
<true/>
```

## Common Runtime Issues

### Window Not Appearing

```swift
// Ensure window is created on main thread
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .defaultSize(width: 800, height: 600) // Add explicit size
    }
}
```

### Menu Commands Not Working

```swift
// Ensure commands are attached to the correct scene
WindowGroup {
    ContentView()
}
.commands {
    MyCommands() // Commands must return valid Commands type
}
```

### Keyboard Shortcuts Not Responding

- Check for conflicting system shortcuts
- Ensure view is in focus
- Verify modifier keys are correct

```swift
// Correct
.keyboardShortcut("s", modifiers: .command)

// Not: modifiers: [.command] for single modifier
```

### Settings Window Not Opening

```swift
// Ensure Settings scene is defined
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        Settings {
            SettingsView() // Must be defined
        }
    }
}
```

### NavigationSplitView Issues

**Sidebar not showing:**
```swift
// Check column visibility
NavigationSplitView(columnVisibility: .constant(.all)) {
    // ...
}
```

**Detail view not updating:**
```swift
// Ensure selection binding is correct
@State private var selection: Item? // Use optional for single selection
@State private var selection: Set<Item.ID> = [] // Use Set for multiple
```

## Performance Issues

### Slow List Scrolling

```swift
// Use LazyVStack instead of VStack in ScrollView
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ItemRow(item: item)
        }
    }
}

// Use List with proper identifiable items
List(items) { item in
    ItemRow(item: item)
}
```

### High Memory Usage

```swift
// Don't load all images at once
AsyncImage(url: item.imageURL) { image in
    image.resizable()
} placeholder: {
    ProgressView()
}

// Use proper image caching
```

### Slow App Launch

- Defer heavy initialization
- Use lazy loading
- Profile with Instruments

```swift
@main
struct MyApp: App {
    init() {
        // Keep lightweight
        // Defer heavy setup
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
                .task {
                    // Load data after UI appears
                    await loadData()
                }
        }
    }
}
```

## Debugging Tips

### Enable Debug Logging

```swift
// In scheme arguments
-com.apple.CoreData.SQLDebug 1
-com.apple.CoreData.Logging.stderr 1
```

### SwiftUI Debugging

```swift
// Print view updates
let _ = Self._printChanges()

// In view body
var body: some View {
    let _ = print("View updating")
    // ...
}
```

### Console Logging

```swift
import os

let logger = Logger(subsystem: "com.example.app", category: "general")

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

## App Store Submission

### Common Rejection Reasons

1. **Missing purpose strings** - Add all required Info.plist descriptions
2. **Incomplete functionality** - App must be functional
3. **Placeholder content** - Remove lorem ipsum, etc.
4. **Missing privacy policy** - Required for data collection
5. **Guideline violations** - Review App Store guidelines

### Required Info.plist Keys

```xml
<!-- Camera usage -->
<key>NSCameraUsageDescription</key>
<string>This app uses the camera to...</string>

<!-- Microphone usage -->
<key>NSMicrophoneUsageDescription</key>
<string>This app uses the microphone to...</string>

<!-- Location usage -->
<key>NSLocationUsageDescription</key>
<string>This app uses your location to...</string>

<!-- Photos access -->
<key>NSPhotoLibraryUsageDescription</key>
<string>This app accesses photos to...</string>
```

## Useful Commands

```bash
# View app entitlements
codesign -d --entitlements - /path/to/MyApp.app

# Check Gatekeeper status
spctl --assess --verbose /path/to/MyApp.app

# Clear Gatekeeper cache (for testing)
sudo spctl --master-disable  # Disable (testing only)
sudo spctl --master-enable   # Re-enable

# View crash logs
open ~/Library/Logs/DiagnosticReports/

# Reset app permissions (for testing)
tccutil reset All com.example.myapp
```
