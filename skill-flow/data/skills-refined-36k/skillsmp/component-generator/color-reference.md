# Theme Color Reference

Semantic guide to all theme color tokens and their use cases. This documents **what each token is for**, not the actual color values (which can change in `index.css`).

## Understanding the Token System

### Theme Colors vs Shared Colors

- **Theme colors** change between light/dark mode (require `-dark` suffix in dark mode)
  - Examples: `primary`, `secondary`, `surface`, `outline`
- **Shared colors** stay the same in both modes (no `-dark` suffix needed)
  - Examples: `info`, `success`, `warning`, `danger`

### The "on-*" Pattern

Colors prefixed with `on-*` are designed to be readable **on top of** their paired background:
- `bg-primary` → use `text-on-primary` for text/icons on top
- `bg-surface-dark` → use `text-on-surface-dark` for text/icons on top

## Surface Colors

**Purpose:** Main background and text colors for your app's surface areas.

### `surface`
- **Use for:** Main application background
- **Light mode:** `bg-surface` - Typically a light neutral
- **Dark mode:** `dark:bg-surface-dark` - Typically a dark neutral
- **Example:** Page backgrounds, card backgrounds

### `surface-alt`
- **Use for:** Elevated or alternate surface areas (subtle differentiation from main surface)
- **Light mode:** `bg-surface-alt` - Slightly different from main surface
- **Dark mode:** `dark:bg-surface-dark-alt` - Slightly different from dark surface
- **Example:** Elevated cards, hover states, secondary panels

### `on-surface`
- **Use for:** Text and icons displayed on surface backgrounds
- **Light mode:** `text-on-surface` - Readable on light surface (typically dark)
- **Dark mode:** `dark:text-on-surface-dark` - Readable on dark surface (typically bright)
- **Example:** Body text, paragraph text

### `on-surface-strong`
- **Use for:** Emphasized text on surface backgrounds (higher contrast than `on-surface`)
- **Light mode:** `text-on-surface-strong` - Strong contrast on light surface
- **Dark mode:** `dark:text-on-surface-dark-strong` - Strong contrast on dark surface
- **Example:** Headings, important labels

## Primary Colors

**Purpose:** Main brand color for primary actions and emphasis.

### `primary`
- **Use for:** Primary buttons, primary actions, brand elements
- **Light mode:** `bg-primary`, `border-primary`, `text-primary`
- **Dark mode:** `dark:bg-primary-dark`, `dark:border-primary-dark`, `dark:text-primary-dark`
- **Example:** "Submit" button, primary links, brand highlights

### `on-primary`
- **Use for:** Text and icons on primary colored backgrounds
- **Light mode:** `text-on-primary` - Readable on primary background
- **Dark mode:** `dark:text-on-primary-dark` - Readable on dark primary background
- **Example:** Button text, icon inside primary button

## Secondary Colors

**Purpose:** Secondary brand color for alternative actions.

### `secondary`
- **Use for:** Secondary buttons, alternative actions
- **Light mode:** `bg-secondary`, `border-secondary`, `text-secondary`
- **Dark mode:** `dark:bg-secondary-dark`, `dark:border-secondary-dark`, `dark:text-secondary-dark`
- **Example:** "Cancel" button, secondary navigation

### `on-secondary`
- **Use for:** Text and icons on secondary colored backgrounds
- **Light mode:** `text-on-secondary` - Readable on secondary background
- **Dark mode:** `dark:text-on-secondary-dark` - Readable on dark secondary background
- **Example:** Text inside secondary buttons

## Outline Colors

**Purpose:** Borders and dividers.

### `outline`
- **Use for:** Default borders, dividers, separators
- **Light mode:** `border-outline` - Subtle border on light backgrounds
- **Dark mode:** `dark:border-outline-dark` - Subtle border on dark backgrounds
- **Example:** Input borders, card borders, dividers

### `outline-strong`
- **Use for:** Emphasized borders that need more visibility
- **Light mode:** `border-outline-strong` - Stronger border on light backgrounds
- **Dark mode:** `dark:border-outline-dark-strong` - Stronger border on dark backgrounds
- **Example:** Focused input borders, active selection borders

## Semantic Colors (Shared - Same in Light & Dark)

These colors remain the same in both light and dark modes. **Do NOT add `dark:` variants.**

### `info`
- **Purpose:** Informational messages and actions
- **Usage:** `bg-info`, `border-info`, `text-info`, `text-on-info`
- **Example:** Info alerts, informational badges, help text highlights
- **Note:** No dark mode variant needed - same color in both modes

### `success`
- **Purpose:** Success states, positive feedback, confirmations
- **Usage:** `bg-success`, `border-success`, `text-success`, `text-on-success`
- **Example:** Success messages, completion badges, positive indicators
- **Note:** No dark mode variant needed - same color in both modes

### `warning`
- **Purpose:** Warning states, caution messages
- **Usage:** `bg-warning`, `border-warning`, `text-warning`, `text-on-warning`
- **Example:** Warning alerts, caution badges, attention indicators
- **Note:** No dark mode variant needed - same color in both modes

### `danger`
- **Purpose:** Error states, destructive actions, critical warnings
- **Usage:** `bg-danger`, `border-danger`, `text-danger`, `text-on-danger`
- **Example:** Error messages, delete buttons, validation errors
- **Note:** No dark mode variant needed - same color in both modes

## Border Radius

### `rounded-radius`
- **Purpose:** Standard border radius for most components
- **Usage:** `rounded-radius`
- **When to use:** Buttons, inputs, cards, most interactive elements
- **Exception:** Use `rounded-full` for badges, avatars, pills; `rounded-none` for flush components

## How to Use These Tokens

### Pattern 1: Theme Color with Dark Mode
```tsx
// For components using primary, secondary, surface, or outline
"bg-primary",
"border-primary",
"text-on-primary",
"dark:bg-primary-dark",
"dark:border-primary-dark",
"dark:text-on-primary-dark"
```

### Pattern 2: Shared Color (No Dark Variant)
```tsx
// For components using info, success, warning, or danger
"bg-success",
"border-success",
"text-on-success"
// No dark: variants needed!
```

### Pattern 3: Surface with Strong Text
```tsx
// For text on surface backgrounds
"bg-surface",
"text-on-surface-strong",  // Use -strong for headings/emphasis
"dark:bg-surface-dark",
"dark:text-on-surface-dark-strong"
```

### Pattern 4: Inverse (Swap Light/Dark)
```tsx
// Dark appearance in light mode, light appearance in dark mode
"bg-surface-dark",        // Dark bg in light mode
"text-on-surface-dark",   // Light text in light mode
"dark:bg-surface",        // Light bg in dark mode
"dark:text-on-surface"    // Dark text in dark mode
```

## Complete Variant Reference

**All variants follow the patterns shown above.**

**Theme color variants:** primary, secondary, alternate, inverse → Use Pattern 1 (with dark mode)
**Shared color variants:** info, success, warning, danger → Use Pattern 2 (no dark mode)

For full examples, see Button component at `/skills/services/frontend/src/components/ui/button/button.tsx`

## Important Rules

### ✅ DO:
1. **Always include dark mode** for theme colors (primary, secondary, surface, outline)
2. **Never add dark mode** for shared colors (info, success, warning, danger)
3. **Use `rounded-radius`** as the default border radius
4. **Pair bg with border** - Same color for both (e.g., `bg-primary` + `border-primary`)
5. **Use on-* colors** for content on colored backgrounds
6. **Match focus outlines** to the variant color

### ❌ DON'T:
1. Don't use `rounded-md` or `rounded-lg` - use `rounded-radius` instead
2. Don't add `dark:bg-info-dark` - shared colors don't have dark variants
3. Don't use `text-primary` on `bg-primary` - use `text-on-primary` instead
4. Don't hardcode color values - always use tokens
5. Don't mix theme and shared color patterns

## Quick Decision Guide

**Choosing a variant:**
- Primary action / CTA → `primary`
- Secondary action / Cancel → `secondary`
- Alternate styling / Subtle → `alternate`
- Dark mode inverted → `inverse`
- Informational → `info`
- Success / Positive → `success`
- Warning / Caution → `warning`
- Error / Destructive → `danger`
- Transparent with border → `outline`

**Choosing text color:**
- Text on colored background → Use `text-on-{color}`
- Body text on surface → Use `text-on-surface`
- Headings on surface → Use `text-on-surface-strong`

**Choosing borders:**
- Default border → `border-outline` (+ `dark:border-outline-dark`)
- Emphasized border → `border-outline-strong` (+ `dark:border-outline-dark-strong`)
- Border matching variant → `border-{variant}` (e.g., `border-primary`)
