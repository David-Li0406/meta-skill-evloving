---
id: earned-value-management
name: "Earned Value Management (EVM)"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Earned Value Management (EVM)

## Metadata
- **Category:** Project Management Framework 7 - Measurement Performance Domain
- **Difficulty:** Advanced
- **Tags:** #product, #methodology, #pmbok
- **Read Time:** 10 min
- **Agent:** faion-pm-agent

---

## Problem

Traditional project tracking fails because:
- "We're 80% done" means nothing without context
- Spending on budget ≠ on track
- Schedule slip is hidden until too late
- No prediction of final cost/date

## Framework

### Core EVM Metrics

| Metric | Formula | Meaning |
|--------|---------|---------|
| **PV** (Planned Value) | Budget × % Planned | How much work should be done |
| **EV** (Earned Value) | Budget × % Complete | How much work is actually done |
| **AC** (Actual Cost) | Money spent | How much we've spent |

### Key Performance Indicators

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **SV** (Schedule Variance) | EV - PV | Positive = ahead, Negative = behind |
| **CV** (Cost Variance) | EV - AC | Positive = under budget, Negative = over |
| **SPI** (Schedule Performance Index) | EV / PV | >1 = ahead, <1 = behind |
| **CPI** (Cost Performance Index) | EV / AC | >1 = under budget, <1 = over |

### Forecasting Metrics

| Metric | Formula | Meaning |
|--------|---------|---------|
| **EAC** (Estimate at Completion) | BAC / CPI | Predicted final cost |
| **ETC** (Estimate to Complete) | EAC - AC | Cost to finish |
| **VAC** (Variance at Completion) | BAC - EAC | Expected final variance |
| **TCPI** (To-Complete Performance Index) | (BAC - EV) / (BAC - AC) | Required efficiency to finish on budget |

---

## Step-by-Step Guide

### Step 1: Establish Baseline

Create time-phased budget (Planned Value curve):

```
Month 1: $10,000 (10%)
Month 2: $25,000 (25%)
Month 3: $50,000 (50%)
Month 4: $75,000 (75%)
Month 5: $100,000 (100%)

BAC (Budget at Completion) = $100,000
```

### Step 2: Measure Progress

At each reporting period:
1. Assess actual % complete for each task
2. Calculate EV = BAC × % Complete
3. Track actual spending (AC)

### Step 3: Calculate Metrics

**Example at Month 3:**
- Planned: 50% complete, PV = $50,000
- Actual: 40% complete, EV = $40,000
- Spent: $55,000, AC = $55,000

```
SV = EV - PV = $40,000 - $50,000 = -$10,000 (behind schedule)
CV = EV - AC = $40,000 - $55,000 = -$15,000 (over budget)
SPI = EV / PV = 0.80 (20% behind schedule)
CPI = EV / AC = 0.73 (27% over budget)
```

### Step 4: Forecast Completion

```
EAC = BAC / CPI = $100,000 / 0.73 = $137,000
ETC = EAC - AC = $137,000 - $55,000 = $82,000 more needed
VAC = BAC - EAC = $100,000 - $137,000 = -$37,000 over budget
```

---

## Templates

### EVM Dashboard

```markdown
## EVM Report - [Project Name] - Month 3

### Key Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Budget at Completion (BAC) | $100,000 | - |
| Planned Value (PV) | $50,000 | - |
| Earned Value (EV) | $40,000 | - |
| Actual Cost (AC) | $55,000 | - |

### Variances

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Schedule Variance (SV) | -$10,000 | Behind schedule |
| Cost Variance (CV) | -$15,000 | Over budget |
| Schedule Performance Index (SPI) | 0.80 | 20% slower than planned |
| Cost Performance Index (CPI) | 0.73 | 27% more expensive |

### Forecasts

| Metric | Value | Meaning |
|--------|-------|---------|
| Estimate at Completion (EAC) | $137,000 | Predicted final cost |
| Estimate to Complete (ETC) | $82,000 | Cost to finish |
| Variance at Completion (VAC) | -$37,000 | Over budget by |

### Status: RED - Needs immediate attention
```

### EVM Trend Chart (Text)

```
$    BAC = $100K
     |
100K |                              . . . . PV
     |                      . . .'
 75K |                 . . '        x EAC forecast
     |           . . '        x
 50K |      . .'         x
     |    .'        x - - - - - - EV
 40K |   '     x
     | .'  x
     |x
     +----------------------------------------
      M1   M2   M3   M4   M5   M6
                     ↑
                  Current
```

---

## Examples

### Example 1: Simple EVM Calculation

**Project:** 10-page website, $10,000 budget, 10 weeks

Week 5 Status:
- Plan: 5 pages done (50%)
- Actual: 4 pages done (40%)
- Spent: $6,000

```
PV = $10,000 × 50% = $5,000
EV = $10,000 × 40% = $4,000
AC = $6,000

SPI = 4,000 / 5,000 = 0.80 (behind schedule)
CPI = 4,000 / 6,000 = 0.67 (over budget)

EAC = 10,000 / 0.67 = $14,925 predicted final cost

Action: Project will cost ~$5,000 more if trend continues
```

### Example 2: EVM for Solopreneurs

Simplified approach for solo projects:

```markdown
## Weekly EVM Check

**Project:** Online Course (40 hours planned, $4,000 value)

Week 2 of 4:
- Should be: 50% = 20 hrs done
- Actually: 30% = 12 hrs done
- Time spent: 15 hrs (my rate: $100/hr = $1,500 value)

PV = $2,000 (planned value)
EV = $1,200 (work completed value)
AC = $1,500 (time invested)

SPI = 0.60 (way behind)
CPI = 0.80 (inefficient)

Next steps:
- [ ] Cut scope to 80% of original
- [ ] Block 4-hr focus sessions daily
- [ ] Cancel non-essential meetings
```

---

## Common Mistakes

1. **Subjective % complete** - Use objective measures (milestones, units)
2. **Not updating baseline** - Re-baseline after approved scope changes
3. **Ignoring early warnings** - CPI rarely improves on its own
4. **Complex calculations** - Start simple: SPI and CPI tell the story
5. **No action on red metrics** - EVM is for decisions, not just reporting

---

## Related Methodologies

- **Cost Estimation:** Budget planning techniques
- **Change Control:** Managing baseline changes
- **Measurement Performance Domain:** Performance tracking framework

---

*Methodology from Project Management Framework 7 - Measurement Performance Domain*
