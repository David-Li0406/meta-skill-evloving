---
name: brand-guidelines
description: 'Apply brand colors, typography, và style guidelines cho artifacts. Sử dụng khi cần brand identity, visual formatting, company design standards, corporate styling.'
---

# Brand Guidelines Skill

Skill này cung cấp brand identity và style resources. Áp dụng cho artifacts cần consistent brand look-and-feel.

## Khi Nào Sử Dụng

- Apply brand colors/typography
- Visual formatting theo brand
- Corporate identity styling
- Consistent design standards
- Post-processing artifacts

---

## Default Brand Template

### Colors

**Main Colors:**
| Color | Hex | Usage |
|-------|-----|-------|
| Dark | `#141413` | Primary text, dark backgrounds |
| Light | `#faf9f5` | Light backgrounds, text on dark |
| Mid Gray | `#b0aea5` | Secondary elements |
| Light Gray | `#e8e6dc` | Subtle backgrounds |

**Accent Colors:**
| Color | Hex | Usage |
|-------|-----|-------|
| Orange | `#d97757` | Primary accent, CTAs |
| Blue | `#6a9bcc` | Secondary accent, links |
| Green | `#788c5d` | Tertiary accent, success |

### Typography

| Type | Font | Fallback |
|------|------|----------|
| Headings | Poppins | Arial |
| Body Text | Lora | Georgia |

---

## CSS Variables Template

```css
:root {
  /* Main Colors */
  --brand-dark: #141413;
  --brand-light: #faf9f5;
  --brand-mid-gray: #b0aea5;
  --brand-light-gray: #e8e6dc;
  
  /* Accent Colors */
  --brand-orange: #d97757;
  --brand-blue: #6a9bcc;
  --brand-green: #788c5d;
  
  /* Typography */
  --font-heading: 'Poppins', Arial, sans-serif;
  --font-body: 'Lora', Georgia, serif;
}
```

---

## Application Guidelines

### Headings
```css
h1, h2, h3 {
  font-family: var(--font-heading);
  color: var(--brand-dark);
  font-weight: 600;
}
```

### Body Text
```css
body, p {
  font-family: var(--font-body);
  color: var(--brand-dark);
  line-height: 1.6;
}
```

### Buttons (Primary)
```css
.btn-primary {
  background: var(--brand-orange);
  color: var(--brand-light);
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
}
```

### Buttons (Secondary)
```css
.btn-secondary {
  background: transparent;
  color: var(--brand-dark);
  border: 2px solid var(--brand-mid-gray);
}
```

### Links
```css
a {
  color: var(--brand-blue);
  text-decoration: none;
}
a:hover {
  color: var(--brand-orange);
}
```

---

## Custom Brand Setup

Khi cần brand riêng, thu thập:

### Required Information

| Element | Details Needed |
|---------|----------------|
| Logo | URL hoặc description |
| Primary Color | Hex code |
| Secondary Colors | Hex codes |
| Heading Font | Font name |
| Body Font | Font name |
| Tone | Professional, playful, etc. |

### Brand Definition Template

```yaml
brand_name: "[Company Name]"
colors:
  primary: "#XXXXXX"
  secondary: "#XXXXXX"
  accent: "#XXXXXX"
  background: "#XXXXXX"
  text: "#XXXXXX"
typography:
  heading: "[Font Name]"
  body: "[Font Name]"
tone: "[professional/playful/modern/classic]"
```

---

## Quick Reference

### Color Contrast Guidelines

| Background | Text | Accent |
|------------|------|--------|
| Light (#faf9f5) | Dark (#141413) | Orange (#d97757) |
| Dark (#141413) | Light (#faf9f5) | Blue (#6a9bcc) |
| Mid Gray (#b0aea5) | Dark (#141413) | Green (#788c5d) |

### Font Pairing Rules

| Heading | Body | Vibe |
|---------|------|------|
| Poppins | Lora | Modern + Classic |
| Montserrat | Open Sans | Clean + Readable |
| Playfair Display | Lato | Elegant + Friendly |

---

**Note**: Fonts should be pre-installed hoặc imported từ Google Fonts for best results.
