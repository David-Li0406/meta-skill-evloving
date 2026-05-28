# Component Patterns for Bookmark Vault

All Bookmark Vault components follow these patterns.

## Form Component Pattern

Used for: Create/Edit modals for bookmarks, spaces, and vault settings.

```typescript
interface CreateBookmarkProps {
  onClose: () => void;
  onSuccess?: () => void;
}

export default function CreateBookmarkModal({
  onClose,
  onSuccess,
}: CreateBookmarkProps) {
  const [title, setTitle] = useState("");
  const [url, setUrl] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    // Validate with Zod
    const result = CreateBookmarkSchema.safeParse({ title, url });
    if (!result.success) {
      setErrors(result.error.flatten().fieldErrors as Record<string, string>);
      return;
    }

    // Submit and clear
    await addBookmark(result.data);
    setTitle("");
    setUrl("");
    onSuccess?.();
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={title} onChange={(e) => setTitle(e.target.value)} />
      {errors.title && <span className="text-red-500">{errors.title}</span>}
      <button type="submit">Save</button>
    </form>
  );
}
```

**Key practices:**
- Controlled inputs with `useState`
- Validate on submit, not onChange
- Show inline errors near fields
- Clear form after successful save
- Return success callback, let parent handle close

## List Component Pattern

Used for: BookmarkListView, SpacesList, tag lists.

```typescript
interface BookmarkListProps {
  bookmarks: Bookmark[];
  isLoading?: boolean;
  onEdit?: (bookmark: Bookmark) => void;
  onDelete?: (bookmark: Bookmark) => void;
}

export default function BookmarkList({
  bookmarks,
  isLoading,
  onEdit,
  onDelete,
}: BookmarkListProps) {
  if (isLoading) return <LoadingSpinner />;
  if (bookmarks.length === 0) return <EmptyState />;

  return (
    <div className="space-y-2">
      {bookmarks.map((bookmark) => (
        <BookmarkCard
          key={bookmark.id}
          bookmark={bookmark}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
```

**Key practices:**
- Load data in parent (via Context or hook), pass as prop
- Handle loading and empty states first
- Use `key={bookmark.id}` (never index)
- Render children via map callback
- Pass CRUD handlers to card component

## Card Component Pattern

Used for: BookmarkCard, SpaceCard, any single-item display.

```typescript
interface BookmarkCardProps {
  bookmark: Bookmark;
  onDelete?: (bookmark: Bookmark) => void;
  onEdit?: (bookmark: Bookmark) => void;
}

export default function BookmarkCard({
  bookmark,
  onDelete,
  onEdit,
}: BookmarkCardProps) {
  const [showPreview, setShowPreview] = useState(false);

  return (
    <div className="rounded border p-3">
      <a href={bookmark.url} target="_blank" rel="noopener noreferrer">
        <h3 className="font-semibold">{bookmark.title}</h3>
      </a>
      <p className="text-sm text-gray-600">{bookmark.description}</p>

      <div className="flex gap-2 mt-2">
        {bookmark.tags?.map((tag) => (
          <Badge key={tag}>{tag}</Badge>
        ))}
      </div>

      <div className="flex gap-2 mt-3">
        <button onClick={() => onEdit?.(bookmark)}>Edit</button>
        <button onClick={() => onDelete?.(bookmark)}>Delete</button>
      </div>
    </div>
  );
}
```

**Key practices:**
- Accept single item as prop (not array)
- Make URLs clickable with `target="_blank"`
- Display array fields (tags) as pills/chips/badges
- Pass delete/edit handlers as callbacks
- Local state only for UI feedback (preview, hover, etc.)

## Client Component Pattern

Used for: Any component accessing localStorage, sessionStorage, window.

```typescript
"use client";

import { useEffect, useState } from "react";

interface ThemeSwitcherProps {
  defaultTheme?: "light" | "dark";
}

export default function ThemeSwitcher({
  defaultTheme = "light",
}: ThemeSwitcherProps) {
  const [theme, setTheme] = useState(defaultTheme);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Load from localStorage after mount
    const saved = localStorage.getItem("theme");
    if (saved) setTheme(saved as "light" | "dark");
    setMounted(true);
  }, []);

  const handleToggle = () => {
    const newTheme = theme === "light" ? "dark" : "light";
    setTheme(newTheme);
    localStorage.setItem("theme", newTheme);
  };

  if (!mounted) return null; // Avoid hydration mismatch

  return <button onClick={handleToggle}>Toggle {theme}</button>;
}
```

**Key practices:**
- Always add `"use client"` directive at top
- Initialize state with default, then hydrate in `useEffect`
- Check `mounted` state before rendering (prevents hydration mismatch)
- Save to localStorage after state change, not before

## Modal/Dialog Component Pattern

Used for: Modals, dialogs, bottom sheets.

```typescript
interface DeleteConfirmSheetProps {
  isOpen: boolean;
  title: string;
  description: string;
  onConfirm: () => void;
  onCancel: () => void;
  isPending?: boolean;
}

export default function DeleteConfirmSheet({
  isOpen,
  title,
  description,
  onConfirm,
  onCancel,
  isPending,
}: DeleteConfirmSheetProps) {
  if (!isOpen) return null;

  return (
    <BottomSheet onClose={onCancel}>
      <div className="space-y-4 p-4">
        <h2 className="font-bold">{title}</h2>
        <p className="text-gray-600">{description}</p>

        <div className="flex gap-2">
          <button onClick={onCancel} disabled={isPending}>
            Cancel
          </button>
          <button
            onClick={onConfirm}
            disabled={isPending}
            className="bg-red-500"
          >
            {isPending ? "Deleting..." : "Delete"}
          </button>
        </div>
      </div>
    </BottomSheet>
  );
}
```

**Key practices:**
- Accept `isOpen` prop, return `null` if closed (don't hide with CSS)
- Pass `onConfirm` and `onCancel` callbacks
- Show loading state on button during async operations
- Disable buttons while operation is pending

## Size Guideline

- **Under 100 lines:** ✅ Preferred
- **100-200 lines:** ⚠️ OK if cohesive (e.g., BookmarkCard with preview logic)
- **200+ lines:** ❌ Split into smaller components

If a component exceeds 200 lines, refactor into:
1. Container component (state + logic)
2. Presentational component (UI only)
3. Separate hooks for complex logic
