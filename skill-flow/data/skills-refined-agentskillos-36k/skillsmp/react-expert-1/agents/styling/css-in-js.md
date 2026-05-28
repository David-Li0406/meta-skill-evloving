---
name: css-in-js
description: CSS-in-JS with styled-components and Emotion
workflows:
  - id: css-in-js-setup
    template: wf-creation
    phase: Production
    name: Setup CSS-in-JS
    duration: 0.5-1 jour
---

# CSS-in-JS - styled-components & Emotion

## Rôle

Implémentation de CSS-in-JS dans React avec styled-components et Emotion.

## Tu NE fais PAS

- ❌ Implémenter la logique métier des composants → `../components/`
- ❌ Gérer la logique JavaScript complexe → `../hooks/`
- ❌ Définir les détails d'accessibilité (ARIA, rôles) → `frontend-developer`
- ❌ Définir les tokens du design system → `design-system-foundations`

## styled-components

### Installation

```bash
npm install styled-components
npm install -D @types/styled-components
```

### Composant Stylé de Base

```tsx
import styled from 'styled-components';

const Button = styled.button`
  background-color: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background-color: #2563eb;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

// Usage
function App() {
  return <Button onClick={handleClick}>Click me</Button>;
}
```

### Props Dynamiques

```tsx
interface ButtonProps {
  $variant?: 'primary' | 'secondary' | 'danger';
  $size?: 'sm' | 'md' | 'lg';
}

const Button = styled.button<ButtonProps>`
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;

  /* Variant */
  background-color: ${({ $variant }) => {
    switch ($variant) {
      case 'secondary':
        return '#e5e7eb';
      case 'danger':
        return '#ef4444';
      default:
        return '#3b82f6';
    }
  }};

  color: ${({ $variant }) =>
    $variant === 'secondary' ? '#1f2937' : 'white'};

  /* Size */
  padding: ${({ $size }) => {
    switch ($size) {
      case 'sm':
        return '0.25rem 0.5rem';
      case 'lg':
        return '0.75rem 1.5rem';
      default:
        return '0.5rem 1rem';
    }
  }};

  font-size: ${({ $size }) =>
    $size === 'sm' ? '0.875rem' : $size === 'lg' ? '1.125rem' : '1rem'};

  &:hover {
    filter: brightness(0.9);
  }
`;

// Usage - $ prefix pour éviter le forward au DOM
<Button $variant="primary" $size="lg">Submit</Button>
```

### Extending Styles

```tsx
const Button = styled.button`
  background-color: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
`;

const IconButton = styled(Button)`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
`;

// Étendre un composant React
const StyledLink = styled(Link)`
  color: #3b82f6;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
`;
```

### Theming

```tsx
import { ThemeProvider, createGlobalStyle } from 'styled-components';

// Theme type
interface Theme {
  colors: {
    primary: string;
    secondary: string;
    background: string;
    text: string;
  };
  spacing: {
    sm: string;
    md: string;
    lg: string;
  };
}

const lightTheme: Theme = {
  colors: {
    primary: '#3b82f6',
    secondary: '#6b7280',
    background: '#ffffff',
    text: '#1f2937',
  },
  spacing: {
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
  },
};

const darkTheme: Theme = {
  colors: {
    primary: '#60a5fa',
    secondary: '#9ca3af',
    background: '#1f2937',
    text: '#f9fafb',
  },
  spacing: lightTheme.spacing,
};

// Global styles
const GlobalStyle = createGlobalStyle`
  body {
    background-color: ${({ theme }) => theme.colors.background};
    color: ${({ theme }) => theme.colors.text};
    margin: 0;
    font-family: system-ui, sans-serif;
  }
`;

// Composant utilisant le thème
const Card = styled.div`
  background-color: ${({ theme }) => theme.colors.background};
  color: ${({ theme }) => theme.colors.text};
  padding: ${({ theme }) => theme.spacing.md};
  border: 1px solid ${({ theme }) => theme.colors.secondary};
  border-radius: 0.5rem;
`;

// App
function App() {
  const [isDark, setIsDark] = useState(false);

  return (
    <ThemeProvider theme={isDark ? darkTheme : lightTheme}>
      <GlobalStyle />
      <Card>Content</Card>
    </ThemeProvider>
  );
}
```

## Emotion

### Installation

```bash
npm install @emotion/react @emotion/styled
```

### css prop (recommandé)

```tsx
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react';

const buttonStyle = css`
  background-color: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;

  &:hover {
    background-color: #2563eb;
  }
`;

function Button({ children }: { children: React.ReactNode }) {
  return <button css={buttonStyle}>{children}</button>;
}

// Inline css prop
function Card() {
  return (
    <div
      css={css`
        padding: 1rem;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
      `}
    >
      Content
    </div>
  );
}
```

### styled (comme styled-components)

```tsx
import styled from '@emotion/styled';

const Button = styled.button`
  background-color: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
`;
```

### Object Styles

```tsx
import styled from '@emotion/styled';

const Button = styled.button({
  backgroundColor: '#3b82f6',
  color: 'white',
  padding: '0.5rem 1rem',
  border: 'none',
  borderRadius: '0.375rem',
  cursor: 'pointer',
  '&:hover': {
    backgroundColor: '#2563eb',
  },
});

// Avec props
interface ButtonProps {
  primary?: boolean;
}

const Button = styled.button<ButtonProps>(({ primary }) => ({
  backgroundColor: primary ? '#3b82f6' : '#e5e7eb',
  color: primary ? 'white' : '#1f2937',
  padding: '0.5rem 1rem',
}));
```

### Composition

```tsx
import { css } from '@emotion/react';

const baseButton = css`
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
`;

const primaryButton = css`
  ${baseButton}
  background-color: #3b82f6;
  color: white;
`;

const secondaryButton = css`
  ${baseButton}
  background-color: #e5e7eb;
  color: #1f2937;
`;

function Button({ variant, children }) {
  return (
    <button css={variant === 'primary' ? primaryButton : secondaryButton}>
      {children}
    </button>
  );
}
```

## Patterns Communs

### Composant avec Variants

```tsx
import styled, { css } from 'styled-components';

interface AlertProps {
  $variant: 'info' | 'success' | 'warning' | 'error';
}

const variantStyles = {
  info: css`
    background-color: #eff6ff;
    border-color: #bfdbfe;
    color: #1e40af;
  `,
  success: css`
    background-color: #f0fdf4;
    border-color: #bbf7d0;
    color: #166534;
  `,
  warning: css`
    background-color: #fffbeb;
    border-color: #fde68a;
    color: #92400e;
  `,
  error: css`
    background-color: #fef2f2;
    border-color: #fecaca;
    color: #991b1b;
  `,
};

const Alert = styled.div<AlertProps>`
  padding: 1rem;
  border: 1px solid;
  border-radius: 0.5rem;
  ${({ $variant }) => variantStyles[$variant]}
`;
```

### Responsive

```tsx
import styled from 'styled-components';

const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
};

const media = {
  sm: `@media (min-width: ${breakpoints.sm})`,
  md: `@media (min-width: ${breakpoints.md})`,
  lg: `@media (min-width: ${breakpoints.lg})`,
  xl: `@media (min-width: ${breakpoints.xl})`,
};

const Container = styled.div`
  padding: 1rem;

  ${media.md} {
    padding: 2rem;
  }

  ${media.lg} {
    padding: 3rem;
    max-width: 1200px;
    margin: 0 auto;
  }
`;
```

### Animation

```tsx
import styled, { keyframes } from 'styled-components';

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const AnimatedCard = styled.div`
  animation: ${fadeIn} 0.3s ease-out;
`;

// Avec Emotion
import { keyframes } from '@emotion/react';

const bounce = keyframes`
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
`;

const BouncingButton = styled.button`
  animation: ${bounce} 1s infinite;
`;
```

## SSR Configuration

### styled-components

```tsx
// next.config.js (Next.js)
module.exports = {
  compiler: {
    styledComponents: true,
  },
};
```

### Emotion

```tsx
// emotion.d.ts
import '@emotion/react';

declare module '@emotion/react' {
  export interface Theme {
    colors: {
      primary: string;
      // ...
    };
  }
}
```

## Bonnes Pratiques

1. **Transient props ($)** - Pour éviter le forward au DOM
2. **Theme pour les tokens** - Couleurs, espacements centralisés
3. **Composants atomiques** - Petits, réutilisables
4. **TypeScript** - Typer les props et le theme
5. **Éviter les styles inline** - Préférer les composants stylés

## Voir aussi

- `tailwind-react.md` - Alternative utility-first
- `../components/functional.md` - Composants React
- `design-system-foundations` skill - Design system

## Livrables

| Livrable | Description |
|----------|-------------|
| Styled components | Composants React avec styled-components ou Emotion |
| Theme setup | Configuration ThemeProvider avec types TypeScript |
| Utility classes | Helper functions pour variants et responsive |
