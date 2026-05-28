---
title: Use TransferState for SSR
impact: MEDIUM
impactDescription: Eliminates duplicate requests on hydration
tags: http, ssr, transfer-state
---

## Use TransferState for SSR

With Server-Side Rendering, HTTP requests run on the server. Without TransferState, the client repeats these requests during hydration. TransferState transfers server data to the client.

**Incorrect (Duplicate requests):**

```typescript
@Component({...})
export class ProductListComponent implements OnInit {
  products: Product[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    // Runs on server AND client = 2 requests
    this.http.get<Product[]>('/api/products')
      .subscribe(products => this.products = products);
  }
}
```

**Correct (Manual TransferState):**

```typescript
import { TransferState, makeStateKey } from '@angular/platform-browser';
import { isPlatformServer } from '@angular/common';

const PRODUCTS_KEY = makeStateKey<Product[]>('products');

@Component({
  template: `
    <div *ngFor="let product of products; trackBy: trackById">
      {{ product.name }}
    </div>
  `
})
export class ProductListComponent implements OnInit {
  products: Product[] = [];

  constructor(
    private http: HttpClient,
    private transferState: TransferState,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit() {
    // Check if data was transferred from server
    if (this.transferState.hasKey(PRODUCTS_KEY)) {
      this.products = this.transferState.get(PRODUCTS_KEY, []);
      this.transferState.remove(PRODUCTS_KEY);
    } else {
      this.http.get<Product[]>('/api/products').subscribe(products => {
        this.products = products;
        // Store on server for client
        if (isPlatformServer(this.platformId)) {
          this.transferState.set(PRODUCTS_KEY, products);
        }
      });
    }
  }

  trackById = (index: number, product: Product) => product.id;
}
```

**Reusable service pattern:**

```typescript
@Injectable({ providedIn: 'root' })
export class TransferStateService {
  constructor(
    private transferState: TransferState,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  fetch<T>(key: string, request: Observable<T>): Observable<T> {
    const stateKey = makeStateKey<T>(key);

    if (this.transferState.hasKey(stateKey)) {
      const data = this.transferState.get(stateKey, null as T);
      this.transferState.remove(stateKey);
      return of(data);
    }

    return request.pipe(
      tap(data => {
        if (isPlatformServer(this.platformId)) {
          this.transferState.set(stateKey, data);
        }
      })
    );
  }
}

// Usage
@Injectable({ providedIn: 'root' })
export class ProductService {
  constructor(
    private http: HttpClient,
    private transferStateService: TransferStateService
  ) {}

  getProducts(): Observable<Product[]> {
    return this.transferStateService.fetch(
      'products',
      this.http.get<Product[]>('/api/products')
    );
  }
}
```

Reference: [Angular TransferState](https://v16.angular.io/api/platform-browser/TransferState)
