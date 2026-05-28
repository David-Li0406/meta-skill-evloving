---
name: flutter-deployment
description: Comprehensive guide for deploying Flutter applications to all platforms including Android, iOS, web, and desktop. Covers build configuration, code signing, app store submission, CI/CD automation, and production best practices. Use when preparing for release or setting up deployment pipelines.
version: 1.0.0
---

# Flutter Deployment

## Description

Comprehensive guide for deploying Flutter applications to all platforms including mobile (Android, iOS), web, and desktop (Windows, macOS, Linux). Covers build configuration, code signing, app store submission, CI/CD automation, and production best practices.

## When to Use

Use this skill when:

- Preparing Flutter apps for release to production
- Configuring build flavors for different environments (dev, staging, production)
- Setting up code signing and certificates for iOS/Android
- Submitting apps to Google Play Store, Apple App Store, or Microsoft Store
- Deploying web apps with PWA capabilities
- Distributing desktop applications
- Implementing CI/CD pipelines with GitHub Actions, Codemagic, or fastlane
- Troubleshooting deployment issues or build failures
- Optimizing release builds for size and performance
- Managing version numbers and release cycles

## Core Deployment Concepts

### Build Modes

Flutter supports three compilation modes optimized for different stages:

**Debug Mode** - Active development with hot reload
- Assertions enabled for runtime validation
- Service extensions enabled (DevTools)
- Fast compilation, slower execution
- Default mode for `flutter run`
- Only mode supported on emulators/simulators

**Profile Mode** - Performance analysis
- Some debugging capabilities maintained
- Service extensions enabled for profiling
- Performance closer to release mode
- DevTools can connect for analysis
- Not supported on emulators/simulators

**Release Mode** - Production deployment
- Assertions disabled
- Debugging stripped
- Optimized for fast startup and small size
- Service extensions disabled
- Required for app store submission

```bash
flutter run                    # debug mode
flutter run --profile         # profile mode
flutter run --release         # release mode
flutter build <target>        # builds in release mode
```

### Platform Build Targets

Each platform has specific build commands and outputs:

```bash
# Mobile
flutter build apk             # Android APK
flutter build appbundle       # Android App Bundle (preferred)
flutter build ipa             # iOS App Store package

# Web
flutter build web             # Static web files

# Desktop
flutter build windows         # Windows executable
flutter build macos           # macOS application bundle
flutter build linux           # Linux executable
```

### Version Management

Version numbers follow semantic versioning with build numbers:

```yaml
# pubspec.yaml
version: 1.2.3+45
```

Format: `MAJOR.MINOR.PATCH+BUILD_NUMBER`

Override during build:
```bash
flutter build appbundle --build-name=1.2.3 --build-number=45
```

**Platform-specific considerations:**
- **Android:** `versionCode` must be unique integer for each upload
- **iOS:** Build number must be unique for each TestFlight/App Store upload
- **Windows:** Last revision number must be 0 (e.g., 1.2.3.0)

### Code Obfuscation

Protect Dart code by obscuring function and class names:

```bash
flutter build appbundle \
  --obfuscate \
  --split-debug-info=out/android
```

**Important notes:**
- Only works on release builds
- Save symbol files for crash report de-obfuscation
- May break reflection-based code
- Not supported for web (uses minification instead)

Use `flutter symbolize` to decode obfuscated stack traces:

```bash
flutter symbolize -i stack_trace.txt -d out/android
```

## Platform-Specific Deployment

### Android Deployment

**Prerequisites:**
- Google Play Developer account ($25 one-time fee)
- Upload keystore for app signing
- Configured `build.gradle` files

**Key steps:**
1. Create and configure signing keystore
2. Reference keystore in `key.properties`
3. Configure Gradle signing in `build.gradle.kts`
4. Build app bundle (preferred) or APK
5. Upload to Play Console
6. Complete store listing
7. Submit for review

**Recommended build:**
```bash
flutter build appbundle --release
```

Output: `build/app/outputs/bundle/release/app.aab`

### iOS Deployment

**Prerequisites:**
- Apple Developer Program membership ($99/year)
- Mac with Xcode installed
- Registered Bundle ID
- Code signing certificates and provisioning profiles

**Key steps:**
1. Register Bundle ID on Apple Developer portal
2. Create app record in App Store Connect
3. Configure Xcode project settings (signing, bundle ID)
4. Build release archive
5. Upload to App Store Connect
6. Optional: TestFlight beta testing
7. Submit for App Store review

**Build command:**
```bash
flutter build ipa --release
```

Output: `build/ios/ipa/*.ipa`

### Web Deployment

**Build command:**
```bash
flutter build web --release
```

Output: `build/web/` directory with static files

**Hosting options:**
- Firebase Hosting (recommended for Flutter)
- GitHub Pages
- Netlify
- Vercel
- Any static web hosting service

**PWA configuration:**
- Edit `web/manifest.json` for app metadata
- Customize `flutter_service_worker.js` for caching
- Serve over HTTPS (required for service workers)

### Desktop Deployment

**Windows:**
- Build MSIX package for Microsoft Store
- Or distribute standalone `.exe`
- Use `msix` pub package for packaging

```bash
flutter build windows --release
```

**macOS:**
- Submit to Mac App Store via App Store Connect
- Or notarize for distribution outside store
- Requires Apple Developer membership

```bash
flutter build macos --release
```

**Linux:**
- Snap Store (recommended)
- AppImage, deb, flatpak (via community tools)
- Requires snapcraft configuration

```bash
flutter build linux --release
```

## Build Flavors

Build flavors allow different configurations for development, staging, and production:

**Benefits:**
- Different app names and icons
- Separate API endpoints
- Environment-specific feature flags
- Multiple versions installed simultaneously

**Android configuration:**

```kotlin
// android/app/build.gradle.kts
android {
    flavorDimensions += "default"
    productFlavors {
        create("dev") {
            dimension = "default"
            applicationIdSuffix = ".dev"
            resValue("string", "app_name", "MyApp Dev")
        }
        create("staging") {
            dimension = "default"
            applicationIdSuffix = ".staging"
            resValue("string", "app_name", "MyApp Staging")
        }
        create("prod") {
            dimension = "default"
            resValue("string", "app_name", "MyApp")
        }
    }
}
```

**iOS configuration:**

Create schemes in Xcode for each flavor with different configurations and build settings.

**Running flavors:**
```bash
flutter run --flavor dev
flutter build appbundle --flavor prod
```

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Flutter App

on:
  push:
    branches: [ main ]

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'
      - run: flutter pub get
      - run: flutter test
      - run: flutter build appbundle --release
      - name: Upload to Play Store
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.SERVICE_ACCOUNT_JSON }}
          packageName: com.example.app
          releaseFiles: build/app/outputs/bundle/release/app.aab
          track: internal
```

### Codemagic

Configure via `codemagic.yaml` or web UI:

```yaml
workflows:
  ios-workflow:
    name: iOS Workflow
    environment:
      flutter: stable
      xcode: latest
    scripts:
      - flutter pub get
      - flutter test
      - flutter build ipa --release
    artifacts:
      - build/ios/ipa/*.ipa
    publishing:
      app_store_connect:
        api_key: $APP_STORE_CONNECT_PRIVATE_KEY
        submit_to_testflight: true
```

### fastlane

Install in both `android/` and `ios/` directories:

```bash
cd android && fastlane init
cd ios && fastlane init
```

**Android Fastfile:**
```ruby
lane :deploy do
  gradle(task: "clean bundleRelease")
  upload_to_play_store(
    track: 'internal',
    aab: '../build/app/outputs/bundle/release/app.aab'
  )
end
```

**iOS Fastfile:**
```ruby
lane :deploy do
  build_app(
    scheme: "Runner",
    export_method: "app-store"
  )
  upload_to_testflight
end
```

## Best Practices

### Pre-Release Checklist

- [ ] Update version number in `pubspec.yaml`
- [ ] Test on physical devices (all target platforms)
- [ ] Run in profile mode to verify performance
- [ ] Check app size and optimize if needed
- [ ] Verify all assets are included correctly
- [ ] Test deep linking and notifications
- [ ] Review permissions in manifests
- [ ] Update store listings and screenshots
- [ ] Test build with obfuscation enabled
- [ ] Verify signing configuration

### Security

- Never commit keystores, certificates, or API keys to version control
- Use environment variables for sensitive configuration
- Store credentials in CI/CD secret managers
- Enable code obfuscation for production builds
- Use HTTPS for all network requests
- Implement certificate pinning for sensitive apps
- Follow platform security guidelines

### Performance Optimization

- Use `--split-debug-info` to separate debug symbols
- Enable R8/ProGuard for Android (enabled by default)
- Optimize images and assets before bundling
- Use tree shaking to remove unused code
- Test startup time and runtime performance
- Monitor app size across releases
- Use `flutter build --analyze-size` for size analysis

### Version Control

- Tag releases in Git: `git tag v1.2.3`
- Maintain a CHANGELOG.md
- Use semantic versioning consistently
- Keep build numbers sequential and unique
- Document breaking changes

### Testing Before Release

```bash
# Build and test release builds locally
flutter build apk --release
flutter install

# Profile performance
flutter run --profile
flutter build apk --profile

# Check app size
flutter build apk --analyze-size
```

## Common Issues and Solutions

**Issue: Build fails with signing error (Android)**
- Verify `key.properties` file exists and is referenced
- Check keystore password is correct
- Ensure `storeFile` path is correct

**Issue: iOS build fails with provisioning profile error**
- Verify Bundle ID matches registered ID
- Check Apple Developer account has valid certificates
- Enable "Automatically manage signing" in Xcode
- Ensure device is registered for development

**Issue: App rejected from store**
- Review store policies and guidelines
- Ensure all required metadata is complete
- Check for missing privacy policy or terms
- Verify app meets minimum functionality requirements
- Address any crashes or performance issues

**Issue: Large app size**
- Use `--split-per-abi` for Android APKs
- Use app bundle instead of APK (Play Store handles ABIs)
- Compress images and assets
- Remove unused resources
- Enable obfuscation and tree shaking

**Issue: Obfuscated stack traces unreadable**
- Save `--split-debug-info` output directory
- Use `flutter symbolize` with saved symbols
- Keep symbols for each release version

## Quick Reference

### Essential Commands

```bash
# Build commands
flutter build apk --release                      # Android APK
flutter build appbundle --release                # Android bundle
flutter build ipa --release                      # iOS
flutter build web --release                      # Web
flutter build windows --release                  # Windows
flutter build macos --release                    # macOS
flutter build linux --release                    # Linux

# With obfuscation
flutter build appbundle --obfuscate --split-debug-info=out/

# With flavors
flutter build appbundle --flavor prod --release

# Version override
flutter build appbundle --build-name=1.2.3 --build-number=45

# Analyze size
flutter build apk --analyze-size
```

### Build Output Locations

```
Android APK:       build/app/outputs/apk/release/
Android Bundle:    build/app/outputs/bundle/release/
iOS:               build/ios/ipa/
Web:               build/web/
Windows:           build/windows/runner/Release/
macOS:             build/macos/Build/Products/Release/
Linux:             build/linux/<arch>/release/bundle/
```

## Related Skills

- **flutter-core**: Core Flutter concepts and architecture
- **flutter-state**: State management patterns
- **flutter-testing**: Testing strategies
- **flutter-performance**: Performance optimization

## Additional Resources

- [Flutter Deployment Documentation](https://docs.flutter.dev/deployment)
- [Android App Signing](https://developer.android.com/studio/publish/app-signing)
- [iOS App Distribution](https://developer.apple.com/distribute/)
- [Google Play Console](https://play.google.com/console)
- [App Store Connect](https://appstoreconnect.apple.com/)

For detailed platform-specific guidance, see the reference files in this skill.
