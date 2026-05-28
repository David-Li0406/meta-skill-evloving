---
title: Use Subject with takeUntil for Cleanup
impact: HIGH
impactDescription: Prevents memory leaks from subscriptions
tags: rxjs, memory-leaks, cleanup
---

## Use Subject with takeUntil for Cleanup

When manually subscribing to observables, use a Subject with `takeUntil` to automatically unsubscribe when the component is destroyed.

**Incorrect (Manual subscription management):**

```typescript
@Component({...})
export class DataComponent implements OnInit, OnDestroy {
  private sub1!: Subscription;
  private sub2!: Subscription;

  ngOnInit() {
    this.sub1 = this.dataService.getData()
      .subscribe(data => this.processData(data));
    this.sub2 = this.eventService.events$
      .subscribe(event => this.handleEvent(event));
  }

  ngOnDestroy() {
    this.sub1.unsubscribe();  // Easy to forget one
    this.sub2.unsubscribe();
  }
}
```

**Correct (Subject with takeUntil pattern):**

```typescript
@Component({...})
export class DataComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  ngOnInit() {
    this.dataService.getData()
      .pipe(takeUntil(this.destroy$))
      .subscribe(data => this.processData(data));

    this.eventService.events$
      .pipe(takeUntil(this.destroy$))
      .subscribe(event => this.handleEvent(event));
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

**Why it matters:**
- Single cleanup point in `ngOnDestroy`
- Can't forget to unsubscribe individual subscriptions
- Works with any number of subscriptions
- Consider base class for reuse across components

Reference: [RxJS takeUntil](https://rxjs.dev/api/operators/takeUntil)
