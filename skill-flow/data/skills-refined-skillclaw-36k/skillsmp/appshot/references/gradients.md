# Gradient Presets

24 built-in gradient presets organized by category.

## Warm

| ID | Name | Colors | Direction |
|----|------|--------|-----------|
| `sunset` | Sunset | #FF5733 → #FFC300 | top-bottom |
| `sunrise` | Sunrise | #F37335 → #FDC830 | diagonal |
| `autumn` | Autumn | #D38312 → #A83279 | top-bottom |
| `peach` | Peach | #FFCCCC → #FF6B6B | top-bottom |

## Cool

| ID | Name | Colors | Direction |
|----|------|--------|-----------|
| `ocean` | Ocean | #0077BE → #33CCCC | top-bottom |
| `arctic` | Arctic | #72EDF2 → #5151E5 | diagonal |
| `mint` | Mint | #00B09B → #96C93D | left-right |
| `lavender` | Lavender | #9796F0 → #FBC7D4 | top-bottom |

## Vibrant

| ID | Name | Colors | Direction |
|----|------|--------|-----------|
| `rainbow` | Rainbow | #FF0080 → #FF8C00 → #40E0D0 | left-right |
| `neon` | Neon | #FF006E → #8338EC → #3A86FF | diagonal |
| `tropical` | Tropical | #FA709A → #FEE140 | top-bottom |
| `candy` | Candy | #FF61D2 → #FE9090 → #FFCC5C | left-right |

## Subtle

| ID | Name | Colors | Direction |
|----|------|--------|-----------|
| `pastel` | Pastel | #E8D8F5 → #D6E6FF | top-bottom |
| `mist` | Mist | #E0EAFC → #CFDEF3 | top-bottom |
| `pearl` | Pearl | #F5F5F5 → #E8E8E8 → #F0F0F0 | diagonal |
| `cloud` | Cloud | #FFFFFF → #F0F0F0 | top-bottom |

## Monochrome

| ID | Name | Colors | Direction |
|----|------|--------|-----------|
| `noir` | Noir | #000000 → #434343 | top-bottom |
| `graphite` | Graphite | #283048 → #859398 | diagonal |
| `charcoal` | Charcoal | #1C1C1C → #494949 | top-bottom |
| `silver` | Silver | #B8B8B8 → #E8E8E8 | diagonal |

## Brand

| ID | Name | Colors | Direction |
|----|------|--------|-----------|
| `instagram` | Instagram | #833AB4 → #FD1D1D → #FCB045 | diagonal |
| `twitter` | Twitter Blue | #1DA1F2 → #14171A | top-bottom |
| `spotify` | Spotify | #1DB954 → #191414 | diagonal |
| `apple` | Apple | #A1C4FD → #C2E9FB | diagonal |

## Usage

To apply a gradient:
```
appshot_gradients with action: "apply", preset: "<id>"
```

To list gradients by category:
```
appshot_gradients with action: "list", category: "warm"
```
