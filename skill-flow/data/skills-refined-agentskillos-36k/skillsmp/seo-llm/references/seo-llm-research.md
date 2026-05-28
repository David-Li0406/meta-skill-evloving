# seo-llm Research

Research document for the SEO and LLM discoverability skill. This skill helps developers optimize their projects and websites for both traditional search engines and AI/LLM systems.

## Phase 1: Upstream Survey

### Existing SEO/LLM Discoverability Skills

| Source | Finding |
|--------|---------|
| [obra/superpowers](https://github.com/obra/superpowers) | No SEO/LLM discoverability skills |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | No dedicated SEO skills |
| [mcpmarket.com](https://mcpmarket.com/tools/skills/seo-audit-geo-optimization) | "SEO Audit & GEO Optimization" skill exists for auditing pages and optimizing for AI search |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | General SEO workflow automation |

### Related Tools in Ecosystem

- **SEO Audit & GEO Optimization** — Audits pages for SEO gaps, optimizes for AI search visibility
- **Claude Skills collections** — 739+ skills across categories, some covering SEO workflows
- **InfraNodus Claude Skills** — Extended prompts for various AI workflows

**Gap identified**: No comprehensive skill combining traditional SEO, LLM discoverability (llms.txt), and AI agent instructions (AGENTS.md).

---

## Phase 2: Research Findings

### 1. llms.txt Specification

Source: [llmstxt.org](https://llmstxt.org/), [Semrush](https://www.semrush.com/blog/llms-txt/)

#### What is llms.txt?

A proposed standard for providing information to help LLMs use a website at inference time. Created by Jeremy Howard, it acts as a curated map guiding AI systems to the most relevant content.

#### File Format

Location: `/llms.txt` (root path)

```markdown
# Project Name
(Required: H1 with project/site name)

> Short summary with key information
(Optional: blockquote with summary)

Additional context paragraphs...
(Optional: markdown sections)

## Section Name
- [Page Title](url): Description
- [Another Page](url): Description
(Optional: H2 headers with file lists)
```

#### Current Adoption Status (Jan 2026)

- **Not yet widely adopted** by major AI companies
- OpenAI, Google, Anthropic have not officially confirmed they follow llms.txt
- Analysis shows minimal crawler visits to llms.txt pages
- Consider it advisory/future-proofing, not critical

#### Best Practices

- Keep content concise and expert-level
- Focus on most authoritative/relevant pages
- Update when significant content changes
- Complement with traditional SEO, not replace

---

### 2. AGENTS.md Convention

Sources: [agents.md](https://agents.md/), [GitHub Blog](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)

#### What is AGENTS.md?

An open standard for configuring AI coding agent behavior, stewarded by the Linux Foundation's Agentic AI Foundation. Launched jointly by Google, OpenAI, Factory, Sourcegraph, and Cursor.

Used by 60k+ open source projects.

#### Purpose

- README.md = for humans (quick starts, descriptions)
- AGENTS.md = for AI agents (build steps, tests, conventions)

#### File Format

Standard Markdown with no required structure. Recommended sections:

```markdown
# Project Name

## Build & Test Commands
npm install
npm test
npm run build

## Code Style
- Use TypeScript strict mode
- Prefer async/await over callbacks
- Max line length: 100 characters

## Directory Structure
- /src - Source code
- /tests - Test files
- /docs - Documentation

## Do Not Touch
- /vendor - Third-party code
- /.env* - Environment files
- /secrets - Sensitive configuration
```

#### Best Practices (from 2,500+ repos analysis)

1. **Put commands early** — `npm test`, `npm run build`, `pytest -v`
2. **Code examples over explanations** — Show, don't tell
3. **Set clear boundaries** — What AI should never touch
4. **Use directory hierarchy** — Place AGENTS.md in subpackages for specific instructions

---

### 3. robots.txt for AI Crawlers

Sources: [Paul Calvano](https://paulcalvano.com/2025-08-21-ai-bots-and-robots-txt/), [Cloudflare Blog](https://blog.cloudflare.com/from-googlebot-to-gptbot-whos-crawling-your-site-in-2025/)

#### AI Crawler User Agents

| Company | Training Crawler | Search/User Crawler |
|---------|------------------|---------------------|
| OpenAI | `GPTBot` | `ChatGPT-User`, `OAI-SearchBot` |
| Anthropic | `ClaudeBot` | `Claude-User`, `Claude-SearchBot` |
| Google | `Google-Extended` | `Googlebot` (unchanged) |
| Perplexity | `PerplexityBot` | `Perplexity-User` |
| Apple | `Applebot-Extended` | `Applebot` |
| Meta | `Meta-ExternalAgent` | `FacebookBot` |
| Common Crawl | `CCBot` | — |

#### Strategy: Block Training, Allow Search

```
# Block AI training crawlers
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /

# Allow AI search/user crawlers
User-agent: ChatGPT-User
Allow: /

User-agent: Claude-User
Allow: /

# Allow traditional search engines
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /
```

#### Important Notes

- Blocking `Google-Extended` does NOT affect traditional SEO rankings
- Major crawlers claim to respect robots.txt, but enforcement varies
- ~5.7% of AI crawler traffic is spoofed
- Cloudflare blocks AI bots by default since July 2025

---

### 4. XML Sitemaps

Sources: [sitemaps.org](https://www.sitemaps.org/protocol.html), [Search Engine Land](https://searchengineland.com/guide/xml-sitemaps)

#### Best Practices

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page</loc>
    <lastmod>2026-01-19</lastmod>
  </url>
</urlset>
```

#### Tag Recommendations

| Tag | Recommendation |
|-----|----------------|
| `<loc>` | Required — canonical URL |
| `<lastmod>` | Recommended — update only on significant changes |
| `<changefreq>` | Skip — ignored by Google |
| `<priority>` | Skip — ignored by Google |

#### Limits

- Max 50,000 URLs per sitemap
- Max 50 MB uncompressed
- Use sitemap index for larger sites

---

### 5. Structured Data (JSON-LD)

Sources: [Google Search Central](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data), [Schema.org](https://schema.org/)

#### Why JSON-LD?

Google's recommended format for structured data:
- Separate from HTML (in `<script>` tags)
- Easier to maintain
- Less prone to errors

#### Common Schema Types

| Type | Use Case |
|------|----------|
| `Organization` | Company info (homepage only) |
| `WebSite` | Site-wide info + search box |
| `Article`/`BlogPosting` | Blog posts, news |
| `Product` | E-commerce products |
| `FAQPage` | FAQ sections |
| `HowTo` | Step-by-step guides |
| `BreadcrumbList` | Navigation breadcrumbs |
| `SoftwareApplication` | Apps and tools |

#### Example: Organization + WebSite

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Example Corp",
      "url": "https://example.com",
      "logo": "https://example.com/logo.png",
      "sameAs": [
        "https://twitter.com/example",
        "https://github.com/example"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://example.com/#website",
      "url": "https://example.com",
      "name": "Example",
      "publisher": {"@id": "https://example.com/#organization"}
    }
  ]
}
```

#### Best Practices

- Place in `<head>` for clarity
- Only add schema for visible content
- Use correct types (don't guess)
- Validate with Google Rich Results Test
- Keep schema.org vocabulary up to date

---

### 6. Open Graph & Twitter Cards

Sources: [Open Graph Protocol](https://ogp.me/), [Twitter Cards Docs](https://developer.twitter.com/en/docs/twitter-for-websites/cards/guides/getting-started)

#### Essential Meta Tags

```html
<!-- Open Graph (Facebook, LinkedIn, etc.) -->
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Page description (155-160 chars)">
<meta property="og:image" content="https://example.com/image.png">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Example">

<!-- Twitter Cards -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@example">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Page description (max 200 chars)">
<meta name="twitter:image" content="https://example.com/image.png">
```

#### Image Best Practices

- Aspect ratio: 16:9 (1200x675px minimum)
- Format: JPG, PNG (no animated GIFs)
- Size: Under 5MB
- Include text sparingly (may be cropped)

#### Testing Tools

- [OpenGraph.xyz](https://www.opengraph.xyz/) — Preview without login
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- Twitter/X — Use Tweet Composer to preview

---

### 7. Generative Engine Optimization (GEO)

Sources: [TripleDart GEO Guide](https://www.tripledart.com/ai-seo/generative-engine-optimization), [Digital Authority](https://www.digitalauthority.me/resources/generative-engine-optimization-best-practices/)

#### What is GEO?

Optimizing content to appear in AI-generated answers from ChatGPT, Gemini, Perplexity, and Claude.

#### Key Differences from SEO

| SEO | GEO |
|-----|-----|
| Rank in search results | Get cited in AI responses |
| Keyword targeting | Topic/entity targeting |
| Page-level optimization | Passage-level optimization |
| Link building | Authority/citation building |

#### GEO Best Practices

1. **Cite authoritative sources** — Link to research, official docs
2. **Include statistics** — Specific numbers, percentages
3. **Add expert quotes** — With proper attribution
4. **Structure for extraction** — Short paragraphs, bullets, lists
5. **Focus on E-E-A-T** — Experience, Expertise, Authority, Trust

#### Content Structure for AI

```markdown
## Clear Question as Heading

Direct answer in first sentence. Supporting context follows.

Key points:
- Specific fact with number
- Another concrete detail
- Citation to authoritative source

According to [Expert Name], "quotable insight here."
```

#### Impact

Princeton research shows GEO optimization can improve AI visibility by 30-40%.

---

### 8. Project-Specific Files

#### Recommended Files for LLM Discoverability

| File | Purpose | Location |
|------|---------|----------|
| `llms.txt` | AI inference guidance | `/llms.txt` |
| `AGENTS.md` | AI coding agent instructions | Root or subdirs |
| `CLAUDE.md` | Claude Code specific | Root |
| `robots.txt` | Crawler directives | `/robots.txt` |
| `sitemap.xml` | Page index | `/sitemap.xml` |
| `humans.txt` | Team credits (optional) | `/humans.txt` |

---

## Audit Checklist Summary

### Critical (Must Have)
- [ ] `robots.txt` exists with AI crawler rules
- [ ] `sitemap.xml` exists and is valid
- [ ] Meta title and description on all pages
- [ ] HTTPS enabled

### Important (Should Have)
- [ ] `AGENTS.md` for code repositories
- [ ] `CLAUDE.md` for Claude Code users
- [ ] JSON-LD structured data (Organization, WebSite)
- [ ] Open Graph meta tags
- [ ] Twitter Card meta tags
- [ ] Canonical URLs set

### Recommended (Nice to Have)
- [ ] `llms.txt` for AI discoverability
- [ ] Schema.org markup for content types
- [ ] FAQ schema for question pages
- [ ] Breadcrumb schema
- [ ] `humans.txt` for team attribution

### AI-Specific Considerations
- [ ] Decide: block training crawlers, allow search crawlers?
- [ ] Content structured for passage extraction
- [ ] Statistics and citations included
- [ ] E-E-A-T signals present

---

## Sources

### Standards & Specifications
- [llmstxt.org](https://llmstxt.org/) — llms.txt specification
- [agents.md](https://agents.md/) — AGENTS.md specification
- [Schema.org](https://schema.org/) — Structured data vocabulary
- [Open Graph Protocol](https://ogp.me/) — Social sharing metadata
- [sitemaps.org](https://www.sitemaps.org/protocol.html) — Sitemap protocol

### Documentation
- [Google Search Central - Structured Data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Twitter Cards Documentation](https://developer.twitter.com/en/docs/twitter-for-websites/cards/guides/getting-started)
- [GitHub Blog - How to write a great AGENTS.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)

### AI Crawlers
- [Cloudflare - From Googlebot to GPTBot](https://blog.cloudflare.com/from-googlebot-to-gptbot-whos-crawling-your-site-in-2025/)
- [Search Engine Journal - AI Crawler User Agents](https://www.searchenginejournal.com/ai-crawler-user-agents-list/558130/)
- [ai-robots-txt/ai.robots.txt](https://github.com/ai-robots-txt/ai.robots.txt) — Community robots.txt for AI

### GEO & SEO
- [TripleDart - GEO Complete Guide](https://www.tripledart.com/ai-seo/generative-engine-optimization)
- [Semrush - What Is llms.txt](https://www.semrush.com/blog/llms-txt/)
- [Search Engine Land - llms.txt Proposed Standard](https://searchengineland.com/llms-txt-proposed-standard-453676)
