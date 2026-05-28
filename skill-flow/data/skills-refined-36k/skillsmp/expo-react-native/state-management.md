# Zustand State Management

## Store Pattern with Persistence
```tsx
// stores/useAuthStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthState {
  user: User | null;
  token: string | null;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      setUser: (user) => set({ user }),
      setToken: (token) => set({ token }),
      logout: () => set({ user: null, token: null }),
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

## Selector Pattern

```tsx
// ❌ Bad - subscribes to entire store, re-renders on any change
const { user } = useAuthStore();

// ✅ Good - subscribes only to user
const user = useAuthStore((state) => state.user);

// ✅ Good - multiple selectors
const user = useAuthStore((state) => state.user);
const logout = useAuthStore((state) => state.logout);
```

## Async Actions
```tsx
const useDataStore = create<DataState>((set, get) => ({
  data: [],
  loading: false,
  fetchData: async () => {
    set({ loading: true });
    try {
      const response = await api.getData();
      set({ data: response, loading: false });
    } catch (error) {
      set({ loading: false });
      throw error;
    }
  },
}));
```

## Access Outside React
```tsx
// Get state anywhere
const token = useAuthStore.getState().token;

// Call actions anywhere
useAuthStore.getState().logout();
```

## Best Practices
- One store per domain (auth, cart, settings)
- Always use selectors to minimize re-renders
- Keep actions inside store, not components
- Use `persist` middleware for data that survives app restart
- Use `expo-secure-store` for sensitive tokens, not persisted Zustand stores
