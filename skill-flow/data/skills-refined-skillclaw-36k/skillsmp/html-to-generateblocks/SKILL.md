---
name: html-to-generateblocks
version: 2.0.0
description: Convert HTML/CSS layouts to GenerateBlocks V2 format with inline styles
author: Gaurav Tiwari
updated: 2026-01-22
trigger:
  - HTML to GenerateBlocks
  - convert to GB
  - convert HTML to blocks
  - GenerateBlocks conversion
tags:
  - wordpress
  - generateblocks
  - conversion
  - html
---

# HTML to GenerateBlocks V2 Conversion

Convert HTML/CSS layouts to GenerateBlocks V2 format using inline styles in block attributes.

## Output Requirements

**ALWAYS output converted blocks to a file, never inline in the chat.**

- Output filename: `{original-name}-converted.html` (e.g., `hero-converted.html`)
- For large conversions: Split into multiple files by section
- Include a brief summary in chat describing what was converted

**Why file output?**
- Converted block code is often 100+ lines
- Easier to copy/paste into WordPress
- Prevents truncation and formatting issues
- Allows side-by-side comparison with original

## Core Principle

**Use both `styles` and `css` attributes:**
- `styles`: Basic properties (padding, margin, colors, display, flex, grid)
- `css`: Complex features (hover states, pseudo-elements, media queries, transitions, animations)

**Never use BEM or custom classes** - all styling goes in block attributes.

## When to Use Core Blocks

For HTML elements not available in GenerateBlocks, use WordPress Core Blocks:

| HTML Element | Convert To | Reason |
|--------------|------------|--------|
| `<video>` | `core/video` | Native player controls, autoplay, loop |
| `<audio>` | `core/audio` | Native audio player |
| `<iframe>` (YouTube, Vimeo) | `core/embed` | oEmbed support, responsive sizing |
| `<table>` | `core/table` | Semantic table structure |
| `<figure>` with `<figcaption>` | `core/image` | Built-in caption support |
| `<blockquote>` with cite | `core/quote` | Semantic quote with citation |
| `<pre>` / `<code>` | `core/code` | Preformatted code display |
| `<ul>` / `<ol>` (semantic lists) | `core/list` | Use with `.list` class |
| `<hr>` | `core/separator` | Horizontal rule |
| Gallery layouts | `core/gallery` | Lightbox, columns, captions |
| Background image sections | `core/cover` | Parallax, overlay, focal point |
| **Text with emojis** | `core/paragraph` | GenerateBlocks doesn't render emojis properly |

**Conversion rule:** Use GenerateBlocks for layout containers and styled text. Use Core Blocks for specialized content types that have built-in functionality (players, embeds, tables, etc.).

## CRITICAL: htmlAttributes Format

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

**linkHtmlAttributes** (for media blocks) uses the same array format:
```json
"linkHtmlAttributes": [
  {"attribute": "href", "value": "/product/"},
  {"attribute": "target", "value": "_blank"}
]
```

## Block Structure

### Standard Element Block

```html
<!-- wp:generateblocks/element {"uniqueId":"elem001","tagName":"div","styles":{"display":"flex","gap":"1rem","padding":"2rem"},"css":".gb-element-elem001{display:flex;gap:1rem;padding:2rem}@media(max-width:768px){.gb-element-elem001{flex-direction:column}}"} -->
<div class="gb-element gb-element-elem001">
    <!-- Inner content -->
</div>
<!-- /wp:generateblocks/element -->
```

### Text Block (for headings, paragraphs, links)

```html
<!-- wp:generateblocks/text {"uniqueId":"text001","tagName":"h2","styles":{"fontSize":"2rem","fontWeight":"900","color":"#0a0a0a"},"css":".gb-text-text001{font-size:2rem;font-weight:900;color:#0a0a0a}"} -->
<h2 class="gb-text gb-text-text001">Heading Text</h2>
<!-- /wp:generateblocks/text -->
```

### Link as Card Wrapper

```html
<!-- wp:generateblocks/text {"uniqueId":"card001","tagName":"a","htmlAttributes":[{"attribute":"href","value":"/services/"}],"styles":{"display":"flex","flexDirection":"column","padding":"2rem","backgroundColor":"white","borderRadius":"1rem","textDecoration":"none"},"css":".gb-text-card001{display:flex;flex-direction:column;padding:2rem;background-color:white;border-radius:1rem;text-decoration:none;transition:all 0.3s}.gb-text-card001:hover{transform:translateY(-6px);box-shadow:0 20px 60px rgba(0,0,0,0.15)}"} -->
<a class="gb-text gb-text-card001" href="/services/">
    <!-- Card content -->
</a>
<!-- /wp:generateblocks/text -->
```

### Media/Image Block

```html
<!-- wp:generateblocks/media {"uniqueId":"img001","mediaType":"image","htmlAttributes":[{"attribute":"src","value":"https://example.com/image.jpg"},{"attribute":"alt","value":"Description"},{"attribute":"loading","value":"lazy"},{"attribute":"width","value":"600"},{"attribute":"height","value":"400"}],"styles":{"display":"block","width":"100%"},"css":".gb-media-img001{display:block;width:100%}"} -->
<img class="gb-media gb-media-img001" src="https://example.com/image.jpg" alt="Description" loading="lazy" width="600" height="400" />
<!-- /wp:generateblocks/media -->
```

## Styles vs CSS Decision Matrix

| Feature | Use `styles` | Use `css` |
|---------|-------------|-----------|
| Layout (display, flex, grid) | ✅ | Also in CSS |
| Spacing (padding, margin, gap) | ✅ | Also in CSS |
| Colors (background, text) | ✅ | Also in CSS |
| Typography (font-size, weight) | ✅ | Also in CSS |
| Basic borders, border-radius | ✅ | Also in CSS |
| Hover states | ❌ | ✅ Only CSS |
| Pseudo-elements (::before, ::after) | ❌ | ✅ Only CSS |
| Media queries | ❌ | ✅ Only CSS |
| Transitions/animations | ❌ | ✅ Only CSS |
| Complex selectors | ❌ | ✅ Only CSS |

**Pattern**: Always put properties in `styles`, then replicate with proper CSS syntax in `css` attribute, adding hover/pseudo/media queries.

## Common Patterns

### Card with Hover Effect

```html
<!-- wp:generateblocks/text {"uniqueId":"card001","tagName":"a","htmlAttributes":[{"attribute":"href","value":"/link/"}],"styles":{"display":"flex","flexDirection":"column","backgroundColor":"white","borderRadius":"1rem","padding":"2rem","border":"1px solid transparent","textDecoration":"none"},"css":".gb-text-card001{display:flex;flex-direction:column;background-color:white;border-radius:1rem;padding:2rem;border:1px solid transparent;text-decoration:none;transition:all 0.3s}.gb-text-card001::after{content:'';position:absolute;bottom:0;left:0;width:100%;height:3px;background:#c0392b;transform:scaleX(0);transform-origin:left;transition:transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)}.gb-text-card001:hover{transform:translateY(-6px);box-shadow:0 20px 60px rgba(0,0,0,0.15);border-color:#e5e5e5}.gb-text-card001:hover::after{transform:scaleX(1)}"} -->
<a class="gb-text gb-text-card001" href="/link/">
    <!-- Card content -->
</a>
<!-- /wp:generateblocks/text -->
```

### Grid Layout (Responsive)

```html
<!-- wp:generateblocks/element {"uniqueId":"grid001","tagName":"div","styles":{"display":"grid","gridTemplateColumns":"repeat(4, 1fr)","gap":"1rem"},"css":".gb-element-grid001{display:grid;grid-template-columns:repeat(4, 1fr);gap:1rem}@media(max-width:1024px){.gb-element-grid001{grid-template-columns:repeat(2, 1fr)!important}}@media(max-width:768px){.gb-element-grid001{grid-template-columns:1fr!important}}"} -->
<div class="gb-element gb-element-grid001">
    <!-- Grid items -->
</div>
<!-- /wp:generateblocks/element -->
```

### Icon Container with Hover

```html
<!-- wp:generateblocks/element {"uniqueId":"icon001","tagName":"div","styles":{"width":"3.5rem","height":"3.5rem","display":"flex","alignItems":"center","justifyContent":"center","backgroundColor":"#f5f5f3","borderRadius":"1rem","color":"#c0392b"},"css":".gb-element-icon001{width:3.5rem;height:3.5rem;display:flex;align-items:center;justify-content:center;background-color:#f5f5f3;border-radius:1rem;color:#c0392b;transition:all 0.3s}.gb-text-parentcard:hover .gb-element-icon001{background-color:#c0392b;color:white;transform:scale(1.05) rotate(-3deg)}"} -->
<div class="gb-element gb-element-icon001">
    <i class="md-icon-bolt" aria-hidden="true"></i>
</div>
<!-- /wp:generateblocks/element -->
```

### Featured Card (Dark, Span Multiple Columns)

```html
<!-- wp:generateblocks/element {"uniqueId":"feat001","tagName":"div","styles":{"gridColumn":"span 2","gridRow":"span 2","background":"linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)","minHeight":"26rem","position":"relative","display":"flex","flexDirection":"column","gap":"1rem","borderRadius":"1rem","padding":"2rem"},"css":".gb-element-feat001{grid-column:span 2;grid-row:span 2;background:linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);min-height:26rem;position:relative;display:flex;flex-direction:column;gap:1rem;border-radius:1rem;padding:2rem}.gb-element-feat001::before{content:'';position:absolute;top:0;right:0;width:60%;height:100%;background:radial-gradient(circle at 100% 0%, rgba(192, 57, 43, 0.2) 0%, transparent 60%);pointer-events:none}.gb-element-feat001>*{position:relative;z-index:1}@media(max-width:1024px){.gb-element-feat001{grid-column:span 2;grid-row:span 1;min-height:auto}}@media(max-width:768px){.gb-element-feat001{grid-column:span 1}}"} -->
<div class="gb-element gb-element-feat001">
    <!-- Featured card content -->
</div>
<!-- /wp:generateblocks/element -->
```

### Badge (Absolute Position)

```html
<!-- wp:generateblocks/text {"uniqueId":"badge001","tagName":"span","styles":{"position":"absolute","top":"1rem","right":"1rem","padding":"0.25rem 0.625rem","fontSize":"0.75rem","fontWeight":"600","letterSpacing":"0.05em","textTransform":"uppercase","backgroundColor":"#c0392b","color":"white","borderRadius":"2rem"},"css":".gb-text-badge001{position:absolute;top:1rem;right:1rem;padding:0.25rem 0.625rem;font-size:0.75rem;font-weight:600;letter-spacing:0.05em;text-transform:uppercase;background-color:#c0392b;color:white;border-radius:2rem}"} -->
<span class="gb-text gb-text-badge001">Recommended</span>
<!-- /wp:generateblocks/text -->
```

## Dynamic Content with Query Blocks

For sections with dynamic WordPress posts, use native query blocks with GenerateBlocks for styling:

```html
<!-- wp:query {"queryId":1,"query":{"perPage":12,"postType":"post","order":"desc","orderBy":"date","taxQuery":{"category":{"terms":[],"operator":"NOT IN"}}}} -->
<div class="wp-block-query">
    <!-- wp:post-template {"style":{"spacing":{"blockGap":"1rem"}}} -->

        <!-- Post Card -->
        <!-- wp:generateblocks/text {"uniqueId":"post001","tagName":"a","styles":{"display":"flex","flexDirection":"column","backgroundColor":"white","border":"1px solid #e5e5e5","borderRadius":"1rem","overflow":"hidden","textDecoration":"none"},"css":".gb-text-post001{display:flex;flex-direction:column;background-color:white;border:1px solid #e5e5e5;border-radius:1rem;overflow:hidden;text-decoration:none;transition:all 0.3s}.gb-text-post001:hover{transform:translateY(-6px);box-shadow:0 20px 60px rgba(0,0,0,0.15);border-color:#c0392b}"} -->
        <a class="gb-text gb-text-post001">
            <!-- wp:post-featured-image {"isLink":false,"aspectRatio":"12/5"} /-->

            <!-- wp:generateblocks/element {"uniqueId":"post002","tagName":"div","styles":{"padding":"1rem","display":"flex","flexDirection":"column","flex":"1"},"css":".gb-element-post002{padding:1rem;display:flex;flex-direction:column;flex:1}"} -->
            <div class="gb-element gb-element-post002">
                <!-- wp:post-title {"isLink":false,"style":{"typography":{"fontSize":"1.125rem","fontWeight":"700"}}} /-->
                <!-- wp:post-excerpt {"excerptLength":14} /-->
            </div>
            <!-- /wp:generateblocks/element -->
        </a>
        <!-- /wp:generateblocks/text -->

    <!-- /wp:post-template -->
</div>
<!-- /wp:query -->
```

## Unique ID Convention

- Format: `{section}{number}{letter}` (e.g., `hero001a`, `serv023`, `tool014`)
- Section prefix: 3-4 characters (hero, serv, tool, blog, feat)
- Number: Sequential 001-999
- Optional letter: For nested elements (a, b, c)

## Conversion Workflow

1. **Read original HTML/CSS** - Understand structure and styles
2. **Identify sections** - Break into logical components
3. **Map BEM classes to blocks** - Each `.block__element` becomes a GenerateBlocks element
4. **Extract base styles** - Put in `styles` attribute
5. **Extract complex styles** - Put in `css` attribute (hovers, pseudo, media queries)
6. **Create unique IDs** - Follow convention
7. **Test responsive behavior** - Ensure media queries work
8. **Handle dynamic content** - Use WordPress query blocks

## CSS Syntax Rules

### In `styles` attribute (JavaScript object):
```json
{
  "display": "flex",
  "flexDirection": "column",
  "backgroundColor": "#ffffff",
  "borderRadius": "1rem",
  "marginBottom": "2rem"
}
```

### In `css` attribute (CSS string):
```css
.gb-element-id{display:flex;flex-direction:column;background-color:#ffffff;border-radius:1rem;margin-bottom:2rem}.gb-element-id:hover{background-color:#f5f5f5}@media(max-width:768px){.gb-element-id{flex-direction:row}}
```

**Note**: CSS should be minified (no line breaks, minimal spaces).

## Responsive Patterns

### Mobile-First Grid
```css
.gb-element-grid{display:grid;grid-template-columns:1fr}@media(min-width:768px){.gb-element-grid{grid-template-columns:repeat(2, 1fr)}}@media(min-width:1024px){.gb-element-grid{grid-template-columns:repeat(4, 1fr)}}
```

### Desktop-First Grid (Match Original)
```css
.gb-element-grid{display:grid;grid-template-columns:repeat(4, 1fr);gap:1rem}@media(max-width:1024px){.gb-element-grid{grid-template-columns:repeat(2, 1fr)!important}}@media(max-width:768px){.gb-element-grid{grid-template-columns:1fr!important}}
```

### Sticky Sidebar
```css
.gb-element-sidebar{position:sticky;top:calc(var(--header-height, 80px) + 1rem)}@media(max-width:1024px){.gb-element-sidebar{position:static}}
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
- `<!-- wp:embed {...} -->` and `<!-- /wp:embed -->`
- Any other `<!-- wp:{namespace}/{block} -->` format

**WRONG - These will break the block editor:**
```html
<!-- This is a card -->
<!-- Section header -->
<!-- Hero content goes here -->
<!-- Button wrapper -->
```

**CORRECT - Only block delimiters:**
```html
<!-- wp:generateblocks/element {"uniqueId":"card001",...} -->
<div class="gb-element gb-element-card001">
    <!-- wp:image {"id":123} -->
    <figure class="wp-block-image"><img src="image.jpg" alt=""/></figure>
    <!-- /wp:image -->
</div>
<!-- /wp:generateblocks/element -->
```

Any extra HTML comments will **break the WordPress block editor** and cause parsing errors. This is non-negotiable. Do NOT add descriptive comments, section labels, or any other HTML comments.

### Design Inference (When CSS Not Provided)

When converting HTML without explicit CSS values, infer styles based on context:

**GeneratePress Defaults:**
- Primary: `#0073e6`
- Text: `#222222`, Muted: `#757575`
- Body: `17px`, line-height `1.7`
- H1: `42px`, H2: `35px`, H3: `29px`
- Section padding: `60px`
- Container max-width: `1200px`

**gauravtiwari.org Design System:**
- Primary: `#c0392b`
- Text: `#0a0a0a`, Muted: `#5c5c5c`
- Background: `#ffffff`, Light: `#f5f5f3`
- Headings: font-weight `900`, letter-spacing `-0.03em`
- Section padding: `4rem`
- Card radius: `1rem`, Button radius: `2rem`
- Hover lift: `translateY(-6px)`
- Shadow: `0 20px 60px rgba(0,0,0,0.15)`

## Common Gotchas

1. **No HTML comments except block markers** - Breaks WordPress block editor
2. **Always escape quotes in CSS strings** - Use single quotes for content, attr values
3. **Duplicate properties** - Put in both `styles` and `css` for consistency
4. **Use !important sparingly** - Only for overriding at breakpoints
5. **Test hover states** - Parent hover affecting child (`.parent:hover .child`)
6. **Pseudo-elements need content** - `content:''` for ::before/::after
7. **Gradients only in CSS** - Can't use in `styles` attribute
8. **CSS variables work** - Use var(--custom-property) freely
9. **Transitions on all** - `transition:all 0.3s` for smooth interactions
10. **Icon containers need `line-height: 1`** - Elements presenting icons must have `lineHeight: "1"` to prevent extra spacing
11. **Lists use `core/list` with `.list` class** - Convert `<ul>`/`<ol>` to native WordPress list block with `className: "list"`
12. **Use `--gb-container-width` for inner containers** - Set inner container width using the CSS variable; add `align: "full"` to parent section

## Performance Notes

- Inline styles are fast (no external CSS file)
- Each block's CSS is scoped to its unique ID
- GenerateBlocks automatically deduplicates common styles
- Media queries only load when needed
- Use `content-visibility: auto` for off-screen sections

## Example: Complete Hero Section

See `to-convert/home-hero-v2.html` for a complete real-world example with:
- Complex grid layout
- Multiple nested components
- Responsive breakpoints
- Hover effects
- Icon fonts
- Images with overlays
