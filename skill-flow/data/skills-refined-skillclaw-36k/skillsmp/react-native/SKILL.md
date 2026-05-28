---
name: react-native
description: React Native and Expo development patterns and best practices
license: MIT
---

# React Native Skill

Modern React Native development with Expo, navigation patterns, and native module integration.

## When to Use

- Building cross-platform mobile applications
- Setting up Expo projects
- Implementing navigation patterns
- Integrating native modules
- Optimizing mobile performance

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

## Project Structure

```
my-app/
├── app/                    # Expo Router (file-based routing)
│   ├── _layout.tsx         # Root layout
│   ├── index.tsx           # Home screen
│   ├── (tabs)/             # Tab group
│   │   ├── _layout.tsx     # Tab layout
│   │   ├── index.tsx       # First tab
│   │   └── settings.tsx    # Settings tab
│   └── [id].tsx            # Dynamic route
├── components/
│   ├── ui/                 # Reusable UI components
│   └── features/           # Feature-specific components
├── hooks/                  # Custom hooks
├── lib/                    # Utilities
├── constants/              # App constants
├── assets/                 # Static assets
└── app.json               # Expo config
```

## Expo Router (Navigation)

### Root Layout

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
        <Stack.Screen 
          name="modal" 
          options={{ presentation: 'modal' }} 
        />
      </Stack>
    </>
  )
}
```

### Tab Navigation

```tsx
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router'
import { Ionicons } from '@expo/vector-icons'

export default function TabLayout() {
  return (
    <Tabs screenOptions={{ tabBarActiveTintColor: '#007AFF' }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="home" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: 'Settings',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="settings" size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  )
}
```

### Navigation

```tsx
import { Link, useRouter, useLocalSearchParams } from 'expo-router'

// Declarative navigation
<Link href="/profile">Go to Profile</Link>
<Link href={{ pathname: '/user/[id]', params: { id: '123' } }}>
  User 123
</Link>

// Imperative navigation
const router = useRouter()
router.push('/profile')
router.replace('/home')
router.back()

// Get params
const { id } = useLocalSearchParams<{ id: string }>()
```

## Styling Patterns

### StyleSheet

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
    elevation: 3, // Android shadow
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 8,
  },
})
```

### NativeWind (Tailwind)

```bash
npm install nativewind tailwindcss
```

```tsx
// With NativeWind
import { View, Text } from 'react-native'

export function Card({ title, children }) {
  return (
    <View className="bg-white rounded-xl p-4 shadow-md">
      <Text className="text-lg font-semibold mb-2">{title}</Text>
      {children}
    </View>
  )
}
```

## Components & Patterns

### Safe Area Handling

```tsx
import { SafeAreaView, SafeAreaProvider } from 'react-native-safe-area-context'

// In root
export default function App() {
  return (
    <SafeAreaProvider>
      <RootLayout />
    </SafeAreaProvider>
  )
}

// In screens
export function HomeScreen() {
  return (
    <SafeAreaView style={{ flex: 1 }} edges={['top', 'bottom']}>
      <Content />
    </SafeAreaView>
  )
}
```

### FlatList Performance

```tsx
import { FlatList } from 'react-native'
import { useCallback } from 'react'

export function UserList({ users }) {
  const renderItem = useCallback(
    ({ item }) => <UserCard user={item} />,
    []
  )
  
  const keyExtractor = useCallback(
    (item) => item.id.toString(),
    []
  )

  return (
    <FlatList
      data={users}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      // Performance optimizations
      removeClippedSubviews={true}
      maxToRenderPerBatch={10}
      windowSize={5}
      initialNumToRender={10}
      // Pull to refresh
      onRefresh={handleRefresh}
      refreshing={isRefreshing}
      // Infinite scroll
      onEndReached={loadMore}
      onEndReachedThreshold={0.5}
      ListFooterComponent={<LoadingFooter />}
      // Empty state
      ListEmptyComponent={<EmptyState />}
    />
  )
}
```

### Keyboard Handling

```tsx
import {
  KeyboardAvoidingView,
  Platform,
  TouchableWithoutFeedback,
  Keyboard,
} from 'react-native'

export function FormScreen() {
  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={{ flex: 1 }}
    >
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <View style={{ flex: 1 }}>
          <TextInput placeholder="Email" />
          <TextInput placeholder="Password" secureTextEntry />
        </View>
      </TouchableWithoutFeedback>
    </KeyboardAvoidingView>
  )
}
```

## State Management

### React Query for Server State

```tsx
import { QueryClient, QueryClientProvider, useQuery, useMutation } from '@tanstack/react-query'

const queryClient = new QueryClient()

// Provider
export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RootLayout />
    </QueryClientProvider>
  )
}

// Usage
export function UserProfile({ userId }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  })

  const mutation = useMutation({
    mutationFn: updateUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user', userId] })
    },
  })

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorView error={error} />

  return <UserView user={data} onUpdate={mutation.mutate} />
}
```

### Zustand for Client State

```tsx
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import AsyncStorage from '@react-native-async-storage/async-storage'

interface AuthStore {
  user: User | null
  token: string | null
  login: (user: User, token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      login: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
)
```

## Native Modules & APIs

### Camera (Expo)

```tsx
import { CameraView, useCameraPermissions } from 'expo-camera'

export function CameraScreen() {
  const [permission, requestPermission] = useCameraPermissions()

  if (!permission) return <View />
  
  if (!permission.granted) {
    return (
      <View>
        <Text>Camera permission required</Text>
        <Button onPress={requestPermission} title="Grant Permission" />
      </View>
    )
  }

  return (
    <CameraView style={{ flex: 1 }} facing="back">
      <View style={styles.overlay}>
        <Button title="Take Photo" onPress={handleCapture} />
      </View>
    </CameraView>
  )
}
```

### Notifications

```tsx
import * as Notifications from 'expo-notifications'
import { useEffect, useRef } from 'react'

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
})

export function useNotifications() {
  const notificationListener = useRef()
  const responseListener = useRef()

  useEffect(() => {
    registerForPushNotifications()

    notificationListener.current = Notifications.addNotificationReceivedListener(
      (notification) => console.log(notification)
    )

    responseListener.current = Notifications.addNotificationResponseReceivedListener(
      (response) => console.log(response)
    )

    return () => {
      Notifications.removeNotificationSubscription(notificationListener.current)
      Notifications.removeNotificationSubscription(responseListener.current)
    }
  }, [])
}

async function registerForPushNotifications() {
  const { status } = await Notifications.requestPermissionsAsync()
  if (status !== 'granted') return

  const token = await Notifications.getExpoPushTokenAsync()
  console.log('Push token:', token.data)
}
```

### Secure Storage

```tsx
import * as SecureStore from 'expo-secure-store'

export const secureStorage = {
  async setItem(key: string, value: string) {
    await SecureStore.setItemAsync(key, value)
  },
  
  async getItem(key: string) {
    return await SecureStore.getItemAsync(key)
  },
  
  async removeItem(key: string) {
    await SecureStore.deleteItemAsync(key)
  },
}
```

## Platform-Specific Code

```tsx
import { Platform, StyleSheet } from 'react-native'

// Inline
<View style={{ paddingTop: Platform.OS === 'ios' ? 20 : 0 }} />

// Platform.select
const styles = StyleSheet.create({
  container: {
    ...Platform.select({
      ios: { shadowColor: '#000', shadowOffset: { width: 0, height: 2 } },
      android: { elevation: 4 },
    }),
  },
})

// File-based (Button.ios.tsx / Button.android.tsx)
import Button from './Button' // Auto-resolves to platform file
```

## Performance Optimization

### Memoization

```tsx
import { memo, useCallback, useMemo } from 'react'

// Memoize components
const UserCard = memo(function UserCard({ user, onPress }) {
  return (
    <Pressable onPress={() => onPress(user.id)}>
      <Text>{user.name}</Text>
    </Pressable>
  )
})

// Memoize callbacks
const handlePress = useCallback((id) => {
  navigation.navigate('User', { id })
}, [navigation])

// Memoize expensive computations
const sortedUsers = useMemo(
  () => users.sort((a, b) => a.name.localeCompare(b.name)),
  [users]
)
```

### Image Optimization

```tsx
import { Image } from 'expo-image'

// Use expo-image for better performance
<Image
  source={{ uri: imageUrl }}
  style={{ width: 200, height: 200 }}
  contentFit="cover"
  placeholder={blurhash}
  transition={200}
/>
```

### Avoid Re-renders

```tsx
// Bad: inline function creates new reference
<FlatList
  renderItem={({ item }) => <Item data={item} />}
/>

// Good: stable callback reference
const renderItem = useCallback(
  ({ item }) => <Item data={item} />,
  []
)
<FlatList renderItem={renderItem} />
```

## Testing

```tsx
// __tests__/UserCard.test.tsx
import { render, fireEvent } from '@testing-library/react-native'
import { UserCard } from '../components/UserCard'

describe('UserCard', () => {
  it('renders user name', () => {
    const { getByText } = render(
      <UserCard user={{ id: '1', name: 'John' }} />
    )
    expect(getByText('John')).toBeTruthy()
  })

  it('calls onPress with user id', () => {
    const onPress = jest.fn()
    const { getByTestId } = render(
      <UserCard user={{ id: '1', name: 'John' }} onPress={onPress} />
    )
    
    fireEvent.press(getByTestId('user-card'))
    expect(onPress).toHaveBeenCalledWith('1')
  })
})
```

## Common Pitfalls

1. **Don't use `flex: 1` without parent flex container**
2. **Always handle keyboard on forms**
3. **Use `keyExtractor` in FlatList**
4. **Test on both iOS and Android**
5. **Handle safe areas properly**
6. **Don't forget to add permissions in app.json**

## Production Checklist

- [ ] Handle all permission requests gracefully
- [ ] Implement proper error boundaries
- [ ] Add offline support where needed
- [ ] Optimize images and assets
- [ ] Test on physical devices
- [ ] Configure app icons and splash screens
- [ ] Set up EAS Build for production builds
- [ ] Implement deep linking
- [ ] Add analytics and crash reporting
