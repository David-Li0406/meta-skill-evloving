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
    <div *ngFor="let product of products; trackBy: trackById">
      <span>{{ formatPrice(product.price) }}</span>
    </div>
  `
})
export class ProductListComponent {
  formatPrice(price: number): string {
    // Called on EVERY change detection cycle
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
  template: `
    <div *ngFor="let product of products; trackBy: trackById">
      <span>{{ product.price | price }}</span>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ProductListComponent {
  trackById = (index: number, product: Product) => product.id;
}
```

**Why it matters:**
- Pure pipes are memoized by Angular
- Only recalculate when input reference changes
- Methods run on every change detection cycle
- Declare pipes in NgModule and add to exports

Reference: [Angular Pipes](https://v16.angular.io/guide/pipes)
