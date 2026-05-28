# Meta Tags Reference

## Essential Meta Tags

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Character encoding (must be first) -->
  <meta charset="UTF-8">

  <!-- Viewport for responsive design -->
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- Page title (50-60 characters) -->
  <title>Page Title | Site Name</title>

  <!-- Meta description (150-160 characters) -->
  <meta name="description" content="Compelling description of the page content that encourages clicks from search results.">

  <!-- Canonical URL -->
  <link rel="canonical" href="https://example.com/page">

  <!-- Robots directives -->
  <meta name="robots" content="index, follow">
</head>
```

## Open Graph (Facebook, LinkedIn)

```html
<!-- Basic Open Graph -->
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Page description for social sharing">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Site Name">
<meta property="og:locale" content="en_US">

<!-- Article-specific -->
<meta property="og:type" content="article">
<meta property="article:published_time" content="2024-01-15T10:00:00Z">
<meta property="article:modified_time" content="2024-01-20T14:30:00Z">
<meta property="article:author" content="https://example.com/authors/jane">
<meta property="article:section" content="Technology">
<meta property="article:tag" content="SEO">
<meta property="article:tag" content="Web Development">

<!-- Image specifications -->
<!-- Recommended: 1200x630px, aspect ratio 1.91:1 -->
<meta property="og:image" content="https://example.com/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Description of the image">
```

## Twitter Cards

```html
<!-- Summary card (small image) -->
<meta name="twitter:card" content="summary">
<meta name="twitter:site" content="@sitehandle">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Page description">
<meta name="twitter:image" content="https://example.com/image.jpg">

<!-- Summary with large image -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@sitehandle">
<meta name="twitter:creator" content="@authorhandle">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Page description">
<meta name="twitter:image" content="https://example.com/large-image.jpg">
<!-- Recommended: 1200x600px minimum -->
<meta name="twitter:image:alt" content="Image description">
```

## Robots Directives

```html
<!-- Default (index and follow) -->
<meta name="robots" content="index, follow">

<!-- Don't index this page -->
<meta name="robots" content="noindex">

<!-- Don't follow links on this page -->
<meta name="robots" content="nofollow">

<!-- Don't show in search results -->
<meta name="robots" content="noindex, nofollow">

<!-- Don't show cached version -->
<meta name="robots" content="noarchive">

<!-- Don't show snippet in results -->
<meta name="robots" content="nosnippet">

<!-- Control snippet length -->
<meta name="robots" content="max-snippet:150">

<!-- Control image preview size -->
<meta name="robots" content="max-image-preview:large">

<!-- Google-specific -->
<meta name="googlebot" content="noindex">
```

## Internationalization

```html
<!-- Page language -->
<html lang="en">

<!-- Alternative language versions -->
<link rel="alternate" hreflang="en" href="https://example.com/en/page">
<link rel="alternate" hreflang="es" href="https://example.com/es/page">
<link rel="alternate" hreflang="de" href="https://example.com/de/page">
<link rel="alternate" hreflang="x-default" href="https://example.com/page">
```

## Mobile & App

```html
<!-- Theme color (browser UI) -->
<meta name="theme-color" content="#0066cc">

<!-- iOS web app -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="App Name">
<link rel="apple-touch-icon" href="/icon-180.png">

<!-- Android web app -->
<link rel="manifest" href="/manifest.json">

<!-- Smart app banner (iOS) -->
<meta name="apple-itunes-app" content="app-id=123456789">

<!-- App links (Android) -->
<meta property="al:android:url" content="myapp://page">
<meta property="al:android:package" content="com.example.myapp">
<meta property="al:android:app_name" content="My App">
```

## Security & Performance

```html
<!-- Content Security Policy -->
<meta http-equiv="Content-Security-Policy" content="default-src 'self'">

<!-- Referrer policy -->
<meta name="referrer" content="strict-origin-when-cross-origin">

<!-- DNS prefetch for external resources -->
<link rel="dns-prefetch" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.googleapis.com">

<!-- Preload critical resources -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/css/critical.css" as="style">
```

## Verification & Ownership

```html
<!-- Google Search Console -->
<meta name="google-site-verification" content="verification-token">

<!-- Bing Webmaster Tools -->
<meta name="msvalidate.01" content="verification-token">

<!-- Pinterest -->
<meta name="p:domain_verify" content="verification-token">

<!-- Facebook domain verification -->
<meta name="facebook-domain-verification" content="verification-token">
```

## Complete Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- SEO -->
  <title>Complete Guide to Meta Tags | Example Site</title>
  <meta name="description" content="Learn how to optimize your web pages with meta tags for better SEO and social sharing. Includes examples for Open Graph, Twitter Cards, and more.">
  <link rel="canonical" href="https://example.com/meta-tags-guide">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="Complete Guide to Meta Tags">
  <meta property="og:description" content="Learn how to optimize your web pages with meta tags for better SEO and social sharing.">
  <meta property="og:url" content="https://example.com/meta-tags-guide">
  <meta property="og:image" content="https://example.com/images/meta-tags-og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:site_name" content="Example Site">
  <meta property="article:published_time" content="2024-01-15T10:00:00Z">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@examplesite">
  <meta name="twitter:title" content="Complete Guide to Meta Tags">
  <meta name="twitter:description" content="Learn how to optimize your web pages with meta tags.">
  <meta name="twitter:image" content="https://example.com/images/meta-tags-twitter.jpg">

  <!-- Mobile -->
  <meta name="theme-color" content="#0066cc">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.json">

  <!-- Performance -->
  <link rel="preconnect" href="https://fonts.googleapis.com">

  <!-- Favicon -->
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" href="/icon.svg" type="image/svg+xml">
</head>
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Missing description | Google generates one | Write unique descriptions |
| Duplicate titles | Confusing for users/SEO | Unique title per page |
| Long titles | Truncated in results | Keep under 60 chars |
| No og:image | Poor social previews | Add compelling image |
| Wrong canonical | Duplicate content | Point to preferred URL |
| noindex on important pages | Pages won't appear | Review robots meta |
