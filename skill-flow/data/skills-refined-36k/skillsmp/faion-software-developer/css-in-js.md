---
id: css-in-js
name: "CSS-in-JS"
domain: DEV
skill: faion-software-developer
category: "development"
---

# CSS-in-JS

## Overview

CSS-in-JS is a styling approach where CSS is written within JavaScript, enabling component-scoped styles, dynamic styling based on props, and co-location of styles with components. Popular libraries include styled-components, Emotion, and vanilla-extract.

## When to Use

- Component-based architectures (React, Vue)
- Dynamic styling based on props/state
- Theming requirements
- CSS scoping without class name conflicts
- Design system implementation

## Key Principles

- **Component co-location**: Styles live with components
- **Scoped styles**: No global namespace pollution
- **Dynamic styling**: JavaScript-powered CSS
- **Type safety**: TypeScript support for style props
- **Zero-runtime options**: Build-time extraction for performance

## Best Practices

### styled-components

```tsx
// components/Button.tsx
import styled, { css } from 'styled-components';

// Basic styled component
const StyledButton = styled.button`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;

  &:focus-visible {
    outline: 2px solid ${({ theme }) => theme.colors.focus};
    outline-offset: 2px;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

// Variants using props
interface ButtonProps {
  $variant?: 'primary' | 'secondary' | 'outline';
  $size?: 'sm' | 'md' | 'lg';
  $fullWidth?: boolean;
}

const Button = styled.button<ButtonProps>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;

  /* Size variants */
  ${({ $size = 'md' }) => {
    const sizes = {
      sm: css`
        padding: 0.375rem 0.75rem;
        font-size: 0.875rem;
      `,
      md: css`
        padding: 0.5rem 1rem;
        font-size: 1rem;
      `,
      lg: css`
        padding: 0.75rem 1.5rem;
        font-size: 1.125rem;
      `,
    };
    return sizes[$size];
  }}

  /* Variant styles */
  ${({ $variant = 'primary', theme }) => {
    const variants = {
      primary: css`
        background: ${theme.colors.primary};
        color: ${theme.colors.primaryForeground};
        border: none;

        &:hover:not(:disabled) {
          background: ${theme.colors.primaryHover};
        }
      `,
      secondary: css`
        background: ${theme.colors.secondary};
        color: ${theme.colors.secondaryForeground};
        border: none;

        &:hover:not(:disabled) {
          background: ${theme.colors.secondaryHover};
        }
      `,
      outline: css`
        background: transparent;
        color: ${theme.colors.foreground};
        border: 1px solid ${theme.colors.border};

        &:hover:not(:disabled) {
          background: ${theme.colors.muted};
        }
      `,
    };
    return variants[$variant];
  }}

  /* Full width */
  ${({ $fullWidth }) => $fullWidth && css`width: 100%;`}

  &:focus-visible {
    outline: 2px solid ${({ theme }) => theme.colors.focus};
    outline-offset: 2px;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

// Usage
<Button $variant="primary" $size="lg">
  Click me
</Button>
```

### Theming with styled-components

```tsx
// theme/theme.ts
export const lightTheme = {
  colors: {
    primary: '#3b82f6',
    primaryHover: '#2563eb',
    primaryForeground: '#ffffff',
    secondary: '#f3f4f6',
    secondaryHover: '#e5e7eb',
    secondaryForeground: '#1f2937',
    background: '#ffffff',
    foreground: '#111827',
    muted: '#f9fafb',
    border: '#e5e7eb',
    focus: '#3b82f6',
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
  },
  radii: {
    sm: '0.125rem',
    md: '0.375rem',
    lg: '0.5rem',
    full: '9999px',
  },
  shadows: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
  },
} as const;

export const darkTheme = {
  ...lightTheme,
  colors: {
    ...lightTheme.colors,
    primary: '#60a5fa',
    primaryHover: '#3b82f6',
    background: '#111827',
    foreground: '#f9fafb',
    muted: '#1f2937',
    border: '#374151',
  },
} as const;

export type Theme = typeof lightTheme;

// TypeScript augmentation
import 'styled-components';

declare module 'styled-components' {
  export interface DefaultTheme extends Theme {}
}

// Theme provider
import { ThemeProvider } from 'styled-components';
import { useState } from 'react';

function App() {
  const [isDark, setIsDark] = useState(false);

  return (
    <ThemeProvider theme={isDark ? darkTheme : lightTheme}>
      <GlobalStyles />
      <AppContent />
    </ThemeProvider>
  );
}

// Global styles
import { createGlobalStyle } from 'styled-components';

const GlobalStyles = createGlobalStyle`
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    font-family: system-ui, sans-serif;
    background: ${({ theme }) => theme.colors.background};
    color: ${({ theme }) => theme.colors.foreground};
  }
`;
```

### Emotion

```tsx
// components/Card.tsx
/** @jsxImportSource @emotion/react */
import { css, Theme, useTheme } from '@emotion/react';
import styled from '@emotion/styled';

// CSS prop approach
function Card({ children, elevated = false }) {
  return (
    <div
      css={(theme: Theme) => css`
        padding: ${theme.spacing.md};
        border-radius: ${theme.radii.lg};
        background: ${theme.colors.background};
        border: 1px solid ${theme.colors.border};

        ${elevated &&
        css`
          box-shadow: ${theme.shadows.md};
          border: none;
        `}
      `}
    >
      {children}
    </div>
  );
}

// Styled approach
const CardContainer = styled.div<{ $elevated?: boolean }>`
  padding: ${({ theme }) => theme.spacing.md};
  border-radius: ${({ theme }) => theme.radii.lg};
  background: ${({ theme }) => theme.colors.background};
  border: 1px solid ${({ theme }) => theme.colors.border};

  ${({ $elevated, theme }) =>
    $elevated &&
    css`
      box-shadow: ${theme.shadows.md};
      border: none;
    `}
`;

// Composition
const baseStyles = css`
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const interactiveStyles = css`
  cursor: pointer;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-2px);
  }
`;

const InteractiveCard = styled.div`
  ${baseStyles}
  ${interactiveStyles}
  padding: 1rem;
  border-radius: 0.5rem;
`;
```

### vanilla-extract (Zero-Runtime)

```typescript
// Button.css.ts
import { style, styleVariants, createVar } from '@vanilla-extract/css';
import { recipe, RecipeVariants } from '@vanilla-extract/recipes';

// Create CSS variables
const accentColor = createVar();

// Base styles
const base = style({
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontWeight: 500,
  borderRadius: '0.375rem',
  cursor: 'pointer',
  transition: 'all 0.2s ease',
  vars: {
    [accentColor]: '#3b82f6',
  },
  ':focus-visible': {
    outline: `2px solid ${accentColor}`,
    outlineOffset: '2px',
  },
  ':disabled': {
    opacity: 0.5,
    cursor: 'not-allowed',
  },
});

// Style variants
const colorVariants = styleVariants({
  primary: {
    background: '#3b82f6',
    color: '#ffffff',
    border: 'none',
    ':hover': {
      background: '#2563eb',
    },
  },
  secondary: {
    background: '#f3f4f6',
    color: '#1f2937',
    border: 'none',
    ':hover': {
      background: '#e5e7eb',
    },
  },
  outline: {
    background: 'transparent',
    color: '#111827',
    border: '1px solid #e5e7eb',
    ':hover': {
      background: '#f9fafb',
    },
  },
});

const sizeVariants = styleVariants({
  sm: {
    padding: '0.375rem 0.75rem',
    fontSize: '0.875rem',
  },
  md: {
    padding: '0.5rem 1rem',
    fontSize: '1rem',
  },
  lg: {
    padding: '0.75rem 1.5rem',
    fontSize: '1.125rem',
  },
});

// Recipe (combines variants)
export const button = recipe({
  base: {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 500,
    borderRadius: '0.375rem',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
  },
  variants: {
    color: {
      primary: {
        background: '#3b82f6',
        color: '#ffffff',
        ':hover': { background: '#2563eb' },
      },
      secondary: {
        background: '#f3f4f6',
        color: '#1f2937',
        ':hover': { background: '#e5e7eb' },
      },
    },
    size: {
      sm: { padding: '0.375rem 0.75rem', fontSize: '0.875rem' },
      md: { padding: '0.5rem 1rem', fontSize: '1rem' },
      lg: { padding: '0.75rem 1.5rem', fontSize: '1.125rem' },
    },
  },
  defaultVariants: {
    color: 'primary',
    size: 'md',
  },
});

export type ButtonVariants = RecipeVariants<typeof button>;

// Button.tsx
import { button, ButtonVariants } from './Button.css';

interface ButtonProps extends ButtonVariants {
  children: React.ReactNode;
}

export function Button({ color, size, children }: ButtonProps) {
  return (
    <button className={button({ color, size })}>
      {children}
    </button>
  );
}
```

### vanilla-extract with Sprinkles

```typescript
// sprinkles.css.ts
import { defineProperties, createSprinkles } from '@vanilla-extract/sprinkles';

const space = {
  none: 0,
  sm: '0.5rem',
  md: '1rem',
  lg: '1.5rem',
  xl: '2rem',
};

const colors = {
  primary: '#3b82f6',
  secondary: '#6b7280',
  white: '#ffffff',
  black: '#000000',
  transparent: 'transparent',
};

const responsiveProperties = defineProperties({
  conditions: {
    mobile: {},
    tablet: { '@media': 'screen and (min-width: 768px)' },
    desktop: { '@media': 'screen and (min-width: 1024px)' },
  },
  defaultCondition: 'mobile',
  properties: {
    display: ['none', 'flex', 'block', 'inline-flex', 'grid'],
    flexDirection: ['row', 'column'],
    alignItems: ['stretch', 'flex-start', 'center', 'flex-end'],
    justifyContent: ['flex-start', 'center', 'flex-end', 'space-between'],
    gap: space,
    padding: space,
    paddingTop: space,
    paddingBottom: space,
    paddingLeft: space,
    paddingRight: space,
    margin: space,
    marginTop: space,
    marginBottom: space,
  },
  shorthands: {
    p: ['padding'],
    px: ['paddingLeft', 'paddingRight'],
    py: ['paddingTop', 'paddingBottom'],
    m: ['margin'],
    mx: ['marginLeft', 'marginRight'],
    my: ['marginTop', 'marginBottom'],
  },
});

const colorProperties = defineProperties({
  conditions: {
    lightMode: {},
    darkMode: { '@media': '(prefers-color-scheme: dark)' },
  },
  defaultCondition: 'lightMode',
  properties: {
    color: colors,
    background: colors,
    borderColor: colors,
  },
});

export const sprinkles = createSprinkles(
  responsiveProperties,
  colorProperties
);

export type Sprinkles = Parameters<typeof sprinkles>[0];

// Usage
import { sprinkles } from './sprinkles.css';

function Card() {
  return (
    <div
      className={sprinkles({
        display: 'flex',
        flexDirection: { mobile: 'column', tablet: 'row' },
        gap: 'md',
        p: 'lg',
        background: { lightMode: 'white', darkMode: 'black' },
      })}
    >
      Content
    </div>
  );
}
```

### Performance Considerations

```tsx
// Avoid creating styles in render
// BAD
function BadComponent({ color }) {
  // Creates new styled component every render!
  const Box = styled.div`
    background: ${color};
  `;
  return <Box />;
}

// GOOD - Use props
const Box = styled.div<{ $color: string }>`
  background: ${({ $color }) => $color};
`;

function GoodComponent({ color }) {
  return <Box $color={color} />;
}

// GOOD - Use CSS variables for frequently changing values
const AnimatedBox = styled.div`
  transform: translateX(var(--x, 0));
  transition: transform 0.1s ease;
`;

function AnimatedComponent({ x }) {
  return <AnimatedBox style={{ '--x': `${x}px` }} />;
}

// GOOD - Memoize computed styles
const DynamicButton = styled.button`
  ${({ $styles }) => $styles}
`;

function OptimizedComponent({ variant }) {
  const styles = useMemo(
    () =>
      css`
        background: ${variant === 'primary' ? 'blue' : 'gray'};
      `,
    [variant]
  );

  return <DynamicButton $styles={styles}>Click</DynamicButton>;
}
```

### CSS Extraction (SSR/SSG)

```tsx
// _document.tsx (Next.js with styled-components)
import Document, { Html, Head, Main, NextScript } from 'next/document';
import { ServerStyleSheet } from 'styled-components';

export default class MyDocument extends Document {
  static async getInitialProps(ctx) {
    const sheet = new ServerStyleSheet();
    const originalRenderPage = ctx.renderPage;

    try {
      ctx.renderPage = () =>
        originalRenderPage({
          enhanceApp: (App) => (props) =>
            sheet.collectStyles(<App {...props} />),
        });

      const initialProps = await Document.getInitialProps(ctx);
      return {
        ...initialProps,
        styles: [initialProps.styles, sheet.getStyleElement()],
      };
    } finally {
      sheet.seal();
    }
  }

  render() {
    return (
      <Html>
        <Head />
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
```

## Anti-patterns

- **Creating styles in render**: Causes style regeneration
- **Over-nesting**: Deep nesting reduces readability
- **Mixing approaches**: Using multiple CSS-in-JS libraries
- **Ignoring bundle size**: Large runtime CSS-in-JS for static styles
- **No extraction**: Missing server-side style extraction
- **Inline everything**: Not extracting reusable styles

## References

- [styled-components](https://styled-components.com/)
- [Emotion](https://emotion.sh/)
- [vanilla-extract](https://vanilla-extract.style/)
- [Linaria](https://linaria.dev/) (Zero-runtime)
- [CSS-in-JS Benchmarks](https://css-tricks.com/a-thorough-analysis-of-css-in-js/)
