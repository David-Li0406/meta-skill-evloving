---
name: creating-opengraph-images
description: Use this skill when you need to generate dynamic OpenGraph and Twitter share images for Next.js applications, enhancing social media sharing with custom designs.
---

# Creating OpenGraph Images for Next.js

Generate dynamic OpenGraph (1200x630) and Twitter (1200x600) images using `next/og` ImageResponse.

## Quick Start

Create `app/opengraph-image.tsx`:

```tsx
import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "Page Title - Site Description";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image() {
  return new ImageResponse(
    (
      <div style={{
        height: "100%",
        width: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(145deg, #0a0a12 0%, #0f1218 50%, #0a0a12 100%)",
        fontFamily: "system-ui, -apple-system, sans-serif",
      }}>
        <h1 style={{ fontSize: 64, color: "#ffffff", margin: 0 }}>
          Page Title
        </h1>
      </div>
    ),
    { ...size }
  );
}
```

## File Naming Convention

| File | Purpose | Dimensions |
|------|---------|------------|
| `opengraph-image.tsx` | Facebook, LinkedIn, iMessage | 1200×630 |
| `twitter-image.tsx` | Twitter/X cards | 1200×600 |

Place in route directory (e.g., `app/about/opengraph-image.tsx` for `/about`).

## Design Patterns

### Gradient Backgrounds

```tsx
background: "linear-gradient(145deg, #0a0a12 0%, #0f1218 35%, #121620 65%, #0a0a12 100%)"
```

### Glowing Orbs (Depth Effect)

```tsx
<div style={{
  position: "absolute",
  top: -150,
  left: -100,
  width: 500,
  height: 500,
  borderRadius: "50%",
  background: "radial-gradient(circle, rgba(34,211,238,0.15) 0%, transparent 60%)",
  display: "flex",
}} />
```

### Gradient Text

```tsx
<h1 style={{
  fontSize: 62,
  fontWeight: 800,
  background: "linear-gradient(135deg, #ffffff 0%, #e2e8f0 50%, #94a3b8 100%)",
  backgroundClip: "text",
  color: "transparent",
  display: "flex",
}}>Title</h1>
```

### SVG Icons with Gradients

```tsx
<svg width="200" height="200" viewBox="0 0 100 100" fill="none"
  style={{ filter: "drop-shadow(0 0 24px rgba(34,211,238,0.35))" }}>
  <defs>
    <linearGradient id="grad" x1="0%" ...
```