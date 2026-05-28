---
name: seo-llm
description: "SEO and LLM optimization review process. Use when optimizing web content for search engines, implementing Schema.org structured data, making content LLM-friendly, or improving meta tags and descriptions. Also use when pages lack meta descriptions, no structured data is present, headings don't form logical hierarchy, content is hard to extract programmatically, or important content is hidden in JavaScript. Essential for sitemap setup, robots.txt configuration, and content discoverability."
---

# SEO/LLM Skill

## Overview

Search engines and LLMs are your content's primary distributors. This skill guides systematic optimization of content for both traditional search and AI understanding.

**Core principle:** Write for humans first, structure for machines second. If content isn't useful to humans, no amount of optimization helps. But structure helps machines surface good content.

## The SEO/LLM Optimization Process

### Phase 1: Check Technical Foundation

**Technical SEO must work first:**

1. **Crawlability**
   - Can search engines access the content?
   - Is robots.txt configured correctly?
   - Are important pages in sitemap?

2. **Indexability**
   - Are pages being indexed?
   - Any noindex tags unintentionally?
   - Canonical URLs correct?

3. **Performance**
   - Core Web Vitals passing?
   - Mobile-friendly?
   - Fast enough for users?

### Phase 2: Check Content Structure

**Then verify content is understandable:**

1. **Semantic HTML**
   - One h1 per page?
   - Logical heading hierarchy?
   - Meaningful markup?

2. **Structured Data**
   - Schema.org for content type?
   - Valid JSON-LD?
   - Testing in Rich Results?

3. **Meta Content**
   - Unique, descriptive titles?
   - Compelling meta descriptions?
   - Open Graph for social?

### Phase 3: Check LLM Readability

**Finally, optimize for AI extraction:**

1. **Clear Structure**
   - Summary at the start?
   - One idea per paragraph?
   - Lists and tables for data?

2. **Explicit Definitions**
   - Terms defined on first use?
   - Context provided?
   - No assumed knowledge?

3. **Extractable Content**
   - Key facts easily identified?
   - FAQs in proper format?
   - No important content in images?

## Red Flags - STOP and Fix

### Technical SEO Red Flags

```html
<!-- ❌ CRITICAL: Blocking search engines -->
<meta name="robots" content="noindex">  <!-- Intentional? -->

<!-- ❌ CRITICAL: Missing canonical -->
<!-- No canonical = duplicate content -->

<!-- ❌ HIGH: No lang attribute -->
<html>  <!-- Should be <html lang="en"> -->

<!-- ❌ HIGH: Missing viewport -->
<!-- Not mobile-friendly -->

<!-- ❌ MEDIUM: HTTP not HTTPS -->
<!-- Modern SEO requires HTTPS -->
```

### Content Structure Red Flags

```html
<!-- ❌ HIGH: Multiple h1 tags -->
<h1>Main Title</h1>
...
<h1>Another Title</h1>  <!-- Should be h2 -->

<!-- ❌ HIGH: Skipped heading levels -->
<h1>Title</h1>
<h3>Subtitle</h3>  <!-- Skipped h2! -->

<!-- ❌ HIGH: Missing meta description -->
<!-- No description = Google writes one -->

<!-- ❌ MEDIUM: Generic title -->
<title>Home</title>  <!-- Should describe content -->
```

### LLM Readability Red Flags

```markdown
<!-- ❌ HIGH: Wall of text -->
[2000 words with no headings, lists, or structure]

<!-- ❌ HIGH: Content in images -->
<img src="pricing-table.png">  <!-- Text should be HTML -->

<!-- ❌ HIGH: No summary -->
[Long article with no intro or TL;DR]

<!-- ❌ MEDIUM: Undefined jargon -->
"Enable HMR for better DX"  <!-- Define acronyms! -->
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "SEO is manipulative" | Good SEO is good UX. Help users find content. |
| "Schema is too complex" | JSON-LD is simple. Use generators if needed. |
| "Meta descriptions are ignored" | They appear in search results. Write them. |
| "LLMs don't matter" | AI search is growing fast. Optimize now. |
| "Our content is niche" | Niche content needs SEO more, not less. |
| "We'll add structure later" | Structure aids writing. Do it first. |

## SEO/LLM Quality Checklist

Before publishing content:

**Technical:**
- [ ] HTTPS enabled
- [ ] Mobile-friendly (viewport, responsive)
- [ ] Core Web Vitals passing
- [ ] robots.txt allows crawling
- [ ] XML sitemap includes page
- [ ] Canonical URL set

**Content Structure:**
- [ ] Single h1 with primary keyword
- [ ] Logical heading hierarchy (h1→h2→h3)
- [ ] Meta title unique and descriptive (50-60 chars)
- [ ] Meta description compelling (150-160 chars)
- [ ] Open Graph tags for social sharing

**Structured Data:**
- [ ] Appropriate Schema.org type
- [ ] JSON-LD valid (test in Rich Results)
- [ ] Required properties present

**LLM Readability:**
- [ ] Summary/TL;DR at start
- [ ] Short paragraphs (3-4 sentences)
- [ ] Lists and tables for data
- [ ] Terms defined on first use

## Quick Patterns

### Essential Meta Tags

```html
<head>
  <!-- Primary -->
  <title>How to Write Accessible Forms | My Site</title>
  <meta name="description" content="Learn to build accessible forms with proper labels, error handling, and ARIA attributes. Step-by-step guide with code examples.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://example.com/accessible-forms">

  <!-- Open Graph -->
  <meta property="og:title" content="How to Write Accessible Forms">
  <meta property="og:description" content="Build forms that work for everyone.">
  <meta property="og:image" content="https://example.com/images/forms.jpg">
  <meta property="og:url" content="https://example.com/accessible-forms">
  <meta property="og:type" content="article">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="How to Write Accessible Forms">
  <meta name="twitter:description" content="Build forms that work for everyone.">
</head>
```

### Article Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Write Accessible Forms",
  "description": "Learn to build accessible forms with proper labels, error handling, and ARIA attributes.",
  "author": {
    "@type": "Person",
    "name": "Jane Developer"
  },
  "datePublished": "2024-01-15",
  "dateModified": "2024-01-20",
  "image": "https://example.com/images/forms.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "My Site",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
</script>
```

### LLM-Friendly Content Structure

```markdown
# Topic Title

**Summary:** One-paragraph overview answering the main question directly.

## What is [Topic]?

Clear definition in the first sentence. Then expand with context.

## Key Concepts

| Concept | Definition |
|---------|------------|
| Term 1 | Clear explanation |
| Term 2 | Clear explanation |

## How to [Action]

1. First step with explanation
2. Second step with explanation
3. Third step with explanation

## Common Questions

### Question 1?
Direct answer in the first sentence. Then elaborate.

### Question 2?
Direct answer in the first sentence. Then elaborate.
```

### FAQ Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is accessibility?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Accessibility means designing products that people with disabilities can use effectively."
      }
    },
    {
      "@type": "Question",
      "name": "Why does accessibility matter?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Accessibility is a legal requirement and improves usability for everyone."
      }
    }
  ]
}
</script>
```

## Quick Commands

```bash
# Validate structured data
npx structured-data-testing-tool <url>

# Check Core Web Vitals
npx lighthouse <url> --only-categories=performance

# Validate HTML
npx html-validate <file>

# Check links
npx linkinator <url>

# Test in Google's tools
# - Rich Results Test: https://search.google.com/test/rich-results
# - Mobile-Friendly: https://search.google.com/test/mobile-friendly
```

## References

Detailed patterns and examples in `references/`:
- `schema-types.md` - Common Schema.org patterns
- `meta-tags.md` - Complete meta tag reference
- `content-structure.md` - LLM-friendly writing patterns
