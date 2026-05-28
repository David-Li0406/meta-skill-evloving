---
title: Use providedIn root for Tree-Shaking
impact: MEDIUM-HIGH
impactDescription: Enables automatic tree-shaking of unused services
tags: di, providedIn, tree-shaking
---

## Use providedIn root for Tree-Shaking

Services with `providedIn: 'root'` are tree-shakeable - if no component injects them, they're excluded from the bundle.

**Incorrect (Service always in bundle):**

```typescript
@Injectable()
export class UserService {}

@NgModule({
  providers: [UserService]  // Always in bundle, even if unused
})
export class UserModule {}
```

**Correct (Tree-shakeable with inject()):**

```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  private http = inject(HttpClient);

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users');
  }
}

// No providers array needed - just inject where used
@Component({...})
export class UserListComponent {
  private userService = inject(UserService);
  users = toSignal(this.userService.getUsers(), { initialValue: [] });
}
```

**Why it matters:**
- Unused services excluded from bundle
- No need to add to providers arrays
- Use `inject()` function for cleaner dependency injection
- Works with signals and OnPush change detection

Reference: [Angular Dependency Injection](https://angular.dev/guide/di)
