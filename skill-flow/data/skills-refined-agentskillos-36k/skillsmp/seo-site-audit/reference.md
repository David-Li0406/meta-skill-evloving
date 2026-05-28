# SEO Site Audit — Reference Library

## 1) Essential Meta / Canonical (HTML)

```html
<title>Page Title | Brand</title>
<meta name="description" content="150–160 chars, intent + CTA." />
<link rel="canonical" href="https://example.com/page" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
```

## 2) Open Graph / Twitter (share assets)

OG image guideline: 1200x630 recommended; include width/height when possible.

```html
<meta property="og:type" content="website" />
<meta property="og:url" content="https://example.com/page" />
<meta property="og:title" content="Page Title" />
<meta property="og:description" content="..." />
<meta property="og:image" content="https://example.com/og.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Page Title" />
<meta name="twitter:description" content="..." />
<meta name="twitter:image" content="https://example.com/og.jpg" />
```

## 3) JSON-LD Snippets

See: templates/schema-snippets.md (Organization, Article, Breadcrumb, Product).

## 4) robots.txt / meta robots / sitemap.xml

### robots.txt example

```
User-agent: *
Disallow: /api/
Disallow: /admin/
Disallow: /search?
Allow: /

Sitemap: https://example.com/sitemap.xml
```

### meta robots

```html
<!-- Allow indexing (default) -->
<meta name="robots" content="index, follow" />

<!-- Block indexing -->
<meta name="robots" content="noindex, nofollow" />

<!-- Index but don't follow links -->
<meta name="robots" content="index, nofollow" />
```

### sitemap.xml structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

Priority guidelines:
- 1.0: Homepage
- 0.8: Core pages (pricing, features, about)
- 0.6: Blog posts, product pages
- 0.4: Archive pages, tags
- 0.2: Utility pages

## 5) CWV quick checklist

Thresholds reference:
- LCP (Largest Contentful Paint): < 2.5s
- FID (First Input Delay): < 100ms (or INP < 200ms)
- CLS (Cumulative Layout Shift): < 0.1

Common fixes:
- LCP: Optimize hero images, preload critical resources
- FID/INP: Reduce JS execution time, defer non-critical scripts
- CLS: Set explicit dimensions for images/embeds, avoid injecting content above existing content

## 6) Next.js implementation patterns

See templates/nextjs-snippets.md for:
- Head wrapper component
- Canonical URL generation
- OG image handling
- Structured data injection

## 7) Internationalization (hreflang)

```html
<html lang="en">
<head>
  <!-- Alternate language versions -->
  <link rel="alternate" hreflang="en" href="https://example.com/en/page" />
  <link rel="alternate" hreflang="zh" href="https://example.com/zh/page" />
  <link rel="alternate" hreflang="x-default" href="https://example.com/page" />
</head>
```

Guidelines:
- Use ISO 639-1 language codes (en, zh, es, etc.)
- Optional: Add region with ISO 3166-1 (en-US, zh-CN, etc.)
- Always include x-default for fallback
- Reciprocal: Each page must link to all language versions

## 8) Favicons & Web App Manifest

```html
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
<link rel="manifest" href="/site.webmanifest" />
<meta name="theme-color" content="#0066cc" />
```

**site.webmanifest:**
```json
{
  "name": "App Name",
  "short_name": "App",
  "icons": [
    { "src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#ffffff",
  "background_color": "#ffffff",
  "display": "standalone"
}
```

## 9) Preload & Preconnect

```html
<!-- Preload critical resources -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin />
<link rel="preload" href="/images/hero.jpg" as="image" />

<!-- Preconnect to external domains -->
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="dns-prefetch" href="https://analytics.example.com" />
```

## 10) Responsive Images

```html
<img
  src="image-800.jpg"
  srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 900px) 800px, 1200px"
  alt="Description"
  loading="lazy"
/>
```

## 11) Testing & Validation Tools

**Google Tools:**
- [Google Search Console](https://search.google.com/search-console)
- [Rich Results Test](https://search.google.com/test/rich-results)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)

**Social Media Validators:**
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)

**Schema Validation:**
- [Schema.org Validator](https://validator.schema.org/)
- [Google Rich Results Test](https://search.google.com/test/rich-results)

## 12) Common Pitfalls

| Issue | Fix |
|-------|-----|
| Duplicate content | Use canonical tags |
| Missing alt text | Add descriptive alt for all images |
| Keyword stuffing | Write naturally for humans |
| Slow page speed | Optimize images, use CDN |
| Not mobile-friendly | Test on real devices |
| Broken links | Check regularly with crawlers |
| Missing structured data | Implement JSON-LD |
| Poor URL structure | Use clean, descriptive URLs |
| No sitemap | Generate and submit to Search Console |
| Ignoring Core Web Vitals | Monitor and optimize continuously |
