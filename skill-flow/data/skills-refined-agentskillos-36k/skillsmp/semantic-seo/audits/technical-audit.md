# Technical & Cost of Retrieval Audit

This audit focuses on minimizing the computational cost for search engines to crawl, render, index, and understand your content. Lower Cost of Retrieval (CoR) leads to better crawl efficiency and indexation.

## Table of Contents

1. [Cost of Retrieval Fundamentals](#cost-of-retrieval-fundamentals)
2. [Crawl Efficiency Audit](#crawl-efficiency-audit)
3. [Core Web Vitals](#core-web-vitals)
4. [HTML & DOM Optimization](#html--dom-optimization)
5. [Server Configuration](#server-configuration)
6. [URL & Architecture](#url--architecture)

---

## Cost of Retrieval Fundamentals

### What Increases CoR

| Factor | Impact | Priority |
|--------|--------|----------|
| Large DOM size | High parsing cost | Critical |
| Slow response time | Crawler waits | Critical |
| Complex JavaScript | Rendering required | High |
| Many HTTP requests | Resource fetching | High |
| Duplicate content | Wasted crawl budget | High |
| Error pages | Failed attempts | Medium |
| Low text-to-code ratio | Content extraction harder | Medium |

### CoR Optimization Goals

| Metric | Target | Why |
|--------|--------|-----|
| Server response | <100ms | Fast initial connection |
| DOM nodes | <1500 | Minimal parsing time |
| HTML size | <100KB | Quick download |
| Text-to-code ratio | >50% | Easy content extraction |
| HTTP requests | <50 per page | Reduced resource fetching |

---

## Crawl Efficiency Audit

### Log File Analysis

| Metric | Target | Check |
|--------|--------|-------|
| HTML hit ratio | >80% | Most hits on content, not assets |
| Bot response time | <100ms | Fast responses to Googlebot |
| Error rate | 0% | No 4xx/5xx errors |
| Crawl depth | <4 clicks | Important content reachable |

### Crawl Budget Optimization

| Issue | Check | Fix |
|-------|-------|-----|
| **Filter URL explosion** | Millions of parameter URLs | Limit faceted navigation |
| **Stale 404s** | Deleted pages returning 404 | Use 410 for permanent removal |
| **Duplicate crawling** | Same content, different URLs | Implement canonical tags |
| **Low-value pages** | Thin content being crawled | Noindex or consolidate |

### Status Code Audit

| Code | Meaning | Action |
|------|---------|--------|
| **200** | Success | Ensure content quality |
| **301** | Permanent redirect | Minimize redirect chains |
| **302** | Temporary redirect | Use 301 for permanent moves |
| **404** | Not found | Fix or 410 if intentional |
| **410** | Gone | Use for permanently removed |
| **500** | Server error | Fix immediately |
| **503** | Unavailable | Temporary, monitor |

### Redirect Chain Audit

```
Goal: Maximum 1 redirect (A -> B)
Avoid: A -> B -> C -> D (chain)

Check:
[ ] No chains longer than 1 redirect
[ ] No redirect loops
[ ] All redirects use 301 (not 302)
[ ] Internal links updated to final URLs
```

---

## Core Web Vitals

### LCP (Largest Contentful Paint)

| Target | Status |
|--------|--------|
| <2.5s | Good |
| 2.5-4s | Needs improvement |
| >4s | Poor |

**Optimization Checklist**:
```
[ ] Optimize hero images (WebP/AVIF)
[ ] Preload critical resources
[ ] Reduce server response time
[ ] Remove render-blocking JS/CSS
[ ] Use CDN for assets
```

### FID/INP (Interaction Delay)

| Target | Status |
|--------|--------|
| <100ms | Good |
| 100-300ms | Needs improvement |
| >300ms | Poor |

**Optimization Checklist**:
```
[ ] Break up long JavaScript tasks
[ ] Use web workers for heavy processing
[ ] Defer non-critical JS
[ ] Minimize main thread work
```

### CLS (Cumulative Layout Shift)

| Target | Status |
|--------|--------|
| <0.1 | Good |
| 0.1-0.25 | Needs improvement |
| >0.25 | Poor |

**Optimization Checklist**:
```
[ ] Set explicit dimensions for images
[ ] Set dimensions for video/iframe
[ ] Reserve space for ads
[ ] Avoid inserting content above existing
[ ] Use transform animations (not layout)
```

---

## HTML & DOM Optimization

### DOM Size Audit

| Metric | Target | Check |
|--------|--------|-------|
| Total nodes | <1500 | Count all DOM elements |
| Maximum depth | <32 levels | No deeply nested divs |
| Maximum children | <60 per node | Avoid flat structures too |

### Code Cleanup

| Issue | Check | Fix |
|-------|-------|-----|
| Unused CSS | >50% unused | Tree shaking, purge unused |
| Unused JS | Dead code present | Remove or lazy load |
| Comments in production | HTML comments exist | Remove for production |
| Inline styles | Repeated inline styles | Consolidate to CSS |
| Empty elements | `<div></div>` present | Remove |

### Semantic HTML Audit

| Element | Purpose | Check |
|---------|---------|-------|
| `<article>` | Self-contained content | Main content wrapped |
| `<section>` | Thematic grouping | Logical sections defined |
| `<aside>` | Tangential content | Sidebars properly marked |
| `<nav>` | Navigation | Menus properly marked |
| `<header>` | Introductory content | Page/section headers |
| `<footer>` | Footer content | Page/section footers |
| `<main>` | Main content | One per page |

### Text-to-Code Ratio

**Calculate**:
```
Ratio = (Text content bytes) / (Total HTML bytes) x 100

Target: >50%
```

**Improvement strategies**:
- Remove inline JavaScript
- Externalize CSS
- Minify HTML
- Remove HTML comments
- Consolidate CSS classes

---

## Server Configuration

### Response Time Optimization

| Component | Target | Check |
|-----------|--------|-------|
| TTFB | <100ms | Time to first byte |
| DNS lookup | <50ms | DNS resolution time |
| SSL handshake | <100ms | TLS connection time |
| Server processing | <50ms | Backend response |

### Caching Configuration

| Resource Type | Cache Duration | Header |
|---------------|----------------|--------|
| HTML (dynamic) | No cache or short | `max-age=0` |
| CSS/JS (versioned) | 1 year | `max-age=31536000` |
| Images (static) | 1 year | `max-age=31536000` |
| Fonts | 1 year | `max-age=31536000` |

### HTTP Headers Audit

| Header | Purpose | Check |
|--------|---------|-------|
| `Link: rel="canonical"` | Canonical for non-HTML | PDFs, images |
| `Vary: User-Agent` | Dynamic serving | If serving different content |
| `Last-Modified` | Content freshness | Matches schema dateModified |
| `HSTS` | Force HTTPS | Reduces redirect hops |
| `X-Robots-Tag` | Indexing control | Correct directives |

### Compression Audit

| Method | Check |
|--------|-------|
| Gzip | Enabled for text resources |
| Brotli | Enabled (better than gzip) |
| Image optimization | WebP/AVIF used |

---

## URL & Architecture

### URL Structure Audit

| Criterion | Requirement | Check |
|-----------|-------------|-------|
| Length | Short, meaningful | <75 characters |
| Hierarchy | Reflects content structure | /category/subcategory/page |
| Keywords | Contains target terms | Not stuffed |
| Consistency | Uniform format | Lowercase, hyphens |
| Trailing slashes | Consistent usage | All with or all without |
| Parameters | Minimal | Avoid unnecessary params |

### URL Cleanup Checklist

```
[ ] No uppercase letters (or redirects handle)
[ ] No special characters (except hyphens)
[ ] No redundant words (/germany/germany-visa/ -> /germany/visa/)
[ ] No session IDs in URLs
[ ] No unnecessary parameters
[ ] Consistent trailing slash policy
```

### Canonicalization Audit

| Issue | Check | Fix |
|-------|-------|-----|
| Missing canonical | Pages without canonical tag | Add self-referencing |
| Wrong canonical | Points to wrong page | Correct the target |
| Conflicting signals | Canonical vs noindex | Align directives |
| Chain canonicals | A -> B -> C | Point directly to C |
| Cross-domain | External canonical | Verify intention |

### XML Sitemap Audit

| Check | Requirement |
|-------|-------------|
| Contains only indexable | No noindex, 404, blocked pages |
| Updated regularly | Reflects current content |
| Under 50MB/50k URLs | Per sitemap file |
| Indexed sitemaps | Submitted to Search Console |
| Accurate lastmod | Matches actual modification |

---

## Technical Audit Scorecard

| Category | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Crawl Efficiency | 25% | /10 | |
| Core Web Vitals | 25% | /10 | |
| HTML/DOM | 20% | /10 | |
| Server Config | 15% | /10 | |
| URL Structure | 15% | /10 | |
| **Total** | 100% | | **/10** |

### Scoring Guide

| Score | Interpretation |
|-------|----------------|
| 9-10 | Excellent technical foundation |
| 7-8 | Good, minor improvements possible |
| 5-6 | Needs attention |
| <5 | Critical issues requiring immediate fix |

### Priority Matrix

| Priority | Issues |
|----------|--------|
| **P0 - Critical** | 5xx errors, major CWV fails, broken canonicals |
| **P1 - High** | Slow response, large DOM, redirect chains |
| **P2 - Medium** | Missing headers, suboptimal caching |
| **P3 - Low** | Minor optimizations, cleanup |
