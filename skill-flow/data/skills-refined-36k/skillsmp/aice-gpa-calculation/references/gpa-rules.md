# GPA Calculation Rules

Extracted from `lib/gpa.ts` implementation.

## Grade Points Definition

```typescript
const GRADE_POINTS: Record<string, number> = {
  "A+": 4.35,
  A: 4.0,
  "A-": 3.65,
  "B+": 3.35,
  B: 3.0,
  "B-": 2.65,
  "C+": 2.35,
  C: 2.0,
  "C-": 1.65,
  "D+": 1.35,
  D: 1.0,
  "D-": 0.65,
  F: 0.0,
  WF: 0.0,
};
```

## Normalization Aliases

```typescript
const ALIASES: Record<string, string> = {
  FAIL: "F",
  PASS: "P",
  CREDIT: "CR",
};
```

## Non-GPA Credits

Grades that count toward Total Credits but NOT GPA:

```typescript
const NON_GPA_CREDITS = new Set(["PASS", "Credit", "Transfer"]);
```

## Calculation Logic

1. **For each course**:
   - Parse credits (use `usCredits` if available, fallback to `credits`)
   - Normalize grade (uppercase, trim, apply aliases)
   - Add to `totalCredits` if valid

2. **GPA calculation**:
   - If grade is in `GRADE_POINTS`: add `credits × points` to `totalPoints`, add credits to `gpaCredits`
   - If grade is in `NON_GPA_CREDITS`: skip (already counted in totalCredits)
   - Final GPA: `gpaCredits > 0 ? totalPoints / gpaCredits : "N/A"`

## Input Parsing (Batch Mode)

When parsing raw course text:

1. Each line = one course
2. Format: `Course Name [TAB or SPACE] Credits [TAB or SPACE] Grade`
3. Split by TAB first; if not 3 parts, merge multiple spaces and split
4. Last field = grade
5. Scan backwards for first numeric field = credits
6. Only count if grade exists in `GRADE_POINTS`

## Display Grouping

- `F` and `WF` → display as `F/WF`
- `P` and `CR` → display as `P/CR`
- `T` → display separately
