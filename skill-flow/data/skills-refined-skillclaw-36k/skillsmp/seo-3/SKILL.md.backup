---
name: seo
description: Use when adding page metadata, implementing OpenGraph tags, creating JSON-LD structured data, generating sitemaps, optimizing LCP/INP/CLS, or configuring robots.txt. Use for Next.js Metadata API, Article/Product/FAQ schemas, or image optimization with next/image.
---

# SEO Optimization

## Overview

SEO requires three pillars: technical performance (Core Web Vitals), proper metadata, and structured data for rich snippets. All three matter for ranking.

## When to Use

- Creating any public-facing page
- Adding metadata to Next.js pages
- Implementing structured data (JSON-LD)
- Optimizing page load performance
- Debugging missing rich snippets in Google

## The Iron Rules

### 1. Core Web Vitals Are Ranking Factors

| Metric | Target | What It Measures | Key Optimization |
|--------|--------|------------------|------------------|
| **LCP** (Largest Contentful Paint) | < 2.5s | Main content load time | `priority` on hero images |
| **INP** (Interaction to Next Paint) | < 200ms | Responsiveness | scheduler.yield() for long tasks |
| **CLS** (Cumulative Layout Shift) | < 0.1 | Visual stability | Always set width/height |

#### LCP Optimization with Next.js Image

```typescript
// ❌ BAD: Unoptimized image kills LCP
<img src="/hero.jpg" alt="Hero" />

// ✅ GOOD: Next.js Image with priority for LCP
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={630}
  priority // Preloads, disables lazy loading
  placeholder="blur" // Shows blur during load
  blurDataURL="data:image/..." // Optional blur data
  sizes="(max-width: 768px) 100vw, 50vw"
/>

// ✅ GOOD: Static import auto-generates blur
import heroImage from './hero.jpg';

<Image
  src={heroImage}
  alt="Hero"
  priority
  placeholder="blur" // Blur data automatically provided
/>
```

#### INP Optimization (< 200ms)

INP has three phases to optimize:

**1. Input Delay** - Time until event handler starts
**2. Processing Time** - Event handler execution
**3. Presentation Delay** - Time to next frame

```typescript
// ❌ BAD: Long synchronous task blocks interactions
button.addEventListener('click', () => {
  // Heavy computation blocks UI for 500ms
  const result = expensiveCalculation();
  updateUI(result);
});

// ✅ GOOD: Break up with scheduler.yield()
button.addEventListener('click', async () => {
  const data = await fetchData();

  // Yield to allow interactions to process
  await scheduler.yield();

  processData(data);

  await scheduler.yield();

  updateUI();
});

// ✅ GOOD: Debounce rapid interactions
const debouncedSearch = debounce((query) => {
  performSearch(query);
}, 300);

input.addEventListener('input', (e) => {
  debouncedSearch(e.target.value);
});
```

**Key INP strategies:**
- Use `scheduler.yield()` in long tasks (> 50ms)
- Debounce rapid user inputs
- Lazy load below-fold interactivity
- Avoid large DOM updates on interaction

#### CLS Optimization

```typescript
// ❌ BAD: CLS - no dimensions on dynamic content
<div className="product-list">
  {products.map(p => <ProductCard key={p.id} product={p} />)}
</div>

// ✅ GOOD: Reserve space with aspect-ratio or fixed height
<div className="product-list min-h-[400px]">
  {products.map(p => <ProductCard key={p.id} product={p} />)}
</div>

// ✅ GOOD: Always set dimensions on images
<Image
  src="/product.jpg"
  alt="Product"
  width={400}  // Prevents CLS
  height={300}
/>
```

### 2. Use Next.js Metadata API Correctly

#### Root Layout: metadataBase + title.template

**Critical:** Set `metadataBase` in your root layout. Without it, relative OG image URLs break.

```typescript
// app/layout.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  metadataBase: new URL('https://site.com'), // REQUIRED for OG images
  title: {
    default: 'Brand Name',
    template: '%s | Brand Name', // Auto-appends to all pages
  },
  description: 'Default site description',
  openGraph: {
    siteName: 'Brand Name',
    locale: 'en_US',
    type: 'website',
  },
};
```

**Why metadataBase matters:**
- Without it: `images: ['/og.png']` → broken URL
- With it: `images: ['/og.png']` → `https://site.com/og.png`

#### Page-Level Metadata

```typescript
// app/products/[slug]/page.tsx
import { Metadata } from 'next';

export async function generateMetadata({ params }): Promise<Metadata> {
  const product = await getProduct(params.slug);

  return {
    title: product.name, // Becomes "Product Name | Brand Name" via template
    description: truncate(product.description, 155), // Max 155 chars

    alternates: {
      canonical: `/products/${product.slug}`, // Relative OK with metadataBase
    },

    // OpenGraph - use 'product' for e-commerce
    openGraph: {
      type: 'product', // NOT 'website' for products
      title: product.name,
      description: truncate(product.description, 155),
      images: [{
        url: product.image,
        width: 1200,
        height: 630,
        alt: product.name,
      }],
    },

    twitter: {
      card: 'summary_large_image',
      title: product.name,
      description: truncate(product.description, 155),
      images: [product.image],
    },

    robots: {
      index: true,
      follow: true,
    },
  };
}
```

### 3. Product Structured Data for Rich Snippets

Google shows price, availability, and reviews in search results. You MUST include:

```typescript
// Minimum required fields for Product rich snippet
const productJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Product',
  name: product.name,
  image: product.images,
  description: product.description,
  sku: product.sku,
  brand: {
    '@type': 'Brand',
    name: product.brand,
  },
  offers: {
    '@type': 'Offer',
    url: `https://site.com/products/${product.slug}`,
    price: product.price,
    priceCurrency: 'USD',
    availability: 'https://schema.org/InStock', // or OutOfStock
    priceValidUntil: '2025-12-31', // Required for validity
  },
  // Optional but highly recommended:
  aggregateRating: product.rating ? {
    '@type': 'AggregateRating',
    ratingValue: product.rating.value,
    reviewCount: product.rating.count,
  } : undefined,
};
```

### 4. JSON-LD Rendering Pattern

Use the Next.js recommended pattern for safe JSON-LD rendering:

```typescript
// NOTE: This pattern is safe because JSON.stringify escapes content
// and the replace() prevents script tag injection
function JsonLd({ data }: { data: object }) {
  const safeJson = JSON.stringify(data).replace(/</g, '\\u003c');
  return (
    <script
      type="application/ld+json"
      // eslint-disable-next-line react/no-danger
      dangerouslySetInnerHTML={{ __html: safeJson }}
    />
  );
}
```

### 5. Essential Structured Data Types

| Page Type | Required Schema | Rich Result |
|-----------|-----------------|-------------|
| Product | Product + Offer | Price, availability in search |
| Article | Article + Author | Article snippet |
| FAQ | FAQPage | Expandable Q&A in search |
| Recipe | Recipe | Recipe card with image |
| Local Business | LocalBusiness | Knowledge panel |
| Breadcrumbs | BreadcrumbList | Breadcrumb trail in results |

#### Article Schema

```typescript
const articleJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: post.title,
  image: post.coverImage,
  datePublished: post.publishedAt,
  dateModified: post.updatedAt,
  author: {
    '@type': 'Person',
    name: post.author.name,
    url: `https://site.com/authors/${post.author.slug}`,
  },
  publisher: {
    '@type': 'Organization',
    name: 'Brand Name',
    logo: {
      '@type': 'ImageObject',
      url: 'https://site.com/logo.png',
    },
  },
};
```

#### FAQPage Schema

```typescript
const faqJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: faqs.map((faq) => ({
    '@type': 'Question',
    name: faq.question,
    acceptedAnswer: {
      '@type': 'Answer',
      text: faq.answer,
    },
  })),
};
```

#### BreadcrumbList Schema

Shows breadcrumb trail in search results:

```typescript
const breadcrumbJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    {
      '@type': 'ListItem',
      position: 1,
      name: 'Home',
      item: 'https://site.com',
    },
    {
      '@type': 'ListItem',
      position: 2,
      name: 'Products',
      item: 'https://site.com/products',
    },
    {
      '@type': 'ListItem',
      position: 3,
      name: product.name,
      item: `https://site.com/products/${product.slug}`,
    },
  ],
};
```

### 6. Answer Engine Optimization (AEO)

AI search engines (ChatGPT, Perplexity, Claude) are becoming traffic sources. Optimize for them:

**Key AEO strategies:**

| Strategy | Implementation |
|----------|----------------|
| **FAQ sections** | Add FAQPage schema - AI pulls from structured Q&A |
| **Direct answers** | Start content with clear, factual statements |
| **Structured data** | Schema.org markup helps AI understand content |
| **Topic authority** | Comprehensive coverage on topic clusters |
| **Citation-friendly** | Include stats, dates, sources that AI can cite |

```typescript
// ✅ GOOD: Content structure for AI search
function ProductPage({ product }) {
  return (
    <>
      {/* Direct answer for AI to extract */}
      <p className="lead">
        The {product.name} is a {product.category} that {product.keyBenefit}.
        Priced at ${product.price}, it's ideal for {product.targetAudience}.
      </p>

      {/* FAQ section with schema */}
      <section>
        <h2>Frequently Asked Questions</h2>
        {product.faqs.map(faq => (
          <details key={faq.id}>
            <summary>{faq.question}</summary>
            <p>{faq.answer}</p>
          </details>
        ))}
      </section>

      {/* Structured data for both Google and AI */}
      <JsonLd data={productJsonLd} />
      <JsonLd data={faqJsonLd} />
    </>
  );
}
```

**Why AEO matters:**
- 40% of Gen Z uses TikTok/AI for search over Google
- AI search engines cite well-structured content
- FAQ sections appear in AI answers
- Structured data = machine-readable = AI-friendly

## Sitemap & Robots

### Dynamic Sitemap Generation

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const products = await db.product.findMany({
    select: { slug: true, updatedAt: true },
  });

  const productUrls = products.map((product) => ({
    url: `https://site.com/products/${product.slug}`,
    lastModified: product.updatedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  return [
    {
      url: 'https://site.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    ...productUrls,
  ];
}
```

### Robots.txt

```typescript
// app/robots.ts
import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin/', '/api/'],
      },
      {
        userAgent: 'Googlebot',
        allow: '/',
        crawlDelay: 0,
      },
    ],
    sitemap: 'https://site.com/sitemap.xml',
  };
}
```

## Quick Reference: Metadata Checklist

Every page needs:
- [ ] `title` - Unique, < 60 chars, includes primary keyword
- [ ] `description` - Compelling, < 155 chars, includes CTA
- [ ] `canonical` URL - Prevents duplicate content
- [ ] `openGraph` - For social sharing (1200x630 images)
- [ ] `twitter` card - For Twitter/X sharing
- [ ] `robots` - index/noindex directive

For e-commerce:
- [ ] OpenGraph `type: 'product'` (not 'website')
- [ ] Product JSON-LD with offers
- [ ] Breadcrumb JSON-LD

## Testing & Measurement

### Validation Tools (Before Deploy)

Test structured data BEFORE deploying:
- [Rich Results Test](https://search.google.com/test/rich-results) - Google's official tool
- [Schema Markup Validator](https://validator.schema.org/) - schema.org validator
- Chrome DevTools → Lighthouse → SEO audit

### Performance Measurement

| Tool | What It Measures | Use For |
|------|------------------|---------|
| **PageSpeed Insights** | Field data (28 days) | Official Core Web Vitals scores |
| **Chrome User Experience Report (CrUX)** | Real user data | P75 scores for ranking |
| **Lighthouse (DevTools)** | Lab data (simulated) | Local testing, not for ranking |
| **Search Console** | Core Web Vitals report | Per-URL performance in field |

**Critical:** Only **Field Data** (real users) affects Google rankings. Lab data helps debug but doesn't count for SEO.

### Core Web Vitals Testing Strategy

```typescript
// Measure INP in production
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.entryType === 'event') {
      const inp = entry.processingStart - entry.startTime;
      if (inp > 200) {
        console.warn('Slow INP:', {
          duration: inp,
          name: entry.name,
          target: entry.target,
        });
      }
    }
  }
}).observe({ type: 'event', buffered: true });

// Log slow LCP
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lcp = entries[entries.length - 1];
  if (lcp.renderTime > 2500) {
    console.warn('Slow LCP:', {
      duration: lcp.renderTime,
      element: lcp.element,
      url: lcp.url,
    });
  }
}).observe({ type: 'largest-contentful-paint', buffered: true });
```

## References

- [Core Web Vitals INP Guide](https://web.dev/articles/inp) - Official INP optimization patterns
- [Optimize INP](https://web.dev/articles/optimize-inp) - Three-phase optimization approach
- [Next.js Image Component](https://nextjs.org/docs/app/api-reference/components/image) - priority, placeholder, sizes
- [Next.js Metadata API](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) - generateMetadata, metadataBase
- [Schema.org](https://schema.org/) - Structured data vocabulary
- [Rich Results Test](https://search.google.com/test/rich-results) - Validate structured data

**Version Notes:**
- INP replaced FID as Core Web Vital (March 2024)
- Next.js 15: Enhanced Image component, metadataBase required for OG
- Good INP: < 200ms (improving from 500ms → 200ms = 22% engagement boost)
- AEO emerging: AI search engines (ChatGPT, Perplexity) use structured data

## Red Flags - STOP and Fix

| Thought | Reality |
|---------|---------|
| "SEO is just meta tags" | Core Web Vitals are ranking factors. Optimize performance. |
| "I'll add structured data later" | No rich snippets = lower CTR. Add from day one. |
| "LCP doesn't matter for this page" | Every page's performance affects site-wide ranking. |
| "Using img tag is fine" | Next.js Image handles optimization. Always use it. |
| "OpenGraph type='website' is fine" | Use 'product' for products, 'article' for articles. |
| "Lab data (Lighthouse) is good enough" | Only field data counts for ranking. Test with real users. |
| "INP is too complex to optimize" | Use scheduler.yield() and debouncing. Start simple. |
| "I don't need a sitemap for small sites" | Sitemaps help discovery. Generate dynamically. |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| HTML img instead of Next.js Image | Use `next/image` with priority for LCP |
| Missing `width`/`height` on images | Always specify to prevent CLS |
| Description > 160 chars | Truncate to 155 with ellipsis |
| No canonical URL | Add `alternates.canonical` |
| Missing `priceValidUntil` in Offer | Required for Product rich snippets |
| OpenGraph type='website' for products | Use type='product' |
| No structured data validation | Test with Rich Results Test before deploy |
| Long tasks without scheduler.yield() | Break up tasks > 50ms to improve INP |
| Testing only with Lighthouse | Use PageSpeed Insights for field data |
| No placeholder on LCP images | Add `placeholder="blur"` for perceived performance |
| Dynamic sitemap with hardcoded URLs | Fetch from database for automatic updates |