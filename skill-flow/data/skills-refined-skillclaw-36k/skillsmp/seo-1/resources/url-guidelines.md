# URL Guidelines

Best practices for URL structure on Lightfast pages.

## Core Principles

1. **Descriptive**: URLs should describe the content
2. **Keyword-rich**: Include primary keyword
3. **Lowercase**: Always use lowercase
4. **Hyphenated**: Use hyphens, not underscores
5. **Concise**: Remove unnecessary words (the, a, and)
6. **Stable**: Avoid changing URLs after publication

## URL Structure

### General Pattern

```
/{section}/{keyword-slug}
/{section}/{category}/{keyword-slug}
```

### Good Examples

```
/features/neural-memory
/guides/semantic-search-implementation
/integrations/github
/pricing
/about
```

### Bad Examples

```
/page-123
/features/feature-1
/announcing-our-new-feature
/the-complete-guide-to-getting-started
```

## Keyword Optimization

### Primary Keyword Placement

1. **In URL**: Required for target pages
2. **Natural**: Should read like a phrase, not keyword stuffing

**Good**:
```
/guides/semantic-search-best-practices     # "semantic search" is keyword
/features/vector-search                     # "vector search" is keyword
```

**Bad**:
```
/guides/semantic-search-vector-search-code-retrieval   # Keyword stuffing
/guides/best-semantic-search-guide-2025-complete       # Too long
```

### Secondary Keywords

- Use in URL only if natural
- Prefer adding to meta description instead

## URL Length

**Optimal**: 50-60 characters (excluding domain)
**Maximum**: 100 characters

**Good** (48 chars):
```
/features/neural-memory-team-knowledge
```

**Too Long** (95 chars):
```
/features/complete-guide-to-neural-memory-and-team-knowledge-retrieval-for-enterprise
```

## Canonical URLs

### Always Set Canonical

```tsx
// In generateMetadata
return {
  alternates: {
    canonical: `https://lightfast.ai${pathname}`,
  },
};
```

### Handle Trailing Slashes

- Choose one format (with or without)
- Redirect the other to canonical
- Lightfast standard: **No trailing slash**

```
https://lightfast.ai/page      # Canonical
https://lightfast.ai/page/     # Redirect to above
```

### Handle WWW

- Redirect www to non-www
- Lightfast standard: **No www**

```
https://lightfast.ai/          # Canonical
https://www.lightfast.ai/      # Redirect to above
```

## URL Migration

### When Changing URLs

1. **Set up 301 redirect** from old to new URL
2. **Update internal links** to point to new URL
3. **Update external references** where possible
4. **Monitor 404s** for 30 days after migration

### Redirect Implementation

```tsx
// next.config.js
module.exports = {
  redirects: async () => [
    {
      source: '/old-url',
      destination: '/new-url',
      permanent: true,  // 301 redirect
    },
  ],
};
```

## Special Cases

### Pagination

```
/content                     # Page 1
/content/page/2              # Page 2+
```

### Filters/Categories

```
/content?category=topic      # Query param for filters
/content/topic               # Dedicated category page (if SEO-important)
```

### Anchors for Subsections

```
/guide#installation          # Anchor for subsection
/guide#configuration
/guide#troubleshooting
```

## Checklist

Before publishing a URL:

- [ ] Includes primary keyword
- [ ] Under 60 characters (ideal) / 100 characters (max)
- [ ] Lowercase with hyphens
- [ ] No unnecessary words (the, a, and, complete, guide)
- [ ] Canonical URL set
- [ ] No duplicate of existing URL
