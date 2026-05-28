# ADB Command Reference

Complete reference for Android Debug Bridge (ADB) commands commonly used for device automation.

## Connection & Device Management

```bash
# Start/stop ADB server
adb start-server
adb kill-server

# List connected devices
adb devices
adb devices -l  # Long format with device details

# Connect to device over WiFi
adb tcpip 5555
adb connect <device-ip>:5555

# Target specific device
adb -s <device-id> <command>
```

## Input Commands

### Touch Input

```bash
# Single tap
adb shell input tap <x> <y>

# Swipe
adb shell input swipe <x1> <y1> <x2> <y2> [duration_ms]

# Long press (swipe in place)
adb shell input swipe <x> <y> <x> <y> 1000

# Drag (touchscreen)
adb shell input draganddrop <x1> <y1> <x2> <y2> [duration_ms]
```

### Text Input

```bash
# Type text (spaces must be %s)
adb shell input text "hello%sworld"

# Special characters that need escaping: ( ) < > | ; & * \ " ' ` $ !
# Use single quotes or escape with backslash
```

### Key Events

```bash
adb shell input keyevent <keycode>

# Common keycodes:
KEYCODE_HOME         # 3 - Home button
KEYCODE_BACK         # 4 - Back button
KEYCODE_POWER        # 26 - Power button
KEYCODE_MENU         # 82 - Menu button
KEYCODE_ENTER        # 66 - Enter key
KEYCODE_DEL          # 67 - Backspace
KEYCODE_TAB          # 61 - Tab
KEYCODE_SPACE        # 62 - Space
KEYCODE_DPAD_UP      # 19 - D-pad up
KEYCODE_DPAD_DOWN    # 20 - D-pad down
KEYCODE_DPAD_LEFT    # 21 - D-pad left
KEYCODE_DPAD_RIGHT   # 22 - D-pad right
KEYCODE_VOLUME_UP    # 24 - Volume up
KEYCODE_VOLUME_DOWN  # 25 - Volume down
KEYCODE_CAMERA       # 27 - Camera shutter
KEYCODE_SEARCH       # 84 - Search
KEYCODE_APP_SWITCH   # 187 - Recent apps
```

## UI Automation (uiautomator)

```bash
# Dump UI hierarchy
adb shell uiautomator dump /sdcard/window_dump.xml
adb pull /sdcard/window_dump.xml ./

# Alternative dump location
adb shell uiautomator dump /data/local/tmp/ui.xml
adb pull /data/local/tmp/ui.xml ./
```

## App Management

### Launching Apps

```bash
# Launch by package/activity
adb shell am start -n <package>/<activity>

# Example: Launch Chrome
adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main

# Launch main activity (using monkey)
adb shell monkey -p <package> -c android.intent.category.LAUNCHER 1

# Open URL in browser
adb shell am start -a android.intent.action.VIEW -d "https://example.com"

# Send intent with extras
adb shell am start -a android.intent.action.SEND -t text/plain --es android.intent.extra.TEXT "Hello"
```

### Package Management

```bash
# List all packages
adb shell pm list packages

# List third-party packages
adb shell pm list packages -3

# Get package info
adb shell dumpsys package <package>

# Find package for app
adb shell pm list packages | grep <search>

# Get current foreground app
adb shell dumpsys window | grep -E "mCurrentFocus|mFocusedApp"

# Force stop app
adb shell am force-stop <package>

# Clear app data
adb shell pm clear <package>
```

### Installing/Uninstalling

```bash
# Install APK
adb install app.apk
adb install -r app.apk  # Replace existing

# Uninstall
adb uninstall <package>
adb uninstall -k <package>  # Keep data
```

## Screen & Display

```bash
# Take screenshot
adb shell screencap /sdcard/screen.png
adb pull /sdcard/screen.png ./

# Record screen (max 3 min)
adb shell screenrecord /sdcard/video.mp4
adb shell screenrecord --time-limit 30 /sdcard/video.mp4

# Get screen resolution
adb shell wm size

# Get screen density
adb shell wm density
```

## File Operations

```bash
# Push file to device
adb push local_file /sdcard/

# Pull file from device
adb pull /sdcard/remote_file ./

# List files
adb shell ls /sdcard/

# Remove file
adb shell rm /sdcard/file

# Create directory
adb shell mkdir /sdcard/folder
```

## Device Info

```bash
# Get device properties
adb shell getprop

# Specific properties
adb shell getprop ro.product.model      # Device model
adb shell getprop ro.product.brand      # Brand
adb shell getprop ro.build.version.sdk  # API level
adb shell getprop ro.serialno           # Serial number

# Battery status
adb shell dumpsys battery

# WiFi info
adb shell dumpsys wifi | grep "mWifiInfo"

# Memory info
adb shell dumpsys meminfo
```

## System Controls

```bash
# Wake up device
adb shell input keyevent KEYCODE_WAKEUP

# Lock screen
adb shell input keyevent KEYCODE_SLEEP

# Toggle screen on/off
adb shell input keyevent KEYCODE_POWER

# Unlock screen (if no security)
adb shell input keyevent KEYCODE_MENU

# Change brightness
adb shell settings put system screen_brightness 255  # 0-255

# Enable/disable WiFi
adb shell svc wifi enable
adb shell svc wifi disable

# Enable/disable mobile data
adb shell svc data enable
adb shell svc data disable
```

## Debugging

```bash
# View logs
adb logcat
adb logcat -d  # Dump and exit
adb logcat *:E  # Errors only
adb logcat -c  # Clear log buffer

# Filter by app
adb logcat | grep <package>

# Get bug report
adb bugreport > bugreport.zip
```

## Common Package Names

```
com.android.chrome          # Chrome
com.google.android.youtube  # YouTube
com.google.android.gm       # Gmail
com.google.android.apps.maps # Google Maps
com.whatsapp               # WhatsApp
com.facebook.katana        # Facebook
com.instagram.android      # Instagram
com.twitter.android        # Twitter
com.spotify.music          # Spotify
com.netflix.mediaclient    # Netflix
com.amazon.mShop.android.shopping # Amazon
```
