---
title: Use httpResource for Signal-Based HTTP
impact: HIGH
impactDescription: Automatic loading states, reactive data fetching
tags: http, resource, signals, data-fetching
---

## Use httpResource for Signal-Based HTTP

`httpResource()` provides automatic loading/error states and reactive refetching when dependencies change, eliminating manual state management boilerplate.

**Incorrect (Manual loading state management):**

```typescript
@Component({
  template: `
    @if (loading) {
      <p>Loading...</p>
    } @else if (error) {
      <p>Error: {{ error }}</p>
    } @else {
      <p>{{ user?.name }}</p>
    }
  `
})
export class UserComponent implements OnInit {
  user: User | null = null;
  loading = false;
  error: string | null = null;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loading = true;
    this.http.get<User>('/api/users/1').subscribe({
      next: (user) => {
        this.user = user;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.message;
        this.loading = false;
      }
    });
  }
}
```

**Correct (httpResource with automatic state):**

```typescript
@Component({
  template: `
    @if (userResource.isLoading()) {
      <p>Loading...</p>
    } @else if (userResource.error()) {
      <p>Error: {{ userResource.error()?.message }}</p>
      <button (click)="userResource.reload()">Retry</button>
    } @else if (userResource.hasValue()) {
      <h1>{{ userResource.value().name }}</h1>
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserComponent {
  userId = signal('123');

  // Auto-refetches when userId changes
  userResource = httpResource<User>(() => `/api/users/${this.userId()}`);
}
```

**Why it matters:**
- Eliminates loading/error state boilerplate
- Automatically refetches when signal dependencies change
- Built-in `reload()` for retry functionality
- Type-safe access via `value()`, `error()`, `isLoading()`

Reference: [Angular HTTP Resource](https://angular.dev/guide/http)
