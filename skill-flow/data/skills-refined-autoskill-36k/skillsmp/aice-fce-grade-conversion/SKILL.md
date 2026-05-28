---
name: aice-fce-grade-conversion
description: "Converts international grades to US grades and credits for FCE reports. Triggered after PDF parsing to auto-fill grade conversion tables. Supports global grading systems with AI inference for unknown systems. Stores rules in Supabase for continuous learning."
---

# AICE FCE Grade Conversion

Convert international grades and credits to US equivalents based on AICE 2025 standards.

## When to Use

- After PDF parsing to convert extracted grades
- When filling grade conversion tables in reports
- When calculating US credits from foreign credit systems

## Core Logic

### Grade Conversion Flow
1. Query `aet_aice_grade_conversion_rules` table by country + grade
2. If found → use stored rule
3. If not found → AI inference with confidence marker
4. On report save → store AI-inferred rules for future use

### Output Format
```json
{
  "originalGrade": "85",
  "usGrade": "A",
  "gpaPoints": 4.0,
  "usCredits": 3.0,
  "level": "UD",
  "source": "AI_INFERRED"
}
```

AI-inferred grades display as: `A (AI_INFERRED)`

### Bilingual Format Rule
When displaying original data, preserve source language with format `{English (Original)}`:

| Field | Example |
|-------|---------|
| Institution | `Warsaw University of Technology (Politechnika Warszawska)` |
| Grade | `5.0 (very good)` / `4.5 (good plus)` / `3.0 (satisfactory)` |
| Program | `Computer Science (Informatyka)` |

## Credit Conversion

**Golden Rule**: 1 Academic Year = 30-32 US Semester Credits

| System | Conversion |
|--------|------------|
| ECTS (Europe) | 60 ECTS = 30 US Credits |
| CATS (UK) | 120 CATS = 30 US Credits |
| China | Normalize to 30/year |

**Rounding Rule**: Round US Credits to nearest 0.5
- 1.62 → 1.50
- 0.95 → 1.00
- 4.28 → 4.50
- 18.34 → 18.50

## Grade Scales

See [references/grade-rules.md](references/grade-rules.md) for country-specific tables.

## Course Level

| Year in 4-Year Program | Level |
|------------------------|-------|
| Year 1-2 | LD (Lower Division) |
| Year 3-4 | UD (Upper Division) |

## Database Table

```sql
aet_aice_grade_conversion_rules (
  country, education_level, original_scale,
  original_grade, us_grade, gpa_points,
  credit_coefficient, source, confidence
)
```

## Integration

**PDF Parsing**: Gemini prompt includes grade conversion instructions.
**Report Save**: AI-inferred rules are stored for future lookups.
