---
name: ios-build-deploy
description: Build and deploy iOS app to simulator or device. Use when testing iOS changes, debugging on simulator, or running the app after code changes. Handles Xcode builds, app installation, and launching.
allowed-tools: Read, Bash
---

# iOS Build & Deploy

## Purpose
Quickly build the iOS app and deploy to simulator or connected device for testing.

## Prerequisites Check

Before building, verify environment:

```bash
# List available simulators
xcrun simctl list devices available

# Check if Xcode command line tools installed
xcode-select -p

# Check connected physical devices
xcrun xctrace list devices
```

## Build Commands

### Quick Compile (Check for Errors)
```bash
cd apps/ios/ConstructionPro
xcodebuild -scheme ConstructionPro -configuration Debug -destination 'platform=iOS Simulator,name=iPhone 15' build 2>&1 | head -50
```

### Build for Simulator
```bash
cd apps/ios/ConstructionPro
xcodebuild -scheme ConstructionPro \
  -configuration Debug \
  -destination 'platform=iOS Simulator,name=iPhone 15' \
  -derivedDataPath build \
  build
```

### Build for Device
```bash
cd apps/ios/ConstructionPro
xcodebuild -scheme ConstructionPro \
  -configuration Debug \
  -destination 'generic/platform=iOS' \
  build
```

## Deploy to Simulator

### Boot Simulator
```bash
# List available simulators
xcrun simctl list devices available | grep iPhone

# Boot specific simulator
xcrun simctl boot "iPhone 15"

# Open Simulator app
open -a Simulator
```

### Install App on Simulator
```bash
# Find the built app
APP_PATH=$(find apps/ios/ConstructionPro/build -name "*.app" -type d | head -1)

# Install to booted simulator
xcrun simctl install booted "$APP_PATH"
```

### Launch App
```bash
xcrun simctl launch booted com.constructionpro.app
```

### Combined: Build, Install, Launch
```bash
cd apps/ios/ConstructionPro && \
xcodebuild -scheme ConstructionPro \
  -configuration Debug \
  -destination 'platform=iOS Simulator,name=iPhone 15' \
  -derivedDataPath build \
  build && \
xcrun simctl install booted build/Build/Products/Debug-iphonesimulator/ConstructionPro.app && \
xcrun simctl launch booted com.constructionpro.app
```

## Debugging

### View Logs (Filtered to App)
```bash
xcrun simctl spawn booted log stream --predicate 'subsystem == "com.constructionpro.app"'
```

### View Recent Console Output
```bash
xcrun simctl spawn booted log show --last 5m --predicate 'subsystem == "com.constructionpro.app"'
```

### Take Simulator Screenshot
```bash
xcrun simctl io booted screenshot screenshot.png
```

## Common Issues

### Simulator Not Found
```bash
# Reset simulator list
xcrun simctl shutdown all
xcrun simctl erase all

# Create new simulator if needed
xcrun simctl create "iPhone 15" "com.apple.CoreSimulator.SimDeviceType.iPhone-15"
```

### Build Cache Issues
```bash
cd apps/ios/ConstructionPro
rm -rf build
rm -rf ~/Library/Developer/Xcode/DerivedData/ConstructionPro-*
xcodebuild clean -scheme ConstructionPro
```

### Code Signing Issues (Device Only)
```bash
# Check signing identity
security find-identity -v -p codesigning

# Build with automatic signing
xcodebuild -scheme ConstructionPro \
  -configuration Debug \
  -allowProvisioningUpdates \
  build
```

### Swift Compile Errors
Check specific errors:
```bash
xcodebuild -scheme ConstructionPro build 2>&1 | grep -A 3 "error:"
```

## Quick Reference

| Task | Command |
|------|---------|
| List simulators | `xcrun simctl list devices available` |
| Boot simulator | `xcrun simctl boot "iPhone 15"` |
| Build for sim | `xcodebuild -scheme ConstructionPro -destination 'platform=iOS Simulator,name=iPhone 15' build` |
| Install app | `xcrun simctl install booted <app_path>` |
| Launch app | `xcrun simctl launch booted com.constructionpro.app` |
| View logs | `xcrun simctl spawn booted log stream` |
| Clean build | `xcodebuild clean -scheme ConstructionPro` |

## Project Paths

- **Root**: `apps/ios/ConstructionPro/`
- **Source**: `apps/ios/ConstructionPro/ConstructionPro/`
- **Models**: `apps/ios/ConstructionPro/ConstructionPro/Models/`
- **Views**: `apps/ios/ConstructionPro/ConstructionPro/Views/`
- **Services**: `apps/ios/ConstructionPro/ConstructionPro/Services/`
- **Build Output**: `apps/ios/ConstructionPro/build/`
