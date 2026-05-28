# Typography

Tenzir uses two font families: **Inter** for UI text and **JetBrains Mono** for
code.

## Inter (Corporate Font)

Inter is the corporate font used for everything except code or where a monospace
font is required.

### Type Scale

| Token              | Size            | Line Height     | Letter Spacing | Weights Available          |
| ------------------ | --------------- | --------------- | -------------- | -------------------------- |
| `text-xxs`         | 0.625rem (10px) | 0.875rem (14px) | —              | regular, medium, semi-bold |
| `text-xs`          | 0.75rem (12px)  | 1.125rem (18px) | —              | regular, medium, semi-bold |
| `text-sm`          | 0.875rem (14px) | 1.25rem (20px)  | —              | regular, medium, semi-bold |
| `text-base`        | 1rem (16px)     | 1.5rem (24px)   | —              | regular, medium, semi-bold |
| `text-lg`          | 1.125rem (18px) | 1.75rem (28px)  | —              | regular, medium, semi-bold |
| `text-xl`          | 1.25rem (20px)  | 1.75rem (28px)  | —              | regular, medium, semi-bold |
| `text-2xl`         | 1.5rem (24px)   | 2rem (32px)     | -0.5%          | regular, medium, semi-bold |
| `text-3xl`         | 1.875rem (30px) | 2.25rem (36px)  | -1%            | regular, medium, semi-bold |
| `text-4xl`         | 2.25rem (36px)  | 2.5rem (40px)   | -1.5%          | regular, medium, semi-bold |
| `text-5xl`         | 3rem (48px)     | 3.5rem (56px)   | -2%            | regular, medium, semi-bold |
| `text-capitalized` | 0.75rem (12px)  | 1rem (16px)     | 5%             | medium, semi-bold          |

### Font Weights

| Weight    | CSS Value | Usage                        |
| --------- | --------- | ---------------------------- |
| Regular   | 400       | Body text, general content   |
| Medium    | 500       | Emphasis, labels             |
| Semi Bold | 600       | Headings, important elements |

### Usage Guidelines

- Use `text-base` (16px) as the default body text size
- Apply negative letter-spacing to sizes `text-2xl` and above
- Use `text-capitalized` for labels and category tags (always uppercase)
- Prefer semi-bold for headings, medium for UI labels, regular for body

## JetBrains Mono (Monospace Font)

JetBrains Mono is used for code or where a monospace font is required.

### Type Scale

| Token       | Size            | Line Height     | Weights Available          |
| ----------- | --------------- | --------------- | -------------------------- |
| `text-xxs`  | 0.625rem (10px) | 0.875rem (14px) | regular, medium, semi-bold |
| `text-xs`   | 0.75rem (12px)  | 1.125rem (18px) | regular, medium, semi-bold |
| `text-sm`   | 0.875rem (14px) | 1.25rem (20px)  | regular, medium, semi-bold |
| `text-base` | 1rem (16px)     | 1.5rem (24px)   | regular, medium, semi-bold |
| `text-lg`   | 1.125rem (18px) | 1.75rem (28px)  | regular, medium, semi-bold |
| `text-xl`   | 1.25rem (20px)  | 1.75rem (28px)  | regular, medium, semi-bold |

### Italic Variants

| Token        | Size            | Line Height     | Letter Spacing | Style   |
| ------------ | --------------- | --------------- | -------------- | ------- |
| `text-xs-em` | 0.75rem (12px)  | 1.125rem (18px) | -0.04em        | italic  |
| `text-sm-em` | 0.875rem (14px) | 1.25rem (20px)  | -0.04em        | regular |

### Font Weights

| Weight    | CSS Value | Usage          |
| --------- | --------- | -------------- |
| Regular   | 400       | General code   |
| Medium    | 500       | Error messages |
| Semi Bold | 600       | Code headlines |

### Usage Guidelines

- Use `text-sm` (14px) as the default code font size
- Use medium weight for error messages to draw attention
- Use semi-bold for code section headlines
- Apply italic variants (`-em` suffix) for emphasis within code

## CSS Custom Properties

Use the `--tnz-` prefix for all custom properties. Include Variable font variants with static fallbacks:

```css
:root {
  /* Font families - use Variable fonts with static fallbacks */
  --tnz-font-sans: "Inter Variable", "Inter", system-ui, sans-serif;
  --tnz-font-mono: "JetBrains Mono Variable", "JetBrains Mono", monospace;

  /* Font sizes */
  --tnz-text-xxs: 0.625rem; /* 10px */
  --tnz-text-xs: 0.75rem; /* 12px */
  --tnz-text-sm: 0.875rem; /* 14px */
  --tnz-text-base: 1rem; /* 16px */
  --tnz-text-lg: 1.125rem; /* 18px */
  --tnz-text-xl: 1.25rem; /* 20px */
  --tnz-text-2xl: 1.5rem; /* 24px */
  --tnz-text-3xl: 1.875rem; /* 30px */
  --tnz-text-4xl: 2.25rem; /* 36px */
  --tnz-text-5xl: 3rem; /* 48px */

  /* Line heights */
  --tnz-leading-xxs: 0.875rem; /* 14px */
  --tnz-leading-xs: 1.125rem; /* 18px */
  --tnz-leading-sm: 1.25rem; /* 20px */
  --tnz-leading-base: 1.5rem; /* 24px */
  --tnz-leading-lg: 1.75rem; /* 28px */
  --tnz-leading-xl: 1.75rem; /* 28px */
  --tnz-leading-2xl: 2rem; /* 32px */
  --tnz-leading-3xl: 2.25rem; /* 36px */
  --tnz-leading-4xl: 2.5rem; /* 40px */
  --tnz-leading-5xl: 3.5rem; /* 56px */

  /* Font weights */
  --tnz-font-regular: 400;
  --tnz-font-medium: 500;
  --tnz-font-semibold: 600;
}
```

**Usage example:**

```css
.heading {
  font-family: var(--tnz-font-sans);
  font-size: var(--tnz-text-2xl);
  line-height: var(--tnz-leading-2xl);
  font-weight: var(--tnz-font-semibold);
  letter-spacing: -0.005em;
}

.code-block {
  font-family: var(--tnz-font-mono);
  font-size: var(--tnz-text-sm);
  line-height: var(--tnz-leading-sm);
}
```

## Tailwind Configuration

```js
// tailwind.config.js
module.exports = {
  theme: {
    fontFamily: {
      sans: ["Inter", "system-ui", "sans-serif"],
      mono: ["JetBrains Mono", "monospace"],
    },
    fontSize: {
      xxs: ["0.625rem", { lineHeight: "0.875rem" }],
      xs: ["0.75rem", { lineHeight: "1.125rem" }],
      sm: ["0.875rem", { lineHeight: "1.25rem" }],
      base: ["1rem", { lineHeight: "1.5rem" }],
      lg: ["1.125rem", { lineHeight: "1.75rem" }],
      xl: ["1.25rem", { lineHeight: "1.75rem" }],
      "2xl": ["1.5rem", { lineHeight: "2rem", letterSpacing: "-0.005em" }],
      "3xl": ["1.875rem", { lineHeight: "2.25rem", letterSpacing: "-0.01em" }],
      "4xl": ["2.25rem", { lineHeight: "2.5rem", letterSpacing: "-0.015em" }],
      "5xl": ["3rem", { lineHeight: "3.5rem", letterSpacing: "-0.02em" }],
    },
    fontWeight: {
      normal: "400",
      medium: "500",
      semibold: "600",
    },
  },
};
```
