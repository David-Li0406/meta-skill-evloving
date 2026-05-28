---
name: seo-article-optimizer
description: Optimize single articles or landing pages for SEO. Analyzes keywords, readability, headings, meta tags, internal links, E-E-A-T signals, featured snippets. Outputs scores, optimized draft, and publish assets. Use for blog posts, landing pages, or single URL optimization.
allowed-tools: Read, Grep, Glob, WebFetch, Edit, Write
---

# SEO Article Optimizer

Optimize a single article or landing page to be publish-ready and trackable.

## Outputs

1. **Structured Report** — Scores, priorities, quick wins
2. **Optimized Draft** — Markdown, preserving original voice
3. **Publishing Assets** — Meta title/description, slug, alt text, internal links, snippet blocks
4. **Implementation Checklist** — Ready for editors or engineering

## When to Use

- "Help me optimize this article for SEO"
- "Generate meta tags for this page"
- "Improve readability and structure"
- "Target featured snippets"
- Input: Full article text, Markdown, or single page URL

## Not Applicable (Use seo-site-audit Instead)

- Multi-page or site-wide: robots.txt, sitemap, canonical, site architecture, performance systems

## Required Inputs

1. **Content**: Full text or URL
2. **Search Intent**: Informational / Commercial / Transactional (must specify one)
3. **Primary Keyword** (optional): If not provided, will infer and state assumption
4. **Internal Link Targets** (1-3 URLs): Product page, pricing page, signup page, etc.
5. **Tone**: Keep original (default) / More authoritative / More marketing / More neutral

## Scoring Model (100 points)

| Category                      | Points |
| ----------------------------- | ------ |
| Keywords & Intent Fit         | 25     |
| Structure & Scanability       | 20     |
| Readability                   | 15     |
| Meta/Slug/Assets              | 15     |
| Internal Linking & Conversion | 10     |
| Content Depth & Trust         | 15     |

Each category must include: score reasoning + highest priority fix.

**Show deductions clearly:**

```
❌ Keyword missing in H1: -5 points
⚠️ Density too low (0.8% vs target 1-2%): -3 points
✅ Good heading hierarchy: +0 (no deduction)
```

## Issue Priority Classification

**Critical** (Fix Immediately):

- Missing or poor meta description
- No keyword in title or H1
- Keyword density too high/low (stuffing or insufficient)

**High Priority**:

- Poor readability score
- Chaotic heading hierarchy
- Images missing alt text
- Thin content

**Medium Priority**:

- Additional keyword opportunities
- Featured snippet opportunities
- Internal link optimization

## Workflow

For detailed step-by-step workflow, see [workflow.md](workflow.md).

**Summary**:

1. Keywords & Intent Analysis
2. Structure & Scanability Check
3. Readability Metrics
4. Meta/Slug/Alt/Links Generation
5. Content Depth & E-E-A-T Signals
6. Featured Snippet Opportunities
7. Final Output (Report + Optimized Draft)

## Constraints

- Never give advice without copy-paste ready meta/slug/rewrites
- Never force keywords unnaturally; prioritize natural expression (flag over-optimization risks)
- Never fabricate competitor data; if user wants comparison, request top URLs or permission to fetch
- Always preserve author's original voice and tone during optimization

## Troubleshooting

| Issue                          | Solution                                     |
| ------------------------------ | -------------------------------------------- |
| Cannot fetch URL               | Ask user to provide page content directly    |
| No keyword provided            | Infer from content, state assumption clearly |
| Content too short for analysis | Request full article or note limitations     |
| Missing internal link targets  | Ask user for 1-3 conversion page URLs        |

## Supporting Files

For detailed information, read these files when needed:

- **Detailed workflow steps**: [workflow.md](workflow.md)
- **Writing rules & SEO reference**: [reference.md](reference.md)
- **Output templates**: See templates/
