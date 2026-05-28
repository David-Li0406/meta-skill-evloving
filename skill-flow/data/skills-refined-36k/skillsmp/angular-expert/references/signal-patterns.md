# Signal Patterns & State Management

Detailed patterns for Angular Signals, SignalStore, and Signal Forms. Load when implementing state management, forms, or reactive patterns.

## Table of Contents
1. [Signal vs RxJS Decision Matrix](#signal-vs-rxjs-decision-matrix)
2. [State Hierarchy](#state-hierarchy)
3. [NgRx SignalStore Patterns](#ngrx-signalstore-patterns)
4. [Signal Forms](#signal-forms)
5. [Effect Patterns](#effect-patterns)
6. [Computed Derivations](#computed-derivations)

---

## Signal vs RxJS Decision Matrix

### The State/Event Duality Heuristic

| Use Case | Use Signals | Use RxJS |
|----------|-------------|----------|
| Hold current value | ✅ | |
| Derive computed values | ✅ | |
| Template binding | ✅ | |
| Streams of user actions | | ✅ |
| HTTP requests | | ✅ |
| Complex timing (debounce, throttle) | | ✅ |
| Combine multiple async sources | | ✅ |

### Core Question

- **Signal**: "What is the value right now?" → Synchronous state
- **Observable**: "What just happened?" → Asynchronous event stream

### Interop Patterns

```typescript
// Observable → Signal (for templates)
import { toSignal } from '@angular/core/rxjs-interop';

@Component({...})
export class UserComponent {
  private users$ = this.http.get<User[]>('/api/users');

  // Convert final stage for template consumption
  users = toSignal(this.users$, { initialValue: [] });
}

// Signal → Observable (for complex side effects)
import { toObservable } from '@angular/core/rxjs-interop';

@Component({...})
export class SearchComponent {
  searchTerm = signal('');

  private searchTerm$ = toObservable(this.searchTerm);

  results = toSignal(
    this.searchTerm$.pipe(
      debounceTime(300),
      switchMap(term => this.api.search(term))
    ),
    { initialValue: [] }
  );
}
```

**Maintenance Nightmare Prevented**: Observable Soup - complex `combineLatest`/`map` chains for simple derived values. Signals provide synchronous, glitch-free derivation.

---

## State Hierarchy

### Push State Down Heuristic

```
┌─────────────────────────────────────────────────┐
│ GLOBAL STATE                                    │
│ User session, theme, language                   │
│ Implementation: Root Signal Service or Store    │
├─────────────────────────────────────────────────┤
│ FEATURE STATE                                   │
│ Filters, pagination, form data, server cache    │
│ Implementation: SignalStore provided in Route   │
├─────────────────────────────────────────────────┤
│ COMPONENT STATE                                 │
│ UI toggles, open/close, ephemeral input         │
│ Implementation: signal() on component class     │
└─────────────────────────────────────────────────┘
```

### Decision Flowchart

1. Does multiple features need this state? → Global
2. Does the route/feature own this state? → Feature (SignalStore)
3. Is it ephemeral UI state? → Component signal

**Maintenance Nightmare Prevented**: The God Store - single global store becomes coupling nexus with merge conflicts, cognitive overload, and performance bottlenecks.

---

## NgRx SignalStore Patterns

### Basic SignalStore

```typescript
import { signalStore, withState, withMethods, patchState } from '@ngrx/signals';
import { inject } from '@angular/core';

interface BookState {
  books: Book[];
  loading: boolean;
  error: string | null;
}

export const BookStore = signalStore(
  withState<BookState>({
    books: [],
    loading: false,
    error: null,
  }),
  withMethods((store, booksService = inject(BooksService)) => ({
    async loadBooks() {
      patchState(store, { loading: true, error: null });
      try {
        const books = await lastValueFrom(booksService.getAll());
        patchState(store, { books, loading: false });
      } catch (e) {
        patchState(store, { loading: false, error: 'Failed to load' });
      }
    },
    addBook(book: Book) {
      patchState(store, { books: [...store.books(), book] });
    },
  }))
);
```

### Feature-Scoped Provision

```typescript
// In route configuration
export const bookRoutes: Routes = [
  {
    path: 'books',
    component: BookListComponent,
    providers: [BookStore], // Scoped to this route tree
  },
];

// In component
@Component({...})
export class BookListComponent {
  readonly store = inject(BookStore);

  books = this.store.books;
  loading = this.store.loading;
}
```

### With Entities (CRUD Pattern)

```typescript
import { withEntities, setEntities, addEntity, removeEntity } from '@ngrx/signals/entities';

export const BookStore = signalStore(
  withEntities<Book>(),
  withMethods((store, api = inject(BookApi)) => ({
    async loadAll() {
      const books = await lastValueFrom(api.getAll());
      patchState(store, setEntities(books));
    },
    async add(book: Omit<Book, 'id'>) {
      const created = await lastValueFrom(api.create(book));
      patchState(store, addEntity(created));
    },
    remove(id: string) {
      patchState(store, removeEntity(id));
    },
  }))
);
```

### With Call State (Loading/Error)

```typescript
import { withCallState, setLoading, setLoaded, setError } from '@ngrx/signals';

export const BookStore = signalStore(
  withEntities<Book>(),
  withCallState(), // Adds loading, loaded, error signals
  withMethods((store, api = inject(BookApi)) => ({
    async loadAll() {
      patchState(store, setLoading());
      try {
        const books = await lastValueFrom(api.getAll());
        patchState(store, setEntities(books), setLoaded());
      } catch {
        patchState(store, setError('Load failed'));
      }
    },
  }))
);

// Usage in template
@if (store.loading()) {
  <spinner />
} @else if (store.error()) {
  <error-message [message]="store.error()" />
} @else {
  @for (book of store.entities(); track book.id) {
    <book-card [book]="book" />
  }
}
```

---

## Signal Forms

### Form Model Structure

Signal Forms use the data signal as source of truth, with `form()` creating a reactive FieldTree.

```typescript
import { Component, signal, computed } from '@angular/core';
import { form, Field } from '@angular/forms/signals';
import { required, email, minLength } from '@angular/forms/signals/validators';

@Component({
  selector: 'user-profile',
  standalone: true,
  imports: [Field],
  template: `
    <form (submit)="save()">
      <div class="field">
        <label for="email">Email</label>
        <input id="email" [field]="form.email" type="email" />
        @if (form.email.touched() && form.email.errors().length) {
          <span class="error">{{ form.email.errors()[0] }}</span>
        }
      </div>

      <div class="field">
        <label for="name">Name</label>
        <input id="name" [field]="form.name" type="text" />
      </div>

      <button type="submit" [disabled]="form.invalid()">Save</button>
    </form>
  `
})
export class UserProfileComponent {
  // 1. Data Source Signal
  user = signal({ email: '', name: '', age: 0 });

  // 2. Form Tree with validation
  form = form(this.user, {
    validators: {
      email: [required(), email()],
      name: [required(), minLength(2)],
    }
  });

  // 3. Derived state
  canSave = computed(() => this.form.valid() && this.form.dirty());

  save() {
    if (this.form.valid()) {
      console.log('Saving:', this.user());
    }
  }
}
```

### Field State Signals

Each field exposes:
- `value()` - Current value
- `valid()` - Validation state
- `invalid()` - Inverse of valid
- `touched()` - Has been blurred
- `dirty()` - Has been modified
- `disabled()` - Disabled state
- `errors()` - Array of error messages

### Testing Signal Forms

Interact via DOM, not directive instances:

```typescript
import { render, screen } from '@testing-library/angular';
import userEvent from '@testing-library/user-event';

it('should validate email', async () => {
  const { fixture } = await render(UserProfileComponent);
  const user = userEvent.setup();

  const input = screen.getByLabelText(/email/i);
  const button = screen.getByRole('button', { name: /save/i });

  // Initial state
  expect(button).toBeDisabled();

  // Invalid input
  await user.type(input, 'not-an-email');
  await user.tab();
  await fixture.whenStable();
  fixture.detectChanges();

  expect(screen.getByText(/invalid email/i)).toBeVisible();
  expect(button).toBeDisabled();

  // Valid input
  await user.clear(input);
  await user.type(input, 'valid@example.com');
  await fixture.whenStable();
  fixture.detectChanges();

  expect(button).toBeEnabled();
});
```

### Zod Integration

Bridge OpenAPI schemas to form validation:

```typescript
import { zodValidator } from '../util/zod-validator';
import { userSchema } from '../api/schemas/user.zod';

form = form(this.user, {
  validators: {
    // Apply OpenAPI-derived schema
    email: [zodValidator(userSchema.shape.email)],
    name: [zodValidator(userSchema.shape.name)],
  }
});
```

---

## Effect Patterns

### Basic Effect

```typescript
import { effect, signal } from '@angular/core';

@Component({...})
export class LoggingComponent {
  userName = signal('');

  constructor() {
    // Runs when userName changes
    effect(() => {
      console.log('User changed to:', this.userName());
    });
  }
}
```

### Effect with Cleanup

```typescript
effect((onCleanup) => {
  const subscription = someObservable$.subscribe();

  onCleanup(() => {
    subscription.unsubscribe();
  });
});
```

### Effect in Tests

Effects are scheduled on microtask queue. Use `TestBed.tick()`:

```typescript
it('should trigger logging effect', async () => {
  const consoleSpy = vi.spyOn(console, 'log');

  component.userName.set('John');
  TestBed.tick(); // Flush effect queue

  expect(consoleSpy).toHaveBeenCalledWith('User changed to:', 'John');
});
```

---

## Computed Derivations

### Basic Computed

```typescript
firstName = signal('John');
lastName = signal('Doe');

// Automatically updates when dependencies change
fullName = computed(() => `${this.firstName()} ${this.lastName()}`);
```

### Computed with Multiple Sources

```typescript
users = signal<User[]>([]);
filter = signal('');
sortBy = signal<'name' | 'date'>('name');

filteredAndSortedUsers = computed(() => {
  const filterValue = this.filter().toLowerCase();
  const sortKey = this.sortBy();

  return this.users()
    .filter(u => u.name.toLowerCase().includes(filterValue))
    .sort((a, b) => a[sortKey].localeCompare(b[sortKey]));
});
```

### Lazy Computed (Avoid Expensive Work)

Computed values are lazy - they only recompute when read AND a dependency changed:

```typescript
// Expensive operation only runs when actually needed
expensiveResult = computed(() => {
  const data = this.largeDataset();
  return performExpensiveTransformation(data);
});

// In template - only computes if visible
@if (showResults) {
  <results [data]="expensiveResult()" />
}
```

### Glitch-Free Guarantee

Signals guarantee glitch-free updates. Intermediate states are never observed:

```typescript
count = signal(0);
doubled = computed(() => this.count() * 2);
quadrupled = computed(() => this.doubled() * 2);

// When count changes, quadrupled sees consistent state
// Never observes "old doubled + new count"
```
