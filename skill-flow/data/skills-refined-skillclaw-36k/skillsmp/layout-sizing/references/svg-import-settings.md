# SVG Import Settings

## The Golden Rule

```text
WORLD SIZE = TEXTURE SIZE / PPU
PPU = 100 (ALWAYS)
Therefore: TEXTURE SIZE = WORLD SIZE x 100
```

## Standard Settings

| Asset  | World Size | Texture Size | PPU |
| ------ | ---------- | ------------ | --- |
| Tiles  | 2.0        | 200          | 100 |
| Tokens | 0.4        | 40           | 100 |

## Unity Import Settings

For all game SVGs:

| Setting                   | Value                  |
| ------------------------- | ---------------------- |
| Generated Asset Type      | Texture2D              |
| Keep Texture Aspect Ratio | Yes                    |
| **Pixels Per Unit**       | **100** (NEVER CHANGE) |
| **Texture Size**          | World Size x 100       |

## Common Mistakes

- **Changing PPU** - WRONG. Always 100.
- **Matching Texture Size to viewBox** - WRONG. Use world size x 100.
- **Using default Texture Size (256)** - WRONG. Calculate correct value.
- **Editing .meta files directly** - WRONG. Use Unity Inspector.

## Quick Reference

```text
PPU = 100 (ALWAYS)
Texture Size = World Size x 100

Tiles:  2.0 world units → Texture Size = 200
Tokens: 0.4 world units → Texture Size = 40
```
