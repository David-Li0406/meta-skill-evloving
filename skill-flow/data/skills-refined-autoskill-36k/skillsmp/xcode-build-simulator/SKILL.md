---
name: Xcode Build & Simulator
description: Complete iOS/macOS/watchOS/tvOS development using native xcodebuild, xcrun simctl, and xcrun devicectl commands. Build, run, test apps on simulators and physical devices. UI automation, screenshots, video capture, log capture, Swift Package Manager. No MCP server required.
version: 2.0.0
---

# Xcode Build & Simulator Skill

## Overview

This skill provides comprehensive guidance for Apple platform development using native CLI tools:
- **xcodebuild** - Build, test, and archive Xcode projects
- **xcrun simctl** - Manage iOS/watchOS/tvOS simulators
- **xcrun devicectl** - Manage physical Apple devices
- **swift** - Swift Package Manager operations

## Project Discovery

### Find Projects & Workspaces
```bash
# Find all Xcode projects
find . -name "*.xcodeproj" -type d 2>/dev/null

# Find all workspaces
find . -name "*.xcworkspace" -type d 2>/dev/null

# Find Swift packages
find . -name "Package.swift" -type f 2>/dev/null
```

### List Schemes & Build Settings
```bash
# List schemes in a project
xcodebuild -list -project MyApp.xcodeproj

# List schemes in a workspace
xcodebuild -list -workspace MyApp.xcworkspace

# Show build settings
xcodebuild -workspace MyApp.xcworkspace -scheme MyApp -showBuildSettings

# Show specific build setting
xcodebuild -workspace MyApp.xcworkspace -scheme MyApp -showBuildSettings | grep PRODUCT_BUNDLE_IDENTIFIER
```

### Extract Bundle Identifier
```bash
# From built .app bundle
defaults read /path/to/MyApp.app/Info.plist CFBundleIdentifier

# Using plutil (more reliable)
plutil -extract CFBundleIdentifier raw /path/to/MyApp.app/Info.plist

# From project build settings
xcodebuild -workspace MyApp.xcworkspace -scheme MyApp -showBuildSettings | grep PRODUCT_BUNDLE_IDENTIFIER | awk '{print $3}'
```

---

## Simulator Management

### List Simulators
```bash
# List all simulators
xcrun simctl list devices

# List available (can be booted) simulators
xcrun simctl list devices available

# List only booted simulators
xcrun simctl list devices booted

# JSON output for parsing
xcrun simctl list devices -j

# List device types
xcrun simctl list devicetypes

# List available runtimes (iOS versions)
xcrun simctl list runtimes
```

### Boot & Open Simulators
```bash
# Boot simulator by UDID
xcrun simctl boot <UDID>

# Boot by device name
xcrun simctl boot "iPhone 15 Pro"

# Open Simulator.app (GUI)
open -a Simulator

# Open specific simulator in GUI
open -a Simulator --args -CurrentDeviceUDID <UDID>

# Shutdown simulator
xcrun simctl shutdown <UDID>
xcrun simctl shutdown booted
xcrun simctl shutdown all
```

### Erase & Delete Simulators
```bash
# Erase content and settings (keeps simulator)
xcrun simctl erase <UDID>
xcrun simctl erase all

# Delete simulator entirely
xcrun simctl delete <UDID>
xcrun simctl delete unavailable  # Remove unavailable simulators
```

### Simulator Appearance & Settings
```bash
# Set dark/light mode
xcrun simctl ui booted appearance dark
xcrun simctl ui booted appearance light

# Set content size (accessibility)
xcrun simctl ui booted content_size extra-small
xcrun simctl ui booted content_size small
xcrun simctl ui booted content_size medium
xcrun simctl ui booted content_size large
xcrun simctl ui booted content_size extra-large
xcrun simctl ui booted content_size extra-extra-large
xcrun simctl ui booted content_size extra-extra-extra-large
xcrun simctl ui booted content_size accessibility-medium
xcrun simctl ui booted content_size accessibility-large
xcrun simctl ui booted content_size accessibility-extra-large
```

### Location Simulation
```bash
# Set GPS location (latitude,longitude)
xcrun simctl location booted set 37.7749,-122.4194

# Set location by name (uses Apple Maps geocoding)
xcrun simctl location booted set "San Francisco, CA"

# Clear/reset location
xcrun simctl location booted clear

# Run GPX route simulation
xcrun simctl location booted start route.gpx

# Stop route simulation
xcrun simctl location booted stop
```

### Status Bar Override (for screenshots)
```bash
# Override status bar appearance
xcrun simctl status_bar booted override \
  --time "9:41" \
  --batteryState charged \
  --batteryLevel 100 \
  --cellularMode active \
  --cellularBars 4 \
  --wifiBars 3 \
  --operatorName "Carrier"

# Clear all status bar overrides
xcrun simctl status_bar booted clear
```

---

## Building for Simulator

### Build Commands
```bash
# Build for iOS Simulator
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -sdk iphonesimulator \
  -configuration Debug \
  build

# Build for specific simulator destination
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro' \
  build

# Build with custom derived data path
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -sdk iphonesimulator \
  -derivedDataPath ./build \
  build

# Clean and build
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  clean build

# Build without code signing (simulator)
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -sdk iphonesimulator \
  CODE_SIGN_IDENTITY="" \
  CODE_SIGNING_REQUIRED=NO \
  build
```

### Find Built App Path
```bash
# From default DerivedData
find ~/Library/Developer/Xcode/DerivedData -name "MyApp.app" -path "*/Debug-iphonesimulator/*" -type d | head -1

# From custom derived data path
find ./build -name "*.app" -type d | head -1

# Get app path from build output
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -sdk iphonesimulator \
  -showBuildSettings | grep -m1 "BUILT_PRODUCTS_DIR" | awk '{print $3}'
```

### Install & Launch on Simulator
```bash
# Install app
xcrun simctl install booted /path/to/MyApp.app

# Launch app (returns immediately)
xcrun simctl launch booted com.yourcompany.MyApp

# Launch and wait for app to exit
xcrun simctl launch --console booted com.yourcompany.MyApp

# Launch with arguments
xcrun simctl launch booted com.yourcompany.MyApp --arg1 value1

# Launch with environment variables
xcrun simctl launch booted com.yourcompany.MyApp MYENV=value

# Terminate app
xcrun simctl terminate booted com.yourcompany.MyApp

# Uninstall app
xcrun simctl uninstall booted com.yourcompany.MyApp
```

### Build & Run Combined Workflow
```bash
# Complete build-install-launch workflow
WORKSPACE="MyApp.xcworkspace"
SCHEME="MyApp"
BUNDLE_ID="com.yourcompany.MyApp"
SIMULATOR="iPhone 15 Pro"

# Boot simulator
xcrun simctl boot "$SIMULATOR" 2>/dev/null || true

# Build
xcodebuild -workspace "$WORKSPACE" \
  -scheme "$SCHEME" \
  -sdk iphonesimulator \
  -derivedDataPath ./build \
  build

# Find and install app
APP_PATH=$(find ./build -name "*.app" -path "*Debug-iphonesimulator*" -type d | head -1)
xcrun simctl install booted "$APP_PATH"

# Launch
xcrun simctl launch booted "$BUNDLE_ID"
```

---

## Physical Device Development

### List Connected Devices
```bash
# Using devicectl (iOS 17+, recommended)
xcrun devicectl list devices

# Using instruments (legacy)
xcrun xctrace list devices

# Using system_profiler
system_profiler SPUSBDataType | grep -A 11 "iPhone\|iPad"
```

### Build for Device
```bash
# Build for iOS device
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -sdk iphoneos \
  -configuration Debug \
  build

# Build for specific device
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -destination 'platform=iOS,id=<DEVICE_UDID>' \
  build

# Build and export for ad-hoc distribution
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -sdk iphoneos \
  -configuration Release \
  -archivePath ./build/MyApp.xcarchive \
  archive
```

### Install & Launch on Device (devicectl - iOS 17+)
```bash
# Install app on device
xcrun devicectl device install app --device <DEVICE_UDID> /path/to/MyApp.app

# Launch app on device
xcrun devicectl device process launch --device <DEVICE_UDID> com.yourcompany.MyApp

# Terminate app on device
xcrun devicectl device process terminate --device <DEVICE_UDID> com.yourcompany.MyApp
```

### Device Log Capture
```bash
# Stream device logs (devicectl)
xcrun devicectl device log stream --device <DEVICE_UDID>

# Stream with process filter
xcrun devicectl device log stream --device <DEVICE_UDID> --process MyApp

# Capture syslog (legacy)
idevicesyslog -u <DEVICE_UDID>
```

---

## macOS Development

### Build macOS App
```bash
# Build for macOS
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -sdk macosx \
  -configuration Debug \
  build

# Build for specific macOS version
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -destination 'platform=macOS' \
  build
```

### Find Built macOS App
```bash
# Find app bundle
find ~/Library/Developer/Xcode/DerivedData -name "MyApp.app" -path "*/Debug/*" -type d | head -1
```

### Launch & Stop macOS App
```bash
# Launch macOS app
open /path/to/MyApp.app

# Launch with arguments
open /path/to/MyApp.app --args --arg1 value1

# Stop macOS app by name
killall "MyApp"

# Stop by process ID
kill $(pgrep -f "MyApp")

# Or using osascript
osascript -e 'quit app "MyApp"'
```

### Test macOS App
```bash
xcodebuild test \
  -workspace MyApp.xcworkspace \
  -scheme MyAppTests \
  -destination 'platform=macOS'
```

---

## Testing

### Run Tests on Simulator
```bash
# Run all tests
xcodebuild test \
  -workspace MyApp.xcworkspace \
  -scheme MyAppTests \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro'

# Run with result bundle
xcodebuild test \
  -workspace MyApp.xcworkspace \
  -scheme MyAppTests \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro' \
  -resultBundlePath ./TestResults.xcresult

# Run specific test class
xcodebuild test \
  -workspace MyApp.xcworkspace \
  -scheme MyAppTests \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro' \
  -only-testing:MyAppTests/MyTestClass

# Run specific test method
xcodebuild test \
  -workspace MyApp.xcworkspace \
  -scheme MyAppTests \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro' \
  -only-testing:MyAppTests/MyTestClass/testSpecificMethod

# Skip specific tests
xcodebuild test \
  -workspace MyApp.xcworkspace \
  -scheme MyAppTests \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro' \
  -skip-testing:MyAppTests/SlowTests
```

### Run Tests on Device
```bash
xcodebuild test \
  -workspace MyApp.xcworkspace \
  -scheme MyAppTests \
  -destination 'platform=iOS,id=<DEVICE_UDID>'
```

### UI Tests
```bash
xcodebuild test \
  -workspace MyApp.xcworkspace \
  -scheme MyAppUITests \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro'
```

---

## Swift Package Manager

### Build Package
```bash
# Build package (debug)
swift build

# Build release
swift build -c release

# Build with verbose output
swift build -v

# Build specific target
swift build --target MyTarget

# Build for specific platform
swift build --triple arm64-apple-ios-simulator
```

### Run Package Executable
```bash
# Run executable target
swift run MyExecutable

# Run with arguments
swift run MyExecutable --arg1 value1

# Run release build
swift run -c release MyExecutable
```

### Test Package
```bash
# Run all tests
swift test

# Run specific test
swift test --filter MyTestClass

# Run tests in parallel
swift test --parallel

# Generate code coverage
swift test --enable-code-coverage
```

### Clean Package
```bash
# Clean build artifacts
swift package clean

# Reset package completely
swift package reset

# Update dependencies
swift package update

# Resolve dependencies
swift package resolve
```

### Package Management
```bash
# Show dependencies
swift package show-dependencies

# Generate Xcode project
swift package generate-xcodeproj

# Dump package description
swift package dump-package
```

---

## Screenshots & Video Capture

### Screenshots
```bash
# Take screenshot of booted simulator
xcrun simctl io booted screenshot screenshot.png

# Screenshot specific simulator
xcrun simctl io <UDID> screenshot screenshot.png

# Screenshot with device mask (frame)
xcrun simctl io booted screenshot --mask black screenshot.png
xcrun simctl io booted screenshot --mask ignored screenshot.png

# Screenshot to stdout (for piping)
xcrun simctl io booted screenshot -
```

### Video Recording
```bash
# Start recording (runs until Ctrl+C)
xcrun simctl io booted recordVideo video.mp4

# Record with codec
xcrun simctl io booted recordVideo --codec h264 video.mp4

# Record with mask
xcrun simctl io booted recordVideo --mask black video.mp4

# Background recording workflow
xcrun simctl io booted recordVideo video.mp4 &
VIDEO_PID=$!
# ... perform test actions ...
kill -INT $VIDEO_PID  # Stop recording gracefully
```

---

## UI Automation

### UI Element Discovery (describe_ui equivalent)
```bash
# Get accessibility hierarchy using Accessibility Inspector CLI
# First, enable in System Preferences > Privacy & Security > Accessibility

# Use XCUITest for programmatic access, or:

# Get window list
osascript -e 'tell application "System Events" to get every window of application process "Simulator"'

# Open Accessibility Inspector for visual inspection
open -a "Accessibility Inspector"
```

### Tap at Coordinates
```bash
# Using AppleScript (requires Accessibility permissions)
osascript -e '
tell application "Simulator" to activate
delay 0.3
tell application "System Events"
    click at {200, 400}
end tell
'

# Tap with specific window
osascript -e '
tell application "System Events"
    tell process "Simulator"
        click at {200, 400} of window 1
    end tell
end tell
'
```

### Long Press
```bash
osascript -e '
tell application "Simulator" to activate
delay 0.2
tell application "System Events"
    -- Click and hold for 1 second
    set mousePos to {200, 400}
    click at mousePos
    delay 1.0
end tell
'
```

### Swipe Gestures
```bash
# Swipe up (scroll down)
osascript -e '
tell application "Simulator" to activate
tell application "System Events"
    tell process "Simulator"
        set frontWindow to window 1
        -- Perform swipe from bottom to top
        click at {200, 600} of frontWindow
        delay 0.05
        -- Note: For true swipes, use XCUITest or simctl gestures
    end tell
end tell
'
```

### Keyboard Input (Type Text)
```bash
# Type text in focused field
osascript -e '
tell application "Simulator" to activate
delay 0.2
tell application "System Events"
    keystroke "Hello World"
end tell
'

# Type with special keys
osascript -e '
tell application "System Events"
    keystroke "a" using command down  -- Cmd+A (select all)
    keystroke return                   -- Press Enter
    keystroke tab                      -- Press Tab
    key code 51                        -- Delete/Backspace
end tell
'
```

### Hardware Button Simulation
```bash
# Home button
osascript -e '
tell application "System Events"
    tell process "Simulator"
        click menu item "Home" of menu "Device" of menu bar 1
    end tell
end tell
'

# Lock screen
osascript -e '
tell application "System Events"
    tell process "Simulator"
        click menu item "Lock Screen" of menu "Device" of menu bar 1
    end tell
end tell
'

# Shake gesture
osascript -e '
tell application "System Events"
    tell process "Simulator"
        click menu item "Shake" of menu "Device" of menu bar 1
    end tell
end tell
'

# Rotate device
osascript -e '
tell application "System Events"
    tell process "Simulator"
        click menu item "Rotate Left" of menu "Device" of menu bar 1
    end tell
end tell
'
```

### Open URL / Deep Links
```bash
# Open URL in simulator
xcrun simctl openurl booted "https://example.com"

# Open custom URL scheme (deep link)
xcrun simctl openurl booted "myapp://path/to/screen?param=value"

# Open universal link
xcrun simctl openurl booted "https://myapp.com/deeplink"
```

---

## Log Capture

### Simulator Logs
```bash
# Stream all logs
xcrun simctl spawn booted log stream

# Stream with process filter
xcrun simctl spawn booted log stream --predicate 'processImagePath contains "MyApp"'

# Stream specific log levels
xcrun simctl spawn booted log stream --level debug
xcrun simctl spawn booted log stream --level info
xcrun simctl spawn booted log stream --level error

# Stream with subsystem filter
xcrun simctl spawn booted log stream --predicate 'subsystem == "com.yourcompany.MyApp"'

# Save logs to file
xcrun simctl spawn booted log stream --predicate 'processImagePath contains "MyApp"' > app.log &
LOG_PID=$!
# ... run tests ...
kill $LOG_PID
```

### Collect Log Archive
```bash
# Collect logs to archive
xcrun simctl spawn booted log collect --output logs.logarchive

# Show logs from archive
log show logs.logarchive

# Filter archived logs
log show logs.logarchive --predicate 'processImagePath contains "MyApp"'
log show logs.logarchive --last 5m  # Last 5 minutes
```

### App Container & Data
```bash
# Get app container paths
xcrun simctl get_app_container booted com.yourcompany.MyApp        # Bundle container
xcrun simctl get_app_container booted com.yourcompany.MyApp data   # Data container
xcrun simctl get_app_container booted com.yourcompany.MyApp groups # App groups

# List app container contents
APP_DATA=$(xcrun simctl get_app_container booted com.yourcompany.MyApp data)
ls -la "$APP_DATA/Documents/"
ls -la "$APP_DATA/Library/Caches/"
```

---

## Push Notifications

```bash
# Create notification payload file
cat > notification.apns << 'EOF'
{
  "aps": {
    "alert": {
      "title": "Test Notification",
      "body": "This is a test push notification"
    },
    "badge": 1,
    "sound": "default"
  },
  "customKey": "customValue"
}
EOF

# Send push notification
xcrun simctl push booted com.yourcompany.MyApp notification.apns

# Send inline push (no file needed)
echo '{"aps":{"alert":"Quick test"}}' | xcrun simctl push booted com.yourcompany.MyApp -
```

---

## Privacy & Permissions

```bash
# Grant permissions
xcrun simctl privacy booted grant photos com.yourcompany.MyApp
xcrun simctl privacy booted grant camera com.yourcompany.MyApp
xcrun simctl privacy booted grant microphone com.yourcompany.MyApp
xcrun simctl privacy booted grant contacts com.yourcompany.MyApp
xcrun simctl privacy booted grant calendar com.yourcompany.MyApp
xcrun simctl privacy booted grant reminders com.yourcompany.MyApp
xcrun simctl privacy booted grant location-always com.yourcompany.MyApp
xcrun simctl privacy booted grant location com.yourcompany.MyApp

# Revoke permissions
xcrun simctl privacy booted revoke photos com.yourcompany.MyApp
xcrun simctl privacy booted revoke all com.yourcompany.MyApp

# Reset permissions (ask again)
xcrun simctl privacy booted reset photos com.yourcompany.MyApp
xcrun simctl privacy booted reset all com.yourcompany.MyApp
```

---

## Clean Operations

```bash
# Clean build products
xcodebuild -workspace MyApp.xcworkspace -scheme MyApp clean

# Clean derived data for project
rm -rf ~/Library/Developer/Xcode/DerivedData/MyApp-*

# Clean all derived data
rm -rf ~/Library/Developer/Xcode/DerivedData/*

# Clean module cache
rm -rf ~/Library/Developer/Xcode/DerivedData/ModuleCache.noindex

# Clean Xcode caches
rm -rf ~/Library/Caches/com.apple.dt.Xcode
```

---

## Common Workflows

### Complete iOS Simulator Workflow
```bash
#!/bin/bash
WORKSPACE="MyApp.xcworkspace"
SCHEME="MyApp"
BUNDLE_ID="com.yourcompany.MyApp"
SIMULATOR="iPhone 15 Pro"

# 1. Boot simulator
xcrun simctl boot "$SIMULATOR" 2>/dev/null || true
open -a Simulator

# 2. Build
xcodebuild -workspace "$WORKSPACE" \
  -scheme "$SCHEME" \
  -sdk iphonesimulator \
  -derivedDataPath ./build \
  build || exit 1

# 3. Find and install
APP_PATH=$(find ./build -name "*.app" -path "*Debug-iphonesimulator*" -type d | head -1)
xcrun simctl install booted "$APP_PATH"

# 4. Launch with log capture
xcrun simctl spawn booted log stream --predicate "processImagePath contains \"$SCHEME\"" > app.log &
LOG_PID=$!
xcrun simctl launch booted "$BUNDLE_ID"

# 5. Take screenshot after delay
sleep 3
xcrun simctl io booted screenshot screenshot.png

# 6. Stop logging
kill $LOG_PID 2>/dev/null
```

### Debug Session
```bash
# Start log capture
xcrun simctl spawn booted log stream --predicate 'processImagePath contains "MyApp"' | tee app.log &
LOG_PID=$!

# Launch app
xcrun simctl launch booted com.yourcompany.MyApp

# ... interact with app ...

# Stop and review
kill $LOG_PID
less app.log
```

### Screenshot Automation
```bash
# Override status bar for clean screenshots
xcrun simctl status_bar booted override --time "9:41" --batteryState charged --batteryLevel 100

# Take screenshots
for device in "iPhone 15 Pro" "iPhone 15 Pro Max" "iPad Pro (12.9-inch)"; do
    xcrun simctl boot "$device" 2>/dev/null || true
    sleep 2
    xcrun simctl io booted screenshot "screenshot_${device// /_}.png"
    xcrun simctl shutdown "$device"
done

# Clear status bar override
xcrun simctl status_bar booted clear
```

---

## Troubleshooting

### Build Failures
```bash
# Show detailed build log
xcodebuild -workspace MyApp.xcworkspace -scheme MyApp build 2>&1 | tee build.log

# Show build settings
xcodebuild -workspace MyApp.xcworkspace -scheme MyApp -showBuildSettings

# Clean and rebuild
xcodebuild -workspace MyApp.xcworkspace -scheme MyApp clean build
```

### Simulator Issues
```bash
# Restart CoreSimulator service
sudo killall -9 com.apple.CoreSimulator.CoreSimulatorService

# Reset all simulators
xcrun simctl shutdown all
xcrun simctl erase all

# Kill Simulator app
killall "Simulator"

# Check simulator status
xcrun simctl list devices booted
```

### Code Signing
```bash
# List signing identities
security find-identity -v -p codesigning

# List provisioning profiles
ls -la ~/Library/MobileDevice/Provisioning\ Profiles/

# Decode provisioning profile
security cms -D -i ~/Library/MobileDevice/Provisioning\ Profiles/<UUID>.mobileprovision
```

### Device Connection Issues
```bash
# List USB devices
system_profiler SPUSBDataType

# Trust device (must be done on device)
# Disconnect and reconnect device, tap "Trust" on device

# Check device pairing
xcrun devicectl list devices
```

---

## Environment Info (Doctor)

```bash
# Xcode version
xcodebuild -version

# Available SDKs
xcodebuild -showsdks

# Xcode path
xcode-select -p

# Switch Xcode version
sudo xcode-select -s /Applications/Xcode.app

# Swift version
swift --version

# macOS version
sw_vers

# Available simulators summary
xcrun simctl list --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Devices: {sum(len(v) for v in d[\"devices\"].values())}')"
```

---

## Resources

- [xcodebuild Man Page](https://keith.github.io/xcode-man-pages/xcodebuild.1.html)
- [simctl Reference](https://nshipster.com/simctl/)
- [devicectl Documentation](https://developer.apple.com/documentation/devicemanagement)
- [Swift Package Manager](https://swift.org/package-manager/)
- [Apple Testing Documentation](https://developer.apple.com/documentation/xctest)
