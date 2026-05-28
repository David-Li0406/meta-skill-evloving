---
name: creating-contexts
description: Create React Context providers with TypeScript for sharing state across components. Use when creating contexts, managing global state, sharing user data, theme state, or when user mentions context, provider, global state, or shared state.
---

# Create React Contexts

Create React Context providers with TypeScript for sharing state across component trees. Contexts eliminate prop drilling for global concerns like user data, themes, and settings, accessed via custom hooks with built-in type safety.

## File Structure

Contexts are organized in a flat structure:

```
resources/js/contexts/{name}-context.tsx
```

**Examples:**

- `resources/js/contexts/user-context.tsx`
- `resources/js/contexts/theme-context.tsx`
- `resources/js/contexts/settings-context.tsx`

## Core Conventions

### 1. Context + Provider + Hook Pattern

Always create three exports: Context, Provider, and custom hook:

```tsx
import type { PropsWithChildren } from 'react'
import { createContext, useContext, useState } from 'react'

interface ThemeState {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeState | undefined>(undefined)

export function ThemeProvider({ children }: PropsWithChildren) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'))
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)

  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }

  return context
}
```

**Key Requirements:**

- Use function declarations for providers and hooks (NOT arrow functions assigned to const)
- Create context with `createContext<StateType | undefined>(undefined)`
- Export a `{Name}Provider` component
- Export a `use{Name}()` custom hook
- Throw error in hook if used outside provider
- Use TypeScript interfaces for state shape

### 2. Integrating with Inertia Shared Props

Access Inertia shared data via `usePage()`:

```tsx
import type { User } from '@/types/models'
import { usePage } from '@inertiajs/react'
import type { PropsWithChildren } from 'react'
import { createContext, useContext } from 'react'

interface UserState {
  user: User
  twoFactorEnabled: boolean
}

const UserContext = createContext<UserState | undefined>(undefined)

export function UserProvider({ children }: PropsWithChildren) {
  const { user } = usePage().props

  // Handle case where user might not be authenticated
  let userState = undefined

  if (user) {
    userState = {
      user,
      twoFactorEnabled: !!user.two_factor_confirmed_at,
    }
  }

  return (
    <UserContext.Provider value={userState}>{children}</UserContext.Provider>
  )
}

export function useUser() {
  const context = useContext(UserContext)

  if (context === undefined) {
    throw new Error(
      'useUser must be used within a UserProvider with an authenticated user'
    )
  }

  return context
}
```

### 3. Context with State Management

Use `useState` or `useReducer` for complex state:

```tsx
import type { PropsWithChildren } from 'react'
import { createContext, useContext, useReducer } from 'react'

interface CartItem {
  id: number
  name: string
  quantity: number
}

interface CartState {
  items: CartItem[]
  total: number
}

interface CartActions {
  addItem: (item: CartItem) => void
  removeItem: (id: number) => void
  clearCart: () => void
}

type CartAction =
  | { type: 'ADD_ITEM'; payload: CartItem }
  | { type: 'REMOVE_ITEM'; payload: number }
  | { type: 'CLEAR_CART' }

const CartContext = createContext<(CartState & CartActions) | undefined>(
  undefined
)

function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case 'ADD_ITEM':
      return {
        items: [...state.items, action.payload],
        total: state.total + action.payload.quantity,
      }
    case 'REMOVE_ITEM':
      return {
        items: state.items.filter((item) => item.id !== action.payload),
        total: state.items.find((item) => item.id === action.payload)
          ? state.total - 1
          : state.total,
      }
    case 'CLEAR_CART':
      return { items: [], total: 0 }
    default:
      return state
  }
}

export function CartProvider({ children }: PropsWithChildren) {
  const [state, dispatch] = useReducer(cartReducer, {
    items: [],
    total: 0,
  })

  const addItem = (item: CartItem) => {
    dispatch({ type: 'ADD_ITEM', payload: item })
  }

  const removeItem = (id: number) => {
    dispatch({ type: 'REMOVE_ITEM', payload: id })
  }

  const clearCart = () => {
    dispatch({ type: 'CLEAR_CART' })
  }

  return (
    <CartContext.Provider value={{ ...state, addItem, removeItem, clearCart }}>
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const context = useContext(CartContext)

  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider')
  }

  return context
}
```

## Examples

### Example 1: Simple Read-Only Context

```tsx
import type { SupportedLocale } from '@/types'
import { usePage } from '@inertiajs/react'
import type { PropsWithChildren } from 'react'
import { createContext, useContext } from 'react'

interface LocaleState {
  currentLocale: string
  supportedLocales: Record<string, SupportedLocale>
}

const LocaleContext = createContext<LocaleState | undefined>(undefined)

export function LocaleProvider({ children }: PropsWithChildren) {
  const { supportedLocales } = usePage().props

  const currentLocale = document.documentElement.lang || 'en'

  return (
    <LocaleContext.Provider value={{ currentLocale, supportedLocales }}>
      {children}
    </LocaleContext.Provider>
  )
}

export function useLocale() {
  const context = useContext(LocaleContext)

  if (context === undefined) {
    throw new Error('useLocale must be used within a LocaleProvider')
  }

  return context
}
```

### Example 2: Context with Actions

```tsx
import type { PropsWithChildren } from 'react'
import { createContext, useContext, useState } from 'react'

interface Notification {
  id: string
  message: string
  type: 'success' | 'error' | 'info'
}

interface NotificationState {
  notifications: Notification[]
  addNotification: (message: string, type: Notification['type']) => void
  removeNotification: (id: string) => void
}

const NotificationContext = createContext<NotificationState | undefined>(
  undefined
)

export function NotificationProvider({ children }: PropsWithChildren) {
  const [notifications, setNotifications] = useState<Notification[]>([])

  const addNotification = (message: string, type: Notification['type']) => {
    const id = Math.random().toString(36).substring(7)
    setNotifications((prev) => [...prev, { id, message, type }])

    // Auto-remove after 5 seconds
    setTimeout(() => {
      removeNotification(id)
    }, 5000)
  }

  const removeNotification = (id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id))
  }

  return (
    <NotificationContext.Provider
      value={{ notifications, addNotification, removeNotification }}
    >
      {children}
    </NotificationContext.Provider>
  )
}

export function useNotifications() {
  const context = useContext(NotificationContext)

  if (context === undefined) {
    throw new Error(
      'useNotifications must be used within a NotificationProvider'
    )
  }

  return context
}
```

## Anti-Patterns

### ❌ Don't Do This

```tsx
// Don't use arrow functions assigned to const
export const ThemeProvider = ({ children }: PropsWithChildren) => {
  // ❌ Use function declaration
  const [theme, setTheme] = useState('light')
  return <ThemeContext.Provider value={{ theme }}>{children}</ThemeContext.Provider>
}

// Don't forget error handling in hook
export function useTheme() {
  return useContext(ThemeContext) // ❌ No error check
}

// Don't use any types
const ThemeContext = createContext<any>(null) // ❌ Use proper types

// Don't export the Context directly for consumption
export const ThemeContext = createContext<ThemeState>(...)
// Then in component: useContext(ThemeContext) // ❌ Use custom hook

// Don't create context without a provider
const theme = useContext(ThemeContext) // ❌ Use useTheme() hook

// Don't use default values that mask errors
const ThemeContext = createContext<ThemeState>({
  theme: 'light',
  toggleTheme: () => {},
}) // ❌ Use undefined and throw in hook
```

### ✅ Do This Instead

```tsx
// Always throw error if used outside provider
export function useTheme() {
  const context = useContext(ThemeContext)

  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }

  return context
}

// Use proper TypeScript types
const ThemeContext = createContext<ThemeState | undefined>(undefined)

// Always use custom hook
const { theme, toggleTheme } = useTheme()

// Set undefined as default and validate in hook
const ThemeContext = createContext<ThemeState | undefined>(undefined)
```

## Wrapping Providers

Wrap providers in `resources/js/app.tsx`:

```tsx
import { UserProvider } from '@/contexts/user-context'
import { ThemeProvider } from '@/contexts/theme-context'

createInertiaApp({
  resolve: (name) => resolvePageComponent(...),
  setup({ el, App, props }) {
    return createRoot(el).render(
      <ThemeProvider>
        <UserProvider>
          <App {...props} />
        </UserProvider>
      </ThemeProvider>
    )
  },
})
```

## Quality Standards

- All contexts must be fully typed with TypeScript
- Always export a custom hook (never use `useContext` directly)
- Throw errors when hooks are used outside providers
- Keep context state minimal and focused
- Use `usePage()` for Inertia shared props
- **When context provides user-facing messages, use `useTranslation()` for i18n support**
- Document required providers in component comments
- Test context providers with Pest browser tests
