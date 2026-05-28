# SEO Site Audit

A Claude Code skill for website-level technical SEO audits with engineering-ready backlog.

## Features

- **Indexability & Canonicalization** — robots.txt, sitemap.xml, canonical tags, redirects, 404s
- **Development Environment Leak Detection** — noindex meta tags, robots blocking, staging URLs
- **Meta & Share Assets** — Title, description, Open Graph, Twitter cards
- **Structured Data** — JSON-LD schemas (Organization, Article, Product, LocalBusiness, Event, Review, etc.)
- **Information Architecture** — Internal linking, hub/pillar structure, orphan pages, breadcrumbs
- **Performance & Mobile** — Core Web Vitals, mobile optimization checklist, accessibility

## Usage

The skill activates when you mention:
- "Audit my website for SEO"
- "Technical SEO review"
- "Site-wide audit / improve indexing"
- robots.txt, sitemap, canonical, redirects, JSON-LD, Core Web Vitals

## Outputs

1. **Executive Summary** — Top findings with P0/P1/P2 priorities
2. **Assumptions & Inputs** — What was analyzed
3. **Findings by Theme** — Organized by priority
4. **Engineering Backlog** — Actionable task table
5. **Implementation Notes** — Where fixes should land
6. **Validation & Rollout Plan** — Pre/post-launch checks

## Files

```
seo-site-audit/
├── SKILL.md                              # Main skill definition
├── workflow.md                           # Detailed audit methodology
├── reference.md                          # Technical SEO reference
└── templates/
    ├── schema-snippets.md                # JSON-LD templates
    ├── nextjs-snippets.md                # Next.js implementation
    └── site-backlog-template.md          # Engineering backlog format
```

## Acknowledgments

This skill was inspired by and incorporates ideas from:
- [ramunasnognys/workflow-template/seo-specialist](https://github.com/ramunasnognys/workflow-template/tree/matt/improve-ui/.claude/skills/seo-specialist)
