---
name: react-native-apps
description: Patterns for React Native (Expo), navigation, and mobile state.
---

# React Native / Mobile Apps

## When to use this skill
- Building mobile apps with React Native or Expo.
- Managing navigation stack.
- Accessing native modules.

## 1. Expo ecosystem
- **Expo Router**: Use file-based routing (similar to Next.js) via `expo-router`.
- **Config**: Manage native permissions via `app.json` config plugins.

## 2. Styling
- **NativeWind**: Use Tailwind-like classes via `nativewind` if standard, or `StyleSheet.create` for performance-critical views.
- **SafeArea**: Always wrap top-level screens in `SafeAreaView` or handle insets manually.

## 3. Performance
- **Lists**: Use `FlashList` (Shopify) or optimized `FlatList` for long lists.
- **Bridge**: Minimize passes over the JS bridge. Use Reanimated for 60fps animations.

## 4. Navigation
- **Stack**: Use Stack for drill-down.
- **Tabs**: Use Tabs for top-level sections.
- **Deep Links**: configure generic links in `app.json` for universal links.
