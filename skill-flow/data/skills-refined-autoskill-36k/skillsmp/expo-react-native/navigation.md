# Expo Router Navigation

## Route Structure
```
app/
├── _layout.tsx          # Root layout (providers)
├── index.tsx            # Entry route (/)
├── (tabs)/
│   ├── _layout.tsx      # Tab navigator
│   ├── index.tsx        # Default tab
│   └── settings.tsx
├── (auth)/
│   ├── _layout.tsx
│   ├── login.tsx
│   └── register.tsx
└── [id].tsx             # Dynamic route
```

## Thin Routes Architecture

### Root Layout
```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';
import { AuthProvider } from '@/providers/AuthProvider';

export default function RootLayout() {
  return (
    <AuthProvider>
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="(auth)" />
      </Stack>
    </AuthProvider>
  );
}
```

### Thin Route File
```tsx
// app/profile/index.tsx
import { useLocalSearchParams } from 'expo-router';
import { Profile } from '@/screens/profile';

export default function ProfileRoute() {
  const { id } = useLocalSearchParams<{ id: string }>();
  return <Profile userId={id} />;
}
```

### Screen Component
```tsx
// screens/profile/index.tsx
import { View, Text } from 'react-native';
import { useAuth } from '@/hooks/useAuth';
import { Redirect } from 'expo-router';
import { Header } from './Header';
import { Card } from './Card';

export default function Profile({ userId }: { userId?: string }) {
  const { user } = useAuth();
  if (!user) return <Redirect href="/login" />;
  
  return (
    <View>
      <Header />
      <Card userId={userId} />
    </View>
  );
}
```

## File Structure
```
app/                      screens/
├─ _layout.tsx            ├─ profile/
├─ (tabs)/                │  ├─ index.tsx (orchestrator)
│  ├─ _layout.tsx         │  ├─ Header.tsx
│  ├─ index.tsx (thin)    │  └─ Card.tsx
│  └─ profile.tsx (thin)  ├─ home/
├─ (auth)/                │  └─ index.tsx
│  ├─ login.tsx (thin)    └─ auth/
│  └─ register.tsx (thin)    ├─ login/
└─ item/                     └─ register/
   └─ [id].tsx (thin)
```

## Navigation API

```tsx
import { useRouter, Link } from 'expo-router';

// Imperative
const router = useRouter();
router.push('/profile');
router.push({ pathname: '/item/[id]', params: { id: '123' } });
router.replace('/home');
router.back();

// Declarative
<Link href="/settings">Settings</Link>
<Link href={{ pathname: '/item/[id]', params: { id: '123' } }}>View Item</Link>
```

## Typed Route Params
```tsx
import { useLocalSearchParams } from 'expo-router';

type ProfileParams = {
  userId: string;
  tab?: 'posts' | 'likes';
};

export default function Profile() {
  const { userId, tab } = useLocalSearchParams<ProfileParams>();
}
```

## Best Practices
- **Thin routes**: Route files only extract params and render screen components
- **Screen logic**: All business logic, hooks, and components in `screens/`
- **Colocation**: Screen-specific components in same folder as screen
- **Shared components**: Place in `components/` for cross-screen reuse
- **Route groups**: Use `(groupName)` to organize without affecting URLs
