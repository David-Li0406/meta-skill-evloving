---
id: seo-fundamentals
name: "SEO Fundamentals"
domain: MKT
skill: faion-marketing-manager
category: "marketing"
---

# SEO Fundamentals

## Metadata

| Field | Value |
|-------|-------|
| **ID** | seo-fundamentals |
| **Name** | SEO Fundamentals |
| **Category** | Marketing |
| **Difficulty** | Intermediate |
| **Agent** | faion-seo-agent |
| **Related** | content-marketing, landing-page-design, analytics-setup |

---

## Problem

You want free, sustainable traffic but don't understand how search engines work. Without SEO, you miss 53% of all website traffic that comes from organic search.

Most SEO advice is outdated or wrong. You waste months on tactics that don't work while competitors rank for your keywords.

---

## Framework

SEO has 3 pillars:

```
Technical SEO  → Can Google crawl and index your site?
On-Page SEO    → Does your content match search intent?
Off-Page SEO   → Do other sites trust and link to you?
```

### Pillar 1: Technical SEO

**Critical technical factors:**

| Factor | What to Check | Tool |
|--------|---------------|------|
| **Crawlability** | robots.txt allows crawling | Search Console |
| **Indexability** | Pages in Google index | site:domain.com |
| **Site speed** | Core Web Vitals pass | PageSpeed Insights |
| **Mobile** | Mobile-friendly | Mobile-Friendly Test |
| **HTTPS** | SSL certificate | Browser |
| **Structure** | XML sitemap exists | /sitemap.xml |

**Technical checklist:**

```markdown
## Technical SEO Audit

### Crawling
- [ ] robots.txt allows important pages
- [ ] No important pages blocked
- [ ] XML sitemap submitted to Search Console
- [ ] No orphan pages

### Indexing
- [ ] Important pages indexed (site:domain.com)
- [ ] Canonical tags correct
- [ ] No duplicate content
- [ ] hreflang for multi-language

### Performance
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] Images optimized (WebP, lazy load)

### Mobile
- [ ] Responsive design
- [ ] Readable text without zoom
- [ ] Tap targets spaced properly

### Security
- [ ] HTTPS enabled
- [ ] No mixed content
- [ ] Security headers set
```

### Pillar 2: On-Page SEO

**On-page optimization checklist:**

| Element | Best Practice |
|---------|---------------|
| **Title tag** | Primary keyword + benefit, <60 chars |
| **Meta description** | Compelling summary, 120-160 chars |
| **URL** | Short, keyword-rich, hyphens |
| **H1** | Single H1, contains keyword |
| **Headers** | H2-H6 hierarchy, keywords naturally |
| **Content** | Comprehensive, answers intent |
| **Images** | Alt text, compressed, descriptive names |
| **Internal links** | Link to related pages |
| **External links** | Link to authoritative sources |

**Content optimization:**

1. **Search intent match**
   - Informational: How-to, guides
   - Commercial: Comparisons, reviews
   - Transactional: Product pages

2. **Content depth**
   - Cover topic completely
   - Beat competitors in comprehensiveness
   - Include related subtopics

3. **Content freshness**
   - Update outdated content
   - Add new information
   - Change "last updated" date

### Pillar 3: Off-Page SEO

**Link building strategies:**

| Strategy | Difficulty | Impact |
|----------|------------|--------|
| **Guest posting** | Medium | High |
| **Resource link building** | Medium | High |
| **Broken link building** | Low | Medium |
| **HARO/Journalist queries** | Low | High |
| **Creating linkable assets** | High | Very High |
| **Digital PR** | High | Very High |

**Link quality factors:**

- Domain authority of linking site
- Relevance of linking site/page
- Anchor text naturalness
- dofollow vs nofollow
- Link placement (in content > footer)

**Avoid:**

- Buying links
- Link farms
- Excessive link exchanges
- Irrelevant directory submissions

---

## Templates

### SEO Content Brief

```markdown
# SEO Brief: [Target Keyword]

## Keyword Data
- Volume: [monthly searches]
- Difficulty: [1-100]
- Intent: [informational/commercial/transactional]

## SERP Analysis
### Top 3 Results
1. [URL] - [Word count] - [Key sections]
2. [URL] - [Word count] - [Key sections]
3. [URL] - [Word count] - [Key sections]

### Common Elements
- All include: [list]
- Missing from all: [opportunity]

## Content Requirements
- Word count: [X-Y words]
- H2s to include: [list]
- Questions to answer: [list from People Also Ask]
- Entities to mention: [related topics]

## On-Page SEO
- Title: [suggestion]
- Meta description: [suggestion]
- URL: /[slug]
- H1: [suggestion]

## Internal Links
- Link TO: [existing pages]
- Link FROM: [existing pages to update]
```

### Monthly SEO Report

```markdown
# SEO Report - [Month Year]

## Summary
- Organic traffic: [X] ([+/-Y%] vs last month)
- Keywords ranking: [X] ([+/-Y] vs last month)
- Backlinks: [X] ([+/-Y] vs last month)

## Traffic

| Source | Sessions | Change |
|--------|----------|--------|
| Organic | [X] | [+/-Y%] |
| Direct | [X] | [+/-Y%] |
| Referral | [X] | [+/-Y%] |

## Top Pages

| Page | Traffic | Keyword | Position |
|------|---------|---------|----------|
| [URL] | [X] | [kw] | [pos] |
| [URL] | [X] | [kw] | [pos] |

## Keyword Movement

| Keyword | Old | New | Change |
|---------|-----|-----|--------|
| [kw] | [X] | [Y] | [+/-] |

## Actions This Month
1. [Action taken]
2. [Action taken]

## Next Month Plan
1. [Action planned]
2. [Action planned]
```

---

## Examples

### Example 1: Blog Post Optimization

**Before:**
- Title: "Our Thoughts on Productivity"
- URL: /blog/post-123
- H1: "Productivity Tips"

**After:**
- Title: "15 Productivity Tips That Actually Work (2026 Guide)"
- URL: /blog/productivity-tips
- H1: "15 Productivity Tips to Get More Done in Less Time"

**Result:** Position 47 to Position 5 in 3 months

### Example 2: Technical Fix

**Problem:** Site not indexed

**Investigation:**
- robots.txt: `Disallow: /` (blocking everything!)
- Meta robots: `noindex` on all pages

**Fix:**
- Update robots.txt to allow crawling
- Remove noindex tags
- Submit sitemap

**Result:** 0 to 500 indexed pages in 2 weeks

---

## Implementation Checklist

- [ ] Set up Google Search Console
- [ ] Set up Google Analytics
- [ ] Run technical SEO audit
- [ ] Fix critical technical issues
- [ ] Do keyword research (50+ terms)
- [ ] Optimize existing pages
- [ ] Create content calendar
- [ ] Build internal linking structure
- [ ] Start link building outreach
- [ ] Set up monthly reporting

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Keyword stuffing | Google penalizes | Write naturally |
| Ignoring technical SEO | Can not rank if not indexed | Fix technical first |
| Chasing high-volume keywords | Too competitive | Start with long-tail |
| Buying links | Google penalty risk | Earn links naturally |
| No patience | SEO takes 6-12 months | Commit long-term |
| Ignoring intent | Traffic but no conversions | Match search intent |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Keyword research | Ahrefs, Semrush, Moz |
| Technical audit | Screaming Frog, Sitebulb |
| On-page | Surfer, Clearscope, Frase |
| Rank tracking | Ahrefs, Semrush, AccuRanker |
| Link building | Ahrefs, Hunter.io, Pitchbox |
| Analytics | Search Console, Google Analytics |

---

## Key Metrics

| Metric | What It Measures | Target |
|--------|------------------|--------|
| Organic traffic | SEO reach | Growing month-over-month |
| Keywords in top 10 | Visibility | Increasing |
| Domain authority | Site strength | Growing |
| Core Web Vitals | Technical health | All green |
| Click-through rate | Title/desc effectiveness | >3% |

---

## Related Methodologies

- **content-marketing:** Content Marketing (content for SEO)
- **landing-page-design:** Landing Page Design (convert SEO traffic)
- **analytics-setup:** Analytics Setup (measure SEO)
- **funnel-optimization:** Funnel Optimization (SEO-to-conversion)

---

*Methodology: seo-fundamentals | Marketing | faion-seo-agent*
