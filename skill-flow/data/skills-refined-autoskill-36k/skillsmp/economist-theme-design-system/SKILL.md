---
name: Economist Theme Design System
description: Guidelines for maintaining visual consistency with The Economist's design language
version: 1.1.0
triggers:
  - Adding new styles or components
  - Modifying existing SCSS
  - Creating new layouts
  - Ensuring design consistency
  - Visual regression testing
---

## Context

This blog uses a custom theme inspired by The Economist's visual identity. The design system is implemented in `_sass/economist-theme.scss` (600+ lines) and follows The Economist's editorial standards:

**Core Principles**:
- Clean, readable typography with generous whitespace
- Economist red (#E3120B) for accents only (not dominant)
- Serif fonts (Merriweather) for body text
- Sans-serif fonts (Inter) for UI elements
- Professional, editorial aesthetic

**Theme Source**: Analyzed The Economist's live website using Playwright MCP Bridge

## Step-by-Step Instructions

### 1. Understanding the Design System

**Typography Hierarchy**:
```scss
// Serif (body content)
font-family: 'Merriweather', Georgia, serif;

// Sans-serif (UI elements, navigation, metadata)
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
```

**Color Palette**:
```scss
$economist-red: #E3120B;      // Accent only (header banner, links)
$text-black: #1a1a1a;         // Primary text
$text-gray: #666;             // Metadata, secondary text
$border-gray: #ddd;           // Subtle borders
$bg-light: #f9f9f9;           // Subtle backgrounds
```

**Spacing System**:
```scss
$spacing-unit: 16px;
// Use multiples: 0.5x, 1x, 1.5x, 2x, 3x, 4x
```

### 2. Adding New Styles

**Process**:
1. Open `_sass/economist-theme.scss`
2. Find the relevant section (layout, components, typography, etc.)
3. Use existing variables—never hardcode values
4. Follow existing patterns and naming conventions
5. Test at all breakpoints (320px, 768px, 1024px, 1920px)

**Example**:
```scss
.new-component {
  // Layout
  max-width: 1040px;
  margin: 0 auto;
  padding: $spacing-unit * 2;
  
  // Typography
  font-family: 'Merriweather', serif;
  font-size: 18px;
  line-height: 1.8;
  color: $text-black;
  
  // Visual
  border-top: 1px solid $border-gray;
  background: $bg-light;
}
```

### 3. Responsive Design

**Mobile-First Approach**:
```scss
.component {
  // Base (mobile): 320px+
  padding: $spacing-unit;
  font-size: 16px;
  
  // Tablet: 768px+
  @media (min-width: 768px) {
    padding: $spacing-unit * 1.5;
    font-size: 17px;
  }
  
  // Desktop: 1024px+
  @media (min-width: 1024px) {
    padding: $spacing-unit * 2;
    font-size: 18px;
  }
}
```

### 4. Component Patterns

**Article Cards** (blog listing):
```scss
.article-card {
  border-top: 1px solid $border-gray;
  padding: $spacing-unit * 2 0;
  
  &:hover {
    background: $bg-light;
  }
}
```

**Category Labels**:
```scss
.category {
  color: $text-gray;          // NOT red
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
```

**Red Header Banner**:
```scss
.site-header {
  background: $economist-red;
  color: white;
  padding: $spacing-unit 0;
}
```

### 5. Testing Visual Changes

1. Start local server: `bundle exec jekyll serve --livereload`
2. Open http://localhost:4000/ in browser
3. Compare side-by-side with https://www.economist.com/ reference
4. Test responsive: resize browser to 320px, 768px, 1024px
5. Check browser console for errors
6. Verify no visual regressions on other pages

## Common Pitfalls

### Pitfall 1: Using Red Too Much
**Problem**: Applying `$economist-red` to multiple elements, making the design loud  
**Solution**: Red is for accents ONLY—header banner, occasional links, CTAs  
**Example**: Category labels should be `$text-gray`, NOT red

### Pitfall 2: Hardcoding Values
**Problem**: Using `color: #1a1a1a;` or `padding: 24px;` directly  
**Solution**: Use variables: `color: $text-black;` and `padding: $spacing-unit * 1.5;`  
**Why**: Maintains consistency and makes theme-wide changes easy

### Pitfall 3: Deep Selector Nesting
**Problem**: `.page .section .container .item .link { }` (5 levels deep)  
**Solution**: Max 3 levels of nesting. Flatten selectors or use classes  
**Example**: `.article-card__title` instead of `.card .content .title`

### Pitfall 4: Mixing Font Families
**Problem**: Using `font-family: Arial` or system fonts inconsistently  
**Solution**: Serif (Merriweather) for body, Sans-serif (Inter) for UI—nothing else  
**Check**: Search for `font-family` in SCSS to ensure consistency

### Pitfall 5: Ignoring Responsive Breakpoints
**Problem**: Looks perfect on desktop but broken on mobile  
**Solution**: ALWAYS test at 320px, 768px, 1024px before committing  
**Tool**: Browser DevTools responsive mode

### Pitfall 6: Overriding Existing Styles
**Problem**: Adding new styles that conflict with existing rules  
**Solution**: Check for existing selectors before adding new ones. Extend, don't override.

## Code Snippets/Patterns

### Standard Component Structure

```scss
.component-name {
  // Layout properties first
  display: block;
  max-width: 1040px;
  margin: 0 auto;
  padding: $spacing-unit * 2;
  
  // Typography
  font-family: 'Merriweather', serif;
  font-size: 18px;
  line-height: 1.8;
  color: $text-black;
  
  // Visual styling
  background: $bg-light;
  border-top: 1px solid $border-gray;
  
  // Responsive overrides
  @media (min-width: 768px) {
    padding: $spacing-unit * 3;
  }
}
```

### Hover States (Subtle)

```scss
.card {
  transition: background-color 0.2s ease;
  
  &:hover {
    background: $bg-light;  // Subtle highlight
  }
}
```

### Typography Mixins (If Needed)

```scss
@mixin economist-serif {
  font-family: 'Merriweather', Georgia, serif;
  font-weight: 400;
  line-height: 1.8;
}

@mixin economist-sans {
  font-family: 'Inter', -apple-system, sans-serif;
  font-weight: 400;
  line-height: 1.6;
}
```

### Spacing Utilities

```scss
// Use multiples of $spacing-unit (16px)
.small-gap { margin-bottom: $spacing-unit * 0.5; }    // 8px
.normal-gap { margin-bottom: $spacing-unit; }         // 16px
.large-gap { margin-bottom: $spacing-unit * 2; }      // 32px
.huge-gap { margin-bottom: $spacing-unit * 4; }       // 64px
```

## Date Formatting Patterns

### Economist Date Format (Liquid)

The Economist uses ordinal date format: "Jan 5th 2026|X min read"

**Implementation:**
```liquid
{% assign day = post.date | date: "%-d" %}
{{ post.date | date: "%b %-d" }}{% if day == '1' or day == '21' or day == '31' %}st{% elsif day == '2' or day == '22' %}nd{% elsif day == '3' or day == '23' %}rd{% else %}th{% endif %} {{ post.date | date: "%Y" }}
```

**Output examples:**
- Jan 1st 2026
- Jan 2nd 2026  
- Jan 3rd 2026
- Jan 5th 2026
- Jan 21st 2026

**Usage in meta tags:**
```liquid
<time class="topic-meta-date" datetime="{{ post.date | date_to_xmlschema }}">
  {{ post.date | date: "%b %-d" }}{% assign day = post.date | date: "%-d" %}{% if day == '1' or day == '21' or day == '31' %}st{% elsif day == '2' or day == '22' %}nd{% elsif day == '3' or day == '23' %}rd{% else %}th{% endif %} {{ post.date | date: "%Y" }}
</time>
<span class="topic-meta-separator">|</span>
<span class="topic-meta-item">{{ words | divided_by: 200 | plus: 1 }} min read</span>
```

**Styling:**
```scss
.topic-meta-date {
  font-family: $font-sans;
  font-size: 0.8125rem;
  color: $text-tertiary;
  font-weight: 400;
}

.topic-meta-separator {
  color: $text-tertiary;
  margin: 0 0.25rem;
}
```

## Image Fallback Strategy

### Default Blog Images

For blog posts without featured images, use default fallback asset.

**Default Image Location:**
```
assets/images/blog-default.svg
```

**SVG Format (1200x675 - 16:9 aspect ratio):**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f6f6f6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#e8e8e8;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="1200" height="675" fill="url(#grad)"/>
</svg>
```

**Usage in Templates:**
```liquid
{% if post.image %}
  <img src="{{ post.image | relative_url }}" alt="{{ post.title }}">
{% else %}
  <img src="/assets/images/blog-default.svg" alt="{{ post.title }}">
{% endif %}
```

**Or simplified with OR operator:**
```liquid
<img src="{% if post.image %}{{ post.image | relative_url }}{% else %}/assets/images/blog-default.svg{% endif %}" alt="{{ post.title }}">
```

**Future Enhancement:**
- economist-agents repo can generate custom theme images per post
- Store in assets/images/generated/
- Fallback chain: post.image → generated image → blog-default.svg

**Styling:**
```scss
.topic-card-image {
  width: 280px;  // Fixed width
  aspect-ratio: 16 / 9;  // Always 16:9
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;  // Crop to fit
  }
}
```

## Related Files

- [`_sass/economist-theme.scss`](../../_sass/economist-theme.scss) - Main theme file (600+ lines)
- [`_layouts/default.html`](../../_layouts/default.html) - Base layout
- [`_layouts/post.html`](../../_layouts/post.html) - Article layout
- [`docs/CURRENT_STATE.md`](../CURRENT_STATE.md) - Theme implementation history
- [`README.md`](../../README.md) - Theme overview

## Success Criteria

- [ ] New styles use variables from `economist-theme.scss`
- [ ] Max 3 levels of selector nesting
- [ ] Tested at 320px, 768px, 1024px, 1920px
- [ ] Follows Economist design language (clean, readable, professional)
- [ ] Red used sparingly (accents only)
- [ ] Serif for body, sans-serif for UI
- [ ] No hardcoded colors, spacing, or fonts
- [ ] No visual regressions on other pages
- [ ] Browser console shows 0 errors

## Version History

- **1.1.0** (2026-01-05): Added Economist date format patterns (ordinal suffixes), image fallback strategy, default blog-default.svg asset documentation
- **1.0.0** (2026-01-05): Initial skill creation from README.md and AI_CODING_GUIDELINES.md
