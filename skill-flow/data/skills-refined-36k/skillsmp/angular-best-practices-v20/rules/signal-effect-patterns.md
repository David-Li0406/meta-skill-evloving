---
title: Use effect() Correctly - Avoid Anti-Patterns
impact: HIGH
impactDescription: Misused effects cause infinite loops, memory leaks, and unpredictable behavior
tags: signals, effect, side-effects, anti-patterns, reactivity
---

## Use effect() Correctly - Avoid Anti-Patterns

effect() should be your last resort for handling side effects. Misuse leads to infinite loops, memory leaks, and hard-to-debug behavior. Prefer computed() for derived values and direct signal updates for state changes.

**Incorrect (Writing to a signal you're reading):**

```typescript
// ❌ INFINITE LOOP - effect reads count, then writes to count
@Component({...})
export class CounterComponent {
  count = signal(0);

  constructor() {
    effect(() => {
      // Reads count, triggers effect
      // Writes count, triggers effect again
      // Infinite loop!
      this.count.set(this.count() + 1);
    });
  }
}
```

**Correct (Use computed or direct update):**

```typescript
// ✅ Use computed for derived values
@Component({...})
export class CounterComponent {
  count = signal(0);
  doubledCount = computed(() => this.count() * 2); // No effect needed!

  increment() {
    this.count.update(c => c + 1);
  }
}
```

---

**Incorrect (Nested effects):**

```typescript
// ❌ Memory leak - inner effect never destroyed
@Component({...})
export class BadComponent {
  user = signal<User | null>(null);

  constructor() {
    effect(() => {
      const user = this.user();
      if (user) {
        // Creates new effect on EVERY user change
        // Old effects never cleaned up!
        effect(() => {
          console.log('Nested effect:', user.name);
        });
      }
    });
  }
}
```

**Correct (Single effect with conditional logic):**

```typescript
// ✅ One effect, conditional inside
@Component({...})
export class GoodComponent {
  user = signal<User | null>(null);

  constructor() {
    effect(() => {
      const user = this.user();
      if (user) {
        console.log('User logged in:', user.name);
        this.analyticsService.identify(user.id);
      } else {
        console.log('User logged out');
        this.analyticsService.reset();
      }
    });
  }
}
```

---

**Incorrect (Using effect to sync state):**

```typescript
// ❌ Anti-pattern: effect to derive state
@Component({...})
export class BadSyncComponent {
  firstName = signal('');
  lastName = signal('');
  fullName = signal(''); // Should be computed!

  constructor() {
    // DON'T: Use effect to sync signals
    effect(() => {
      this.fullName.set(`${this.firstName()} ${this.lastName()}`);
    }, { allowSignalWrites: true });
  }
}
```

**Correct (Use computed for derived state):**

```typescript
// ✅ computed is the right tool for derived values
@Component({...})
export class GoodSyncComponent {
  firstName = signal('');
  lastName = signal('');
  fullName = computed(() => `${this.firstName()} ${this.lastName()}`);
}
```

---

**Incorrect (Effect for parent-to-child communication):**

```typescript
// ❌ Anti-pattern: calling child methods from parent effect
@Component({
  template: `<app-child #child />`
})
export class BadParentComponent {
  data = signal<Data | null>(null);
  @ViewChild('child') child!: ChildComponent;

  constructor() {
    effect(() => {
      const data = this.data();
      if (data) {
        this.child.updateData(data); // Imperative, fragile
      }
    });
  }
}
```

**Correct (Use input binding):**

```typescript
// ✅ Declarative data flow with inputs
@Component({
  template: `<app-child [data]="data()" />`
})
export class GoodParentComponent {
  data = signal<Data | null>(null);
}

// Child receives data reactively via input
@Component({...})
export class ChildComponent {
  data = input<Data | null>(null);

  processedData = computed(() => {
    const d = this.data();
    return d ? this.process(d) : null;
  });
}
```

---

**Correct use cases for effect():**

```typescript
@Component({...})
export class CorrectEffectUsageComponent {
  theme = signal<'light' | 'dark'>('light');
  searchQuery = signal('');
  user = signal<User | null>(null);

  constructor() {
    // ✅ Sync with external API (DOM, localStorage, etc.)
    effect(() => {
      document.body.classList.toggle('dark-mode', this.theme() === 'dark');
    });

    // ✅ Persist to localStorage
    effect(() => {
      localStorage.setItem('theme', this.theme());
    });

    // ✅ Logging/Analytics (non-reactive world)
    effect(() => {
      const user = this.user();
      if (user) {
        this.analytics.identify(user.id);
      }
    });

    // ✅ Trigger imperative APIs
    effect(() => {
      const query = this.searchQuery();
      if (query.length > 0) {
        this.autocomplete.updateSuggestions(query);
      }
    });
  }
}
```

---

**Using untracked() to prevent re-runs:**

```typescript
@Component({...})
export class SmartEffectComponent {
  query = signal('');
  page = signal(1);

  constructor() {
    // Only re-run when query changes, not when page changes
    effect(() => {
      const q = this.query(); // Tracked - triggers effect
      const p = untracked(() => this.page()); // Untracked - doesn't trigger

      this.logSearch(q, p);
    });
  }
}
```

**Effect cleanup:**

```typescript
@Component({...})
export class CleanupEffectComponent {
  elementId = signal('my-element');

  constructor() {
    effect((onCleanup) => {
      const id = this.elementId();
      const handler = () => console.log('clicked');

      document.getElementById(id)?.addEventListener('click', handler);

      // Cleanup runs before next effect execution and on destroy
      onCleanup(() => {
        document.getElementById(id)?.removeEventListener('click', handler);
      });
    });
  }
}
```

**Why it matters:**
- `allowSignalWrites: true` is a code smell - usually means you should use computed()
- Effects are for syncing with non-reactive external systems
- Nested effects = guaranteed memory leaks
- Circular signal writes = infinite loops

Reference: [Angular Effect Guide](https://angular.dev/guide/signals/effect)
