# Build Flavors and Configurations

Complete guide to implementing build flavors and environment-specific configurations in Flutter applications.

## Overview

Build flavors (also called build variants) allow you to create different versions of your app from a single codebase. This enables you to maintain separate configurations for development, staging, and production environments with different API endpoints, app names, icons, feature flags, and build settings—all from one project.

## Why Use Flavors

### Common Use Cases

**Environment Management:**
- Development environment with debug tools
- Staging environment for QA testing
- Production environment for end users

**Multi-Tenancy:**
- White-label apps for different clients
- Regional variants with different branding
- Free and paid versions with different features

**Testing:**
- Mock data vs. real data
- Beta features enabled/disabled
- Different analytics configurations

**Operational Benefits:**
- Install multiple versions simultaneously on one device
- Visual differentiation (different names/icons)
- Separate crash reports per environment
- Environment-specific logging levels

## Build Variants vs Build Modes

**Important distinction:**

**Build Modes** (debug, profile, release):
- Flutter compilation modes
- Determined by `flutter run --release`, `flutter build apk`, etc.
- Control optimization level and debugging capabilities

**Build Flavors** (dev, staging, prod):
- Environment configurations
- Determined by `--flavor` flag
- Control API endpoints, app identity, features

**Combinations:**
```bash
flutter run --flavor dev --debug          # Dev environment, debug mode
flutter run --flavor staging --profile    # Staging environment, profile mode
flutter build apk --flavor prod --release # Prod environment, release mode
```

## Android Flavor Configuration

### Basic Setup

Edit `android/app/build.gradle.kts`:

```kotlin
android {
    namespace = "com.example.myapp"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    defaultConfig {
        applicationId = "com.example.myapp"
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutterVersionCode.toInteger()
        versionName = flutterVersionName
    }

    // Define flavor dimensions
    flavorDimensions += "environment"

    // Define product flavors
    productFlavors {
        create("dev") {
            dimension = "environment"
            applicationIdSuffix = ".dev"
            versionNameSuffix = "-dev"
            resValue("string", "app_name", "MyApp Dev")
            buildConfigField("String", "API_URL", "\"https://dev-api.example.com\"")
        }

        create("staging") {
            dimension = "environment"
            applicationIdSuffix = ".staging"
            versionNameSuffix = "-staging"
            resValue("string", "app_name", "MyApp Staging")
            buildConfigField("String", "API_URL", "\"https://staging-api.example.com\"")
        }

        create("prod") {
            dimension = "environment"
            // No suffix for production
            resValue("string", "app_name", "MyApp")
            buildConfigField("String", "API_URL", "\"https://api.example.com\"")
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

### Key Configuration Options

**`applicationIdSuffix`** - Appends to application ID:
```kotlin
applicationIdSuffix = ".dev"
// com.example.myapp → com.example.myapp.dev
```

Allows multiple flavors installed simultaneously on one device.

**`versionNameSuffix`** - Appends to version name:
```kotlin
versionNameSuffix = "-dev"
// 1.0.0 → 1.0.0-dev
```

Helps identify flavor in crash reports and analytics.

**`resValue`** - Defines resource values:
```kotlin
resValue("string", "app_name", "MyApp Dev")
```

Creates string resource accessible in AndroidManifest.xml and code.

**`buildConfigField`** - Defines compile-time constants:
```kotlin
buildConfigField("String", "API_URL", "\"https://dev-api.example.com\"")
```

Accessible in Kotlin/Java code as `BuildConfig.API_URL`.

### AndroidManifest Configuration

Update `android/app/src/main/AndroidManifest.xml` to use flavor-specific app name:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:label="@string/app_name"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher">

        <!-- Activities and other components -->

    </application>
</manifest>
```

The `@string/app_name` reference is resolved to the flavor-specific value defined in `resValue`.

### Flavor-Specific Icons

Create separate icon resources for each flavor:

```
android/app/src/
├── main/
│   └── res/
│       ├── mipmap-hdpi/ic_launcher.png    # Default icons
│       ├── mipmap-mdpi/ic_launcher.png
│       └── ...
├── dev/
│   └── res/
│       ├── mipmap-hdpi/ic_launcher.png    # Dev icons (e.g., blue)
│       ├── mipmap-mdpi/ic_launcher.png
│       └── ...
├── staging/
│   └── res/
│       ├── mipmap-hdpi/ic_launcher.png    # Staging icons (e.g., orange)
│       ├── mipmap-mdpi/ic_launcher.png
│       └── ...
└── prod/
    └── res/
        ├── mipmap-hdpi/ic_launcher.png    # Production icons
        ├── mipmap-mdpi/ic_launcher.png
        └── ...
```

**Required sizes:**
- `mipmap-mdpi/` - 48x48 px
- `mipmap-hdpi/` - 72x72 px
- `mipmap-xhdpi/` - 96x96 px
- `mipmap-xxhdpi/` - 144x144 px
- `mipmap-xxxhdpi/` - 192x192 px

Android automatically selects the appropriate icon based on the active flavor.

### Flavor-Specific Assets

Bundle different assets per flavor:

```
android/app/src/
├── dev/
│   └── assets/
│       └── config.json
├── staging/
│   └── assets/
│       └── config.json
└── prod/
    └── assets/
        └── config.json
```

Assets in flavor-specific directories override those in `main/assets/`.

### Multiple Dimensions

Use multiple flavor dimensions for complex configurations:

```kotlin
flavorDimensions += listOf("environment", "audience")

productFlavors {
    // Environment dimension
    create("dev") {
        dimension = "environment"
        applicationIdSuffix = ".dev"
    }
    create("prod") {
        dimension = "environment"
    }

    // Audience dimension
    create("free") {
        dimension = "audience"
        applicationIdSuffix = ".free"
        buildConfigField("Boolean", "PREMIUM_FEATURES", "false")
    }
    create("premium") {
        dimension = "audience"
        applicationIdSuffix = ".premium"
        buildConfigField("Boolean", "PREMIUM_FEATURES", "true")
    }
}
```

This creates build variants:
- `devFreeDebug`, `devFreeRelease`
- `devPremiumDebug`, `devPremiumRelease`
- `prodFreeDebug`, `prodFreeRelease`
- `prodPremiumDebug`, `prodPremiumRelease`

## iOS Flavor Configuration

### Xcode Schemes and Configurations

iOS uses **Schemes** and **Build Configurations** for flavors.

**Steps:**

1. **Open Xcode workspace:**
```bash
open ios/Runner.xcworkspace
```

2. **Duplicate configurations:**

Select **Runner** project → **Info** tab → **Configurations**

Duplicate `Debug` and `Release` configurations for each flavor:
- Debug-dev, Release-dev
- Debug-staging, Release-staging
- Debug-prod, Release-prod

3. **Create schemes:**

**Product** → **Scheme** → **Manage Schemes**

Click **+** to create new scheme for each flavor:

**Dev Scheme:**
- Name: dev
- Run: Debug-dev
- Test: Debug-dev
- Profile: Release-dev
- Analyze: Debug-dev
- Archive: Release-dev

**Staging Scheme:**
- Name: staging
- Run: Debug-staging
- Test: Debug-staging
- Profile: Release-staging
- Analyze: Debug-staging
- Archive: Release-staging

**Prod Scheme:**
- Name: prod
- Run: Debug-prod
- Test: Debug-prod
- Profile: Release-prod
- Analyze: Debug-prod
- Archive: Release-prod

**Mark schemes as "Shared"** by checking the "Shared" checkbox so they're committed to version control.

4. **Configure build settings per configuration:**

Select **Runner** target → **Build Settings** tab

Add user-defined settings:

| Setting | Debug-dev | Debug-staging | Debug-prod | Release-dev | Release-staging | Release-prod |
|---------|-----------|---------------|------------|-------------|-----------------|--------------|
| APP_DISPLAY_NAME | MyApp Dev | MyApp Staging | MyApp | MyApp Dev | MyApp Staging | MyApp |
| APP_BUNDLE_ID | com.example.myapp.dev | com.example.myapp.staging | com.example.myapp | com.example.myapp.dev | com.example.myapp.staging | com.example.myapp |

5. **Update Info.plist to use build settings:**

Edit `ios/Runner/Info.plist`:

```xml
<key>CFBundleDisplayName</key>
<string>$(APP_DISPLAY_NAME)</string>

<key>CFBundleIdentifier</key>
<string>$(APP_BUNDLE_ID)</string>
```

6. **Create configuration files:**

Create `ios/Flutter/Dev.xcconfig`:

```
#include "Generated.xcconfig"

APP_DISPLAY_NAME = MyApp Dev
APP_BUNDLE_ID = com.example.myapp.dev
```

Create `ios/Flutter/Staging.xcconfig`:

```
#include "Generated.xcconfig"

APP_DISPLAY_NAME = MyApp Staging
APP_BUNDLE_ID = com.example.myapp.staging
```

Create `ios/Flutter/Prod.xcconfig`:

```
#include "Generated.xcconfig"

APP_DISPLAY_NAME = MyApp
APP_BUNDLE_ID = com.example.myapp
```

7. **Link xcconfig files to configurations:**

Select **Runner** project → **Info** tab → **Configurations**

Set configurations to use respective xcconfig files:
- Debug-dev → Dev
- Release-dev → Dev
- Debug-staging → Staging
- Release-staging → Staging
- Debug-prod → Prod
- Release-prod → Prod

### Flavor-Specific Icons (iOS)

Create separate asset catalogs for each flavor:

1. Duplicate `Assets.xcassets`:
   - `Assets-Dev.xcassets`
   - `Assets-Staging.xcassets`
   - `Assets-Prod.xcassets`

2. Add different icons to each asset catalog

3. Configure build settings to use flavor-specific asset catalogs:

Select **Runner** target → **Build Settings** → Search "Asset Catalog"

Set **ASSETCATALOG_COMPILER_APPICON_NAME** per configuration:
- Debug-dev: AppIcon-Dev
- Debug-staging: AppIcon-Staging
- Debug-prod: AppIcon

### Alternative: Flutter Flavorizr

Automate flavor setup with the **flutter_flavorizr** package:

Add to `pubspec.yaml`:

```yaml
dev_dependencies:
  flutter_flavorizr: ^2.2.3

flavorizr:
  app:
    android:
      flavorDimensions: "environment"
    ios:

  flavors:
    dev:
      app:
        name: "MyApp Dev"
      android:
        applicationId: "com.example.myapp.dev"
        icon: "assets/icons/icon_dev.png"
      ios:
        bundleId: "com.example.myapp.dev"
        icon: "assets/icons/icon_dev.png"

    staging:
      app:
        name: "MyApp Staging"
      android:
        applicationId: "com.example.myapp.staging"
        icon: "assets/icons/icon_staging.png"
      ios:
        bundleId: "com.example.myapp.staging"
        icon: "assets/icons/icon_staging.png"

    prod:
      app:
        name: "MyApp"
      android:
        applicationId: "com.example.myapp"
        icon: "assets/icons/icon_prod.png"
      ios:
        bundleId: "com.example.myapp"
        icon: "assets/icons/icon_prod.png"
```

Run:

```bash
flutter pub get
flutter pub run flutter_flavorizr
```

This automatically configures Android and iOS flavors based on your specification.

## Flutter/Dart Configuration

### Passing Flavor to Dart Code

**Option 1: Entry point parameters**

Create separate entry points for each flavor:

`lib/main_dev.dart`:
```dart
import 'package:flutter/material.dart';
import 'app.dart';
import 'config/env_config.dart';

void main() {
  EnvConfig.init(Environment.dev);
  runApp(const MyApp());
}
```

`lib/main_staging.dart`:
```dart
import 'package:flutter/material.dart';
import 'app.dart';
import 'config/env_config.dart';

void main() {
  EnvConfig.init(Environment.staging);
  runApp(const MyApp());
}
```

`lib/main_prod.dart`:
```dart
import 'package:flutter/material.dart';
import 'app.dart';
import 'config/env_config.dart';

void main() {
  EnvConfig.init(Environment.prod);
  runApp(const MyApp());
}
```

**Update build configuration:**

For Android, edit `android/app/build.gradle.kts`:

```kotlin
productFlavors {
    create("dev") {
        // ...existing config...
        buildConfigField("String", "FLUTTER_TARGET", "\"lib/main_dev.dart\"")
    }
    create("staging") {
        buildConfigField("String", "FLUTTER_TARGET", "\"lib/main_staging.dart\"")
    }
    create("prod") {
        buildConfigField("String", "FLUTTER_TARGET", "\"lib/main_prod.dart\"")
    }
}
```

**Run with target:**
```bash
flutter run --flavor dev --target lib/main_dev.dart
```

**Option 2: Compile-time constants**

Use `--dart-define` to pass values:

```bash
flutter run --flavor dev --dart-define=ENVIRONMENT=dev
flutter build apk --flavor prod --dart-define=ENVIRONMENT=prod
```

Access in Dart:

```dart
const environment = String.fromEnvironment('ENVIRONMENT', defaultValue: 'prod');

void main() {
  print('Running in $environment environment');
  runApp(const MyApp());
}
```

**Option 3: Configuration files**

Create configuration files per flavor:

`assets/config/dev.json`:
```json
{
  "apiUrl": "https://dev-api.example.com",
  "apiKey": "dev-key-123",
  "analyticsEnabled": false,
  "logLevel": "debug"
}
```

`assets/config/prod.json`:
```json
{
  "apiUrl": "https://api.example.com",
  "apiKey": "prod-key-456",
  "analyticsEnabled": true,
  "logLevel": "error"
}
```

Load at runtime:

```dart
import 'dart:convert';
import 'package:flutter/services.dart';

class Config {
  final String apiUrl;
  final String apiKey;
  final bool analyticsEnabled;
  final String logLevel;

  Config({
    required this.apiUrl,
    required this.apiKey,
    required this.analyticsEnabled,
    required this.logLevel,
  });

  static late Config instance;

  static Future<void> load(String flavor) async {
    final configString = await rootBundle.loadString('assets/config/$flavor.json');
    final configJson = json.decode(configString);
    instance = Config(
      apiUrl: configJson['apiUrl'],
      apiKey: configJson['apiKey'],
      analyticsEnabled: configJson['analyticsEnabled'],
      logLevel: configJson['logLevel'],
    );
  }
}

// In main:
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Config.load('dev'); // Or pass from dart-define
  runApp(const MyApp());
}
```

### Environment Configuration Class

Create centralized configuration:

`lib/config/env_config.dart`:

```dart
enum Environment { dev, staging, prod }

class EnvConfig {
  static late Environment _environment;
  static late String _apiUrl;
  static late String _apiKey;
  static late bool _analyticsEnabled;

  static void init(Environment env) {
    _environment = env;

    switch (env) {
      case Environment.dev:
        _apiUrl = 'https://dev-api.example.com';
        _apiKey = 'dev-key-123';
        _analyticsEnabled = false;
        break;
      case Environment.staging:
        _apiUrl = 'https://staging-api.example.com';
        _apiKey = 'staging-key-456';
        _analyticsEnabled = true;
        break;
      case Environment.prod:
        _apiUrl = 'https://api.example.com';
        _apiKey = 'prod-key-789';
        _analyticsEnabled = true;
        break;
    }
  }

  static Environment get environment => _environment;
  static String get apiUrl => _apiUrl;
  static String get apiKey => _apiKey;
  static bool get analyticsEnabled => _analyticsEnabled;

  static bool get isDev => _environment == Environment.dev;
  static bool get isStaging => _environment == Environment.staging;
  static bool get isProd => _environment == Environment.prod;
}
```

Usage:

```dart
import 'package:http/http.dart' as http;
import 'config/env_config.dart';

Future<void> fetchData() async {
  final response = await http.get(
    Uri.parse('${EnvConfig.apiUrl}/data'),
    headers: {'Authorization': 'Bearer ${EnvConfig.apiKey}'},
  );

  if (EnvConfig.isDev) {
    print('Response: ${response.body}');
  }
}
```

## Running and Building with Flavors

### Development

```bash
# Run dev flavor
flutter run --flavor dev

# Run dev flavor with specific target
flutter run --flavor dev --target lib/main_dev.dart

# Run staging on specific device
flutter run --flavor staging -d <device-id>
```

### Building

**Android:**
```bash
# Build APK
flutter build apk --flavor dev --release
flutter build apk --flavor prod --release

# Build App Bundle
flutter build appbundle --flavor staging --release

# Build split APKs
flutter build apk --flavor prod --split-per-abi --release
```

**iOS:**
```bash
# Build IPA
flutter build ipa --flavor dev --release
flutter build ipa --flavor prod --release

# Build for specific scheme in Xcode
# Product → Scheme → Select "dev"
# Product → Archive
```

### Set Default Flavor

Add to `pubspec.yaml`:

```yaml
flutter:
  default-flavor: dev
```

Now `flutter run` uses dev flavor by default.

## Advanced Flavor Techniques

### Feature Flags

Toggle features per flavor:

```dart
class Features {
  static bool get debugTools => EnvConfig.isDev;
  static bool get betaFeatures => EnvConfig.isDev || EnvConfig.isStaging;
  static bool get analytics => EnvConfig.isProd;
  static bool get crashReporting => !EnvConfig.isDev;
}

// Usage:
if (Features.debugTools) {
  return DebugToolsWidget();
}
```

### Conditional UI

Show environment indicator:

```dart
class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      home: Stack(
        children: [
          HomePage(),
          if (EnvConfig.isDev || EnvConfig.isStaging)
            Positioned(
              bottom: 0,
              left: 0,
              right: 0,
              child: Container(
                color: EnvConfig.isDev ? Colors.red : Colors.orange,
                padding: EdgeInsets.all(4),
                child: Text(
                  '${EnvConfig.environment.name.toUpperCase()} ENVIRONMENT',
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                ),
              ),
            ),
        ],
      ),
    );
  }
}
```

### Logging Configuration

Adjust logging per flavor:

```dart
import 'package:logger/logger.dart';

Logger createLogger() {
  return Logger(
    level: EnvConfig.isDev ? Level.debug : Level.error,
    printer: PrettyPrinter(
      methodCount: EnvConfig.isDev ? 2 : 0,
      errorMethodCount: 5,
      lineLength: 120,
      colors: true,
      printEmojis: true,
      printTime: true,
    ),
  );
}
```

### Mock Data

Use mock data in development:

```dart
abstract class ApiService {
  Future<List<User>> getUsers();
}

class RealApiService implements ApiService {
  @override
  Future<List<User>> getUsers() async {
    final response = await http.get(Uri.parse('${EnvConfig.apiUrl}/users'));
    return parseUsers(response.body);
  }
}

class MockApiService implements ApiService {
  @override
  Future<List<User>> getUsers() async {
    await Future.delayed(Duration(seconds: 1));
    return [
      User(id: 1, name: 'Mock User 1'),
      User(id: 2, name: 'Mock User 2'),
    ];
  }
}

// In app initialization:
final apiService = EnvConfig.isDev ? MockApiService() : RealApiService();
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Build Flavors

on: [push, pull_request]

jobs:
  build-android:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        flavor: [dev, staging, prod]
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2

      - run: flutter pub get
      - run: flutter build apk --flavor ${{ matrix.flavor }} --release

      - uses: actions/upload-artifact@v3
        with:
          name: android-${{ matrix.flavor }}
          path: build/app/outputs/apk/${{ matrix.flavor }}/release/

  build-ios:
    runs-on: macos-latest
    strategy:
      matrix:
        flavor: [dev, staging, prod]
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2

      - run: flutter pub get
      - run: flutter build ios --flavor ${{ matrix.flavor }} --release --no-codesign

      - uses: actions/upload-artifact@v3
        with:
          name: ios-${{ matrix.flavor }}
          path: build/ios/iphoneos/
```

### Fastlane

`android/fastlane/Fastfile`:

```ruby
lane :build_all_flavors do
  ['dev', 'staging', 'prod'].each do |flavor|
    gradle(
      task: 'assemble',
      flavor: flavor,
      build_type: 'Release'
    )
  end
end

lane :deploy_flavor do |options|
  flavor = options[:flavor]
  gradle(
    task: 'bundle',
    flavor: flavor,
    build_type: 'Release'
  )
  upload_to_play_store(
    track: flavor == 'prod' ? 'production' : 'internal',
    aab: "app/build/outputs/bundle/#{flavor}Release/app-#{flavor}-release.aab"
  )
end
```

Run:
```bash
cd android
fastlane build_all_flavors
fastlane deploy_flavor flavor:prod
```

## Best Practices

### Naming Conventions

- Use lowercase for flavor names: `dev`, `staging`, `prod`
- Be consistent across Android and iOS
- Use descriptive suffixes: `.dev`, `.staging`
- Avoid generic names that might conflict

### Security

- **Never commit API keys or secrets** to version control
- Use environment variables in CI/CD for sensitive values
- Store production secrets separately from development
- Use different Firebase projects per flavor
- Rotate keys regularly

### Organization

- Keep flavor-specific code minimal
- Use dependency injection to swap implementations
- Centralize configuration in one class
- Document flavor differences clearly
- Test all flavors before releases

### Version Management

- Use consistent versioning across flavors
- Consider flavor-specific version suffixes
- Increment versions appropriately for each flavor
- Tag releases per flavor: `dev/1.0.0`, `prod/1.0.0`

### Testing

- Test each flavor independently
- Verify flavor-specific features work correctly
- Check correct API endpoints are used
- Ensure icons and names are correct
- Test simultaneous installation of multiple flavors

## Common Issues and Solutions

### Flavor Not Found

**Problem:** "No flavor with name 'dev' exists"

**Solutions:**
- Verify flavor defined in `build.gradle.kts`
- Check spelling matches exactly (case-sensitive)
- Run `flutter clean` and rebuild

### Wrong App Name Displayed

**Problem:** App shows default name instead of flavor name

**Solutions:**
- Verify `resValue` in Android or build setting in iOS
- Check AndroidManifest uses `@string/app_name`
- Clean and rebuild project

### Cannot Install Multiple Flavors

**Problem:** Installing one flavor uninstalls another

**Solutions:**
- Verify each flavor has unique `applicationId` (Android) or `bundleId` (iOS)
- Check suffixes are applied correctly
- Confirm package names don't conflict

### Build Fails After Adding Flavors

**Problem:** Build errors after flavor configuration

**Solutions:**
- Run `flutter clean`
- Delete `build/` directory
- Invalidate caches in Android Studio/Xcode
- Verify all flavor configurations are complete

## Quick Reference

### Commands

```bash
# Run flavors
flutter run --flavor dev
flutter run --flavor staging --target lib/main_staging.dart

# Build flavors
flutter build apk --flavor prod --release
flutter build appbundle --flavor staging --release
flutter build ipa --flavor dev --release

# Build with dart-define
flutter run --flavor dev --dart-define=ENVIRONMENT=dev
flutter build apk --flavor prod --dart-define=ENVIRONMENT=prod --release

# Set default
flutter config default-flavor dev
```

### Configuration Checklist

Android:
- [ ] Flavor dimensions defined
- [ ] Product flavors configured
- [ ] Application ID suffixes set
- [ ] App names configured
- [ ] Icons created per flavor
- [ ] AndroidManifest uses `@string/app_name`

iOS:
- [ ] Build configurations duplicated
- [ ] Schemes created for each flavor
- [ ] xcconfig files created
- [ ] Info.plist uses build settings
- [ ] Icons configured per flavor
- [ ] Schemes marked as shared

Flutter:
- [ ] Entry points created or dart-defines used
- [ ] Configuration class implemented
- [ ] Environment-specific values set
- [ ] Default flavor configured (optional)

## Resources

- [Flutter Android Flavors](https://docs.flutter.dev/deployment/flavors)
- [Flutter iOS Flavors](https://docs.flutter.dev/deployment/flavors-ios)
- [flutter_flavorizr Package](https://pub.dev/packages/flutter_flavorizr)
- [Android Product Flavors](https://developer.android.com/studio/build/build-variants)

## Summary

Build flavors enable powerful environment management in Flutter apps, allowing you to maintain separate configurations for development, staging, and production from a single codebase. By properly configuring Android product flavors, iOS schemes, and Flutter/Dart configurations, you can streamline your development workflow, simplify testing, and safely deploy to production. Remember to keep configurations centralized, secure sensitive data, and test all flavors thoroughly before release. Flavors are essential for professional Flutter app development and significantly improve operational efficiency.
