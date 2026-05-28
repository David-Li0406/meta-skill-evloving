# Expo

## Patterns


---
  #### **Name**
Project Setup
  #### **Description**
Create and configure Expo project
  #### **When To Use**
Starting new mobile project
  #### **Implementation**
    # Create new project with Expo Router
    npx create-expo-app@latest my-app --template tabs
    
    # Project structure
    my-app/
    ├── app/                 # Expo Router pages
    │   ├── (tabs)/         # Tab navigator group
    │   │   ├── index.tsx   # First tab
    │   │   ├── explore.tsx # Second tab
    │   │   └── _layout.tsx # Tab layout
    │   ├── _layout.tsx     # Root layout
    │   └── +not-found.tsx  # 404 page
    ├── components/         # Reusable components
    ├── constants/          # App constants
    ├── hooks/              # Custom hooks
    ├── assets/             # Images, fonts
    ├── app.json           # Expo config
    └── eas.json           # EAS Build config
    
    # app.json configuration
    {
      "expo": {
        "name": "My App",
        "slug": "my-app",
        "version": "1.0.0",
        "orientation": "portrait",
        "icon": "./assets/icon.png",
        "scheme": "myapp",  // For deep linking
        "splash": {
          "image": "./assets/splash.png",
          "resizeMode": "contain",
          "backgroundColor": "#ffffff"
        },
        "ios": {
          "bundleIdentifier": "com.company.myapp",
          "supportsTablet": true
        },
        "android": {
          "package": "com.company.myapp",
          "adaptiveIcon": {
            "foregroundImage": "./assets/adaptive-icon.png",
            "backgroundColor": "#ffffff"
          }
        },
        "plugins": [
          "expo-router"
        ]
      }
    }
    

---
  #### **Name**
Expo Router Navigation
  #### **Description**
File-based routing for React Native
  #### **When To Use**
All navigation in Expo apps
  #### **Implementation**
    // app/_layout.tsx - Root layout
    import { Stack } from "expo-router";
    
    export default function RootLayout() {
      return (
        <Stack>
          <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
          <Stack.Screen name="modal" options={{ presentation: "modal" }} />
        </Stack>
      );
    }
    
    // app/(tabs)/_layout.tsx - Tab layout
    import { Tabs } from "expo-router";
    import { Ionicons } from "@expo/vector-icons";
    
    export default function TabLayout() {
      return (
        <Tabs screenOptions={{ tabBarActiveTintColor: "#007AFF" }}>
          <Tabs.Screen
            name="index"
            options={{
              title: "Home",
              tabBarIcon: ({ color }) => (
                <Ionicons name="home" size={24} color={color} />
              ),
            }}
          />
          <Tabs.Screen
            name="profile"
            options={{
              title: "Profile",
              tabBarIcon: ({ color }) => (
                <Ionicons name="person" size={24} color={color} />
              ),
            }}
          />
        </Tabs>
      );
    }
    
    // Navigation between screens
    import { Link, router } from "expo-router";
    
    // Link component
    <Link href="/profile">Go to Profile</Link>
    
    // Programmatic navigation
    router.push("/profile");
    router.replace("/home");
    router.back();
    
    // Dynamic routes: app/user/[id].tsx
    import { useLocalSearchParams } from "expo-router";
    
    export default function UserPage() {
      const { id } = useLocalSearchParams<{ id: string }>();
      return <Text>User: {id}</Text>;
    }
    
    // Navigate with params
    router.push({ pathname: "/user/[id]", params: { id: "123" } });
    
    // Typed routes with expo-router/typed-routes
    // tsconfig.json: "include": [".expo/types/**/*.ts", ...]
    

---
  #### **Name**
EAS Build Configuration
  #### **Description**
Set up cloud builds
  #### **When To Use**
Building for production or testing
  #### **Implementation**
    # Install EAS CLI
    npm install -g eas-cli
    
    # Login to Expo
    eas login
    
    # Configure EAS
    eas build:configure
    
    # eas.json
    {
      "cli": {
        "version": ">= 5.0.0"
      },
      "build": {
        "development": {
          "developmentClient": true,
          "distribution": "internal",
          "ios": {
            "simulator": true
          }
        },
        "preview": {
          "distribution": "internal",
          "android": {
            "buildType": "apk"
          }
        },
        "production": {
          "autoIncrement": true
        }
      },
      "submit": {
        "production": {
          "ios": {
            "appleId": "your@email.com",
            "ascAppId": "1234567890"
          },
          "android": {
            "serviceAccountKeyPath": "./google-services.json"
          }
        }
      }
    }
    
    # Build commands
    eas build --platform ios --profile development
    eas build --platform android --profile preview
    eas build --platform all --profile production
    
    # Submit to stores
    eas submit --platform ios --profile production
    eas submit --platform android --profile production
    
    # Or build and submit together
    eas build --platform all --profile production --auto-submit
    

---
  #### **Name**
Development Build with Native Modules
  #### **Description**
Use native modules with Expo
  #### **When To Use**
Need native libraries not in Expo Go
  #### **Implementation**
    # Why development builds?
    # - Expo Go has limited native modules
    # - Development builds are YOUR custom Expo Go
    # - Add any native library you need
    
    # Install native module
    npx expo install expo-camera
    
    # Some libraries need config plugins
    npx expo install react-native-ble-plx
    
    # app.json with config plugins
    {
      "expo": {
        "plugins": [
          "expo-camera",
          [
            "react-native-ble-plx",
            {
              "isBackgroundEnabled": true,
              "modes": ["peripheral", "central"]
            }
          ],
          [
            "expo-build-properties",
            {
              "ios": {
                "deploymentTarget": "15.0"
              },
              "android": {
                "compileSdkVersion": 34
              }
            }
          ]
        ]
      }
    }
    
    # Build development client
    eas build --platform ios --profile development
    # Or for simulator
    eas build --platform ios --profile development --local
    
    # Install on device/simulator
    # iOS: drag .app to simulator
    # Android: adb install app.apk
    
    # Start dev server
    npx expo start --dev-client
    
    # Custom config plugin (for advanced cases)
    // plugins/with-custom-config.js
    const { withAppDelegate } = require("expo-build-properties");
    
    module.exports = function withCustomConfig(config) {
      return withAppDelegate(config, async (config) => {
        // Modify native code
        return config;
      });
    };
    

---
  #### **Name**
EAS Update (OTA Updates)
  #### **Description**
Deploy updates without app store review
  #### **When To Use**
Bug fixes, content updates
  #### **Implementation**
    # Configure updates in app.json
    {
      "expo": {
        "runtimeVersion": {
          "policy": "appVersion"  // or "sdkVersion", "fingerprint"
        },
        "updates": {
          "url": "https://u.expo.dev/your-project-id"
        }
      }
    }
    
    # eas.json - add channel to builds
    {
      "build": {
        "production": {
          "channel": "production"
        },
        "preview": {
          "channel": "preview"
        }
      }
    }
    
    # Publish update
    eas update --channel production --message "Fix login bug"
    
    # Check updates in app
    import * as Updates from "expo-updates";
    
    async function checkForUpdates() {
      try {
        const update = await Updates.checkForUpdateAsync();
        if (update.isAvailable) {
          await Updates.fetchUpdateAsync();
          await Updates.reloadAsync();  // Restart app with update
        }
      } catch (e) {
        console.log("Update check failed:", e);
      }
    }
    
    // Run on app start
    useEffect(() => {
      if (!__DEV__) {
        checkForUpdates();
      }
    }, []);
    
    # Rollback if needed
    eas update:rollback --channel production
    
    # View update history
    eas update:list
    

---
  #### **Name**
Performance Optimization
  #### **Description**
Optimize Expo app performance
  #### **When To Use**
App feels slow or janky
  #### **Implementation**
    // 1. Use FlashList instead of FlatList
    import { FlashList } from "@shopify/flash-list";
    
    <FlashList
      data={items}
      renderItem={({ item }) => <ItemComponent item={item} />}
      estimatedItemSize={100}  // Required!
    />
    
    // 2. Memoize expensive components
    import { memo, useMemo, useCallback } from "react";
    
    const ExpensiveItem = memo(({ item, onPress }) => {
      // Only re-renders if item or onPress changes
      return <Pressable onPress={onPress}>...</Pressable>;
    });
    
    // Parent component
    const handlePress = useCallback((id) => {
      // Stable function reference
    }, []);
    
    // 3. Optimize images
    import { Image } from "expo-image";
    
    <Image
      source={{ uri: imageUrl }}
      style={{ width: 200, height: 200 }}
      contentFit="cover"
      placeholder={blurhash}  // Show placeholder while loading
      transition={200}
    />
    
    // 4. Reduce re-renders with selectors
    import { useStore } from "./store";
    
    // BAD - re-renders on any store change
    const { user } = useStore();
    
    // GOOD - only re-renders when user changes
    const user = useStore((state) => state.user);
    
    // 5. Lazy load screens
    import { lazy, Suspense } from "react";
    
    const HeavyScreen = lazy(() => import("./HeavyScreen"));
    
    <Suspense fallback={<LoadingSpinner />}>
      <HeavyScreen />
    </Suspense>
    
    // 6. Use native driver for animations
    import Animated, {
      useSharedValue,
      useAnimatedStyle,
      withSpring,
    } from "react-native-reanimated";
    
    const offset = useSharedValue(0);
    
    const animatedStyle = useAnimatedStyle(() => ({
      transform: [{ translateX: offset.value }],
    }));
    
    // 7. Profile with React DevTools
    // Enable in development to find slow components
    

## Anti-Patterns


---
  #### **Name**
Using Expo Go for Everything
  #### **Description**
Not using development builds when needed
  #### **Why Bad**
    Limited native modules.
    Can't test production features.
    Frustrating native library issues.
    
  #### **What To Do Instead**
    Use development builds when you need:
    - Custom native libraries
    - Push notifications setup
    - Production-like testing
    

---
  #### **Name**
Ignoring Bundle Size
  #### **Description**
Not monitoring app size
  #### **Why Bad**
    Slow downloads.
    App store rejection risk.
    Poor user experience.
    
  #### **What To Do Instead**
    Monitor with npx expo-optimize.
    Use dynamic imports.
    Compress images.
    Remove unused dependencies.
    

---
  #### **Name**
Not Using Expo Image
  #### **Description**
Using React Native Image for remote images
  #### **Why Bad**
    No caching.
    Poor performance.
    Missing features.
    
  #### **What To Do Instead**
    Use expo-image for all remote images.
    Add blurhash placeholders.
    Set proper cache policies.
    

---
  #### **Name**
Hardcoded Environment Values
  #### **Description**
API keys in code
  #### **Why Bad**
    Security risk.
    Can't change per environment.
    Exposed in build.
    
  #### **What To Do Instead**
    Use eas.json environment variables.
    Use expo-constants for runtime config.
    Use .env with expo-env plugin.
    