# 3D Icon & Asset Strategy

Based on the provided references, the ArtFrost portfolio utilizes high-fidelity 3D renders instead of flat 2D icons for major visual anchors.

> Important: This does **not** ban flat icons. Flat UI icons (navigation, social links, buttons, small badges) are expected and encouraged for clarity.

## Style Guide for Generation
*   **Material**: Metallic green, frosted glass, semi-transparent plastic.
*   **Lighting**: Dramatic rim lighting, neon green ambient glow.
*   **Background**: Transparent (isolate object).
*   **Vibe**: Futuristic, Software, Stability, "Frost/Crystal" aesthetics allowed.

## Icon Manifest & Placement

| Location | Icon/Asset Concept | Description |
| :--- | :--- | :--- |
| **Hero Section (Right)** | **"The Core Star"** | Large, abstract 6 or 8-pointed 3D star or geometric knot. Metallic green finish with soft edges. Represents "Innovation & Core Skills". |
| **Value Prop / Features** | **"Floating Layers"** | Stacked glass sheets or floating interface panels. Represents "Software Development / UI/UX". |
| **About Me** | **"Abstract Avatar"** | A stylized glass bust or a floating creative sphere with "frost" particles. Represents the "ArtFrost" persona. |
| **Services - Dev** | **"Code Cube"** | A glossy cube with brackets `{}` glowing inside or embossed. |
| **Services - Design** | **"Fluid Droplet"** | A solidified, metallic liquid shape. Represents creativity and flow. |
| **Contact / CTA** | **"Communication Orb"** | A glowing orb or 3D mail envelope with glass texture. |

## Implementation Note
When implementing:
1.  Place these assets on `z-index: 10`.
2.  Add a generic radial gradient glow (color: `#10B981`, opacity: `0.2`) *behind* the image in CSS to integrate it into the dark background.
3.  Keep 3D assets optimized (WebP/AVIF, sensible dimensions) to respect the performance budget; avoid huge PNGs.
4.  Provide meaningful `alt` text when the asset is informative; use empty alt (`""`) when purely decorative.
