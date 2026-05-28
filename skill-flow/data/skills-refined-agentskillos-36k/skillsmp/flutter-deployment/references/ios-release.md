# iOS Release Deployment

Complete guide to building, code signing, and releasing Flutter apps to the Apple App Store.

## Overview

Releasing a Flutter app on iOS requires Apple Developer Program membership, code signing with certificates and provisioning profiles, building release archives with Xcode, and submitting to App Store Connect for review. The iOS release process is more complex than Android due to Apple's strict signing requirements and review guidelines.

## Prerequisites

### Required Accounts and Tools

- **Apple Developer Program membership** - $99 USD per year
- **Mac computer** - Required for iOS builds and code signing
- **Xcode** - Latest stable version (available from Mac App Store)
- **Flutter SDK** - Latest stable version recommended
- **Valid Apple ID** - Associated with Developer account

### Initial Setup

Verify your development environment:

```bash
flutter doctor -v
```

Ensure Xcode, CocoaPods, and iOS toolchain are properly configured.

### Apple Developer Account Setup

1. Visit [Apple Developer Program](https://developer.apple.com/programs/)
2. Enroll using your Apple ID
3. Complete identity verification (can take 24-48 hours)
4. Accept program agreements
5. Pay annual membership fee ($99 USD)

## Pre-Release Configuration

### 1. Register Bundle ID

The Bundle ID uniquely identifies your app across Apple's ecosystem.

**Steps:**
1. Go to [Apple Developer Portal → Identifiers](https://developer.apple.com/account/resources/identifiers/list)
2. Click **+** to register new identifier
3. Select **App IDs** and click **Continue**
4. Choose **App** type and click **Continue**
5. Enter details:
   - **Description:** Internal name for the Bundle ID
   - **Bundle ID:** Use explicit format (e.g., `com.example.myapp`)
   - **Capabilities:** Select services your app uses (Push Notifications, Sign in with Apple, etc.)
6. Click **Register**

**Bundle ID naming conventions:**
- Use reverse-domain notation: `com.company.appname`
- Cannot contain spaces or special characters except periods and hyphens
- Cannot be changed after App Store submission
- Case-insensitive but typically lowercase

### 2. Create App Store Connect Record

**Steps:**
1. Go to [App Store Connect](https://appstoreconnect.apple.com/)
2. Click **My Apps** → **+** → **New App**
3. Fill in app information:
   - **Platforms:** Select iOS (and iPadOS if applicable)
   - **Name:** App name (max 30 characters, must be unique)
   - **Primary Language:** Default language
   - **Bundle ID:** Select from registered Bundle IDs
   - **SKU:** Unique identifier for your app (internal use)
   - **User Access:** Full Access (default)
4. Click **Create**

### 3. Review Xcode Project Settings

Open your Flutter project's iOS workspace:

```bash
cd ios
open Runner.xcworkspace
```

**IMPORTANT:** Always open `.xcworkspace`, not `.xcodeproj`, when using CocoaPods.

**Verify settings in Xcode:**

**General Tab:**
- **Display Name** - User-visible app name
- **Bundle Identifier** - Must match registered Bundle ID
- **Version** - User-facing version (e.g., 1.0.0)
- **Build** - Build number (unique for each upload)
- **Deployment Info** - Minimum iOS version (Flutter requires iOS 13.0+)

**Signing & Capabilities Tab:**
- **Automatically manage signing** - Enabled (recommended for beginners)
- **Team** - Select your Apple Developer team
- **Signing Certificate** - Xcode manages automatically
- **Provisioning Profile** - Xcode manages automatically

**Build Settings Tab:**
- **iOS Deployment Target** - Minimum 13.0 for Flutter
- **Enable Bitcode** - No (deprecated, Flutter doesn't require it)

### 4. Configure App in Flutter Project

Update iOS configuration via `ios/Runner/Info.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>My App</string>

    <key>CFBundleName</key>
    <string>MyApp</string>

    <key>CFBundleShortVersionString</key>
    <string>$(FLUTTER_BUILD_NAME)</string>

    <key>CFBundleVersion</key>
    <string>$(FLUTTER_BUILD_NUMBER)</string>

    <key>LSRequiresIPhoneOS</key>
    <true/>

    <key>UILaunchStoryboardName</key>
    <string>LaunchScreen</string>

    <key>UIMainStoryboardFile</key>
    <string>Main</string>

    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>

    <!-- Add required usage descriptions -->
    <key>NSPhotoLibraryUsageDescription</key>
    <string>This app requires access to the photo library.</string>

    <key>NSCameraUsageDescription</key>
    <string>This app requires camera access.</string>

    <key>NSLocationWhenInUseUsageDescription</key>
    <string>This app requires location access.</string>
</dict>
</plist>
```

**CRITICAL:** Add usage descriptions for all permissions your app requests. Missing descriptions will cause App Store rejection.

### 5. Add App Icon

iOS requires app icons in specific sizes for different devices and contexts.

**Automated approach using flutter_launcher_icons:**

Add to `pubspec.yaml`:

```yaml
dev_dependencies:
  flutter_launcher_icons: ^0.13.1

flutter_launcher_icons:
  android: false
  ios: true
  image_path: "assets/icon/app_icon.png"
  remove_alpha_ios: true
```

Generate icons:

```bash
flutter pub get
flutter pub run flutter_launcher_icons
```

**Manual approach:**

In Xcode, select `ios/Runner/Assets.xcassets/AppIcon.appiconset` and drag icon files to appropriate slots.

**Required sizes:**
- iPhone App: 60x60pt @2x (120x120), @3x (180x180)
- iPad App: 76x76pt @2x (152x152)
- App Store: 1024x1024pt (no alpha channel)

**Icon guidelines:**
- No alpha transparency
- Square with no rounded corners (iOS adds corners automatically)
- Follow [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/app-icons)

### 6. Configure Launch Screen

Flutter generates a default launch screen. Customize in:
```
ios/Runner/Assets.xcassets/LaunchImage.imageset/
ios/Runner/Base.lproj/LaunchScreen.storyboard
```

**Best practices:**
- Keep launch screen simple
- Match your app's visual style
- Avoid text or content that requires localization
- Use solid colors or simple gradients

## Code Signing

### Understanding iOS Code Signing

iOS requires apps to be signed with cryptographic certificates to verify developer identity and ensure app integrity. Code signing involves:

1. **Certificates** - Identify the developer
2. **Provisioning Profiles** - Link certificates to devices and Bundle IDs
3. **Entitlements** - Define app capabilities (push notifications, iCloud, etc.)

### Code Signing Approaches

#### Option 1: Automatic Signing (Recommended for Beginners)

Xcode manages certificates and provisioning profiles automatically.

**Setup:**
1. Open `ios/Runner.xcworkspace` in Xcode
2. Select **Runner** project in navigator
3. Select **Runner** target
4. Navigate to **Signing & Capabilities** tab
5. Check **Automatically manage signing**
6. Select your **Team** from dropdown
7. Xcode downloads or creates necessary certificates and profiles

**Advantages:**
- Simplest approach
- Xcode handles renewals
- Good for solo developers or small teams

**Disadvantages:**
- Less control over signing assets
- Can have issues in CI/CD environments
- Multiple developers may create conflicting certificates

#### Option 2: Manual Signing (Recommended for Teams)

Manually create and manage certificates and provisioning profiles.

**Setup:**

**Step 1: Create Certificate Signing Request (CSR)**

1. Open **Keychain Access** on Mac
2. Menu: **Keychain Access** → **Certificate Assistant** → **Request a Certificate from a Certificate Authority**
3. Enter email address and common name
4. Select **Saved to disk**
5. Save CSR file

**Step 2: Create Distribution Certificate**

1. Go to [Apple Developer Portal → Certificates](https://developer.apple.com/account/resources/certificates/list)
2. Click **+** to create new certificate
3. Select **Apple Distribution** (for App Store)
4. Upload CSR file
5. Download certificate
6. Double-click to install in Keychain Access

**Step 3: Create Provisioning Profile**

1. Go to [Apple Developer Portal → Profiles](https://developer.apple.com/account/resources/profiles/list)
2. Click **+** to create new profile
3. Select **App Store** distribution
4. Select your Bundle ID
5. Select distribution certificate
6. Name the profile (e.g., "MyApp Production")
7. Download profile

**Step 4: Configure Xcode**

1. Open Xcode → **Settings** → **Accounts**
2. Select your Apple ID
3. View Developer Teams → Download Manual Profiles
4. In project settings, disable **Automatically manage signing**
5. Select provisioning profile for Release configuration

#### Option 3: Fastlane Match (Recommended for CI/CD)

Fastlane match synchronizes certificates and profiles across team via Git repo.

**Setup:**

```bash
cd ios
fastlane match init
```

Choose **git** storage and provide private repository URL.

Create certificates:

```bash
fastlane match appstore
```

This generates and stores certificates/profiles in Git repo, encrypted.

**Update Xcode:**
1. Disable automatic signing
2. Set provisioning profile to match profile: `match AppStore com.example.myapp`

### Managing Certificates and Profiles

**Certificate validity:**
- Distribution certificates: 1 year
- Development certificates: 1 year

**Profile validity:**
- Provisioning profiles: 1 year

**Important notes:**
- Only 2 distribution certificates allowed per account
- Renew before expiration to avoid build failures
- Revoking certificate invalidates all associated profiles
- Keep private keys secure (stored in Mac Keychain)

## Building Release Archive

### Option 1: Using Flutter CLI (Recommended)

Build IPA directly from command line:

```bash
flutter build ipa --release
```

**With obfuscation:**

```bash
flutter build ipa \
  --release \
  --obfuscate \
  --split-debug-info=build/ios/symbols
```

**Output locations:**
- `.xcarchive`: `build/ios/archive/Runner.xcarchive`
- `.ipa`: `build/ios/ipa/Runner.ipa`

### Option 2: Using Xcode

**Step 1: Build Flutter framework**

```bash
flutter build ios --release
```

**Step 2: Create archive in Xcode**

1. Open `ios/Runner.xcworkspace` in Xcode
2. Select **Any iOS Device** (or your device) as target
3. Verify **Release** configuration is selected
4. Menu: **Product** → **Archive**
5. Wait for archive to complete

**Step 3: Validate archive**

1. Archive organizer opens automatically
2. Select your archive
3. Click **Validate App**
4. Sign in with Apple ID if prompted
5. Review validation results
6. Fix any issues and re-archive if necessary

### Build Configuration Options

**For non-App Store distribution:**

```bash
# Ad hoc distribution
flutter build ipa --export-method ad-hoc

# Development distribution
flutter build ipa --export-method development

# Enterprise distribution
flutter build ipa --export-method enterprise
```

### Export Options Plist

For advanced control, create `ios/ExportOptions.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>

    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>

    <key>uploadBitcode</key>
    <false/>

    <key>uploadSymbols</key>
    <true/>

    <key>compileBitcode</key>
    <false/>

    <key>signingStyle</key>
    <string>automatic</string>

    <key>provisioningProfiles</key>
    <dict>
        <key>com.example.myapp</key>
        <string>MyApp Production</string>
    </dict>
</dict>
</plist>
```

Use with build command:

```bash
flutter build ipa --export-options-plist=ios/ExportOptions.plist
```

## Version Management

### Update Version in pubspec.yaml

```yaml
version: 1.2.3+45
```

Format: `BUILD_NAME+BUILD_NUMBER`
- `BUILD_NAME` (1.2.3) → `CFBundleShortVersionString`
- `BUILD_NUMBER` (45) → `CFBundleVersion`

### Override Version via Command Line

```bash
flutter build ipa \
  --build-name=1.2.3 \
  --build-number=45 \
  --release
```

### Version Requirements

- **CFBundleShortVersionString** - User-visible version (e.g., "1.2.3")
- **CFBundleVersion** - Build number, must be unique for each upload
- Build number can be integer or formatted string (1.2.3.45)
- Each TestFlight/App Store upload requires unique build number
- Cannot reuse build numbers, even after deletion

## Uploading to App Store Connect

### Option 1: Transporter App (Easiest)

1. Install [Transporter](https://apps.apple.com/app/transporter/id1450874784) from Mac App Store
2. Sign in with Apple ID
3. Drag and drop `.ipa` file from `build/ios/ipa/`
4. Click **Deliver**
5. Wait for upload to complete

### Option 2: Xcode Archive Organizer

1. In Xcode, open **Window** → **Organizer**
2. Select your archive
3. Click **Distribute App**
4. Choose distribution method: **App Store Connect**
5. Select **Upload**
6. Choose signing options (automatic recommended)
7. Review content and click **Upload**

### Option 3: Command Line (altool)

```bash
xcrun altool --upload-app \
  --type ios \
  --file build/ios/ipa/Runner.ipa \
  --apiKey YOUR_API_KEY \
  --apiIssuer YOUR_ISSUER_ID
```

**Generate API key:**
1. Go to App Store Connect → Users and Access → Keys
2. Click **+** to generate key
3. Download `.p8` key file
4. Note Key ID and Issuer ID

### Option 4: Fastlane

```bash
cd ios
fastlane deliver
```

Or create custom lane in `Fastfile`:

```ruby
lane :release do
  build_app(
    scheme: "Runner",
    export_method: "app-store",
    output_directory: "../build/ios/ipa"
  )
  upload_to_testflight(
    skip_waiting_for_build_processing: true
  )
end
```

Run with:

```bash
cd ios
fastlane release
```

### Upload Status

After upload:
- Processing typically takes 5-30 minutes
- You receive email when processing completes
- Build appears in App Store Connect → TestFlight tab
- Processing includes symbol upload and compatibility checks

## TestFlight Beta Testing

TestFlight allows beta testing before App Store release.

### Internal Testing

**Setup:**
1. Go to App Store Connect → TestFlight → Internal Testing
2. Select your build
3. Add internal testers (up to 100)
4. Internal testers must be added in Users and Access first
5. Testers receive email invitation
6. No review required, available immediately

**Advantages:**
- Fast distribution (no review)
- Up to 100 testers
- Testers can be team members or external
- Unlimited builds

### External Testing

**Setup:**
1. Go to App Store Connect → TestFlight → External Testing
2. Create new group or use existing
3. Add external testers (up to 10,000)
4. Submit for Beta App Review (required for first build)
5. Add test information and notes for reviewers
6. Review typically completes in 24-48 hours

**Requirements:**
- Beta App Review required
- Export compliance documentation
- Provide test account if app requires login

### Managing Test Builds

- Each build is available for 90 days
- Testers automatically get updated builds
- Can expire builds early if needed
- View crash reports and feedback from testers
- Monitor adoption metrics

## App Store Submission

### 1. Complete App Information

Navigate to App Store Connect → Your App → App Information:

**Required fields:**
- **Privacy Policy URL** - Required for all apps
- **App Category** - Primary and optional secondary category
- **Content Rights** - Copyright information
- **Age Rating** - Complete questionnaire
- **License Agreement** - Default or custom EULA

### 2. Complete Pricing and Availability

Navigate to Pricing and Availability:

- **Price** - Select price tier or free (cannot change free to paid later)
- **Availability** - All territories or specific countries
- **Pre-order** - Optional pre-order period
- **App distribution methods** - App Store, Custom Apps, etc.

### 3. Prepare App Store Screenshots

Required for all display sizes:

**iPhone:**
- 6.7" display (1290 x 2796 pixels) - Required
- 6.5" display (1284 x 2778 pixels) - Optional
- 5.5" display (1242 x 2208 pixels) - Optional

**iPad:**
- 12.9" display (2048 x 2732 pixels) - Required
- Can use same as 11" if App is Universal

**Screenshot tips:**
- Show actual app functionality
- Use high-quality images
- Include captions or annotations
- Localize for different markets
- Use tools like [Fastlane Frameit](https://fastlane.tools/frameit)

### 4. Prepare App Preview Videos (Optional)

- 15-30 seconds length
- Same orientations as screenshots
- Show actual app footage
- No third-party app content
- Optional but increases conversion

### 5. Complete Version Information

Navigate to App Store → iOS App → Version:

**App Store Information:**
- **Name** - Max 30 characters
- **Subtitle** - Max 30 characters (optional)
- **Promotional Text** - Max 170 characters (updateable without review)
- **Description** - Max 4000 characters
- **Keywords** - Max 100 characters, comma-separated
- **Support URL** - Required
- **Marketing URL** - Optional

**App Review Information:**
- **Contact information** - Phone and email
- **Notes** - Additional context for reviewers
- **Demo account** - If app requires login
- **Attachments** - Supporting documentation

**Version Release:**
- Automatic release after approval
- Manual release (you control timing)
- Scheduled release (specific date/time)

### 6. Select Build

1. Under **Build** section, click **Select a build before you submit your app**
2. Choose uploaded build from TestFlight
3. Wait for build to finish processing if needed
4. Provide export compliance information

### 7. Submit for Review

1. Review all information for completeness
2. Click **Add for Review** (or **Submit for Review** if all sections complete)
3. Confirm submission
4. App enters review queue

### App Review Process

**Typical timeline:**
- **In Review:** 24-48 hours (can be faster or slower)
- **Waiting for Review:** Varies based on volume
- **Processing:** After approval, 1-2 hours to appear on App Store

**Review statuses:**
- **Waiting for Review** - In queue
- **In Review** - Actively being reviewed
- **Pending Developer Release** - Approved, awaiting your release
- **Ready for Sale** - Live on App Store
- **Rejected** - Issues found, see Resolution Center

### Handling Rejections

If rejected:
1. Read rejection reason in Resolution Center
2. Review App Store Review Guidelines
3. Fix issues in code
4. Increment build number
5. Upload new build
6. Update version with new build
7. Respond to reviewer in Resolution Center
8. Resubmit for review

**Common rejection reasons:**
- Crashes or major bugs
- Missing privacy policy
- Incomplete functionality
- Misleading metadata or screenshots
- Using private APIs
- Poor user experience
- Missing required permissions explanations

## Post-Release Management

### Update Releases

To release an update:
1. Increment version in `pubspec.yaml`
2. Build new IPA with higher build number
3. Upload to App Store Connect
4. Create new version in App Store Connect
5. Add "What's New" release notes
6. Submit for review

### Phased Release

- Gradually release to percentage of users over 7 days
- Available for automatic updates only
- Can pause or complete early if needed
- Helps identify issues before full rollout

### Monitoring

Monitor app health in App Store Connect:

**Metrics:**
- Downloads and installs
- Crashes and energy reports
- Customer ratings and reviews
- App Store impressions and conversions

**Tools:**
- App Analytics (App Store Connect)
- Xcode Organizer (crashes)
- TestFlight feedback
- Customer reviews

## Common Issues and Solutions

### Code Signing Issues

**Problem:** "Provisioning profile doesn't include signing certificate"

**Solutions:**
- Verify certificate is installed in Keychain
- Regenerate provisioning profile to include certificate
- Check certificate hasn't expired
- Ensure correct team is selected

**Problem:** "No profiles for 'com.example.app' were found"

**Solutions:**
- Create provisioning profile with correct Bundle ID
- Download profiles in Xcode (Settings → Accounts → Download Manual Profiles)
- Enable automatic signing to let Xcode handle profiles

### Build Failures

**Problem:** "Command PhaseScriptExecution failed with a nonzero exit code"

**Solutions:**
- Run `flutter clean` and rebuild
- Delete `ios/Pods` and run `pod install`
- Check CocoaPods are up to date: `sudo gem install cocoapods`
- Review build logs for specific errors

**Problem:** "Undefined symbols for architecture arm64"

**Solutions:**
- Clean build folder in Xcode (Product → Clean Build Folder)
- Update CocoaPods: `cd ios && pod update`
- Check all dependencies support ARM64 architecture

### Upload Errors

**Problem:** "Asset validation failed: Invalid bundle"

**Solutions:**
- Verify Bundle ID matches registered ID exactly
- Check all required icons are present
- Ensure Info.plist is correctly formatted
- Validate archive in Xcode before uploading

**Problem:** "Missing compliance"

**Solutions:**
- Answer export compliance questions in App Store Connect
- Most apps use encryption (HTTPS) and require documentation
- Indicate if app qualifies for exemption

### App Store Rejection

**Problem:** Rejected for "Guideline 2.1 - Performance - App Completeness"

**Solutions:**
- Ensure all features work correctly
- Remove any placeholder content
- Test on physical devices
- Provide comprehensive test account

**Problem:** Rejected for "Guideline 5.1.1 - Legal - Privacy - Data Collection and Storage"

**Solutions:**
- Add privacy policy URL
- Describe data collection in App Store Connect
- Add required usage descriptions in Info.plist
- Implement privacy controls in app

## Best Practices

### Security

- Never commit certificates or private keys to version control
- Use Keychain for storing signing credentials
- Rotate API keys periodically
- Use fastlane match for team certificate management
- Enable two-factor authentication for Apple ID

### Build Process

- Automate builds with CI/CD (fastlane, GitHub Actions, Codemagic)
- Test on physical devices before submission
- Use TestFlight internal testing for QA
- Maintain consistent versioning scheme
- Tag releases in Git: `git tag v1.2.3`

### App Store Optimization

- Write clear, concise app description
- Use all 100 characters for keywords
- Include high-quality screenshots
- Add app preview video
- Localize for key markets
- Monitor and respond to reviews

### Release Management

- Use phased release for major updates
- Schedule releases during business hours
- Monitor crash reports immediately after release
- Prepare rollback plan for critical issues
- Communicate release to users via in-app messaging

### Testing

- Test on oldest supported iOS version
- Test on various device sizes (iPhone, iPad)
- Test in different localizations
- Test with poor network conditions
- Verify deep links and notifications
- Test app resume from background

## Advanced Topics

### App Store Connect API

Automate tasks using App Store Connect API:

```bash
# Generate API key in App Store Connect
# Use with xcrun altool or fastlane

xcrun altool --upload-app \
  --type ios \
  --file Runner.ipa \
  --apiKey YOUR_KEY \
  --apiIssuer YOUR_ISSUER
```

### Custom Product Pages

Create alternate app store pages for different user segments:
- Different screenshots
- Different promotional text
- Different app preview videos
- Track performance per page

### In-App Events

Promote timely events in your app:
- Visible on App Store
- Appears in search and editorial
- Drive engagement for limited-time content

### App Clips

Lightweight version of app for quick tasks:
- Max 10 MB uncompressed
- Fast, focused experiences
- Invoked via NFC, QR codes, or links

## Helpful Commands

```bash
# Build IPA
flutter build ipa --release

# Build with obfuscation
flutter build ipa --obfuscate --split-debug-info=symbols/

# Build for development
flutter build ipa --export-method development

# Build with custom version
flutter build ipa --build-name=1.2.3 --build-number=45

# Clean and rebuild
flutter clean && flutter pub get && flutter build ipa

# Run on connected device
flutter run --release

# Check CocoaPods
cd ios && pod install && pod update

# Fastlane commands
cd ios && fastlane match appstore
cd ios && fastlane release
```

## Resources

- [Apple App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [App Store Connect Help](https://help.apple.com/app-store-connect/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Flutter iOS Deployment](https://docs.flutter.dev/deployment/ios)
- [Code Signing Guide](https://developer.apple.com/support/code-signing/)
- [TestFlight Documentation](https://developer.apple.com/testflight/)

## Summary

iOS deployment requires careful attention to code signing, build configuration, and App Store guidelines. While more complex than Android, following this guide will help you successfully release Flutter apps on iOS. Remember to test thoroughly using TestFlight, maintain secure signing practices, and stay up-to-date with Apple's changing requirements and guidelines. The iOS review process is rigorous but ensures a high-quality user experience across the App Store.
