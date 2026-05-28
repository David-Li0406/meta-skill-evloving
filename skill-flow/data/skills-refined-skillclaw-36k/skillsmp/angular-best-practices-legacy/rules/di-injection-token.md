---
title: Use InjectionToken for Type-Safe Configuration
impact: MEDIUM-HIGH
impactDescription: Type safety, better testability
tags: di, injection-token, configuration
---

## Use InjectionToken for Type-Safe Configuration

`InjectionToken` provides type-safe dependency injection for non-class values like configuration objects and feature flags.

**Incorrect (String tokens lose type safety):**

```typescript
@NgModule({
  providers: [
    { provide: 'API_URL', useValue: 'https://api.example.com' }
  ]
})
export class AppModule {}

@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(@Inject('API_URL') private apiUrl: any) {}  // No type safety
}
```

**Correct (InjectionToken with @Inject):**

```typescript
// tokens.ts
export interface AppConfig {
  apiUrl: string;
  timeout: number;
}

export const APP_CONFIG = new InjectionToken<AppConfig>('app.config');

// app.module.ts
@NgModule({
  providers: [
    {
      provide: APP_CONFIG,
      useValue: { apiUrl: 'https://api.example.com', timeout: 5000 }
    }
  ]
})
export class AppModule {}

// api.service.ts
@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(@Inject(APP_CONFIG) private config: AppConfig) {}  // Typed!
}
```

**Why it matters:**
- Full type safety with `@Inject()` decorator
- Compile-time checking for configuration values
- Easy to test by providing mock tokens
- Self-documenting code

Reference: [Angular InjectionToken](https://angular.dev/api/core/InjectionToken)
