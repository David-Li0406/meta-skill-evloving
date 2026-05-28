---
name: cgi-brand-stylist
description: Applies CGI branding guidelines, color palettes, and typography to UI components. Use this whenever generating CSS, Tailwind classes, or charting configurations.
---

# CGI Brand Stylist

You are the guardian of the CGI visual identity.

## Color Palette

| Role           | Hex       | Usage                                                             |
| -------------- | --------- | ----------------------------------------------------------------- |
| **CGI Red**    | `#E31937` | Primary actions, critical alerts, key data points. Use sparingly. |
| **Deep Blue**  | `#005288` | Trust indicators, positive trends, secondary actions              |
| **Slate Gray** | `#5A5B5D` | Neutral text, grid lines, labels                                  |
| **White**      | `#FFFFFF` | Primary backgrounds                                               |
| **Light Gray** | `#F5F5F5` | Secondary backgrounds, cards                                      |

## Design Rules

1. **Never** use generic traffic light patterns (green/red). Use Blue for positive, CGI Red for negative.
2. **Never** use gradients for data visualization unless representing continuous heatmaps.
3. **Always** enforce WCAG AA accessibility (4.5:1 contrast ratio minimum).
4. **Always** use Z-pattern layout: KPIs top-left, context top-right, details center/bottom.
5. **Always** use generous whitespace—avoid chart junk (3D effects, excessive grid lines).

## Typography

- **Headers**: Inter or Roboto, Bold
- **Body**: Inter or Roboto, Regular
- **Data**: Roboto Mono for numbers

## Chart Styling

```javascript
const CGI_COLORS = {
  primary: "#E31937",
  secondary: "#005288",
  neutral: "#5A5B5D",
  background: "#FFFFFF",
  surface: "#F5F5F5",
};
```
