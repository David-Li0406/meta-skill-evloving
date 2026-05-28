---
title: SVG Icons Reference
description: Shape block patterns and inline SVG techniques for GenerateBlocks
---

# SVG Icons Reference

Three approaches for icons in GenerateBlocks V2:

1. **Shape Block** - `generateblocks/shape` for standalone SVG icons
2. **Inline SVG** - SVG inside text blocks (buttons, links)
3. **Icon Fonts** - CSS icon classes (md-icon-*)

---

## 1. Shape Block (`generateblocks/shape`)

Best for: Standalone icons, decorative elements, complex SVGs.

### Basic Structure

```html
<!-- wp:generateblocks/shape {"uniqueId":"icon001","styles":{"width":"1.5rem","height":"1.5rem"},"css":".gb-shape-icon001{width:1.5rem;height:1.5rem}.gb-shape-icon001 svg{width:100%;height:100%;fill:currentColor}"} -->
<span class="gb-shape gb-shape-icon001">
    <svg viewBox="0 0 24 24">
        <path d="..."/>
    </svg>
</span>
<!-- /wp:generateblocks/shape -->
```

### CSS Targeting Pattern

```css
/* Wrapper span - size and positioning */
.gb-shape-icon001 {
    width: 1.5rem;
    height: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* SVG element - fill, stroke */
.gb-shape-icon001 svg {
    width: 100%;
    height: 100%;
    fill: currentColor;
}
```

### Examples

**Arrow Icon:**
```html
<!-- wp:generateblocks/shape {"uniqueId":"arrow001","styles":{"width":"1rem","height":"1rem","display":"inline-flex"},"css":".gb-shape-arrow001{width:1rem;height:1rem;display:inline-flex}.gb-shape-arrow001 svg{width:100%;height:100%;stroke:currentColor;fill:none}"} -->
<span class="gb-shape gb-shape-arrow001">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <path d="M5 12h14M12 5l7 7-7 7"/>
    </svg>
</span>
<!-- /wp:generateblocks/shape -->
```

**Filled Icon with Color:**
```html
<!-- wp:generateblocks/shape {"uniqueId":"heart001","styles":{"width":"2rem","height":"2rem","color":"#c0392b"},"css":".gb-shape-heart001{width:2rem;height:2rem;color:#c0392b;transition:all 0.3s}.gb-shape-heart001 svg{width:100%;height:100%;fill:currentColor}.gb-shape-heart001:hover{transform:scale(1.1)}"} -->
<span class="gb-shape gb-shape-heart001">
    <svg viewBox="0 0 24 24">
        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="currentColor"/>
    </svg>
</span>
<!-- /wp:generateblocks/shape -->
```

**Stroke Icon (Lucide style):**
```html
<!-- wp:generateblocks/shape {"uniqueId":"check001","styles":{"width":"1.25rem","height":"1.25rem","color":"#22c55e"},"css":".gb-shape-check001{width:1.25rem;height:1.25rem;color:#22c55e}.gb-shape-check001 svg{width:100%;height:100%;stroke:currentColor;stroke-width:2.5;fill:none;stroke-linecap:round;stroke-linejoin:round}"} -->
<span class="gb-shape gb-shape-check001">
    <svg viewBox="0 0 24 24" fill="none">
        <polyline points="20 6 9 17 4 12"/>
    </svg>
</span>
<!-- /wp:generateblocks/shape -->
```

**Icon with Background:**
```html
<!-- wp:generateblocks/shape {"uniqueId":"star001","styles":{"width":"3rem","height":"3rem","display":"flex","alignItems":"center","justifyContent":"center","backgroundColor":"#f5f5f3","borderRadius":"0.75rem","color":"#c0392b"},"css":".gb-shape-star001{width:3rem;height:3rem;display:flex;align-items:center;justify-content:center;background-color:#f5f5f3;border-radius:0.75rem;color:#c0392b;transition:all 0.3s}.gb-shape-star001 svg{width:1.5rem;height:1.5rem;fill:currentColor}.gb-shape-star001:hover{background-color:#c0392b;color:white}"} -->
<span class="gb-shape gb-shape-star001">
    <svg viewBox="0 0 24 24">
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" fill="currentColor"/>
    </svg>
</span>
<!-- /wp:generateblocks/shape -->
```

---

## 2. Inline SVG in Text Blocks

Best for: Icons inside buttons, links with arrow icons.

### Button with Arrow

```html
<!-- wp:generateblocks/text {"uniqueId":"btn001","tagName":"a","htmlAttributes":[{"attribute":"href","value":"/services/"}],"styles":{"display":"inline-flex","alignItems":"center","gap":"0.75rem","padding":"0.75rem 1.25rem","fontSize":"0.9375rem","fontWeight":"600","color":"#0a0a0a","border":"2px solid #e5e5e5","borderRadius":"2rem","textDecoration":"none"},"css":".gb-text-btn001{display:inline-flex;align-items:center;gap:0.75rem;padding:0.75rem 1.25rem;font-size:0.9375rem;font-weight:600;color:#0a0a0a;border:2px solid #e5e5e5;border-radius:2rem;text-decoration:none;transition:all 0.3s}.gb-text-btn001:hover{border-color:#c0392b;color:#c0392b}.gb-text-btn001 svg{width:1rem;height:1rem;transition:transform 0.3s}.gb-text-btn001:hover svg{transform:translateX(4px)}"} -->
<a class="gb-text gb-text-btn001" href="/services/">View all services<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
<!-- /wp:generateblocks/text -->
```

### Badge with Icon

```html
<!-- wp:generateblocks/text {"uniqueId":"badge001","tagName":"span","styles":{"display":"inline-flex","alignItems":"center","gap":"0.375rem","padding":"0.375rem 0.75rem","background":"#16a34a","borderRadius":"2rem","fontSize":"0.75rem","fontWeight":"700","textTransform":"uppercase","letterSpacing":"0.03em","color":"white"},"css":".gb-text-badge001{display:inline-flex;align-items:center;gap:0.375rem;padding:0.375rem 0.75rem;background:#16a34a;border-radius:2rem;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.03em;color:white}.gb-text-badge001 svg{width:0.75rem;height:0.75rem}"} -->
<span class="gb-text gb-text-badge001"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>Most Popular</span>
<!-- /wp:generateblocks/text -->
```

### Link with External Icon

```html
<!-- wp:generateblocks/text {"uniqueId":"ext001","tagName":"a","htmlAttributes":[{"attribute":"href","value":"https://example.com"},{"attribute":"target","value":"_blank"},{"attribute":"rel","value":"noopener"}],"styles":{"display":"inline-flex","alignItems":"center","gap":"0.25rem","color":"#c0392b","textDecoration":"none"},"css":".gb-text-ext001{display:inline-flex;align-items:center;gap:0.25rem;color:#c0392b;text-decoration:none;transition:all 0.3s}.gb-text-ext001:hover{text-decoration:underline}.gb-text-ext001 svg{width:0.875rem;height:0.875rem}"} -->
<a class="gb-text gb-text-ext001" href="https://example.com" target="_blank" rel="noopener">Visit site<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/></svg></a>
<!-- /wp:generateblocks/text -->
```

---

## 3. Icon Fonts (md-icon-*)

Best for: Quick icons using existing CSS icon font.

### Using Icon Font Class

```html
<!-- wp:generateblocks/element {"uniqueId":"iconbox001","tagName":"div","styles":{"width":"3rem","height":"3rem","display":"flex","alignItems":"center","justifyContent":"center","backgroundColor":"#c0392b","borderRadius":"0.75rem","color":"#ffffff","fontSize":"1.5rem"},"css":".gb-element-iconbox001{width:3rem;height:3rem;display:flex;align-items:center;justify-content:center;background-color:#c0392b;border-radius:0.75rem;color:#ffffff;font-size:1.5rem}"} -->
<div class="gb-element gb-element-iconbox001">
    <i class="md-icon-bolt" aria-hidden="true"></i>
</div>
<!-- /wp:generateblocks/element -->
```

### Icon Font in Link

```html
<!-- wp:generateblocks/text {"uniqueId":"social001","tagName":"a","htmlAttributes":[{"attribute":"href","value":"https://twitter.com/handle"},{"attribute":"aria-label","value":"Follow on Twitter"}],"styles":{"width":"2.5rem","height":"2.5rem","display":"flex","alignItems":"center","justifyContent":"center","backgroundColor":"rgba(255,255,255,0.1)","borderRadius":"50%","color":"#ffffff","fontSize":"1.25rem","textDecoration":"none"},"css":".gb-text-social001{width:2.5rem;height:2.5rem;display:flex;align-items:center;justify-content:center;background-color:rgba(255,255,255,0.1);border-radius:50%;color:#ffffff;font-size:1.25rem;text-decoration:none;transition:all 0.3s}.gb-text-social001:hover{background-color:rgba(255,255,255,0.2);transform:translateY(-2px)}"} -->
<a class="gb-text gb-text-social001" href="https://twitter.com/handle" aria-label="Follow on Twitter"><i class="md-icon-twitter" aria-hidden="true"></i></a>
<!-- /wp:generateblocks/text -->
```

---

## Common SVG Icons (Copy-Ready)

### Arrow Right
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
```

### Check
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
```

### Star (Filled)
```html
<svg viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
```

### External Link
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/></svg>
```

### Bolt/Lightning
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>
```

### Code/Terminal
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4m-5-9 3 3-3 3M14 14h3"/></svg>
```

### Search
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
```

### Edit/Pencil
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 20h9M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z M15 5l3 3"/></svg>
```

### Mail
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
```

### Menu/Hamburger
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>
```

### Close/X
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg>
```

### Chevron Down
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>
```

---

## SVG Best Practices

1. **Always include `viewBox`** - Enables proper scaling
2. **Use `fill="none"` + `stroke`** for line icons
3. **Use `fill="currentColor"`** to inherit text color
4. **Add `aria-hidden="true"`** for decorative icons
5. **Add descriptive `aria-label`** on parent for functional icons
6. **Remove `width`/`height` from SVG** - Control via CSS
7. **Minify paths** - Remove unnecessary whitespace
8. **Use consistent stroke-width** (1.5 or 2 typically)
