# Next.js SEO Implementation Snippets

## App Router (Next.js 13+)

### Metadata API (layout.tsx / page.tsx)

```tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Page Title | Brand',
  description: 'Page description (150-160 chars)',
  openGraph: {
    title: 'Page Title',
    description: 'OG description',
    url: 'https://example.com/page',
    siteName: 'Site Name',
    images: [
      {
        url: 'https://example.com/og.jpg',
        width: 1200,
        height: 630,
        alt: 'OG Image Alt',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Page Title',
    description: 'Twitter description',
    images: ['https://example.com/og.jpg'],
  },
  alternates: {
    canonical: 'https://example.com/page',
  },
  robots: {
    index: true,
    follow: true,
  },
}
```

### Dynamic Metadata

```tsx
import type { Metadata, ResolvingMetadata } from 'next'

type Props = {
  params: { slug: string }
}

export async function generateMetadata(
  { params }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const post = await getPost(params.slug)

  return {
    title: `${post.title} | Brand`,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.featuredImage],
    },
    alternates: {
      canonical: `https://example.com/blog/${params.slug}`,
    },
  }
}
```

### JSON-LD Component

```tsx
// components/JsonLd.tsx
export function JsonLd({ data }: { data: Record<string, unknown> }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  )
}

// Usage in page.tsx
import { JsonLd } from '@/components/JsonLd'

export default function Page() {
  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: 'Article Title',
    // ... rest of schema
  }

  return (
    <>
      <JsonLd data={articleSchema} />
      {/* page content */}
    </>
  )
}
```

### Sitemap Generation

```tsx
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getAllPosts()

  const postUrls = posts.map((post) => ({
    url: `https://example.com/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.6,
  }))

  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: 'https://example.com/pricing',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    ...postUrls,
  ]
}
```

### robots.txt

```tsx
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/api/', '/admin/', '/search?'],
    },
    sitemap: 'https://example.com/sitemap.xml',
  }
}
```

## Pages Router (Legacy)

### next-seo package

```tsx
// pages/_app.tsx
import { DefaultSeo } from 'next-seo'

export default function App({ Component, pageProps }) {
  return (
    <>
      <DefaultSeo
        titleTemplate="%s | Brand"
        defaultTitle="Brand - Tagline"
        description="Default description"
        openGraph={{
          type: 'website',
          locale: 'en_US',
          url: 'https://example.com',
          siteName: 'Site Name',
        }}
        twitter={{
          handle: '@handle',
          site: '@site',
          cardType: 'summary_large_image',
        }}
      />
      <Component {...pageProps} />
    </>
  )
}
```

```tsx
// pages/blog/[slug].tsx
import { NextSeo, ArticleJsonLd } from 'next-seo'

export default function BlogPost({ post }) {
  return (
    <>
      <NextSeo
        title={post.title}
        description={post.excerpt}
        canonical={`https://example.com/blog/${post.slug}`}
        openGraph={{
          title: post.title,
          description: post.excerpt,
          url: `https://example.com/blog/${post.slug}`,
          type: 'article',
          article: {
            publishedTime: post.publishedAt,
            modifiedTime: post.updatedAt,
            authors: [post.author.url],
          },
          images: [
            {
              url: post.featuredImage,
              width: 1200,
              height: 630,
              alt: post.title,
            },
          ],
        }}
      />
      <ArticleJsonLd
        url={`https://example.com/blog/${post.slug}`}
        title={post.title}
        images={[post.featuredImage]}
        datePublished={post.publishedAt}
        dateModified={post.updatedAt}
        authorName={post.author.name}
        publisherName="Publisher Name"
        publisherLogo="https://example.com/logo.png"
        description={post.excerpt}
      />
      {/* page content */}
    </>
  )
}
```
