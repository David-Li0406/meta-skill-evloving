---
name: build
description: Build and run the Guidr React Native application on Metro, Android, and iOS platforms. Includes development commands, debug/release builds, common troubleshooting, and CI/CD workflows.
---

# Build Skill

Build and run the Guidr React Native application.

## Development Commands

### Start Metro Bundler
```bash
npm start
```
Starts the Metro bundler. Keep this running while developing.

### Run on Android
```bash
npm run android
```
Builds and runs the app on connected Android device or emulator.

**Requirements**:
- Android device connected via USB (with USB debugging enabled)
- OR Android emulator running
- Android SDK installed
- JDK 17 installed

### Run on iOS (macOS only)
```bash
npm run ios
```
Builds and runs the app on iOS simulator or device.

**Requirements**:
- macOS
- Xcode installed
- iOS simulator or device

## Build Commands

### Android Debug APK
```bash
cd android
./gradlew assembleDebug
```
Builds debug APK at:
`android/app/build/outputs/apk/debug/app-debug.apk`

### Android Release APK
```bash
cd android
./gradlew assembleRelease
```
Builds release APK (requires signing configuration).

### Clean Android Build
```bash
cd android
./gradlew clean
```
Removes build artifacts. Use when experiencing build issues.

## Common Issues

### Metro Bundler Issues
```bash
# Clear Metro cache
npm start -- --reset-cache

# Or manually clear
rm -rf /tmp/metro-*
rm -rf /tmp/haste-map-*
```

### Android Build Issues
```bash
# Clear Gradle cache
cd android
./gradlew clean

# Clear node modules and reinstall
rm -rf node_modules
npm install
```

### Port Already in Use
```bash
# Kill process on port 8081 (Metro)
lsof -ti:8081 | xargs kill -9

# Or use different port
npm start -- --port 8088
```

## CI/CD Builds

GitHub Actions automatically builds on push/PR:
- Lint checks
- Test suite (171 tests)
- TypeScript type checking
- Android debug APK build

Workflow file: `.github/workflows/ci-cd.yml`

## Device Requirements

### Android
- **Minimum SDK**: 21 (Android 5.0)
- **Target SDK**: Latest (configured in android/build.gradle)
- **Architecture**: ARM64, ARMv7, x86, x86_64

### iOS
- **Minimum iOS**: 13.0 (configured in ios/Podfile)
- **Architecture**: ARM64 (device), x86_64 (simulator)

## Development Setup

First time setup:
```bash
# Install dependencies
npm install

# For iOS (macOS only)
cd ios && pod install && cd ..
```

## Build Artifacts

After successful Android build, APK location:
- **Debug**: `android/app/build/outputs/apk/debug/app-debug.apk`
- **Release**: `android/app/build/outputs/apk/release/app-release.apk`

Install APK on device:
```bash
adb install android/app/build/outputs/apk/debug/app-debug.apk
```
