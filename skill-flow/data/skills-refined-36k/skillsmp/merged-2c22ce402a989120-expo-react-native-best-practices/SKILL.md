---
name: expo-react-native-best-practices
description: Use this skill for best practices in building high-quality React Native applications with Expo, focusing on code structure, navigation, performance optimization, and UI design.
---

# Expo & React Native Best Practices

Guidelines for building high-quality Expo React Native applications, focusing on clean code, modularity, performance, and effective navigation.

## Code Style and Structure

- **Clean, Readable Code**: Ensure your code is easy to read and understand. Use descriptive names for variables and functions.
- **Functional Components**: Prefer functional components with hooks (useState, useEffect) over class components.
- **Component Modularity**: Break components into smaller, reusable pieces with a single responsibility.
- **Feature-Based Organization**: Group related components, hooks, and styles into feature directories (e.g., user-profile, chat-screen).

## Naming Conventions

- **Variables and Functions**: Use camelCase (e.g., `isFetchingData`, `handleUserInput`).
- **Components**: Use PascalCase (e.g., `UserProfile`, `ChatScreen`).
- **Directories**: Use lowercase hyphenated names (e.g., `user-profile`, `chat-screen`).

## Project Setup with Expo

```bash
# Create new Expo project
npx create-expo-app@latest my-app --template tabs

# Or with blank template
npx create-expo-app@latest my-app --template blank-typescript

# Start development
cd my-app
npx expo start
```

## Navigation (Expo Router)

- Use **File-based routing** in the `app/` directory.
- Use `Link` from `expo-router` for navigation, but prefer `router.push()` or `router.replace()` for logic-based navigation in event handlers.
- Screens should be wrapped in `Stack.Screen` or `Tabs.Screen` to configure headers.

### Root Layout Example

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router'
import { StatusBar } from 'expo-status-bar'

export default function RootLayout() {
  return (
    <>
      <StatusBar style="auto" />
      <Stack>
        <Stack.Screen name="index" options={{ title: 'Home' }} />
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="modal" options={{ presentation: 'modal' }} />
      </Stack>
    </>
  )
}
```

## Performance Optimization

- **Avoid unnecessary state updates**; use local state when needed.
- Apply `React.memo()` to prevent unnecessary re-renders.
- Optimize `FlatList` with props like `removeClippedSubviews`, `maxToRenderPerBatch`, and `windowSize`.
- Use inline `style={{ flex: 1 }}` for components like `CameraView` to prevent layout issues.

## UI and Styling

- Use `StyleSheet.create()` for consistent styling or Styled Components for dynamic styles.
- Ensure responsive design across screen sizes and orientations.
- Use optimized image libraries like `expo-image` for better performance.

## Best Practices

- Follow React Native's threading model for smooth UI performance.
- Use Expo's EAS Build and OTA updates for deployment.
- Implement a session listener in the `RootLayout` to manage user authentication states.

## Common Pitfalls

1. **Don't use `flex: 1` without a parent flex container**.
2. **Always handle keyboard on forms**.
3. **Use `keyExtractor` in `FlatList`**.
4. **Test on both iOS and Android**.
5. **Handle safe areas properly**.

## Production Checklist

- [ ] Handle all permission requests gracefully.
- [ ] Implement proper error boundaries.
- [ ] Optimize images and assets.
- [ ] Test on physical devices.
- [ ] Configure app icons and splash screens.
- [ ] Set up EAS Build for production builds.