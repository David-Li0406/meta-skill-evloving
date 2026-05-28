---
name: analysis-report
description: Write data analysis reports where all quantitative information appears in programmatically-generated plots, never in hand-written text tables. Prevents AI from fabricating numbers by ensuring all values come from computed data rendered visually. Use when creating analysis reports, generating summary statistics, or presenting correlation/comparison results.
---

# Analysis Report Writing

Rules for AI-generated analysis reports that prevent number fabrication.

## The Problem

When generating analysis reports, AI can:
1. **Make up numbers** instead of computing them from data
2. **Write tables with fabricated values** that don't match actual analysis
3. **Make interpretive claims** not grounded in computed results

## The Solution: Plots Only, No Text Tables

**Core Principle: If it's quantitative, it must be in a plot.**

All quantitative information must be rendered as plots generated directly from data.

### Why This Works

1. **Plots are generated programmatically** - plotting code reads from data files
2. **No hand-written numbers** - eliminates fabrication
3. **Source of truth is the data** - not AI "memory" or guesses

## Report Structure Rules

### DO:
- Use headings and prose to explain what a plot shows
- Reference plots with `![Caption](plots/filename.png)`
- Keep interpretive text minimal and qualitative
- Let the plots speak with their embedded values

### DON'T:
- Write tables with numbers (use bar charts instead)
- Quote specific correlation values in prose
- Make quantitative claims not visible in a plot
- Summarize plot data in text form

### Example - BAD:
```markdown
The correlation matrix shows:
| A-B | 0.93 |
| A-C | 0.55 |
```

### Example - GOOD:
```markdown
The correlation matrix:
![Pairwise Correlations](plots/biomarker_pairwise.png)
```

## Plot Design Guidelines

Each plot should be self-documenting:

1. **Include values on the plot** - bar labels, coefficients in titles
2. **Add context lines** - reference lines (y=0, y=1.0, thresholds)
3. **Use color coding** - positive/negative, above/below threshold
4. **Show sample size** - n= in titles or labels
5. **Add stats boxes** - mean, std, n for distributions

## Implementation Pattern

```
analysis.py
  → reads from data source (cached)
  → computes statistics
  → saves to results/*.csv
  → generates plots/*.png from the data
  → report.md references only the plots
```

## File Structure

```
analysis/{name}/
├── analysis.py          # Main script - generates everything
├── scripts/             # Modular functions
│   ├── __init__.py
│   ├── data.py          # Data fetching
│   ├── compute.py       # Calculations
│   └── plotting.py      # All plot functions
├── results/             # CSV outputs
├── plots/               # PNG outputs
└── report.md            # References plots only
```

## Verification Checklist

Before finalizing a report:

- [ ] Run the analysis script to regenerate all plots
- [ ] Verify report contains ONLY plot references, no text tables
- [ ] Check that all claims in prose are visible in referenced plots
- [ ] Confirm no specific numbers are written in prose

## When to Use This Skill

**Use when:**
- Creating data analysis reports
- Generating summary statistics
- Presenting correlation or comparison results
- Building dashboards or visualizations from data

**Key trigger phrases:**
- "write an analysis report"
- "summarize these results"
- "create a report from this data"
- "show the correlations between..."
