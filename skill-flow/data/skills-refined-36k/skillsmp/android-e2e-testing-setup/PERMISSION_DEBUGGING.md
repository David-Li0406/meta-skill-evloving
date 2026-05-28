# Debugging Permission UI with UI Automator

If the smoke test fails due to permission dialogs not being handled correctly,
use this guide to find the right UI selectors.

## Step 1: Capture UI Hierarchy

With the permission dialog showing on the device:

```bash
# Dump the UI hierarchy to a file
adb shell uiautomator dump /sdcard/ui_dump.xml

# Pull the file to your computer
adb pull /sdcard/ui_dump.xml

# View the XML
cat ui_dump.xml
```

## Step 2: Find Relevant Elements

Look for:
- `text` attributes containing "Allow", "Deny", "Health Connect", etc.
- `resource-id` attributes for buttons
- `class` attributes to understand element types

Example from HealthConnect:
```xml
<node resource-id="com.google.android.healthconnect:id/allow_button"
      text="Allow"
      class="android.widget.Button" />
```

## Step 3: Update SmokeTest.kt

Add selectors based on what you found:

```kotlin
// By resource ID (most reliable)
device.findObject(
    UiSelector().resourceId("com.google.android.healthconnect:id/allow_button")
)

// By text (works across versions)
device.findObject(
    UiSelector().text("Allow")
)

// By text pattern (handles variations)
device.findObject(
    UiSelector().textMatches("(?i)allow|permit")
)
```

## Step 4: Use UI Automator Viewer (Alternative)

If you have Android Studio:

```bash
$ANDROID_HOME/tools/bin/uiautomatorviewer
```

This provides a visual tool to inspect the UI hierarchy.

## Common HealthConnect Selectors

These may vary by Android version:

```kotlin
// Permission screen title
UiSelector().textContains("Health Connect")

// Allow all button
UiSelector().textMatches("(?i)allow all|select all")

// Individual permission toggle
UiSelector().className("android.widget.Switch")

// Confirm button
UiSelector().textMatches("(?i)allow|done|confirm|save")

// Cancel button (if you need to deny)
UiSelector().textMatches("(?i)cancel|deny|don't allow")
```
