---
title: Use Signal Inputs for Route Parameters
impact: MEDIUM
impactDescription: Simpler routing, reactive route params
tags: routing, signals, inputs
---

## Use Signal Inputs for Route Parameters

With `withComponentInputBinding()`, route parameters are automatically bound to component inputs. Combined with signal inputs, this eliminates manual `ActivatedRoute` subscriptions.

**Incorrect (Manual route parameter subscription):**

```typescript
@Component({
  template: `<h1>User {{ userId }}</h1>`
})
export class UserDetailComponent implements OnInit, OnDestroy {
  userId: string | null = null;
  private subscription?: Subscription;

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.subscription = this.route.paramMap.subscribe((params) => {
      this.userId = params.get('id');
    });
  }

  ngOnDestroy() {
    this.subscription?.unsubscribe();
  }
}
```

**Correct (Signal input for route params):**

```typescript
// app.config.ts - Enable input binding
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withComponentInputBinding())
  ]
};

// Route: { path: 'users/:id', component: UserDetailComponent }
@Component({
  template: `<h1>User {{ id() }}</h1>`,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserDetailComponent {
  id = input.required<string>();  // Route param auto-bound
  userId = computed(() => parseInt(this.id(), 10));
}
```

**Why it matters:**
- No manual `ActivatedRoute` subscription management
- Route params, query params, and resolver data all become inputs
- Reactive updates when route changes
- Clean teardown handled automatically

Reference: [Angular Routing](https://angular.dev/guide/routing)
