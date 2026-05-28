---
name: seo-content-generation
description: "Use when optimizing for search engines, creating content, or implementing structured data. Covers meta tags, schema markup, and content structure."
---

# SEO & Content Generation

## Overview

SEO best practices and content optimization for web applications. Covers meta tags, structured data (schema.org), content structure, and technical SEO implementation.

## When to Use

- Setting up page metadata
- Implementing structured data
- Creating blog/article pages
- Optimizing content for search
- Generating sitemaps

## Quick Reference

| Element | Purpose | Location |
|---------|---------|----------|
| **Title** | Page title in search results | `<head>` |
| **Meta Description** | Search result snippet | `<head>` |
| **Open Graph** | Social sharing preview | `<head>` |
| **Schema.org** | Rich snippets | `<script type="application/ld+json">` |
| **Sitemap** | Page discovery | `/sitemap.xml` |

---

## Meta Tags

### Basic Meta Tags (Next.js)

```typescript
// app/layout.tsx or page.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    default: 'Site Name',
    template: '%s | Site Name', // For child pages
  },
  description: 'Clear description of your site (150-160 chars)',
  keywords: ['keyword1', 'keyword2', 'keyword3'],
  authors: [{ name: 'Author Name' }],
  creator: 'Creator Name',
  robots: {
    index: true,
    follow: true,
  },
};
```

### Dynamic Page Metadata

```typescript
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: 'article',
      publishedTime: post.publishedAt,
      authors: [post.author.name],
      images: [
        {
          url: post.coverImage,
          width: 1200,
          height: 630,
          alt: post.title,
        },
      ],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
  };
}
```

### Open Graph & Twitter Cards

```typescript
export const metadata: Metadata = {
  openGraph: {
    title: 'Page Title',
    description: 'Page description for social sharing',
    url: 'https://example.com/page',
    siteName: 'Site Name',
    images: [
      {
        url: 'https://example.com/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Image description',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Page Title',
    description: 'Page description',
    creator: '@twitterhandle',
    images: ['https://example.com/twitter-image.jpg'],
  },
};
```

---

## Schema Markup (Structured Data)

### Article Schema

```typescript
// components/ArticleSchema.tsx
export function ArticleSchema({ post }: { post: Post }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.excerpt,
    image: post.coverImage,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      '@type': 'Person',
      name: post.author.name,
      url: post.author.url,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Site Name',
      logo: {
        '@type': 'ImageObject',
        url: 'https://example.com/logo.png',
      },
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `https://example.com/blog/${post.slug}`,
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```

### Product Schema

```typescript
const productSchema = {
  '@context': 'https://schema.org',
  '@type': 'Product',
  name: product.name,
  description: product.description,
  image: product.images,
  brand: {
    '@type': 'Brand',
    name: 'Brand Name',
  },
  offers: {
    '@type': 'Offer',
    price: product.price,
    priceCurrency: 'USD',
    availability: 'https://schema.org/InStock',
    url: `https://example.com/products/${product.slug}`,
  },
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: product.rating,
    reviewCount: product.reviewCount,
  },
};
```

### FAQ Schema

```typescript
const faqSchema = {
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

### Organization Schema

```typescript
const orgSchema = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'Company Name',
  url: 'https://example.com',
  logo: 'https://example.com/logo.png',
  sameAs: [
    'https://twitter.com/handle',
    'https://linkedin.com/company/name',
    'https://github.com/org',
  ],
  contactPoint: {
    '@type': 'ContactPoint',
    email: 'support@example.com',
    contactType: 'customer service',
  },
};
```

---

## Content Structure

### Heading Hierarchy

```markdown
# H1 - One per page (main topic)
  ## H2 - Major sections
    ### H3 - Subsections
      #### H4 - Details (use sparingly)
```

### SEO-Friendly Content

```typescript
// Blog post structure
interface BlogPost {
  title: string;        // H1, include primary keyword
  excerpt: string;      // Meta description, 150-160 chars
  content: string;      // Body with H2s, H3s, internal links
  slug: string;         // URL-friendly, include keywords
  coverImage: string;   // Alt text with context
  publishedAt: Date;
  category: string;     // Helps with topical authority
  tags: string[];       // Related keywords
}
```

### URL Structure

```
Good:
/blog/seo-best-practices-2024
/products/running-shoes
/about

Bad:
/blog/post?id=123
/p/12345
/page-1
```

---

## Sitemap Generation

### Next.js Sitemap

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getAllPosts();
  const products = await getAllProducts();

  const blogUrls = posts.map((post) => ({
    url: `https://example.com/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }));

  const productUrls = products.map((product) => ({
    url: `https://example.com/products/${product.slug}`,
    lastModified: product.updatedAt,
    changeFrequency: 'daily' as const,
    priority: 0.8,
  }));

  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    ...blogUrls,
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
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/api/', '/admin/', '/private/'],
    },
    sitemap: 'https://example.com/sitemap.xml',
  };
}
```

---

## SEO Checklist

### Technical SEO
- [ ] HTTPS enabled
- [ ] Mobile-friendly (responsive)
- [ ] Fast loading (Core Web Vitals)
- [ ] Sitemap submitted to Search Console
- [ ] robots.txt configured
- [ ] Canonical URLs set

### On-Page SEO
- [ ] Unique title tags (50-60 chars)
- [ ] Meta descriptions (150-160 chars)
- [ ] One H1 per page
- [ ] Proper heading hierarchy
- [ ] Alt text on images
- [ ] Internal linking

### Structured Data
- [ ] Schema markup validated
- [ ] Organization schema on homepage
- [ ] Article schema on blog posts
- [ ] Product schema on product pages

---

## Red Flags - STOP

**Never:**
- Duplicate content without canonicals
- Keyword stuffing
- Hidden text/links
- Thin/low-quality content
- Broken internal links

**Always:**
- Write for users first, search engines second
- Use descriptive, unique titles
- Include relevant structured data
- Test with Google Rich Results Test
- Monitor Search Console for issues

---

## Integration

**Related skills:** frontend-design, nextjs-patterns
**Tools:** Google Search Console, Rich Results Test, PageSpeed Insights
