---
name: analyze
description: Unified analysis skill - Python data analysis (--data) or KB gap identification (--kb)
---

# Analyze

## Overview

The analysis skill provides two modes for generating PM insights from structured sources:

| Mode | Purpose | Output |
|------|---------|--------|
| `--data` | Python-based analysis of CSV/Excel files (retention, funnel, segmentation) | `outputs/insights/data-analysis-YYYY-MM-DD.md` |
| `--kb` | Knowledge Base gap analysis (pain points, missing articles, AI opportunities) | `outputs/insights/kb-gaps-YYYY-MM-DD.md` |

## When to Use

### --data Mode
- User provides CSV, Excel, or structured data files
- User asks for "analysis", "insights", "metrics", "trends", or "charts"
- Data exists in `inputs/data/` folder
- User wants to understand product performance

### --kb Mode
- Have KB article exports to analyze
- Want to understand what users struggle with most
- Exploring AI assistant opportunities
- Planning documentation improvements

---

## Mode: --data

### Process

**Step 1: Choose Analysis Method**

Your goal is to provide the most accurate analysis. Autonomously select the best method based on the data and the user's query.

1.  **Examine the data source and the user's query.**
2.  **If** the data is simple (e.g., < 500 rows, clear headers) and the query is a straightforward aggregation (counting, sorting, grouping), you may perform the analysis **directly via LLM calculation**.
3.  **Else** (i.e., the analysis requires complex calculations, statistics, visualizations, or the data is large/complex), you **must** generate and execute a **Python script** to ensure accuracy.
4.  **When in doubt, default to using a Python script.**
5.  Announce which method you are choosing and why before proceeding with the analysis.

**Step 2: Execute Analysis**

---
***IF `Direct LLM Calculation` was chosen:***

1.  Read the content of the data file.
2.  Perform the requested calculations directly.
3.  Proceed to **Step 3**, ensuring all findings and claims are based on your direct calculations.

---
***IF `Python Script Execution` was chosen:***

1.  **Exploratory Data Analysis (EDA):** Write and execute a Python script to get basic info.
    ```python
    import pandas as pd
    # Load data, print shape, dtypes, head, describe, isnull, etc.
    ```
2.  **Data Dictionary:** Create a markdown table for the data dictionary. Ask the user to clarify any unknown column meanings before proceeding.
3.  **Analysis Plan:** Propose an analysis plan to the user.
4.  **Execution & Visualization:** Upon approval, write and execute the Python script to perform the analysis and generate any required visualizations (e.g., charts saved to `outputs/insights/`).
5.  Proceed to **Step 3**, ensuring all findings and claims are based on the Python script's output.

---

**Step 3: Generate Output**

Write to `outputs/insights/data-analysis-YYYY-MM-DD.md`. The output must be structured as follows and must include the `analysis_method` field in the YAML frontmatter.

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: analyze --data
analysis_method: "Direct LLM Calculation" # or "Python Script Execution"
sources:
  - inputs/data/filename.csv (modified: YYYY-MM-DD)
downstream: []
---

# Data Analysis: [Dataset Name]

## Analysis Method
This analysis was performed via **[Direct LLM Calculation / Python Script Execution]**.

## Dataset Overview
| Attribute | Value |
|-----------|-------|
| Rows | N |
| Columns | N |
| Date range | [if applicable] |

## Data Dictionary
| Column | Type | Example Values | Meaning |
|--------|------|----------------|---------|
| ... | ... | ... | Explicit/Unknown |

## Key Metrics
| Metric | Value | Source |
|--------|-------|--------|
| [Metric name] | [Number] | [Direct Calculation / Python output] |

## Findings
1. **[Finding]** - Evidence: [Direct Calculation / Python output]

## Hypotheses (require validation)
1. **[Hypothesis]** - Based on: [observation]

## Visualizations
- [Chart description]: outputs/insights/[filename].png

## Sources Used
- [file paths]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [Metric] | Evidence | [Direct Calculation / Python output] |
| [Trend interpretation] | Hypothesis | [Based on metric X] |
```

---

## Mode: --kb

### Process

**Step 1: Gather Sources**

Read files in:
- `inputs/knowledge_base/` - KB article exports
- `outputs/insights/voc-synthesis-*.md` - VOC insights (if available, for correlation)

**Step 2: Analyze Article Coverage**

For each KB article (or category), note:
- Topic / Category
- Article count
- Last updated date
- Estimated complexity (simple how-to vs. complex troubleshooting)

**Step 3: Identify Gaps**

Look for:
1. **High-volume topics** - Many articles = users struggle here
2. **Outdated articles** - Not updated in 6+ months
3. **Missing topics** - VOC mentions issues with no KB coverage
4. **Complex troubleshooting** - Multi-step processes that could be simplified

**Step 4: Assess AI Opportunities**

For each gap, evaluate:

| Opportunity Type | Criteria | Risk Level |
|------------------|----------|------------|
| Better search/IA | Hard to find articles | Low |
| Guided resolution | Multi-step process | Low-Medium |
| AI-assisted | Can be automated with citations | Medium |
| **DO NOT automate** | Compliance, billing, trust-sensitive | High |

**Step 5: Generate Output**

Write to `outputs/insights/kb-gaps-YYYY-MM-DD.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: analyze --kb
sources:
  - inputs/knowledge_base/*.md
  - outputs/insights/voc-synthesis-*.md (if used)
downstream:
  - outputs/roadmap/Qx-YYYY-charters.md
---

# KB Gap Analysis: [Date]

## Executive Summary
[2-3 sentences: What's the state of KB? Where are the biggest gaps?]

## Coverage Overview

| Category | Article Count | Last Updated | Complexity | Gap Score |
|----------|---------------|--------------|------------|-----------|
| [Category 1] | N | YYYY-MM-DD | Simple/Complex | High/Med/Low |

## High-Volume Topics
*Categories with most articles (signal: users struggle here)*

| Topic | Article Count | Sample Titles | VOC Correlation |
|-------|---------------|---------------|-----------------|
| [Topic] | N | [title1, title2] | [Yes/No/Unknown] |

## Missing / Outdated Articles

| Gap | Type | Evidence | Priority |
|-----|------|----------|----------|
| [Topic with no article] | Missing | VOC mentions in [file] | High |
| [Article X] | Outdated | Last updated [date] | Medium |

## AI Opportunity Assessment

### Safe to Automate (Low Risk)
| Opportunity | Type | Rationale |
|-------------|------|-----------|
| [Better search for X] | Search/IA | Articles exist but hard to find |
| [Guided wizard for Y] | Guided resolution | Clear steps, no judgment needed |

### Automate with Caution (Medium Risk)
| Opportunity | Type | Guardrails Needed |
|-------------|------|-------------------|
| [AI assist for Z] | AI-assisted | Must cite source article, human review |

### DO NOT Automate (High Risk)
| Topic | Reason |
|-------|--------|
| [Billing disputes] | Financial, requires human judgment |
| [Data deletion] | Compliance, irreversible |
| [Access control] | Trust/security sensitive |

## Recommendations
1. **[Recommendation]** - Evidence: [source]

## Sources Used
- [file paths]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [High volume in X] | Evidence | [article count] |
| [Users struggle with Y] | Evidence | [VOC file] |
```

---

## Quick Reference

### --data Mode

| Action | Command |
|--------|---------|
| Load CSV | `pd.read_csv('inputs/data/file.csv')` |
| Load Excel | `pd.read_excel('inputs/data/file.xlsx')` |
| Save chart | `plt.savefig('outputs/insights/output.png')` |
| Check nulls | `df.isnull().sum()` |

### --kb Mode

| Risk Level | Examples | Action |
|------------|----------|--------|
| Low | Search improvements, FAQ bots | Safe to build |
| Medium | Troubleshooting assistants | Build with guardrails |
| High | Billing, compliance, security | Human only |

---

## Common Mistakes

### --data Mode
- **Assuming column meanings:** "user_id probably means..." -> Ask user to confirm
- **Stating implications as facts:** "Users are churning because..." -> Label as hypothesis
- **Using sample data for conclusions:** "Based on 10 rows..." -> Ensure representative data
- **Ignoring missing data:** 50% nulls in key column -> Report this prominently
- **No data dictionary:** Jumping to analysis -> Always document columns first

### --kb Mode
- **Counting wrong:** "Many articles" -> Exact count: "47 articles"
- **Missing VOC correlation:** KB analysis in isolation -> Cross-reference with VOC
- **Underestimating risk:** "AI can handle billing" -> Compliance topics need humans
- **No priorities:** "Everything is a gap" -> Rank by impact
- **Stale analysis:** Using old VOC -> Check VOC synthesis date

---

## Verification Checklist

### --data
- [ ] Data dictionary created with all columns
- [ ] Unknown meanings explicitly marked
- [ ] User confirmed column semantics before analysis
- [ ] Metrics separated from hypotheses
- [ ] Missing data reported
- [ ] Charts saved to outputs/insights/
- [ ] All code executed successfully
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

### --kb
- [ ] All KB files read
- [ ] Article counts accurate
- [ ] Outdated articles identified (6+ months)
- [ ] VOC correlation checked (if available)
- [ ] AI opportunities categorized by risk
- [ ] DO NOT automate list includes compliance/billing/trust topics
- [ ] Recommendations backed by evidence
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

---

## Output Locations

| Mode | Primary Output | History |
|------|---------------|---------|
| `--data` | `outputs/insights/data-analysis-YYYY-MM-DD.md` | `history/analyze/data/` |
| `--kb` | `outputs/insights/kb-gaps-YYYY-MM-DD.md` | `history/analyze/kb/` |

---

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Metric] | Evidence | [Python output] |
| [Trend interpretation] | Hypothesis | [Based on metric X] |
| [Column meaning] | Evidence/Unknown | [User confirmed / Not stated] |
| [47 articles on X] | Evidence | [KB export count] |
| [Users complain about Y] | Evidence | [VOC file:line] |
| [Safe to automate Z] | Assumption | [no compliance concern identified] |
