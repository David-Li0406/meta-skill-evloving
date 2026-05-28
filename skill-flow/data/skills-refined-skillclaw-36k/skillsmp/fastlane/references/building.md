# Building Actions

## gym / build_app / build_ios_app

Build and sign iOS/macOS apps. The primary action for creating .ipa files.

```ruby
build_app(
  workspace: "MyApp.xcworkspace",
  scheme: "MyApp",
  configuration: "Release",
  clean: true,
  output_directory: "./build",
  output_name: "MyApp.ipa",
  export_method: "app-store",  # app-store, ad-hoc, enterprise, development
  include_bitcode: false,
  include_symbols: true,
  export_options: {
    provisioningProfiles: {
      "com.example.app" => "MyApp Distribution"
    }
  }
)
```

**Key Parameters:**
- `workspace` / `project`: Path to .xcworkspace or .xcodeproj
- `scheme`: Build scheme name
- `configuration`: Debug, Release, or custom
- `export_method`: app-store, ad-hoc, enterprise, development
- `output_directory`: Where to save the .ipa
- `codesigning_identity`: Signing identity name
- `xcargs`: Extra xcodebuild arguments

## build_mac_app

Same as build_app but specifically for macOS targets.

```ruby
build_mac_app(
  scheme: "MyMacApp",
  export_method: "app-store"
)
```

## gradle / build_android_app

Build Android apps using Gradle.

```ruby
gradle(
  task: "assembleRelease",
  project_dir: "./android",
  properties: {
    "versionCode" => 123,
    "versionName" => "1.0.0"
  }
)

# Build AAB for Play Store
gradle(task: "bundleRelease")

# Clean and build
gradle(task: "clean assembleRelease")

# Multiple tasks
gradle(tasks: ["clean", "assembleRelease"])
```

**Key Parameters:**
- `task` / `tasks`: Gradle task(s) to run
- `project_dir`: Android project directory
- `build_type`: Build type (release, debug)
- `flavor`: Product flavor
- `properties`: Gradle properties hash
- `flags`: Additional Gradle flags

## xcodebuild

Direct xcodebuild command execution.

```ruby
xcodebuild(
  workspace: "MyApp.xcworkspace",
  scheme: "MyApp",
  configuration: "Release",
  build_settings: {
    "CODE_SIGN_IDENTITY" => "iPhone Distribution"
  },
  xcargs: "-allowProvisioningUpdates"
)
```

## cocoapods

Run pod install/update.

```ruby
cocoapods(
  podfile: "./ios/Podfile",
  repo_update: true,
  clean_install: true,
  deployment: true  # Uses Podfile.lock versions
)
```

## carthage

Build dependencies with Carthage.

```ruby
carthage(
  command: "bootstrap",  # bootstrap, update, build
  platform: "iOS",
  cache_builds: true,
  use_xcframeworks: true
)
```

## spm

Swift Package Manager operations.

```ruby
spm(
  command: "resolve",  # resolve, update, build, test
  build_path: ".build",
  configuration: "release"
)
```

## create_xcframework

Create XCFramework from multiple architectures.

```ruby
create_xcframework(
  frameworks: [
    "build/iOS/MyFramework.framework",
    "build/iOS-Simulator/MyFramework.framework"
  ],
  output: "build/MyFramework.xcframework"
)
```

## xcodes

Ensure specific Xcode version is installed.

```ruby
xcodes(
  version: "15.0",
  select_for_current_build_only: true
)
```

## clear_derived_data

Delete Xcode's DerivedData folder.

```ruby
clear_derived_data(derived_data_path: "~/Library/Developer/Xcode/DerivedData")
```

## adb

Run ADB commands for Android.

```ruby
adb(command: "install app.apk")
adb(command: "shell am start -n com.example/.MainActivity")
```
