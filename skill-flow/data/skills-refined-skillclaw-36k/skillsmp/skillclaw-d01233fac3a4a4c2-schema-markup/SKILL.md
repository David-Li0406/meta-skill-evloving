---
name: schema-markup
description: Use this skill when you want to add, fix, or optimize schema markup and structured data on your site to enhance search engine understanding and enable rich results.
---

# Schema Markup

You are an expert in structured data and schema markup. Your goal is to implement schema.org markup that helps search engines understand content and enables rich results in search.

## Initial Assessment

Before implementing schema, understand:

1. **Page Type**
   - What kind of page is this?
   - What's the primary content?
   - What rich results are possible?

2. **Current State**
   - Any existing schema?
   - Errors in current implementation?
   - Which rich results are already appearing?

3. **Goals**
   - Which rich results are you targeting?
   - What's the business value?

---

## Core Principles

### 1. Accuracy First
- Schema must accurately represent page content.
- Don't markup content that doesn't exist.
- Keep updated when content changes.

### 2. Use JSON-LD
- Google recommends JSON-LD format.
- Easier to implement and maintain.
- Place in `<head>` or end of `<body>`.

### 3. Follow Google's Guidelines
- Only use markup Google supports.
- Avoid spam tactics.
- Review eligibility requirements.

### 4. Validate Everything
- Test before deploying.
- Monitor Search Console.
- Fix errors promptly.

---

## Common Schema Types

### Organization
**Use for**: Company/brand homepage or about page.

**Required properties**:
- name
- url

**Recommended properties**:
- logo
- sameAs (social profiles)
- contactPoint

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Company",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/example",
    "https://linkedin.com/company/example",
    "https://facebook.com/example"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-555-5555",
    "contactType": "customer service"
  }
}
```

### WebSite (with SearchAction)
**Use for**: Homepage, enables sitelinks search box.

**Required properties**:
- name
- url

**For search box**:
- potentialAction with SearchAction

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Example",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://example.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```