# SEO Article Optimizer — Workflow

Execute these steps in order for every article optimization.

## Step 1: Keywords & Intent (Target Keywords)

Must cover:

- Identify Primary keyword (from user or infer from content)
- Check keyword placement: Title, H1, first 100 words, subheadings
- Calculate density (target 1-2% as reference)
- List LSI / semantic variations (avoid stuffing)
- Flag keyword stuffing (if present)

### Keyword Placement Checklist (Visual Format)

Use visual indicators for clarity:

```
✅ Title: Contains primary keyword
❌ H1: Missing → Add "{keyword}" to H1
⚠️ First 100 words: Weak presence → Strengthen intro
✅ H2 headings: 2/5 contain keyword variations
⚠️ Density: 0.8% (low) → Target 1-2% (add 8-10 mentions)
```

### LSI Keywords Analysis

Identify and report:

- **LSI Keywords Found**: List semantic variations already in content
- **Recommended Additions**: Suggest 3-5 related terms to add naturally
- **Over-optimization Warning**: Flag if any term appears too frequently

## Step 2: Structure & Scanability (Content Structure)

- Heading hierarchy: Single H1 → Multiple H2 → H3 (no level skipping)
- Subheadings should be descriptive (independently convey section content)
- Paragraph length: Recommend < 150 words for readability and scanning
- Consider adding: TOC, key takeaways, step lists, comparison tables

## Step 3: Readability Metrics

Must output these metrics in a structured format:

### Readability Score Card

```
┌─────────────────────────────────────────────┐
│ READABILITY METRICS                         │
├─────────────────────────────────────────────┤
│ Flesch Reading Ease:    XX/100 (target 60-70)
│ Estimated Grade Level:  X
│ Avg Sentence Length:    XX words (target <20)
│ Passive Voice:          X% (target <10%)
│ Transition Words:       X% (target >25%)
└─────────────────────────────────────────────┘
```

### Required Outputs

- Flesch Reading Ease (target 60-70 for general audience)
- Estimated Grade Level (target 8th grade for broad audience)
- Average sentence length (target < 20 words)
- Passive voice percentage (target < 10%)
- Transition words percentage (target > 25% for good flow)
- Long sentence/paragraph examples (at least 2 before/after rewrites)

> **Note for non-English content**: Flesch may not perfectly apply. Output actionable metrics like sentence length, paragraph length, abstract noun density, transition word usage, and note applicability boundaries.

## Step 4: Publishing Assets (Meta / Slug / Alt / Links)

Must generate:

- **Meta title**: 50-60 characters (or equivalent strategy), include primary keyword
- **Meta description**: 150-160 characters, include keyword + CTA
- **URL slug**: Short, readable, hyphenated, keyword-rich
- **Image alt**: Naturally include keyword (when appropriate); distinguish decorative images (alt="")

### Internal Links (Content-Length Based Formula)

Recommend internal links based on article length:
| Word Count | Recommended Links |
|------------|-------------------|
| < 1000 words | 2-3 internal links |
| 1000-2500 words | 4-6 internal links |
| > 2500 words | 7-10 internal links |

Must include:

- **Early link** (first 20%): Point to key conversion page
- **Mid-content links**: Point to related features/docs/case studies
- **CTA link in conclusion**: Point to signup/trial/contact

Provide recommended anchor text for each link.

### External Links

- If citing data/sources, suggest linking to high-quality sources (enhances credibility)
- Recommend opening external links in new tab

## Step 5: Content Depth & E-E-A-T Signals (Content Quality)

- **Word count analysis**: Competitive topics typically need 1500+ words; provide current count and recommendation
- **Question chain coverage**: Does content answer the full user journey? (definition → why → steps → comparison → recommendation → FAQ)
- **Topic coverage completeness**: List missing subtopics (Content Gaps)
- **Unique value**: What's your unique angle compared to typical articles? (must identify)
- **Trust signals**: Author bio, case studies, data sources, update date, screenshots/demos (recommend based on article type)

### Schema Markup Recommendations

Evaluate and recommend appropriate structured data:

| Schema Type | When to Use             | Required Fields                               |
| ----------- | ----------------------- | --------------------------------------------- |
| Article     | Blog posts, news        | headline, author, datePublished, dateModified |
| FAQ         | Q&A sections present    | question, acceptedAnswer                      |
| HowTo       | Step-by-step tutorials  | name, step (with text)                        |
| Review      | Product/service reviews | itemReviewed, reviewRating, author            |
| Product     | Product pages           | name, offers, aggregateRating                 |

If applicable, provide ready-to-use JSON-LD snippet.

## Step 6: Featured Snippet / SERP Opportunities

Must evaluate and output:

- Snippet suitability (definition 40-60 words, steps/lists, tables)
- If suitable: Generate insertable snippet block (see templates/snippet-blocks.md)
- If FAQ suitable: Provide FAQ question set (3-6) and suggest FAQ schema (recommendation only, not mandatory)

### Featured Snippet Opportunity Criteria

| Snippet Type | Trigger Phrases                           | Format                    |
| ------------ | ----------------------------------------- | ------------------------- |
| Definition   | "What is...", "Define..."                 | 40-60 word paragraph      |
| List         | "How to...", "Steps to...", "Types of..." | 5-8 numbered/bullet items |
| Table        | "vs", "comparison", "differences"         | 2-4 column comparison     |
| FAQ          | Multiple questions in content             | Q&A pairs                 |

## Step 7: Output (Strict Format)

Must follow templates/article-report-template.md structure, plus:

- Optimized Draft (Markdown, preserve original voice)
- Implementation Checklist (publish checklist)

## Example Workflow

**User**: "Help me optimize this article about 'best project management tools'"

**Analysis Steps**:

1. Check keyword placement → Title has it but H1 doesn't (needs fix)
2. Calculate density → 0.5% (too low, need 8-10 more mentions)
3. Analyze readability → Flesch 55 (good), but sentences too long
4. Generate meta tags → Create compelling meta description
5. Identify content gaps → Missing "pricing comparison" and "team size recommendations"
6. Find internal link opportunities → Link to "project management tips" article
7. Suggest snippet format → Create comparison table
8. Output prioritized action list
