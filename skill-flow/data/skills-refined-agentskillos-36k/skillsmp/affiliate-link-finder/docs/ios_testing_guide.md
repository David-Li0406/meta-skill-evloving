# Testing on iOS

This guide outlines the steps to build and test the ADHD Supplement App on iOS devices or simulators.

## Prerequisites
1.  **Xcode**: Ensure you have Xcode installed (from the Mac App Store).
2.  **CocoaPods**: Ensure CocoaPods is installed (`brew install cocoapods` is recommended on Apple Silicon).
3.  **Firebase Configuration**: You must have `GoogleService-Info.plist` in `ios/Runner/`.

## Setup Steps

### 1. Verify Firebase Configuration
Ensure your `GoogleService-Info.plist` file is present in `ios/Runner/`. This file links the app to your Firebase project.
- If missing, download it from the Firebase Console (Settings > Project Settings > Your Apps > iOS).
- Drag and drop it into `ios/Runner/` via Finder or Xcode (ensure it's added to the "Runner" target).

### 2. Install Dependencies
Run the following commands in your terminal to install Flutter and iOS dependencies:

```bash
flutter pub get
cd ios
pod install
cd ..
```

### 3. Open Simulator
Open a simulator via terminal or Xcode:
```bash
open -a Simulator
```

### 4. Run the App
To run the app on the active simulator:
```bash
flutter run
```

## Troubleshooting
- **"Module 'firebase_core' not found"**: Run `pod install` in the `ios` directory again. Update your Podfile `platform :ios` version if needed (uncomment line 2 to specific `platform :ios, '13.0'`).
- **Duplicate Plist Error**: If you see `Multiple commands produce GoogleService-Info.plist`, ensure there is only one reference to this file in the `project.pbxproj`.
- **Swift Compiler Errors (app_settings)**: The `app_settings` package can cause Swift version errors. We've switched to `url_launcher` for opening settings to avoid this.
- **Firebase Swift 6 Incompatibility**: If you see errors like `Cannot find type 'sending' in scope` in Firebase pods, it means the Firebase version is too new for your Xcode/Swift version. We've pinned the versions in `pubspec.yaml` to remain compatible with Swift 5.
- **Simulators Not Detected**: If `flutter run` doesn't see your simulators, run `sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer` and `sudo xcodebuild -runFirstLaunch`.
- **Signing Issues**: Open `ios/Runner.xcworkspace` in Xcode. Go to **Runner > Signing & Capabilities** and ensure a Team is selected.

## Testing the New Data Integration
Once the app is running on iOS:
1.  **Log In**: Use a fresh account or existing one.
2.  **Verify Articles**: Go to the "Library" or "Home" tab to see if articles load.
3.  **Verify Badges**: Navigate to the Profile. Check if badges unlock after 7 days (simulated) or if your level is high enough.
