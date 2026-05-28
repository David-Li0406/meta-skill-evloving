---
name: figma-to-generateblocks
version: 1.0.0
description: Convert Figma designs to GenerateBlocks V2 format for WordPress
author: Gaurav Tiwari
updated: 2026-01-22
trigger:
  - Figma to GenerateBlocks
  - convert Figma
  - Figma design to WordPress
  - Figma to GB
  - implement Figma design
  - Figma screenshot
  - design to blocks
tags:
  - wordpress
  - generateblocks
  - figma
  - conversion
  - design
---

# Figma to GenerateBlocks Converter

Convert Figma designs to clean, semantic GenerateBlocks V2 blocks for WordPress.

## Output Requirements

**ALWAYS output converted blocks to a file, never inline in the chat.**

- Output filename: `{design-name}.html` (e.g., `homepage-hero.html`, `pricing-section.html`)
- For complex designs: Split into multiple files by section
- Include a brief summary in chat describing what was created

**Why file output?**
- Block code is often 100+ lines
- Easier to copy/paste into WordPress
- Prevents truncation and formatting issues
- Allows iterative refinement of design implementation

## Input Types

This skill handles multiple Figma input formats:

| Input Type | How to Process |
|------------|----------------|
| **Screenshot/Image** | Analyze visual layout, colors, typography, spacing |
| **Figma URL** | Extract design tokens if Dev Mode access available |
| **Copied CSS** | Parse Figma's generated CSS values |
| **Design specs** | Use provided measurements and colors |
| **Verbal description** | Infer from user's description of the design |

## Conversion Workflow

### Step 1: Analyze the Design

Extract these elements from the Figma design:

**Layout Structure:**
- Container hierarchy (sections, rows, columns)
- Grid/flex layout patterns
- Spacing between elements (gaps, padding, margins)
- Alignment (center, start, end, space-between)

**Typography:**
- Font families (map to web-safe or Google Fonts)
- Font sizes (convert to rem/clamp for responsiveness)
- Font weights (100-900)
- Line heights
- Letter spacing
- Text colors

**Colors:**
- Background colors
- Text colors
- Border colors
- Gradient definitions
- Opacity/transparency

**Spacing:**
- Padding values
- Margin values
- Gap between elements
- Section spacing

**Visual Effects:**
- Border radius
- Box shadows
- Hover states (infer from design variants)
- Transitions

### Step 2: Map to GenerateBlocks

| Figma Element | GenerateBlocks Block |
|---------------|---------------------|
| Frame/Section | `generateblocks/element` with `tagName: "section"` |
| Auto Layout (horizontal) | `generateblocks/element` with `display: flex` |
| Auto Layout (vertical) | `generateblocks/element` with `display: flex; flex-direction: column` |
| Grid | `generateblocks/element` with `display: grid` |
| Text | `generateblocks/text` with appropriate `tagName` |
| Image (simple) | `generateblocks/media` |
| Icon/Vector | `generateblocks/shape` with inline SVG |
| Button | `generateblocks/text` with `tagName: "a"` or `"button"` |
| Card | `generateblocks/element` or `generateblocks/text` (if clickable) |
| Link | `generateblocks/text` with `tagName: "a"` |

### Step 2b: When to Use Core Blocks

Some Figma elements should convert to WordPress Core Blocks instead:

| Figma Element | Use Core Block | Reason |
|---------------|----------------|--------|
| Image with caption | `core/image` | Built-in caption support |
| Image gallery/grid | `core/gallery` | Lightbox, columns, captions |
| Video player | `core/video` | Native video controls |
| Embedded video (YouTube/Vimeo) | `core/embed` | oEmbed support |
| Audio player | `core/audio` | Native audio controls |
| Data table | `core/table` | Semantic table structure |
| Quote with attribution | `core/quote` | Semantic blockquote |
| Code snippet | `core/code` | Preformatted code display |
| Bulleted/numbered list | `core/list` | Semantic list structure |
| Hero with background image | `core/cover` | Background image, overlay, parallax |
| Horizontal divider | `core/separator` | Semantic hr element |
| Download link/file | `core/file` | Download button with filename |
| **Text with emojis** | `core/paragraph` | GenerateBlocks doesn't render emojis properly |

**Conversion rule:** Use GenerateBlocks for custom layouts and styled containers. Use Core Blocks for content types with built-in functionality (media players, embeds, tables, etc.).

### Step 3: Generate Block Code

Use this structure for each block:

```html
<!-- wp:generateblocks/{type} {"uniqueId":"{id}","tagName":"{tag}","styles":{...},"css":"..."} -->
<{tag} class="gb-{type} gb-{type}-{id}">
    {content}
</{tag}>
<!-- /wp:generateblocks/{type} -->
```

## Figma CSS to GenerateBlocks

### Typography Conversion

**Figma CSS:**
```css
font-family: Inter;
font-size: 48px;
font-weight: 700;
line-height: 120%;
letter-spacing: -0.02em;
```

**GenerateBlocks:**
```json
{
  "styles": {
    "fontFamily": "'Inter', sans-serif",
    "fontSize": "clamp(2rem, 5vw, 3rem)",
    "fontWeight": "700",
    "lineHeight": "1.2",
    "letterSpacing": "-0.02em"
  },
  "css": ".gb-text-head001{font-family:'Inter', sans-serif;font-size:clamp(2rem, 5vw, 3rem);font-weight:700;line-height:1.2;letter-spacing:-0.02em}"
}
```

### Auto Layout to Flexbox

**Figma Auto Layout:**
- Direction: Horizontal
- Gap: 24px
- Padding: 32px
- Align: Center

**GenerateBlocks:**
```json
{
  "styles": {
    "display": "flex",
    "flexDirection": "row",
    "gap": "1.5rem",
    "padding": "2rem",
    "alignItems": "center"
  },
  "css": ".gb-element-row001{display:flex;flex-direction:row;gap:1.5rem;padding:2rem;align-items:center}"
}
```

### Grid Layout

**Figma Grid (3 columns, 24px gap):**

**GenerateBlocks:**
```json
{
  "styles": {
    "display": "grid",
    "gridTemplateColumns": "repeat(3, 1fr)",
    "gap": "1.5rem"
  },
  "css": ".gb-element-grid001{display:grid;grid-template-columns:repeat(3, 1fr);gap:1.5rem}@media(max-width:1024px){.gb-element-grid001{grid-template-columns:repeat(2, 1fr)}}@media(max-width:768px){.gb-element-grid001{grid-template-columns:1fr}}"
}
```

### Shadow Conversion

**Figma Shadow:**
- X: 0, Y: 20px
- Blur: 60px
- Color: rgba(0, 0, 0, 0.15)

**GenerateBlocks:**
```json
{
  "styles": {
    "boxShadow": "0 20px 60px rgba(0,0,0,0.15)"
  },
  "css": ".gb-element-card001{box-shadow:0 20px 60px rgba(0,0,0,0.15)}"
}
```

### Border Radius

**Figma:** Corner radius: 16px

**GenerateBlocks:**
```json
{
  "styles": {
    "borderRadius": "1rem"
  },
  "css": ".gb-element-card001{border-radius:1rem}"
}
```

## Responsive Conversion

Figma designs are typically at desktop width. Add responsive breakpoints:

### Breakpoint Strategy

| Figma Width | Target | Media Query |
|-------------|--------|-------------|
| 1440px | Desktop | Base styles |
| 1024px | Tablet | `@media(max-width:1024px)` |
| 768px | Mobile landscape | `@media(max-width:768px)` |
| 375px | Mobile | `@media(max-width:480px)` |

### Font Size Scaling

Convert fixed Figma sizes to fluid typography:

| Figma Size | GenerateBlocks |
|------------|----------------|
| 64px | `clamp(2.5rem, 5vw, 4rem)` |
| 48px | `clamp(2rem, 4vw, 3rem)` |
| 36px | `clamp(1.75rem, 3vw, 2.25rem)` |
| 24px | `clamp(1.25rem, 2vw, 1.5rem)` |
| 18px | `1.125rem` |
| 16px | `1rem` |
| 14px | `0.875rem` |

### Spacing Scaling

| Figma Spacing | GenerateBlocks |
|---------------|----------------|
| 80px | `4rem` (desktop), `2rem` (mobile) |
| 60px | `3rem` (desktop), `1.5rem` (mobile) |
| 40px | `2rem` (desktop), `1rem` (mobile) |
| 24px | `1.5rem` |
| 16px | `1rem` |
| 8px | `0.5rem` |

## Common Figma Patterns

### Hero Section

**Figma structure:**
```
Frame (Hero)
├── Frame (Content)
│   ├── Text (Tagline)
│   ├── Text (Headline)
│   ├── Text (Description)
│   └── Frame (Buttons)
│       ├── Button (Primary)
│       └── Button (Secondary)
└── Image (Hero Image)
```

**GenerateBlocks:**
```html
<!-- wp:generateblocks/element {"uniqueId":"hero001","tagName":"section","styles":{"paddingTop":"4rem","paddingBottom":"4rem"},"css":".gb-element-hero001{padding-top:4rem;padding-bottom:4rem}@media(max-width:768px){.gb-element-hero001{padding-top:2rem;padding-bottom:2rem}}"} -->
<section class="gb-element gb-element-hero001">
    <!-- wp:generateblocks/element {"uniqueId":"hero002","tagName":"div","styles":{"maxWidth":"1200px","marginLeft":"auto","marginRight":"auto","paddingLeft":"1rem","paddingRight":"1rem","display":"grid","gridTemplateColumns":"1fr 1fr","gap":"3rem","alignItems":"center"},"css":".gb-element-hero002{max-width:1200px;margin-left:auto;margin-right:auto;padding-left:1rem;padding-right:1rem;display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:center}@media(max-width:768px){.gb-element-hero002{grid-template-columns:1fr;text-align:center}}"} -->
    <div class="gb-element gb-element-hero002">
        <!-- wp:generateblocks/element {"uniqueId":"hero003","tagName":"div","styles":{"display":"flex","flexDirection":"column","gap":"1.5rem"},"css":".gb-element-hero003{display:flex;flex-direction:column;gap:1.5rem}"} -->
        <div class="gb-element gb-element-hero003">
            <!-- Tagline, Headline, Description, Buttons -->
        </div>
        <!-- /wp:generateblocks/element -->
        <!-- wp:generateblocks/media ... -->
    </div>
    <!-- /wp:generateblocks/element -->
</section>
<!-- /wp:generateblocks/element -->
```

### Card Component

**Figma structure:**
```
Frame (Card)
├── Image
├── Frame (Content)
│   ├── Text (Title)
│   ├── Text (Description)
│   └── Link (Read more)
```

**GenerateBlocks (clickable card):**
```html
<!-- wp:generateblocks/text {"uniqueId":"card001","tagName":"a","htmlAttributes":[{"attribute":"href","value":"/link/"}],"styles":{"display":"flex","flexDirection":"column","backgroundColor":"white","borderRadius":"1rem","overflow":"hidden","textDecoration":"none","border":"1px solid #e5e5e5"},"css":".gb-text-card001{display:flex;flex-direction:column;background-color:white;border-radius:1rem;overflow:hidden;text-decoration:none;border:1px solid #e5e5e5;transition:all 0.3s}.gb-text-card001:hover{transform:translateY(-6px);box-shadow:0 20px 60px rgba(0,0,0,0.15);border-color:transparent}"} -->
<a class="gb-text gb-text-card001" href="/link/">
    <!-- wp:generateblocks/media {"uniqueId":"card002","mediaType":"image","htmlAttributes":[{"attribute":"src","value":"image.jpg"},{"attribute":"alt","value":"Card image"}],"styles":{"width":"100%","aspectRatio":"16/9","objectFit":"cover"},"css":".gb-media-card002{width:100%;aspect-ratio:16/9;object-fit:cover}"} -->
    <img class="gb-media gb-media-card002" src="image.jpg" alt="Card image" />
    <!-- /wp:generateblocks/media -->
    <!-- wp:generateblocks/element {"uniqueId":"card003","tagName":"div","styles":{"padding":"1.5rem","display":"flex","flexDirection":"column","gap":"0.75rem"},"css":".gb-element-card003{padding:1.5rem;display:flex;flex-direction:column;gap:0.75rem}"} -->
    <div class="gb-element gb-element-card003">
        <!-- Title, Description -->
    </div>
    <!-- /wp:generateblocks/element -->
</a>
<!-- /wp:generateblocks/text -->
```

### Navigation Bar

**Figma structure:**
```
Frame (Nav)
├── Logo
├── Frame (Links)
│   ├── Link
│   ├── Link
│   └── Link
└── Button (CTA)
```

**GenerateBlocks:**
```html
<!-- wp:generateblocks/element {"uniqueId":"nav001","tagName":"header","styles":{"display":"flex","justifyContent":"space-between","alignItems":"center","padding":"1rem 0"},"css":".gb-element-nav001{display:flex;justify-content:space-between;align-items:center;padding:1rem 0}"} -->
<header class="gb-element gb-element-nav001">
    <!-- Logo -->
    <!-- wp:generateblocks/element {"uniqueId":"nav002","tagName":"nav","styles":{"display":"flex","gap":"2rem"},"css":".gb-element-nav002{display:flex;gap:2rem}@media(max-width:768px){.gb-element-nav002{display:none}}"} -->
    <nav class="gb-element gb-element-nav002">
        <!-- Navigation links -->
    </nav>
    <!-- /wp:generateblocks/element -->
    <!-- CTA Button -->
</header>
<!-- /wp:generateblocks/element -->
```

## Color Extraction

### From Figma Dev Mode

If you have access to Figma Dev Mode, extract:
- Color variables/tokens
- Exact hex/rgba values
- Gradient definitions

### From Screenshot

When analyzing a screenshot:
1. Identify primary brand color (usually buttons, links, accents)
2. Identify text colors (dark for body, lighter for secondary)
3. Identify background colors (white, off-white, dark sections)
4. Note any gradients or overlays

### Default Fallbacks

When colors aren't clear, use these sensible defaults:

**Light theme:**
- Primary: `#c0392b` or `#0073e6`
- Text: `#0a0a0a`
- Muted: `#5c5c5c`
- Background: `#ffffff`
- Light background: `#f5f5f3`
- Border: `#e5e5e5`

**Dark theme:**
- Primary: `#e74c3c` or `#3498db`
- Text: `#ffffff`
- Muted: `#a0a0a0`
- Background: `#0a0a0a`
- Card background: `#1a1a1a`
- Border: `#333333`

## Hover States

Figma designs often show only the default state. Add these hover effects:

### Buttons
```css
.gb-text-btn001:hover{background-color:#a33024;transform:translateY(-2px);box-shadow:0 4px 12px rgba(192,57,43,0.3)}
```

### Cards
```css
.gb-text-card001:hover{transform:translateY(-6px);box-shadow:0 20px 60px rgba(0,0,0,0.15);border-color:transparent}
```

### Links
```css
.gb-text-link001:hover{color:#c0392b;text-decoration:underline}
```

### Icons
```css
.parent:hover .gb-element-icon001{background-color:#c0392b;color:white;transform:scale(1.05)}
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
- `<!-- wp:cover {...} -->` and `<!-- /wp:cover -->`
- Any other `<!-- wp:{namespace}/{block} -->` format

**WRONG - These will break the block editor:**
```html
<!-- Hero Section -->
<!-- Card component -->
<!-- Converted from Figma -->
<!-- Navigation -->
```

**CORRECT - Only block delimiters:**
```html
<!-- wp:generateblocks/element {"uniqueId":"hero001",...} -->
<section class="gb-element gb-element-hero001">
    <!-- wp:generateblocks/text {"uniqueId":"hero002",...} -->
    <h1 class="gb-text gb-text-hero002">Heading</h1>
    <!-- /wp:generateblocks/text -->
</section>
<!-- /wp:generateblocks/element -->
```

Any extra HTML comments will **break the WordPress block editor** and cause parsing errors. This is non-negotiable.

## Other Critical Rules

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

### 2. Both styles AND css Required

Always include both attributes:
```json
{
  "styles": {"padding": "2rem"},
  "css": ".gb-element-id{padding:2rem}"
}
```

### 2. Minified CSS

No line breaks in css attribute:
```css
.gb-element-id{padding:2rem;background:#fff}.gb-element-id:hover{background:#f5f5f5}
```

### 3. Unique IDs

Format: `{section}{number}{letter}`
- `hero001`, `hero001a`, `hero001b`
- `card023`, `card023a`

### 4. Always Add Transitions

For interactive elements:
```css
transition:all 0.3s
```

### 5. Test Responsive

Always add media queries for:
- Tablet: `@media(max-width:1024px)`
- Mobile: `@media(max-width:768px)`

### 6. Icon Containers Need `line-height: 1`

Elements presenting icons must have `lineHeight: "1"` to prevent extra spacing:
```json
{"styles": {"lineHeight": "1", "display": "flex", "alignItems": "center"}}
```

### 7. Lists Use `core/list` with `.list` Class

Convert Figma list designs to native WordPress list block:
```html
<!-- wp:list {"className":"list"} -->
<ul class="wp-block-list list">...</ul>
<!-- /wp:list -->
```

### 8. Container Width with CSS Variable

Use `--gb-container-width` for inner container width and `align: "full"` on parent section:
```json
{"align": "full", "styles": {"maxWidth": "var(--gb-container-width)"}}
```

## Image Handling

### Placeholder Images

When Figma shows placeholder images, use:
```json
{
  "htmlAttributes": [
    {"attribute": "src", "value": "https://placehold.co/800x600/f5f5f3/5c5c5c?text=Image"},
    {"attribute": "alt", "value": "Descriptive alt text"},
    {"attribute": "width", "value": "800"},
    {"attribute": "height", "value": "600"},
    {"attribute": "loading", "value": "lazy"}
  ]
}
```

### Aspect Ratios

Common Figma image ratios:
| Ratio | Use Case | CSS |
|-------|----------|-----|
| 16:9 | Hero, video thumbnails | `aspect-ratio:16/9` |
| 4:3 | Blog cards, features | `aspect-ratio:4/3` |
| 1:1 | Avatars, icons | `aspect-ratio:1/1` |
| 3:2 | Product images | `aspect-ratio:3/2` |

## Output Format

When converting, provide:

1. **Complete block code** - Ready to paste into WordPress
2. **Section-by-section** - For complex designs, break into chunks
3. **Mobile considerations** - Note any responsive adjustments made
4. **Image placeholders** - Indicate where user should replace images
5. **Content placeholders** - Mark text that needs customization
