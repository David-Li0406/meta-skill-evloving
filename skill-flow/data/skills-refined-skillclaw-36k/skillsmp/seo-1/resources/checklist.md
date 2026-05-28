# SEO/AEO Checklist

Pre-publish validation for Lightfast pages.

## Quick Checklist

### Meta & Technical
- [ ] **Title**: 50-60 chars, keyword near start, "| Lightfast" at end
- [ ] **Description**: 150-160 chars, includes primary keyword
- [ ] **Canonical URL**: Set and correct (https://lightfast.ai/...)
- [ ] **OpenGraph**: title, description, type, url, image complete
- [ ] **Twitter card**: summary_large_image configured
- [ ] **Image**: 1200x630px, under 1MB, alt text set

### Content Structure
- [ ] **TL;DR**: 40-100 words, self-contained, at top
- [ ] **Answer-first**: Key answer in first 200 words
- [ ] **Headings**: Question-format for key sections
- [ ] **FAQ section**: 3-5 Q&A pairs with self-contained answers
- [ ] **Internal links**: 3-5 relevant links
- [ ] **Tables/lists**: At least one structured element

### Schema
- [ ] **Primary schema**: Article, WebPage, or Product
- [ ] **FAQPage schema**: If FAQ section present
- [ ] **HowTo schema**: If step-by-step content
- [ ] **Schema validated**: Tested with Google Rich Results

---

## Detailed Checklist

### Required Fields

| Field | Constraint | Purpose |
|-------|------------|---------|
| Title | 50-60 chars, keyword + brand | Meta title |
| Meta description | 150-160 chars | Search snippet |
| TL;DR | 40-100 words | AI citation |
| Focus keyword | Selected and used 2-3x | SEO targeting |
| FAQ | 3-5 Q&A pairs | Featured snippets |

### Content Requirements

| Element | Requirement | Why |
|---------|-------------|-----|
| Answer-first | Key answer in first 200 words | AI extraction |
| Question headings | H2/H3 as questions | Voice search |
| Internal links | 3-5 per page | Topic authority |
| External citations | 5+ sources | E-E-A-T signals |
| Comparison table | At least one | Easy AI extraction |
| Author attribution | Name + credentials | Trust signals |

### Technical Requirements

| Element | Requirement | Implementation |
|---------|-------------|----------------|
| Canonical URL | Set correctly | `alternates.canonical` |
| OpenGraph | Complete | `openGraph` in metadata |
| Twitter card | Configured | `twitter` in metadata |
| JSON-LD | Appropriate schema | `<JsonLd>` component |
| Image alt text | Descriptive | All images |
| Mobile-friendly | Responsive | Test on mobile |

---

## Common Issues

### Title Problems

| Issue | Fix |
|-------|-----|
| Too long (>60 chars) | Shorten, move keyword to start |
| Missing keyword | Add primary keyword naturally |
| Missing brand | Add " \| Lightfast" at end |

### Description Problems

| Issue | Fix |
|-------|-----|
| Too short (<140 chars) | Expand with benefits |
| Too long (>160 chars) | Trim to 155-160 |
| Missing keyword | Include primary keyword naturally |
| Passive voice | Rewrite with active voice |

### Content Problems

| Issue | Fix |
|-------|-----|
| No TL;DR | Add 40-100 word summary at top |
| Generic headings | Convert to question format |
| No FAQ | Add 3-5 Q&A pairs |
| Missing internal links | Add 3-5 related page links |
| No tables/lists | Add at least one structured element |

### Schema Problems

| Issue | Fix |
|-------|-----|
| Missing FAQPage | Add if page has Q&A content |
| Invalid JSON-LD | Validate with Google tool |
| Missing dates | Add publishedDate, modifiedDate |
| Missing author | Add author with profile link |

---

## Validation Tools

- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- [PageSpeed Insights](https://pagespeed.web.dev/)

---

## Pre-Publish Summary

Before publishing any Lightfast page:

1. **Meta**: Title (50-60 chars) + Description (150-160 chars) + Canonical
2. **Content**: TL;DR + Answer-first + Question headings + FAQ
3. **Links**: 3-5 internal + 5+ external citations
4. **Schema**: Appropriate type + FAQPage if Q&A present
5. **Validate**: Rich Results Test + social card preview
