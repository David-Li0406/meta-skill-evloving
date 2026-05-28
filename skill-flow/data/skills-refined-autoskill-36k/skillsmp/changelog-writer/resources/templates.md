# Changelog Templates

## BaseHub Entry Fields

This frontmatter structure maps directly to `ChangelogEntryInput` type in `@repo/cms-workflows`, enabling zero-mapping publish via `/publish_changelog`.

### Core Fields

- **title**: 2-3 key features (e.g., "GitHub File Sync, Semantic Search, Team Workspaces")
- **slug**: Format: `0-<version>-lightfast-<feature-slug>` (e.g., "0-1-lightfast-github-file-sync-semantic-search")
- **publishedAt**: ISO date string (YYYY-MM-DD)
- **body**: Main changelog content (markdown) - this is the content after frontmatter

### AEO Fields (Answer Engine Optimization)

- **excerpt**: Short summary for listing pages (max 300 chars). Appears on changelog index pages and RSS feeds.
- **tldr**: 50-100 word summary optimized for AI citation engines. Rendered in a highlighted box at the top of the changelog page.

### SEO Fields (nested under `seo:`)

- **seo.metaDescription**: 150-160 char meta description with version number and target keyword
- **seo.focusKeyword**: Primary keyword phrase for SEO optimization (e.g., "webhook-driven sync", "semantic code search")
- **seo.secondaryKeyword**: Optional secondary keyword phrase for additional optimization
- **seo.faq**: Array of 2-4 question/answer pairs. Generates FAQPage schema for Google featured snippets.

### Internal Fields (nested under `_internal:`)

These fields are stripped before publishing to BaseHub:

- **_internal.status**: `draft` or `published`
- **_internal.source_prs**: Array of PR numbers or commit SHAs for traceability
- **_internal.generated**: ISO timestamp when draft was generated

### Frontmatter Template

```yaml
---
# Fields that map directly to ChangelogEntryInput
title: "Feature Name, Feature Name, Feature Name"
slug: "0-<version>-lightfast-<feature-slug>"  # e.g., "0-1-lightfast-github-file-sync"
publishedAt: "YYYY-MM-DD"
excerpt: "Short summary for listings, max 300 chars"
tldr: "50-100 word summary for AI citation and featured snippets. Appears at top of page."

# Categorized change sections (optional, arrays converted to newline-separated text)
improvements:
  - "Improved X for better Y"
  - "Enhanced Z performance by N%"
infrastructure:
  - "Migrated to new database schema"
  - "Added caching layer for API responses"
fixes:
  - "Fixed issue where X caused Y"
  - "Resolved race condition in Z"
patches:
  - "Security patch for CVE-XXXX"
  - "Updated dependencies to latest versions"

# SEO nested object (matches ChangelogSeoInput)
seo:
  metaDescription: "150-160 char meta description with version and keyword"
  focusKeyword: "primary-keyword-phrase"
  secondaryKeyword: "secondary-keyword-phrase"
  faq:
    - question: "What is [feature]?"
      answer: "Concise answer optimized for featured snippets and voice search."
    - question: "How do I [action]?"
      answer: "Step-by-step answer with specifics."

# Internal fields (stripped before publish, not sent to BaseHub)
_internal:
  status: draft
  source_prs: ["#123", "commit-hash"]
  generated: "YYYY-MM-DDTHH:MM:SSZ"
---
```

**Note on categorized sections:** The `improvements`, `infrastructure`, `fixes`, and `patches` fields are optional. Use them to organize changes into categories that render as bullet lists in BaseHub. Each array item becomes a bullet point.

## Document Structure


```markdown
**[2-3 key features as subtitle]**

---

### [Feature Name]

[1-3 sentences: what it does + user benefit]

**What's included:**
- Bullet list of specific capabilities
- Include limitations if any
- Mention beta/rollout status if applicable

**Example:**
\`\`\`yaml
# Config snippet or API example
\`\`\`

[Optional: "Why we built it this way" insight]

---

### [Next Feature]

[Repeat structure]

---

### What's Coming Next

[ONLY include if validated by implementation docs]

**Based on your feedback:**
1. **[Feature]** (vX.X) — [brief description, validated by roadmap]
2. **[Integration]** (when N+ customers request it)

---

### Resources

- [Quick Start](/docs/quick-start)
- [GitHub Setup](/docs/integrations/github)
- [API Reference](/docs/api)
- [Configuration Docs](/docs/config)
```

## Section Guidelines

### Feature Sections (in body)
- Lead with user benefit
- Include "What's included" bullets
- Add code example
- Disclose what's NOT included
- Optional: "Why we built it this way"

### Categorized Sections (in frontmatter)

Use the frontmatter arrays for categorized changes. These render as bullet lists in BaseHub:

- **improvements**: Enhancements to existing features (1-2 lines per item, focus on user impact)
- **infrastructure**: Platform/architecture changes (can be more technical)
- **fixes**: Bug fixes (describe what was broken and how it's fixed)
- **patches**: Security updates, dependency bumps

### What's Coming Next (in body)
- ONLY validated items from roadmap
- Use conditionals: "when N+ customers request"
- Be honest about prioritization
