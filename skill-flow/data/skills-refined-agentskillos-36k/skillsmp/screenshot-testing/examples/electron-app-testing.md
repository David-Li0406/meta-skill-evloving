# Electron App Testing Example

This example demonstrates how to test an Electron application's login flow using screenshot testing.

## Scenario

Test the login screen of an Electron app to verify:
1. Login form renders correctly
2. Error states display properly
3. Successful login transitions to main view

## Step-by-Step Workflow

### 1. Launch and Identify the App

First, ensure the Electron app is running, then identify its window:

```
Call: list_windows

Response includes:
{
  "id": "12345",
  "title": "MyApp - Login",
  "app": "Electron",
  "bounds": { "x": 100, "y": 100, "width": 800, "height": 600 }
}
```

### 2. Capture Baseline Login Screen

Capture the initial login screen state:

```
Call: screenshot_window
Parameters: {
  "window_title": "MyApp - Login",
  "save_dir": "/path/to/test-screenshots/login-baseline"
}
```

This creates a baseline at:
`/path/to/test-screenshots/login-baseline/2024-01-21/20240121_143052.png`

### 3. Analyze Login Form

After capturing, verify the login screen:

**Expected elements:**
- Username/email input field
- Password input field
- "Login" button
- "Forgot password?" link
- App logo at top

**Check for:**
- Proper alignment and spacing
- Correct colors matching brand guidelines
- All text readable and properly sized
- Input fields have correct placeholder text

### 4. Test Error State

Trigger an error state (invalid credentials), then capture:

```
Call: screenshot_window
Parameters: {
  "window_title": "MyApp - Login",
  "save_dir": "/path/to/test-screenshots/login-error"
}
```

**Verify error state shows:**
- Error message visible
- Input fields highlighted (if applicable)
- Form remains usable

### 5. Test Successful Login

After successful login, the window title may change:

```
Call: list_windows

Find new window:
{
  "id": "12346",
  "title": "MyApp - Dashboard",
  "app": "Electron",
  ...
}
```

Capture the post-login state:

```
Call: screenshot_window
Parameters: {
  "window_id": "12346",
  "save_dir": "/path/to/test-screenshots/dashboard"
}
```

### 6. Compare with Previous Version

For regression testing, compare current screenshots with baseline:

1. Load baseline screenshot from saved location
2. Capture current state with same window size
3. Compare visually for unexpected changes

**Report format:**
```
Login Screen Comparison:
- ✓ Logo position unchanged
- ✓ Input fields aligned correctly
- ⚠ Button color slightly different (was #007AFF, now #0066CC)
- ✓ Error message displays correctly
```

## Tips for Electron Apps

### Window Identification

Electron apps often have:
- Multiple windows (main, preferences, dialogs)
- Dynamic window titles
- DevTools windows (filter these out)

Use `app: "Electron"` to find Electron windows, then match by title.

### Handling DevTools

DevTools windows appear separately. Filter by checking:
- Title doesn't contain "DevTools"
- Window size matches expected app dimensions

### Testing Different States

For comprehensive testing:
1. Initial/empty state
2. Loading state (if applicable)
3. Error states
4. Success states
5. Edge cases (long text, empty fields)

### Responsive Testing

To test different window sizes:
1. Resize the Electron window manually
2. Capture at each size
3. Compare layouts across sizes

## Complete Test Script Example

A full testing session might look like:

```
1. list_windows → Find "MyApp" window
2. screenshot_window (title="MyApp - Login", save_dir="./baseline")
   → Analyze: Login form correct
3. [User enters invalid credentials]
4. screenshot_window (title="MyApp - Login", save_dir="./error-state")
   → Analyze: Error message visible
5. [User enters valid credentials]
6. list_windows → Find new "Dashboard" window
7. screenshot_window (title="MyApp - Dashboard", save_dir="./dashboard")
   → Analyze: Dashboard renders correctly
8. Compare all screenshots with previous baseline
   → Report: No regressions found
```
