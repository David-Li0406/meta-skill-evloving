# Screenshots Actions

## snapshot / capture_ios_screenshots

Automatically capture localized iOS screenshots on multiple devices.

```ruby
capture_ios_screenshots(
  workspace: "MyApp.xcworkspace",
  scheme: "MyAppUITests",
  
  # Devices
  devices: [
    "iPhone 15 Pro Max",
    "iPhone 15",
    "iPhone SE (3rd generation)",
    "iPad Pro (12.9-inch) (6th generation)"
  ],
  
  # Languages
  languages: ["en-US", "de-DE", "ja-JP", "es-ES"],
  
  # Output
  output_directory: "./screenshots",
  clear_previous_screenshots: true,
  
  # Options
  concurrent_simulators: true,
  number_of_retries: 3,
  stop_after_first_error: false,
  
  # Configuration
  dark_mode: false,
  override_status_bar: true,
  override_status_bar_arguments: "--time 9:41"
)
```

**Snapfile Configuration:**
```ruby
# fastlane/Snapfile
devices([
  "iPhone 15 Pro Max",
  "iPhone SE (3rd generation)",
  "iPad Pro (12.9-inch) (6th generation)"
])

languages(["en-US", "de-DE", "ja-JP"])

scheme("MyAppUITests")
output_directory("./screenshots")

clear_previous_screenshots(true)
override_status_bar(true)
concurrent_simulators(true)
```

**UI Test Setup:**
```swift
// MyAppUITests/SnapshotTests.swift
import XCTest

class SnapshotTests: XCTestCase {
    override func setUpWithError() throws {
        continueAfterFailure = false
        let app = XCUIApplication()
        setupSnapshot(app)
        app.launch()
    }
    
    func testHomeScreen() throws {
        snapshot("01_HomeScreen")
    }
    
    func testDetailScreen() throws {
        app.buttons["Details"].tap()
        snapshot("02_DetailScreen")
    }
}
```

## screengrab / capture_android_screenshots

Capture Android screenshots using UI Automator.

```ruby
capture_android_screenshots(
  app_package_name: "com.example.app",
  app_apk_path: "./app/build/outputs/apk/debug/app-debug.apk",
  tests_apk_path: "./app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk",
  
  # Locales
  locales: ["en-US", "de-DE", "ja-JP"],
  
  # Output
  output_directory: "./screenshots/android",
  clear_previous_screenshots: true,
  
  # Options
  use_tests_in_classes: ["com.example.ScreenshotTests"],
  ending_locale: "en-US",
  
  # ADB
  adb_host: "localhost",
  specific_device: "emulator-5554"
)
```

**Screengrabfile Configuration:**
```ruby
# fastlane/Screengrabfile
app_package_name("com.example.app")
app_apk_path("./app/build/outputs/apk/debug/app-debug.apk")
tests_apk_path("./app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk")

locales(["en-US", "de-DE", "ja-JP"])
output_directory("./screenshots/android")
clear_previous_screenshots(true)
```

**Android Test Setup:**
```kotlin
// app/src/androidTest/java/com/example/ScreenshotTests.kt
@RunWith(JUnit4::class)
class ScreenshotTests {
    @Rule
    @JvmField
    val activityRule = ActivityScenarioRule(MainActivity::class.java)
    
    @Test
    fun testHomeScreen() {
        Screengrab.screenshot("01_HomeScreen")
    }
    
    @Test
    fun testDetailScreen() {
        onView(withId(R.id.detailsButton)).perform(click())
        Screengrab.screenshot("02_DetailScreen")
    }
}
```

## frameit / frame_screenshots

Add device frames around screenshots.

```ruby
frame_screenshots(
  path: "./screenshots",
  
  # Frame style
  white: false,  # Use white device frames
  silver: false,
  rose_gold: false,
  
  # Background
  background: "./background.jpg",
  background_color: "#ffffff",
  
  # Text
  use_platform: "IOS",
  title_min_height: 10
)
```

**Framefile.json Configuration:**
```json
{
  "default": {
    "title": {
      "color": "#000000",
      "font": "./fonts/MyFont-Bold.ttf",
      "font_size": 128
    },
    "keyword": {
      "color": "#0066CC",
      "font": "./fonts/MyFont-Regular.ttf",
      "font_size": 64
    },
    "background": "./background.png",
    "padding": 50,
    "show_complete_frame": true
  },
  "data": [
    {
      "filter": "01_Home",
      "keyword": "Easy to use",
      "title": "Your tasks,\norganized"
    },
    {
      "filter": "02_Detail",
      "keyword": "Powerful features",
      "title": "Complete\ncontrol"
    }
  ]
}
```

**Title Files (Alternative):**
```
screenshots/
├── en-US/
│   ├── iPhone 15 Pro Max/
│   │   ├── 01_Home.png
│   │   ├── 01_Home.strings       # Keyword and title
│   │   ├── 02_Detail.png
│   │   └── 02_Detail.strings
```

**strings file format:**
```
"keyword" = "Easy to use";
"title" = "Your tasks organized";
```

## Screenshots Directory Structure

**iOS:**
```
fastlane/screenshots/
├── en-US/
│   ├── iPhone 15 Pro Max-01_Home.png
│   ├── iPhone 15 Pro Max-02_Detail.png
│   ├── iPhone SE (3rd generation)-01_Home.png
│   └── iPad Pro (12.9-inch)-01_Home.png
├── de-DE/
│   └── ...
└── Framefile.json
```

**Android:**
```
fastlane/metadata/android/
├── en-US/
│   └── images/
│       ├── phoneScreenshots/
│       │   ├── 1_en-US.png
│       │   └── 2_en-US.png
│       ├── sevenInchScreenshots/
│       └── tenInchScreenshots/
```

## Complete Screenshots Workflow

```ruby
lane :screenshots do
  # iOS Screenshots
  capture_ios_screenshots(
    scheme: "MyAppUITests",
    devices: ["iPhone 15 Pro Max", "iPad Pro (12.9-inch)"],
    languages: ["en-US", "de-DE"]
  )
  
  # Frame screenshots
  frame_screenshots(white: true)
  
  # Upload to App Store
  upload_to_app_store(
    skip_binary_upload: true,
    skip_metadata: true
  )
end

lane :android_screenshots do
  # Build test APKs
  gradle(task: "assembleDebug assembleAndroidTest")
  
  # Capture screenshots
  capture_android_screenshots
  
  # Upload to Play Store
  upload_to_play_store(
    skip_upload_apk: true,
    skip_upload_metadata: true,
    skip_upload_changelogs: true
  )
end
```
