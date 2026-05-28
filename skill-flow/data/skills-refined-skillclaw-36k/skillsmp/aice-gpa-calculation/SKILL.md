---
name: aice-gpa-calculation
description: Calculate GPA and total credits for Foreign Credential Evaluation (FCE) reports. Use when calculating course statistics, processing grade data, or validating GPA calculations in credential evaluation contexts.
---

# AICE GPA Calculation

Calculate GPA and total credits for FCE course tables using AICE standards.

## Grade Points Scale

| Grade | Points | Notes |
|-------|--------|-------|
| A+ | 4.35 | Highest |
| A | 4.00 | |
| A- | 3.65 | |
| B+ | 3.35 | |
| B | 3.00 | |
| B- | 2.65 | |
| C+ | 2.35 | |
| C | 2.00 | |
| C- | 1.65 | |
| D+ | 1.35 | |
| D | 1.00 | |
| D- | 0.65 | |
| F / WF | 0.00 | Counts toward GPA |
| P / CR / T | — | Credit only, excluded from GPA |

## Calculation Rules

### GPA Formula

```
GPA = totalPoints / gpaCredits
```

- `totalPoints` = Sum of (credits × gradePoint) for graded courses
- `gpaCredits` = Sum of credits for graded courses only

### Credit Categories

1. **GPA Credits**: A through F grades (including WF)
2. **Total Credits**: All valid grades including P/CR/T
3. **Excluded**: Invalid or unrecognized grades

### Grade Normalization

- Uppercase and trim all grades
- Aliases: `FAIL` → `F`, `PASS` → `P`, `CREDIT` → `CR`

## Implementation Reference

See [references/gpa-rules.md](references/gpa-rules.md) for detailed implementation notes.
