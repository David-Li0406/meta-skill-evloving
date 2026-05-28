---
id: seo-for-spas
name: "SEO for SPAs"
domain: DEV
skill: faion-software-developer
category: "development"
---

# SEO for SPAs

## Overview

Search Engine Optimization for Single Page Applications addresses the unique challenges of making JavaScript-heavy applications indexable by search engines. This includes server-side rendering, meta tag management, and structured data implementation.

## When to Use

- Building React, Vue, or Angular applications for public web
- Content-heavy sites requiring search visibility
- E-commerce applications
- Marketing and landing pages
- Blog platforms with SPA architecture

## Key Principles

- **Server-side render critical content**: First paint must include content
- **Dynamic meta tags**: Update per page for proper indexing
- **Structured data**: Help search engines understand content
- **Performance matters**: Core Web Vitals affect ranking
- **Crawlable links**: Use proper anchor tags with href

## Best Practices

### Server-Side Rendering Setup (Next.js)

```typescript
// pages/products/[slug].tsx
import { GetStaticProps, GetStaticPaths } from 'next';
import Head from 'next/head';

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  image: string;
  category: string;
}

interface Props {
  product: Product;
}

export default function ProductPage({ product }: Props) {
  const canonicalUrl = `https://example.com/products/${product.id}`;

  return (
    <>
      <Head>
        {/* Primary Meta Tags */}
        <title>{product.name} | Example Store</title>
        <meta name="description" content={product.description.slice(0, 160)} />
        <link rel="canonical" href={canonicalUrl} />

        {/* Open Graph */}
        <meta property="og:type" content="product" />
        <meta property="og:title" content={product.name} />
        <meta property="og:description" content={product.description} />
        <meta property="og:image" content={product.image} />
        <meta property="og:url" content={canonicalUrl} />
        <meta property="og:site_name" content="Example Store" />

        {/* Twitter Card */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={product.name} />
        <meta name="twitter:description" content={product.description} />
        <meta name="twitter:image" content={product.image} />

        {/* Product specific */}
        <meta property="product:price:amount" content={product.price.toString()} />
        <meta property="product:price:currency" content="USD" />
      </Head>

      <main>
        <h1>{product.name}</h1>
        {/* Product content */}
      </main>
    </>
  );
}

export const getStaticPaths: GetStaticPaths = async () => {
  const products = await fetchAllProducts();
  return {
    paths: products.map((p) => ({ params: { slug: p.slug } })),
    fallback: 'blocking', // Generate new pages on demand
  };
};

export const getStaticProps: GetStaticProps<Props> = async ({ params }) => {
  const product = await fetchProduct(params?.slug as string);

  if (!product) {
    return { notFound: true };
  }

  return {
    props: { product },
    revalidate: 3600, // ISR: regenerate every hour
  };
};
```

### Structured Data (JSON-LD)

```typescript
// components/StructuredData.tsx
import Head from 'next/head';

interface Props {
  data: object;
}

export function StructuredData({ data }: Props) {
  return (
    <Head>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
      />
    </Head>
  );
}

// Usage for Product
function ProductPage({ product }: { product: Product }) {
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.images,
    sku: product.sku,
    brand: {
      '@type': 'Brand',
      name: product.brand,
    },
    offers: {
      '@type': 'Offer',
      url: `https://example.com/products/${product.slug}`,
      priceCurrency: 'USD',
      price: product.price,
      availability: product.inStock
        ? 'https://schema.org/InStock'
        : 'https://schema.org/OutOfStock',
      seller: {
        '@type': 'Organization',
        name: 'Example Store',
      },
    },
    aggregateRating: product.rating ? {
      '@type': 'AggregateRating',
      ratingValue: product.rating.average,
      reviewCount: product.rating.count,
    } : undefined,
  };

  return (
    <>
      <StructuredData data={structuredData} />
      {/* Page content */}
    </>
  );
}

// Usage for Article/Blog Post
function BlogPost({ post }: { post: BlogPost }) {
  const structuredData = {
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
      url: post.author.profileUrl,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Example Blog',
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
    <>
      <StructuredData data={structuredData} />
      {/* Blog post content */}
    </>
  );
}

// Breadcrumb structured data
function Breadcrumbs({ items }: { items: BreadcrumbItem[] }) {
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  };

  return (
    <>
      <StructuredData data={structuredData} />
      <nav aria-label="Breadcrumb">
        <ol>
          {items.map((item, index) => (
            <li key={item.url}>
              {index < items.length - 1 ? (
                <a href={item.url}>{item.name}</a>
              ) : (
                <span aria-current="page">{item.name}</span>
              )}
            </li>
          ))}
        </ol>
      </nav>
    </>
  );
}
```

### Dynamic Meta Tags (React Helmet)

```typescript
// For non-Next.js React apps
import { Helmet } from 'react-helmet-async';

interface SEOProps {
  title: string;
  description: string;
  image?: string;
  url: string;
  type?: 'website' | 'article' | 'product';
  article?: {
    publishedTime: string;
    modifiedTime?: string;
    author: string;
    section?: string;
    tags?: string[];
  };
}

export function SEO({
  title,
  description,
  image,
  url,
  type = 'website',
  article,
}: SEOProps) {
  const siteName = 'Example Site';
  const defaultImage = 'https://example.com/og-default.png';
  const fullTitle = `${title} | ${siteName}`;

  return (
    <Helmet>
      {/* Primary */}
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      <link rel="canonical" href={url} />

      {/* Open Graph */}
      <meta property="og:type" content={type} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={image || defaultImage} />
      <meta property="og:url" content={url} />
      <meta property="og:site_name" content={siteName} />

      {/* Article specific */}
      {article && (
        <>
          <meta property="article:published_time" content={article.publishedTime} />
          {article.modifiedTime && (
            <meta property="article:modified_time" content={article.modifiedTime} />
          )}
          <meta property="article:author" content={article.author} />
          {article.section && (
            <meta property="article:section" content={article.section} />
          )}
          {article.tags?.map((tag) => (
            <meta property="article:tag" content={tag} key={tag} />
          ))}
        </>
      )}

      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={image || defaultImage} />
    </Helmet>
  );
}
```

### Sitemap Generation

```typescript
// scripts/generate-sitemap.ts
import { writeFileSync } from 'fs';
import { globby } from 'globby';

async function generateSitemap() {
  const baseUrl = 'https://example.com';

  // Get static pages
  const staticPages = await globby([
    'pages/**/*.tsx',
    '!pages/_*.tsx',
    '!pages/api/**',
    '!pages/**/[*.tsx',
  ]);

  // Get dynamic content
  const products = await fetchAllProducts();
  const posts = await fetchAllPosts();
  const categories = await fetchAllCategories();

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  ${staticPages
    .map((page) => {
      const path = page
        .replace('pages', '')
        .replace('.tsx', '')
        .replace('/index', '');
      return `
  <url>
    <loc>${baseUrl}${path}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>`;
    })
    .join('')}

  ${products
    .map((product) => `
  <url>
    <loc>${baseUrl}/products/${product.slug}</loc>
    <lastmod>${product.updatedAt}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
    <image:image>
      <image:loc>${product.image}</image:loc>
      <image:title>${product.name}</image:title>
    </image:image>
  </url>`)
    .join('')}

  ${posts
    .map((post) => `
  <url>
    <loc>${baseUrl}/blog/${post.slug}</loc>
    <lastmod>${post.updatedAt}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>`)
    .join('')}
</urlset>`;

  writeFileSync('public/sitemap.xml', sitemap);

  // Generate robots.txt
  const robots = `User-agent: *
Allow: /

Sitemap: ${baseUrl}/sitemap.xml

# Block admin pages
Disallow: /admin/
Disallow: /api/
`;

  writeFileSync('public/robots.txt', robots);

  console.log('Sitemap and robots.txt generated!');
}

generateSitemap();
```

### Proper Link Handling

```tsx
// WRONG: JavaScript navigation without href
<div onClick={() => router.push('/products')}>
  Products
</div>

// CORRECT: Anchor tag with href
import Link from 'next/link';

<Link href="/products">
  <a>Products</a>
</Link>

// Or with Next.js 13+
<Link href="/products">
  Products
</Link>

// For dynamic routes
<Link href={`/products/${product.slug}`}>
  {product.name}
</Link>

// For external links
<a
  href="https://external-site.com"
  rel="noopener noreferrer"
  target="_blank"
>
  External Link
</a>
```

### Performance Optimization

```typescript
// next.config.js
module.exports = {
  // Enable image optimization
  images: {
    domains: ['example.com', 'cdn.example.com'],
    formats: ['image/avif', 'image/webp'],
  },

  // Compress responses
  compress: true,

  // Generate production source maps for debugging
  productionBrowserSourceMaps: false,

  // Headers for caching
  async headers() {
    return [
      {
        source: '/:all*(svg|jpg|png|webp|avif)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/:all*(js|css)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
};

// Component-level optimization
import dynamic from 'next/dynamic';
import Image from 'next/image';

// Lazy load non-critical components
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />,
  ssr: false, // Don't SSR if not needed for SEO
});

// Optimized images
function ProductImage({ product }: { product: Product }) {
  return (
    <Image
      src={product.image}
      alt={product.name}
      width={400}
      height={400}
      priority={true} // For LCP images
      placeholder="blur"
      blurDataURL={product.blurDataUrl}
    />
  );
}
```

### Meta Tags for Social Sharing

```typescript
// components/SocialMeta.tsx
interface SocialMetaProps {
  title: string;
  description: string;
  image: string;
  url: string;
  twitterHandle?: string;
}

export function SocialMeta({
  title,
  description,
  image,
  url,
  twitterHandle = '@examplesite',
}: SocialMetaProps) {
  return (
    <Head>
      {/* Open Graph */}
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={image} />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      <meta property="og:url" content={url} />
      <meta property="og:type" content="website" />

      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:site" content={twitterHandle} />
      <meta name="twitter:creator" content={twitterHandle} />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={image} />
      <meta name="twitter:image:alt" content={title} />
    </Head>
  );
}

// OG Image generation API route
// pages/api/og.tsx (with @vercel/og)
import { ImageResponse } from '@vercel/og';

export const config = {
  runtime: 'edge',
};

export default function OGImage(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get('title') || 'Default Title';

  return new ImageResponse(
    (
      <div
        style={{
          height: '100%',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#fff',
        }}
      >
        <h1 style={{ fontSize: 60 }}>{title}</h1>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  );
}
```

## Anti-patterns

- **JavaScript-only navigation**: Links without href attributes
- **Missing meta tags**: No description or Open Graph tags
- **Blocking render**: Large JS bundles before content
- **Client-only content**: Critical content not in initial HTML
- **Duplicate content**: Same content on multiple URLs without canonical
- **Hidden content**: Text hidden with CSS that search engines may penalize

## References

- [Google Search Central](https://developers.google.com/search)
- [Next.js SEO Guide](https://nextjs.org/learn/seo/introduction-to-seo)
- [Schema.org](https://schema.org/)
- [Open Graph Protocol](https://ogp.me/)
- [Core Web Vitals](https://web.dev/vitals/)
