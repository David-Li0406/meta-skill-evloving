# Mobile MCP Usage Examples

Real-world examples from the YourCompany shared-mobile-modules project.

## Shell App Navigation Example

The Android shell app uses Jetpack Compose Navigation to route to React Native modules:

```kotlin
// MainActivity.kt
@Composable
fun MainScreen() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = "shellAppHome") {
        composable("shellAppHome") { HomeScreen(navController) }
        composable("onboardingModule") { OnboardingModule(navController) }
        composable("snapOnboardingModule") { SnapOnboardingModule(navController) }
        composable("storeModule?initialRouteName={initialRouteName}") { backStackEntry ->
            val initialRouteName = backStackEntry.arguments?.getString("initialRouteName") ?: "Storefront"
            StoreModule(navController, initialRouteName)
        }
    }
}
```

### Mobile MCP Workflow for Navigation Verification

```
1. Launch the shell app
2. Use mobile_take_screenshot to verify home screen loaded
3. Use mobile_list_elements_on_screen to find "Go to Onboarding" button
4. Use mobile_click_on_screen_at_coordinates with button coordinates
5. Wait 3 seconds for navigation
6. Use mobile_take_screenshot to verify onboarding screen loaded
7. Check accessibility tree for onboarding content
```

## Maestro Test Example

From `MaestroTests/flows/onboarding/onboarding_screen_v1_test.yaml`:

```yaml
appId: ${APP_ID}
---
- launchApp:
    stopApp: true
    arguments:
      isE2ETesting: true
      testName: 'onboarding_screen_v1_test'
- assertVisible: 'Go to Onboarding'
- tapOn:
    text: 'Go to Onboarding'
- assertVisible:
    id: 'welcome-carousel-v1'
```

### Equivalent Mobile MCP Workflow

```
Launch the app with test arguments:
1. Terminate existing app instance
2. Launch app with arguments: isE2ETesting=true, testName=onboarding_screen_v1_test
3. Assert "Go to Onboarding" button is visible
4. Tap "Go to Onboarding"
5. Wait for navigation
6. Assert element with ID "welcome-carousel-v1" is visible
```

## React Native Module Integration Verification

### Example: Verifying Onboarding Module

```
Verify onboarding module integration:
1. Ensure Metro is running (check port 8081)
2. Launch shell app
3. Take screenshot of home screen
4. List all elements on screen
5. Find and tap "Go to Onboarding" button
6. Wait 3 seconds for React Native module to load
7. Check Android logcat for module errors:
   adb logcat -d | grep -E "(Onboarding|ReactNative)" | tail -20
8. Take screenshot of onboarding screen
9. Verify carousel elements are visible in accessibility tree
10. If blank screen, check for Metro connection errors
```

### Common Error Patterns to Check

**Navigation error:**
```bash
adb logcat -d | grep "IllegalArgumentException: Navigation destination"
# Indicates route not registered in MainActivity
```

**Metro disconnection:**
```bash
adb logcat -d | grep "Unable to display loading message because react activity"
# Indicates Metro bundler connection lost
```

**Auth/data error:**
```bash
adb logcat -d | grep -E "TokenManager|fetchRepository"
# Indicates missing auth or data in shell app
```

## Multi-Step Workflow Example

### Recipe Favoriting Flow

```
Test recipe favoriting:
1. Launch app and navigate to recipe detail
2. Take screenshot before action
3. Find "Add to Favorites" button using mobile_list_elements_on_screen
4. Tap button at coordinates
5. Wait 2 seconds for animation
6. Take screenshot showing favorited state
7. Press back button to return to home
8. Navigate to favorites section
9. Verify recipe appears in favorites list
10. Take final screenshot for documentation
```

## Debugging Flow with Mobile MCP

### When Module Doesn't Load

```
Debug React Native module not loading:
1. Check if Metro is running:
   lsof -ti:8081
2. If not running, start Metro:
   yarn start &
   sleep 5
3. Rebuild and reinstall app:
   cd app/android && ./gradlew clean && yarn run:android
4. Wait for app to install and launch
5. Navigate to module again
6. Check logcat for specific errors:
   adb logcat -d | grep -E "(ModuleName|Error)" | tail -30
7. If Metro disconnected, reload app:
   adb shell input keyevent 82  # Open dev menu
   # Then tap reload in dev menu
```

## Screenshot Comparison Workflow

```
Capture screenshots for visual regression:
1. Launch app in clean state
2. Navigate to target screen
3. Wait for all content to load (check for loading indicators)
4. Take screenshot with mobile_save_screenshot to specific path:
   /screenshots/feature-name/baseline.png
5. Make code changes
6. Rebuild app
7. Navigate to same screen
8. Take comparison screenshot:
   /screenshots/feature-name/current.png
9. Compare screenshots manually or with image diff tool
```

## Performance Verification

```
Verify module loads within performance budget:
1. Launch app
2. Note timestamp
3. Navigate to module
4. Poll accessibility tree every 500ms until content appears
5. Calculate load time
6. Assert load time < 3 seconds
7. Check logcat for performance warnings
8. Take screenshot of loaded module
```

## Data Extraction Example

```
Extract visible recipe cards:
1. Navigate to recipe list screen
2. Use mobile_list_elements_on_screen
3. Filter elements with type "button" or "card"
4. Extract text/labels from each element
5. Structure data:
   {
     "recipes": [
       {"name": "Element Label 1", "position": {"x": 10, "y": 100}},
       {"name": "Element Label 2", "position": {"x": 10, "y": 250}}
     ]
   }
6. Validate expected recipes are visible
```

## Swipe Gesture Example

```
Test horizontal carousel swipe:
1. Navigate to carousel screen
2. Take initial screenshot
3. Use mobile_get_screen_size to get dimensions
4. Calculate swipe coordinates:
   startX = screenWidth * 0.8
   startY = screenHeight * 0.5
   endX = screenWidth * 0.2
   endY = screenHeight * 0.5
5. Execute mobile_swipe_on_screen with "left" direction
6. Wait 1 second for animation
7. Take screenshot of next slide
8. Repeat for all slides
9. Verify final slide shows "Continue" button
```

## Real Device Testing

```
Test on real Android device:
1. Enable USB debugging on device
2. Connect device via USB
3. Verify device appears: adb devices
4. List available devices with mobile_list_available_devices
5. Select device ID for testing
6. Run test workflow with device parameter
7. For iOS real device, ensure device is trusted and in developer mode
```
