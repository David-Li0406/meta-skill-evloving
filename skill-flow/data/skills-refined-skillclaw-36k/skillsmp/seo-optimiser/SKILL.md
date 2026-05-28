---
name: seo-optimiser
description: Оптимізація мета-тегів, Open Graph та AI-readiness для пошукових систем та соцмереж.
version: 1.0.0
---

# 🎯 @SEO – Meta & Search Optimization Expert

Expert guidance for search engine optimization (SEO), social sharing (Open Graph), and AI-readiness (GEO/AEO).

## 🛠 Capabilities

- **Metadata Management**: Title tags (50-60 chars), meta descriptions (150-160 chars).
- **Social Graph Optimization**: Open Graph (og:) and Twitter Card properties.
- **Structured Data**: Schema.org (JSON-LD) implementation for Rich Results.
- **AI-Readiness (GEO)**: Information architecture for AI crawlers (ChatGPT, Perplexity, Gemini).
- **Technical SEO**: Robots.txt, sitemaps, canonical tags, and mobile-first validation.

## 📋 Best Practices

### 1. Essential Meta Tags

```html
<!-- Primary Meta Tags -->
<title>Title | Brand Name</title>
<meta name="title" content="Unique Title" />
<meta name="description" content="Compelling summary for search results." />
<link rel="canonical" href="https://example.com/" />
```

### 2. Open Graph / Facebook (OG)

```html
<meta property="og:type" content="website" />
<meta property="og:url" content="https://example.com/" />
<meta property="og:title" content="Social Media Title" />
<meta property="og:description" content="Social Media specific summary." />
<meta property="og:image" content="https://example.com/og-image.jpg" />
<meta
  property="og:image:alt"
  content="Description of the image for accessibility"
/>
```

### 3. Twitter Card

```html
<meta property="twitter:card" content="summary_large_image" />
<meta property="twitter:url" content="https://example.com/" />
<meta property="twitter:title" content="Twitter Specific Title" />
<meta property="twitter:description" content="Twitter Specific Summary." />
<meta property="twitter:image" content="https://example.com/og-image.jpg" />
```

### 4. JSON-LD (Structured Data)

```html
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Project Name",
    "url": "https://example.com/",
    "description": "Unique value proposition."
  }
</script>
```

## 🔍 Validation Checklist

- [ ] Unique title and meta description for every page.
- [ ] Canonical URL matches the actual page location.
- [ ] OG images are optimized (recommended 1200x630px).
- [ ] Heading hierarchy (`h1` -> `h2` -> `h3`) is semantic.
- [ ] Images have descriptive `alt` text.
- [ ] Fast performance (Core Web Vitals).
