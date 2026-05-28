---
title: Use Functional HTTP Interceptors
impact: MEDIUM
impactDescription: Cleaner code, better tree-shaking
tags: http, interceptors, functional
---

## Use Functional HTTP Interceptors

Functional interceptors are simpler functions that replace class-based interceptors, with better tree-shaking and no boilerplate.

**Incorrect (Class-based interceptor):**

```typescript
@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = this.authService.getToken();
    if (token) {
      req = req.clone({
        setHeaders: { Authorization: `Bearer ${token}` }
      });
    }
    return next.handle(req);
  }
}

// Registration requires verbose provider config
providers: [
  { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
]
```

**Correct (Functional interceptor):**

```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  if (token) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }

  return next(req);
};

// app.config.ts - Clean registration
export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([authInterceptor])
    )
  ]
};
```

**Why it matters:**
- Just a function, no class boilerplate
- Use `inject()` to get dependencies
- Clean array-based registration
- Automatically applies to `httpResource()` calls

Reference: [Angular HTTP Interceptors](https://angular.dev/guide/http/interceptors)
