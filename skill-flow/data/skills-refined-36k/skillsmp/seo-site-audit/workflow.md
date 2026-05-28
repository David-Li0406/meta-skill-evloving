# SEO Site Audit — Workflow

Execute these audit steps in order.

## Step A: Build Page Type Model

First, bucket the site by template/page type. Example:

- Homepage / Pricing / Product or Feature pages / Category pages / Blog list / Article pages / Login/Dashboard / Search results

For each bucket, sample 2-5 representative URLs to avoid fragmented per-page conclusions.

## Step B: P0 — Indexability & Canonicalization

Must explicitly output "pass/risk/recommendation" for each:

### 1. robots.txt & meta robots

- Verify core pages aren't accidentally blocked
- Confirm sitemap location is declared
- **Check for dev environment leaks**: Look for `Disallow: /` that shouldn't be in production

### 2. sitemap.xml

- Should only contain indexable URLs
- Exclude noindex/redirected/404 pages
- Check lastmod is reasonable
- **Check for staging URLs**: Ensure no dev/staging domain URLs leaked into production sitemap
- Priority guidelines:
  - 1.0: Homepage
  - 0.8: Core pages (pricing, features, about)
  - 0.6: Blog posts, product pages
  - 0.4: Archive pages, tags
  - 0.2: Utility pages

### 3. Canonical tags

- Duplicate content handling: parameters, pagination, sorting, UTM
- Use prev/next where necessary

### 4. Redirects & URL normalization

- HTTP → HTTPS
- www ↔ non-www
- Trailing slash consistency
- Post-migration 301 chains (avoid 302/multi-hop)

### 5. 404 / Soft 404

- Error pages return correct status codes
- Check for thin/auto-generated pages being indexed

### 6. Site search & filter pages

- Should these be noindex?
- Infinite URL combinations from filters?

### Development Environment Leak Detection (Critical P0)

These issues commonly survive from dev/staging to production:

| Issue                         | Detection Method                        | Fix                                    |
| ----------------------------- | --------------------------------------- | -------------------------------------- |
| `noindex, nofollow` in meta   | Check `<head>` for robots meta tag      | Remove or make environment-conditional |
| robots.txt blocking all       | Check `/robots.txt` for `Disallow: /`   | Update for production                  |
| Staging domain in sitemap     | Grep sitemap for non-production domains | Regenerate sitemap                     |
| Debug mode enabled            | Check for debug headers/console logs    | Disable in production config           |
| Preview/draft content indexed | Check for preview URLs in search        | Add noindex to preview routes          |

**Environment-Aware Fix Example (Next.js):**

```jsx
<meta
  name="robots"
  content={
    process.env.NODE_ENV === "production"
      ? "index, follow"
      : "noindex, nofollow"
  }
/>
```

**P0 Output**: Must list "indexing blockers" with URL types and fix order.

## Step C: P1 — Site-level Meta & Share Assets

### Meta tags

- **Title**: 50-60 characters (common practice), include primary keyword + brand, unique per page
- **Meta description**: 150-160 characters, compelling, include intent + CTA

### Open Graph

- og:type, og:url, og:title, og:description, og:image
- Image: 1200×630 recommended; include width/height

### Twitter cards

- summary_large_image or appropriate type
- Consistent with OG tags

**Requirement**: Don't just give principles — specify WHERE to implement (e.g., Next.js Layout/Head component, WordPress SEO plugin template, SSR framework head injection point).

## Step D: P1 — Structured Data (JSON-LD / schema.org)

Cover these schemas:

- **Organization / WebSite** (site-level)
- **BreadcrumbList** (navigation hierarchy)
- **Article** (content sites)
- **Product/Offer** (e-commerce)
- **LocalBusiness** (local businesses with physical locations)
- **Event** (events, conferences, webinars)
- **Review/AggregateRating** (review pages)

Provide examples and field notes (dates, author, publisher, logo, sameAs).

> Reference code snippets from `templates/schema-snippets.md` — don't paste full templates into main output.

## Step E: P1 — Information Architecture & Internal Linking

Output must be actionable:

### Three-click reach

- Can key conversion pages be reached within 3 clicks?

### Hub/Pillar structure (Topic Clusters)

- Are there topic aggregation pages?
- Identify orphan pages (no internal links pointing to them)
- Map pillar pages to cluster content
- Recommend cluster groupings based on semantic similarity

### Breadcrumbs

- Match hierarchy
- Consistent with Breadcrumb schema

### Anchor text

- Semantically consistent
- Avoid meaningless anchors ("click here", "read more")
- Ensure anchor text diversity (don't over-optimize with exact match)

### Template-based recommendations

- Article/product pages: "Related posts" / "Related features" sections
- Systematic weighting through templates

### Internal Linking Strategy

| Principle            | Check                                         | Fix                                      |
| -------------------- | --------------------------------------------- | ---------------------------------------- |
| Anchor diversity     | No over-optimized exact-match anchors         | Vary anchor text naturally               |
| Link flow            | High-authority pages link to conversion pages | Add strategic links from popular content |
| Contextual relevance | Links match surrounding content               | Remove or relocate irrelevant links      |
| Link depth           | Key pages within 3 clicks                     | Add navigation shortcuts                 |
| Footer/sidebar links | Used sparingly                                | Prioritize in-content contextual links   |

## Step F: P2 — Performance, Mobile, Accessibility

### Core Web Vitals

- LCP < 2.5s
- FID < 100ms (or INP < 200ms)
- CLS < 0.1

### Images

- Lazy loading
- Responsive srcset/sizes

### Critical resources

- Preload/preconnect (see reference.md for examples)

### Semantic HTML & Accessibility

- Single H1 per page
- Heading hierarchy (no skipped levels)
- Alt text rules
- ARIA where appropriate

## Output Format (Strict)

Output in 6 parts, fixed order:

### 1. Executive Summary (5-12 items)

- Conclusion first, then reasoning
- Each item tagged with priority (P0/P1/P2)

### 2. Assumptions & Inputs

- List which URLs/page types informed your analysis
- List missing information and associated risks

### 3. Findings by Theme (P0→P1→P2)

- At least 2 example URLs/templates per theme

### 4. Backlog (Engineering-Executable Table)

- Use `templates/site-backlog-template.md` format

### 5. Implementation Notes

- Reference `templates/nextjs-snippets.md` or `reference.md`
- Specify implementation layer (layout, route, middleware, CMS template, build process)

### 6. Validation & Rollout Plan

- **Pre-launch**: Crawl verification, status codes, structured data validation
- **Post-launch 7-day watch**: Index status, crawl stats, 404s, redirect chains
