// TypeScript Code Review: React Best Practices
// This file demonstrates React patterns for code review.

import {
  useState,
  useEffect,
  useCallback,
  useMemo,
  useRef,
  createContext,
  useContext,
  memo,
  forwardRef,
  type ReactNode,
  type ComponentProps,
  type ForwardedRef,
} from 'react';

// =============================================================================
// Component Props Patterns
// =============================================================================

// Pattern: Explicit props interface
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  children: ReactNode;
}

function Button({ variant, size = 'medium', disabled, loading, onClick, children }: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled || loading}
      onClick={onClick}
    >
      {loading ? 'Loading...' : children}
    </button>
  );
}

// Pattern: Extending HTML element props
type InputProps = ComponentProps<'input'> & {
  label: string;
  error?: string;
};

function Input({ label, error, id, ...inputProps }: InputProps) {
  const inputId = id ?? `input-${label.toLowerCase().replace(/\s/g, '-')}`;

  return (
    <div className="input-group">
      <label htmlFor={inputId}>{label}</label>
      <input id={inputId} aria-invalid={!!error} aria-describedby={error ? `${inputId}-error` : undefined} {...inputProps} />
      {error && (
        <span id={`${inputId}-error`} className="error">
          {error}
        </span>
      )}
    </div>
  );
}

// Pattern: Children as function (render props)
interface DataFetcherProps<T> {
  url: string;
  children: (data: T | null, loading: boolean, error: Error | null) => ReactNode;
}

function DataFetcher<T>({ url, children }: DataFetcherProps<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;

    fetch(url)
      .then((res) => res.json())
      .then((json) => !cancelled && setData(json))
      .catch((err) => !cancelled && setError(err))
      .finally(() => !cancelled && setLoading(false));

    return () => {
      cancelled = true;
    };
  }, [url]);

  return <>{children(data, loading, error)}</>;
}

// =============================================================================
// forwardRef Pattern
// =============================================================================

interface FancyInputProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
}

const FancyInput = forwardRef(function FancyInput(
  { label, value, onChange }: FancyInputProps,
  ref: ForwardedRef<HTMLInputElement>
) {
  return (
    <div className="fancy-input">
      <label>{label}</label>
      <input ref={ref} value={value} onChange={(e) => onChange(e.target.value)} />
    </div>
  );
});

// =============================================================================
// Context Pattern
// =============================================================================

interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthContextValue {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextValue | null>(null);

function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}

function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });
      const userData = await response.json();
      setUser(userData);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({ user, login, logout, isLoading }),
    [user, login, logout, isLoading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// =============================================================================
// Custom Hooks
// =============================================================================

// Pattern: Debounced value hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Pattern: Previous value hook
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// Pattern: Local storage hook
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') {
      return initialValue;
    }
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback(
    (value: T) => {
      setStoredValue(value);
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(value));
      }
    },
    [key]
  );

  return [storedValue, setValue];
}

// Pattern: Fetch hook with status
interface UseFetchResult<T> {
  data: T | null;
  error: Error | null;
  isLoading: boolean;
  refetch: () => void;
}

function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }
      const json = await response.json();
      setData(json);
    } catch (e) {
      setError(e instanceof Error ? e : new Error('Unknown error'));
    } finally {
      setIsLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, error, isLoading, refetch: fetchData };
}

// =============================================================================
// Memoization Patterns
// =============================================================================

// Pattern: Memoized component
interface UserCardProps {
  user: User;
  onSelect: (user: User) => void;
}

const UserCard = memo(function UserCard({ user, onSelect }: UserCardProps) {
  return (
    <div className="user-card" onClick={() => onSelect(user)}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
});

// Pattern: Memoized list with stable callback
interface UserListProps {
  users: User[];
  onUserSelect: (userId: string) => void;
}

function UserList({ users, onUserSelect }: UserListProps) {
  // Memoize the callback factory
  const handleSelect = useCallback(
    (user: User) => {
      onUserSelect(user.id);
    },
    [onUserSelect]
  );

  // Memoize sorted users
  const sortedUsers = useMemo(() => [...users].sort((a, b) => a.name.localeCompare(b.name)), [users]);

  return (
    <div className="user-list">
      {sortedUsers.map((user) => (
        <UserCard key={user.id} user={user} onSelect={handleSelect} />
      ))}
    </div>
  );
}

// =============================================================================
// Compound Component Pattern
// =============================================================================

interface TabsContextValue {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabs() {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error('Tab components must be used within Tabs');
  }
  return context;
}

interface TabsProps {
  defaultTab: string;
  children: ReactNode;
}

function Tabs({ defaultTab, children }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  const value = useMemo(() => ({ activeTab, setActiveTab }), [activeTab]);

  return (
    <TabsContext.Provider value={value}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

interface TabListProps {
  children: ReactNode;
}

function TabList({ children }: TabListProps) {
  return (
    <div className="tab-list" role="tablist">
      {children}
    </div>
  );
}

interface TabProps {
  value: string;
  children: ReactNode;
}

function Tab({ value, children }: TabProps) {
  const { activeTab, setActiveTab } = useTabs();

  return (
    <button
      role="tab"
      aria-selected={activeTab === value}
      className={activeTab === value ? 'tab active' : 'tab'}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  );
}

interface TabPanelProps {
  value: string;
  children: ReactNode;
}

function TabPanel({ value, children }: TabPanelProps) {
  const { activeTab } = useTabs();

  if (activeTab !== value) return null;

  return (
    <div role="tabpanel" className="tab-panel">
      {children}
    </div>
  );
}

// Attach sub-components
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage:
// <Tabs defaultTab="tab1">
//   <Tabs.List>
//     <Tabs.Tab value="tab1">Tab 1</Tabs.Tab>
//     <Tabs.Tab value="tab2">Tab 2</Tabs.Tab>
//   </Tabs.List>
//   <Tabs.Panel value="tab1">Content 1</Tabs.Panel>
//   <Tabs.Panel value="tab2">Content 2</Tabs.Panel>
// </Tabs>

export {
  Button,
  Input,
  DataFetcher,
  FancyInput,
  AuthProvider,
  useAuth,
  useDebounce,
  usePrevious,
  useLocalStorage,
  useFetch,
  UserCard,
  UserList,
  Tabs,
};
