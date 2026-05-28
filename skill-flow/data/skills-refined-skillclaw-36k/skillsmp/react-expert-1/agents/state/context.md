---
name: context
description: Context API for sharing state without prop drilling
workflows:
  - id: context-setup
    template: wf-creation
    phase: Production
    name: Setup Context API
    duration: 0.5 jour
---

# Context API - État Partagé React Natif

## Rôle

Implémentation du Context API pour partager l'état entre composants sans prop drilling.

## Tu NE fais PAS

- ❌ Gérer le server state (cache, mutations) → `../data/react-query.md` ou `../data/swr.md`
- ❌ Implémenter l'UI des composants → `../components/`
- ❌ Implémenter le backend → `backend-developer`
- ❌ Définir la stratégie de tests → `testing-process`

## Quand Utiliser Context

✅ **Bon usage** :
- Thème (dark/light mode)
- Utilisateur authentifié
- Langue / i18n
- Configuration globale

❌ **Éviter pour** :
- État fréquemment mis à jour (performance)
- État complexe avec beaucoup de logique
- Cache de données serveur

## Pattern de Base

### Création du Context

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

// 1. Types
interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

// 2. Contexte avec valeur par défaut
const AuthContext = createContext<AuthContextType | null>(null);

// 3. Hook personnalisé
function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}

// 4. Provider
interface AuthProviderProps {
  children: ReactNode;
}

function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const login = async (credentials: Credentials) => {
    setIsLoading(true);
    try {
      const user = await authService.login(credentials);
      setUser(user);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    authService.logout();
  };

  const value: AuthContextType = {
    user,
    login,
    logout,
    isLoading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export { AuthProvider, useAuth };
```

### Usage

```tsx
// App.tsx
function App() {
  return (
    <AuthProvider>
      <Router />
    </AuthProvider>
  );
}

// Composant consommateur
function UserProfile() {
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <div>
      <p>Welcome, {user.name}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

## Theme Context

```tsx
type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>(() => {
    // Persister dans localStorage
    const saved = localStorage.getItem('theme') as Theme;
    return saved ?? 'light';
  });

  const toggleTheme = useCallback(() => {
    setTheme((prev) => {
      const next = prev === 'light' ? 'dark' : 'light';
      localStorage.setItem('theme', next);
      return next;
    });
  }, []);

  const value = useMemo(
    () => ({ theme, toggleTheme, setTheme }),
    [theme, toggleTheme]
  );

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}
```

## Optimisation des Re-renders

### Problème

```tsx
// ❌ Tous les enfants re-render quand value change
function BadProvider({ children }) {
  const [user, setUser] = useState(null);
  const [settings, setSettings] = useState({});

  return (
    <AppContext.Provider value={{ user, setUser, settings, setSettings }}>
      {children}
    </AppContext.Provider>
  );
}
```

### Solution 1 : Séparer les contextes

```tsx
// ✅ Contextes séparés
const UserContext = createContext<UserContextType | null>(null);
const SettingsContext = createContext<SettingsContextType | null>(null);

function AppProvider({ children }: { children: ReactNode }) {
  return (
    <UserProvider>
      <SettingsProvider>
        {children}
      </SettingsProvider>
    </UserProvider>
  );
}
```

### Solution 2 : useMemo pour la value

```tsx
// ✅ Memoize la valeur
function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const value = useMemo(
    () => ({ user, setUser }),
    [user]
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
```

### Solution 3 : Séparer state et dispatch

```tsx
const UserStateContext = createContext<User | null>(null);
const UserDispatchContext = createContext<Dispatch<UserAction> | null>(null);

function UserProvider({ children }: { children: ReactNode }) {
  const [user, dispatch] = useReducer(userReducer, null);

  return (
    <UserStateContext.Provider value={user}>
      <UserDispatchContext.Provider value={dispatch}>
        {children}
      </UserDispatchContext.Provider>
    </UserStateContext.Provider>
  );
}

// Hooks séparés
function useUserState() {
  const context = useContext(UserStateContext);
  if (context === undefined) {
    throw new Error('useUserState must be used within UserProvider');
  }
  return context;
}

function useUserDispatch() {
  const context = useContext(UserDispatchContext);
  if (!context) {
    throw new Error('useUserDispatch must be used within UserProvider');
  }
  return context;
}
```

## Context avec useReducer

```tsx
interface State {
  items: CartItem[];
  total: number;
}

type Action =
  | { type: 'ADD_ITEM'; payload: CartItem }
  | { type: 'REMOVE_ITEM'; payload: string }
  | { type: 'CLEAR' };

function cartReducer(state: State, action: Action): State {
  switch (action.type) {
    case 'ADD_ITEM':
      return {
        ...state,
        items: [...state.items, action.payload],
        total: state.total + action.payload.price,
      };
    case 'REMOVE_ITEM':
      const item = state.items.find(i => i.id === action.payload);
      return {
        ...state,
        items: state.items.filter(i => i.id !== action.payload),
        total: state.total - (item?.price ?? 0),
      };
    case 'CLEAR':
      return { items: [], total: 0 };
    default:
      return state;
  }
}

function CartProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(cartReducer, { items: [], total: 0 });

  const addItem = useCallback((item: CartItem) => {
    dispatch({ type: 'ADD_ITEM', payload: item });
  }, []);

  const removeItem = useCallback((id: string) => {
    dispatch({ type: 'REMOVE_ITEM', payload: id });
  }, []);

  const clear = useCallback(() => {
    dispatch({ type: 'CLEAR' });
  }, []);

  const value = useMemo(
    () => ({ ...state, addItem, removeItem, clear }),
    [state, addItem, removeItem, clear]
  );

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
}
```

## Composition de Providers

```tsx
// Éviter le "Provider Hell"
function AppProviders({ children }: { children: ReactNode }) {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <ThemeProvider>
            <I18nProvider>
              {children}
            </I18nProvider>
          </ThemeProvider>
        </AuthProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

// Ou avec un helper
function composeProviders(...providers: React.FC<{ children: ReactNode }>[]) {
  return ({ children }: { children: ReactNode }) =>
    providers.reduceRight(
      (acc, Provider) => <Provider>{acc}</Provider>,
      children
    );
}

const AppProviders = composeProviders(
  ErrorBoundary,
  QueryClientProvider,
  AuthProvider,
  ThemeProvider
);
```

## Bonnes Pratiques

1. **Hook personnalisé obligatoire** - Jamais `useContext` directement
2. **Validation du context** - Throw si utilisé hors provider
3. **Memoize la value** - Éviter les re-renders inutiles
4. **Contextes granulaires** - Séparer les préoccupations
5. **Préférer Zustand/Redux** - Pour l'état complexe

## Anti-patterns

```tsx
// ❌ Context pour tout l'état de l'app
const AppContext = createContext(/* tout */);

// ❌ Pas de hook personnalisé
const user = useContext(UserContext); // Pas de validation

// ❌ Object inline dans value
<Context.Provider value={{ user, setUser }}> // Nouveau ref à chaque render
```

## Voir aussi

- `zustand.md` - Alternative légère
- `redux-toolkit.md` - Pour applications complexes
- `../hooks/state-hooks.md` - État local

## Livrables

| Livrable | Description |
|----------|-------------|
| Context Provider | Provider component avec state management |
| Types TypeScript | Interfaces pour context value et props |
| Hook personnalisé | Custom hook use* avec validation |
