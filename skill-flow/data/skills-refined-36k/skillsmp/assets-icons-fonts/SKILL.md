---
name: assets-icons-fonts
description: Optimization and usage of SVGs, fonts, and static assets.
---

# Icons, Fonts & Assets

## When to use this skill
- Adding icons (SVG, Lucide, FontAwesome).
- Loading custom fonts (Google Fonts, local WOFF2).
- Optimizing images.

## 1. Icons
- **SVG**: Prefer inline SVGs or Sprites over font icons for accessibility and performance.
- **React**: Use libraries like `lucide-react` or `heroicons` that treeshake well.
- **Attributes**: Always set `aria-hidden="true"` for decorative icons, or providing decent `aria-label`.

## 2. Fonts
- **Format**: Use `WOFF2` for local fonts.
- **Loading**: Use `font-display: swap;` in CSS to show fallback text immediately.
- **Next.js**: Use `next/font` to optimize Google Fonts and eliminate layout shift (CLS).

## 3. Images
- **Formats**: Prefer WebP or AVIF over PNG/JPEG.
- **Sizing**: Always specify `width` and `height` attributes (or aspect ratio) to prevent layout shifts.
- **Lazy Loading**: Use `loading="lazy"` for below-the-fold images.
