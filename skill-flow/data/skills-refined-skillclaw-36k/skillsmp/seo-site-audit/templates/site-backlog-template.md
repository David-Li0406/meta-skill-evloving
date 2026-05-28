# Site SEO Backlog Template

## Backlog Table

| # | Priority | Issue | Affected Pages | Fix Description | Implementation Layer | Validation Method | Risk/Rollback |
|---|----------|-------|----------------|-----------------|---------------------|-------------------|---------------|
| 1 | P0 | {Issue title} | {Page type or URL pattern} | {Specific fix instructions} | {layout/route/middleware/CMS/build} | {How to verify fix} | {Risk level + rollback plan} |
| 2 | P0 | ... | ... | ... | ... | ... | ... |
| 3 | P1 | ... | ... | ... | ... | ... | ... |

## Priority Definitions

| Priority | Definition | SLA |
|----------|------------|-----|
| P0 | Blocks indexing or causes major SEO damage | Fix immediately |
| P1 | Significant impact on rankings or UX | Fix within 1-2 sprints |
| P2 | Optimization opportunity | Backlog for future sprints |

## Example Entries

| # | Priority | Issue | Affected Pages | Fix Description | Implementation Layer | Validation Method | Risk/Rollback |
|---|----------|-------|----------------|-----------------|---------------------|-------------------|---------------|
| 1 | P0 | robots.txt blocks /blog/ | All blog posts (~200 pages) | Remove `Disallow: /blog/` from robots.txt | Static file / build config | Fetch robots.txt, verify /blog/ not blocked | Low risk, revert file if needed |
| 2 | P0 | Missing canonical on paginated pages | /blog?page=2,3,4... | Add `<link rel="canonical">` pointing to page 1 or self-referencing | Layout component | Check page source for canonical tag | Low risk |
| 3 | P1 | Duplicate meta descriptions | Product category pages | Generate unique descriptions per category using template: "[Category] products - browse [count] items..." | CMS template | Crawl site, check for duplicate descriptions | Medium risk, test on staging |
| 4 | P1 | Missing OG images | 50% of blog posts | Add default OG image fallback + per-post featured image | Layout metadata | Facebook Sharing Debugger | Low risk |
| 5 | P2 | No FAQ schema on FAQ pages | /faq, /product/*/faq | Implement FAQPage JSON-LD schema | Page component | Rich Results Test | Low risk |

## Implementation Notes Template

### For Next.js App Router
- **Layout-level**: `app/layout.tsx` — site-wide meta, OG defaults, JSON-LD (Organization)
- **Route-level**: `app/blog/[slug]/page.tsx` — dynamic meta, article schema
- **Middleware**: `middleware.ts` — redirects, trailing slash normalization
- **Build config**: `next.config.js` — redirects, rewrites

### For WordPress
- **Theme-level**: `functions.php` or theme SEO hooks
- **Plugin-level**: Yoast/RankMath templates
- **Page-level**: Custom fields for per-page overrides

### For Static Sites
- **Build-time**: Generate sitemap.xml, robots.txt
- **Template-level**: Meta tag injection per page type
