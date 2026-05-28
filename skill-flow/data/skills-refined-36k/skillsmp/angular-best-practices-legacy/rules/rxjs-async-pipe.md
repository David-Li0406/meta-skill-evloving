---
title: Use Async Pipe Instead of Manual Subscribe
impact: HIGH
impactDescription: Automatic cleanup, better change detection
tags: rxjs, async-pipe, memory-leaks
---

## Use Async Pipe Instead of Manual Subscribe

The async pipe automatically subscribes and unsubscribes from observables, preventing memory leaks and working seamlessly with OnPush change detection.

**Incorrect (Manual subscription):**

```typescript
@Component({
  template: `
    <div *ngIf="user">
      <h1>{{ user.name }}</h1>
    </div>
  `
})
export class UserProfileComponent implements OnInit, OnDestroy {
  user: User | null = null;
  private subscription!: Subscription;

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.subscription = this.userService.getCurrentUser()
      .subscribe(user => this.user = user);
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();  // Easy to forget
  }
}
```

**Correct (Async pipe handles lifecycle):**

```typescript
@Component({
  template: `
    <div *ngIf="user$ | async as user">
      <h1>{{ user.name }}</h1>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserProfileComponent {
  user$ = this.userService.getCurrentUser();

  constructor(private userService: UserService) {}
  // No manual subscribe/unsubscribe needed
}
```

**Why it matters:**
- No manual `Subscription` management
- No `ngOnDestroy` cleanup needed
- Works perfectly with OnPush change detection
- Use `*ngIf="obs$ | async as value"` pattern for single subscription

Reference: [Angular AsyncPipe](https://v16.angular.io/api/common/AsyncPipe)
