---
title: Use trackBy with *ngFor
impact: HIGH
impactDescription: Prevents unnecessary DOM recreation
tags: template, ngfor, trackby, performance
---

## Use trackBy with *ngFor

Without `trackBy`, Angular recreates all DOM elements when the array reference changes. `trackBy` tells Angular how to identify items for efficient DOM reuse.

**Incorrect (DOM recreated on every update):**

```typescript
@Component({
  template: `
    <div *ngFor="let user of users">
      <app-user-card [user]="user"></app-user-card>
    </div>
  `
})
export class UserListComponent {
  users: User[] = [];

  refresh() {
    // New array = all DOM destroyed and recreated
    this.users = [...this.fetchedUsers];
  }
}
```

**Correct (trackBy enables DOM reuse):**

```typescript
@Component({
  template: `
    <div *ngFor="let user of users; trackBy: trackById">
      <app-user-card [user]="user"></app-user-card>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserListComponent {
  users: User[] = [];

  trackById(index: number, user: User): number {
    return user.id;
  }
}
```

**Why it matters:**
- Same IDs = DOM elements reused
- Only changed items are re-rendered
- Significant performance gain in large lists
- Track by `index` only when items have no unique ID

Reference: [Angular NgForOf](https://v16.angular.io/api/common/NgForOf)
