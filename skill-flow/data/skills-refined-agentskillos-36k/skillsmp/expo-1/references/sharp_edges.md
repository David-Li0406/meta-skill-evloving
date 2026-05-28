# Expo - Sharp Edges

## Expo Go Native Limits

### **Id**
expo-go-native-limits
### **Summary**
Native module not working in Expo Go
### **Severity**
high
### **Situation**
Library crashes or doesn't load in Expo Go
### **Why**
  Expo Go has fixed native modules.
  Custom native code needs dev build.
  Some libraries need config plugins.
  
### **Solution**
  # Check if library needs native code
  # Look for "native" or "pod" in installation docs
  
  # Option 1: Use Expo-compatible alternative
  # BAD
  npm install react-native-ble-plx
  # GOOD
  npx expo install expo-bluetooth  # If available
  
  # Option 2: Create development build
  # Install the library
  npx expo install react-native-ble-plx
  
  # Add config plugin if needed (check library docs)
  // app.json
  {
    "expo": {
      "plugins": ["react-native-ble-plx"]
    }
  }
  
  # Build development client
  eas build --platform ios --profile development
  
  # Install on device
  # Then run: npx expo start --dev-client
  
  # Check Expo compatibility
  # https://reactnative.directory/?expo=true
  
  # Common libraries that need dev builds:
  # - react-native-ble-plx
  # - react-native-maps (with custom config)
  # - react-native-video
  # - Any library with native code not in Expo SDK
  
### **Symptoms**
  - Native module not found
  - App crashes on import
  - White screen on device
### **Detection Pattern**
NativeModules|requireNativeComponent

## Eas Build Credentials

### **Id**
eas-build-credentials
### **Summary**
Build fails with signing/credentials error
### **Severity**
high
### **Situation**
EAS build fails on iOS or Android
### **Why**
  Missing or expired certificates.
  Wrong provisioning profile.
  Keystore issues.
  
### **Solution**
  # iOS: Let EAS manage credentials (recommended)
  eas credentials
  
  # Or configure manually
  eas build:configure
  
  # Clear credentials and regenerate
  eas credentials --platform ios
  # Select "Remove" then build again
  
  # Android: Set up keystore
  eas credentials --platform android
  # EAS can generate or you can provide existing
  
  # For App Store submission
  # Need Apple Developer account ($99/year)
  # EAS creates certificates automatically
  
  # Common fixes:
  # 1. Expired certificate: regenerate in eas credentials
  # 2. Wrong bundle ID: check app.json bundleIdentifier
  # 3. Team mismatch: verify Apple Developer account
  
  # eas.json for manual credentials
  {
    "build": {
      "production": {
        "ios": {
          "credentialsSource": "local",
          "provisioningProfilePath": "./certs/profile.mobileprovision",
          "distributionCertificate": {
            "path": "./certs/dist.p12",
            "password": "@env:CERT_PASSWORD"
          }
        }
      }
    }
  }
  
### **Symptoms**
  - No matching provisioning profile
  - Code signing error
  - Keystore not found
### **Detection Pattern**
credentialsSource|provisioningProfile

## Metro Cache Stale

### **Id**
metro-cache-stale
### **Summary**
Changes not reflected, weird behavior
### **Severity**
medium
### **Situation**
App shows old code or crashes unexpectedly
### **Why**
  Metro bundler caches aggressively.
  Node modules cache stale.
  Watchman has old state.
  
### **Solution**
  # Clear Metro cache
  npx expo start --clear
  
  # Full cache clear
  rm -rf node_modules
  rm -rf .expo
  npm install
  npx expo start --clear
  
  # Clear watchman (macOS)
  watchman watch-del-all
  
  # Reset Metro bundler
  npx react-native start --reset-cache
  
  # For persistent issues
  rm -rf ~/Library/Developer/Xcode/DerivedData  # iOS
  rm -rf android/.gradle  # Android
  
  # Clear EAS build cache (for builds)
  eas build --clear-cache --platform ios
  
  # Useful script in package.json
  {
    "scripts": {
      "clean": "rm -rf node_modules .expo && npm install && npx expo start --clear"
    }
  }
  
### **Symptoms**
  - Old code still running
  - Unable to resolve module
  - Random crashes after update
### **Detection Pattern**
start --clear|reset-cache

## Deep Linking Not Working

### **Id**
deep-linking-not-working
### **Summary**
Deep links don't open app
### **Severity**
medium
### **Situation**
URLs don't navigate to correct screen
### **Why**
  Missing scheme in app.json.
  Associated domains not configured.
  Wrong path pattern.
  
### **Solution**
  # 1. Configure scheme in app.json
  {
    "expo": {
      "scheme": "myapp",  // For myapp://
      "ios": {
        "bundleIdentifier": "com.company.myapp",
        "associatedDomains": ["applinks:myapp.com"]
      },
      "android": {
        "package": "com.company.myapp",
        "intentFilters": [
          {
            "action": "VIEW",
            "autoVerify": true,
            "data": [
              { "scheme": "https", "host": "myapp.com" }
            ],
            "category": ["BROWSABLE", "DEFAULT"]
          }
        ]
      }
    }
  }
  
  # 2. Handle in Expo Router (automatic!)
  # Links map to files:
  # myapp://user/123 → app/user/[id].tsx
  # https://myapp.com/product/456 → app/product/[id].tsx
  
  # 3. Test deep links
  # iOS Simulator
  xcrun simctl openurl booted "myapp://user/123"
  
  # Android Emulator
  adb shell am start -a android.intent.action.VIEW -d "myapp://user/123"
  
  # 4. Handle link in app
  import { useURL } from "expo-linking";
  import { router } from "expo-router";
  
  function App() {
    const url = useURL();
  
    useEffect(() => {
      if (url) {
        // Expo Router handles this automatically
        // Manual handling if needed:
        const { path, queryParams } = Linking.parse(url);
        router.push(path);
      }
    }, [url]);
  }
  
  # 5. For universal links (iOS) - need AASA file
  # Host at: https://myapp.com/.well-known/apple-app-site-association
  {
    "applinks": {
      "apps": [],
      "details": [
        {
          "appID": "TEAMID.com.company.myapp",
          "paths": ["/user/*", "/product/*"]
        }
      ]
    }
  }
  
### **Symptoms**
  - Links open browser instead of app
  - Wrong screen after link
  - No route found
### **Detection Pattern**
scheme|intentFilters|associatedDomains

## Ota Update Not Applying

### **Id**
ota-update-not-applying
### **Summary**
EAS Update published but app doesn't update
### **Severity**
medium
### **Situation**
Old version still showing after update
### **Why**
  Wrong channel.
  Runtime version mismatch.
  Update not fetched.
  
### **Solution**
  # 1. Check runtime version matches
  # app.json
  {
    "expo": {
      "runtimeVersion": "1.0.0"  // Must match built app
    }
  }
  
  # Or use policy (recommended)
  {
    "expo": {
      "runtimeVersion": {
        "policy": "appVersion"  // Uses version field
      }
    }
  }
  
  # 2. Check channel matches
  # eas.json
  {
    "build": {
      "production": {
        "channel": "production"  // Must match update channel
      }
    }
  }
  
  # Publish to correct channel
  eas update --channel production
  
  # 3. Force update check in app
  import * as Updates from "expo-updates";
  
  async function forceUpdate() {
    if (__DEV__) return;  // No updates in dev
  
    try {
      const update = await Updates.checkForUpdateAsync();
      console.log("Update available:", update.isAvailable);
  
      if (update.isAvailable) {
        const result = await Updates.fetchUpdateAsync();
        console.log("Update fetched:", result);
  
        // Reload to apply
        await Updates.reloadAsync();
      }
    } catch (e) {
      console.error("Update error:", e);
    }
  }
  
  # 4. Debug update status
  console.log("Update channel:", Updates.channel);
  console.log("Runtime version:", Updates.runtimeVersion);
  console.log("Is embedded:", Updates.isEmbeddedLaunch);
  
  # 5. Verify update published
  eas update:list --channel production
  
### **Symptoms**
  - App shows old version
  - No update available
  - Update fetched but not applied
### **Detection Pattern**
runtimeVersion|Updates\.

## Android Build Oom

### **Id**
android-build-oom
### **Summary**
Android build runs out of memory
### **Severity**
medium
### **Situation**
EAS Build fails with memory error
### **Why**
  Default Gradle memory too low.
  Large assets.
  Many dependencies.
  
### **Solution**
  # Increase Gradle memory
  // app.json
  {
    "expo": {
      "plugins": [
        [
          "expo-build-properties",
          {
            "android": {
              "extraMavenRepos": [],
              "extraProguardRules": "",
              "enableProguardInReleaseBuilds": true
            }
          }
        ]
      ]
    }
  }
  
  # android/gradle.properties (if bare workflow)
  org.gradle.jvmargs=-Xmx4096m -XX:MaxPermSize=512m
  
  # Use EAS large workers
  // eas.json
  {
    "build": {
      "production": {
        "android": {
          "resourceClass": "large"  // More memory
        }
      }
    }
  }
  
  # Optimize assets
  npx expo-optimize  # Compresses images
  
  # Enable Proguard (shrinks app)
  // app.json plugins
  [
    "expo-build-properties",
    {
      "android": {
        "enableProguardInReleaseBuilds": true
      }
    }
  ]
  
### **Symptoms**
  - OutOfMemoryError
  - GC overhead limit exceeded
  - Build killed
### **Detection Pattern**
jvmargs|resourceClass