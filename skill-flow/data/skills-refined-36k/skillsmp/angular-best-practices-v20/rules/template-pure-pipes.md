---
title: Use Pure Pipes for Data Transformation
impact: HIGH
impactDescription: Memoized computation, called only when input changes
tags: pipes, pure-pipes, performance
---

## Use Pure Pipes for Data Transformation

Pure pipes are only executed when inputs change by reference. They're memoized, unlike template methods which run on every change detection cycle.

**Incorrect (Method called on every change detection):**

```typescript
@Component({
  template: `
    @for (product of products; track product.id) {
      <!-- formatPrice called on EVERY change detection cycle -->
      <span>{{ formatPrice(product.price) }}</span>
    }
  `
})
export class ProductListComponent {
  formatPrice(price: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  }
}
```

**Correct (Pure pipe only runs when input changes):**

```typescript
@Pipe({ name: 'price' })
export class PricePipe implements PipeTransform {
  transform(value: number, currency = 'USD'): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency
    }).format(value);
  }
}

@Component({
  imports: [PricePipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @for (product of products; track product.id) {
      <span>{{ product.price | price }}</span>
    }
  `
})
export class ProductListComponent {
  products = signal<Product[]>([]);
}
```

**Why it matters:**
- Pure pipes are memoized by Angular
- Only recalculate when input reference changes
- Methods in templates run on every change detection
- Significant performance gain in loops

Reference: [Angular Pipes](https://angular.dev/guide/pipes)
