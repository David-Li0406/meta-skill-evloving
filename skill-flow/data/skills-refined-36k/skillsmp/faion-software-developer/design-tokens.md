---
id: design-tokens
name: "Design Tokens"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Design Tokens

## Overview

Design tokens are the atomic values of a design system, storing visual design decisions as data. They ensure consistency across platforms (web, iOS, Android) and enable theming while maintaining a single source of truth.

## When to Use

- Building design systems
- Multi-platform applications
- Theming support (dark mode, white-label)
- Design-to-development handoff
- Maintaining brand consistency

## Key Principles

- **Single source of truth**: One definition, multiple outputs
- **Platform agnostic**: Tokens work across web, mobile, desktop
- **Semantic naming**: Names describe purpose, not value
- **Hierarchical structure**: Primitive to semantic to component
- **Version controlled**: Tokens in code, not just design tools

## Best Practices

### Token Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    TOKEN HIERARCHY                          │
├─────────────────────────────────────────────────────────────┤
│ PRIMITIVE TOKENS (Core)                                     │
│   Raw values: colors, sizes, fonts                          │
│   Example: blue-500: #3B82F6                                │
├─────────────────────────────────────────────────────────────┤
│ SEMANTIC TOKENS (Alias)                                     │
│   Purpose-based references to primitives                    │
│   Example: color-primary: {blue-500}                        │
├─────────────────────────────────────────────────────────────┤
│ COMPONENT TOKENS (Specific)                                 │
│   Component-specific tokens                                 │
│   Example: button-bg-primary: {color-primary}               │
└─────────────────────────────────────────────────────────────┘
```

### Token Definition (JSON)

```json
// tokens/primitive.json
{
  "color": {
    "gray": {
      "50": { "value": "#f9fafb" },
      "100": { "value": "#f3f4f6" },
      "200": { "value": "#e5e7eb" },
      "300": { "value": "#d1d5db" },
      "400": { "value": "#9ca3af" },
      "500": { "value": "#6b7280" },
      "600": { "value": "#4b5563" },
      "700": { "value": "#374151" },
      "800": { "value": "#1f2937" },
      "900": { "value": "#111827" },
      "950": { "value": "#030712" }
    },
    "blue": {
      "50": { "value": "#eff6ff" },
      "100": { "value": "#dbeafe" },
      "200": { "value": "#bfdbfe" },
      "300": { "value": "#93c5fd" },
      "400": { "value": "#60a5fa" },
      "500": { "value": "#3b82f6" },
      "600": { "value": "#2563eb" },
      "700": { "value": "#1d4ed8" },
      "800": { "value": "#1e40af" },
      "900": { "value": "#1e3a8a" }
    },
    "red": {
      "500": { "value": "#ef4444" },
      "600": { "value": "#dc2626" },
      "700": { "value": "#b91c1c" }
    },
    "green": {
      "500": { "value": "#22c55e" },
      "600": { "value": "#16a34a" },
      "700": { "value": "#15803d" }
    }
  },
  "spacing": {
    "0": { "value": "0" },
    "1": { "value": "0.25rem" },
    "2": { "value": "0.5rem" },
    "3": { "value": "0.75rem" },
    "4": { "value": "1rem" },
    "5": { "value": "1.25rem" },
    "6": { "value": "1.5rem" },
    "8": { "value": "2rem" },
    "10": { "value": "2.5rem" },
    "12": { "value": "3rem" },
    "16": { "value": "4rem" },
    "20": { "value": "5rem" }
  },
  "fontSize": {
    "xs": { "value": "0.75rem" },
    "sm": { "value": "0.875rem" },
    "base": { "value": "1rem" },
    "lg": { "value": "1.125rem" },
    "xl": { "value": "1.25rem" },
    "2xl": { "value": "1.5rem" },
    "3xl": { "value": "1.875rem" },
    "4xl": { "value": "2.25rem" }
  },
  "fontWeight": {
    "normal": { "value": "400" },
    "medium": { "value": "500" },
    "semibold": { "value": "600" },
    "bold": { "value": "700" }
  },
  "borderRadius": {
    "none": { "value": "0" },
    "sm": { "value": "0.125rem" },
    "md": { "value": "0.375rem" },
    "lg": { "value": "0.5rem" },
    "xl": { "value": "0.75rem" },
    "2xl": { "value": "1rem" },
    "full": { "value": "9999px" }
  },
  "shadow": {
    "sm": { "value": "0 1px 2px 0 rgb(0 0 0 / 0.05)" },
    "md": { "value": "0 4px 6px -1px rgb(0 0 0 / 0.1)" },
    "lg": { "value": "0 10px 15px -3px rgb(0 0 0 / 0.1)" },
    "xl": { "value": "0 20px 25px -5px rgb(0 0 0 / 0.1)" }
  }
}
```

```json
// tokens/semantic.json
{
  "color": {
    "bg": {
      "primary": { "value": "{color.white}" },
      "secondary": { "value": "{color.gray.50}" },
      "tertiary": { "value": "{color.gray.100}" },
      "inverse": { "value": "{color.gray.900}" }
    },
    "text": {
      "primary": { "value": "{color.gray.900}" },
      "secondary": { "value": "{color.gray.600}" },
      "tertiary": { "value": "{color.gray.500}" },
      "inverse": { "value": "{color.white}" },
      "disabled": { "value": "{color.gray.400}" }
    },
    "border": {
      "default": { "value": "{color.gray.200}" },
      "hover": { "value": "{color.gray.300}" },
      "focus": { "value": "{color.blue.500}" }
    },
    "action": {
      "primary": { "value": "{color.blue.600}" },
      "primaryHover": { "value": "{color.blue.700}" },
      "secondary": { "value": "{color.gray.100}" },
      "secondaryHover": { "value": "{color.gray.200}" }
    },
    "status": {
      "success": { "value": "{color.green.600}" },
      "error": { "value": "{color.red.600}" },
      "warning": { "value": "{color.yellow.500}" },
      "info": { "value": "{color.blue.500}" }
    },
    "focus": {
      "ring": { "value": "{color.blue.500}" }
    }
  }
}
```

```json
// tokens/semantic-dark.json
{
  "color": {
    "bg": {
      "primary": { "value": "{color.gray.900}" },
      "secondary": { "value": "{color.gray.800}" },
      "tertiary": { "value": "{color.gray.700}" },
      "inverse": { "value": "{color.white}" }
    },
    "text": {
      "primary": { "value": "{color.gray.50}" },
      "secondary": { "value": "{color.gray.300}" },
      "tertiary": { "value": "{color.gray.400}" },
      "inverse": { "value": "{color.gray.900}" },
      "disabled": { "value": "{color.gray.600}" }
    },
    "border": {
      "default": { "value": "{color.gray.700}" },
      "hover": { "value": "{color.gray.600}" },
      "focus": { "value": "{color.blue.400}" }
    },
    "action": {
      "primary": { "value": "{color.blue.500}" },
      "primaryHover": { "value": "{color.blue.400}" }
    }
  }
}
```

### Style Dictionary Configuration

```javascript
// style-dictionary.config.js
const StyleDictionary = require('style-dictionary');

// Custom format for CSS custom properties
StyleDictionary.registerFormat({
  name: 'css/variables',
  formatter: function({ dictionary, file }) {
    return `:root {\n${dictionary.allProperties.map(prop =>
      `  --${prop.name}: ${prop.value};`
    ).join('\n')}\n}`;
  }
});

// Custom transform for CSS property names
StyleDictionary.registerTransform({
  name: 'name/kebab',
  type: 'name',
  transformer: (token) => {
    return token.path.join('-').toLowerCase();
  }
});

module.exports = {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'dist/css/',
      files: [
        {
          destination: 'variables.css',
          format: 'css/variables',
          options: {
            showFileHeader: false
          }
        }
      ]
    },
    scss: {
      transformGroup: 'scss',
      buildPath: 'dist/scss/',
      files: [
        {
          destination: '_variables.scss',
          format: 'scss/variables'
        }
      ]
    },
    js: {
      transformGroup: 'js',
      buildPath: 'dist/js/',
      files: [
        {
          destination: 'tokens.js',
          format: 'javascript/es6'
        }
      ]
    },
    ts: {
      transformGroup: 'js',
      buildPath: 'dist/ts/',
      files: [
        {
          destination: 'tokens.ts',
          format: 'javascript/es6'
        },
        {
          destination: 'tokens.d.ts',
          format: 'typescript/es6-declarations'
        }
      ]
    },
    json: {
      transformGroup: 'js',
      buildPath: 'dist/json/',
      files: [
        {
          destination: 'tokens.json',
          format: 'json/nested'
        }
      ]
    }
  }
};
```

### Generated CSS Output

```css
/* dist/css/variables.css */
:root {
  /* Primitives */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-500: #6b7280;
  --color-gray-900: #111827;
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-blue-700: #1d4ed8;

  /* Semantic */
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f9fafb;
  --color-text-primary: #111827;
  --color-text-secondary: #6b7280;
  --color-border-default: #e5e7eb;
  --color-action-primary: #2563eb;
  --color-action-primary-hover: #1d4ed8;

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;
  --spacing-8: 2rem;

  /* Typography */
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-weight-medium: 500;
  --font-weight-bold: 700;

  /* Border Radius */
  --radius-sm: 0.125rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

/* Dark mode */
[data-theme="dark"] {
  --color-bg-primary: #111827;
  --color-bg-secondary: #1f2937;
  --color-text-primary: #f9fafb;
  --color-text-secondary: #d1d5db;
  --color-border-default: #374151;
  --color-action-primary: #3b82f6;
}
```

### Using Tokens in Components

```tsx
// Using CSS custom properties
import styles from './Button.module.css';

export function Button({ children, variant = 'primary' }) {
  return (
    <button className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  );
}
```

```css
/* Button.module.css */
.button {
  padding: var(--spacing-2) var(--spacing-4);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  border-radius: var(--radius-md);
  transition: all 0.2s;
}

.primary {
  background: var(--color-action-primary);
  color: var(--color-text-inverse);
  border: none;
}

.primary:hover {
  background: var(--color-action-primary-hover);
}

.secondary {
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-default);
}

.secondary:hover {
  background: var(--color-bg-tertiary);
}
```

### TypeScript Token Types

```typescript
// tokens.ts (generated)
export const tokens = {
  color: {
    gray: {
      50: '#f9fafb',
      100: '#f3f4f6',
      // ...
    },
    blue: {
      500: '#3b82f6',
      600: '#2563eb',
      // ...
    },
  },
  spacing: {
    1: '0.25rem',
    2: '0.5rem',
    4: '1rem',
    // ...
  },
  // ...
} as const;

// Type helpers
type TokenPath<T, K extends keyof T = keyof T> = K extends string
  ? T[K] extends Record<string, unknown>
    ? `${K}.${TokenPath<T[K]>}` | K
    : K
  : never;

type ColorToken = TokenPath<typeof tokens.color>;
// 'gray' | 'gray.50' | 'gray.100' | 'blue' | 'blue.500' | ...

// Token getter with type safety
export function getToken<T extends TokenPath<typeof tokens>>(
  path: T
): string {
  return path.split('.').reduce((obj, key) => obj[key], tokens as any);
}

// Usage
const primaryColor = getToken('color.blue.600'); // '#2563eb'
```

### Tailwind Integration

```javascript
// tailwind.config.js
const tokens = require('./dist/js/tokens');

function flattenTokens(obj, prefix = '') {
  return Object.entries(obj).reduce((acc, [key, value]) => {
    const newKey = prefix ? `${prefix}-${key}` : key;
    if (typeof value === 'object' && !value.value) {
      return { ...acc, ...flattenTokens(value, newKey) };
    }
    return { ...acc, [newKey]: value.value || value };
  }, {});
}

module.exports = {
  theme: {
    colors: flattenTokens(tokens.color),
    spacing: flattenTokens(tokens.spacing),
    fontSize: flattenTokens(tokens.fontSize),
    fontWeight: flattenTokens(tokens.fontWeight),
    borderRadius: flattenTokens(tokens.borderRadius),
    boxShadow: flattenTokens(tokens.shadow),
  },
};
```

### Figma Token Sync

```javascript
// scripts/sync-figma-tokens.js
const fetch = require('node-fetch');
const fs = require('fs');

const FIGMA_TOKEN = process.env.FIGMA_TOKEN;
const FILE_KEY = process.env.FIGMA_FILE_KEY;

async function fetchFigmaTokens() {
  const response = await fetch(
    `https://api.figma.com/v1/files/${FILE_KEY}/variables/local`,
    {
      headers: {
        'X-Figma-Token': FIGMA_TOKEN,
      },
    }
  );

  const data = await response.json();
  return transformFigmaTokens(data);
}

function transformFigmaTokens(figmaData) {
  // Transform Figma variable format to Style Dictionary format
  const tokens = {};

  for (const variable of figmaData.meta.variables) {
    const path = variable.name.split('/');
    let current = tokens;

    for (let i = 0; i < path.length - 1; i++) {
      current[path[i]] = current[path[i]] || {};
      current = current[path[i]];
    }

    current[path[path.length - 1]] = {
      value: resolveValue(variable.valuesByMode),
    };
  }

  return tokens;
}

async function main() {
  const tokens = await fetchFigmaTokens();
  fs.writeFileSync(
    'tokens/figma-sync.json',
    JSON.stringify(tokens, null, 2)
  );
  console.log('Tokens synced from Figma!');
}

main();
```

## Anti-patterns

- **Hardcoded values**: Using raw colors/sizes instead of tokens
- **Too many tokens**: Creating tokens for every variation
- **Poor naming**: Using values in names (blue-500 as semantic)
- **No hierarchy**: Flat token structure without levels
- **Platform-specific**: Tokens that only work on one platform
- **Missing documentation**: Tokens without usage guidance

## References

- [Style Dictionary](https://amzn.github.io/style-dictionary/)
- [Design Tokens W3C](https://design-tokens.github.io/community-group/format/)
- [Tokens Studio](https://tokens.studio/)
- [Design Tokens Format Module](https://tr.designtokens.org/format/)
