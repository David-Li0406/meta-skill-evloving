---
title: Use Class-Based HTTP Interceptors
impact: MEDIUM
impactDescription: Centralized request/response handling
tags: http, interceptors
---

## Use Class-Based HTTP Interceptors

Class-based interceptors centralize cross-cutting concerns like authentication and error handling, eliminating duplicated logic across services.

**Incorrect (Duplicated auth logic in services):**

```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  constructor(private http: HttpClient, private authService: AuthService) {}

  getUsers(): Observable<User[]> {
    // Auth header added manually in every method
    const headers = new HttpHeaders().set(
      'Authorization', `Bearer ${this.authService.getToken()}`
    );
    return this.http.get<User[]>('/api/users', { headers });
  }
}
```

**Correct (Class-based interceptor):**

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

// app.module.ts
@NgModule({
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ]
})
export class AppModule {}

// Services are now clean
@Injectable({ providedIn: 'root' })
export class UserService {
  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users');  // No auth logic needed
  }
}
```

**Why it matters:**
- Centralized auth, logging, and error handling
- Services stay focused on business logic
- Use `multi: true` for multiple interceptors
- Interceptors run in order registered

Reference: [Angular HTTP Interceptors](https://v16.angular.io/guide/http#intercepting-requests-and-responses)
