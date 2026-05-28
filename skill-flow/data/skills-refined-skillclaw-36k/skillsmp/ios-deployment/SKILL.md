---
name: ios-deployment
description: iOS deployment workflow for Flutter apps. Use when configuring Xcode projects, setting up code signing, creating provisioning profiles, submitting to TestFlight, or publishing to the App Store. Includes Fastlane automation and CI/CD integration for iOS builds.
---

# iOS Deployment

## Overview

Complete iOS deployment workflow for MagentaLine EFB, from development builds to App Store submission.

## Quick Start

### Build for Testing

```bash
# Debug build for simulator
flutter build ios --debug --simulator

# Release build for device
flutter build ios --release

# Archive for distribution
flutter build ipa --release
```

### Deploy to TestFlight

```bash
# With Fastlane (recommended)
cd ios && fastlane beta

# Manual upload
xcrun altool --upload-app -f build/ios/ipa/*.ipa \
  --type ios \
  --apiKey YOUR_API_KEY \
  --apiIssuer YOUR_ISSUER_ID
```

## Code Signing

### Automatic Signing (Development)

```ruby
# ios/Runner.xcodeproj - Automatically managed
DEVELOPMENT_TEAM = YOUR_TEAM_ID
CODE_SIGN_STYLE = Automatic
```

### Manual Signing (Distribution)

```ruby
# ios/Runner.xcodeproj
CODE_SIGN_STYLE = Manual
PROVISIONING_PROFILE_SPECIFIER = "MagentaLine AppStore"
CODE_SIGN_IDENTITY = "iPhone Distribution"
```

### Fastlane Match (Recommended for Teams)

```bash
# Setup (one time)
fastlane match init

# Download/create certificates
fastlane match development
fastlane match appstore
```

## Xcode Project Configuration

### Bundle Identifier

```
ios/Runner.xcodeproj/project.pbxproj
PRODUCT_BUNDLE_IDENTIFIER = com.magentaline.app
```

### Capabilities

Required capabilities for EFB:
- Background Modes (Location updates, Background fetch)
- Maps
- Push Notifications (optional)

```xml
<!-- ios/Runner/Runner.entitlements -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
  <key>com.apple.developer.networking.wifi-info</key>
  <true/>
  <key>com.apple.external-accessory.wireless-configuration</key>
  <true/>
</dict>
</plist>
```

### Info.plist Keys

```xml
<!-- Required for EFB location features -->
<key>NSLocationWhenInUseUsageDescription</key>
<string>MagentaLine needs location for moving map navigation</string>
<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>MagentaLine needs background location for flight tracking</string>
<key>UIBackgroundModes</key>
<array>
  <string>location</string>
  <string>fetch</string>
  <string>external-accessory</string>
</array>

<!-- Stratux WiFi connection -->
<key>NSLocalNetworkUsageDescription</key>
<string>MagentaLine connects to Stratux ADS-B receivers</string>
```

## Fastlane Setup

See `references/fastlane_config.md` for complete configuration.

### Fastfile

```ruby
# ios/fastlane/Fastfile
default_platform(:ios)

platform :ios do
  desc "Build and upload to TestFlight"
  lane :beta do
    setup_ci if ENV['CI']
    match(type: "appstore", readonly: true)

    build_app(
      workspace: "Runner.xcworkspace",
      scheme: "Runner",
      export_method: "app-store",
      output_directory: "../build/ios/ipa"
    )

    upload_to_testflight(
      skip_waiting_for_build_processing: true
    )
  end

  desc "Deploy to App Store"
  lane :release do
    build_app(
      workspace: "Runner.xcworkspace",
      scheme: "Runner",
      export_method: "app-store"
    )

    upload_to_app_store(
      force: true,
      skip_metadata: false,
      skip_screenshots: false
    )
  end
end
```

## Version Management

### Automatic Version Bumping

```bash
# Bump build number
cd ios && agvtool next-version -all

# Set marketing version
agvtool new-marketing-version 1.2.0

# Or use Flutter
flutter build ipa --build-number=42 --build-name=1.2.0
```

### pubspec.yaml

```yaml
version: 1.2.0+42  # version+build_number
```

## App Store Connect

### Required Assets

| Asset | Specs |
|-------|-------|
| App Icon | 1024x1024 PNG, no alpha |
| Screenshots | See `references/screenshots.md` |
| Privacy Policy | URL required |
| Support URL | Required |

### App Store Review Notes

For aviation apps, include:
- Test account credentials (if applicable)
- Device requirements (iPad recommended for EFB)
- Note about Stratux/ADS-B if using external devices

## CI/CD Integration

```yaml
# .github/workflows/ios.yml
jobs:
  ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2

      - name: Install CocoaPods
        run: cd ios && pod install

      - name: Setup signing
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
        run: cd ios && fastlane match appstore --readonly

      - name: Build IPA
        run: flutter build ipa --release

      - name: Upload to TestFlight
        env:
          APP_STORE_CONNECT_API_KEY: ${{ secrets.ASC_KEY }}
        run: cd ios && fastlane beta
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Signing failed | Check team ID and provisioning profile |
| CocoaPods error | `cd ios && pod deintegrate && pod install` |
| Archive failed | Clean build folder, check Xcode version |
| Upload rejected | Check bundle ID, version, build number |

### Clean Build

```bash
flutter clean
cd ios && rm -rf Pods Podfile.lock
cd ios && pod install
flutter build ios --release
```

## References

| Document | Description |
|----------|-------------|
| `references/fastlane_config.md` | Complete Fastlane setup |
| `references/screenshots.md` | App Store screenshot specs |
| `references/certificates.md` | Signing certificate guide |
| `assets/Fastfile` | Ready-to-use Fastfile |
