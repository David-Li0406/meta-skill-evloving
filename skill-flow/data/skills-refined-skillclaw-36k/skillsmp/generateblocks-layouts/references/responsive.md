---
title: Responsive Design Reference
description: Media queries and breakpoint patterns for GenerateBlocks layouts
---

# Responsive Design Reference

GenerateBlocks uses desktop-first responsive design with CSS media queries.

## Standard Breakpoints

| Device | Media Query | Width |
|--------|-------------|-------|
| Desktop | Default (no query) | 1025px+ |
| Tablet | `@media(max-width:1024px)` | 768-1024px |
| Mobile | `@media(max-width:768px)` | <768px |

## CSS Format

Media queries go in the `css` attribute after base styles:

```css
.gb-element-id{base styles}@media(max-width:1024px){.gb-element-id{tablet styles}}@media(max-width:768px){.gb-element-id{mobile styles}}
```

**Important:** Keep CSS minified (no line breaks).

---

## Grid Patterns

### 4 → 2 → 1 Column Grid

```json
{
  "styles": {
    "display": "grid",
    "gridTemplateColumns": "repeat(4, 1fr)",
    "gap": "1rem"
  },
  "css": ".gb-element-grid001{display:grid;grid-template-columns:repeat(4, 1fr);gap:1rem}@media(max-width:1024px){.gb-element-grid001{grid-template-columns:repeat(2, 1fr)}}@media(max-width:768px){.gb-element-grid001{grid-template-columns:1fr}}"
}
```

### 3 → 2 → 1 Column Grid

```css
.gb-element-grid002{display:grid;grid-template-columns:repeat(3, 1fr);gap:2rem}@media(max-width:1024px){.gb-element-grid002{grid-template-columns:repeat(2, 1fr);gap:1.5rem}}@media(max-width:768px){.gb-element-grid002{grid-template-columns:1fr;gap:1rem}}
```

### 2 → 1 Column Grid

```css
.gb-element-grid003{display:grid;grid-template-columns:1fr 1fr;gap:2rem}@media(max-width:768px){.gb-element-grid003{grid-template-columns:1fr}}
```

### Complex Grid Areas

```css
.gb-element-grid004{display:grid;grid-template-columns:repeat(3, 1fr);gap:1rem;grid-template-areas:'primary primary profile' 'newsletter services profile'}@media(max-width:1024px){.gb-element-grid004{grid-template-columns:1fr;grid-template-areas:'primary' 'profile' 'newsletter' 'services'}}
```

---

## Flexbox Patterns

### Row → Column

```css
.gb-element-flex001{display:flex;flex-direction:row;gap:2rem;align-items:center}@media(max-width:768px){.gb-element-flex001{flex-direction:column;gap:1rem}}
```

### Flex Wrap

```css
.gb-element-flex002{display:flex;flex-wrap:wrap;gap:1rem}@media(max-width:768px){.gb-element-flex002{gap:0.5rem}}
```

### Justify Content Changes

```css
.gb-element-flex003{display:flex;justify-content:space-between;align-items:center}@media(max-width:768px){.gb-element-flex003{justify-content:center;flex-direction:column;gap:1rem}}
```

---

## Typography Patterns

### Heading Sizes

```css
.gb-text-head001{font-size:clamp(2rem, 5vw, 3.5rem);font-weight:900;line-height:1.1}
```

Using `clamp()` handles most responsive typography automatically.

### Explicit Breakpoints

```css
.gb-text-head002{font-size:3rem;line-height:1.2}@media(max-width:1024px){.gb-text-head002{font-size:2.5rem}}@media(max-width:768px){.gb-text-head002{font-size:2rem}}
```

### Text Alignment

```css
.gb-text-head003{text-align:left}@media(max-width:768px){.gb-text-head003{text-align:center}}
```

---

## Spacing Patterns

### Padding Changes

```css
.gb-element-sect001{padding:4rem 2rem}@media(max-width:1024px){.gb-element-sect001{padding:3rem 1.5rem}}@media(max-width:768px){.gb-element-sect001{padding:2rem 1rem}}
```

### Gap Changes

```css
.gb-element-grid005{gap:2rem}@media(max-width:768px){.gb-element-grid005{gap:1rem}}
```

### Margin Changes

```css
.gb-element-card001{margin-bottom:2rem}@media(max-width:768px){.gb-element-card001{margin-bottom:1rem}}
```

---

## Show/Hide Patterns

### Desktop Only

```css
.gb-element-desk001{display:block}@media(max-width:768px){.gb-element-desk001{display:none}}
```

### Mobile Only

```css
.gb-element-mob001{display:none}@media(max-width:768px){.gb-element-mob001{display:block}}
```

### Tablet Only

```css
.gb-element-tab001{display:none}@media(min-width:769px) and (max-width:1024px){.gb-element-tab001{display:block}}
```

---

## Sizing Patterns

### Width Changes

```css
.gb-element-box001{width:50%}@media(max-width:768px){.gb-element-box001{width:100%}}
```

### Max-Width Changes

```css
.gb-element-cont001{max-width:1200px}@media(max-width:1024px){.gb-element-cont001{max-width:100%}}
```

### Min-Height Changes

```css
.gb-element-hero001{min-height:600px}@media(max-width:768px){.gb-element-hero001{min-height:400px}}
```

---

## Grid Span Changes

### Featured Card Span

```css
.gb-element-feat001{grid-column:span 2;grid-row:span 2}@media(max-width:1024px){.gb-element-feat001{grid-column:span 2;grid-row:span 1}}@media(max-width:768px){.gb-element-feat001{grid-column:span 1}}
```

### Profile Card Span

```css
.gb-element-profile001{grid-area:profile;grid-row:span 4}@media(max-width:1024px){.gb-element-profile001{grid-row:span 1}}
```

---

## Position Changes

### Sticky → Static

```css
.gb-element-sidebar001{position:sticky;top:calc(var(--header-height, 80px) + 1rem)}@media(max-width:1024px){.gb-element-sidebar001{position:static}}
```

### Absolute Position Adjustments

```css
.gb-text-badge001{position:absolute;top:1rem;right:1rem}@media(max-width:768px){.gb-text-badge001{top:0.5rem;right:0.5rem}}
```

---

## Order Changes

### Reorder Columns

```css
.gb-element-img001{order:1}@media(max-width:768px){.gb-element-img001{order:2}}
.gb-element-text001{order:2}@media(max-width:768px){.gb-element-text001{order:1}}
```

---

## Complete Section Example

```html
<!-- wp:generateblocks/element {"uniqueId":"sect001","tagName":"section","styles":{"paddingTop":"4rem","paddingBottom":"4rem"},"css":".gb-element-sect001{padding-top:4rem;padding-bottom:4rem}@media(max-width:768px){.gb-element-sect001{padding-top:2rem;padding-bottom:2rem}}"} -->
<section class="gb-element gb-element-sect001">

    <!-- wp:generateblocks/element {"uniqueId":"inner001","tagName":"div","styles":{"maxWidth":"1200px","marginLeft":"auto","marginRight":"auto","paddingLeft":"1rem","paddingRight":"1rem"},"css":".gb-element-inner001{max-width:1200px;margin-left:auto;margin-right:auto;padding-left:1rem;padding-right:1rem}"} -->
    <div class="gb-element gb-element-inner001">

        <!-- wp:generateblocks/element {"uniqueId":"grid001","tagName":"div","styles":{"display":"grid","gridTemplateColumns":"repeat(3, 1fr)","gap":"2rem"},"css":".gb-element-grid001{display:grid;grid-template-columns:repeat(3, 1fr);gap:2rem}@media(max-width:1024px){.gb-element-grid001{grid-template-columns:repeat(2, 1fr)}}@media(max-width:768px){.gb-element-grid001{grid-template-columns:1fr;gap:1rem}}"} -->
        <div class="gb-element gb-element-grid001">
            <!-- Grid items -->
        </div>
        <!-- /wp:generateblocks/element -->

    </div>
    <!-- /wp:generateblocks/element -->

</section>
<!-- /wp:generateblocks/element -->
```

---

## Using !important

Use `!important` sparingly for media query overrides when needed:

```css
@media(max-width:768px){.gb-element-grid001{grid-template-columns:1fr!important}}
```

This ensures the responsive style takes precedence over any inline or conflicting styles.

---

## Mobile-First Alternative

While desktop-first is standard, mobile-first can be used:

```css
.gb-element-grid001{grid-template-columns:1fr}@media(min-width:768px){.gb-element-grid001{grid-template-columns:repeat(2, 1fr)}}@media(min-width:1024px){.gb-element-grid001{grid-template-columns:repeat(4, 1fr)}}
```

Use whichever approach matches your design workflow.
