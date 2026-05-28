---
name: migestion-web
description: >
  Frontend patterns for MiGestion Web - React, Vite, Zustand, design system.
  Trigger: When working on Web code (components, pages, stores, services).
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [web]
  auto_invoke: 'Creating new React components/pages'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## File Structure

```
src/
├── components/
│   └── ui/              # Reusable UI components (Button, Input, etc.)
├── pages/               # Feature pages (ClientsPage, DashboardPage, etc.)
│   └── example/
│       ├── ExamplePage.tsx
│       └── index.ts     # Barrel export
├── services/            # API service functions
├── stores/              # Zustand state stores
├── contexts/            # React contexts (Socket, etc.)
├── hooks/               # Custom hooks (useAuth, etc.)
├── lib/                 # Utilities (cn, constants)
└── types/               # Shared TypeScript types
```

## Component Pattern

```typescript
// ✅ ALWAYS: Named exports
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(baseStyles, variantStyles[variant], sizeStyles[size])}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';

// ❌ NEVER: Default export (except pages)
export default function Page() { } // OK for pages only
```

## Page Pattern

Pages are default exports in feature folders.

```typescript
// pages/example/ExamplePage.tsx
export default function ExamplePage() {
  return <div>Example Page</div>;
}

// pages/example/index.ts
export { default } from './ExamplePage';
```

## Zustand Store Pattern

```typescript
import { create } from 'zustand';

interface ExampleState {
  // State
  items: Item[];
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchItems: () => Promise<void>;
  addItem: (item: Item) => Promise<void>;
}

export const useExampleStore = create<ExampleState>((set, get) => ({
  // Initial state
  items: [],
  isLoading: false,
  error: null,

  // Actions
  fetchItems: async () => {
    try {
      set({ isLoading: true, error: null });
      const items = await exampleService.getItems();
      set({ items, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  addItem: async item => {
    const newItem = await exampleService.createItem(item);
    set(state => ({ items: [...state.items, newItem] }));
  },
}));
```

## Service Pattern

Services handle API calls using TanStack Query pattern (or direct fetch).

```typescript
import api from './api';

export const exampleService = {
  async getItems(): Promise<Item[]> {
    const response = await api.get('/examples');
    return response.data;
  },

  async getItem(id: string): Promise<Item> {
    const response = await api.get(`/examples/${id}`);
    return response.data;
  },

  async createItem(data: CreateItemInput): Promise<Item> {
    const response = await api.post('/examples', data);
    return response.data;
  },
};
```

## Design System

**Color Palette:** Neutral scale (white, black, grays)

```typescript
// ✅ ALWAYS: Use neutral colors
className = 'bg-neutral-900 text-white'; // Primary
className = 'bg-white border-neutral-300'; // Secondary
className = 'bg-error-600 text-white'; // Danger

// ❌ NEVER: No gradients in UI
className = 'bg-gradient-to-r from-blue-500 to-purple-500'; // NO!
```

**Typography:** Clean, readable, enterprise-focused

**Border-based:** No heavy shadows

```typescript
// ✅ ALWAYS: Border-based design
className = 'border border-neutral-200 rounded';

// ❌ NEVER: Heavy shadows
className = 'shadow-lg shadow-xl'; // NO!
```

## Import Pattern

Use absolute imports with `@/` alias.

```typescript
// ✅ ALWAYS: Absolute imports
import { Button } from '@/components/ui/Button';
import { useExampleStore } from '@/stores/example.store';
import * as exampleService from '@/services/example.service';

// ❌ NEVER: Relative imports (except within same folder)
import { Button } from '../../../components/ui/Button';
```

## Loading States

```typescript
const { isLoading, items, fetchItems } = useExampleStore();

useEffect(() => {
  fetchItems();
}, []);

if (isLoading) {
  return <Spinner />;
}
```

## Error Handling

```typescript
const { error, clearError } = useExampleStore();

if (error) {
  return (
    <Alert variant="error">
      {error}
      <button onClick={clearError}>Dismiss</button>
    </Alert>
  );
}
```

## Hooks Pattern

```typescript
export function useAuth() {
  const { user, token } = useAuthStore();

  return {
    isAuthenticated: !!token,
    user,
    logout: useAuthStore.getState().logout,
  };
}
```

## Context Pattern (Socket.IO)

```typescript
const SocketContext = createContext<Socket | null>(null);

export function SocketProvider({ children }: { children: ReactNode }) {
  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    const newSocket = io(SOCKET_URL);
    setSocket(newSocket);

    return () => {
      newSocket.disconnect();
    };
  }, []);

  return <SocketContext.Provider value={socket}>{children}</SocketContext.Provider>;
}
```

## Commands

```bash
npm run dev:web              # Start dev server
npm run build:web            # Build
npm run test:web             # Run tests
npm run test:e2e             # Run E2E tests
npm run lint --workspace=@migestion/web  # Lint
npm run typecheck            # Type check
```

## Related Skills

- `react-18` - React component patterns
- `zustand-4` - Zustand store patterns
- `tailwind` - Tailwind CSS utilities
- `vite` - Vite build patterns
- `migestion-test-web` - E2E testing patterns
