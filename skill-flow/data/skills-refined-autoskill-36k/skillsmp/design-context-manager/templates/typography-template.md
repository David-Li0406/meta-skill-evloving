# Typography

## Font Families

### Display / Headings
- **Font:** [Font name]
- **Stack:** `[Font name], [fallback], sans-serif`
- **Source:** [Google Fonts / Adobe / Local]
- **Weights:** [400, 500, 600, 700]

### Body
- **Font:** [Font name]
- **Stack:** `[Font name], [fallback], sans-serif`
- **Source:** [Google Fonts / Adobe / Local]
- **Weights:** [400, 500, 600]

### Mono (Code)
- **Font:** [Font name, e.g., JetBrains Mono]
- **Stack:** `[Font name], monospace`
- **Source:** [Google Fonts / Local]
- **Weights:** [400, 500]

## Type Scale

| Token | Size | Line Height | Letter Spacing | Weight |
|-------|------|-------------|----------------|--------|
| xs | 0.75rem (12px) | 1.5 | 0 | 400 |
| sm | 0.875rem (14px) | 1.5 | 0 | 400 |
| base | 1rem (16px) | 1.5 | 0 | 400 |
| lg | 1.125rem (18px) | 1.5 | -0.01em | 400 |
| xl | 1.25rem (20px) | 1.4 | -0.01em | 500 |
| 2xl | 1.5rem (24px) | 1.3 | -0.02em | 600 |
| 3xl | 1.875rem (30px) | 1.3 | -0.02em | 600 |
| 4xl | 2.25rem (36px) | 1.2 | -0.02em | 700 |
| 5xl | 3rem (48px) | 1.1 | -0.02em | 700 |
| 6xl | 3.75rem (60px) | 1.1 | -0.02em | 700 |
| 7xl | 4.5rem (72px) | 1.0 | -0.02em | 700 |

## Semantic Styles

### Headings

| Element | Size | Weight | Line Height | Family |
|---------|------|--------|-------------|--------|
| h1 | 3rem | 700 | 1.1 | Display |
| h2 | 2.25rem | 600 | 1.2 | Display |
| h3 | 1.875rem | 600 | 1.3 | Display |
| h4 | 1.5rem | 600 | 1.3 | Display |
| h5 | 1.25rem | 600 | 1.4 | Display |
| h6 | 1.125rem | 600 | 1.4 | Display |

### Body Text

| Style | Size | Weight | Line Height | Family |
|-------|------|--------|-------------|--------|
| body | 1rem | 400 | 1.5 | Body |
| bodySmall | 0.875rem | 400 | 1.5 | Body |
| caption | 0.75rem | 400 | 1.5 | Body |

### UI Text

| Style | Size | Weight | Letter Spacing | Family |
|-------|------|--------|----------------|--------|
| button | 0.875rem | 500 | 0.02em | Body |
| overline | 0.75rem | 600 | 0.1em | Body |
| label | 0.875rem | 500 | 0 | Body |

## Usage Guidelines

### Heading Hierarchy
- **h1:** Page titles, hero sections (one per page)
- **h2:** Major sections
- **h3:** Subsections
- **h4-h6:** Nested content, cards

### Body Text
- **body:** Default paragraph text
- **bodySmall:** Supporting text, metadata
- **caption:** Image captions, timestamps, helper text

### Line Length
- Optimal: 50-75 characters per line
- Max: 80 characters for comfortable reading
- Use `max-w-prose` or similar constraint

### Responsive Scaling
[If applicable]
- Mobile: Scale down headings by ~20%
- Use `clamp()` for fluid typography

---
_Source: [e.g., Extracted from layout.tsx font imports]_
_Last Updated: [Date]_
