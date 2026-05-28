# Analysis Document Templates

Templates for documenting subproblem analysis.

---

## Full Analysis Template

Use this for the main analysis document (`analysis-XX-X-function-name.md`):

```markdown
# Analysis: Subproblem XX.X - `function_name`

**Analyst:** [Your Name]
**Date:** [Month Year]
**Classification:** [MAJOR/MINOR]

---

## Quick Summary

| Aspect | Details |
|--------|---------|
| **Problem** | [Brief description] |
| **Domain** | [Physics/Chemistry/Math/Biology] |
| **Function** | `function_name(params)` |
| **Issue Found** | [One-line summary] |
| **Classification** | **[MAJOR/MINOR]** — [brief reason] |

---

## MAJOR OR MINOR ISSUE AND WHY

**Classification: [MAJOR/MINOR]**

**In plain terms:** [Explain the issue in accessible language]

### The Core Problem (Analogy)

[Use a relatable analogy for non-expert readers]

### Why This Cannot Be [Other Classification]

| Criteria | Assessment |
|----------|------------|
| **Key Question** | "Can an expert still produce correct code despite the issue?" |
| **Answer** | [Yes/No] — [explanation] |
| **Result** | [What happens when LLM tries to solve] |

---

## What's Wrong

[Clear problem statement with specific details]

| Component | What It Shows | Problem |
|-----------|---------------|---------|
| **[Component 1]** | [What it says] | [What's wrong] |
| **[Component 2]** | [What it says] | [What's wrong] |

**The Reviewer correctly identified this:** *"[Quote from reviewer]"*

---

## Components Changed

| Component | Changed? | What Was Changed |
|-----------|----------|------------------|
| **Subquestion Text** | [Yes/No] | [Description or "Already correct"] |
| **Function Header** | [Yes/No] | [Description or "Already correct"] |
| **Step Background** | [Yes/No] | [Description or "Already correct"] |
| **Test Cases** | [Yes/No] | [Description or "Already correct"] |

---

## The Fix

[For MAJOR only - describe the minimal fix]

**ORIGINAL:**
> [Original text/code]

**UPDATED:**
> [Fixed text/code]

---

## Why This Fix Works

1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

---

## Agreement with Reviewer

| Reviewer's Point | My Analysis |
|-----------------|-------------|
| "[Quote 1]" | Agreed — [your response] |
| "[Quote 2]" | Agreed — [your response] |

---

## Spreadsheet Submission

### Your Name
[Your Name]

### MAJOR OR MINOR ISSUE AND WHY

> [Copy-paste ready text for spreadsheet]

### Explain what change you made to the benchmark and why it solves the issue

> [Copy-paste ready text for spreadsheet - MAJOR only]

---

## Updated Subproblem (Complete Before/After)

### Updated [Component Name]

**ORIGINAL:**
> [Complete original text]

**UPDATED:**
> [Complete updated text]

*(Description of what changed)*
```

---

## Spreadsheet Submission Template

For the Google Spreadsheet columns:

### MAJOR Issue

**MAJOR OR MINOR ISSUE AND WHY:**
> MAJOR. [Issue description in 1-2 sentences]. This makes the problem impossible to solve as specified.
>
> This aligns with the Reviewer's assessment: *"[Brief quote]"*

**Explain what change you made:**
> **Change made to [Component]:**
>
> [Describe the minimal change]
>
> - Original: `[original]`
> - Updated: `[updated]`
>
> **Why this works:** [Brief explanation]

### MINOR Issue

**MAJOR OR MINOR ISSUE AND WHY:**
> MINOR. [Issue description]. However, an LLM with domain expertise would [know/use] [the correct approach] and still produce working code.
>
> This aligns with the Reviewer's assessment that the [core algorithm/method] is [clear/standard/well-known].

**Explain what change you made:**
> No changes needed. The issue is a [documentation gap/typo in non-critical value] that does not block correct implementation.

---

## Validation Test Template

For `validation_test.py`:

```python
#!/usr/bin/env python3
"""
SciCode Pilot: MAJOR/MINOR Classification Validation

Empirically validates classifications by implementing and testing functions.
"""

import numpy as np

SEP = "=" * 70

def print_section(title: str, subtitle: str = None) -> None:
    print("\n" + SEP)
    print(title)
    if subtitle:
        print(subtitle)
    print(SEP)


# =============================================================================
# TEST: XX.X - function_name (MAJOR/MINOR)
# =============================================================================

print_section(
    "TEST: Subproblem XX.X - function_name",
    "Classification: [MAJOR/MINOR] ([brief reason])",
)

# Implement EXACTLY as specified in the problem
def function_name(params):
    '''[Docstring from problem]'''
    # Implementation
    pass

# Test cases from problem
test_cases = [
    # (args, description)
]

# Run tests and report results
for args, description in test_cases:
    print(f"\n  Test: {description}")
    try:
        result = function_name(*args)
        print(f"  Result: {result}")
        print("  Status: PASSED")
    except Exception as e:
        print(f"  Error: {type(e).__name__} - {e}")
        print("  Status: FAILED (confirms MAJOR)")


# =============================================================================
# FINAL SUMMARY
# =============================================================================

print_section("FINAL VALIDATION SUMMARY")
print("- XX.X: [MAJOR/MINOR] confirmed ([brief evidence])")
```

---

## File Naming Convention

| File Type | Pattern | Example |
|-----------|---------|---------|
| Analysis | `analysis-XX-X-function-name.md` | `analysis-71-1-ket.md` |
| Validation | `validation_test.py` | Single file for all tests |
| Lessons | `LESSONS-LEARNED.md` | Project learnings |
| Alignment | `ALIGNMENT-REVIEW.md` | Cross-file consistency |
