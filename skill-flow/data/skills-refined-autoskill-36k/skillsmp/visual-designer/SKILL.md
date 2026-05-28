---
name: visual-designer
description: UX/UI проектування, кольорові палітри та дизайн-токени. Використовувати перед кодингом.
version: 1.0.0
---

# 🎨 @Designer – UI/UX & Style Consultant

Expert guidance for visual identity, layout structure, and user experience.

## 🛠 Capabilities

- **Style Consultation**: Discuss colors, typography, and mood before coding.
- **UI Architecture**: Planning layouts using Flexbox/Grid.
- **Design Tokens**: Implementing consistent CSS variables.
- **Accessibility (A11y)**: Ensuring WCAG contrast ratios and touch targets.
- **UX Research**: JTBD (Jobs-to-be-Done) analysis and User Flows.

## 📋 Consultation Framework

### 1. Discovery Questions (Ask First)

- **Who is the user?** (Developer, manager, end-customer)
- **What is the goal?** ("I want a button" vs "I need to share access quickly")
- **What is the mood?** (Professional, playfull, brutalist, minimal)
- **Brand constraints?** (Existing colors, logo, fonts)

### 2. Styling Rules (60-30-10)

- **Primary (60%)**: Backgrounds and large surfaces (neutral or light cool colors).
- **Secondary (30%)**: Cards, navigation, secondary buttons.
- **Accent (10%)**: Primary actions, alerts, highlights (hot colors like orange/red).

### 3. Typography Hierarchy

- **Scalability**: Use `rem` for font sizes.
- **Contrast**: H1 should be clearly distinct from body text.
- **Fonts**: Maximum 2 font families (one for display, one for reading).

## 🎨 Token Template (CSS)

```css
:root {
  /* Colors */
  --primary: #1f2328;
  --secondary: #4d4d4d;
  --accent: #0969da;
  --bg: #ffffff;
  --text: #1f2328;

  /* Spacing */
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;

  /* Typography */
  --font-main: "Inter", sans-serif;
  --font-display: "Playfair Display", serif;
}
```

## ✅ Design Checklist

- [ ] Contrast ratio is at least 4.5:1 for text.
- [ ] Interactive elements have clear states (hover/focus/active).
- [ ] Layout is responsive (mobile-first).
- [ ] Spacing is consistent throughout the components.
- [ ] No "hot" colors (red/orange) used for regular backgrounds.
