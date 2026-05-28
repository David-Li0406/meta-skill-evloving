---
name: android-deployment
description: Android deployment workflow for Flutter apps. Use when configuring Gradle builds, setting up signing keys, creating release builds, managing Play Store listings, or publishing to Google Play. Includes Fastlane automation, AAB generation, and CI/CD integration.
---

# Android Deployment

## Overview

Complete Android deployment workflow for MagentaLine EFB, from development builds to Play Store publication.

## Quick Start

### Build APK

```bash
# Debug APK
flutter build apk --debug

# Release APK
flutter build apk --release

# Split APKs by ABI (smaller downloads)
flutter build apk --release --split-per-abi
```

### Build App Bundle (Play Store)

```bash
# AAB for Play Store (recommended)
flutter build appbundle --release

# With version
flutter build appbundle --release --build-number=42 --build-name=1.2.0
```

### Deploy to Play Store

```bash
# With Fastlane
cd android && fastlane deploy

# Internal testing track
cd android && fastlane internal
```

## Signing Configuration

### Generate Keystore

```bash
keytool -genkey -v -keystore android/app/upload-keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias magentaline \
  -dname "CN=MagentaLine, O=MagentaLine, L=City, ST=State, C=US"
```

### Key Properties File

```properties
# android/key.properties (DO NOT commit to git)
storePassword=your_store_password
keyPassword=your_key_password
keyAlias=magentaline
storeFile=upload-keystore.jks
```

### Gradle Signing Config

```groovy
// android/app/build.gradle

def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

## Gradle Configuration

### App Level build.gradle

```groovy
// android/app/build.gradle

android {
    namespace "com.magentaline.app"
    compileSdkVersion 34

    defaultConfig {
        applicationId "com.magentaline.app"
        minSdkVersion 23  // Android 6.0+ for EFB features
        targetSdkVersion 34
        versionCode flutterVersionCode.toInteger()
        versionName flutterVersionName

        // Required for location background service
        ndk {
            abiFilters 'armeabi-v7a', 'arm64-v8a', 'x86_64'
        }
    }

    buildTypes {
        debug {
            applicationIdSuffix ".debug"
            versionNameSuffix "-debug"
        }
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

### ProGuard Rules

```pro
# android/app/proguard-rules.pro

# Flutter
-keep class io.flutter.** { *; }
-keep class io.flutter.plugins.** { *; }

# Keep native methods
-keepclasseswithmembernames class * {
    native <methods>;
}

# Stratux/GDL90 UDP parsing
-keep class com.magentaline.gdl90.** { *; }

# SQLite/SpatiaLite
-keep class org.spatialite.** { *; }

# Location services
-keep class com.google.android.gms.location.** { *; }
```

## Permissions

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <!-- Internet for weather, charts -->
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>

    <!-- Location for moving map -->
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
    <uses-permission android:name="android.permission.ACCESS_BACKGROUND_LOCATION"/>

    <!-- Stratux WiFi connection -->
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
    <uses-permission android:name="android.permission.CHANGE_WIFI_STATE"/>

    <!-- Keep screen on during flight -->
    <uses-permission android:name="android.permission.WAKE_LOCK"/>

    <!-- Foreground service for tracking -->
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE"/>
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_LOCATION"/>

    <application
        android:label="MagentaLine"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher">
        <!-- ... -->

        <!-- Background location service -->
        <service
            android:name=".LocationService"
            android:foregroundServiceType="location"
            android:exported="false"/>
    </application>
</manifest>
```

## Fastlane Setup

See `references/fastlane_android.md` for complete configuration.

```ruby
# android/fastlane/Fastfile
default_platform(:android)

platform :android do
  desc "Deploy to internal testing"
  lane :internal do
    gradle(
      task: "clean bundleRelease",
      project_dir: "./"
    )
    upload_to_play_store(
      track: "internal",
      aab: "../build/app/outputs/bundle/release/app-release.aab"
    )
  end

  desc "Deploy to production"
  lane :deploy do
    gradle(task: "clean bundleRelease")
    upload_to_play_store(
      track: "production",
      aab: "../build/app/outputs/bundle/release/app-release.aab"
    )
  end
end
```

## Play Store Configuration

### Required Assets

| Asset | Specs |
|-------|-------|
| App Icon | 512x512 PNG |
| Feature Graphic | 1024x500 PNG |
| Screenshots | Min 2, various sizes |
| Privacy Policy | URL required |

### Store Listing

```
# android/fastlane/metadata/android/en-US/

full_description.txt
short_description.txt
title.txt
changelogs/
  default.txt
  42.txt  # Version-specific
images/
  featureGraphic.png
  icon.png
  phoneScreenshots/
  sevenInchScreenshots/
  tenInchScreenshots/
```

## CI/CD Integration

```yaml
# .github/workflows/android.yml
jobs:
  android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Setup Flutter
        uses: subosito/flutter-action@v2

      - name: Decode keystore
        env:
          KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
        run: echo "$KEYSTORE_BASE64" | base64 -d > android/app/upload-keystore.jks

      - name: Create key.properties
        run: |
          echo "storePassword=${{ secrets.STORE_PASSWORD }}" >> android/key.properties
          echo "keyPassword=${{ secrets.KEY_PASSWORD }}" >> android/key.properties
          echo "keyAlias=magentaline" >> android/key.properties
          echo "storeFile=upload-keystore.jks" >> android/key.properties

      - name: Build AAB
        run: flutter build appbundle --release

      - name: Upload to Play Store
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.PLAY_STORE_JSON }}
          packageName: com.magentaline.app
          releaseFiles: build/app/outputs/bundle/release/app-release.aab
          track: internal
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Signing failed | Verify key.properties path and passwords |
| Gradle sync failed | `./gradlew clean` then rebuild |
| ProGuard issues | Add keep rules for affected classes |
| AAB too large | Enable `shrinkResources`, use split APKs |

## References

| Document | Description |
|----------|-------------|
| `references/fastlane_android.md` | Complete Fastlane setup |
| `references/play_store_listing.md` | Store listing guide |
| `assets/build.gradle` | Sample Gradle config |
| `assets/proguard-rules.pro` | ProGuard template |
