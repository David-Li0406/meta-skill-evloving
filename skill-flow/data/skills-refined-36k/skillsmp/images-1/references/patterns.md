# Images - Implementation Patterns

Implementation patterns for image optimization in web applications.

## Pattern: Use next/image

Use Next.js Image component for optimization.

✅ **Good:**
\`\`\`typescript
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority
/>
\`\`\`

❌ **Bad:**
\`\`\`typescript
<img src="/hero.jpg" alt="Hero" />
\`\`\`

**Why:** next/image:
- Automatic optimization
- Lazy loading
- Responsive images
- Modern formats (WebP)

## Pattern: Provide Alt Text

Always include alt text.

✅ **Good:**
\`\`\`typescript
<Image src="/product.jpg" alt="Red running shoes" />
\`\`\`

❌ **Bad:**
\`\`\`typescript
<Image src="/product.jpg" alt="" />
\`\`\`

**Why:** Alt text:
- Accessibility
- SEO
- Fallback for broken images

## Pattern: Use Responsive Images

Provide multiple sizes.

✅ **Good:**
\`\`\`typescript
<Image
  src="/hero.jpg"
  alt="Hero"
  sizes="(max-width: 768px) 100vw, 50vw"
  fill
/>
\`\`\`

**Why:** Responsive:
- Better performance
- Appropriate sizes
- Bandwidth savings

## Pattern: Lazy Load Images

Load images as needed.

✅ **Good:**
\`\`\`typescript
<Image
  src="/product.jpg"
  alt="Product"
  loading="lazy"
/>
\`\`\`

**Why:** Lazy loading:
- Faster initial load
- Save bandwidth
- Better performance

## Summary

**Key Patterns:**
- Use next/image
- Provide alt text
- Responsive images
- Lazy loading
- Optimize file size

**Anti-Patterns:**
- Plain img tags
- Missing alt text
- No optimization
- Loading all images upfront
