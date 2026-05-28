# Good Examples from Bookmark Vault

Real patterns to follow in the Bookmark Vault codebase.

## BookmarkCard Component (Excellent Size & Structure)

**Location:** `components/bookmarks/BookmarkCard.tsx` (339 lines total)

What makes it good:
- ✅ Single responsibility: render one bookmark
- ✅ Accepts single item as prop, not array
- ✅ Props are well-typed (9 props, justified by preview logic)
- ✅ Handles local state (preview loading)
- ✅ Delegates deletions to parent via callback
- ✅ URL is clickable and opens in new tab
- ✅ Shows pending states during mutations

```typescript
interface BookmarkCardProps {
  bookmark: Bookmark;
  onDelete: (bookmark: Bookmark) => void;
  onEdit: (bookmark: Bookmark) => void;
  onTagClick: (tag: string) => void;
  isPendingAdd: boolean;
  isPendingDelete: boolean;
  isSelected: boolean;
  onToggleSelect: (id: string) => void;
  fetchPreview: (url: string) => Promise<Preview>;
  refreshPreview: (id: string) => void;
}

export default function BookmarkCard({
  bookmark,
  onDelete,
  onEdit,
  // ... other props
}: BookmarkCardProps) {
  const [preview, setPreview] = useState<Preview | null>(null);
  const [loadingPreview, setLoadingPreview] = useState(false);

  return (
    <div className="card">
      <a href={bookmark.url} target="_blank" rel="noopener noreferrer">
        <h3>{bookmark.title}</h3>
      </a>
      {/* Tags as pills */}
      {bookmark.tags?.map((tag) => (
        <Badge key={tag} onClick={() => onTagClick(tag)}>
          {tag}
        </Badge>
      ))}
      <button onClick={() => onEdit(bookmark)}>Edit</button>
      <button onClick={() => onDelete(bookmark)}>Delete</button>
    </div>
  );
}
```

## useBookmarks Context Hook (Complex but Well-Structured)

**Location:** `hooks/useBookmarks.ts` (741 lines)

Why it's good despite being large:
- ✅ Single purpose: manage bookmark state
- ✅ Uses reducer pattern (pure, testable)
- ✅ Separates concerns: CRUD from sync from import
- ✅ Exports single hook for consumers (encapsulation)
- ✅ Implements optimistic UI correctly
- ✅ Typed action discriminated union
- ✅ Error states passed to UI

```typescript
interface BookmarksContextValue {
  state: BookmarksState;
  addBookmark: (bookmark: CreateBookmarkInput) => Promise<AddResult>;
  deleteBookmark: (id: string) => Promise<void>;
  updateBookmark: (id: string, updates: Partial<Bookmark>) => Promise<void>;
  importBookmarks: (items: Bookmark[]) => Promise<void>;
}

type BookmarkAction =
  | { type: "SET_BOOKMARKS"; payload: Bookmark[] }
  | { type: "ADD_BOOKMARK"; payload: Bookmark }
  | { type: "ADD_BOOKMARK_PENDING"; payload: string }
  | { type: "ADD_BOOKMARK_ERROR"; payload: string }
  | { type: "DELETE_BOOKMARK"; payload: string }
  | { type: "SET_ERROR"; payload: string | null };

function bookmarkReducer(
  state: BookmarksState,
  action: BookmarkAction
): BookmarksState {
  switch (action.type) {
    case "ADD_BOOKMARK":
      return {
        ...state,
        bookmarks: [...state.bookmarks, action.payload],
        pendingAdds: new Set(
          [...state.pendingAdds].filter((id) => id !== action.payload.id)
        ),
      };
    // ... other cases
    default:
      return state;
  }
}
```

## EnableVaultModal (Large but Justified)

**Location:** `components/vault/EnableVaultModal.tsx` (525 lines)

Why it's good despite being large:
- ✅ Unified feature: entire vault setup flow
- ✅ Complex state machine (can't be split further without losing cohesion)
- ✅ Well-commented (explains crypto operations)
- ✅ Progressive disclosure (step by step)
- ✅ Shows loading states and progress
- ✅ Handles all error cases
- ✅ Data counts calculated correctly

Pattern:
```typescript
export function EnableVaultModal({
  isOpen,
  onClose,
  onComplete,
}: EnableVaultModalProps) {
  const [step, setStep] = useState<"passphrase" | "confirm" | "progress">(
    "passphrase"
  );
  const [passphrase, setPassphrase] = useState("");
  const [confirmPassphrase, setConfirmPassphrase] = useState("");
  const [progress, setProgress] = useState(0);

  // Progressive UI based on step
  if (step === "passphrase") return <PassphraseInput />;
  if (step === "confirm") return <ConfirmInput />;
  if (step === "progress") return <ProgressDisplay />;
}
```

## BookmarkListView (Good Container Component)

**Location:** `components/bookmarks/BookmarkListView.tsx` (176 lines)

What makes it good:
- ✅ Container component: handles data + passes to presentational
- ✅ Proper separation: data fetching vs rendering
- ✅ Uses Context to get data (not props drilling from root)
- ✅ Composes smaller components
- ✅ Handles loading/empty states
- ✅ Memoizes list to prevent unnecessary re-renders

```typescript
export default function BookmarkListView() {
  const { state, deleteBookmark, updateBookmark } = useBookmarks();
  const { bookmarks } = state;

  const memoizedList = useMemo(
    () => bookmarks.map((bookmark) => (
      <BookmarkCard
        key={bookmark.id}
        bookmark={bookmark}
        onDelete={deleteBookmark}
        onEdit={updateBookmark}
      />
    )),
    [bookmarks, deleteBookmark, updateBookmark]
  );

  if (state.isLoading) return <LoadingSpinner />;
  if (bookmarks.length === 0) return <EmptyState />;

  return <div>{memoizedList}</div>;
}
```

## BookmarkFormModal (Good Form Pattern)

**Location:** `components/bookmarks/BookmarkFormModal.tsx` (125 lines)

What makes it good:
- ✅ Controlled inputs with useState
- ✅ Validates on submit (not onChange)
- ✅ Uses Zod for validation
- ✅ Shows field-level errors
- ✅ Disables submit while pending
- ✅ Clears form after successful save

```typescript
export function BookmarkFormModal({ isOpen, onClose }: Props) {
  const [formData, setFormData] = useState<CreateBookmarkInput>({
    title: "",
    url: "",
    tags: [],
    description: "",
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    // Validate with Zod
    const result = CreateBookmarkSchema.safeParse(formData);
    if (!result.success) {
      setErrors(result.error.flatten().fieldErrors);
      return;
    }

    setIsSubmitting(true);
    try {
      await addBookmark(result.data);
      setFormData(initialState); // Reset
      onClose();
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={formData.title}
        onChange={(e) =>
          setFormData((prev) => ({ ...prev, title: e.target.value }))
        }
      />
      {errors.title && <span className="error">{errors.title}</span>}
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Saving..." : "Save"}
      </button>
    </form>
  );
}
```

## useVaultEnable Hook (Good Complex Hook)

**Location:** `hooks/useVaultEnable.ts` (274 lines)

Why it's good:
- ✅ Single responsibility: vault setup only
- ✅ Typed progress state
- ✅ Step-by-step encryption process
- ✅ Error handling at each step
- ✅ Returns progress callback for UI
- ✅ Type-safe: uses interfaces for result types

```typescript
interface VaultEnableProgress {
  step: "initializing" | "encrypting" | "uploading" | "complete";
  percentComplete: number;
  message: string;
}

interface UseVaultEnableResult {
  enable: (
    passphrase: string
  ) => Promise<{ success: true; dataCounts: DataCounts }>;
  progress: VaultEnableProgress;
  error: Error | null;
}

export function useVaultEnable(): UseVaultEnableResult {
  const [progress, setProgress] = useState<VaultEnableProgress>({
    step: "initializing",
    percentComplete: 0,
    message: "",
  });

  const enable = async (passphrase: string) => {
    // Validate passphrase strength
    setProgress((p) => ({
      ...p,
      step: "encrypting",
      message: "Generating encryption key...",
    }));

    // Steps...
    return { success: true, dataCounts };
  };

  return { enable, progress, error };
}
```

## useImportBookmarks Hook (Good State Machine)

**Location:** `hooks/useImportBookmarks.ts` (247 lines)

Why it's good:
- ✅ Clear state machine (select → preview → merge/replace → done)
- ✅ Validates file format
- ✅ Shows preview before committing
- ✅ Allows user choice (merge vs replace)
- ✅ Rollback on error
- ✅ Uses discriminated union for state

```typescript
type ImportState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "preview"; bookmarks: Bookmark[] }
  | { status: "importing"; progress: number }
  | { status: "complete"; count: number }
  | { status: "error"; message: string };

export function useImportBookmarks() {
  const [state, setState] = useState<ImportState>({ status: "idle" });

  const selectFile = async (file: File) => {
    setState({ status: "loading" });
    try {
      const json = await file.text();
      const parsed = JSON.parse(json);
      const validated = ImportBookmarksSchema.parse(parsed);
      setState({ status: "preview", bookmarks: validated });
    } catch (error) {
      setState({ status: "error", message: String(error) });
    }
  };

  const confirmImport = async (mode: "merge" | "replace") => {
    // ... import logic
  };

  return { state, selectFile, confirmImport };
}
```

## Zod Validation (Good Pattern)

**Location:** `lib/validation.ts` (126 lines)

What makes it good:
- ✅ Reusable schemas for all major types
- ✅ Custom validators (URL protocol checks, etc.)
- ✅ Discriminated unions for operations
- ✅ Exported TypeScript types from schemas
- ✅ Comprehensive validation for Bookmark type

```typescript
export const urlSchema = z
  .string()
  .url("Must be valid URL")
  .refine(
    (url) => url.startsWith("http://") || url.startsWith("https://"),
    "Must start with http:// or https://"
  );

export const CreateBookmarkSchema = z.object({
  title: z.string().min(1, "Required").max(200),
  url: urlSchema,
  description: z.string().max(500).optional(),
  tags: z.array(z.string().max(50)).max(20).optional(),
});

export type CreateBookmarkInput = z.infer<typeof CreateBookmarkSchema>;
```

## Optimistic UI in Action

**Location:** `hooks/useBookmarks.ts` + `components/bookmarks/BookmarkCard.tsx`

Pattern:
1. Show pending state immediately (opacity, loading spinner)
2. Send mutation to server
3. On success: replace temp with real data
4. On error: show toast, revert UI

```typescript
// In hook
const addBookmark = async (input: CreateBookmarkInput) => {
  const tempId = nanoid();

  // 1. Optimistic add
  dispatch({
    type: "ADD_BOOKMARK_PENDING",
    payload: tempId,
  });

  try {
    const result = await fetch("/api/bookmarks", {
      method: "POST",
      body: JSON.stringify(input),
    });

    // 2. Replace temp with real
    dispatch({
      type: "ADD_BOOKMARK",
      payload: await result.json(),
    });
  } catch {
    // 3. Revert on error
    dispatch({
      type: "ADD_BOOKMARK_ERROR",
      payload: tempId,
    });
  }
};

// In component
<BookmarkCard
  isPendingAdd={state.pendingAdds.has(bookmark.id)}
  className={state.pendingAdds.has(bookmark.id) ? "opacity-50" : ""}
/>
```

## TypeScript Strict Mode (Properly Configured)

**Location:** `tsconfig.json`

What's good:
- ✅ `"strict": true` enables all strict type checks
- ✅ No `any` type in main code (only crypto/db boundaries)
- ✅ All component props typed
- ✅ All hook returns typed
- ✅ Discriminated unions for state

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "jsx": "preserve"
  }
}
```
