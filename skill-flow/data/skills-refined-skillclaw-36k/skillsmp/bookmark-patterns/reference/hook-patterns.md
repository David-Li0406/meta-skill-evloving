# Hook Patterns for Bookmark Vault

Reusable logic patterns in Bookmark Vault hooks.

## Context + Reducer Hook Pattern

Used for: Complex cross-component state (bookmarks, vault).

```typescript
// 1. Define state interface
interface BookmarksState {
  bookmarks: Bookmark[];
  error: string | null;
  pendingAdds: Set<string>; // temp IDs of adds in flight
  pendingDeletes: Set<string>;
}

// 2. Define context value interface
interface BookmarksContextValue {
  state: BookmarksState;
  addBookmark: (bookmark: CreateBookmarkInput) => Promise<void>;
  deleteBookmark: (id: string) => Promise<void>;
  updateBookmark: (id: string, updates: Partial<Bookmark>) => Promise<void>;
}

// 3. Create context
const BookmarksContext = createContext<BookmarksContextValue | null>(null);

// 4. Define reducer
type BookmarkAction =
  | { type: "SET_BOOKMARKS"; payload: Bookmark[] }
  | { type: "ADD_BOOKMARK"; payload: Bookmark }
  | { type: "ADD_BOOKMARK_PENDING"; payload: string } // temp ID
  | { type: "DELETE_BOOKMARK"; payload: string }
  | { type: "SET_ERROR"; payload: string | null };

function bookmarkReducer(state: BookmarksState, action: BookmarkAction) {
  switch (action.type) {
    case "SET_BOOKMARKS":
      return { ...state, bookmarks: action.payload };
    case "ADD_BOOKMARK_PENDING":
      return {
        ...state,
        pendingAdds: new Set([...state.pendingAdds, action.payload]),
      };
    case "ADD_BOOKMARK":
      return {
        ...state,
        bookmarks: [...state.bookmarks, action.payload],
        pendingAdds: new Set(
          [...state.pendingAdds].filter((id) => id !== action.payload.id)
        ),
      };
    case "DELETE_BOOKMARK":
      return {
        ...state,
        bookmarks: state.bookmarks.filter((b) => b.id !== action.payload),
        pendingDeletes: new Set(
          [...state.pendingDeletes].filter((id) => id !== action.payload)
        ),
      };
    case "SET_ERROR":
      return { ...state, error: action.payload };
    default:
      return state;
  }
}

// 5. Create provider hook
export function useBookmarksProvider() {
  const [state, dispatch] = useReducer(bookmarkReducer, initialState);

  const addBookmark = async (bookmark: CreateBookmarkInput) => {
    const tempId = nanoid();
    dispatch({ type: "ADD_BOOKMARK_PENDING", payload: tempId });

    try {
      const result = await fetch("/api/bookmarks", {
        method: "POST",
        body: JSON.stringify(bookmark),
      });
      const created = await result.json();
      dispatch({ type: "ADD_BOOKMARK", payload: created });
    } catch (error) {
      dispatch({ type: "SET_ERROR", payload: String(error) });
    }
  };

  return {
    state,
    addBookmark,
    deleteBookmark,
    updateBookmark,
  };
}

// 6. Create hook for consumers
export function useBookmarks() {
  const context = useContext(BookmarksContext);
  if (!context) throw new Error("useBookmarks must be inside provider");
  return context;
}
```

**Key practices:**
- Define state interface first
- Actions are discriminated unions (type-safe)
- Keep reducer pure (no side effects)
- Provider hook orchestrates async operations
- Consumer hook validates context exists

## Zustand Store Pattern

Used for: Singleton state (settings, UI state, vault).

```typescript
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface SettingsStore {
  syncEnabled: boolean;
  syncMode: "off" | "plaintext" | "e2e";
  setSyncEnabled: (enabled: boolean) => void;
  setSyncMode: (mode: "off" | "plaintext" | "e2e") => void;
}

export const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      syncEnabled: false,
      syncMode: "off",
      setSyncEnabled: (enabled) => set({ syncEnabled: enabled }),
      setSyncMode: (mode) => set({ syncMode: mode }),
    }),
    {
      name: "bookmark-vault-settings", // localStorage key
      version: 1,
      migrate: (state: any, version) => {
        // Handle schema migrations
        if (version === 0) {
          return { ...state, syncMode: "plaintext" };
        }
        return state;
      },
    }
  )
);
```

**Key practices:**
- Interface defines state + actions
- `create()` initializes store
- `persist` middleware persists to localStorage
- Migration function handles schema changes
- Use selectors in components: `useSettingsStore((s) => s.syncEnabled)`

## Custom Hook for Data Fetching

Used for: Async operations with loading/error states.

```typescript
interface UseAsyncResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  retry: () => Promise<void>;
}

export function useFetchBookmarks(): UseAsyncResult<Bookmark[]> {
  const [data, setData] = useState<Bookmark[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/bookmarks");
      const bookmarks = await response.json();
      setData(bookmarks);
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Unknown error"));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetch();
  }, [fetch]);

  return { data, loading, error, retry: fetch };
}
```

**Key practices:**
- Return object with all states
- Use `useCallback` to prevent infinite loops
- Empty deps array → fetch on mount
- Provide `retry` function for user-triggered refetch
- Error is Error or null, never string

## Form Hook Pattern

Used for: Forms with validation.

```typescript
interface UseFormOptions<T> {
  initialValues: T;
  onSubmit: (values: T) => Promise<void>;
  validate?: (values: T) => Record<string, string>;
}

export function useForm<T>({
  initialValues,
  onSubmit,
  validate,
}: UseFormOptions<T>) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setValues((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (validate) {
      const newErrors = validate(values);
      setErrors(newErrors);
      if (Object.keys(newErrors).length > 0) return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(values);
      setValues(initialValues); // Reset on success
    } catch (error) {
      setErrors({ submit: String(error) });
    } finally {
      setIsSubmitting(false);
    }
  };

  return {
    values,
    errors,
    isSubmitting,
    handleChange,
    handleSubmit,
  };
}
```

**Key practices:**
- Generic type for values
- Validate on submit (not onChange)
- Provide error object with field names as keys
- Reset form after successful submit
- Return `isSubmitting` for button state

## Effect Hook Dependency Rules

```typescript
// ❌ WRONG: Dependencies missing
useEffect(() => {
  const save = async () => {
    await api.saveBookmarks(bookmarks);
  };
  save();
}, []); // Missing bookmarks dependency!

// ✅ CORRECT: All dependencies listed
useEffect(() => {
  const save = async () => {
    await api.saveBookmarks(bookmarks);
  };
  save();
}, [bookmarks]);

// ✅ GOOD: Using useCallback to stabilize function
const saveBookmarks = useCallback(async () => {
  await api.saveBookmarks(bookmarks);
}, [bookmarks]);

useEffect(() => {
  saveBookmarks();
}, [saveBookmarks]);
```

**Key practices:**
- List all external values in deps array
- Use `useCallback` to memoize functions
- Empty deps `[]` → runs once on mount
- Deps with values → runs when those values change

## Derived State Pattern

Used for: Computed values from state.

```typescript
export function useBookmarkFilters(
  bookmarks: Bookmark[],
  searchQuery: string,
  selectedTag: string | null,
  sortBy: "recent" | "title"
) {
  const filtered = useMemo(
    () =>
      bookmarks
        .filter((b) =>
          searchQuery
            ? b.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
              b.description?.toLowerCase().includes(searchQuery.toLowerCase())
            : true
        )
        .filter((b) =>
          selectedTag ? b.tags?.includes(selectedTag) : true
        )
        .sort((a, b) => {
          if (sortBy === "recent") {
            return new Date(b.createdAt).getTime() -
                   new Date(a.createdAt).getTime();
          }
          return a.title.localeCompare(b.title);
        }),
    [bookmarks, searchQuery, selectedTag, sortBy]
  );

  return {
    filtered,
    count: filtered.length,
  };
}
```

**Key practices:**
- Use `useMemo` for expensive computations
- List all dependencies in deps array
- Return object with derived data
- Never mutate original array, return new one
