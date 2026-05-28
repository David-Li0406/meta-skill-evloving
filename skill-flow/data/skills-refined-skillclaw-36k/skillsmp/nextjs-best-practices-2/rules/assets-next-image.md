---
title: Use next/image for Automatic Optimization
impact: MEDIUM
impactDescription: Reduces image sizes by 30-50% and improves LCP
tags: images, optimization, performance, lcp
---

## Use next/image for Automatic Optimization

next/image automatically optimizes, resizes, and serves images in modern formats. Native img tags send unoptimized images.

**Incorrect (native img):**

```typescript
// ❌ No optimization, no lazy loading by default
<img src="/hero.jpg" alt="Hero" />

// ❌ Large image sent regardless of viewport
<img src="/photo.jpg" width="1920" height="1080" alt="Photo" />

// ❌ No responsive sizing
<img src="/product.jpg" className="w-full" alt="Product" />
```

**Correct (next/image):**

```typescript
import Image from 'next/image'

// Fixed size image
<Image
  src="/hero.jpg"
  alt="Hero"
  width={800}
  height={400}
  priority // Above-the-fold, preload
/>

// Responsive image
<Image
  src="/photo.jpg"
  alt="Photo"
  fill // Takes parent container size
  className="object-cover"
  sizes="(max-width: 768px) 100vw, 50vw" // Responsive hint
/>

// Product image with placeholder
<Image
  src="/product.jpg"
  alt="Product"
  width={400}
  height={400}
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,/9j..." // Low-res preview
/>
```

**Remote images:**

```typescript
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
      },
      {
        protocol: 'https',
        hostname: '*.cloudinary.com',
      },
    ],
  },
}

// Usage
<Image
  src="https://cdn.example.com/photo.jpg"
  alt="Remote"
  width={600}
  height={400}
/>
```

**Common patterns:**

```typescript
// Hero image (priority for LCP)
<Image src="/hero.webp" alt="Hero" fill priority sizes="100vw" />

// Grid of images
<div className="grid grid-cols-3">
  {products.map(p => (
    <Image
      key={p.id}
      src={p.image}
      alt={p.name}
      width={300}
      height={300}
      sizes="(max-width: 768px) 33vw, 300px"
    />
  ))}
</div>

// Avatar
<Image
  src={user.avatar}
  alt={user.name}
  width={40}
  height={40}
  className="rounded-full"
/>
```

Reference: [next/image](https://nextjs.org/docs/app/api-reference/components/image)
