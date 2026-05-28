---
title: Use TransferState for SSR Hydration
impact: MEDIUM
impactDescription: Eliminates duplicate requests on hydration
tags: http, ssr, transfer-state
---

## Use TransferState for SSR Hydration

Without TransferState, HTTP requests made on the server are repeated on the client during hydration. TransferState transfers server responses to the client, avoiding duplicates.

**Incorrect (Duplicate requests during hydration):**

```typescript
@Component({...})
export class ProductListComponent implements OnInit {
  products$!: Observable<Product[]>;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    // Runs on server AND client = 2 identical requests
    this.products$ = this.http.get<Product[]>('/api/products');
  }
}
```

**Correct (Enable HTTP cache transfer):**

```typescript
// app.config.ts
import { provideClientHydration, withHttpTransferCacheOptions } from '@angular/platform-browser';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(withFetch()),
    provideClientHydration(
      withHttpTransferCacheOptions({
        includePostRequests: true
      })
    )
  ]
};

// component.ts - No changes needed
@Component({...})
export class ProductListComponent {
  products$ = inject(HttpClient).get<Product[]>('/api/products');
  // Response transferred from server to client automatically
}
```

**Why it matters:**
- Server response cached and transferred to client
- No duplicate HTTP requests during hydration
- Faster initial page interactivity
- Works automatically with HttpClient

Reference: [Angular SSR Hydration](https://angular.dev/guide/ssr)
