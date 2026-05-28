---
title: Use Standalone Components
impact: CRITICAL
impactDescription: Better tree-shaking, simpler architecture
tags: standalone, modules, bundle-size
---

## Use Standalone Components

Standalone components don't require NgModules, enabling better tree-shaking and granular lazy loading. In Angular v19+, components are standalone by default.

**Incorrect (NgModule-based with implicit dependencies):**

```typescript
@NgModule({
  declarations: [UserListComponent, UserDetailComponent],
  imports: [CommonModule, SharedModule],
  exports: [UserListComponent]
})
export class UserModule {}

@Component({
  selector: 'app-user-list',
  template: `...`
})
export class UserListComponent {}
// Dependencies come from module - not explicit
```

**Correct (Standalone with explicit imports):**

```typescript
@Component({
  selector: 'app-user-list',
  // No standalone: true needed in v19+
  imports: [RouterLink, UserAvatarComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @for (user of users(); track user.id) {
      <app-user-avatar [user]="user" />
      <a [routerLink]="['/users', user.id]">{{ user.name }}</a>
    }
  `
})
export class UserListComponent {
  private userService = inject(UserService);
  users = toSignal(this.userService.getUsers(), { initialValue: [] });
}
```

**Why it matters:**
- Dependencies explicit in component's `imports` array
- Better tree-shaking (unused components excluded)
- No NgModule boilerplate needed
- Components are standalone by default in v19+

Reference: [Angular Standalone Components](https://angular.dev/guide/components/importing)
