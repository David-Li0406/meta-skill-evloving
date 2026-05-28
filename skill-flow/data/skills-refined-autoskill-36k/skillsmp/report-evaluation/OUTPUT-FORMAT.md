# Output Format

This document defines the exact structure for grading results output.

## GRADING-RESULTS.md Structure

### File Header

```markdown
# Grading Results - Assignment [N]

**Course:** [Course Name]
**Evaluated by:** Claude Code (3-reviewer consensus method)
**Date:** YYYY-MM-DD

---
```

### Per-Student Entry

Each evaluated student gets this exact structure:

```markdown
## [Student Full Name]

**Fil:** `lastname_firstname_originalname.pdf`

### Bedömning per avsnitt

| Avsnitt | Bedömning | Kommentar |
|---------|-----------|-----------|
| Sammanfattning | [Okej/Bra/Mycket bra/Utmärkt] | [Swedish comment] |
| Teknisk arkitektur | [Okej/Bra/Mycket bra/Utmärkt] | [Swedish comment] |
| Applikationsstack | [Okej/Bra/Mycket bra/Utmärkt] | [Swedish comment] |
| Säkerhet | [Okej/Bra/Mycket bra/Utmärkt] | [Swedish comment] |
| Riskmedvetenhet | [Okej/Bra/Mycket bra/Utmärkt] | [Swedish comment] |
| Processreflektion | [Okej/Bra/Mycket bra/Utmärkt] | [Swedish comment] |

### Betyg: **[Godkänt/Väl godkänt]** ([3/3] or [2/3])

### Återkoppling

[3-sentence feedback in Swedish, addressing student with "du/din"]

---
```

### Example Complete Entry

```markdown
## Anna Andersson

**Fil:** `andersson_anna_rapport_slutversion.pdf`

### Bedömning per avsnitt

| Avsnitt | Bedömning | Kommentar |
|---------|-----------|-----------|
| Sammanfattning | Bra | Tydlig översikt av projektets syfte och komponenter |
| Teknisk arkitektur | Mycket bra | Detaljerad NSG-förklaring med säkerhetsmotivering |
| Applikationsstack | Bra | Fungerande formulär demonstrerat med tydliga screenshots |
| Säkerhet | Mycket bra | Försvar på djupet med verifiering av blockerade anslutningar |
| Riskmedvetenhet | Bra | Relevanta risker med praktiska åtgärder |
| Processreflektion | Bra | Ärlig reflektion om AI-användning och iterativ utveckling |

### Betyg: **Väl godkänt (VG)** (3/3)

### Återkoppling

Riktigt snyggt jobbat med säkerhetsverifieringen - du testade både vad som tillåts och vad som blockeras! Din arkitekturdokumentation är tydlig och visar att du förstår hur alla komponenter hänger ihop. Roligt att läsa en rapport med personlig touch som ändå håller tekniskt.

---
```

### Summary Table (End of File)

After all students, add summary table:

```markdown
# Sammanfattning

| Student | Betyg | Sammanfattning | Arkitektur | Appstack | Säkerhet | Risk | Reflektion |
|---------|-------|----------------|------------|----------|----------|------|------------|
| Andersson, Anna | VG (3/3) | Bra | Mycket bra | Bra | Mycket bra | Bra | Bra |
| Eriksson, Erik | G (2/3) | Okej | Bra | Bra | Bra | Okej | Bra |
| Johansson, Johan | VG (3/3) | Bra | Bra | Mycket bra | Utmärkt | Bra | Mycket bra |

## Statistik

- **Totalt utvärderade:** X
- **Väl godkänt (VG):** Y
- **Godkänt (G):** Z
- **Enhälliga beslut (3/3):** N
- **Majoritetsbeslut (2/3):** M
```

## STUDENT-LIST.md Updates

After evaluation, update the Betyg column:

### Before Evaluation

```markdown
| Full Name | File Prefix | Report Submitted | Betyg |
|-----------|-------------|------------------|-------|
| Anna Andersson | `andersson_anna` | Yes | |
| Erik Eriksson | `eriksson_erik` | Yes | |
| Johan Johansson | `johansson_johan` | No | |
```

### After Evaluation

```markdown
| Full Name | File Prefix | Report Submitted | Betyg |
|-----------|-------------|------------------|-------|
| Anna Andersson | `andersson_anna` | Yes | VG (3/3) |
| Erik Eriksson | `eriksson_erik` | Yes | G (2/3) |
| Johan Johansson | `johansson_johan` | No | - |
```

## Vote Count Format

| Pattern | Meaning | Display |
|---------|---------|---------|
| 3 agree | Unanimous | `(3/3)` |
| 2 agree VG | Majority VG | `(2/3)` |
| 2 agree G | Majority G | `(2/3)` |
| Split | No majority | `(split)` |

## Terminal Output Format

After each student evaluation, display:

```
## Anna Andersson - Evaluation Complete

| Reviewer | Grade | Key Observation |
|----------|-------|-----------------|
| 1 | VG | Strong security with NSG verification |
| 2 | VG | Excellent architecture documentation |
| 3 | VG | Defense-in-depth approach |

**Final Grade: VG (3/3 unanimous)**

✓ Saved to GRADING-RESULTS.md
✓ Updated STUDENT-LIST.md
```

For split decisions:

```
## Erik Eriksson - Evaluation Complete

| Reviewer | Grade | Key Observation |
|----------|-------|-----------------|
| 1 | VG | Good security implementation |
| 2 | G | Security meets minimum only |
| 3 | G | Basic verification shown |

**Final Grade: G (2/3 majority)**

⚠ Split decision: 1 reviewer gave VG

✓ Saved to GRADING-RESULTS.md
✓ Updated STUDENT-LIST.md
```

## Section Comment Guidelines

Keep comments concise (under 10 words) and in Swedish:

| Section | Good Example | Too Long |
|---------|--------------|----------|
| Sammanfattning | "Tydlig översikt" | "Studenten ger en tydlig översikt av projektets syfte..." |
| Teknisk arkitektur | "Detaljerad NSG-förklaring" | "Arkitekturen är väl dokumenterad med detaljerade NSG-regler..." |
| Säkerhet | "Försvar på djupet" | "Visar försvar på djupet med flera säkerhetslager..." |

## Privacy Note

GRADING-RESULTS.md contains:
- Student names
- Grades
- Individual feedback

Must be protected:
- Add to `.gitignore`
- Never commit to public repositories
- Share only with authorized instructors
- Delete after course completion
