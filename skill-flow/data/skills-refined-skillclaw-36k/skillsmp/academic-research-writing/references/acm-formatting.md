# ACM Paper Formatting Specifications

Complete formatting guide based on ACM conference/journal paper template.

## Page Setup

### Page Size and Orientation
- **Size**: US Letter (8.5" x 11") or A4 (210mm x 297mm)
- **Orientation**: Portrait

### Margins
- **Top**: 1 inch (25.4mm)
- **Bottom**: 1 inch (25.4mm)
- **Left**: 0.75 inch (19.05mm)
- **Right**: 0.75 inch (19.05mm)

### Column Layout
- **Abstract**: Single column
- **Body**: Two columns
- **Column separation**: 0.33 inches (8.38mm)

## Typography

### Font Family
- **Primary**: Libertine (Linux Libertine)
- **Monospace**: Inconsolata or Courier
- **Fallback**: Times New Roman acceptable

### Font Sizes and Styles

| Element | Size | Weight | Notes |
|---------|------|--------|-------|
| Title | 17pt | Bold | Left-aligned |
| Subtitle | 14pt | Regular | Left-aligned |
| Author Names | 12pt | Regular | Left-aligned |
| Author Affiliations | 10pt | Regular | Email in monospace |
| Abstract | 10pt | Regular | Single column, justified |
| CCS Concepts | 9pt | Regular | Bulleted hierarchy |
| Keywords | 9pt | Regular | Comma-separated |
| Section Headings (L1) | 11pt | Bold | Title Case |
| Subsection (L2) | 10pt | Bold | Title Case |
| Sub-subsection (L3) | 10pt | Italic | Title Case |
| Body Text | 10pt | Regular | Justified |
| Figure Captions | 9pt | Regular | "Figure X:" in bold |
| Table Captions | 9pt | Regular | "Table X:" in bold |
| References | 9pt | Regular | Hanging indent |

## Document Structure

### Front Matter (Single Column)
1. Title
2. Subtitle (optional)
3. Authors and affiliations
4. Abstract
5. CCS Concepts
6. Keywords
7. ACM Reference Format

### Body (Two Columns)
8. Main content sections
9. Acknowledgments
10. References

## Required Sections

### CCS Concepts
```
CCS CONCEPTS
- Human-centered computing -> Ubiquitous and mobile computing;
- Software and its engineering -> Context specific languages.
```

### Keywords
```
KEYWORDS
context-awareness, ubiquitous computing, adaptation, personalization
```

### ACM Reference Format
```
ACM Reference Format:
John Smith and Jane Doe. 2025. Title of Paper. In Proceedings of
Conference Name (CONF '25), Month Day-Day, Year, City, Country.
ACM, New York, NY, USA, XX pages. https://doi.org/10.1145/XXXXXX.XXXXXX
```

## Citations and References

### In-Text Citations
Format: [1], [2, 3, 4]

### Reference Formats

**Journal article:**
```
[1] Author1 Name, Author2 Name, and Author3 Name. Year.
    Title of article. Journal Name Volume, Issue (Month Year),
    pages. DOI:10.1145/XXXXXXX
```

**Conference paper:**
```
[2] Author1 Name and Author2 Name. Year. Title of paper.
    In Proceedings of Conference Name (CONF 'YY), Month,
    City, Country. ACM, New York, NY, USA, pages.
    DOI:10.1145/XXXXXXX
```

**Key difference from IEEE:** Full first and last names (not initials)

## LaTeX Document Classes

| Type | Class |
|------|-------|
| Conference proceedings | `\documentclass[sigconf]{acmart}` |
| SIGPLAN proceedings | `\documentclass[sigplan]{acmart}` |
| Small journal | `\documentclass[acmsmall]{acmart}` |
| Large journal | `\documentclass[acmlarge]{acmart}` |

## Submission Checklist

- [ ] Correct document class for publication type
- [ ] Title and subtitle properly formatted
- [ ] All authors and affiliations included
- [ ] Abstract 150-250 words
- [ ] CCS Concepts section included
- [ ] Keywords section included (4-8 keywords)
- [ ] ACM Reference Format section included
- [ ] Two-column layout for body
- [ ] All section headings numbered correctly
- [ ] All figures have captions below
- [ ] All tables have captions above
- [ ] Full author names in references (not initials)
- [ ] DOIs included when available
- [ ] All fonts embedded in PDF

## Resources

- ACM Author Center: https://authors.acm.org/
- ACM Templates: https://www.acm.org/publications/proceedings-template
- ACM CCS Generator: https://dl.acm.org/ccs
