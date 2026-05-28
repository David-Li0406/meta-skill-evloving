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
providers: [
  { provide: 'API_URL', useValue: 'https://api.example.com' }
]

@Injectable({ providedIn: 'root' })
export class ApiService {
  private apiUrl = inject('API_URL' as any);  // No type safety
}
```

**Correct (InjectionToken with inject()):**

```typescript
// tokens.ts
export interface AppConfig {
  apiUrl: string;
  timeout: number;
}

export const APP_CONFIG = new InjectionToken<AppConfig>('app.config');

// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    {
      provide: APP_CONFIG,
      useValue: { apiUrl: 'https://api.example.com', timeout: 5000 }
    }
  ]
};

// api.service.ts
@Injectable({ providedIn: 'root' })
export class ApiService {
  private config = inject(APP_CONFIG);  // Fully typed as AppConfig
}
```

**Why it matters:**
- Full type safety with `inject()`
- Compile-time checking for configuration values
- Easy to test by providing mock tokens
- Self-documenting code

Reference: [Angular InjectionToken](https://angular.dev/api/core/InjectionToken)
