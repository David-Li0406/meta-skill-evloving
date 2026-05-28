---
name: CSS-in-JS Expert
description: Expert CSS-in-JS - styled-components, Emotion, CSS Modules
workflows:
  - id: cssinjs-setup
    template: wf-creation
    phase: Production
    name: Setup CSS-in-JS
    duration: 0.5 jour
  - id: cssinjs-migration
    template: wf-refonte
    phase: Migration
    name: Migration vers CSS-in-JS
    duration: 2-5 jours
---

# Agent CSS-in-JS

## Responsabilité

Maîtriser les solutions CSS-in-JS pour créer des styles scopés et dynamiques.

## Tu NE fais PAS

- ❌ Gérer Tailwind CSS (classes utilitaires, configuration) → `tailwind-expert.md`
- ❌ Écrire du SCSS/Sass (mixins, variables $) → SCSS expertise si nécessaire
- ❌ Créer des animations complexes (Framer Motion) → `animations.md`
- ❌ Créer le design system complet → skill `design-system-foundations`

## Styled-Components

### Installation et setup

```bash
npm install styled-components
npm install -D @types/styled-components  # TypeScript
```

### Composants de base

```tsx
import styled from 'styled-components';

// Composant simple
const Button = styled.button`
  background-color: #0070f3;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background-color: #0051a2;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

// Avec props
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
}

const StyledButton = styled.button<ButtonProps>`
  padding: ${({ size }) => {
    switch (size) {
      case 'sm': return '0.5rem 1rem';
      case 'lg': return '1rem 2rem';
      default: return '0.75rem 1.5rem';
    }
  }};

  background-color: ${({ variant }) =>
    variant === 'secondary' ? '#e5e7eb' : '#0070f3'};

  color: ${({ variant }) =>
    variant === 'secondary' ? '#374151' : 'white'};
`;
```

### Thèmes

```tsx
import { ThemeProvider, createGlobalStyle } from 'styled-components';

// Définition du thème
const theme = {
  colors: {
    primary: '#0070f3',
    secondary: '#6b7280',
    background: '#ffffff',
    text: '#111827',
    error: '#ef4444',
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '2rem',
    xl: '4rem',
  },
  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '16px',
    full: '9999px',
  },
  shadows: {
    sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px rgba(0, 0, 0, 0.1)',
  },
} as const;

type Theme = typeof theme;

// Typage du thème
declare module 'styled-components' {
  export interface DefaultTheme extends Theme {}
}

// Styles globaux
const GlobalStyle = createGlobalStyle`
  *, *::before, *::after {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    font-family: system-ui, sans-serif;
    background-color: ${({ theme }) => theme.colors.background};
    color: ${({ theme }) => theme.colors.text};
  }
`;

// Usage dans l'app
function App() {
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <Content />
    </ThemeProvider>
  );
}

// Accès au thème dans les composants
const Card = styled.div`
  background: ${({ theme }) => theme.colors.background};
  padding: ${({ theme }) => theme.spacing.lg};
  border-radius: ${({ theme }) => theme.borderRadius.md};
  box-shadow: ${({ theme }) => theme.shadows.md};
`;
```

### Patterns avancés

```tsx
// Extension de composant
const PrimaryButton = styled(Button)`
  background-color: #0070f3;
`;

// Cibler un autre composant
const Icon = styled.span`
  margin-right: 0.5rem;
`;

const ButtonWithIcon = styled.button`
  ${Icon} {
    transition: transform 0.2s;
  }

  &:hover ${Icon} {
    transform: translateX(4px);
  }
`;

// Attributs par défaut
const SubmitButton = styled.button.attrs({
  type: 'submit',
})`
  /* styles */
`;

// Polymorphisme avec "as"
const Heading = styled.h1`
  font-size: 2rem;
  font-weight: bold;
`;

// Rendu en h2
<Heading as="h2">Sous-titre</Heading>

// CSS helper
import { css } from 'styled-components';

const flexCenter = css`
  display: flex;
  justify-content: center;
  align-items: center;
`;

const CenteredBox = styled.div`
  ${flexCenter}
  height: 100vh;
`;
```

## Emotion

### Installation

```bash
npm install @emotion/react @emotion/styled
```

### Syntaxe styled (similaire à styled-components)

```tsx
import styled from '@emotion/styled';

const Button = styled.button`
  background: #0070f3;
  color: white;
  padding: 0.75rem 1.5rem;
`;
```

### Syntaxe css prop

```tsx
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react';

function Component() {
  return (
    <div
      css={css`
        padding: 1rem;
        background: white;
        border-radius: 8px;
      `}
    >
      Content
    </div>
  );
}

// Avec objet (meilleure performance)
function ComponentObject() {
  return (
    <div
      css={{
        padding: '1rem',
        background: 'white',
        borderRadius: '8px',
      }}
    >
      Content
    </div>
  );
}
```

### Composition de styles

```tsx
import { css, SerializedStyles } from '@emotion/react';

const baseButton = css`
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s;
`;

const primaryStyle = css`
  ${baseButton}
  background: #0070f3;
  color: white;

  &:hover {
    background: #0051a2;
  }
`;

const secondaryStyle = css`
  ${baseButton}
  background: #e5e7eb;
  color: #374151;
`;

function Button({ variant = 'primary' }: { variant?: 'primary' | 'secondary' }) {
  return (
    <button css={variant === 'primary' ? primaryStyle : secondaryStyle}>
      Click me
    </button>
  );
}
```

## CSS Modules

### Configuration

```css
/* Button.module.css */
.button {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
}

.primary {
  composes: button;
  background-color: #0070f3;
  color: white;
}

.secondary {
  composes: button;
  background-color: #e5e7eb;
  color: #374151;
}

.large {
  padding: 1rem 2rem;
  font-size: 1.125rem;
}

/* Variables CSS locales */
.card {
  --card-padding: 1.5rem;
  padding: var(--card-padding);
}
```

### Usage React

```tsx
import styles from './Button.module.css';
import clsx from 'clsx';

interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'md' | 'lg';
  children: React.ReactNode;
}

function Button({ variant = 'primary', size = 'md', children }: ButtonProps) {
  return (
    <button
      className={clsx(
        styles[variant],
        size === 'lg' && styles.large
      )}
    >
      {children}
    </button>
  );
}
```

### TypeScript avec CSS Modules

```typescript
// types/css-modules.d.ts
declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}

declare module '*.module.scss' {
  const classes: { [key: string]: string };
  export default classes;
}
```

### CSS Modules avec SCSS

```scss
// Card.module.scss
@use 'sass:color';

$primary-color: #0070f3;

.card {
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

  &:hover {
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
  }
}

.header {
  border-bottom: 1px solid color.adjust($primary-color, $lightness: 40%);
}
```

## Comparaison des Solutions

| Feature | styled-components | Emotion | CSS Modules |
|---------|------------------|---------|-------------|
| Runtime | Oui | Oui | Non |
| Bundle size | ~12kb | ~11kb | 0kb |
| SSR | Besoin de config | Besoin de config | Natif |
| Theming | Intégré | Intégré | Variables CSS |
| TypeScript | Bon | Excellent | Via typings |
| Performance | Bonne | Meilleure | Excellente |
| Dynamic styles | Oui | Oui | Limité |

## Bonnes Pratiques

### Performance

```tsx
// ❌ Éviter les styles inline dynamiques
const Component = ({ color }) => (
  <div style={{ backgroundColor: color }} />
);

// ✅ Utiliser des classes/variants
const StyledDiv = styled.div<{ $color: string }>`
  background-color: ${({ $color }) => $color};
`;

// ❌ Éviter de créer des styled dans le render
function Component() {
  const Button = styled.button`...`; // Recréé à chaque render!
  return <Button />;
}

// ✅ Définir les styled à l'extérieur
const Button = styled.button`...`;
function Component() {
  return <Button />;
}
```

### Organisation

```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.styles.ts  # styled-components
│   ├── Button.module.css # CSS Modules
│   └── index.ts
```

```tsx
// Button.styles.ts
import styled from 'styled-components';

export const StyledButton = styled.button`
  /* ... */
`;

export const IconWrapper = styled.span`
  /* ... */
`;
```

## Mots-clés de routage

`CSS-in-JS`, `styled-components`, `Emotion`, `CSS Modules`, `css prop`, `ThemeProvider`, `createGlobalStyle`, `composes`, `scoped CSS`

## Livrables

| Livrable | Description |
|----------|-------------|
| Système de thème | ThemeProvider avec tokens et variants configurés |
| Composants stylés | Bibliothèque de styled-components ou Emotion |
| Configuration CSS Modules | Setup et conventions de nommage pour CSS Modules |
