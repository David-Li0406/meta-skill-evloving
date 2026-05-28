---
name: android-build-deploy
description: Build and deploy Android app to emulator or device. Use when testing Android changes, debugging on device, or running the app after code changes. Handles Gradle builds, APK installation, and app launching.
allowed-tools: Read, Bash
---

# Android Build & Deploy

## Purpose
Quickly build the Android app and deploy to connected device or emulator for testing.

## Prerequisites Check

Before building, verify environment:

```bash
# Check for connected devices/emulators
~/Library/Android/sdk/platform-tools/adb devices

# If no devices, start emulator
~/Library/Android/sdk/emulator/emulator -list-avds
~/Library/Android/sdk/emulator/emulator -avd <avd_name> &
```

## Build Commands

### Quick Compile (Check for Errors)
```bash
cd apps/android/construction-android
./gradlew :app:compileDebugKotlin
```

### Full Debug Build
```bash
cd apps/android/construction-android
./gradlew assembleDebug
```

### Build & Install in One Step
```bash
cd apps/android/construction-android
./gradlew installDebug
```

## Deploy to Device

### Install APK
```bash
~/Library/Android/sdk/platform-tools/adb install -r app/build/outputs/apk/debug/app-debug.apk
```

### Launch App
```bash
~/Library/Android/sdk/platform-tools/adb shell am start -n com.constructionpro.app/.MainActivity
```

### Combined: Build, Install, Launch
```bash
cd apps/android/construction-android && \
./gradlew installDebug && \
~/Library/Android/sdk/platform-tools/adb shell am start -n com.constructionpro.app/.MainActivity
```

## Debugging

### View Logs (Filtered to App)
```bash
~/Library/Android/sdk/platform-tools/adb logcat -s "ConstructionPro"
```

### View All Recent Logs
```bash
~/Library/Android/sdk/platform-tools/adb logcat -d -t 100
```

### Clear Logs Before Testing
```bash
~/Library/Android/sdk/platform-tools/adb logcat -c
```

## Common Issues

### Device Not Found
```bash
# Restart ADB server
~/Library/Android/sdk/platform-tools/adb kill-server
~/Library/Android/sdk/platform-tools/adb start-server
~/Library/Android/sdk/platform-tools/adb devices
```

### Build Cache Issues
```bash
cd apps/android/construction-android
./gradlew clean
./gradlew assembleDebug
```

### Kotlin Compile Errors
Check specific file:
```bash
./gradlew :app:compileDebugKotlin 2>&1 | grep -A 5 "error:"
```

## Quick Reference

| Task | Command |
|------|---------|
| Compile check | `./gradlew :app:compileDebugKotlin` |
| Full build | `./gradlew assembleDebug` |
| Build + Install | `./gradlew installDebug` |
| Launch app | `adb shell am start -n com.constructionpro.app/.MainActivity` |
| View logs | `adb logcat -d -t 50` |
| List devices | `adb devices` |

## Project Paths

- **Root**: `apps/android/construction-android/`
- **APK Output**: `app/build/outputs/apk/debug/app-debug.apk`
- **Source**: `app/src/main/java/com/constructionpro/app/`
- **Models**: `app/src/main/java/com/constructionpro/app/data/model/`
- **Screens**: `app/src/main/java/com/constructionpro/app/ui/screens/`
- **API Service**: `app/src/main/java/com/constructionpro/app/data/ApiService.kt`
