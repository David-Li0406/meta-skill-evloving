---
name: expo-react-native
description: Best practices for developing Expo SDK 54 React Native apps with Expo Router, Zustand, and NativeWind. Use when building mobile apps with this stack, implementing navigation, state management, styling, performance optimization, TypeScript patterns, or security.
---

# Expo React Native Best Practices (SDK 54)

## Core Stack
- **Expo SDK 54** (React Native 0.81, React 19.1)
- **Expo Router** - File-based navigation
- **Zustand** - State management
- **NativeWind** - Tailwind CSS styling
- **TypeScript** - Type safety
- **React Compiler** - Automatic memoization (React 19+)

## New Architecture
SDK 54 defaults to New Architecture (Fabric + TurboModules). SDK 55+ requires it.
Check library compatibility at [reactnativedirectory.com](https://reactnativedirectory.com).

## React Compiler

Enable in `app.json`:
```json
{ "expo": { "experiments": { "reactCompiler": true } } }
```

**Key principle**: Default to no manual memoization—the compiler handles `useMemo`, `useCallback`, and `React.memo` automatically.

Manual memoization still needed for:
- External API calls/side effects
- Third-party libraries requiring referential equality
- Explicit control over expensive computations

See [references/react-compiler.md](references/react-compiler.md) for patterns.

## Expo Router

### Thin Routes Architecture
Route files (`app/`) only extract params and delegate to screen components:

```tsx
// app/profile/index.tsx - Thin route
import { useLocalSearchParams } from 'expo-router';
import { Profile } from '@/screens/profile';

export default function ProfileRoute() {
  const { id } = useLocalSearchParams<{ id: string }>();
  return <Profile userId={id} />;
}
```

All business logic lives in `screens/`. See [references/navigation.md](references/navigation.md) for full patterns.

## Zustand

Use selectors to prevent unnecessary re-renders:
```tsx
// ❌ Subscribes to entire store
const { user } = useAuthStore();

// ✅ Subscribes only to user
const user = useAuthStore((state) => state.user);
```

See [references/state-management.md](references/state-management.md) for store patterns and persistence.

## NativeWind

```tsx
<View className="bg-white rounded-lg p-4 shadow-md">
  <Text className={isActive ? 'text-white' : 'text-gray-700'}>{label}</Text>
</View>
```

Use `cssInterop` for third-party components. See [references/styling.md](references/styling.md).

## Performance

- **FlashList** for large lists (cell recycling, 10x faster than FlatList)
- **Enable React Compiler** for automatic optimization
- **Profile first**—only add manual memoization if measured

See [references/performance.md](references/performance.md) for list optimization patterns.

## Security

Use `expo-secure-store` for tokens—**never** AsyncStorage:
```tsx
await SecureStore.setItemAsync('authToken', token);
await SecureStore.setItemAsync('sensitiveKey', value, { requireAuthentication: true });
```

## Quick Reference

| Task | Solution |
|------|----------|
| Navigation | `expo-router` file-based routes |
| Global state | Zustand with selectors |
| Styling | NativeWind className |
| Secure storage | `expo-secure-store` |
| Large lists | FlashList |
| Forms | react-hook-form + zod |
