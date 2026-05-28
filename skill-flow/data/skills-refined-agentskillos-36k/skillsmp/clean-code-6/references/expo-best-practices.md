# Expo Best Practices (React Native)

## Core Principles

- **Mobile-First**: Design for mobile constraints, adapt for web/desktop
- **Cross-Platform**: Write once with platform-specific optimizations
- **Keep it Simple**: Fewest lines with straightforward approaches
- **Performance**: Leverage native optimizations, avoid re-renders
- **Managed Workflow**: Use Expo's managed workflow
- **Mobile Web Vitals**: Prioritize Load Time, Jank, Responsiveness

---

## Configuration & Environment

- **Environment Variables**: Use `expo-constants` for env variables
- **Permissions**: Use individual modules (e.g., `expo-camera`, `expo-location`)
- **OTA Updates**: Implement `expo-updates`

---

## Navigation (Expo Router)

### Layouts

Define with `_layout.tsx` for shared UI.

### Navigation Methods

| Method              | Use Case                |
| ------------------- | ----------------------- |
| `Link`              | Declarative navigation  |
| `router.navigate()` | Programmatic navigation |
| `router.replace()`  | Replace current screen  |
| `Redirect`          | Immediate redirect      |

**CRITICAL**: Always use `router.navigate()` or `router.replace()` from `expo-router`. Never use `useRouter()` hook.

```typescript
import { router } from "expo-router";

function handlePress() {
  router.navigate("/profile");
}
```

---

## Lists & Performance

### List Components

- Use `FlatList`, `SectionList`, `VirtualizedList` (never `map()` for long lists)
- Provide stable `keyExtractor`

```typescript
<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <ItemCard item={item} />}
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
/>
```

### Heavy Rendering

- Use `@legendapp/list` for complex lists
- Implement `getItemLayout` for fixed heights

---

## Keyboard Handling

Use `react-native-keyboard-controller` for consistent behavior across platforms.

---

## Animations

Use `react-native-reanimated` for 60fps animations:

```typescript
import Animated, { useAnimatedStyle, withSpring } from "react-native-reanimated";

function AnimatedBox() {
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: withSpring(1.2) }],
  }));

  return <Animated.View style={animatedStyle} />;
}
```

---

## Images

### Formats

- **WebP**: For photos (smaller, better quality)
- **SVG**: For icons and illustrations

### Optimization

- Use `expo-image` with lazy loading and blurhash
- Provide multiple densities (`@1x`, `@2x`, `@3x`)
- Use CDN for remote images
- Optimize SVGs (remove unnecessary metadata)

```typescript
import { Image } from "expo-image";

<Image
  source={{ uri: imageUrl }}
  placeholder={{ blurhash }}
  contentFit="cover"
  transition={200}
/>
```

---

## Internationalization

- Support multiple languages with `react-i18next` or `expo-localization`
- Support RTL layouts

---

## Security

- **Secure Storage**: Use `expo-secure-store` with `requireAuthentication` for biometric
- **OAuth**: Use `expo-auth-session` for OAuth flows

```typescript
import * as SecureStore from "expo-secure-store";

await SecureStore.setItemAsync("token", value, {
  requireAuthentication: true,
});
```

---

## Assets & Device Optimization

### Asset Management

- Use asset bundles for efficient loading
- Implement offline-first approach with asset caching

### Performance

- Apply adaptive rendering for different device capabilities
- Use device-specific optimizations
- Handle low-end devices gracefully
- Use Expo dev tools to identify bottlenecks

---

## Component Patterns

### Platform-Specific Code

```typescript
import { Platform } from "react-native";

const styles = {
  padding: Platform.select({
    ios: 20,
    android: 16,
    default: 20,
  }),
};
```

### Safe Areas

Always use `react-native-safe-area-context`:

```typescript
import { SafeAreaView } from "react-native-safe-area-context";

function Screen() {
  return (
    <SafeAreaView edges={["top", "bottom"]}>
      <Content />
    </SafeAreaView>
  );
}
```

---

## Anti-Patterns

| Pattern              | Problem           | Solution                    |
| -------------------- | ----------------- | --------------------------- |
| `.map()` for lists   | No virtualization | Use FlatList/SectionList    |
| `useRouter()` hook   | Stale navigation  | Use `router` from module    |
| PNG for photos       | Large file size   | Use WebP                    |
| No blurhash          | Loading jank      | Add blurhash placeholders   |
| Inline animations    | Poor performance  | Use react-native-reanimated |
| No keyboard handling | Hidden inputs     | Use keyboard-controller     |
| Storing tokens plain | Security risk     | Use expo-secure-store       |
