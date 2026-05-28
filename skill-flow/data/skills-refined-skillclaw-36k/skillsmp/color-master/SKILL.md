---
name: color-master
description: Convert colors between formats (HEX, RGB, HSL, CMYK, LAB, LCH, oklch, ANSI), generate color harmonies (complementary, triadic, analogous), check accessibility (WCAG contrast), and simulate color blindness. Use when working with colors, design systems, CSS themes.
---

# Color Master

Color conversion, harmony generation, and accessibility checking.

## Setup

```bash
cd <color-master skill directory> && bun install
```

## Usage

```bash
cd <color-master skill directory> && bun run scripts/color.ts <command> <args>
```

## Commands

### convert - Convert to all formats

```bash
bun run scripts/color.ts convert "#f7931a"
bun run scripts/color.ts convert "oklch(0.75 0.16 55)"
```

### harmony - Generate color harmonies

Types: `complementary`, `triadic`, `analogous`, `split-complementary`, `tetradic`, `monochromatic`

```bash
bun run scripts/color.ts harmony "#f7931a" triadic
```

### tints / shades / palette - Generate variations

```bash
bun run scripts/color.ts tints "#f7931a" 5      # lighter
bun run scripts/color.ts shades "#f7931a" 5     # darker
bun run scripts/color.ts palette "#f7931a" 10   # full range
```

### contrast - WCAG accessibility check

```bash
bun run scripts/color.ts contrast "#f7931a" "#ffffff"
```

Returns contrast ratio and WCAG AA/AAA pass/fail status.

### colorblind - Color blindness simulation

```bash
bun run scripts/color.ts colorblind "#f7931a"
```

Simulates: protanopia, deuteranopia, tritanopia, achromatopsia.

### preview / batch-preview - Terminal preview

```bash
bun run scripts/color.ts preview "#f7931a"
bun run scripts/color.ts batch-preview "#f7931a" "#3b82f6" "oklch(0.5 0.2 30)"
bun run scripts/color.ts batch-preview --types=hex,rgb,oklch "#f7931a" "#3b82f6"
```

### terminfo - Detect terminal color capability

```bash
bun run scripts/color.ts terminfo
```

## Supported Formats

HEX, RGB, RGBA, HSL, HSLA, HSV, CMYK, LAB, LCH, oklch, oklab, ANSI 16/256.

See [references/formats.md](references/formats.md) for full format details and ANSI color names.
