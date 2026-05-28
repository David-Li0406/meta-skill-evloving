---
name: react-native-expo-development
description: Use this skill for best practices and patterns in building mobile applications with React Native and Expo.
---

# React Native & Expo Development

## When to Use
- Building cross-platform mobile applications with React Native or Expo.
- Implementing navigation patterns and managing the navigation stack.
- Integrating native modules and optimizing mobile performance.

## Project Setup with Expo
```bash
# Create new Expo project
npx create-expo-app@latest <project-name> --template <template-type>
# Start development
cd <project-name>
npx expo start
```

## Project Structure
```
<project-name>/
├── app/                    # Expo Router (file-based routing)
│   ├── _layout.tsx         # Root layout
│   ├── index.tsx           # Home screen
│   ├── (tabs)/             # Tab group
│   └── [id].tsx            # Dynamic route
├── components/             # Reusable UI components
├── hooks/                  # Custom hooks
├── lib/                    # Utilities
├── constants/              # App constants
├── assets/                 # Static assets
└── app.json                # Expo config
```

## Navigation Patterns
- Use **File-based routing** in the `app/` directory.
- Use `Link` from `expo-router` for navigation, but prefer `router.push()` or `router.replace()` for logic-based navigation in event handlers.
- Wrap screens in `Stack.Screen` or `Tabs.Screen` to configure headers.

### Example Navigation Code
```tsx
import { Stack } from 'expo-router'
import { StatusBar } from 'expo-status-bar'

export default function RootLayout() {
  return (
    <>
      <StatusBar style="auto" />
      <Stack>
        <Stack.Screen name="index" options={{ title: 'Home' }} />
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      </Stack>
    </>
  )
}
```

## Styling & UI Robustness
- Use `StyleSheet.create` for performance-critical views or `NativeWind` for Tailwind-like classes.
- Always wrap top-level screens in `SafeAreaView` to handle insets properly.
- Avoid using raw strings outside of `<Text>` components to prevent crashes.

### Example Styling Code
```tsx
import { StyleSheet, View, Text } from 'react-native'

export function Card({ title, children }) {
  return (
    <View style={styles.card}>
      <Text style={styles.title}>{title}</Text>
      {children}
    </View>
  )
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 8,
  },
})
```

## Performance Optimization
- Use `FlatList` for long lists and optimize rendering with `removeClippedSubviews`, `maxToRenderPerBatch`, and `initialNumToRender`.
- Implement memoization for components and callbacks to avoid unnecessary re-renders.

### Example Performance Code
```tsx
import { FlatList } from 'react-native'
import { useCallback } from 'react'

export function UserList({ users }) {
  const renderItem = useCallback(({ item }) => <UserCard user={item} />, [])
  
  return (
    <FlatList
      data={users}
      renderItem={renderItem}
      keyExtractor={(item) => item.id.toString()}
      removeClippedSubviews={true}
      initialNumToRender={10}
    />
  )
}
```

## Native Modules & APIs
- Use `expo-camera` for camera functionalities and handle permissions gracefully.
- Implement push notifications with `expo-notifications`, ensuring to guard logic for Expo Go clients.

### Example Camera Code
```tsx
import { CameraView, useCameraPermissions } from 'expo-camera'

export function CameraScreen() {
  const [permission, requestPermission] = useCameraPermissions()

  if (!permission.granted) {
    return <Button onPress={requestPermission} title="Grant Permission" />
  }

  return <CameraView style={{ flex: 1 }} />
}
```

## Common Pitfalls
1. Avoid using `flex: 1` without a parent flex container.
2. Always handle keyboard interactions in forms.
3. Use `keyExtractor` in `FlatList` to prevent rendering issues.
4. Test on both iOS and Android devices.

## Production Checklist
- Handle all permission requests gracefully.
- Implement error boundaries and offline support.
- Optimize images and assets for performance.
- Test on physical devices and configure app icons and splash screens.