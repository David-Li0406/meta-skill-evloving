# GenuVerity Report Input Schema

> This document defines the exact data format Claude Code needs to generate a GenuVerity fact-check report. Gemini Deep Research should output data in this format.

---

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        REPORT GENERATION PIPELINE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  GEMINI DEEP RESEARCH                    CLAUDE CODE                     │
│  ────────────────────                    ───────────                     │
│                                                                          │
│  1. User provides query                  4. Receives JSON input          │
│  2. Gemini researches 5-15 min           5. Validates all URLs           │
│  3. Outputs structured JSON ──────────►  6. Generates HTML from template │
│                                          7. Creates Chart.js visuals     │
│                                          8. Updates reports-data.js      │
│                                          9. Runs validation              │
│                                          10. Commits & deploys           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Required JSON Schema

### Single Report Format

```json
{
  "slug": "claim-name-month-year",
  "title": "Full Title: Is [X Claim] True?",
  "subtitle": "Optional subtitle providing additional context",
  "verdict": "FALSE",
  "verdict_explanation": "One sentence explaining the verdict",
  "category": "Health & Science",
  "subcategory": "Vaccines",
  "read_time": 8,
  "publish_date": "2026-01-15",

  "claim": {
    "text": "The exact claim being fact-checked, in one sentence",
    "claimant": "Person or organization who made the claim",
    "date_made": "January 10, 2026",
    "platform": "Twitter/X"
  },

  "forensics": {
    "patient_zero": "Description of earliest detectable source with link if available",
    "propagation_vector": "Bot Injection | State-Sourced | Algorithmic | Organic",
    "forensic_markers": ["AI synthetic signature", "LLM-generated patterns"],
    "velocity_12h": 50000,
    "bot_density_percent": 35
  },

  "tldr": "One paragraph (2-3 sentences) summary of the verdict and key finding",

  "executive_summary": "A longer summary (3-5 sentences) providing context, the key evidence, and the conclusion",

  "sources": [
    {
      "id": 1,
      "title": "Source Article Title",
      "url": "https://example.gov/article",
      "domain": "example.gov",
      "type": "GOV",
      "credibility_score": 5,
      "quote": "Verbatim quote from this source that supports the verdict",
      "accessed": "2026-01-15"
    }
  ],

  "sections": [
    {
      "heading": "Background",
      "content": "Full paragraph of analysis text. Reference sources using [N] notation.",
      "source_refs": [1, 2]
    },
    {
      "heading": "The Evidence",
      "content": "Detailed analysis with inline source references [3][4].",
      "source_refs": [3, 4]
    }
  ],

  "why_this_spread": "For FALSE/MISLEADING verdicts: 2-3 sentences explaining why people believed this claim. What made it seem credible? What legitimate concerns does it tap into?",

  "charts": [
    {
      "id": "comparisonChart",
      "type": "bar",
      "title": "Chart Title",
      "caption": "Explanation of what the chart shows",
      "labels": ["Label 1", "Label 2", "Label 3"],
      "datasets": [
        {
          "label": "Dataset Name",
          "data": [100, 250, 75],
          "color": "#ef4444"
        }
      ]
    }
  ],

  "tables": [
    {
      "title": "Claim vs Reality",
      "headers": ["Claim", "Reality", "Source"],
      "rows": [
        ["What was claimed", "What evidence shows", "Source name [1]"],
        ["Another claim", "Another reality", "Source name [2]"]
      ]
    }
  ],

  "keywords": ["keyword1", "keyword2", "keyword3", "fact-check"]
}
```

---

## Field Requirements

### Required Fields (MUST be present)

| Field | Type | Description |
|-------|------|-------------|
| `slug` | string | URL-safe identifier: `lowercase-with-dashes` |
| `title` | string | Full title, often in question format |
| `verdict` | enum | One of: `FALSE`, `TRUE`, `MISLEADING`, `MIXED`, `CONTEXT` |
| `category` | enum | See categories list below |
| `claim.text` | string | The exact claim being checked |
| `tldr` | string | 2-3 sentence summary |
| `executive_summary` | string | 3-5 sentence detailed summary |
| `sources` | array | Minimum 8 sources, each with url, title, quote |
| `sections` | array | Minimum 2 content sections |

### Optional Fields (Enhance quality)

| Field | Type | When to Include |
|-------|------|-----------------|
| `subtitle` | string | When title needs clarification |
| `verdict_explanation` | string | Always recommended |
| `claim.claimant` | string | If known who made the claim |
| `claim.platform` | string | Where the claim spread |
| `why_this_spread` | string | **Required** for FALSE/MISLEADING verdicts |
| `charts` | array | When data can be visualized |
| `tables` | array | When comparing claims to reality |
| `keywords` | array | For SEO (auto-generated if missing) |

### Forensics Fields (For Deep Analysis)

| Field | Type | Description |
|-------|------|-------------|
| `forensics.patient_zero` | string | Earliest detectable source of the claim |
| `forensics.propagation_vector` | enum | `Bot Injection`, `State-Sourced`, `Algorithmic`, `Organic` |
| `forensics.forensic_markers` | array | AI signatures, patterns (e.g., "Flux.1 artifacts") |
| `forensics.velocity_12h` | number | Estimated reach in first 12 hours |
| `forensics.bot_density_percent` | number | Estimated % of automated amplification |

### Source Credibility Score (GenuVerity Rubric)

| Score | Level | Description |
|-------|-------|-------------|
| 5 | Primary | Live data, court dockets, official gov transcripts |
| 4 | Verified | Editorial oversight (AP, Reuters, WSJ) |
| 3 | Regional | High-quality localized/specialized reporting |
| 2 | Partisan | Biased framing, omitted context |
| 1 | Malign | Known hoax history, anonymous sourcing, bot-driven |

---

## Standard Categories (Use Only These)

| Category | Use For |
|----------|---------|
| `Fact Check` | Standard claim verification |
| `AI & Deepfakes` | Synthetic media, AI-generated content |
| `Foreign Influence` | State-sponsored disinfo, foreign operations |
| `Conspiracy & Hoaxes` | Debunked conspiracy theories |
| `U.S. Politics & Policy` | Domestic political claims |
| `International` | Non-US political/world events |
| `Health & Science` | Medical, scientific misinformation |
| `Platform & Tech` | Social media, tech company issues |
| `Media & Journalism` | Press accuracy, media manipulation |
| `Economic & Financial` | Financial misinformation |

---

## Verdicts

| Verdict | Color | When to Use |
|---------|-------|-------------|
| `FALSE` | Red | Claim is demonstrably untrue |
| `TRUE` | Green | Claim is verified as accurate |
| `MISLEADING` | Amber | Contains truth but distorts context |
| `MIXED` | Cyan | Partially true, partially false |
| `CONTEXT` | Blue | Needs additional context to evaluate |

---

## Source Requirements

### Minimum: 8 sources per report

### Source Types (for `type` field)

| Type | Description | Trust Score |
|------|-------------|-------------|
| `GOV` | Government sources (.gov) | 95-100 |
| `STUDY` | Peer-reviewed research | 90-98 |
| `NEWS` | Major news outlets | 85-92 |
| `FACTCHECK` | Fact-checking organizations | 90-95 |
| `ORG` | Official organizations | 85-95 |
| `DATA` | Statistical databases | 90-98 |
| `PRIMARY` | Direct/primary sources | 95-100 |

### Source Quality Rules

1. **NO Wikipedia** - Find the primary source Wikipedia cites
2. **Verify URLs** - All URLs must be accessible
3. **Include quotes** - Verbatim quotes that support the analysis
4. **Date accessed** - When the source was verified

---

## Chart Configuration

### Supported Chart Types

| Type | Use For |
|------|---------|
| `bar` | Comparing categories |
| `line` | Trends over time |
| `doughnut` | Parts of a whole |
| `hbar` | Horizontal comparisons |

### Allowed Colors

```json
{
  "blue": "#3b82f6",
  "cyan": "#06b6d4",
  "green": "#10b981",
  "amber": "#f59e0b",
  "red": "#ef4444"
}
```

**NEVER use purple (#8b5cf6)**

### Chart Example

```json
{
  "id": "vaccineScheduleChart",
  "type": "bar",
  "title": "Vaccine Doses: Claim vs Reality",
  "caption": "Actual CDC schedule shows far fewer doses than viral claim suggests",
  "labels": ["Viral Claim", "CDC Schedule"],
  "datasets": [{
    "label": "Number of Doses",
    "data": [72, 27],
    "color": "#ef4444"
  }]
}
```

---

## Table Configuration

### When to Use Tables

- Comparing claims to evidence
- Showing timelines
- Listing multiple sub-claims with verdicts
- Presenting structured data

### Table Example

```json
{
  "title": "What the Claim Got Wrong",
  "headers": ["Claim", "Reality", "Verdict"],
  "rows": [
    ["72 vaccines required", "27 doses recommended", "FALSE"],
    ["Mandatory for all children", "Parents can decline", "FALSE"],
    ["No safety testing", "Decades of safety data", "FALSE"]
  ]
}
```

---

## Section Writing Guidelines

### Content Rules

1. **Inline citations**: Reference sources as `[N]` where N is the source ID
2. **Specific experts**: Never write "experts say" - name the expert and institution
3. **Evidence-first**: Lead with evidence, then analysis
4. **Neutral tone**: Present facts without editorializing

### Example Section

```json
{
  "heading": "What the CDC Actually Recommends",
  "content": "The CDC's official immunization schedule recommends 27 doses of vaccines by age 18 [1]. This includes multi-dose vaccines like DTaP (5 doses) and seasonal flu (annual) [2]. Dr. Amanda Cohn, Chief Medical Officer at CDC's National Center for Immunization, confirmed in January 2026 that 'the 72-dose figure circulating online conflates individual antigens with actual injections' [3].",
  "source_refs": [1, 2, 3]
}
```

---

## Why This Spread Section (Required for FALSE/MISLEADING)

### Purpose
Explain what made the misinformation believable. This shows fairness and helps readers understand the appeal.

### Structure
- What legitimate concern does it address?
- What kernel of truth (if any) was distorted?
- What made it emotionally compelling?

### Example

```json
{
  "why_this_spread": "The 72-vaccine claim resonates because parents genuinely worry about medical interventions for their children. The number sounds alarming and plays into broader concerns about pharmaceutical industry transparency. Additionally, the actual vaccine schedule IS more extensive than previous generations, which creates a factual foundation that gets distorted into misinformation."
}
```

---

## Batch Report Format

For multiple reports, wrap in a `reports` array with optional metadata:

```json
{
  "generated_date": "2026-01-15",
  "reports": [
    { /* Report 1 - full schema */ },
    { /* Report 2 - full schema */ },
    { /* Report 3 - full schema */ }
  ],
  "meta": {
    "media_polarization": {
      "partisan_sources": 65,
      "institutional_sources": 35
    },
    "aggregate_bot_density": 28,
    "source_credibility_distribution": {
      "score_5": 12,
      "score_4": 18,
      "score_3": 25,
      "score_2": 30,
      "score_1": 15
    }
  }
}
```

### Meta Fields (Aggregate Analytics)

| Field | Type | Description |
|-------|------|-------------|
| `meta.media_polarization` | object | % split between partisan vs institutional coverage |
| `meta.aggregate_bot_density` | number | Average bot amplification across all reports |
| `meta.source_credibility_distribution` | object | Distribution of source scores across all reports |

---

## Gemini Deep Research Prompt Template

Copy this to Gemini to generate properly formatted output:

```
Research these claims and produce a fact-check report. Return your findings as JSON.

CLAIMS TO RESEARCH:
1. [Claim 1]
2. [Claim 2]
...

For EACH claim, provide:
- 10-15 primary sources (NO Wikipedia) with verbatim quotes
- A clear verdict: FALSE, TRUE, MISLEADING, MIXED, or CONTEXT
- Full analysis organized into sections
- Data for visualizations if applicable

Return JSON in this exact format:

{
  "reports": [
    {
      "slug": "claim-name-2026",
      "title": "Full Title",
      "verdict": "FALSE",
      "category": "Category Name",
      "claim": {
        "text": "The exact claim",
        "claimant": "Who made it",
        "date_made": "When",
        "platform": "Where it spread"
      },
      "tldr": "2-3 sentence summary",
      "executive_summary": "3-5 sentence detailed summary",
      "sources": [
        {
          "id": 1,
          "title": "Source Title",
          "url": "https://...",
          "domain": "domain.com",
          "type": "GOV|NEWS|FACTCHECK|ORG|STUDY",
          "quote": "Verbatim quote"
        }
      ],
      "sections": [
        {
          "heading": "Section Title",
          "content": "Analysis with [N] citations",
          "source_refs": [1, 2]
        }
      ],
      "why_this_spread": "Why people believed it",
      "charts": [
        {
          "id": "chartId",
          "type": "bar|line|doughnut",
          "title": "Chart Title",
          "labels": ["A", "B"],
          "datasets": [{"label": "Data", "data": [10, 20], "color": "#ef4444"}]
        }
      ],
      "tables": [
        {
          "title": "Table Title",
          "headers": ["Col1", "Col2"],
          "rows": [["A", "B"]]
        }
      ]
    }
  ]
}

Categories: Fact Check, AI & Deepfakes, Health & Science, U.S. Politics & Policy, International, Economic & Financial, Conspiracy & Hoaxes, Platform & Tech

IMPORTANT:
- Minimum 10 sources per claim
- NO Wikipedia - use primary sources
- All quotes must be verbatim
- All URLs must be working
```

---

## Validation Checklist

Claude Code validates these before generating:

- [ ] Slug is URL-safe (lowercase, dashes only)
- [ ] Verdict is valid enum value
- [ ] Category is from standard list
- [ ] Minimum 8 sources
- [ ] All source URLs are accessible
- [ ] No Wikipedia URLs
- [ ] Executive summary present
- [ ] At least 2 content sections
- [ ] `why_this_spread` present for FALSE/MISLEADING
- [ ] Chart colors are from allowed palette (no purple)
- [ ] Source quotes are present

---

## Output

Claude Code will produce:

1. **HTML file**: `localreports/{slug}.html`
2. **Reports data entry**: Added to `js/reports-data.js`
3. **Sitemaps**: Updated `sitemap.xml` and `sitemap-news.xml`
4. **Vercel config**: Updated `vercel.json` with clean URL rewrite

---

*Last updated: January 15, 2026 — Added forensics fields, credibility scores, and meta analytics*
