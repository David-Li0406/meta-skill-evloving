---
name: frontend-design-complete
description: Create distinctive, production-grade frontend interfaces with high design quality AND comprehensive mobile responsiveness. Combines aesthetic guidelines with mobile-first patterns, form consistency, and color contrast rules. Use this as your single frontend design skill.
version: 1.0.0
author: Design Styles Explorer Project
updated: 2025-01-11
---

# Complete Frontend Design Guidelines

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics while ensuring proper mobile responsiveness and cross-element consistency.

---

## Part 1: Design Thinking & Aesthetics

### Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail
- **Fully mobile responsive** (see Part 2)

### Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

### AI Slop Patterns to Avoid

These specific patterns have become telltale signs of AI-generated design. Avoid them:

**Colors:**
- Cream/off-white backgrounds (`#f8f6f3`, `#fdfcfb`, `#faf8f5` type colors)
- Terracotta/coral/rust accents (`#c45c48`, `#e07860`, `#d4715f`, `#bf4a37`)
- Orange and teal combinations
- Purple/blue gradients on white backgrounds
- Warm shadows with colored tints

**Layout & Components:**
- Generous rounded corners (12-16px+ border-radius)
- Left-border accent lines on cards (the colored vertical stripe)
- Pill-shaped tabs and buttons
- Cards with subtle warm shadows and hover lift effects
- Overly "friendly" and "approachable" feeling

**Visual Effects:**
- Texture overlays (noise, grain, paper textures)
- Glow effects and colored shadows
- Gradient backgrounds with warm color temperature
- Soft, diffused aesthetic everywhere

**Overall Aesthetic:**
- The "cozy webapp" look - warm, soft, inviting
- Designs that feel like Notion/Linear clones
- Safe, inoffensive, "premium but accessible" feeling
- Lack of sharp contrast or bold decisions

Instead, make distinctive choices: cooler color temperatures, sharper geometry, unexpected color combinations, higher contrast, or commit fully to a specific design tradition (Swiss, Japanese, Brutalist, Editorial, etc.) rather than the generic "modern SaaS" look.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

---

## Part 2: Mobile-First Responsive Patterns

### Hero Sections

**Problem**: 2-column grid layouts leave empty space when one column is hidden on mobile.

```css
/* Desktop: 2-column grid */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;
}

/* Mobile: Switch to centered flex */
@media (max-width: 768px) {
  .hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 40px 20px;
    gap: 24px;
  }

  .hero-content {
    align-items: center;
  }

  .hero-badge {
    align-self: center;
  }

  .hero-title {
    font-size: 32px;
    text-align: center;
  }

  .hero-subtitle {
    font-size: 14px;
    text-align: center;
  }

  .hero-cta {
    flex-direction: column;
    align-items: center;
    width: 100%;
  }

  .hero-cta .btn {
    width: 100%;
    max-width: 280px;
  }

  .hero-visual {
    display: none;
  }
}
```

**Key Rule**: When hiding grid columns on mobile, switch from `display: grid` to `display: flex` to eliminate reserved empty space.

### Large Selection Lists (Accordion Pattern)

**Problem**: Horizontal scroll for many items (20+) is unusable on mobile - text gets cut off.

**Solution**: Use collapsible accordion with category headers.

```jsx
function StyleSelector({ items, categories }) {
  const [expandedCategory, setExpandedCategory] = useState(null);

  return (
    <div className="selector">
      {categories.map(category => (
        <div key={category.name} className={`category ${expandedCategory === category.name ? 'expanded' : ''}`}>
          <button
            className="category-header"
            onClick={() => setExpandedCategory(
              expandedCategory === category.name ? null : category.name
            )}
          >
            <span>{category.name}</span>
            <ChevronIcon />
          </button>
          <div className="category-items">
            {category.items.map(item => (
              <button key={item.id} className="item">{item.name}</button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```

```css
@media (max-width: 768px) {
  .category-items {
    display: none;
  }

  .category.expanded .category-items {
    display: flex;
    flex-direction: column;
  }

  .chevron-icon {
    transition: transform 0.2s ease;
  }

  .category.expanded .chevron-icon {
    transform: rotate(180deg);
  }
}
```

### Form Layouts

**Problem**: Multi-column form layouts get cut off on mobile.

```css
.form-row {
  display: flex;
  gap: 16px;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }

  .form-group {
    width: 100%;
  }
}
```

### Status/Alert Cards

**Problem**: Inconsistent text alignment when stacking horizontally-laid elements vertically.

```css
.alert {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

@media (max-width: 768px) {
  .alert {
    flex-direction: column;
    align-items: center;  /* Center the flex items */
    text-align: center;   /* Center the text within items */
    gap: 8px;
  }

  .alert strong {
    text-align: center;  /* Explicit for block elements */
  }
}
```

**Key Rule**: Stacked flex items need BOTH `align-items: center` AND `text-align: center` for proper centering.

### Grid Layouts

```css
@media (max-width: 768px) {
  .pricing-grid,
  .feature-grid,
  .team-grid,
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
```

### Breakpoint Reference

```css
/* Tablet - Stack sidebars, maintain content width */
@media (max-width: 1200px) { }

/* Mobile - Full single-column, centered hero */
@media (max-width: 768px) { }

/* Small Mobile - Compact spacing, reduced font sizes */
@media (max-width: 480px) { }
```

### Mobile Font Scaling

```css
@media (max-width: 768px) {
  .hero-title {
    font-size: 32px;  /* Down from ~48px */
  }

  .section-title {
    font-size: 24px;  /* Down from ~32px */
  }

  .section-subtitle {
    font-size: 14px;  /* Down from ~16px */
  }
}
```

---

## Part 3: Form Element Consistency

### Always Style as a Group

**Problem**: Styling only `.input` leaves `.select` and `.textarea` unstyled.

```css
/* WRONG - Only targets input */
.style-brutalist .input {
  border: 2px solid var(--border);
  border-radius: 0;
}

/* CORRECT - Targets all form fields */
.style-brutalist .input,
.style-brutalist .select,
.style-brutalist .textarea {
  border: 2px solid var(--border);
  border-radius: 0;
}
```

### Textarea Border Radius Exceptions

Pill-shaped inputs (border-radius: 100px) look wrong on textareas:

```css
.style-kawaii .input,
.style-kawaii .select {
  border-radius: 100px;
}

/* Textarea needs smaller radius */
.style-kawaii .textarea {
  border-radius: 20px;
}
```

### Dropdown Option Styling

`<option>` elements can't inherit backdrop-filter or complex backgrounds:

```css
.style-glassmorphism .select {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
}

/* Options need solid backgrounds */
.style-glassmorphism .select option {
  background: #1a1a2e;
  color: white;
}
```

### Transparent Border Styles (Neomorphism, Claymorphism)

**Problem**: Styles with `border: transparent` make form controls invisible.

```css
/* These styles use transparent borders */
.style-neomorphism .radio-mark,
.style-claymorphism .radio-mark {
  border: 2px solid #B8BEC7;  /* Add visible border */
  background: var(--bg-primary);
  box-shadow: inset 2px 2px 4px rgba(163,177,198,0.3),
              inset -2px -2px 4px rgba(255,255,255,0.8);
}
```

---

## Part 4: Color Contrast Rules

### Badge/Pill Elements

Always verify badge text contrasts with its background:

```css
/* WRONG - May be invisible on light backgrounds */
.badge {
  color: white;
}

/* CORRECT - Uses semantic variable */
.badge {
  color: var(--bg-primary);  /* Inverts with background */
}
```

### Color Swatches Display

Swatches showing colors need visible borders regardless of swatch color:

```css
.color-swatch {
  border: 2px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.3);
}
```

### Dark Theme Form Labels

**Problem**: Assuming labels should be white/light on dark themes.

```css
/* WRONG - Hardcoded color */
.label {
  color: white;
}

/* CORRECT - Uses semantic variable */
.label {
  color: var(--text-primary);
}
```

---

## Pre-Implementation Checklist

Before finalizing any frontend design, verify:

### Aesthetics
- [ ] Committed to a bold, distinctive aesthetic direction
- [ ] Avoided AI slop patterns (cream backgrounds, terracotta accents, purple gradients)
- [ ] Used distinctive typography (not Inter, Roboto, Arial)
- [ ] Created cohesive color palette with CSS variables

### Mobile Responsiveness
- [ ] Hero section centers on mobile (not left-aligned with empty space)
- [ ] Grid layouts collapse to single column on mobile
- [ ] Large selection lists use accordion on mobile (not horizontal scroll)
- [ ] Status/alert cards center properly on mobile
- [ ] Font sizes scale appropriately for mobile

### Form Elements
- [ ] All form fields (input, select, textarea) styled consistently
- [ ] Radio buttons and checkboxes visible (especially for transparent-border styles)
- [ ] Dropdown options have readable backgrounds
- [ ] Textarea has appropriate border-radius (not pill-shaped)

### Color Contrast
- [ ] Labels use semantic color variables (not hardcoded)
- [ ] Badge/pill text contrasts with background
- [ ] Color swatches have visible borders
- [ ] Dark theme elements properly contrasted

---

## Common Issues Quick Reference

| Issue | Cause | Fix |
|-------|-------|-----|
| Hero left-aligned with empty space | Grid reserves hidden column | Switch to flex on mobile |
| Form fields cut off | Fixed-width grid | Stack vertically with flex |
| Inconsistent alert alignment | Missing align-items | Add `align-items: center` + `text-align: center` |
| Invisible form controls | Transparent borders | Add explicit borders or shadows |
| White text on light background | Hardcoded colors | Use semantic CSS variables |
| Horizontal scroll on selections | Too many items | Use accordion pattern |
| Textarea looks wrong | Pill border-radius | Use smaller radius for textarea |
| Design looks "AI-generated" | AI slop patterns | Follow aesthetic guidelines, be bold |

---

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision - while ensuring it works beautifully on every screen size.
