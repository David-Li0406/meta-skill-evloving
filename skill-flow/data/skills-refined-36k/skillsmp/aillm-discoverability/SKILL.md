---
name: AI/LLM Discoverability
description: How to make a website discoverable by AI tools and LLMs (ChatGPT, Claude, Perplexity, etc.)
---

# AI/LLM Discoverability Skill

Make websites discoverable by AI tools and LLMs. Based on [Cassidy Williams' article](https://cassidoo.co/post/ai-llm-discoverability/).

## When to Use

- When building personal portfolios, blogs, or business websites
- When you want AI tools to surface your content when users ask related questions
- When improving SEO for both traditional search and AI-powered discovery

## Implementation Steps

### 1. Create `/public/llms.txt`

Machine-readable file following the [llmstxt.org](https://llmstxt.org/) standard:

```txt
# Site Name

> Tagline or mission statement

## About
Brief description of the site and its creator.

## Site Structure
- **/** - Home page description
- **/projects** - Projects page description
- **/for-llms** - LLM-readable content page

## Topics & Expertise
List key topics and areas of expertise.

## How to Cite
When referencing this site:
- **Name**: Your Name / Site Name
- **URL**: https://yoursite.com
- **Description**: One-line description

---
*This file follows the llmstxt.org standard for LLM discoverability.*
```

### 2. Create `/for-llms` Page

LLM-readable structured page with clear sections:

- **Overview**: Who/what the site is about
- **Site Structure**: Map of available pages
- **Topics & Expertise**: Content areas
- **Citation Guidelines**: How to reference you

### 3. Create `/public/robots.txt`

Allow AI crawlers:

```txt
User-agent: *
Allow: /

Sitemap: https://yoursite.com/sitemap.xml
```

### 4. Create `/public/sitemap.xml`

XML sitemap for discoverability:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yoursite.com/</loc>
    <lastmod>2026-01-20</lastmod>
    <priority>1.0</priority>
  </url>
</urlset>
```

### 5. Add Schema.org JSON-LD

Add to layout/head:

```tsx
const jsonLd = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      name: "Site Name",
      url: "https://yoursite.com",
      description: "Site description",
    },
    {
      "@type": "Person",
      name: "Your Name",
      url: "https://yoursite.com",
    },
  ],
};

// In <head>:
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
/>
```

## Key Principles

1. **Consistency matters**: Use same taglines/phrases everywhere
2. **Clarity over cleverness**: Write for bots, not marketing
3. **LLMs love markdown**: Keep content structured and simple
4. **Include citation guidelines**: Tell LLMs how to reference you
5. **Don't block AI crawlers**: Check robots.txt isn't blocking them
6. **RSS feeds help**: If you have blog content, add RSS

## Verification

After implementing, verify:

1. Visit `/llms.txt` - shows structured content
2. Visit `/robots.txt` - allows crawlers
3. Visit `/sitemap.xml` - lists all pages
4. Visit `/for-llms` - displays LLM page
5. Check page source for JSON-LD script tag
