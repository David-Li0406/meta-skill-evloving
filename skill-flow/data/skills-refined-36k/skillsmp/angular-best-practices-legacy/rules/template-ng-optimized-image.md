---
title: Use NgOptimizedImage for Images (v15+)
impact: HIGH
impactDescription: LCP improvement, automatic lazy loading
tags: images, performance, lcp, lazy-loading
---

## Use NgOptimizedImage for Images (v15+)

NgOptimizedImage (available from Angular 15) enforces best practices: automatic lazy loading, priority hints, srcset generation, and preconnect warnings.

**Incorrect (Native img):**

```html
<img src="/assets/hero.jpg" alt="Hero image">
<img src="{{ user.avatar }}" alt="User avatar">
```

**Correct (NgOptimizedImage):**

```typescript
// app.module.ts
import { NgOptimizedImage } from '@angular/common';

@NgModule({
  imports: [NgOptimizedImage]
})
export class AppModule {}

// component.ts
@Component({
  template: `
    <!-- Priority image (LCP candidate) -->
    <img
      ngSrc="/assets/hero.jpg"
      alt="Hero image"
      width="1200"
      height="600"
      priority
    />

    <!-- Lazy loaded (below fold) -->
    <img
      [ngSrc]="user.avatar"
      alt="User avatar"
      width="64"
      height="64"
    />

    <!-- Fill mode -->
    <div class="image-container">
      <img
        ngSrc="/assets/product.jpg"
        alt="Product"
        fill
        sizes="(max-width: 768px) 100vw, 50vw"
      />
    </div>
  `,
  styles: [`
    .image-container {
      position: relative;
      width: 100%;
      aspect-ratio: 4/3;
    }
  `]
})
export class ProductComponent {}
```

**With image loader:**

```typescript
// app.module.ts
import { NgOptimizedImage, provideImgixLoader } from '@angular/common';

@NgModule({
  imports: [NgOptimizedImage],
  providers: [
    provideImgixLoader('https://my-site.imgix.net/')
  ]
})
export class AppModule {}
```

**For Angular 12-14 (without NgOptimizedImage):**

```typescript
// Manual optimization
@Component({
  template: `
    <!-- Manual lazy loading -->
    <img
      [src]="imageSrc"
      [alt]="imageAlt"
      loading="lazy"
      width="400"
      height="300"
    />

    <!-- Intersection Observer for more control -->
    <img
      #lazyImage
      [attr.data-src]="imageSrc"
      [alt]="imageAlt"
      width="400"
      height="300"
    />
  `
})
export class ImageComponent implements AfterViewInit {
  @ViewChild('lazyImage') lazyImage!: ElementRef;

  ngAfterViewInit() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target as HTMLImageElement;
          img.src = img.dataset['src']!;
          observer.unobserve(img);
        }
      });
    });
    observer.observe(this.lazyImage.nativeElement);
  }
}
```

Reference: [Angular Image Optimization](https://v16.angular.io/guide/image-directive)
