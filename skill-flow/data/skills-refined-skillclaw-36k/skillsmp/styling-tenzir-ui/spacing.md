# Spacing

Consistent spacing scale for padding and margin throughout the design system.

## Spacing Scale

| Token | rem   | px   | Visual     |
| ----- | ----- | ---- | ---------- |
| `0`   | 0     | 0px  | -          |
| `0.5` | 0.125 | 2px  | ▎          |
| `1`   | 0.25  | 4px  | ▌          |
| `1.5` | 0.375 | 6px  | ▊          |
| `2`   | 0.5   | 8px  | █          |
| `3`   | 0.75  | 12px | █▌         |
| `4`   | 1     | 16px | ██         |
| `5`   | 1.25  | 20px | ██▌        |
| `6`   | 1.5   | 24px | ███        |
| `7`   | 1.75  | 28px | ███▌       |
| `8`   | 2     | 32px | ████       |
| `10`  | 2.5   | 40px | █████      |
| `16`  | 4     | 64px | ████████   |
| `20`  | 5     | 80px | ██████████ |

## Token Naming

### Margin Tokens

| Token   | Value        |
| ------- | ------------ |
| `m-0`   | margin: 0px  |
| `m-0.5` | margin: 2px  |
| `m-1`   | margin: 4px  |
| `m-1.5` | margin: 6px  |
| `m-2`   | margin: 8px  |
| `m-3`   | margin: 12px |
| `m-4`   | margin: 16px |
| `m-5`   | margin: 20px |
| `m-6`   | margin: 24px |
| `m-7`   | margin: 28px |
| `m-8`   | margin: 32px |
| `m-10`  | margin: 40px |
| `m-16`  | margin: 64px |
| `m-20`  | margin: 80px |

### Padding Tokens

| Token   | Value         |
| ------- | ------------- |
| `p-0`   | padding: 0px  |
| `p-0.5` | padding: 2px  |
| `p-1`   | padding: 4px  |
| `p-1.5` | padding: 6px  |
| `p-2`   | padding: 8px  |
| `p-3`   | padding: 12px |
| `p-4`   | padding: 16px |
| `p-5`   | padding: 20px |
| `p-6`   | padding: 24px |
| `p-7`   | padding: 28px |
| `p-8`   | padding: 32px |
| `p-10`  | padding: 40px |
| `p-16`  | padding: 64px |
| `p-20`  | padding: 80px |

## CSS Custom Properties

Use the `--tnz-` prefix for all custom properties:

```css
:root {
  /* Spacing scale */
  --tnz-space-0: 0;
  --tnz-space-0-5: 0.125rem; /* 2px */
  --tnz-space-1: 0.25rem; /* 4px */
  --tnz-space-1-5: 0.375rem; /* 6px */
  --tnz-space-2: 0.5rem; /* 8px */
  --tnz-space-3: 0.75rem; /* 12px */
  --tnz-space-4: 1rem; /* 16px */
  --tnz-space-5: 1.25rem; /* 20px */
  --tnz-space-6: 1.5rem; /* 24px */
  --tnz-space-7: 1.75rem; /* 28px */
  --tnz-space-8: 2rem; /* 32px */
  --tnz-space-10: 2.5rem; /* 40px */
  --tnz-space-16: 4rem; /* 64px */
  --tnz-space-20: 5rem; /* 80px */
}
```

**Usage example:**

```css
.container {
  padding: var(--tnz-space-4); /* 16px */
  gap: var(--tnz-space-2); /* 8px */
  margin-bottom: var(--tnz-space-6); /* 24px */
}
```

## Common Usage Patterns

### Component Padding

| Component   | Padding Token     | Value       |
| ----------- | ----------------- | ----------- |
| Button XS   | `p-1` / `p-2`     | 4px / 8px   |
| Button S    | `p-1` / `p-2`     | 4px / 8px   |
| Button M    | `p-2` / `p-3`     | 8px / 12px  |
| Button L    | `p-2` / `p-4`     | 8px / 16px  |
| Input Field | `p-2`             | 8px         |
| Toast       | `p-3` / `p-4`     | 12px / 16px |
| Tag         | `p-0.5` / `p-1.5` | 3px / 6px   |
| Badge       | `p-0.5` / `p-1`   | 1px / 4px   |

### Gap Spacing

| Context       | Gap Token | Value |
| ------------- | --------- | ----- |
| Button icon   | `gap-1`   | 4px   |
| Tab bar       | `gap-1`   | 4px   |
| Toast content | `gap-4`   | 16px  |
| Form fields   | `gap-4`   | 16px  |
| Section       | `gap-8`   | 32px  |

## Usage Guidelines

1. **Use rem for scalability**:
   - Spacing uses rem units (based on 16px root)
   - This allows spacing to scale with user font preferences

2. **Choose semantic values**:
   - `0-2` (0-8px): Tight spacing for inline elements, icons
   - `3-4` (12-16px): Standard component padding
   - `5-8` (20-32px): Section spacing, larger gaps
   - `10-20` (40-80px): Page-level spacing, major sections

3. **Maintain consistency**:
   - Use the same spacing token for related elements
   - Vertical rhythm: Use consistent vertical spacing (e.g., `p-4` between sections)

4. **Scale jumps**:
   - Note the jump from `8` (32px) to `10` (40px)
   - And from `10` (40px) to `16` (64px)
   - These larger values are for major layout spacing

5. **Directional variants**:
   - Use suffixes for directional spacing: `-x`, `-y`, `-t`, `-r`, `-b`, `-l`
   - Example: `px-4` for horizontal padding of 16px
