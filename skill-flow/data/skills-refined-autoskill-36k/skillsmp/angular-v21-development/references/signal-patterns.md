# Signal Patterns

Comprehensive guide for Angular signals usage in v21.

## Table of Contents

- [Basic Signals](#basic-signals)
- [Computed Signals](#computed-signals)
- [Effects](#effects)
- [RxJS Interop](#rxjs-interop)
- [Model Signals](#model-signals)
- [Best Practices](#best-practices)

## Basic Signals

### Creating Signals

```typescript
import { signal } from '@angular/core';

// WHY: signal() creates a reactive primitive
const count = signal(0);

// WHY: signal() with explicit type
const user = signal<User | null>(null);

// WHY: signal() with initial value
const items = signal<string[]>([]);
```

### Reading and Writing

```typescript
// WHY: Call signal as function to read
const currentValue = count();

// WHY: set() replaces the value entirely
count.set(5);

// WHY: update() transforms based on previous value
count.update((prev) => prev + 1);
```

### Readonly Signals

```typescript
@Injectable({ providedIn: 'root' })
export class CounterService {
  // WHY: Private mutable signal
  private readonly _count = signal(0);

  // WHY: Public readonly signal prevents external mutation
  readonly count = this._count.asReadonly();

  increment(): void {
    this._count.update((c) => c + 1);
  }
}
```

## Computed Signals

### Basic Computed

```typescript
import { signal, computed } from '@angular/core';

const firstName = signal('John');
const lastName = signal('Doe');

// WHY: computed() creates derived state that auto-updates
const fullName = computed(() => `${firstName()} ${lastName()}`);
```

### Computed with Multiple Dependencies

```typescript
const items = signal<Item[]>([]);
const filter = signal('');

// WHY: Computed reacts to any signal read inside
const filteredItems = computed(() => {
  const query = filter().toLowerCase();
  return items().filter((item) =>
    item.name.toLowerCase().includes(query)
  );
});
```

### Computed with Object Equality

```typescript
import { computed } from '@angular/core';

// WHY: Custom equality function prevents unnecessary updates
const userDetails = computed(
  () => ({
    name: user()?.name,
    email: user()?.email,
  }),
  {
    equal: (a, b) => a.name === b.name && a.email === b.email,
  }
);
```

## Effects

### Basic Effect

```typescript
import { effect, signal } from '@angular/core';

const theme = signal<'light' | 'dark'>('light');

// WHY: effect() runs side effects when signals change
effect(() => {
  document.body.classList.toggle('dark', theme() === 'dark');
});
```

### Effect with Cleanup

```typescript
effect((onCleanup) => {
  const subscription = someObservable$.subscribe();

  // WHY: onCleanup runs before next effect execution or on destroy
  onCleanup(() => subscription.unsubscribe());
});
```

### Effect in Components

```typescript
@Component({
  selector: 'app-logger',
  template: `...`,
})
export class LoggerComponent {
  readonly data = input.required<Data>();

  constructor() {
    // WHY: Effects in constructor/field initializer are destroyed with component
    effect(() => {
      console.log('Data changed:', this.data());
    });
  }
}
```

## RxJS Interop

### toSignal

```typescript
import { toSignal } from '@angular/core/rxjs-interop';
import { interval } from 'rxjs';

// WHY: toSignal() converts Observable to Signal
const counter = toSignal(interval(1000), { initialValue: 0 });

// WHY: requireSync for synchronous observables
const route = toSignal(this.route.params, { requireSync: true });
```

### toObservable

```typescript
import { toObservable } from '@angular/core/rxjs-interop';
import { switchMap } from 'rxjs/operators';

const userId = signal<string | null>(null);

// WHY: toObservable() converts Signal to Observable for RxJS operators
const user$ = toObservable(userId).pipe(
  switchMap((id) => (id ? this.userService.getUser(id) : of(null)))
);
```

## Model Signals

### Two-Way Binding with model()

```typescript
import { Component, model } from '@angular/core';

@Component({
  selector: 'app-counter',
  template: `
    <button (click)="decrement()">-</button>
    <span>{{ value() }}</span>
    <button (click)="increment()">+</button>
  `,
})
export class CounterComponent {
  // WHY: model() enables two-way binding with parent
  readonly value = model(0);

  increment(): void {
    this.value.update((v) => v + 1);
  }

  decrement(): void {
    this.value.update((v) => v - 1);
  }
}

// Usage in parent:
// <app-counter [(value)]="count" />
```

### Required Model

```typescript
// WHY: model.required() for mandatory two-way binding
readonly selected = model.required<string>();
```

## Best Practices

### DO

```typescript
// Use signal() for component state
readonly count = signal(0);

// Use computed() for derived values
readonly doubled = computed(() => this.count() * 2);

// Use input() for component inputs
readonly data = input<Data>();

// Use asReadonly() for public exposure
readonly items = this._items.asReadonly();
```

### DON'T

```typescript
// DON'T use mutate() - it's deprecated
count.mutate((v) => v++); // WRONG

// DON'T read signals in event handlers without tracking
onClick() {
  // This won't trigger reactivity
  const value = this.count();
}

// DON'T use @Input() decorator
@Input() data: Data; // WRONG - use input() instead
```

### Performance Tips

```typescript
// 1. Avoid unnecessary signal reads in templates
// BAD: Multiple reads
<div>{{ user().name }} - {{ user().email }}</div>

// GOOD: Single read with @if
@if (user(); as u) {
  <div>{{ u.name }} - {{ u.email }}</div>
}

// 2. Use computed() for expensive calculations
readonly expensive = computed(() => {
  // This only recalculates when dependencies change
  return this.items().reduce((sum, item) => sum + item.value, 0);
});
```
