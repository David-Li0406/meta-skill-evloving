# SignalStore

## What is this?

NGRX SignalStore for managing component state, replacing BehaviorSubject and rxMethod.

## When to use

- Pages that need to manage state (lists, loading, error)
- Need to call API and update UI

## Import

```typescript
import { patchState, signalStore, withState, withMethods, withComputed } from '@ngrx/signals';
import { queryMethod, mutationMethod, loadingInitialState, type LoadingState } from '@one-ui/shared/domain';
```

---

## Basic Usage

```typescript
interface State extends LoadingState {
  items: Item[];
}

const initialState: State = {
  ...loadingInitialState,
  items: []
};

export const FeatureStore = signalStore(
  withState(initialState),

  withComputed(({ items }) => ({
    itemCount: computed(() => items().length)
  })),

  withMethods((store, api = inject(FeatureApiService)) => ({
    // GET requests
    loadItems: queryMethod<void, Item[]>({
      store,
      observe: () => api.getAll$(),
      next: (items) => patchState(store, { items })
    }),

    // POST/PUT/DELETE requests
    createItem: mutationMethod<CreateInput, Item>({
      store,
      observe: (input) => api.create$(input),
      next: (item) => patchState(store, { items: [...store.items(), item] })
    })
  }))
);
```

---

## queryMethod vs mutationMethod

| Method | Use Case | Loading State | Success Feedback |
|--------|----------|---------------|------------------|
| `queryMethod` | GET requests | `fetching()` | None |
| `mutationMethod` | POST/PUT/DELETE | `updating()` | Auto snackbar |

---

## Loading States

`LoadingState` automatically manages these states:

```typescript
store.updating()   // POST/PUT/DELETE in progress
store.fetching()   // GET in progress
store.loading()    // updating() || fetching()
store.successful() // Last mutation succeeded
```

---

## Background Refresh

To not show loading animation:

```typescript
loadItems: queryMethod<void, Item[]>({
  store,
  observe: () => api.getAll$(),
  next: (items) => patchState(store, { items }),
  showPageLoading: false  // No loading indicator
})
```

---

## Routes with Resolver

```typescript
const loadDataResolver = (store = inject(FeatureStore)) => {
  store.loadItems();
  return true;
};

export const createRoutes = (): Route[] => [
  {
    path: '',
    component: FeaturePageComponent,
    providers: [FeatureStore, FeatureApiService],
    resolve: { data: () => loadDataResolver() }
  }
];
```

---

## Common Mistakes

```typescript
// ❌ WRONG: Using BehaviorSubject
private items$ = new BehaviorSubject<Item[]>([]);

// ✅ CORRECT: Using signal
readonly items = signal<Item[]>([]);

// ❌ WRONG: Using rxMethod with manual loading management
loadData: rxMethod<void>(pipe(
  tap(() => patchState(store, { loading: true })),
  switchMap(() => api.getData$()),
  ...
))

// ✅ CORRECT: Using queryMethod (auto-manages loading)
loadData: queryMethod<void, Data[]>({
  store,
  observe: () => api.getData$(),
  next: (data) => patchState(store, { data })
})
```

---

## Related Tools

- [dialogs.md](./ui/dialogs.md) - Using Store in Dialog
- [../reference/ddd-architecture.md](../reference/ddd-architecture.md) - Store belongs in Domain layer
