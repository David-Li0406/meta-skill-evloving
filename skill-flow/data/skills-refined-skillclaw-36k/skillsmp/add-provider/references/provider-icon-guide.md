# Provider Icon Guide

Create provider icons that match ClaudeBar's visual style.

## Icon Specifications

| Property | Value |
|----------|-------|
| Format | SVG (source) + PNG (assets) |
| Sizes | 64px (1x), 128px (2x), 192px (3x) |
| Background | Rounded rectangle (rx/ry ~20% of size) |
| Logo size | ~75% of icon, centered |

## SVG Template

Follow ClaudeIcon.svg structure:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">
  <!-- Rounded rectangle background with brand color -->
  <rect fill="#YOUR_COLOR" width="256" height="256" rx="52" ry="52"/>

  <!-- Logo centered and scaled to ~75% -->
  <g transform="translate(32, 32) scale(0.75)">
    <!-- Your logo path here -->
    <path fill="#FFFFFF" d="..."/>
  </g>
</svg>
```

## Brand Colors

| Provider | Background | Logo |
|----------|------------|------|
| Claude | `#CC9B7A` (coral) | `#1F1F1E` (dark) |
| Codex | `#17B8A6` (teal) | `#FFFFFF` (white) |
| Gemini | `#F5A623` (golden) | `#FFFFFF` (white) |
| Copilot | `#24292E` (dark) | `#FFFFFF` (white) |
| Antigravity | `#B85AD6` (purple) | Logo colors |

## File Locations

```
Sources/App/Resources/
├── {Provider}Icon.svg           # Source SVG (keep for reference)
└── Assets.xcassets/
    └── {Provider}Icon.imageset/
        ├── Contents.json
        ├── {provider}_64.png    # 1x
        ├── {provider}_128.png   # 2x
        └── {provider}_192.png   # 3x
```

## Generate PNGs from SVG

Requirements: `rsvg-convert` (install via `brew install librsvg`)

```bash
cd Sources/App/Resources/Assets.xcassets/{Provider}Icon.imageset

# Generate all sizes
rsvg-convert -w 64 -h 64 ../../{Provider}Icon.svg -o {provider}_64.png
rsvg-convert -w 128 -h 128 ../../{Provider}Icon.svg -o {provider}_128.png
rsvg-convert -w 192 -h 192 ../../{Provider}Icon.svg -o {provider}_192.png
```

## Contents.json Template

```json
{
  "images" : [
    {
      "filename" : "{provider}_64.png",
      "idiom" : "universal",
      "scale" : "1x"
    },
    {
      "filename" : "{provider}_128.png",
      "idiom" : "universal",
      "scale" : "2x"
    },
    {
      "filename" : "{provider}_192.png",
      "idiom" : "universal",
      "scale" : "3x"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
```

## Visual Identity Extension

Add to `Sources/App/Views/ProviderVisualIdentity.swift`:

```swift
// MARK: - {Provider}Provider Visual Identity

extension {Provider}Provider: ProviderVisualIdentity {
    public var symbolIcon: String { "sparkles" }  // SF Symbol fallback

    public var iconAssetName: String { "{Provider}Icon" }

    public func themeColor(for scheme: ColorScheme) -> Color {
        scheme == .dark
            ? Color(red: R, green: G, blue: B)  // Dark mode
            : Color(red: R, green: G, blue: B)  // Light mode
    }

    public func themeGradient(for scheme: ColorScheme) -> LinearGradient {
        LinearGradient(
            colors: [
                themeColor(for: scheme),
                scheme == .dark
                    ? Color(red: R2, green: G2, blue: B2)
                    : Color(red: R2, green: G2, blue: B2)
            ],
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        )
    }
}
```

## Quick Script

One-liner to generate all PNGs:

```bash
PROVIDER=MyProvider && LOWER=$(echo $PROVIDER | tr '[:upper:]' '[:lower:]') && \
cd Sources/App/Resources/Assets.xcassets/${PROVIDER}Icon.imageset && \
for s in 64 128 192; do rsvg-convert -w $s -h $s ../../${PROVIDER}Icon.svg -o ${LOWER}_${s}.png; done
```

## Checklist

- [ ] SVG source created with rounded rect background
- [ ] PNG assets generated at 64, 128, 192px
- [ ] Contents.json created in imageset folder
- [ ] ProviderVisualIdentity extension added
- [ ] Build succeeds and icon displays correctly
