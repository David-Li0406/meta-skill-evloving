# Storage Patterns for Bookmark Vault

Data persistence patterns for localStorage and server sync.

## localStorage Basic Pattern

Used for: Persisting bookmarks, settings locally.

```typescript
"use client";

import { useEffect, useState } from "react";

const STORAGE_KEY = "bookmark-vault-bookmarks";

export function useLocalBookmarks() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [mounted, setMounted] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setBookmarks(parsed);
      } catch (error) {
        console.error("Failed to parse bookmarks:", error);
      }
    }
    setMounted(true);
  }, []);

  // Save to localStorage when bookmarks change
  const saveBookmarks = useCallback((newBookmarks: Bookmark[]) => {
    setBookmarks(newBookmarks);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(newBookmarks));
  }, []);

  return { bookmarks, saveBookmarks, mounted };
}
```

**Key practices:**
- Use `useEffect` to load on mount only
- Check `mounted` before rendering to avoid hydration mismatch
- JSON.stringify/parse with error handling
- Always validate parsed data
- Call setter before writing to storage (not after)

## Zod Validation Before Saving

Used for: Ensuring valid data in storage.

```typescript
import { z } from "zod";

// Define schema
const BookmarkSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(1).max(200),
  url: z.string().url(),
  tags: z.array(z.string()).max(20).optional(),
  createdAt: z.date(),
  updatedAt: z.date(),
});

export function useValidatedStorage(key: string) {
  const save = (value: unknown) => {
    // Validate before saving
    const result = BookmarkSchema.safeParse(value);
    if (!result.success) {
      throw new Error(`Validation failed: ${result.error.message}`);
    }

    localStorage.setItem(key, JSON.stringify(result.data));
  };

  const load = () => {
    const stored = localStorage.getItem(key);
    if (!stored) return null;

    const parsed = JSON.parse(stored);
    const result = BookmarkSchema.safeParse(parsed);

    if (!result.success) {
      console.error("Stored data invalid, clearing:", result.error);
      localStorage.removeItem(key);
      return null;
    }

    return result.data;
  };

  return { save, load };
}
```

**Key practices:**
- Define Zod schema matching data type
- Use `safeParse()` (returns result object, never throws)
- Check `success` before accessing `data`
- On validation failure, log + clear corrupted data
- Save only after successful validation

## Optimistic UI Pattern

Used for: Immediate feedback while server operation completes.

```typescript
"use client";

export function useOptimisticBookmark() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [pendingAdds, setPendingAdds] = useState<Set<string>>(new Set());

  const addBookmarkOptimistic = async (
    input: CreateBookmarkInput
  ): Promise<void> => {
    // 1. Create temp ID and add to UI immediately
    const tempId = nanoid();
    const tempBookmark: Bookmark = {
      ...input,
      id: tempId,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    setBookmarks((prev) => [...prev, tempBookmark]);
    setPendingAdds((prev) => new Set([...prev, tempId]));

    // 2. Send to server
    try {
      const response = await fetch("/api/bookmarks", {
        method: "POST",
        body: JSON.stringify(input),
      });

      if (!response.ok) throw new Error("Failed to save");

      const created: Bookmark = await response.json();

      // 3. Replace temp with real bookmark
      setBookmarks((prev) =>
        prev.map((b) => (b.id === tempId ? created : b))
      );
      setPendingAdds((prev) => {
        const updated = new Set(prev);
        updated.delete(tempId);
        return updated;
      });
    } catch (error) {
      // 4. On error, remove temp bookmark
      setBookmarks((prev) => prev.filter((b) => b.id !== tempId));
      setPendingAdds((prev) => {
        const updated = new Set(prev);
        updated.delete(tempId);
        return updated;
      });
      throw error;
    }
  };

  return {
    bookmarks,
    addBookmarkOptimistic,
    pendingAdds,
  };
}
```

**Key practices:**
- Generate temp ID (e.g. with nanoid)
- Add to UI immediately with temp ID
- Mark as pending while request is in flight
- On success, replace temp with server response
- On error, remove temp bookmark
- Use pending set to show loading state on UI

## Sync Engine Pattern

Used for: Bidirectional sync between local and server.

```typescript
interface SyncState {
  isSyncing: boolean;
  lastSync: Date | null;
  error: string | null;
  pendingCount: number;
}

export function useSyncEngine() {
  const [state, setState] = useState<SyncState>({
    isSyncing: false,
    lastSync: null,
    error: null,
    pendingCount: 0,
  });

  const syncPush = async (bookmarks: Bookmark[]) => {
    setState((prev) => ({ ...prev, isSyncing: true, error: null }));

    try {
      const response = await fetch("/api/sync/push", {
        method: "POST",
        body: JSON.stringify({ bookmarks }),
      });

      if (!response.ok) throw new Error("Push failed");

      setState((prev) => ({
        ...prev,
        isSyncing: false,
        lastSync: new Date(),
        pendingCount: 0,
      }));
    } catch (error) {
      setState((prev) => ({
        ...prev,
        isSyncing: false,
        error: String(error),
      }));
      throw error;
    }
  };

  const syncPull = async () => {
    setState((prev) => ({ ...prev, isSyncing: true, error: null }));

    try {
      const response = await fetch("/api/sync/pull");
      const { bookmarks } = await response.json();

      setState((prev) => ({
        ...prev,
        isSyncing: false,
        lastSync: new Date(),
      }));

      return bookmarks;
    } catch (error) {
      setState((prev) => ({
        ...prev,
        isSyncing: false,
        error: String(error),
      }));
      throw error;
    }
  };

  return { state, syncPush, syncPull };
}
```

**Key practices:**
- Track `isSyncing` state for UI feedback
- Record `lastSync` timestamp
- Clear errors when starting new sync
- Set `pendingCount` to show queue size
- Throw errors to caller after setting state

## SessionStorage for Temporary Data

Used for: Session-only data (vault key, auth tokens).

```typescript
"use client";

const VAULT_KEY_SESSION_KEY = "bookmark-vault-key";

export function useVaultSession() {
  // Session storage is cleared on browser close
  const setUnlockedKey = (key: CryptoKey) => {
    // Store serialized key (sessionStorage only accepts strings)
    // CryptoKey cannot be JSON.stringify'd, so store reference in memory instead
    sessionStorage.setItem(VAULT_KEY_SESSION_KEY, "unlocked");
    // Keep actual key in module-level variable or Context
  };

  const getUnlockedKey = (): CryptoKey | null => {
    const isUnlocked = sessionStorage.getItem(VAULT_KEY_SESSION_KEY);
    return isUnlocked ? getKeyFromContext() : null;
  };

  const clearSession = () => {
    sessionStorage.removeItem(VAULT_KEY_SESSION_KEY);
  };

  return { setUnlockedKey, getUnlockedKey, clearSession };
}
```

**Key practices:**
- Use sessionStorage for data that should expire on browser close
- Cannot serialize CryptoKey directly, store flag + keep key in memory/Context
- Clear session on logout
- SessionStorage is per-tab (not shared across tabs)

## Error Handling in Storage

Used for: Graceful degradation when storage fails.

```typescript
export class StorageError extends Error {
  constructor(message: string, public code: "QUOTA_EXCEEDED" | "PARSE_ERROR") {
    super(message);
  }
}

export function useRobustStorage(key: string) {
  const save = (value: unknown): void => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      if (error instanceof DOMException) {
        if (error.code === 22) {
          // QuotaExceededError
          throw new StorageError("Storage quota exceeded", "QUOTA_EXCEEDED");
        }
      }
      throw new StorageError("Failed to save", "PARSE_ERROR");
    }
  };

  const load = (): unknown | null => {
    try {
      const stored = localStorage.getItem(key);
      return stored ? JSON.parse(stored) : null;
    } catch (error) {
      throw new StorageError("Failed to parse stored data", "PARSE_ERROR");
    }
  };

  return { save, load };
}
```

**Key practices:**
- Catch `DOMException` for quota exceeded errors
- Distinguish between error types
- Provide error codes for UI handling
- Log errors but don't crash the app
- Offer user option to clear old data if quota exceeded
