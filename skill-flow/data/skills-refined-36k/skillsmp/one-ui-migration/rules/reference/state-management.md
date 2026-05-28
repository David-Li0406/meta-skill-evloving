# State Management with NgRx SignalStore

## NgRx SignalStore Pattern

**Always use NgRx SignalStore pattern:**

```typescript
import { signalStore, withState, withMethods, withComputed } from '@ngrx/signals';
import { queryMethod, mutationMethod, type LoadingState } from '@one-ui/mxsecurity/shared/domain';

interface State extends LoadingState {
  data: MyData | null;
}

const initialState: State = {
  ...loadingInitialState,
  data: null
};

export const MyFeatureStore = signalStore(
  withState(initialState),
  withComputed(({ data }) => ({
    hasData: computed(() => data() !== null)
  })),
  withMethods((store, api = inject(MyApiService)) => ({
    loadData: queryMethod<void, MyData>({
      store,
      observe: () => api.getData(),
      next: (data) => {
        patchState(store, { data });
      }
    }),

    updateData: mutationMethod<MyData, void>({
      store,
      observe: (payload) => api.updateData(payload)
    })
  }))
);
```

## API Response Typing - DO NOT USE `void`

**CRITICAL**: API methods must use actual response types, NOT `void`.

### ❌ WRONG - Using `void`

```typescript
// api.ts
saveSettings$(payload: SRV_BCAST_FWD): Observable<void> {
  return this.#rest.post<void>(...);
}

// store.ts
updateData: mutationMethod<MyData, void>({
  store,
  observe: (payload) => api.saveData(payload)
})
```

### ✅ CORRECT - Using actual response type

```typescript
// shared/domain - generic response type
export type SettingDataResponse<K extends string, T> = {
  [P in K]: T;
} & {
  success: string;
};

// model.ts - feature-specific response type
export type BroadcastForwardingSettingsResponse = SettingDataResponse<'SRV_BCAST_FWD', SRV_BCAST_FWD>;

// api.ts
saveSettings$(payload: SRV_BCAST_FWD): Observable<BroadcastForwardingSettingsResponse> {
  return this.#rest.post<BroadcastForwardingSettingsResponse>(...);
}

// store.ts
updateData: mutationMethod<MyData, BroadcastForwardingSettingsResponse>({
  store,
  observe: (payload) => api.saveData(payload)
})
```

### Why?

1. **API Contract**: Types should reflect actual API responses for accurate intellisense
2. **Developer Experience**: Other developers can understand the response structure
3. **Type Safety**: Enables proper type checking when accessing response data

---

## Loading State Pattern

Use `queryMethod` and `mutationMethod` from `@one-ui/mxsecurity/shared/domain`:

- **`queryMethod`**: For fetching data (GET requests)
  - Automatically manages `fetching`, `loading` states
  - Shows page loading indicator
  - **Does NOT show success snackbar** (manual handling required if needed)

- **`mutationMethod`**: For modifying data (POST/PUT/DELETE requests)
  - Automatically manages `updating`, `loading` states
  - **Automatically shows success snackbar** (default: `response_handler.res_global_success`)
  - Handles errors with ErrorsHandler

```typescript
interface State extends LoadingState {
  // fetching: boolean
  // updating: boolean
  // loading: boolean
  // successful: boolean
  // fetchingCount: number
  // updatingCount: number
}
```

---

## ⚠️ mutationMethod Success Message (IMPORTANT)

`mutationMethod` **automatically shows a success snackbar** after successful API calls. You do NOT need to manually show a snackbar in most cases.

### ✅ Correct - Let mutationMethod handle snackbar

```typescript
// In page component
onFormSubmit(formValue: FormValue) {
  this.#store.updateSettings(() => ({
    input: formValue,
    next: () => this.#store.loadPageData() // Just reload data, no manual snackbar
  }));
}
```

### ❌ Wrong - Manually showing snackbar (redundant)

```typescript
// In page component
onFormSubmit(formValue: FormValue) {
  this.#store.updateSettings(() => ({
    input: formValue,
    next: () => {
      this.#store.loadPageData();
      // ❌ This is redundant - mutationMethod already shows success snackbar
      this.#snackBar.open(this.#transloco.translate('response_handler.res_global_success'), '', {
        duration: 3000
      });
    }
  }));
}
```

### Custom Success Message

If you need a different success message:

```typescript
this.#store.updateSettings(() => ({
  input: formValue,
  successMessage: 'custom.success.key' // Custom i18n key
}));
```

### Skip Success Snackbar

If you want to skip the success snackbar entirely:

```typescript
this.#store.updateSettings(() => ({
  input: formValue,
  skipSnackbar: true
}));
```

### queryMethod Does NOT Show Snackbar

Note that `queryMethod` does NOT automatically show a success snackbar. If you need to show a message after a refresh/load operation, you must do it manually:

```typescript
// Refresh needs manual snackbar
onRefresh() {
  this.#store.loadPageData(() => ({
    next: () => {
      this.#snackBar.open(this.#transloco.translate('response_handler.res_complete_refresh'), '', {
        duration: 3000
      });
    }
  }));
}
```

## Route Resolver Pattern

Place data loading in route resolvers, not component constructors:

```typescript
// login-page.routes.ts
import { inject } from '@angular/core';
import { Route } from '@angular/router';
import { LoginPageStore, LoginPageApiService } from '@one-ui/mxsecurity/login-page/domain';
import { LoginPageComponent } from '@one-ui/mxsecurity/login-page/features';

const loadStaticDataResolverFn = (store = inject(LoginPageStore)) => {
  store.loadStaticData();
  return true;
};

export const createRoutes = (): Route[] => [
  {
    path: '',
    component: LoginPageComponent,
    providers: [LoginPageStore, LoginPageApiService],
    resolve: {
      loadStaticData: () => loadStaticDataResolverFn()
    }
  }
];
```

## Store Best Practices

1. **Use Signals with SignalStore**

```typescript
// ❌ Mixing observables unnecessarily
export class MyComponent {
  data$ = this.store.data$.pipe(...);
}

// ✅ Use signals directly
export class MyComponent {
  data = computed(() => this.store.data());
}
```

2. **Expose Store Signals to Template**

```typescript
export class MyPageComponent {
  private store = inject(MyFeatureStore);

  // Expose store signals to template
  users = this.store.users;
  isLoading = this.store.loading;
  error = this.store.error;
}
```

3. **Use Effect for Side Effects**

```typescript
constructor() {
  effect(() => {
    // React to signal changes
    if (this.store.successful()) {
      this.router.navigate(['/success']);
    }
  });
}
```

## Shared Services

### FileDownloadService

Location: `libs/mxsecurity/shared/domain/src/lib/services/file-download.service.ts`

Use this service for downloading files from the server:

```typescript
import { FileDownloadService } from '@one-ui/mxsecurity/shared/domain';

// In store
withMethods((store, fileDownload = inject(FileDownloadService)) => ({
  exportFile: mutationMethod<void, void>({
    store,
    observe: () =>
      api.triggerExport$().pipe(
        switchMap(() => fileDownload.downloadAndSave$('filename.ini'))
      )
  })
}))
```

**Available Methods:**

- `apiHost`: Get the API host from `window.location.origin`
- `downloadFile$(fileName, basePath?)`: Download file and return `Observable<{ url, fileName }>`
- `downloadAndSave$(fileName, basePath?)`: Download file and trigger browser download

**Example - Local Config Backup:**

```typescript
localBackup: mutationMethod<void, void>({
  store,
  observe: () =>
    api.localConfigExport$().pipe(
      switchMap(() => fileDownload.downloadAndSave$('MOXA_CFG.ini'))
    )
})
```
