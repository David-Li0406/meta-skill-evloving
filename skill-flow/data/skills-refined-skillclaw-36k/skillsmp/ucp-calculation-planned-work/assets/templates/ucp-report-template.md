# Use Case Points (UCP) Analysis Report
## [Project Name]

**Analysis Date:** [YYYY-MM-DD]
**Project Status:** [Planning/In Progress/Production]
**Analysis Method:** Use Case Points (UCP) v4.0 - Complete Work Coverage
**Technology Stack:** [Technologies]

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Unadjusted Actor Weight (UAW)** | [X] |
| **Unadjusted Use Case Weight (UUCW)** | [XXX] |
| **Total UUCP** | [XXX] |
| **TCF** | [X.XX] |
| **ECF** | [X.XX] |
| **Adjusted UCP** | [XXX] |
| **Realistic UCP (with framework leverage)** | [XXX] |
| **Estimated Hours** | [X,XXX-X,XXX] |

---

## 1. ACTOR SUMMARY TABLE

| Actor Type | Actor Name | Classification | Weight | Interaction Method | Justification |
|------------|------------|----------------|--------|-------------------|---------------|
| **Human Users** |
| | [Actor] | Simple/Average/Complex | 1/2/3 | [Method] | [Why] |
| **External Systems** |
| | [System] | Simple/Average/Complex | 1/2/3 | [Method] | [Why] |

**Actor Calculation:**
- Simple (×1): [X] × 1 = [X] UAW
- Average (×2): [X] × 2 = [X] UAW
- Complex (×3): [X] × 3 = [X] UAW
- **Total UAW = [X]**

---

## 2. WORK ITEM ANALYSIS (v4.0 Complete Coverage)

### 2A. NEW FUNCTIONALITY (Category 1: Stories & Features, 1.0x)

| UC ID | Work Item | Transactions | Complexity | Base UUCW | SAF | Final UUCW |
|-------|-----------|--------------|------------|-----------|-----|------------|
| UC-01 | [Name] | [X.X] | Simple/Avg/Complex | 5/10/15 | [0.XX] | [Base] × 1.0 × [0.7+0.3×SAF] = [X.X] |

**Category 1 Subtotal: [XXX.X] UUCW**

### 2B. ENHANCEMENTS (Category 2: Tasks, 0.6x)

| Task ID | Work Item | Transactions | Complexity | Base UUCW | SAF | Multiplier | Final UUCW |
|---------|-----------|--------------|------------|-----------|-----|------------|------------|
| T-01 | [Name] | [X.X] | Simple/Avg/Complex | 5/10/15 | [0.XX] | 0.6 | [X.X] |

**Category 2 Subtotal: [XXX.X] UUCW**

### 2C. MAINTENANCE (Category 3: Bugs, 0.4x)

| Bug ID | Work Item | Transactions | Complexity | Base UUCW | SAF | Urgency | Final UUCW |
|--------|-----------|--------------|------------|-----------|-----|---------|------------|
| B-01 | [Name] | [X.X] | Simple/Avg/Complex | 5/10/15 | [0.XX] | 1.0/1.2/1.5 | [X.X] |

**Category 3 Subtotal: [XXX.X] UUCW**

### 2D. QUALITY ASSURANCE (Category 4: Tests, 0.3x)

| Test ID | Work Item | Functionality | Base UUCW | Multiplier | Final UUCW |
|---------|-----------|---------------|-----------|------------|------------|
| TS-01 | [Name] | [What tested] | [X] | 0.3 | [X.X] |

**Category 4 Subtotal: [XXX.X] UUCW**

### 2E. WORK ITEM SUMMARY

| Category | Count | Base UUCW | After Multipliers | % of Total |
|----------|-------|-----------|-------------------|------------|
| Category 1: New Functionality | [X] | [XXX] | [XXX.X] | [XX]% |
| Category 2: Enhancements | [X] | [XXX] | [XXX.X] | [XX]% |
| Category 3: Maintenance | [X] | [XXX] | [XXX.X] | [XX]% |
| Category 4: Quality Assurance | [X] | [XXX] | [XXX.X] | [XX]% |
| **TOTAL UUCW** | **[XXX]** | **[XXX]** | **[XXX.X]** | **100%** |

---

## 3. SPECIFICITY ADJUSTMENT FACTOR (SAF)

**Average SAF for project:** [0.XX]

| SAF Range | Count | Percentage |
|-----------|-------|------------|
| High (≥0.8) | [X] | [XX]% |
| Good (0.6-0.8) | [X] | [XX]% |
| Moderate (<0.6) | [X] | [XX]% |

---

## 4. UUCP CALCULATION

```
UUCP = UAW + Total UUCW
UUCP = [X] + [XXX.X] = [XXX.X]
```

---

## 5. TECHNICAL COMPLEXITY FACTOR (TCF)

**TFactor = [XX.X]**
**TCF = 0.6 + (0.01 × [XX.X]) = [X.XX]**

[See references/tcf-factors.md for detailed breakdown]

---

## 6. ENVIRONMENTAL COMPLEXITY FACTOR (ECF)

**EFactor = [XX.X]**
**ECF = 1.4 + (-0.03 × [XX.X]) = [X.XX]**

---

## 7. UCP CALCULATION

```
Adjusted UCP = UUCP × TCF × ECF
Adjusted UCP = [XXX.X] × [X.XX] × [X.XX] = [XXX.X]

Realistic UCP = Adjusted UCP × Framework Leverage
Realistic UCP = [XXX.X] × [0.XX] = [XXX.X]
```

**Final UCP: [XXX]**

---

## 8. EFFORT ESTIMATION

**Productivity Factor:** [XX-XX] hours/UCP
**Estimated Total Hours:** [X,XXX - X,XXX]

---

## 9. KEY METRICS SUMMARY

| Metric | Value |
|--------|-------|
| Total Work Items | [XXX] |
| Actors Identified | [XX] |
| UUCP | [XXX.X] |
| TCF | [X.XX] |
| ECF | [X.XX] |
| **Final UCP** | **[XXX]** |
| **Estimated Hours** | **[X,XXX-X,XXX]** |

---

**Analysis Complete**
