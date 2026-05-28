---
name: custom-hooks
description: Creating reusable custom hooks to share logic
workflows:
  - id: custom-hooks-creation
    template: wf-creation
    phase: Production
    name: Création custom hooks
    duration: 0.5-1 jour
---

# Custom Hooks - Création de Hooks Personnalisés

## Rôle

Création de hooks réutilisables pour extraire et partager la logique entre composants.

## Tu NE fais PAS

- ❌ Définir la structure des composants qui utilisent ces hooks → `../components/`
- ❌ Implémenter des solutions de styling → `../styling/`
- ❌ Définir la stratégie de tests → `testing-process`
- ❌ Implémenter le backend des APIs → `backend-developer`

## Principes

1. **Nom commence par `use`** - Convention obligatoire
2. **Appeler d'autres hooks** - C'est leur raison d'être
3. **Logique réutilisable** - Extraire ce qui est commun
4. **Composition** - Combiner plusieurs hooks

## Patterns Courants

### useToggle

```tsx
function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => setValue(v => !v), []);
  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);

  return { value, toggle, setTrue, setFalse };
}

// Usage
function Modal() {
  const { value: isOpen, toggle, setFalse: close } = useToggle();

  return (
    <>
      <button onClick={toggle}>Toggle Modal</button>
      {isOpen && <Dialog onClose={close} />}
    </>
  );
}
```

### useLocalStorage

```tsx
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') {
      return initialValue;
    }
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function
        ? value(storedValue)
        : value;
      setStoredValue(valueToStore);
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
      }
    } catch (error) {
      console.error(error);
    }
  }, [key, storedValue]);

  return [storedValue, setValue] as const;
}

// Usage
function Settings() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');

  return (
    <select value={theme} onChange={e => setTheme(e.target.value)}>
      <option value="light">Light</option>
      <option value="dark">Dark</option>
    </select>
  );
}
```

### useFetch

```tsx
interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const json = await response.json();
      setData(json);
    } catch (e) {
      setError(e instanceof Error ? e : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    const controller = new AbortController();
    fetchData();
    return () => controller.abort();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data, loading, error, refetch } = useFetch<User>(
    `/api/users/${userId}`
  );

  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} onRetry={refetch} />;
  return <Profile user={data!} />;
}
```

### useDebounce

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function Search() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery) {
      searchAPI(debouncedQuery);
    }
  }, [debouncedQuery]);

  return (
    <input
      value={query}
      onChange={e => setQuery(e.target.value)}
      placeholder="Search..."
    />
  );
}
```

### useClickOutside

```tsx
function useClickOutside<T extends HTMLElement>(
  handler: () => void
): React.RefObject<T> {
  const ref = useRef<T>(null);

  useEffect(() => {
    function handleClick(event: MouseEvent) {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        handler();
      }
    }

    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [handler]);

  return ref;
}

// Usage
function Dropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useClickOutside<HTMLDivElement>(() => setIsOpen(false));

  return (
    <div ref={dropdownRef}>
      <button onClick={() => setIsOpen(!isOpen)}>Menu</button>
      {isOpen && <Menu />}
    </div>
  );
}
```

### useMediaQuery

```tsx
function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(() => {
    if (typeof window === 'undefined') return false;
    return window.matchMedia(query).matches;
  });

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);

    function handleChange(event: MediaQueryListEvent) {
      setMatches(event.matches);
    }

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [query]);

  return matches;
}

// Usage
function ResponsiveComponent() {
  const isMobile = useMediaQuery('(max-width: 768px)');
  const prefersDark = useMediaQuery('(prefers-color-scheme: dark)');

  return isMobile ? <MobileLayout /> : <DesktopLayout />;
}
```

### useAsync

```tsx
interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

function useAsync<T>(
  asyncFunction: () => Promise<T>,
  deps: React.DependencyList = []
): AsyncState<T> & { execute: () => Promise<void> } {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const execute = useCallback(async () => {
    setState({ data: null, loading: true, error: null });
    try {
      const data = await asyncFunction();
      setState({ data, loading: false, error: null });
    } catch (error) {
      setState({
        data: null,
        loading: false,
        error: error instanceof Error ? error : new Error('Unknown error'),
      });
    }
  }, deps);

  useEffect(() => {
    execute();
  }, [execute]);

  return { ...state, execute };
}
```

## Bonnes Pratiques

### 1. Retourner des valeurs stables

```tsx
// ✅ Utiliser useMemo/useCallback
function useCounter(initial: number) {
  const [count, setCount] = useState(initial);

  const increment = useCallback(() => setCount(c => c + 1), []);
  const decrement = useCallback(() => setCount(c => c - 1), []);

  return useMemo(
    () => ({ count, increment, decrement }),
    [count, increment, decrement]
  );
}
```

### 2. Gérer le cleanup

```tsx
function useInterval(callback: () => void, delay: number | null) {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delay === null) return;

    const id = setInterval(() => savedCallback.current(), delay);
    return () => clearInterval(id);
  }, [delay]);
}
```

### 3. Documenter les hooks

```tsx
/**
 * Hook pour gérer un état de formulaire avec validation
 * @param initialValues - Valeurs initiales du formulaire
 * @param validate - Fonction de validation
 * @returns État du formulaire et handlers
 */
function useForm<T>(
  initialValues: T,
  validate: (values: T) => Partial<Record<keyof T, string>>
) {
  // ...
}
```

## Anti-patterns

```tsx
// ❌ Hook conditionnel
if (condition) {
  const [value] = useState(); // Erreur!
}

// ❌ Hook dans une boucle
for (const item of items) {
  useEffect(() => {}); // Erreur!
}

// ❌ Ne pas utiliser de hooks dans le custom hook
function useBadHook() {
  return { value: 42 }; // Ce n'est pas vraiment un hook
}
```

## Voir aussi

- `state-hooks.md` - useState et useReducer
- `effect-hooks.md` - useEffect
- `ref-hooks.md` - useRef

## Livrables

| Livrable | Description |
|----------|-------------|
| Hook personnalisé | Fonction use* réutilisable avec types |
| Documentation | JSDoc avec paramètres et valeur de retour |
| Exemples d'usage | Cas d'utilisation concrets du hook |
