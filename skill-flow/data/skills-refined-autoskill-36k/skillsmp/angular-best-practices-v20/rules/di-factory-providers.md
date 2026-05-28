---
title: Use Factory Providers for Complex Setup
impact: MEDIUM-HIGH
impactDescription: Conditional logic, dependency injection in factories
tags: di, factory, providers
---

## Use Factory Providers for Complex Setup

Factory providers allow conditional service creation with access to other dependencies via `inject()` inside the factory function.

**Incorrect (Complex logic in constructor):**

```typescript
@Injectable({ providedIn: 'root' })
export class StorageService {
  private storage: Storage;

  constructor() {
    // Complex logic in constructor - hard to test
    if (typeof window !== 'undefined' && window.localStorage) {
      this.storage = window.localStorage;
    } else {
      this.storage = new MemoryStorage();
    }
  }
}
```

**Correct (Factory with inject()):**

```typescript
export abstract class StorageService {
  abstract getItem(key: string): string | null;
  abstract setItem(key: string, value: string): void;
}

export class LocalStorageService extends StorageService {
  getItem(key: string) { return localStorage.getItem(key); }
  setItem(key: string, value: string) { localStorage.setItem(key, value); }
}

export class MemoryStorageService extends StorageService {
  private store = new Map<string, string>();
  getItem(key: string) { return this.store.get(key) ?? null; }
  setItem(key: string, value: string) { this.store.set(key, value); }
}

// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    {
      provide: StorageService,
      useFactory: () => {
        const platformId = inject(PLATFORM_ID);
        return isPlatformBrowser(platformId)
          ? new LocalStorageService()
          : new MemoryStorageService();
      }
    }
  ]
};
```

**Why it matters:**
- Use `inject()` inside factory for dependencies
- Conditional service creation based on environment
- Clean separation of implementations
- Easy to test each implementation independently

Reference: [Angular Factory Providers](https://angular.dev/guide/di/dependency-injection-providers)
