# Anti-Patterns to Avoid in Bookmark Vault

Common mistakes and what to do instead.

## Anti-Pattern 1: Rendering Component Inside Render

❌ **WRONG:**
```typescript
export function BookmarkList() {
  // This creates new component every render!
  const BookmarkItemWrapper = () => (
    <div>
      {bookmarks.map((b) => (
        <BookmarkCard key={b.id} bookmark={b} />
      ))}
    </div>
  );

  return <BookmarkItemWrapper />;
}
```

✅ **CORRECT:**
```typescript
// Extract to separate component
interface BookmarkItemWrapperProps {
  bookmarks: Bookmark[];
}

function BookmarkItemWrapper({ bookmarks }: BookmarkItemWrapperProps) {
  return (
    <div>
      {bookmarks.map((b) => (
        <BookmarkCard key={b.id} bookmark={b} />
      ))}
    </div>
  );
}

export function BookmarkList() {
  return <BookmarkItemWrapper bookmarks={bookmarks} />;
}
```

**Why:** Creating components inside render causes React to unmount/remount the wrapper on every render, losing state and performance.

## Anti-Pattern 2: Missing Dependency in useEffect

❌ **WRONG:**
```typescript
export function BookmarkDetail({ bookmarkId }: Props) {
  const [bookmark, setBookmark] = useState<Bookmark | null>(null);

  useEffect(() => {
    // bookmarkId is used but not in deps array!
    fetch(`/api/bookmarks/${bookmarkId}`)
      .then((r) => r.json())
      .then(setBookmark);
  }, []); // ❌ Missing bookmarkId!

  return <div>{bookmark?.title}</div>;
}
```

✅ **CORRECT:**
```typescript
export function BookmarkDetail({ bookmarkId }: Props) {
  const [bookmark, setBookmark] = useState<Bookmark | null>(null);

  useEffect(() => {
    fetch(`/api/bookmarks/${bookmarkId}`)
      .then((r) => r.json())
      .then(setBookmark);
  }, [bookmarkId]); // ✅ Included
}
```

**Why:** Missing dependencies cause stale closures. When `bookmarkId` changes, the effect doesn't re-run, so the component shows old data.

## Anti-Pattern 3: Unvalidated localStorage Data

❌ **WRONG:**
```typescript
"use client";

export function useBookmarks() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);

  useEffect(() => {
    const stored = localStorage.getItem("bookmarks");
    // No validation! Could crash if data is corrupted
    setBookmarks(JSON.parse(stored || "[]"));
  }, []);

  return bookmarks;
}
```

✅ **CORRECT:**
```typescript
"use client";

export function useBookmarks() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);

  useEffect(() => {
    const stored = localStorage.getItem("bookmarks");
    try {
      const parsed = JSON.parse(stored || "[]");

      // Validate with Zod
      const result = z.array(BookmarkSchema).safeParse(parsed);
      if (result.success) {
        setBookmarks(result.data);
      } else {
        console.error("Corrupted bookmarks, clearing:", result.error);
        localStorage.removeItem("bookmarks");
      }
    } catch (error) {
      console.error("Failed to load bookmarks:", error);
    }
  }, []);

  return bookmarks;
}
```

**Why:** Corrupted or manually-edited localStorage data will crash the app. Always validate with Zod before using.

## Anti-Pattern 4: Prop Drilling Too Deep

❌ **WRONG:**
```typescript
// Level 1
function Dashboard() {
  const onDelete = (id: string) => {
    // ...
  };
  return <BookmarkList onDelete={onDelete} />;
}

// Level 2
function BookmarkList({ onDelete }) {
  return (
    <div>
      {bookmarks.map((b) => (
        <BookmarkItem key={b.id} bookmark={b} onDelete={onDelete} />
      ))}
    </div>
  );
}

// Level 3
function BookmarkItem({ bookmark, onDelete }) {
  return (
    <div>
      <BookmarkCard bookmark={bookmark} onDelete={onDelete} />
    </div>
  );
}

// Level 4
function BookmarkCard({ bookmark, onDelete }) {
  return <button onClick={() => onDelete(bookmark.id)}>Delete</button>;
}
```

✅ **CORRECT:**
```typescript
// Use Context for cross-component state
const BookmarksContext = createContext<BookmarksContextValue | null>(null);

function BookmarkCard({ bookmark }) {
  const { deleteBookmark } = useContext(BookmarksContext);
  return (
    <button onClick={() => deleteBookmark(bookmark.id)}>Delete</button>
  );
}

// Or extract to hook
function BookmarkCard({ bookmark }) {
  const { deleteBookmark } = useBookmarks();
  return (
    <button onClick={() => deleteBookmark(bookmark.id)}>Delete</button>
  );
}
```

**Why:** Passing callbacks through 4+ levels makes refactoring hard and props unclear. Use Context or custom hooks instead.

## Anti-Pattern 5: Storing entire state in localStorage naively

❌ **WRONG:**
```typescript
"use client";

export function useBookmarks() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);

  const addBookmark = (bookmark: Bookmark) => {
    const updated = [...bookmarks, bookmark];
    setBookmarks(updated);
    // Every state change syncs to localStorage - inefficient!
    localStorage.setItem("bookmarks", JSON.stringify(updated));
  };

  return { bookmarks, addBookmark };
}
```

✅ **CORRECT:**
```typescript
"use client";

export function useBookmarks() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);

  const addBookmark = useCallback((bookmark: Bookmark) => {
    setBookmarks((prev) => [...prev, bookmark]);
  }, []);

  // Sync to localStorage when bookmarks change (via sync engine)
  useEffect(() => {
    const syncToServer = async () => {
      await useSyncEngine().syncPush(bookmarks);
    };
    syncToServer();
  }, [bookmarks]);

  return { bookmarks, addBookmark };
}
```

**Why:** Syncing on every change is inefficient. Batch changes and sync periodically or on explicit user action.

## Anti-Pattern 6: No Hydration Guard

❌ **WRONG:**
```typescript
"use client";

export function ThemeSwitcher() {
  const [theme, setTheme] = useState(() => {
    // This runs on server too during SSR!
    return localStorage.getItem("theme") || "light";
  });

  return (
    <button onClick={() => setTheme(theme === "light" ? "dark" : "light")}>
      {theme}
    </button>
  );
}
```

✅ **CORRECT:**
```typescript
"use client";

export function ThemeSwitcher() {
  const [theme, setTheme] = useState("light"); // Server-safe default
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Load after mount - only in browser
    const saved = localStorage.getItem("theme") || "light";
    setTheme(saved);
    setMounted(true);
  }, []);

  // Don't render until hydrated
  if (!mounted) return null;

  return (
    <button onClick={() => setTheme(theme === "light" ? "dark" : "light")}>
      {theme}
    </button>
  );
}
```

**Why:** Accessing localStorage during SSR causes hydration mismatch. Check `mounted` before rendering server-dependent state.

## Anti-Pattern 7: Async State Updates Without Loading State

❌ **WRONG:**
```typescript
export function DeleteBookmarkButton({ bookmarkId }: Props) {
  const handleDelete = async () => {
    // No loading state - button stays clickable while request is in flight!
    await fetch(`/api/bookmarks/${bookmarkId}`, { method: "DELETE" });
    onSuccess?.();
  };

  return <button onClick={handleDelete}>Delete</button>;
}
```

✅ **CORRECT:**
```typescript
export function DeleteBookmarkButton({ bookmarkId }: Props) {
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await fetch(`/api/bookmarks/${bookmarkId}`, { method: "DELETE" });
      onSuccess?.();
    } catch (error) {
      console.error("Delete failed:", error);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <button onClick={handleDelete} disabled={isDeleting}>
      {isDeleting ? "Deleting..." : "Delete"}
    </button>
  );
}
```

**Why:** Without loading state, users can click multiple times, causing duplicate requests. Disable button and show feedback.

## Anti-Pattern 8: Using `index` as key in lists

❌ **WRONG:**
```typescript
export function BookmarkList({ bookmarks }: Props) {
  return (
    <div>
      {bookmarks.map((b, index) => (
        <BookmarkCard key={index} bookmark={b} /> // ❌ Using index!
      ))}
    </div>
  );
}
```

If list is reordered or item is deleted, React can't track which component corresponds to which data, causing:
- Lost component state
- Incorrect animations
- Performance issues

✅ **CORRECT:**
```typescript
export function BookmarkList({ bookmarks }: Props) {
  return (
    <div>
      {bookmarks.map((b) => (
        <BookmarkCard key={b.id} bookmark={b} /> // ✅ Stable ID
      ))}
    </div>
  );
}
```

**Why:** Key should be stable across renders. Use unique ID from data, never index.

## Anti-Pattern 9: Mutating state directly

❌ **WRONG:**
```typescript
const handleAddTag = (tag: string) => {
  // Directly mutating array!
  bookmark.tags.push(tag); // ❌
  setBookmark(bookmark); // React doesn't detect change
};
```

✅ **CORRECT:**
```typescript
const handleAddTag = (tag: string) => {
  setBookmark((prev) => ({
    ...prev,
    tags: [...(prev.tags || []), tag], // New array
  }));
};
```

**Why:** React detects changes via reference equality. Mutating the same object won't trigger re-render.

## Anti-Pattern 10: Silent Errors (No Error Handling)

❌ **WRONG:**
```typescript
export function SaveBookmarkButton() {
  const handleSave = async () => {
    // If this fails, user never knows
    await fetch("/api/bookmarks", {
      method: "POST",
      body: JSON.stringify(formData),
    });
  };

  return <button onClick={handleSave}>Save</button>;
}
```

✅ **CORRECT:**
```typescript
export function SaveBookmarkButton() {
  const [error, setError] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  const handleSave = async () => {
    setError(null);
    setIsSaving(true);

    try {
      const response = await fetch("/api/bookmarks", {
        method: "POST",
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`Failed with status ${response.status}`);
      }

      const data = await response.json();
      onSuccess?.(data);
    } catch (err) {
      setError(String(err));
      toast.error("Failed to save bookmark");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <>
      <button onClick={handleSave} disabled={isSaving}>
        {isSaving ? "Saving..." : "Save"}
      </button>
      {error && <p className="text-red-500">{error}</p>}
    </>
  );
}
```

**Why:** Users need feedback when things fail. Always show error state and allow retry.

## Anti-Pattern 11: Not validating form input

❌ **WRONG:**
```typescript
const handleSubmit = (e: FormEvent) => {
  e.preventDefault();
  // No validation - could send garbage to server
  saveBookmark({ title, url, tags });
};
```

✅ **CORRECT:**
```typescript
const handleSubmit = (e: FormEvent) => {
  e.preventDefault();

  // Validate with Zod
  const result = CreateBookmarkSchema.safeParse({ title, url, tags });
  if (!result.success) {
    const errors = result.error.flatten().fieldErrors;
    setFormErrors(errors);
    return;
  }

  saveBookmark(result.data);
};
```

**Why:** Server-side validation is not enough. Validate on client for instant feedback and prevent unnecessary API calls.

## Anti-Pattern 12: Context re-renders entire tree

❌ **WRONG:**
```typescript
// Every state change re-renders all consumers
const BookmarksContext = createContext<BookmarksState | null>(null);

export function BookmarksProvider({ children }: Props) {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [filters, setFilters] = useState<Filters>({});

  return (
    <BookmarksContext.Provider value={{ bookmarks, filters }}>
      {children}
    </BookmarksContext.Provider>
  );
}
```

✅ **CORRECT:**
```typescript
// Split into separate contexts or use Zustand with selectors
const BookmarksContext = createContext<Bookmark[] | null>(null);
const FiltersContext = createContext<Filters | null>(null);

// Or use Zustand with selector
const useBookmarks = () => useBookmarksStore((s) => s.bookmarks);
const useFilters = () => useFiltersStore((s) => s.filters);

// Consumer only re-renders when their selector value changes
function BookmarkList() {
  const bookmarks = useBookmarks(); // Only re-renders on bookmarks change
  const filters = useFilters(); // Only re-renders on filter change
  return <div>{/* ... */}</div>;
}
```

**Why:** Single context value causes all consumers to re-render together. Split contexts or use Zustand for fine-grained updates.

## Anti-Pattern 13: No error boundary

❌ **WRONG:**
```typescript
export function App() {
  return (
    <BookmarksProvider>
      <Dashboard />
    </BookmarksProvider>
  );
  // If Dashboard crashes, entire app goes down
}
```

✅ **CORRECT:**
```typescript
export function App() {
  return (
    <ErrorBoundary fallback={<ErrorPage />}>
      <BookmarksProvider>
        <Dashboard />
      </BookmarksProvider>
    </ErrorBoundary>
  );
}
```

**Why:** Error boundaries prevent component crashes from taking down entire app. Provides graceful error UI.

## Anti-Pattern 14: Clearing localStorage without confirmation

❌ **WRONG:**
```typescript
const handleClear = () => {
  localStorage.clear(); // No confirmation!
};
```

✅ **CORRECT:**
```typescript
const handleClear = async () => {
  const confirmed = await showConfirmDialog({
    title: "Clear all data?",
    description: "This cannot be undone",
  });

  if (!confirmed) return;

  localStorage.removeItem("bookmark-vault-bookmarks");
  localStorage.removeItem("bookmark-vault-vault");
  toast.success("Data cleared");
};
```

**Why:** Destructive operations need explicit user confirmation. Add confirmation dialog with descriptive message.

## Summary: Red Flags to Watch For

- ❌ `useState` initialized with localStorage access
- ❌ Missing dependency in `useEffect`
- ❌ Unvalidated data from storage or API
- ❌ Prop drilling > 3 levels deep
- ❌ Components created inside render functions
- ❌ Using array index as key
- ❌ Mutating state directly
- ❌ Silent errors with no user feedback
- ❌ Destructive operations without confirmation
- ❌ No loading states on async operations
