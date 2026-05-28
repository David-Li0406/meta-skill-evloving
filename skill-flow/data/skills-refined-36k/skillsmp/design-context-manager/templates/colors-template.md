# Color System

## Brand Colors

### Primary
- **500 (Main):** `#[hex]`
- **50-950 Scale:** [Include full scale if available]
- **Usage:** Primary actions, key UI elements, links

### Secondary
- **500 (Main):** `#[hex]`
- **Usage:** Supporting elements, secondary actions

### Accent
- **500 (Main):** `#[hex]`
- **Usage:** Highlights, special emphasis, badges

## Neutral Scale

| Token | Value | Usage |
|-------|-------|-------|
| 50 | `#[hex]` | Backgrounds |
| 100 | `#[hex]` | Hover backgrounds |
| 200 | `#[hex]` | Borders, dividers |
| 300 | `#[hex]` | Disabled text |
| 400 | `#[hex]` | Placeholder text |
| 500 | `#[hex]` | Secondary text |
| 600 | `#[hex]` | Body text |
| 700 | `#[hex]` | Headings |
| 800 | `#[hex]` | High emphasis text |
| 900 | `#[hex]` | Maximum contrast |
| 950 | `#[hex]` | Near black |

## Semantic Colors

### Success
- **Background:** `#[hex]`
- **Foreground:** `#[hex]`
- **Border:** `#[hex]`
- **Usage:** Confirmations, completed states, positive feedback

### Warning
- **Background:** `#[hex]`
- **Foreground:** `#[hex]`
- **Border:** `#[hex]`
- **Usage:** Cautions, attention required, pending states

### Error
- **Background:** `#[hex]`
- **Foreground:** `#[hex]`
- **Border:** `#[hex]`
- **Usage:** Validation errors, destructive actions, failures

### Info
- **Background:** `#[hex]`
- **Foreground:** `#[hex]`
- **Border:** `#[hex]`
- **Usage:** Informational messages, tips, neutral alerts

## Surface Colors

### Backgrounds
| Token | Value | Usage |
|-------|-------|-------|
| Primary | `#[hex]` | Main page background |
| Secondary | `#[hex]` | Cards, elevated surfaces |
| Tertiary | `#[hex]` | Nested elements, inputs |
| Inverse | `#[hex]` | Dark sections on light theme |

### Foregrounds
| Token | Value | Usage |
|-------|-------|-------|
| Primary | `#[hex]` | Main text |
| Secondary | `#[hex]` | Supporting text |
| Tertiary | `#[hex]` | Subtle text, captions |
| Inverse | `#[hex]` | Text on inverse backgrounds |

## Border Colors

| Token | Value | Usage |
|-------|-------|-------|
| Default | `#[hex]` | Standard borders |
| Muted | `#[hex]` | Subtle dividers |
| Emphasis | `#[hex]` | Focus rings, selected states |

## Usage Guidelines

### Color Pairing
- Primary on white: [contrast ratio]
- Primary on dark: [contrast ratio]
- Always ensure 4.5:1 contrast for text

### State Variations
- **Hover:** Lighten by 10% or use next scale value
- **Active:** Darken by 10%
- **Disabled:** Reduce opacity to 50%

### Dark Mode
[Include if applicable]
- Surface colors invert
- Semantic colors adjust for dark backgrounds
- Maintain contrast ratios

---
_Source: [e.g., Extracted from tailwind.config.ts]_
_Last Updated: [Date]_
