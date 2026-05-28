---
name: elementor-to-generateblocks
version: 1.0.0
description: Convert Elementor layouts to clean GenerateBlocks V2 format, eliminating DIVception
author: Gaurav Tiwari
updated: 2026-01-22
trigger:
  - Elementor to GenerateBlocks
  - convert Elementor
  - Elementor migration
  - clean up Elementor
  - simplify Elementor
tags:
  - wordpress
  - generateblocks
  - elementor
  - conversion
  - migration
---

# Elementor to GenerateBlocks Converter

Convert bloated Elementor layouts to clean, semantic GenerateBlocks V2 blocks.

## Output Requirements

**ALWAYS output converted blocks to a file, never inline in the chat.**

- Output filename: `{section-name}-converted.html` (e.g., `hero-converted.html`)
- For full page conversions: Split into multiple files by section
- Include a brief summary in chat describing what was converted

**Why file output?**
- Converted block code is often 100+ lines
- Easier to copy/paste into WordPress
- Prevents truncation and formatting issues
- Allows comparison with original Elementor output

## The DIVception Problem

Elementor wraps everything in excessive nested divs with utility classes:

```html
<!-- Elementor's typical output -->
<section class="elementor-section elementor-top-section elementor-element elementor-element-abc123 elementor-section-boxed elementor-section-height-default elementor-section-height-default">
  <div class="elementor-container elementor-column-gap-default">
    <div class="elementor-column elementor-col-50 elementor-top-column elementor-element elementor-element-def456">
      <div class="elementor-widget-wrap elementor-element-populated">
        <div class="elementor-element elementor-element-ghi789 elementor-widget elementor-widget-heading">
          <div class="elementor-widget-container">
            <h2 class="elementor-heading-title elementor-size-default">Hello World</h2>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
```

**Result:** 7 nested divs for a simple heading.

## GenerateBlocks Solution

Same content, cleaner structure:

```html
<!-- wp:generateblocks/element {"uniqueId":"sect001","tagName":"section","styles":{"paddingTop":"4rem","paddingBottom":"4rem"},"css":".gb-element-sect001{padding-top:4rem;padding-bottom:4rem}"} -->
<section class="gb-element gb-element-sect001">
    <!-- wp:generateblocks/element {"uniqueId":"sect001a","tagName":"div","styles":{"maxWidth":"1200px","marginLeft":"auto","marginRight":"auto","paddingLeft":"1rem","paddingRight":"1rem"},"css":".gb-element-sect001a{max-width:1200px;margin-left:auto;margin-right:auto;padding-left:1rem;padding-right:1rem}"} -->
    <div class="gb-element gb-element-sect001a">
        <!-- wp:generateblocks/text {"uniqueId":"sect001b","tagName":"h2","styles":{"fontSize":"2rem","fontWeight":"700","color":"#0a0a0a"},"css":".gb-text-sect001b{font-size:2rem;font-weight:700;color:#0a0a0a}"} -->
        <h2 class="gb-text gb-text-sect001b">Hello World</h2>
        <!-- /wp:generateblocks/text -->
    </div>
    <!-- /wp:generateblocks/element -->
</section>
<!-- /wp:generateblocks/element -->
```

**Result:** 3 semantic elements. Clean, maintainable, fast.

## Conversion Rules

### 1. Flatten the Structure

| Elementor Pattern | GenerateBlocks Equivalent |
|-------------------|---------------------------|
| `elementor-section` > `elementor-container` | Single `section` + inner `div` |
| `elementor-column` > `elementor-widget-wrap` | Single `div` with flex/grid |
| `elementor-widget` > `elementor-widget-container` | Direct content block |
| Multiple wrapper divs | Remove all unnecessary wrappers |

### 2. Map Elementor Classes to Inline Styles

| Elementor Class | CSS Property |
|-----------------|--------------|
| `elementor-section-boxed` | `max-width: 1200px; margin: auto` |
| `elementor-section-full_width` | `max-width: 100%` |
| `elementor-column-gap-default` | `gap: 1rem` |
| `elementor-column-gap-extended` | `gap: 2rem` |
| `elementor-col-50` | `flex: 0 0 50%` or grid column |
| `elementor-col-33` | `flex: 0 0 33.333%` or grid column |
| `elementor-hidden-desktop` | `@media(min-width:1025px){display:none}` |
| `elementor-hidden-tablet` | `@media(max-width:1024px){display:none}` |
| `elementor-hidden-mobile` | `@media(max-width:767px){display:none}` |

### 3. Widget to Block Mapping

| Elementor Widget | GenerateBlocks Block |
|------------------|---------------------|
| `elementor-widget-heading` | `generateblocks/text` with h1-h6 |
| `elementor-widget-text-editor` | `generateblocks/text` with p/div |
| `elementor-widget-button` | `generateblocks/text` with tagName="a" |
| `elementor-widget-image` | `generateblocks/media` (or `core/image` if caption needed) |
| `elementor-widget-icon` | `generateblocks/shape` or inline SVG |
| `elementor-widget-icon-box` | `generateblocks/element` container |
| `elementor-widget-image-box` | `generateblocks/element` container |
| `elementor-widget-spacer` | Remove (use margins/padding instead) |
| `elementor-widget-divider` | `generateblocks/element` with border (or `core/separator`) |

### 4. Widgets Requiring Core Blocks

Some Elementor widgets should convert to Core Blocks instead of GenerateBlocks:

| Elementor Widget | Use Core Block | Reason |
|------------------|----------------|--------|
| `elementor-widget-video` | `core/video` or `core/embed` | Native player, embed support |
| `elementor-widget-image-gallery` | `core/gallery` | Lightbox, columns, captions |
| `elementor-widget-image-carousel` | `core/gallery` + CSS or third-party | Slider functionality |
| `elementor-widget-audio` | `core/audio` | Native audio player |
| `elementor-widget-table` | `core/table` | Semantic table structure |
| `elementor-widget-blockquote` | `core/quote` | Semantic quote with citation |
| `elementor-widget-code-highlight` | `core/code` | Preformatted code display |
| `elementor-widget-text-path` | Keep as SVG | No Core equivalent |
| `elementor-widget-lottie` | Keep as custom | No Core equivalent |
| `elementor-widget-image` (with caption) | `core/image` | Built-in caption support |
| `elementor-widget-tabs` | `core/details` or custom | Accordion/tabs functionality |
| `elementor-widget-accordion` | `core/details` | Native disclosure widget |
| `elementor-widget-toggle` | `core/details` | Native disclosure widget |
| **Text with emojis** | `core/paragraph` | GenerateBlocks doesn't render emojis properly |

**Rule:** Use GenerateBlocks for layout and styling. Use Core Blocks for specialized functionality (media players, embeds, tables, interactive elements).

### 4. Column Layouts

**Elementor 2-column:**
```html
<div class="elementor-container">
  <div class="elementor-column elementor-col-50">...</div>
  <div class="elementor-column elementor-col-50">...</div>
</div>
```

**GenerateBlocks equivalent:**
```html
<!-- wp:generateblocks/element {"uniqueId":"col001","tagName":"div","styles":{"display":"grid","gridTemplateColumns":"repeat(2, 1fr)","gap":"2rem"},"css":".gb-element-col001{display:grid;grid-template-columns:repeat(2, 1fr);gap:2rem}@media(max-width:768px){.gb-element-col001{grid-template-columns:1fr}}"} -->
<div class="gb-element gb-element-col001">
    <!-- Column 1 content -->
    <!-- Column 2 content -->
</div>
<!-- /wp:generateblocks/element -->
```

### 5. Common Elementor Patterns

**Hero with background:**
```html
<!-- wp:generateblocks/element {"uniqueId":"hero001","tagName":"section","styles":{"minHeight":"80vh","display":"flex","alignItems":"center","justifyContent":"center","backgroundImage":"url(image.jpg)","backgroundSize":"cover","backgroundPosition":"center"},"css":".gb-element-hero001{min-height:80vh;display:flex;align-items:center;justify-content:center;background-image:url(image.jpg);background-size:cover;background-position:center}.gb-element-hero001::before{content:'';position:absolute;inset:0;background:rgba(0,0,0,0.5)}"} -->
<section class="gb-element gb-element-hero001">
    <!-- Hero content -->
</section>
<!-- /wp:generateblocks/element -->
```

**Card grid:**
```html
<!-- wp:generateblocks/element {"uniqueId":"cards001","tagName":"div","styles":{"display":"grid","gridTemplateColumns":"repeat(3, 1fr)","gap":"2rem"},"css":".gb-element-cards001{display:grid;grid-template-columns:repeat(3, 1fr);gap:2rem}@media(max-width:1024px){.gb-element-cards001{grid-template-columns:repeat(2, 1fr)}}@media(max-width:768px){.gb-element-cards001{grid-template-columns:1fr}}"} -->
<div class="gb-element gb-element-cards001">
    <!-- Card blocks -->
</div>
<!-- /wp:generateblocks/element -->
```

## Design Inference (When CSS Not Provided)

When converting Elementor without CSS values, infer styles based on context:

### Default GeneratePress Design System

Use these defaults when no specific styles are provided:

**Colors:**
- Primary: `#0073e6` (GeneratePress default accent)
- Text: `#222222`
- Muted text: `#757575`
- Background: `#ffffff`
- Light background: `#f7f8f9`
- Border: `#e0e0e0`

**Typography:**
- Body: `17px`, line-height `1.7`
- H1: `42px`, font-weight `600`
- H2: `35px`, font-weight `600`
- H3: `29px`, font-weight `600`
- H4: `24px`, font-weight `600`

**Spacing:**
- Section padding: `60px` top/bottom
- Container max-width: `1200px`
- Content padding: `20px`
- Gap between elements: `20px`

**Buttons:**
- Padding: `15px 30px`
- Border-radius: `4px`
- Background: primary color
- Hover: darken 10%

### Site-Specific Inference

When the target site is known, extract design tokens from:

1. **Theme's style.css** - Primary colors, fonts, base sizes
2. **theme.json** (block themes) - Color palette, typography presets
3. **Existing pages** - Match the established visual language

**Example inference for gauravtiwari.org:**
```json
{
  "colors": {
    "primary": "#c0392b",
    "text": "#0a0a0a",
    "muted": "#5c5c5c",
    "background": "#ffffff",
    "lightBg": "#f5f5f3",
    "border": "#e5e5e5"
  },
  "typography": {
    "body": "1rem",
    "h1": "clamp(2rem, 5vw, 3.5rem)",
    "h2": "clamp(1.5rem, 3vw, 2.5rem)",
    "fontWeight": "900 for headings"
  },
  "spacing": {
    "sectionPadding": "4rem",
    "containerMax": "1200px",
    "gap": "1rem to 2rem"
  },
  "effects": {
    "borderRadius": "1rem for cards, 2rem for buttons",
    "hoverLift": "translateY(-6px)",
    "shadow": "0 20px 60px rgba(0,0,0,0.15)"
  }
}
```

## CRITICAL: No Extra HTML Comments

**⛔ NEVER add HTML comments other than WordPress block markers.**

The ONLY allowed comments are WordPress block delimiters:
- `<!-- wp:generateblocks/element {...} -->` and `<!-- /wp:generateblocks/element -->`
- `<!-- wp:generateblocks/text {...} -->` and `<!-- /wp:generateblocks/text -->`
- `<!-- wp:generateblocks/media {...} -->` and `<!-- /wp:generateblocks/media -->`
- `<!-- wp:generateblocks/shape {...} -->` and `<!-- /wp:generateblocks/shape -->`
- `<!-- wp:image {...} -->` and `<!-- /wp:image -->`
- `<!-- wp:video {...} -->` and `<!-- /wp:video -->`
- `<!-- wp:gallery {...} -->` and `<!-- /wp:gallery -->`
- Any other `<!-- wp:{namespace}/{block} -->` format

**WRONG - These will break the block editor:**
```html
<!-- This is a card -->
<!-- Hero section -->
<!-- Converted from Elementor -->
```

**CORRECT - Only block delimiters:**
```html
<!-- wp:generateblocks/element {"uniqueId":"sect001",...} -->
<section class="gb-element gb-element-sect001">
    <!-- wp:generateblocks/text {"uniqueId":"sect001a",...} -->
    <h2 class="gb-text gb-text-sect001a">Hello World</h2>
    <!-- /wp:generateblocks/text -->
</section>
<!-- /wp:generateblocks/element -->
```

Any extra HTML comments will **break the WordPress block editor** and cause parsing errors. This is non-negotiable.

## Critical Rules

### 1. htmlAttributes MUST Use Array Format

**htmlAttributes MUST be an array of objects, NOT a plain object:**

```json
// ✅ CORRECT - Array of objects
"htmlAttributes": [
  {"attribute": "href", "value": "/contact/"},
  {"attribute": "target", "value": "_blank"},
  {"attribute": "id", "value": "section-id"}
]

// ❌ WRONG - Plain object (causes block editor recovery errors)
"htmlAttributes": {"href": "/contact/", "target": "_blank"}
```

**linkHtmlAttributes** (for media blocks) uses the same array format.

### 2. Always Include Both styles and css

Every block needs:
- `styles` object with camelCase properties
- `css` string with minified CSS (kebab-case)

### 2. Icon Containers Need `line-height: 1`

Elements presenting icons must have `lineHeight: "1"` to prevent extra spacing:
```json
{"styles": {"lineHeight": "1", "display": "flex", "alignItems": "center"}}
```

### 3. Lists Use `core/list` with `.list` Class

Convert Elementor list widgets to native WordPress list block:
```html
<!-- wp:list {"className":"list"} -->
<ul class="wp-block-list list">...</ul>
<!-- /wp:list -->
```

### 4. Container Width with CSS Variable

Use `--gb-container-width` for inner container width and `align: "full"` on parent section:
```json
{"align": "full", "styles": {"maxWidth": "var(--gb-container-width)"}}
```

### 6. Use Semantic HTML

Replace Elementor's generic divs with proper tags:

| Content Type | Tag |
|--------------|-----|
| Page section | `section` |
| Header area | `header` |
| Footer area | `footer` |
| Navigation | `nav` |
| Main content | `article` |
| Sidebar | `aside` |
| Card wrapper | `div` or `a` (if clickable) |

### 7. Remove Spacers

Never convert `elementor-widget-spacer` to a block. Use:
- `marginBottom` on preceding element
- `marginTop` on following element
- `gap` on parent container

### 8. Flatten Icon Boxes

**Elementor icon box (simplified):**
```html
<div class="elementor-icon-box">
  <div class="elementor-icon-box-icon">
    <span class="elementor-icon"><i class="fab fa-wordpress"></i></span>
  </div>
  <div class="elementor-icon-box-content">
    <h3>Title</h3>
    <p>Description</p>
  </div>
</div>
```

**GenerateBlocks:**
```html
<!-- wp:generateblocks/element {"uniqueId":"ibox001","tagName":"div","styles":{"display":"flex","gap":"1rem","alignItems":"flex-start"},"css":".gb-element-ibox001{display:flex;gap:1rem;align-items:flex-start}"} -->
<div class="gb-element gb-element-ibox001">
    <!-- wp:generateblocks/shape {"uniqueId":"ibox001a","styles":{"width":"3rem","height":"3rem","display":"flex","alignItems":"center","justifyContent":"center","backgroundColor":"#f5f5f3","borderRadius":"0.75rem","color":"#c0392b","flexShrink":"0"},"css":".gb-shape-ibox001a{width:3rem;height:3rem;display:flex;align-items:center;justify-content:center;background-color:#f5f5f3;border-radius:0.75rem;color:#c0392b;flex-shrink:0}"} -->
    <span class="gb-shape gb-shape-ibox001a">
        <svg viewBox="0 0 24 24" fill="currentColor"><path d="..."/></svg>
    </span>
    <!-- /wp:generateblocks/shape -->
    <!-- wp:generateblocks/element {"uniqueId":"ibox001b","tagName":"div","styles":{"flex":"1"},"css":".gb-element-ibox001b{flex:1}"} -->
    <div class="gb-element gb-element-ibox001b">
        <!-- wp:generateblocks/text {"uniqueId":"ibox001c","tagName":"h3","styles":{"fontSize":"1.125rem","fontWeight":"700","marginBottom":"0.5rem"},"css":".gb-text-ibox001c{font-size:1.125rem;font-weight:700;margin-bottom:0.5rem}"} -->
        <h3 class="gb-text gb-text-ibox001c">Title</h3>
        <!-- /wp:generateblocks/text -->
        <!-- wp:generateblocks/text {"uniqueId":"ibox001d","tagName":"p","styles":{"color":"#5c5c5c","lineHeight":"1.6"},"css":".gb-text-ibox001d{color:#5c5c5c;line-height:1.6}"} -->
        <p class="gb-text gb-text-ibox001d">Description</p>
        <!-- /wp:generateblocks/text -->
    </div>
    <!-- /wp:generateblocks/element -->
</div>
<!-- /wp:generateblocks/element -->
```

## Conversion Workflow

1. **Analyze Elementor HTML** - Identify sections, columns, widgets
2. **Extract content** - Isolate actual text, images, links
3. **Determine layout** - Map column structure to grid/flex
4. **Apply design tokens** - Use provided CSS or infer from site
5. **Build blocks** - Create GenerateBlocks with inline styles
6. **Test responsive** - Add media queries for breakpoints
7. **Validate** - Ensure no HTML comments except block markers

## Performance Benefits

| Metric | Elementor | GenerateBlocks |
|--------|-----------|----------------|
| DOM nodes | 50-100+ per section | 5-15 per section |
| CSS file size | 200KB+ | 0 (inline) |
| Render blocking | Multiple CSS files | None |
| First paint | Delayed | Fast |
| CLS issues | Common | Rare |

## Font Awesome to SVG

Replace Elementor's Font Awesome icons with inline SVGs:

```html
<!-- Instead of <i class="fab fa-twitter"></i> -->
<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
</svg>
```

See [SVG Icons Reference](../generateblocks-layouts/references/svg-icons.md) for common icons.
