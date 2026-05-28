---
title: Troubleshooting Guide
description: Error recovery, chunking strategies, and debugging for complex GenerateBlocks layouts
---

# Troubleshooting Guide

Solutions for common issues when building GenerateBlocks layouts.

## "Attempt Recovery" Errors

This error typically occurs when:
1. JSON attributes are too long or complex
2. Deeply nested structures confuse parsing
3. Special characters break JSON encoding

### Solutions

**1. Simplify CSS Attribute**

Split complex CSS into multiple blocks instead of one massive string:

```css
/* Instead of this (500+ chars) */
.gb-element-id{prop1;prop2;prop3;...many more...}.gb-element-id:hover{...}.gb-element-id::before{...}@media{...}

/* Break into smaller chunks by nesting elements */
```

**2. Use Chunked Generation**

For sections with 20+ blocks, generate in chunks:

```
Chunk 1: Section wrapper + header (3-5 blocks)
Chunk 2: First row of cards (4-6 blocks)
Chunk 3: Second row of cards (4-6 blocks)
Chunk 4: Footer/CTA area (2-4 blocks)
```

**3. Escape Special Characters**

In `css` attribute, escape:
- Single quotes: Use `'` not `"`
- Content property: `content:''` or `content:'→'`
- URLs: Encode special characters

**4. Validate JSON Before Output**

Ensure:
- All quotes are properly escaped
- No trailing commas
- Brackets match

---

## Chunking Strategy for Complex Layouts

### Planning Phase

1. **Map the structure** - List all components before coding
2. **Identify nesting levels** - Max 4-5 levels deep
3. **Group related blocks** - Cards, stats, etc.
4. **Estimate block count** - Plan chunks if >20 blocks

### Example: Services Section (50+ blocks)

```
Section: Services
├── Container (sect001)
│   ├── Inner (sect002)
│   │   ├── Trust Block (trust001-trust010) → CHUNK 1
│   │   ├── Header (head001-head003) → CHUNK 2
│   │   └── Grid (grid001) → CHUNK 3 wrapper
│   │       ├── Featured Card (feat001-feat008) → CHUNK 4
│   │       ├── Cards 1-4 (card001-card016) → CHUNK 5
│   │       └── Cards 5-8 (card017-card032) → CHUNK 6
```

### Chunked Output Format

**Chunk 1: Trust Block**
```html
<!-- CHUNK 1: Trust Block -->
<!-- wp:generateblocks/element {"uniqueId":"trust001"...} -->
...
<!-- /wp:generateblocks/element -->
<!-- END CHUNK 1 -->
```

**Chunk 2: Header**
```html
<!-- CHUNK 2: Header -->
<!-- wp:generateblocks/element {"uniqueId":"head001"...} -->
...
<!-- /wp:generateblocks/element -->
<!-- END CHUNK 2 -->
```

### Assembly

After generating all chunks, combine in order with proper nesting.

---

## Common Syntax Errors

### Missing Closing Comments

```html
<!-- WRONG -->
<!-- wp:generateblocks/text {"uniqueId":"txt001"} -->
<p class="gb-text">Text</p>
<!-- Missing closing comment -->

<!-- CORRECT -->
<!-- wp:generateblocks/text {"uniqueId":"txt001"} -->
<p class="gb-text">Text</p>
<!-- /wp:generateblocks/text -->
```

### Mismatched Block Types

```html
<!-- WRONG -->
<!-- wp:generateblocks/element {"uniqueId":"elem001"} -->
<div>Content</div>
<!-- /wp:generateblocks/text -->  <!-- Wrong type -->

<!-- CORRECT -->
<!-- wp:generateblocks/element {"uniqueId":"elem001"} -->
<div>Content</div>
<!-- /wp:generateblocks/element -->
```

### Invalid JSON

```json
// WRONG - trailing comma
{"uniqueId":"id001","styles":{"padding":"1rem",}}

// CORRECT
{"uniqueId":"id001","styles":{"padding":"1rem"}}
```

```json
// WRONG - unescaped quotes in content
{"css":".class{content:"text"}"}

// CORRECT - use single quotes
{"css":".class{content:'text'}"}
```

---

## CSS Debugging

### CSS Not Applying

1. **Check unique ID matches** - Class must match `uniqueId`
2. **Verify minification** - No line breaks in `css` attribute
3. **Check selector format** - `.gb-{type}-{uniqueId}`

```css
/* Element block: */
.gb-element-elem001{...}

/* Text block: */
.gb-text-text001{...}

/* Media block: */
.gb-media-img001{...}

/* Shape block: */
.gb-shape-icon001{...}
```

### Hover Not Working

1. **Include transition** - `transition:all 0.3s`
2. **Check selector** - `.gb-text-card001:hover`
3. **Verify element type** - Can't hover non-interactive elements

### Responsive Not Working

1. **Check breakpoint order** - Desktop first, then tablet, then mobile
2. **Use !important if needed** - For overriding specificity
3. **Verify media query syntax** - `@media(max-width:768px)`

---

## Nesting Issues

### Maximum Nesting Depth

Keep nesting to 4-5 levels max:

```
section (1)
  └── container (2)
        └── grid (3)
              └── card (4)
                    └── content (5) ← MAX
```

### Breaking Deep Nesting

Instead of:
```html
<section>
  <div>
    <div>
      <div>
        <div>
          <div>Content</div>  <!-- Too deep -->
        </div>
      </div>
    </div>
  </div>
</section>
```

Flatten structure:
```html
<section>
  <div class="container">
    <div class="grid">
      <div class="card">Content</div>
    </div>
  </div>
</section>
```

---

## Performance Issues

### Too Many Blocks

**Symptoms:** Slow editor, lag when editing

**Solutions:**
1. Combine related text into single blocks
2. Use reusable patterns/synced patterns
3. Consider query loops for repeated content

### Large CSS Strings

**Symptoms:** Large page size, slow rendering

**Solutions:**
1. Remove redundant properties
2. Use shorthand CSS (`padding` instead of `padding-top/right/bottom/left`)
3. Extract common styles to global classes

---

## Validation Checklist

Before finalizing complex layouts:

- [ ] All blocks have unique IDs
- [ ] All opening comments have matching closings
- [ ] JSON is valid (no trailing commas, proper escaping)
- [ ] CSS selectors match unique IDs
- [ ] Media queries are in correct order
- [ ] Nesting depth ≤ 5 levels
- [ ] No orphaned blocks (all within containers)

---

## Quick Fixes

### Block Not Rendering

```html
<!-- Check: Is content between comments? -->
<!-- wp:generateblocks/text {"uniqueId":"txt001"} -->
<p class="gb-text gb-text-txt001">Content HERE</p>
<!-- /wp:generateblocks/text -->
```

### Styles Not Applying

```html
<!-- Check: Does class match uniqueId? -->
<!-- wp:generateblocks/element {"uniqueId":"box001","css":".gb-element-box001{...}"} -->
<div class="gb-element gb-element-box001">...</div>  <!-- box001 matches -->
<!-- /wp:generateblocks/element -->
```

### Hover Breaking Layout

```css
/* Add transition to prevent layout shift */
.gb-text-card001{transition:transform 0.3s,box-shadow 0.3s}
.gb-text-card001:hover{transform:translateY(-6px)}  /* Only transform, no size change */
```

---

## Getting Help

If issues persist:

1. **Test single block** - Isolate the problematic block
2. **Validate JSON** - Use online JSON validator
3. **Check browser console** - Look for JS errors
4. **Compare with working example** - Use examples folder as reference
