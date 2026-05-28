---
name: expo-app-design
description: Use this skill when building beautiful, performant cross-platform mobile apps with Expo Router, NativeWind, and React Native.
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
// Example of using Reanimated for animations
import Animated, { Easing } from 'react-native-reanimated';

const fadeIn = (opacity: Animated.SharedValue<number>) => {
  return Animated.timing(opacity, {
    toValue: 1,
    duration: 500,
    easing: Easing.inOut(Easing.ease),
    useNativeDriver: true,
  });
};
```