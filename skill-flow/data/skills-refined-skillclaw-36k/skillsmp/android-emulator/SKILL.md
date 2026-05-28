---
name: android-emulator
description: Run and test the MagentaLine Flutter app on Android emulators. Use when the user asks to test on Android, run the emulator, start the phone/tablet emulator, or test on mobile devices. This skill handles launching AVDs, waiting for boot, deploying the Flutter app, and troubleshooting common emulator issues.
---

# Android Emulator Testing

## Quick Start

### 1. Launch Emulator
```bash
.claude/skills/android-emulator/scripts/launch_emulator.sh phone
```

### 2. Run Flutter App
```bash
.claude/skills/android-emulator/scripts/run_flutter_app.sh
```

Or manually:
```bash
cd /Users/william/Workspaces/MagentaLine/app && flutter run -d emulator-5554
```

## Available AVDs

| Name | Form Factor | Resolution |
|------|-------------|------------|
| `Medium_Phone_API_36.1` | Phone | 1080x2400 |
| `Medium_Tablet_API_36` | Tablet | 2560x1600 |

## Manual Commands

### Start Phone Emulator
```bash
export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
~/Library/Android/sdk/emulator/emulator -avd Medium_Phone_API_36.1 -no-snapshot-load &
sleep 45 && flutter devices
```

### Stop Emulator
```bash
pkill -f "qemu-system-aarch64"
~/Library/Android/sdk/platform-tools/adb kill-server
```

## Troubleshooting

**Device shows offline**: Wait longer (2+ min on first boot), or restart ADB:
```bash
~/Library/Android/sdk/platform-tools/adb kill-server && ~/Library/Android/sdk/platform-tools/adb start-server
```

**Tablet emulator permission errors**: Known issue on Apple Silicon. Use Android Studio Device Manager GUI or test tablet layouts in Chrome.

**Build failures**: Run `flutter doctor -v` to diagnose.
