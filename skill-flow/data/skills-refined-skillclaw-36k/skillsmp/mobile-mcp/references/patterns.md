# Mobile MCP Implementation Patterns

Common patterns for mobile automation with Mobile MCP in React Native projects.

## Pattern: Sequential Verification

Always verify state after each significant action to catch failures early.

```
✅ Good Pattern:
1. Take screenshot (verify starting state)
2. Perform action
3. Wait for animation/transition
4. Take screenshot (verify result)
5. Check accessibility tree (verify UI updated)
6. Continue to next step

❌ Bad Pattern:
1. Perform 5 actions in sequence
2. Check final state only
3. Hard to debug where failure occurred
```

## Pattern: Element Discovery

Use accessibility tree first, fall back to screenshots when needed.

```
✅ Good Pattern:
1. Use mobile_list_elements_on_screen to get structured data
2. Filter elements by type, text, or label
3. Calculate tap coordinates from element bounds
4. Tap using mobile_click_on_screen_at_coordinates

❌ Bad Pattern:
1. Take screenshot
2. Guess coordinates based on visual inspection
3. Hardcode coordinates that break on different devices
```

## Pattern: React Native Module Loading

Handle the asynchronous nature of React Native module initialization.

```
✅ Good Pattern:
1. Ensure Metro is running before navigation
2. Navigate to module
3. Wait 3-5 seconds for React Native bridge initialization
4. Check logcat/console for connection status
5. Verify content loaded via accessibility tree
6. If Metro error detected, reload and retry

❌ Bad Pattern:
1. Navigate to module
2. Immediately check for content
3. Fail without checking Metro connection
```

## Pattern: Metro Connection Management

Proactively manage Metro bundler connection for React Native modules.

```typescript
// Before testing React Native modules:

// 1. Verify Metro is running
lsof -ti:8081 || yarn start &

// 2. Wait for Metro to be ready
sleep 5

// 3. If Metro disconnects during test:
adb shell input keyevent 82  // Open dev menu (Android)
// Tap reload

// 4. For iOS, restart app if Metro disconnects:
xcrun simctl terminate <UDID> <bundle-id>
xcrun simctl launch <UDID> <bundle-id>
```

## Pattern: Wait Strategies

Different waiting strategies for different scenarios.

### Fixed Wait (Simple)
```
Use after: Navigation, animations, simple transitions
Wait time: 1-3 seconds
Example: "Wait 2 seconds for animation to complete"
```

### Polling (Reliable)
```
Use for: Content loading, API responses, dynamic elements
Pattern:
  1. Set max wait time (e.g., 10 seconds)
  2. Poll every 500ms
  3. Check accessibility tree for target element
  4. Exit when found or timeout reached
```

### Screenshot Comparison (Visual Changes)
```
Use for: Loading states, progress indicators
Pattern:
  1. Take initial screenshot
  2. Wait 1 second
  3. Take second screenshot
  4. Compare screenshots
  5. If different, content is still changing
  6. Repeat until stable or timeout
```

## Pattern: Error Detection and Recovery

Build resilient automation with error detection and recovery.

```
Standard Error Check Pattern:

1. Perform action
2. Wait for completion
3. Check for error indicators:
   - Red error text in UI
   - Toast messages
   - Alert dialogs
   - Logcat errors
4. If error detected:
   - Take screenshot for debugging
   - Log error details
   - Attempt recovery (close dialog, go back)
   - Retry or fail gracefully
```

## Pattern: Cross-Platform Testing

Handle differences between iOS and Android.

```typescript
// Detect platform first
const platform = await detectPlatform(); // from device info

if (platform === 'android') {
  // Android-specific actions
  // - Use adb commands
  // - Check logcat for errors
  // - Use back button (keyevent 4)
  adb shell input keyevent 4
} else if (platform === 'ios') {
  // iOS-specific actions
  // - Use xcrun simctl commands
  // - Check system logs
  // - Use swipe from left edge for back navigation
}
```

## Pattern: Module Integration Verification

Comprehensive pattern for verifying React Native module integration in shell apps.

```
Full Verification Workflow:

1. Pre-flight Checks:
   ✓ Metro running on port 8081
   ✓ App built and installed
   ✓ Device/emulator ready

2. Initial State:
   ✓ Take screenshot of home screen
   ✓ Verify expected buttons present

3. Navigation:
   ✓ Find navigation button
   ✓ Tap button
   ✓ Wait for navigation animation

4. Module Load Verification:
   ✓ Wait 3-5 seconds for React Native initialization
   ✓ Check logs for errors:
      - Navigation errors (route not found)
      - Metro connection errors
      - Module initialization errors
   ✓ Verify accessibility tree has content

5. Content Verification:
   ✓ Check for expected UI elements
   ✓ Verify no error screens
   ✓ Verify no Metro disconnection messages

6. Interaction Testing:
   ✓ Test basic interactions (tap, swipe)
   ✓ Verify state updates
   ✓ Take screenshots for documentation

7. Error Recovery:
   If failures detected:
   ✓ Check if Metro disconnected → reload app
   ✓ Check if route not found → verify MainActivity
   ✓ Check if content blank → verify auth/data
```

## Pattern: Maestro Test Migration

Convert existing Maestro tests to Mobile MCP workflows.

```yaml
# Maestro Test
- launchApp
- assertVisible: "Button Text"
- tapOn: { text: "Button Text" }
- assertVisible: { id: "next-screen" }
```

```
# Equivalent Mobile MCP Workflow
Launch app:
1. Use mobile_launch_app with bundle ID
2. Wait 2 seconds for app to load
3. Use mobile_list_elements_on_screen
4. Assert element with text "Button Text" exists
5. Get coordinates of button element
6. Use mobile_click_on_screen_at_coordinates
7. Wait 2 seconds for navigation
8. Use mobile_list_elements_on_screen
9. Assert element with ID "next-screen" exists
```

## Pattern: Screenshot-Based Documentation

Generate documentation screenshots automatically.

```
Documentation Screenshot Pattern:

1. Navigate to feature
2. Set up ideal state (clean data, good examples)
3. Wait for all content to load
4. Hide development overlays
5. Take high-quality screenshot with descriptive filename
6. Save to docs/screenshots/{feature-name}/{screen-name}.png
7. Generate markdown referencing screenshot
```

## Pattern: Data Entry Automation

Automate repetitive data entry tasks.

```
Form Filling Pattern:

1. Navigate to form screen
2. Use mobile_list_elements_on_screen to find form fields
3. For each field:
   a. Tap field to focus
   b. Wait for keyboard
   c. Use mobile_type_keys with field value
   d. Take screenshot (optional, for verification)
4. Find and tap submit button
5. Wait for submission
6. Verify success state
```

## Pattern: State Machine Testing

Test state transitions systematically.

```
State Transition Pattern:

Define states: [Initial, Loading, Loaded, Error, Empty]

For each state:
1. Set up preconditions to reach state
2. Take screenshot showing state
3. Verify expected UI elements for state
4. Test all valid transitions from state:
   a. Perform action triggering transition
   b. Verify new state reached
   c. Document transition
5. Test invalid transitions (should remain in state)
```

## Pattern: Performance Budgets

Verify performance meets requirements.

```
Performance Verification Pattern:

1. Define budget (e.g., module loads in < 3 seconds)
2. Clear app state
3. Record start timestamp
4. Trigger action (navigation, data load)
5. Poll for completion indicator
6. Record end timestamp
7. Calculate duration
8. Assert duration < budget
9. Log metrics for tracking
10. If exceeded, capture additional diagnostics:
    - Logcat for bottlenecks
    - Network requests
    - Memory usage
```

## Pattern: Conditional Flows

Handle dynamic content and optional steps.

```
Conditional Flow Pattern:

1. Take screenshot to assess state
2. Use mobile_list_elements_on_screen
3. Check if optional element exists:
   if (element.exists("Optional Dialog")) {
     // Handle dialog
     tap("Dismiss")
     wait(1)
   }
4. Continue with main flow
5. Adapt to different app states without failing
```

## Pattern: Regression Detection

Detect unintended changes.

```
Regression Detection Pattern:

1. Maintain baseline:
   - Expected elements list
   - Screenshot reference
   - Performance metrics

2. Run test workflow

3. Compare results:
   - Element count changed?
   - Unexpected elements appeared?
   - Expected elements missing?
   - Screenshot diff > threshold?
   - Performance degraded?

4. Flag regressions for review

5. Update baseline when intentional changes made
```

## Pattern: Release Build Verification

Use release builds for final verification without Metro dependency.

```
Release Build Pattern:

For Android:
1. Build release APK:
   cd app/android && ./gradlew assembleRelease

2. Install release build:
   adb install app/build/outputs/apk/release/app-release.apk

3. Run verification workflow

4. No Metro required - JavaScript bundled in APK

For iOS:
1. Build with Release configuration in Xcode
2. Install to simulator
3. Run verification workflow
4. No Metro required - JavaScript bundled in app
```

## Anti-Patterns to Avoid

### ❌ Hardcoded Coordinates
```
// Don't do this
mobile_click_on_screen_at_coordinates(device, 200, 300)
```

### ❌ No Verification Between Steps
```
// Don't do this
tap("Button 1")
tap("Button 2")
tap("Button 3")
// What if Button 2 navigation failed?
```

### ❌ Ignoring Platform Differences
```
// Don't assume back button exists on iOS
mobile_press_button(device, "BACK")
// Use platform-specific patterns
```

### ❌ Not Handling Metro Disconnection
```
// Don't ignore Metro errors
navigate("ReactNativeModule")
// Check for Metro connection before assuming success
```

### ❌ Timing Assumptions
```
// Don't assume fixed timing
tap("Submit")
verify("Success")
// Add waits and polling for reliability
```
