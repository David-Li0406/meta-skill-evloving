# Meta Templates

Templates for meta tags, OpenGraph, and Twitter cards.

## Essential Meta Tags

### Title Tag

**Format**: `{Page Title} | Lightfast`

**Requirements**:
- 50-60 characters total
- Primary keyword near start
- Brand at end

**Examples**:

```html
<title>Neural Memory: AI-Powered Team Knowledge | Lightfast</title>
<title>Semantic Search Setup Guide | Lightfast</title>
<title>Pricing - Simple, Transparent Plans | Lightfast</title>
```

### Meta Description

**Requirements**:
- 150-160 characters
- Include primary keyword
- Active voice
- End with benefit or CTA

**Templates**:

```html
<!-- Feature/Product -->
<meta name="description" content="Build organizational memory with semantic search. Connect your tools, search by meaning, trace every decision. Start free.">

<!-- Tutorial/Guide -->
<meta name="description" content="Set up the integration in under 5 minutes. Webhook-driven sync ensures instant updates within seconds of each change. Step-by-step guide inside.">

<!-- General Content -->
<meta name="description" content="Learn how semantic search finds content by meaning, not keywords. Discover the benefits of vector embeddings for knowledge retrieval.">
```

### Robots Meta

**Default** (allow indexing):
```html
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
```

**For AI-friendly content** (maximize snippet length):
```html
<meta name="robots" content="max-snippet:-1, max-image-preview:large, max-video-preview:-1">
```

**No index** (for internal/draft pages):
```html
<meta name="robots" content="noindex, nofollow">
```

## OpenGraph Tags

### Required Tags

```html
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Page description here...">
<meta property="og:type" content="website">
<meta property="og:url" content="https://lightfast.ai/page">
<meta property="og:image" content="https://lightfast.ai/og-image.jpg">
<meta property="og:site_name" content="Lightfast">
<meta property="og:locale" content="en_US">
```

### Article-Specific Tags

```html
<meta property="article:published_time" content="2025-01-15T00:00:00Z">
<meta property="article:modified_time" content="2025-01-20T00:00:00Z">
<meta property="article:author" content="https://twitter.com/lightfastai">
<meta property="article:section" content="Technology">
<meta property="article:tag" content="semantic search">
<meta property="article:tag" content="knowledge base">
```

### Image Requirements

**Dimensions**: 1200x630px (1.91:1 ratio)
**Format**: JPG or PNG
**File size**: Under 1MB

```html
<meta property="og:image" content="https://lightfast.ai/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Page title or description">
```

## Twitter Cards

### Summary Large Image (Default)

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@lightfastai">
<meta name="twitter:creator" content="@lightfastai">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Page description here...">
<meta name="twitter:image" content="https://lightfast.ai/og-image.jpg">
<meta name="twitter:image:alt" content="Page title or description">
```

### Summary Card (For short content)

```html
<meta name="twitter:card" content="summary">
<!-- Same other tags as above -->
```

## Next.js Implementation

### Using generateMetadata

```tsx
import type { Metadata } from "next";

export async function generateMetadata({ params }): Promise<Metadata> {
  const page = await getPage(params.slug);

  const title = `${page.title} | Lightfast`;
  const description = page.metaDescription || page.excerpt;
  const canonicalUrl = `https://lightfast.ai/${params.slug}`;
  const ogImage = page.ogImage || "https://lightfast.ai/og.jpg";

  return {
    title,
    description,
    alternates: {
      canonical: canonicalUrl,
    },
    openGraph: {
      title,
      description,
      type: "article",
      url: canonicalUrl,
      siteName: "Lightfast",
      publishedTime: page.publishedAt,
      modifiedTime: page.modifiedAt,
      images: [{
        url: ogImage,
        width: 1200,
        height: 630,
        alt: page.title,
      }],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [ogImage],
      creator: "@lightfastai",
    },
    robots: {
      index: true,
      follow: true,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  };
}
```

### Using createMetadata Utility

```tsx
import { createMetadata } from "@vendor/seo/metadata";

export const metadata = createMetadata({
  title: "Neural Memory",
  description: "Search your team's knowledge by meaning...",
  image: "https://lightfast.ai/og/neural-memory.jpg",
});
```

## Verification

Test meta tags with:
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)

## Checklist

- [ ] Title: 50-60 chars, keyword near start
- [ ] Description: 150-160 chars, includes keyword
- [ ] Canonical URL set
- [ ] OpenGraph complete (title, description, type, url, image)
- [ ] Twitter card configured
- [ ] Article dates included (for dated content)
- [ ] Image dimensions correct (1200x630)
