---
title: Use @for with track for Loops
impact: HIGH
impactDescription: Prevents unnecessary DOM recreation
tags: template, control-flow, for, track
---

## Use @for with track for Loops

`@for` requires a `track` expression, enforcing efficient DOM reuse. Without tracking, Angular recreates all DOM elements when the array changes.

**Incorrect (No tracking causes full DOM recreation):**

```typescript
@Component({
  template: `
    <!-- All items re-render when array changes -->
    <div *ngFor="let user of users">
      <app-user-card [user]="user" />
    </div>
  `
})
export class UserListComponent {
  users: User[] = [];
}
```

**Correct (@for with required track):**

```typescript
@Component({
  template: `
    @for (user of users(); track user.id) {
      <app-user-card [user]="user" />
    } @empty {
      <p>No users found</p>
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserListComponent {
  users = signal<User[]>([]);
}
```

**Why it matters:**
- `track user.id` identifies items for DOM reuse
- Only changed items are re-rendered, not the entire list
- `@empty` block handles empty array case
- Required `track` prevents accidental performance issues

Reference: [Angular Control Flow](https://angular.dev/guide/templates/control-flow)
