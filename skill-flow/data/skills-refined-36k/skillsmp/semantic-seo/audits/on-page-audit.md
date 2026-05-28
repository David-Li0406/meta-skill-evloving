# On-Page Audit Framework

Complete checklist for optimizing an existing webpage based on Algorithmic Authorship, Microsemantics, and Cost of Retrieval minimization principles.

## Table of Contents

1. [Strategic Fundamentals & E-A-T](#i-strategic-fundamentals--e-a-t-audit)
2. [Content Structure & Flow](#ii-content-structure--flow-audit)
3. [Visuals, Schema & Layout](#iii-visuals-schema--layout-audit)
4. [Interlinking & Anchor Text](#iv-interlinking--anchor-text-audit)
5. [Technical & Crawl Efficiency](#v-technical--crawl-efficiency-audit)
6. [Additional Concepts](#vi-additional-audit-concepts)

---

## I. Strategic Fundamentals & E-A-T Audit

Verify the page is strategically positioned and projects credibility.

### A. Macro Context Focus

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Single focus | Page targets ONE Macro Context and ONE Central Entity | |
| H1/Title alignment | H1, Title, and Centerpiece Text share the same core goal | |
| No topic mixing | Two main themes on same page = relevance dilution | |

**Correct**: Page focuses on "Types of Glasses" only
**Incorrect**: Page covers both "Glasses" and "Eye Health"

### B. Source Context Alignment

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| SC match | Content aligns with Source Context and CSI | |
| Attribute priority | Prioritized attributes match monetization goal | |
| Core/Author clarity | Clear whether page is CS or AS | |

**Correct**: Money-saving site prioritizes "Energy Consumption" over "Energy History"
**Incorrect**: B2B site prioritizes entertainment content unlinked to services

### C. E-A-T Signaling

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Author Entity | Defined, coherent author with credentials | |
| Human effort signals | Original research, studies, unique insights | |
| Expertise markers | Domain-specific terminology, depth | |
| No AI patterns | No generic phrases like "Overall" or "I had the pleasure" | |

### D. Factual Consensus (KBT)

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| EAV consistency | Facts match rest of website | |
| External alignment | Facts match authoritative knowledge bases | |
| Truth ranges | Uncertain values show ranges ("between X and Y") | |
| No contradictions | Numbers, dates, definitions consistent | |

### E. Content Coverage Weight

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Balanced weight | Subsection length matches importance to Macro Context | |
| No over-coverage | Minor attributes don't dominate the page | |
| Proportional H2s | Important topics get more coverage | |

**Incorrect**: 49 of 50 subheadings about one micro-detail

---

## II. Content Structure & Flow Audit

Verify logical flow and efficient answer presentation.

### A. Centerpiece Text

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| First 400 chars | Contains most crucial information | |
| Definition present | Core answer/definition in first sentence | |
| No blocking elements | No share buttons/ads before main text | |

### B. Subordinate Text (Featured Snippet)

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Direct answer | First sentence after heading answers directly | |
| Length | <40 words or <340 characters | |
| No fluff | No "As stated before" or contextless phrases | |

**Correct**: H2: "How to apply?" -> "The application process involves five steps:..."
**Incorrect**: H2: "How to apply?" -> "Many people wonder about this important topic..."

### C. Contextual Vector Flow

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Logical order | H1 -> H2 -> H3 follows incremental thought stream | |
| Natural progression | Definition -> Types -> Risks -> Treatment | |
| No interruptions | Related sections adjacent | |

### D. Contextual Bridge

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Bridge present | Transition between Macro and Micro context justified | |
| H2/H3 bridge | Subsection explains thematic shift | |
| Smooth transitions | No abrupt topic jumps | |

### E. Discourse Integration

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Anchor segments | Last sentence introduces next section's theme | |
| Mutual phrases | Key terms repeated at paragraph boundaries | |
| Connected flow | Paragraphs don't start with unrelated concepts | |

**Correct**: "...these **battery types** affect performance." -> H3: "**Battery Types** and Lifespan"

### F. Modality and Consensus

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Facts definitive | Present tense for established facts | |
| Conditional appropriate | "can/may" only for variable outcomes | |
| No false hedging | No "might" for consensus facts | |

---

## III. Visuals, Schema & Layout Audit

Verify non-textual content contributes to semantic signals.

### A. Visual Hierarchy

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Size reflects importance | Important components larger/higher | |
| Order matches intent | CTA/key info above fold for commercial | |
| LIFT model compliance | Components ordered by user intent | |

### B. Unique Visual Content

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Images unique | Not duplicate stock photos | |
| Branded | Contains site branding | |
| Informative | Infographics contain data/definitions | |

### C. Image Metadata

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| EXIF/IPTC data | Owner, license, description embedded | |
| Alt text varied | Expands topicality beyond H1 | |
| URL optimized | Short, max 3 words, no stopwords | |

### D. Structured Data

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Schema present | Appropriate type (Article, Product, FAQ, etc.) | |
| Complete properties | All relevant EAV info included | |
| No errors | Validated without warnings | |
| LCP in schema | Featured image URL matches visible LCP | |

### E. List Format Validation

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Format matches intent | Superlative = ordered; Instruction = ordered | |
| Intro sentence | States exact item count | |
| HTML correct | `<ol>` for ordered, `<ul>` for unordered | |

### F. Accessibility & Semantics

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Semantic HTML | Proper `<article>`, `<section>`, `<aside>` | |
| ARIA labels | Present where needed | |
| Screenreader ready | Logical reading order | |

---

## IV. Interlinking & Anchor Text Audit

Assess link quality and strategic positioning.

### A. Anchor Text Repetition

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Max 3x rule | Same exact anchor text <=3 times in main content | |
| Variation used | Synonyms, word order changes for 4th+ instance | |

### B. Link Precedence

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Definition first | Link placed AFTER entity/concept defined | |
| Not in first sentence | Links not in opening lines of paragraphs | |

### C. Annotation Text Quality

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Semantic alignment | Surrounding text supports anchor + target | |
| Context match | Annotation discusses target page's topic | |

**Correct**: Text about immigration -> anchor "Germany Visa" -> link to visa page
**Incorrect**: Generic sidebar link with no contextual support

### D. Link Count & Prominence

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Total count | <150 internal links per page | |
| Main content priority | More links in main content than boilerplate | |
| Dynamic headers | Headers/footers minimize static links | |

### E. URL Fragments

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| TOC present | Long articles have Table of Contents | |
| Jump links work | #fragment links to correct sections | |
| H2/H3 linkable | All major headings have IDs | |

---

## V. Technical & Crawl Efficiency Audit

Ensure low Cost of Retrieval.

### A. Indexation Status

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| No "crawled not indexed" | Check GSC for warnings | |
| No "discovered not indexed" | Quality issues suspected | |
| URL count optimal | Fewer, higher-quality pages | |

### B. Core Web Vitals

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| LCP | <2.5 seconds | |
| FID/INP | <100ms | |
| CLS | <0.1 | |
| Explicit dimensions | All images/dynamic elements sized | |

### C. Crawl KPIs

| Check | Requirement | Target | Pass/Fail |
|-------|-------------|--------|-----------|
| Response time | Server response | <100ms | |
| HTML hit ratio | % of crawl on HTML | >80% | |
| Error rate | 404/301/500 errors | 0% | |

### D. HTML Simplicity

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| DOM size | <1500 nodes | |
| Unused CSS/JS | Tree shaking applied | |
| Text-to-code ratio | High text, minimal code | |

### E. URL Structure

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Consistent | Casing, trailing slashes uniform | |
| Hierarchical | `/topic/subtopic` format | |
| Short | No redundant words | |
| Canonical correct | Points to preferred URL | |

### F. Index Exclusion Errors

| Check | Requirement | Pass/Fail |
|-------|-------------|-----------|
| Sitemap accuracy | Contains only indexable pages | |
| No robots.txt conflicts | Submitted pages not blocked | |
| No noindex conflicts | Submitted pages indexable | |

---

## VI. Additional Audit Concepts

### Quick Checks

| Concept | Check |
|---------|-------|
| **Contextless N-grams** | Remove "all also known as", "basically", "overall" |
| **Uniqueness Score** | Vocabulary richness indicates expertise |
| **Title Query Coverage** | % of ranking queries in Title Tag |
| **Momentum** | Publication frequency sufficient |
| **Review Authenticity** | No AI-generated review signatures |

### Scoring Template

| Section | Max Score | Actual |
|---------|-----------|--------|
| Strategic Fundamentals | 25 | |
| Content Structure | 25 | |
| Visuals & Schema | 20 | |
| Interlinking | 15 | |
| Technical | 15 | |
| **Total** | **100** | |

**Target**: 85+ for high-quality pages
