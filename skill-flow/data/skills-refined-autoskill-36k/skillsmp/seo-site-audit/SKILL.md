---
name: seo-site-audit
description: Website-level technical SEO audit with engineering backlog. Covers robots.txt, sitemap, canonical, redirects, meta/OG/Twitter, JSON-LD, internal linking, Core Web Vitals, mobile. Use for site-wide SEO improvements or technical SEO implementation.
allowed-tools: Read, Grep, Glob, WebFetch, Edit, Write
---

# SEO Site Audit

Transform website-level SEO into an engineering-executable task backlog.

## Outputs

1. **Executive Summary** — Top findings with P0/P1/P2 priorities
2. **Assumptions & Inputs** — What URLs/templates were analyzed
3. **Findings by Theme** — Organized P0→P1→P2 with example URLs
4. **Engineering Backlog** — Actionable task table (see templates/site-backlog-template.md)
5. **Implementation Notes** — Where fixes should land (layout, route, middleware, CMS, build)
6. **Validation & Rollout Plan** — Pre-launch checks and 7-day monitoring

## When to Use

- "Audit my website for SEO"
- "Technical SEO review"
- "Site-wide audit / improve indexing"
- Mentions: robots.txt, sitemap, canonical, redirects, 404s, soft 404s
- Mentions: meta tags, Open Graph, Twitter cards, JSON-LD structured data
- Mentions: internal linking, information architecture, hub-pillar, orphan pages
- Mentions: Core Web Vitals, performance, mobile, accessibility

## Not Applicable (Use seo-article-optimizer Instead)

- Single article or landing page content optimization (keywords, readability, meta/slug)

## Required Inputs

1. **Site type**: SaaS / Content site / E-commerce / Documentation / Other
2. **Tech stack**: Next.js / Nuxt / WordPress / Webflow / Static / Other
3. **Target language & region**: zh-CN/en/multilingual; hreflang needed?
4. **URL samples** (at least one of):
   - sitemap.xml
   - Route list / exported URL list
   - Key site pages (>= 10 URLs)
5. **Business goal**: Lead gen (signup/demo/trial) / E-commerce / Brand awareness; plus 1-3 most important conversion page URLs

> **If user cannot provide URL list or sitemap**: Only deliver "principle-based recommendations + required information checklist". Do NOT pretend to complete an audit.

## Priority Levels

- **P0 (Critical)**: Blocks indexing or causes major SEO damage
- **P1 (High)**: Significant impact on rankings or user experience
- **P2 (Medium)**: Optimization opportunities for improvement

## Common P0 Issues (Development Environment Leaks)

These often survive from dev/staging to production:

| Issue                            | Where to Check         |
| -------------------------------- | ---------------------- |
| `noindex, nofollow` meta tag     | `<head>` section       |
| robots.txt blocking all crawlers | `/robots.txt`          |
| Staging URLs in sitemap          | `sitemap.xml`          |
| Debug/preview modes enabled      | CMS settings, env vars |

## Quality Gates

- No vague advice (e.g., "improve meta") — must give specific fix + validation method
- No assumptions about sitemap/robots/schema existence without verification
- Must produce actionable backlog with priority ranking

## Workflow

For detailed audit methodology, see [workflow.md](workflow.md).

**Summary**:

1. Build Page Type Model (bucket by template/page type)
2. P0: Indexability & Canonicalization
3. P1: Site-level Meta & Share Assets (Meta/OG/Twitter)
4. P1: Structured Data (JSON-LD / schema.org)
5. P1: Information Architecture & Internal Linking
6. P2: Performance, Mobile, Accessibility

## Troubleshooting

| Issue                      | Solution                                         |
| -------------------------- | ------------------------------------------------ |
| Cannot access site         | Ask user to provide HTML source or exported data |
| No sitemap available       | Request URL list or route export                 |
| Missing required inputs    | List specific missing items before proceeding    |
| Site behind authentication | Ask for public pages or static exports           |

## Supporting Files

For detailed information, read these files when needed:

- **Detailed workflow steps**: [workflow.md](workflow.md)
- **Implementation snippets & reference**: [reference.md](reference.md)
- **Output templates**: See templates/
