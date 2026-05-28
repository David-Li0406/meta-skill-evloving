---
name: building-ui-with-expo-router
description: Use this skill when you want to build beautiful applications using Expo Router, covering fundamentals, styling, components, navigation, animations, and native tabs.
---

# Expo UI Guidelines

## References

Consult these resources as needed:

- `./references/route-structure.md` -- Route file conventions, dynamic routes, query parameters, groups, and folder organization
- `./references/tabs.md` -- Native tab bar with NativeTabs, migration from JS tabs, iOS 26 features
- `./references/icons.md` -- SF Symbols with expo-symbols, common icon names, animations, and weights
- `./references/controls.md` -- Native iOS controls: Switch, Slider, SegmentedControl, DateTimePicker, Picker
- `./references/visual-effects.md` -- Blur effects with expo-blur and liquid glass with expo-glass-effect
- `./references/animations.md` -- Reanimated animations: entering, exiting, layout, scroll-driven, and gestures
- `./references/search.md` -- Search bar integration with headers, useSearch hook, and filtering patterns
- `./references/gradients.md` -- CSS gradients using experimental_backgroundImage (New Architecture only)
- `./references/media.md` -- Media handling for Expo Router including camera, audio, video, and file saving
- `./references/storage.md` -- Data storage patterns including SQLite, AsyncStorage, and SecureStore
- `./references/webgpu-three.md` -- 3D graphics, games, and GPU-powered visualizations with WebGPU and Three.js

## Running the App

**CRITICAL: Always try Expo Go first before creating custom builds.**

Most Expo apps work in Expo Go without any custom native code. Before running `npx expo run:ios` or `npx expo run:android`:

1. **Start with Expo Go**: Run `npx expo start` and scan the QR code with Expo Go.
2. **Check if features work**: Test your app thoroughly in Expo Go.
3. **Only create custom builds when required** - see below.

### When Custom Builds Are Required

You need `npx expo run:ios/android` or `eas build` ONLY when using:

- **Local Expo modules** (custom native code in `modules/`)
- **Apple targets** (widgets, app clips, extensions via `@bacons/apple-targets`)
- **Third-party native modules** not included in Expo Go
- **Custom native configuration** that can't be expressed in `app.json`

### When Expo Go Works

Expo Go supports a huge range of features out of the box:

- All `expo-*` packages (camera, location, notifications, etc.)
- Expo Router navigation
- Most UI libraries (reanimated, gesture handler, etc.)