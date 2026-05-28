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

**Correct (Tree-shakeable with constructor injection):**

```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users');
  }
}

// Inject in constructor
@Component({...})
export class UserListComponent implements OnInit {
  users$!: Observable<User[]>;

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.users$ = this.userService.getUsers();
  }
}
```

**Why it matters:**
- Unused services excluded from bundle
- No need to add to providers arrays
- Constructor injection is the standard pattern
- Use BehaviorSubject for service state

Reference: [Angular Dependency Injection](https://angular.dev/guide/di)
