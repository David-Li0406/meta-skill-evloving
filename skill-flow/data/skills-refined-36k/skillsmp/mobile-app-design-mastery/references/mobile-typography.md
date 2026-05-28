# Mobile Typography

Typography principles optimized for mobile readability.

---

## Mobile Type Scale

Tighter scale than web due to screen constraints.

| Size (sp/pt) | Use Case |
|--------------|----------|
| 11 | Captions, tertiary labels |
| 12 | Small labels, tab bar |
| 14 | Body text, default |
| 16 | Emphasized body, subtitles |
| 18-20 | Subheadings, card titles |
| 22-24 | Screen titles |
| 28-34 | Large titles (iOS style) |

**Minimum legible size:** 11sp (anything smaller is inaccessible)

---

## Font Weight

| Role | Weight |
|------|--------|
| Body | Regular (400) |
| Emphasis | Medium (500) |
| Headings | SemiBold (600) |
| Display | Bold (700) |

**Rule:** Don't use Light (300) on mobile—poor contrast on many screens.

---

## Line Height (Leading)

Mobile screens mean shorter line lengths, so line height can be tighter.

| Text Type | Line Height |
|-----------|-------------|
| Single line (labels) | 1.0-1.2 |
| Body text | 1.4-1.5 |
| Small captions | 1.3 |
| Headings | 1.1-1.2 |

---

## Letter Spacing (Tracking)

| Context | Adjustment |
|---------|------------|
| Large titles | Tighten (-0.5 to -1.5%) |
| All-caps labels | Widen (+5 to +10%) |
| Body text | Default (0) |

---

## Font Selection

**System fonts recommended:**

- iOS: SF Pro (or SF Compact for smaller sizes)
- Android: Roboto
- Cross-platform: System default, Inter, or Nunito Sans

**Custom fonts:**

- Ensure multiple weights available
- Test at 12sp—must be legible
- Load only needed weights (performance)

---

## Text Truncation

Mobile can't show everything. Handle overflow gracefully.

**Single line:** Ellipsis at end (`maxLines: 1, overflow: ellipsis`)

**Multi-line:** Fade out or "...more" expander

**Never:** Clip text without indication
