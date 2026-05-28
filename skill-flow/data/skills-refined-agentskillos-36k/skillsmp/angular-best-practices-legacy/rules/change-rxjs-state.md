---
title: Use BehaviorSubject for Reactive State
impact: CRITICAL
impactDescription: Reactive state management without Signals
tags: rxjs, behaviorsubject, state-management
---

## Use BehaviorSubject for Reactive State

Before Angular Signals (v16+), BehaviorSubject provides reactive state management. Combined with OnPush change detection and async pipe, it offers efficient updates.

**Incorrect (Imperative state with manual change detection):**

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

**Correct (BehaviorSubject with async pipe):**

```typescript
@Component({
  selector: 'app-counter',
  template: `
    <ng-container *ngIf="vm$ | async as vm">
      <p>Count: {{ vm.count }}</p>
      <p>Double: {{ vm.double }}</p>
    </ng-container>
    <button (click)="increment()">+</button>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CounterComponent {
  private countSubject = new BehaviorSubject<number>(0);

  vm$ = this.countSubject.pipe(
    map(count => ({
      count,
      double: count * 2
    }))
  );

  increment() {
    this.countSubject.next(this.countSubject.value + 1);
    // No manual markForCheck needed - async pipe handles it
  }
}
```

**State service pattern:**

```typescript
@Injectable({ providedIn: 'root' })
export class CounterState {
  private countSubject = new BehaviorSubject<number>(0);

  readonly count$ = this.countSubject.asObservable();
  readonly double$ = this.count$.pipe(map(c => c * 2));

  increment() {
    this.countSubject.next(this.countSubject.value + 1);
  }

  decrement() {
    this.countSubject.next(this.countSubject.value - 1);
  }
}
```

Reference: [RxJS BehaviorSubject](https://rxjs.dev/api/index/class/BehaviorSubject)
