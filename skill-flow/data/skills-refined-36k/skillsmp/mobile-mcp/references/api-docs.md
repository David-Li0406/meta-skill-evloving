# Mobile MCP API Reference

Complete reference for Mobile MCP server tools and methods.

**Version**: 0.0.33
**Repository**: [mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp)
**License**: Apache-2.0

## Overview

Mobile MCP provides a Model Context Protocol interface for automating iOS and Android mobile applications. It works with simulators, emulators, and real devices using native accessibility trees and screenshot-based coordinates.

## Installation

### NPM Package
```bash
npx -y @mobilenext/mobile-mcp@latest
```

### Claude Code Setup
```bash
claude mcp add mobile-mcp -- npx -y @mobilenext/mobile-mcp@latest
```

### Manual Configuration
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

## Core Tools

### Device Management

#### `mobile_list_available_devices`

Lists all available devices (simulators, emulators, real devices).

**Parameters**: None

**Returns**:
```typescript
{
  devices: Array<{
    id: string;           // Device identifier
    name: string;         // Device name
    platform: 'ios' | 'android';
    state: 'booted' | 'shutdown' | 'device';
    type: 'simulator' | 'emulator' | 'real';
  }>
}
```

**Example**:
```typescript
// Lists all connected devices
mobile_list_available_devices()
// Returns: iOS simulators, Android emulators, and USB-connected devices
```

#### `mobile_list_apps`

Lists all installed apps on a device.

**Parameters**:
- `device: string` - Device identifier from `mobile_list_available_devices`

**Returns**:
```typescript
{
  apps: Array<{
    packageName: string;  // Bundle ID (iOS) or package name (Android)
    name: string;         // App display name
    version: string;      // App version
  }>
}
```

#### `mobile_launch_app`

Launches an app on the device.

**Parameters**:
- `device: string` - Device identifier
- `packageName: string` - Bundle ID (iOS) or package name (Android)

**Returns**: Success/failure status

**Example**:
```typescript
mobile_launch_app(device, "com.yourcompany.app")
```

#### `mobile_terminate_app`

Stops and terminates a running app.

**Parameters**:
- `device: string` - Device identifier
- `packageName: string` - Bundle ID or package name

**Returns**: Success/failure status

#### `mobile_install_app`

Installs an app on the device.

**Parameters**:
- `device: string` - Device identifier
- `path: string` - Path to app file (.app, .ipa for iOS; .apk for Android)

**Returns**: Success/failure status

**Example**:
```typescript
mobile_install_app(device, "/path/to/app-release.apk")
```

#### `mobile_uninstall_app`

Uninstalls an app from the device.

**Parameters**:
- `device: string` - Device identifier
- `bundle_id: string` - Bundle ID (iOS) or package name (Android)

**Returns**: Success/failure status

### Screen Interaction

#### `mobile_get_screen_size`

Gets the screen dimensions in pixels.

**Parameters**:
- `device: string` - Device identifier

**Returns**:
```typescript
{
  width: number;   // Screen width in pixels
  height: number;  // Screen height in pixels
}
```

**Example**:
```typescript
mobile_get_screen_size(device)
// Returns: { width: 1080, height: 1920 }
```

#### `mobile_take_screenshot`

Takes a screenshot of the current screen.

**Parameters**:
- `device: string` - Device identifier

**Returns**: Screenshot image data (base64 or image object)

**Example**:
```typescript
mobile_take_screenshot(device)
// Returns visual representation of current screen
```

#### `mobile_save_screenshot`

Saves a screenshot to a file.

**Parameters**:
- `device: string` - Device identifier
- `saveTo: string` - File path to save screenshot

**Returns**: Success/failure status

**Example**:
```typescript
mobile_save_screenshot(device, "/screenshots/feature/screen.png")
```

#### `mobile_list_elements_on_screen`

Lists all interactive elements with their properties and coordinates.

**Parameters**:
- `device: string` - Device identifier

**Returns**:
```typescript
{
  elements: Array<{
    type: string;              // Element type (button, text, image, etc.)
    text?: string;             // Visible text
    label?: string;            // Accessibility label
    id?: string;               // Accessibility ID / resource ID
    coordinates: {
      x: number;               // Top-left X coordinate
      y: number;               // Top-left Y coordinate
      width: number;           // Element width
      height: number;          // Element height
    };
    isClickable: boolean;      // Whether element responds to taps
    isVisible: boolean;        // Whether element is visible
  }>
}
```

**Example**:
```typescript
mobile_list_elements_on_screen(device)
// Returns structured accessibility tree with coordinates
```

### Touch Interactions

#### `mobile_click_on_screen_at_coordinates`

Taps on the screen at specific coordinates.

**Parameters**:
- `device: string` - Device identifier
- `x: number` - X coordinate in pixels
- `y: number` - Y coordinate in pixels

**Returns**: Success/failure status

**Example**:
```typescript
// Tap center of button at (100, 200) with size 200x50
mobile_click_on_screen_at_coordinates(device, 200, 225)
```

**Best Practice**: Use `mobile_list_elements_on_screen` to get coordinates, then tap center:
```typescript
const center_x = element.coordinates.x + (element.coordinates.width / 2);
const center_y = element.coordinates.y + (element.coordinates.height / 2);
mobile_click_on_screen_at_coordinates(device, center_x, center_y);
```

#### `mobile_double_tap_on_screen`

Performs a double-tap at coordinates.

**Parameters**:
- `device: string` - Device identifier
- `x: number` - X coordinate in pixels
- `y: number` - Y coordinate in pixels

**Returns**: Success/failure status

#### `mobile_long_press_on_screen_at_coordinates`

Performs a long press (hold) at coordinates.

**Parameters**:
- `device: string` - Device identifier
- `x: number` - X coordinate in pixels
- `y: number` - Y coordinate in pixels

**Returns**: Success/failure status

**Example**:
```typescript
// Long press to show context menu
mobile_long_press_on_screen_at_coordinates(device, 200, 300)
```

#### `mobile_swipe_on_screen`

Performs a swipe gesture.

**Parameters**:
- `device: string` - Device identifier
- `direction: 'up' | 'down' | 'left' | 'right'` - Swipe direction
- `distance?: number` - Swipe distance in pixels (optional)
- `x?: number` - Starting X coordinate (optional, defaults to center)
- `y?: number` - Starting Y coordinate (optional, defaults to center)

**Returns**: Success/failure status

**Example**:
```typescript
// Swipe up to scroll down
mobile_swipe_on_screen(device, "up", 400)

// Swipe left on carousel
mobile_swipe_on_screen(device, "left", 300)
```

### Text Input

#### `mobile_type_keys`

Types text into the focused element.

**Parameters**:
- `device: string` - Device identifier
- `text: string` - Text to type
- `submit: boolean` - Whether to press enter/submit after typing

**Returns**: Success/failure status

**Example**:
```typescript
// Type email without submitting
mobile_type_keys(device, "user@example.com", false)

// Type password and submit
mobile_type_keys(device, "password123", true)
```

**Note**: Element must be focused first by tapping on it.

### Navigation

#### `mobile_press_button`

Presses a device button.

**Parameters**:
- `device: string` - Device identifier
- `button: string` - Button name

**Supported Buttons**:
- `BACK` (Android only) - Back button
- `HOME` - Home button
- `VOLUME_UP` - Volume up button
- `VOLUME_DOWN` - Volume down button
- `ENTER` - Enter/Return key
- `DPAD_CENTER` (Android TV) - D-pad center
- `DPAD_UP` (Android TV) - D-pad up
- `DPAD_DOWN` (Android TV) - D-pad down
- `DPAD_LEFT` (Android TV) - D-pad left
- `DPAD_RIGHT` (Android TV) - D-pad right

**Returns**: Success/failure status

**Example**:
```typescript
// Android: Press back button
mobile_press_button(device, "BACK")

// Go to home screen
mobile_press_button(device, "HOME")
```

#### `mobile_open_url`

Opens a URL in the device browser.

**Parameters**:
- `device: string` - Device identifier
- `url: string` - URL to open

**Returns**: Success/failure status

**Example**:
```typescript
mobile_open_url(device, "https://yourcompany.com")
```

### Device State

#### `mobile_set_orientation`

Changes the screen orientation.

**Parameters**:
- `device: string` - Device identifier
- `orientation: 'portrait' | 'landscape'` - Desired orientation

**Returns**: Success/failure status

**Example**:
```typescript
// Switch to landscape for better viewing
mobile_set_orientation(device, "landscape")
```

#### `mobile_get_orientation`

Gets the current screen orientation.

**Parameters**:
- `device: string` - Device identifier

**Returns**:
```typescript
{
  orientation: 'portrait' | 'landscape'
}
```

## Platform-Specific Tools

### iOS Simulator (via idb)

#### `ui_describe_all`

Gets comprehensive accessibility information for the entire screen.

**Parameters**:
- `udid?: string` - Optional iOS simulator UDID

**Returns**: Detailed accessibility tree for entire screen

#### `ui_tap`

Taps on screen with optional press duration.

**Parameters**:
- `udid?: string` - Optional simulator UDID
- `x: number` - X coordinate
- `y: number` - Y coordinate
- `duration?: string` - Press duration (e.g., "0.1")

**Returns**: Success/failure status

#### `ui_type`

Types text into iOS simulator.

**Parameters**:
- `udid?: string` - Optional simulator UDID
- `text: string` - Text to type (max 500 chars, ASCII only)

**Returns**: Success/failure status

#### `ui_swipe`

Performs swipe gesture on iOS simulator.

**Parameters**:
- `udid?: string` - Optional simulator UDID
- `x_start: number` - Starting X
- `y_start: number` - Starting Y
- `x_end: number` - Ending X
- `y_end: number` - Ending Y
- `duration?: string` - Swipe duration (e.g., "0.1")
- `delta?: number` - Step size (default 1)

**Returns**: Success/failure status

#### `ui_describe_point`

Gets accessibility element at specific coordinates.

**Parameters**:
- `udid?: string` - Optional simulator UDID
- `x: number` - X coordinate
- `y: number` - Y coordinate

**Returns**: Accessibility element information at that point

#### `ui_view`

Gets compressed screenshot of current simulator view.

**Parameters**:
- `udid?: string` - Optional simulator UDID

**Returns**: Screenshot image data

## Error Handling

All tools return error information when operations fail:

```typescript
{
  success: false,
  error: {
    code: string,           // Error code
    message: string,        // Human-readable error message
    details?: any          // Additional error context
  }
}
```

**Common Error Codes**:
- `DEVICE_NOT_FOUND` - Device ID doesn't exist or not connected
- `APP_NOT_FOUND` - App not installed on device
- `ELEMENT_NOT_FOUND` - Element doesn't exist in accessibility tree
- `TIMEOUT` - Operation timed out
- `PERMISSION_DENIED` - Missing required permissions
- `PLATFORM_ERROR` - Platform-specific error (adb/xcrun failed)

## Best Practices

### Use Accessibility Tree First
```typescript
// ✅ Good: Get structured element data
const elements = mobile_list_elements_on_screen(device);
const button = elements.find(e => e.text === "Submit");
mobile_click_on_screen_at_coordinates(device,
  button.coordinates.x + button.coordinates.width/2,
  button.coordinates.y + button.coordinates.height/2
);

// ❌ Bad: Hardcode coordinates
mobile_click_on_screen_at_coordinates(device, 200, 300);
```

### Wait for Content to Load
```typescript
// ✅ Good: Wait and verify
mobile_swipe_on_screen(device, "up");
await wait(2000);  // Wait for animation
const screen = mobile_take_screenshot(device);

// ❌ Bad: Don't verify
mobile_swipe_on_screen(device, "up");
mobile_swipe_on_screen(device, "up");  // May fail if previous swipe still animating
```

### Handle Platform Differences
```typescript
// ✅ Good: Platform-aware
if (platform === 'android') {
  mobile_press_button(device, "BACK");
} else {
  // iOS: Swipe from left edge
  mobile_swipe_on_screen(device, "right", 100, 0, screenHeight/2);
}

// ❌ Bad: Assume Android
mobile_press_button(device, "BACK");  // Fails on iOS
```

## Resources

- **GitHub**: https://github.com/mobile-next/mobile-mcp
- **Wiki**: https://github.com/mobile-next/mobile-mcp/wiki
- **NPM**: https://www.npmjs.com/package/@mobilenext/mobile-mcp
- **Slack Community**: http://mobilenexthq.com/join-slack
- **Example Prompts**: https://github.com/mobile-next/mobile-mcp/wiki/Prompt-Example-repo-list

## Version History

- **0.0.33** (2025-10-20): Latest release
- **0.0.28**: Updated mobilecli dependency
- **0.0.x**: Active development, frequent updates

Check [CHANGELOG.md](https://github.com/mobile-next/mobile-mcp/blob/main/CHANGELOG.md) for detailed version history.
