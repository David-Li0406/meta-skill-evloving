---
title: Use Angular Signals for Reactive State
impact: CRITICAL
impactDescription: Fine-grained reactivity, automatic optimization
tags: signals, reactivity, state-management
---

## Use Angular Signals for Reactive State

Signals provide fine-grained reactivity where only components reading a signal are updated when it changes. This eliminates the need for manual `ChangeDetectorRef` calls.

**Incorrect (Manual change detection with OnPush):**

```typescript
@Component({
  selector: 'app-counter',
  template: `
    <p>Count: {{ count }}</p>
    <p>Double: {{ count * 2 }}</p>
    <button (click)="increment()">+</button>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CounterComponent {
  count = 0;

  constructor(private cdr: ChangeDetectorRef) {}

  increment() {
    this.count++;
    this.cdr.markForCheck(); // Manual trigger required
  }
}
```

**Correct (Signals with automatic change detection):**

```typescript
@Component({
  selector: 'app-counter',
  template: `
    <p>Count: {{ count() }}</p>
    <p>Double: {{ doubleCount() }}</p>
    <button (click)="increment()">+</button>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CounterComponent {
  count = signal(0);
  doubleCount = computed(() => this.count() * 2);

  increment() {
    this.count.update(c => c + 1);
    // No markForCheck needed - signals handle it automatically
  }
}
```

**Why it matters:**
- Signals automatically notify Angular when values change
- `computed()` creates derived values that update reactively
- No manual `ChangeDetectorRef` management needed
- Works seamlessly with OnPush change detection

Reference: [Angular Signals](https://angular.dev/guide/signals)
