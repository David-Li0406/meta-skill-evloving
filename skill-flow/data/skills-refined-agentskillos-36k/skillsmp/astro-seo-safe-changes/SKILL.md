---
name: astro-seo-safe-changes
description: Safely update SEO metadata, OpenGraph/Twitter tags, canonical URLs, robots directives, and schema JSON-LD for the Top10Maison Astro site. Use when editing page-level SEO or structured data; extend existing tags/components; reuse the shared SEO component and schema helpers; avoid inline JSON-LD unless explicitly requested.
---

# Astro SEO Safe Changes

## Overview
- Use for any SEO, metadata, or schema edits on the Top10Maison Astro site.
- Guardrails: never remove existing meta tags; extend or enhance only. Reuse `SEO.astro` and schema helpers; do not inline JSON-LD unless requested; prefer reusable Astro components for schema.

## Quick start checklist
1. Locate the layout (`src/layouts/BaseLayout.astro` or `src/layouts/MinimalLayout.astro`) and pass props: `title`, `description`, `canonical`, optional `schema` array, `ogImage`, `ogType`, `robots`, `metaRefresh`.
2. Canonical: `const site = requireSite(Astro.site); const canonical = buildCanonical(site, "<pathname>");` from `src/utils/seo.ts`. Keep URLs absolute.
3. Titles/descriptions: concise, unique, and aligned with on-page content. If adding brand, use `buildTitle(pageTitle, "Top10Maison")` only when the brand is not already present.
4. Schema: build objects with helpers in `src/utils/schema.ts`; append to existing `schema` arrays; never delete existing entries. The SEO component auto-adds Organization and WebSite schema.
5. OpenGraph/Twitter: pass `ogImage` (relative or absolute) and optional `ogType`. The SEO component resolves absolute URLs; set OG/Twitter alt text to the page title.
6. Robots/meta refresh: default is `index,follow`. Use `noindex` only when intentional (e.g., staging or gated pages). `metaRefresh` only if explicitly needed.

## Components and helpers to reuse (do not duplicate)
- `src/components/SEO.astro`: renders meta, OpenGraph/Twitter tags, and outputs the `schema` array via `<script type="application/ld+json">`. Do not add inline JSON-LD elsewhere unless explicitly requested.
- `src/utils/seo.ts`: `requireSite`, `buildCanonical`, `buildTitle`.
- `src/utils/schema.ts`: schema builders; prefer these over hand-crafted schema objects.
- Layout meta: Base/Minimal layouts already include theme color, fonts, analytics, verification tags—do not remove or rename these when editing SEO.

## Structured data patterns (helpers only)
- Breadcrumbs: `buildBreadcrumbSchema(site, items)`.
- Products: `buildProductSchema(site, product)`.
- Reviews: `buildReviewSchema(site, product)`.
- Articles/toplists: `buildArticleSchema(site, toplist, canonicalUrl?)`.
- FAQs: `buildFaqSchema(items)`.
- Lists: `buildItemListSchema(items, { ordered?: boolean })`.
- Keep `@context` and `@type` on every object; ensure URLs are absolute and values match on-page content.

## Safety checklist before committing
- All existing meta tags remain; only extend/update values as needed.
- SEO component and schema helpers are reused; no new inline `<head>` tags or JSON-LD blobs.
- Canonical/OG/Twitter URLs are absolute; `og:image:alt` matches the page title.
- Robots directives are intentional and minimal.
- Schema objects include required fields and align with visible content.
- No routing/slug changes or layout meta removals are introduced as part of SEO tweaks.
