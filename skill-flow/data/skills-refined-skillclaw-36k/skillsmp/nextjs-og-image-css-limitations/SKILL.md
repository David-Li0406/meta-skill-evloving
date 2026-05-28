---
name: nextjs-og-image-css-limitations
description: |
  Fix for Next.js OG image build errors with invalid CSS display values. Use when:
  (1) Build fails with "Invalid value for CSS property display", (2) error mentions
  allowed values "flex" | "block" | "none" | "-webkit-box", (3) using display: inline-block
  or other CSS display values in next/og ImageResponse components. The fix is to use
  display: flex with alignSelf: flex-start instead of inline-block.
author: Claude Code
version: 1.0.0
date: 2026-01-21
---

# Next.js OG Image CSS Limitations

## Problem
Next.js `next/og` ImageResponse uses Satori for rendering, which only supports a subset
of CSS. Using unsupported `display` values like `inline-block` causes build failures
during static generation.

## Context / Trigger Conditions
- Build error: `Error occurred prerendering page "/opengraph-image"`
- Error message: `Invalid value for CSS property "display". Allowed values: "flex" | "block" | "none" | "-webkit-box". Received: "inline-block"`
- Files affected: `opengraph-image.tsx`, `twitter-image.tsx`, or similar OG image routes
- Using `next/og` ImageResponse component

## Solution

### Replace inline-block with flex + alignSelf

**Before (causes error):**
```tsx
<div
  style={{
    display: 'inline-block',
    padding: '10px 24px',
    background: '#FFCC00',
    width: 'fit-content',  // Also not supported
  }}
>
  Badge Text
</div>
```

**After (works):**
```tsx
<div
  style={{
    display: 'flex',
    padding: '10px 24px',
    background: '#FFCC00',
    alignSelf: 'flex-start',  // Prevents stretching to full width
  }}
>
  Badge Text
</div>
```

### Allowed display values
- `flex` - Most versatile, use with flexbox properties
- `block` - Simple block element
- `none` - Hide element
- `-webkit-box` - Legacy flexbox (rarely needed)

### Other CSS limitations to watch for
- `width: fit-content` - Not supported, use `alignSelf: flex-start` instead
- `grid` - Not supported, use nested flex containers
- `inline`, `inline-flex` - Not supported
- Complex selectors - Not supported, inline styles only

## Verification
- Run `npm run build` or `next build`
- No errors during static page generation
- OG image routes generate successfully
- Preview OG images at `/opengraph-image` or using OG debugger tools

## Example

Full working OG image component:

```tsx
import { ImageResponse } from 'next/og'

export const runtime = 'nodejs'

export default function OpengraphImage() {
  return new ImageResponse(
    <div
      style={{
        height: '100%',
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        background: '#FFFEF5',
        padding: '60px 80px',
      }}
    >
      {/* Badge - use flex + alignSelf instead of inline-block */}
      <div
        style={{
          display: 'flex',
          padding: '10px 24px',
          background: '#FFCC00',
          border: '4px solid #1a1a1a',
          fontSize: '20px',
          fontWeight: 700,
          alignSelf: 'flex-start',  // Key: prevents full-width stretch
        }}
      >
        CASE STUDY
      </div>

      {/* Title */}
      <div
        style={{
          fontSize: '72px',
          fontWeight: 900,
          color: '#1a1a1a',
          marginTop: '24px',
        }}
      >
        Project Title
      </div>
    </div>,
    {
      width: 1200,
      height: 630,
    }
  )
}
```

## Notes
- Satori (used by next/og) is designed for server-side rendering to images
- It intentionally limits CSS to ensure consistent cross-platform rendering
- Complex layouts should use nested flex containers
- Fonts must be loaded explicitly in the ImageResponse options
- Testing locally with `next dev` may not catch all issues; always test with `next build`

## References
- [Next.js OG Image Generation](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image)
- [Satori (underlying library)](https://github.com/vercel/satori)
- [Satori Supported CSS](https://github.com/vercel/satori#css)
