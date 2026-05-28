---
name: mobile-mcp
description: "WHAT: Automate iOS/Android apps via Mobile MCP server for testing. WHEN: testing mobile features, validating UI changes, regression testing. KEYWORDS: mobile, mcp, automation, testing, simulator, emulator, ios, android, tap, swipe."
---

# Mobile MCP - Mobile Automation

Mobile MCP is a Model Context Protocol server that enables AI agents to automate iOS and Android applications through a platform-agnostic interface.

## When to Use

Use Mobile MCP for:
- Automated testing of mobile features during development
- Regression testing of critical user flows
- Validating UI changes across different screen sizes
- Verifying React Native module integration in shell apps
- Data extraction from mobile applications
- Repetitive manual testing tasks

**Don't use for:**
- Production app automation (use Maestro tests instead)
- Load testing or performance testing
- Security testing requiring specialized tools

## Prerequisites

Ensure these are installed before using Mobile MCP:

**Required:**
- Node.js v22+
- Android Platform Tools (for Android)
- Xcode command line tools (for iOS, macOS only)

**Device Setup:**
- **iOS Simulator (Recommended)**: Fastest and most reliable option on macOS
- **Android Emulator**: Cross-platform but may be slower
- **Real Devices**: Require developer mode and USB debugging

## Installation

Add Mobile MCP server to Claude Code:

```bash
claude mcp add mobile-mcp -- npx -y @mobilenext/mobile-mcp@latest
```

Or manually add to `.claude/mcp_settings.json`:

```json
{
  "mcpServers": {
    "mobile-mcp": {
      "command": "npx",
      "args": ["-y", "@mobilenext/mobile-mcp@latest"]
    }
  }
}
```

## Device Setup

### iOS Simulator (Recommended)

```bash
# List available simulators
xcrun simctl list

# Boot a simulator
xcrun simctl boot "iPhone 16"
```

**Why iOS Simulator?** Excellent performance on macOS, fast boot times, and reliable accessibility tree support.

### Android Emulator

```bash
# Start emulator
emulator -avd <avd_name>

# Verify connection
adb devices
```

### Real Devices

- **Android**: Enable USB debugging in developer options
- **iOS**: Connect via USB, ensure device is trusted and in developer mode (requires macOS + Xcode)

## Usage Patterns

### Testing Mobile Onboarding

```
Open the mobile app, go through the onboarding flow:
1. Take a screenshot of the welcome screen
2. Tap "Get Started"
3. Verify the carousel appears
4. Swipe through all carousel slides
5. Tap "Continue" on the last slide
6. Verify the main screen loads
```

### Data Entry Workflow

```
Open the app:
1. Navigate to the recipe detail screen
2. Add the recipe to favorites
3. Take a screenshot showing the favorited state
4. Navigate back to the home screen
5. Verify the recipe appears in favorites
```

### Multi-Step User Journey

```
Test the checkout flow:
1. Add 3 recipes to the cart
2. Navigate to checkout
3. Fill in delivery address
4. Select payment method
5. Take screenshots at each step
6. Verify order summary is correct
```

## Available Tools

Mobile MCP provides:
- **Device interaction**: Tap, swipe, type, scroll
- **UI inspection**: Screenshots, accessibility snapshot
- **Navigation**: Back, home, open app
- **Data extraction**: Extract structured data from visible UI elements
- **State verification**: Assert visible elements, check UI state

## Verifying React Native Module Integration

When adding React Native modules to a shell app:

### Step 1: Ensure Metro is Running

```bash
# Check if Metro is running
lsof -ti:8081

# Start Metro if needed
yarn start &
sleep 5
```

### Step 2: Build and Deploy

```bash
# Development build
yarn run:android  # or yarn run:ios

# Release build (no Metro required)
cd app/android && ./gradlew assembleRelease
```

### Step 3: Verify Module

1. List available devices using `mobile_list_available_devices`
2. Take initial screenshot with `mobile_take_screenshot`
3. Navigate to module using `mobile_list_elements_on_screen` and `mobile_click_on_screen_at_coordinates`
4. Wait for module to load (3-5 seconds)
5. Check logs for errors:

```bash
# Android
adb logcat -d | grep -E "(ModuleName|ReactNative|Metro)" | tail -30

# iOS
# Check accessibility tree for content
```

### Step 4: Handle Metro Disconnection

If Metro disconnects:

```bash
# Android: Open dev menu and reload
adb shell input keyevent 82

# iOS: Relaunch the app
xcrun simctl terminate <UDID> <bundle-id>
xcrun simctl launch <UDID> <bundle-id>
```

## Best Practices

### Be Specific About Target Elements

✅ **Do:**
```
Tap the "Add to Cart" button
```

❌ **Don't:**
```
Tap at coordinates (150, 300)
```

**Why**: Coordinates break with different screen sizes or UI changes.

### Account for Animations

✅ **Do:**
```
Tap submit, wait for loading spinner to disappear, then verify confirmation
```

❌ **Don't:**
```
Tap submit, then verify confirmation message
```

**Why**: Mobile apps have animations and network delays.

### Break Down Complex Workflows

✅ **Do:**
```
Step 1: Navigate to checkout (verify checkout screen appears)
Step 2: Fill form (verify form is filled)
Step 3: Submit (verify success message)
```

❌ **Don't:**
```
Complete 10-step workflow in one instruction
```

**Why**: Incremental verification makes it easier to identify failures.

### Use Accessibility Labels

- Use accessibility IDs when available
- Describe UI elements clearly (button text, location)
- Take screenshots to verify state before complex interactions
- Wait for elements to appear before interacting

## Common Integration Issues

### Navigation Route Not Found

**Symptom**: Clicking navigation button returns to home screen without error.

**Check:**
- Route exists in MainActivity.kt (Android) or AppDelegate.swift (iOS)
- Route name matches exactly between UI and navigation config
- Module composable/view controller is properly imported

**Solution**: Check logcat for navigation errors:
```bash
adb logcat -d | grep -E "Navigation|IllegalArgument"
```

### Module Not Loading After Code Changes

**Symptom**: Module UI appears blank or shows old behavior.

**Solution**: Clean build and reinstall:
```bash
cd app/android && ./gradlew clean && yarn run:android
```

**Why**: Native code changes require full rebuild.

### Module Renders But Content is Blank

**Check logs for:**
- Authentication errors
- Data fetching timeouts
- Missing initial props

**Example error patterns:**
```
[TokenManager] Auth data not found
[fetchRepository] Timeout waiting for repository
Analytics Event Successfully Fired - Name: ModuleName_Shown
```

**Why**: Shell apps often lack production auth/data.

## Troubleshooting

### Mobile MCP Can't Connect to Device

**Check:**
- iOS: Is simulator booted? (`xcrun simctl list`)
- iOS: Are Xcode command line tools installed? (`xcrun --version`)
- Android: Is emulator running? (`adb devices`)
- Android: Are Android Platform Tools in PATH? (`adb --version`)

### Interactions Failing

**Solutions:**
- Take a screenshot first to verify UI state
- Use accessibility IDs instead of coordinates
- Add wait/delay for animations and loading states
- Check accessibility snapshot for available elements

### Emulator/Simulator is Slow

**iOS:**
- Close other applications to free resources
- Use simulator-only builds for faster iteration

**Android:**
- Allocate more RAM and CPU cores in AVD settings
- Enable hardware acceleration (Intel HAXM or Hyper-V)
- Use x86/x86_64 emulator images instead of ARM

## Integration with Maestro Tests

Mobile MCP complements Maestro E2E tests:

- **Maestro**: Scripted, repeatable test flows in YAML for CI/CD
- **Mobile MCP**: Agent-driven, exploratory testing and validation

Use Mobile MCP during development to:
1. Explore and validate new features
2. Generate screenshots for documentation
3. Quickly test edge cases
4. Prototype test scenarios

Then formalize critical paths as Maestro tests for production.

## Resources

For detailed API documentation and examples, see:
- [references/api-docs.md](references/api-docs.md) - Mobile MCP API reference
- [references/examples.md](references/examples.md) - Real-world usage examples
- [references/patterns.md](references/patterns.md) - Implementation patterns from production code
