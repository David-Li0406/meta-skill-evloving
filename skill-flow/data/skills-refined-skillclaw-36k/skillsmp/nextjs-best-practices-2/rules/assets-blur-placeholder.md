---
title: Add blurDataURL for Better LCP
impact: MEDIUM
impactDescription: Shows instant placeholder while image loads
tags: images, placeholder, blur, lcp
---

## Add blurDataURL for Better LCP

Blur placeholders show a low-resolution preview immediately while the full image loads. This improves perceived performance and prevents layout shift.

**Incorrect (no placeholder):**

```typescript
// ❌ Empty space while image loads
<Image
  src="/large-photo.jpg"
  alt="Photo"
  width={800}
  height={600}
/>

// User sees blank rectangle, then sudden image pop-in
```

**Correct (blur placeholder):**

```typescript
// Static import - blur generated automatically
import heroImage from '@/public/hero.jpg'

<Image
  src={heroImage}
  alt="Hero"
  placeholder="blur" // ✓ Automatic blur from static import
/>

// Remote image - provide blurDataURL
<Image
  src="https://cdn.example.com/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRg..."
/>
```

**Generate blur placeholder:**

```typescript
// lib/images.ts
import { getPlaiceholder } from 'plaiceholder'

export async function getImageWithBlur(src: string) {
  const buffer = await fetch(src).then(res => res.arrayBuffer())
  const { base64 } = await getPlaiceholder(Buffer.from(buffer))

  return {
    src,
    blurDataURL: base64,
  }
}

// Usage in page
export default async function GalleryPage() {
  const images = await Promise.all(
    imageUrls.map(url => getImageWithBlur(url))
  )

  return (
    <div>
      {images.map(img => (
        <Image
          key={img.src}
          src={img.src}
          alt="Gallery image"
          width={400}
          height={300}
          placeholder="blur"
          blurDataURL={img.blurDataURL}
        />
      ))}
    </div>
  )
}
```

**Simple color placeholder:**

```typescript
// Quick alternative - solid color
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  placeholder="blur"
  blurDataURL="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
/>

// Or use placeholder="empty" and style background
<div className="bg-gray-200">
  <Image
    src="/photo.jpg"
    alt="Photo"
    fill
    placeholder="empty"
  />
</div>
```

**Store blur in database:**

```typescript
// Store blurDataURL when image is uploaded
const image = await db.images.create({
  data: {
    url: uploadedUrl,
    blurDataURL: await generateBlur(uploadedUrl),
    width: metadata.width,
    height: metadata.height,
  }
})
```

Reference: [Image placeholder](https://nextjs.org/docs/app/api-reference/components/image#placeholder)
