---
title: Use takeUntilDestroyed for Cleanup
impact: HIGH
impactDescription: Prevents memory leaks automatically
tags: rxjs, memory-leaks, cleanup
---

## Use takeUntilDestroyed for Cleanup

`takeUntilDestroyed()` automatically unsubscribes when the component is destroyed, eliminating manual cleanup boilerplate.

**Incorrect (Manual Subject-based cleanup):**

```typescript
@Component({...})
export class DataComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  ngOnInit() {
    this.dataService.getData()
      .pipe(takeUntil(this.destroy$))
      .subscribe(data => this.processData(data));
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
    // Boilerplate, easy to forget
  }
}
```

**Correct (takeUntilDestroyed handles cleanup):**

```typescript
@Component({...})
export class DataComponent {
  constructor() {
    // In constructor, DestroyRef is auto-injected
    this.dataService.getData()
      .pipe(takeUntilDestroyed())
      .subscribe(data => this.processData(data));
  }
}

// Or outside constructor:
export class DataComponent implements OnInit {
  private destroyRef = inject(DestroyRef);

  ngOnInit() {
    this.dataService.getData()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(data => this.processData(data));
  }
}
```

**Why it matters:**
- No `ngOnDestroy` boilerplate needed
- No manual `Subject` management
- Works with `DestroyRef` outside constructor
- `toSignal()` is even cleaner when possible

Reference: [Angular takeUntilDestroyed](https://angular.dev/api/core/rxjs-interop/takeUntilDestroyed)
