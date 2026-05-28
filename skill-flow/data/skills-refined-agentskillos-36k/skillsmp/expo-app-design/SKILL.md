---
name: expo-app-design
description: Build beautiful cross-platform mobile apps with Expo Router, NativeWind, and React Native.
author: expo
category: development
tags: [expo, react-native, mobile, typescript, nativewind]
license: MIT
version: 2.0.0
---

# Expo App Design

Build beautiful, performant cross-platform mobile apps with Expo Router, NativeWind, and React Native best practices.

## When to Use

- Building mobile apps with Expo SDK 52+
- Navigation with Expo Router (file-based routing)
- Styling with NativeWind (Tailwind for React Native)
- Native tabs, stacks, and modal navigation
- Animations with Reanimated
- Cross-platform (iOS, Android, Web) development

## Core Principles

### 1. File-Based Routing with Expo Router

```typescript
// app/_layout.tsx - Root layout
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen name="modal" options={{ presentation: 'modal' }} />
    </Stack>
  );
}

// app/(tabs)/_layout.tsx - Tab navigation
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
  return (
    <Tabs screenOptions={{ tabBarActiveTintColor: '#007AFF' }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color }) => <Ionicons name="home" size={24} color={color} />,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color }) => <Ionicons name="person" size={24} color={color} />,
        }}
      />
    </Tabs>
  );
}
```

### 2. NativeWind Styling (Tailwind CSS)

```typescript
// tailwind.config.js
module.exports = {
  content: ['./app/**/*.{js,jsx,ts,tsx}', './components/**/*.{js,jsx,ts,tsx}'],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      colors: {
        primary: '#007AFF',
        secondary: '#5856D6',
      },
    },
  },
  plugins: [],
};

// Component with NativeWind
import { View, Text, Pressable } from 'react-native';

export function Button({ title, onPress }: { title: string; onPress: () => void }) {
  return (
    <Pressable
      onPress={onPress}
      className="bg-primary px-6 py-3 rounded-xl active:opacity-80"
    >
      <Text className="text-white font-semibold text-center">{title}</Text>
    </Pressable>
  );
}
```

### 3. Reanimated Animations

```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
} from 'react-native-reanimated';

export function AnimatedCard({ children }: { children: React.ReactNode }) {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  const onPressIn = () => {
    scale.value = withSpring(0.95);
    opacity.value = withTiming(0.8);
  };

  const onPressOut = () => {
    scale.value = withSpring(1);
    opacity.value = withTiming(1);
  };

  return (
    <Pressable onPressIn={onPressIn} onPressOut={onPressOut}>
      <Animated.View style={animatedStyle} className="bg-white rounded-2xl p-4 shadow-lg">
        {children}
      </Animated.View>
    </Pressable>
  );
}
```

### 4. Type-Safe Navigation

```typescript
// types/navigation.ts
import { Href } from 'expo-router';

export type AppRoutes = {
  '/': undefined;
  '/profile': undefined;
  '/settings': undefined;
  '/post/[id]': { id: string };
  '/modal': { title: string };
};

// Usage with type safety
import { useRouter, useLocalSearchParams } from 'expo-router';

export function PostScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();

  const goToProfile = () => {
    router.push('/profile');
  };

  const goToPost = (postId: string) => {
    router.push(`/post/${postId}`);
  };

  return (/* ... */);
}
```

## Best Practices

### Project Structure

```
app/
├── _layout.tsx           # Root layout
├── index.tsx             # Home screen (/)
├── (tabs)/               # Tab group
│   ├── _layout.tsx       # Tab layout
│   ├── index.tsx         # First tab
│   └── profile.tsx       # Profile tab
├── (auth)/               # Auth group (unauthenticated)
│   ├── _layout.tsx
│   ├── login.tsx
│   └── register.tsx
├── post/
│   └── [id].tsx          # Dynamic route
└── modal.tsx             # Modal screen

components/
├── ui/                   # Reusable UI components
│   ├── Button.tsx
│   ├── Card.tsx
│   └── Input.tsx
├── features/             # Feature-specific components
└── providers/            # Context providers

hooks/
├── useAuth.ts
├── useTheme.ts
└── useApi.ts

lib/
├── api.ts
├── storage.ts
└── utils.ts
```

### Performance Optimization

1. **Use FlashList for large lists**
```typescript
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  estimatedItemSize={100}
  keyExtractor={(item) => item.id}
/>
```

2. **Optimize images with expo-image**
```typescript
import { Image } from 'expo-image';

<Image
  source={{ uri: imageUrl }}
  placeholder={blurhash}
  contentFit="cover"
  transition={200}
  className="w-full h-48 rounded-xl"
/>
```

3. **Memoize expensive components**
```typescript
import { memo } from 'react';

export const ExpensiveComponent = memo(({ data }: Props) => {
  // Component implementation
});
```

### Common Patterns

#### Authentication Flow
```typescript
// app/(auth)/_layout.tsx
import { Redirect, Stack } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';

export default function AuthLayout() {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return <Redirect href="/(tabs)" />;
  }

  return <Stack screenOptions={{ headerShown: false }} />;
}
```

#### Safe Area Handling
```typescript
import { SafeAreaView } from 'react-native-safe-area-context';

export function Screen({ children }: { children: React.ReactNode }) {
  return (
    <SafeAreaView className="flex-1 bg-white" edges={['top', 'bottom']}>
      {children}
    </SafeAreaView>
  );
}
```

#### Form Handling with React Hook Form
```typescript
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export function LoginForm() {
  const { control, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
  });

  return (
    <View className="gap-4">
      <Controller
        control={control}
        name="email"
        render={({ field: { onChange, value } }) => (
          <Input
            placeholder="Email"
            value={value}
            onChangeText={onChange}
            error={errors.email?.message}
          />
        )}
      />
      {/* ... */}
    </View>
  );
}
```

## Dependencies to Install

```bash
# Core
npx expo install expo-router react-native-safe-area-context react-native-screens

# Styling
npm install nativewind tailwindcss
npx pod-install

# Animations
npx expo install react-native-reanimated

# Performance
npm install @shopify/flash-list
npx expo install expo-image

# Forms
npm install react-hook-form @hookform/resolvers zod

# Icons
npx expo install @expo/vector-icons
```

## Source

This skill extends patterns from [Expo's official skills](https://github.com/expo/skills) and [Expo documentation](https://docs.expo.dev/).
