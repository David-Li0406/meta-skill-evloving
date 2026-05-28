# Loading States

## What is this?

One-UI loading state management with automatic page loading and button loading patterns.

## When to use

- Page loading during data fetch
- Button loading during form submit
- Background refresh without loading indicator

## Import

```typescript
import { queryMethod, mutationMethod, loadingInitialState, type LoadingState } from '@one-ui/shared/domain';
import { MxLoadingButtonDirective } from '@moxa/formoxa/mx-button';
```

---

## LoadingState Interface

```typescript
interface LoadingState {
  fetching: boolean;      // GET requests in progress
  updating: boolean;      // POST/PUT/DELETE in progress
  loading: boolean;       // fetching || updating
  successful: boolean;    // Last mutation succeeded
  fetchingCount: number;  // Concurrent GET count
  updatingCount: number;  // Concurrent mutation count
}
```

| Signal | When True | Use Case |
|--------|-----------|----------|
| `fetching()` | `queryMethod` executing | Show page loading |
| `updating()` | `mutationMethod` executing | Show button loading |
| `loading()` | Either fetching or updating | General loading check |
| `successful()` | After mutation succeeded | Trigger navigation/close dialog |

---

## Page Loading vs Button Loading

| Type | Trigger | UI | Auto-managed |
|------|---------|-----|--------------|
| **Page Loading** | `queryMethod` | Full-page spinner overlay | ✅ Yes |
| **Button Loading** | `mutationMethod` | Button spinner + disabled | ⚠️ Partial (need `[disabled]`) |

---

## Page Loading (queryMethod)

`queryMethod` automatically shows full-page loading spinner.

```typescript
// ✅ Auto page loading
loadItems: queryMethod<void, Item[]>({
  store,
  observe: () => api.getAll$(),
  next: (items) => patchState(store, { items })
})
```

### Background Refresh (No Loading)

```typescript
// ✅ No loading indicator
loadItems: queryMethod<void, Item[]>({
  store,
  observe: () => api.getAll$(),
  next: (items) => patchState(store, { items }),
  showPageLoading: false  // Silent refresh
})
```

Use `showPageLoading: false` for:
- Auto-refresh / polling
- Partial data updates
- Silent background sync

---

## Button Loading (mutationMethod)

`mutationMethod` sets `updating()` but does NOT auto-disable button.

### Critical Pattern

```html
<!-- ❌ Wrong: Button still clickable -->
<button
  mat-flat-button
  [mxButtonIsLoading]="loading()"
  [disabled]="form.invalid">
  Submit
</button>

<!-- ✅ Correct: Include loading() in disabled -->
<button
  mat-flat-button
  [mxButtonIsLoading]="loading()"
  [disabled]="form.invalid || loading()">
  Submit
</button>
```

### Why Both Are Required

| Directive | Effect |
|-----------|--------|
| `[mxButtonIsLoading]="loading()"` | Shows spinner inside button |
| `[disabled]="... \|\| loading()"` | Actually prevents clicks |

⚠️ `[mxButtonIsLoading]` only shows spinner UI — it does NOT disable the button!

---

## Dialog Close on Success

Use `successful()` signal or callback to close dialog only after API success.

### Pattern 1: Callback (Recommended)

```typescript
onSubmit(): void {
  this.#store.createItem({
    input: this.form.getRawValue(),
    next: () => this.#dialogRef.close({ success: true })  // Close on success
  });
}
```

### Pattern 2: Effect with successful()

```typescript
constructor() {
  effect(() => {
    if (this.#store.successful()) {
      this.#dialogRef.close({ success: true });
    }
  });
}
```

### Common Mistake

```typescript
// ❌ Wrong: Closes immediately, even on API failure
onSubmit(): void {
  this.#store.updateItem(formData);
  this.#dialogRef.close();  // Closes before API completes!
}
```

---

## Common Disabled Patterns

| Pattern | Expression | Use Case |
|---------|------------|----------|
| Basic | `form.invalid \|\| loading()` | Standard form submit |
| With pristine | `form.invalid \|\| !form.dirty \|\| loading()` | Enable only after changes |
| With async | `form.invalid \|\| asyncValidating() \|\| loading()` | Wait for async validators |

---

## Migration from Manual Loading

### Before (Manual)

```typescript
// ❌ Old pattern with manual loading
interface State {
  loading: boolean;
  items: Item[];
}

loadData: rxMethod<void>(
  pipe(
    tap(() => patchState(store, { loading: true })),
    switchMap(() => api.getData$()),
    tapResponse({
      next: (data) => patchState(store, { data, loading: false }),
      error: () => patchState(store, { loading: false })
    })
  )
)
```

### After (LoadingState)

```typescript
// ✅ New pattern with LoadingState
interface State extends LoadingState {
  items: Item[];
}

const initialState: State = {
  ...loadingInitialState,
  items: []
};

loadData: queryMethod<void, Item[]>({
  store,
  observe: () => api.getData$(),
  next: (data) => patchState(store, { data })
})
```

---

## Troubleshooting

### Page Loading Not Showing

1. Verify store uses `queryMethod` (not `rxMethod`)
2. Check you didn't pass `showPageLoading: false`
3. Verify `ShellComponent` passes `[isPageLoading]` to layout

### Page Loading Stuck

1. Check API error handling
2. Verify `observe` returns proper Observable
3. Check for concurrent request issues

### Button Still Clickable During Loading

Missing `loading()` in `[disabled]`:

```html
<!-- ❌ Missing -->
[disabled]="form.invalid"

<!-- ✅ Fixed -->
[disabled]="form.invalid || loading()"
```

### Refresh Not Triggering Loading

```typescript
// ❌ Wrong: showPageLoading: false
onRefresh(): void {
  this.store.loadItems(() => ({ showPageLoading: false }));
}

// ✅ Correct: Default shows loading
onRefresh(): void {
  this.store.loadItems();
}
```

---

## Related Tools

- [signal-store.md](./signal-store.md) - SignalStore pattern
- [dialogs.md](./ui/dialogs.md) - Dialog with loading
- [mx-components.md](./mx-components.md) - MxLoadingButtonDirective
