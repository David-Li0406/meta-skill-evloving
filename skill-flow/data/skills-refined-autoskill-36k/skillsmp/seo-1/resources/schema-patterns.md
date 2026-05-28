# Schema Patterns

JSON-LD structured data templates for Lightfast pages.

## Schema Priority

1. **FAQPage** - Highest priority for AI citation
2. **HowTo** - Step-by-step instructions
3. **Article** - Content with dates and authors
4. **WebPage** - General pages, landing pages
5. **Product** - Features with pricing
6. **Organization** - Site-wide identity
7. **BreadcrumbList** - Navigation structure

## Base Patterns

### Organization Schema (Site-wide)

Include on all pages via layout:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Lightfast",
  "url": "https://lightfast.ai",
  "logo": {
    "@type": "ImageObject",
    "url": "https://lightfast.ai/android-chrome-512x512.png"
  },
  "sameAs": [
    "https://twitter.com/lightfastai",
    "https://github.com/lightfastai"
  ]
}
```

### BreadcrumbList Schema

For navigation clarity:

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://lightfast.ai"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Category",
      "item": "https://lightfast.ai/category"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Page Title"
    }
  ]
}
```

## Content Schemas

### Article Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "description": "Meta description here",
  "datePublished": "2025-01-15T00:00:00Z",
  "dateModified": "2025-01-20T00:00:00Z",
  "url": "https://lightfast.ai/article-slug",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://twitter.com/handle"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Lightfast",
    "logo": {
      "@type": "ImageObject",
      "url": "https://lightfast.ai/android-chrome-512x512.png"
    }
  },
  "image": {
    "@type": "ImageObject",
    "url": "https://lightfast.ai/og-image.jpg",
    "width": 1200,
    "height": 630
  }
}
```

### FAQPage Schema

**Critical for AEO** - Add to any page with Q&A content:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is Neural Memory?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Neural Memory is Lightfast's AI-powered knowledge retrieval system. It connects your tools and enables semantic search across all sources."
      }
    },
    {
      "@type": "Question",
      "name": "How do I set up integrations?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Navigate to Settings > Integrations, select your source, and follow the OAuth flow. Webhooks are configured automatically."
      }
    }
  ]
}
```

### HowTo Schema

For step-by-step guides:

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Set Up GitHub Integration",
  "description": "Step-by-step guide to connecting GitHub repositories to Lightfast",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Install the App",
      "text": "Navigate to Settings > Integrations and click 'Add GitHub'",
      "url": "https://lightfast.ai/guide#step-1"
    },
    {
      "@type": "HowToStep",
      "name": "Configure Settings",
      "text": "Select repositories and configure file patterns",
      "url": "https://lightfast.ai/guide#step-2"
    },
    {
      "@type": "HowToStep",
      "name": "Verify Setup",
      "text": "Test the integration to confirm sync is working",
      "url": "https://lightfast.ai/guide#step-3"
    }
  ],
  "totalTime": "PT5M"
}
```

### WebPage Schema

For general pages:

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Neural Memory - Search by Meaning",
  "description": "Build organizational memory that grows with your team",
  "url": "https://lightfast.ai/features/neural-memory",
  "primaryImageOfPage": {
    "@type": "ImageObject",
    "url": "https://lightfast.ai/og-image.jpg"
  },
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".hero-headline", ".hero-description"]
  }
}
```

### Product Schema

For features with pricing:

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Lightfast Pro",
  "description": "Advanced AI-powered code search and team memory",
  "brand": {
    "@type": "Brand",
    "name": "Lightfast"
  },
  "offers": {
    "@type": "AggregateOffer",
    "lowPrice": "0",
    "highPrice": "99",
    "priceCurrency": "USD",
    "offerCount": "3"
  }
}
```

### SoftwareApplication Schema

For the main product:

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Lightfast",
  "applicationCategory": "DeveloperApplication",
  "operatingSystem": "Web",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
```

## Page-Type Examples

### Documentation Pages

Docs pages should use HowTo (for guides) or WebPage (for reference) with FAQPage:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "TechArticle",
      "headline": "GitHub Integration Guide",
      "description": "Connect GitHub repositories to Lightfast",
      "datePublished": "2025-01-15T00:00:00Z",
      "dateModified": "2025-01-20T00:00:00Z"
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "How do I authenticate with GitHub?",
          "acceptedAnswer": { "@type": "Answer", "text": "..." }
        }
      ]
    }
  ]
}
```

### Landing Pages

Landing pages should use WebPage with Product (if pricing) or SoftwareApplication:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "name": "Neural Memory - AI-Powered Knowledge Search",
      "description": "Build organizational memory that grows with your team",
      "speakable": {
        "@type": "SpeakableSpecification",
        "cssSelector": [".hero-headline", ".hero-description"]
      }
    },
    {
      "@type": "SoftwareApplication",
      "name": "Lightfast",
      "applicationCategory": "DeveloperApplication",
      "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" }
    }
  ]
}
```

## Graph Pattern (Multiple Schemas)

Combine multiple schemas using @graph:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": "...",
      ...
    },
    {
      "@type": "FAQPage",
      "mainEntity": [...]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [...]
    }
  ]
}
```

## Implementation

### Using JsonLd Component

```tsx
import { JsonLd } from "@vendor/seo/json-ld";

export default function Page() {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "Article",
    // ...
  };

  return (
    <>
      <JsonLd code={structuredData} />
      {/* Page content */}
    </>
  );
}
```

### Inline Script Pattern

```tsx
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
/>
```

## Validation

Test schemas with:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)
