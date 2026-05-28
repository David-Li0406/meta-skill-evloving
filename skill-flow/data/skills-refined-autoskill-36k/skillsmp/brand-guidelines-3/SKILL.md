---
name: brand-guidelines
description: Applies EquipQR's brand colors and design-system tokens to any artifact that should match EquipQR's look-and-feel. Use it when brand colors, style guidelines, visual formatting, or EquipQR design standards apply.
license: Complete terms in LICENSE.txt
---

# EquipQR Brand Styling

## Overview

Use this skill whenever Cursor should style an output to look like **EquipQR** (docs, UI mockups, slide decks, diagrams, emails, etc.). It summarizes the **source-of-truth design tokens** used by the EquipQR app so outputs stay consistent with the product.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, EquipQR brand, design tokens, Tailwind, shadcn/ui, visual formatting, visual design

## Brand Guidelines

### Source of truth

- **Design tokens**: `src/index.css` (CSS variables under `:root` and `.dark`)
- **Tailwind mapping**: `tailwind.config.ts` (colors like `primary`, `secondary`, `success`, `info`, `warning`, `destructive`, and `brand` map to CSS variables)

### Colors

EquipQR uses **token-based colors** (HSL triplets) so the same semantic color names work in light and dark mode. Prefer semantic tokens (`brand`, `primary`, `secondary`, `foreground`, `muted-foreground`, etc.) over hard-coded hex values.

**Core (Light mode / `:root`):**

- Background: `0 0% 100%`
- Foreground: `222.2 84% 4.9%`
- Primary (brand): `258 82% 57%`
- Primary foreground (text on primary): `210 40% 98%`
- Secondary: `224 61% 19%`
- Secondary foreground: `210 40% 98%`
- Muted: `210 40% 96.1%`
- Muted foreground: `215.4 16.3% 46.9%`
- Border/Input: `214.3 31.8% 91.4%`

**Status accents (Light mode / `:root`):**

- Success: `142 76% 36%` (foreground `210 40% 98%`)
- Info: `217 91% 60%` (foreground `210 40% 98%`)
- Warning: `38 92% 50%` (foreground `222.2 84% 4.9%`)
- Destructive: `0 84.2% 60.2%` (foreground `210 40% 98%`)

**Dark mode (`.dark`):** Use the same semantic tokens; values shift for contrast.

- Background: `222.2 84% 4.9%`
- Foreground: `210 40% 98%`
- Primary (brand): `258 82% 67%`
- Secondary: `224 61% 29%`
- Muted: `217.2 32.6% 17.5%`
- Muted foreground: `215 20.2% 65.1%`

**Practical usage rules:**

- Use **`brand` / `primary`** for primary calls-to-action and key highlights.
- Use **`secondary`** sparingly (supporting actions, secondary emphasis).
- Use **`muted` + `muted-foreground`** for de-emphasized UI (helper text, subtle separators).
- For alerts/state, use **`success` / `info` / `warning` / `destructive`**; don’t invent new status colors.
- Ensure text contrast by using the paired `*-foreground` token when placing text on a colored background.

### Typography

EquipQR’s UI uses a **clean, product-style system font** approach (no decorative brand fonts required).

- **Recommended stack (web/docs/email)**: `system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`
- **Headings**: Slightly heavier weight (semibold/bold), tighter line-height
- **Body**: Regular weight, comfortable line-height
- **Note**: Prefer consistency and legibility over custom fonts; don’t require font installs for good results.

## Features

### Token-based styling (light + dark)

- Uses semantic tokens (`brand`, `primary`, `foreground`, etc.) instead of hard-coded colors
- Maintains contrast by pairing backgrounds with their `*-foreground` tokens
- Keeps outputs consistent with EquipQR UI in both light and dark themes

### Text Styling

- Keeps clear hierarchy (headline → section header → body)
- Uses foreground/muted-foreground appropriately for emphasis
- Avoids overly dense text blocks; favors scannable layouts

### Shapes, highlights, and accents

- Use `brand`/`primary` for highlights and key shapes (badges, callouts)
- Use status colors only when the shape represents a status/alert
- Prefer subtle neutrals (`border`, `muted`) for non-essential decoration

## Technical Details

### Font Management

- Use a **system font stack** for predictable rendering across environments.
- If a target format supports only a single font choice, pick the closest available system UI font and adjust weight/size for hierarchy.

### Color Application

- For **CSS/Tailwind** outputs, use `hsl(var(--token))` via the semantic color name (e.g. `text-foreground`, `bg-primary`, `bg-brand`, `border-border`).
- For **non-CSS formats** (slides, images, diagrams), convert the HSL tokens from `src/index.css` into the required color space (RGB/HEX) and keep the same semantic mapping.
- Maintain fidelity by referencing the tokens rather than eyeballing colors.