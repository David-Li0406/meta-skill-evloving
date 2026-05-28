# Naming Conventions

Ce guide définit les conventions de nommage pour un design system cohérent et maintenable.

## Tokens CSS

### Structure Générale

```
--{category}-{property}-{variant}-{state}
```

### Couleurs

```css
/* Primitives (raw values) */
--color-blue-500: #3b82f6;
--color-gray-100: #f4f4f5;

/* Semantics (by usage) */
--color-primary: var(--color-blue-600);
--color-primary-hover: var(--color-blue-700);
--color-success: var(--color-green-500);
--color-error: var(--color-red-500);

/* Component tokens */
--button-primary-bg: var(--color-primary);
--input-border-focus: var(--color-primary);
```

### Typographie

```css
/* Familles */
--font-sans: 'Inter', sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Tailles (scale) */
--font-size-xs: 0.75rem;
--font-size-sm: 0.875rem;
--font-size-base: 1rem;
--font-size-lg: 1.125rem;

/* Poids */
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-bold: 700;

/* Line heights */
--line-height-tight: 1.25;
--line-height-normal: 1.5;
```

### Espacement

```css
/* Échelle numérique */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-4: 1rem;      /* 16px */
--space-8: 2rem;      /* 32px */

/* Sémantique */
--space-inset-sm: var(--space-2);
--space-stack-md: var(--space-4);
```

### Ombres

```css
/* Échelle */
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);

/* Sémantique */
--elevation-1: var(--shadow-sm);
--elevation-2: var(--shadow-md);
```

## CSS Nesting

### Browser Compatibility

Ce design system utilise la syntaxe **CSS Nesting** native pour les exemples de code. Cette fonctionnalité est supportée par les navigateurs modernes depuis 2023.

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 120+ | ✅ Full |
| Firefox | 117+ | ✅ Full |
| Safari | 17.2+ | ✅ Full |
| Edge | 120+ | ✅ Full |

**Note**: Pour les navigateurs plus anciens, utilisez un préprocesseur CSS (Sass, PostCSS) ou transpilateur.

### Syntaxe

```css
/* CSS Nesting natif */
.button {
  background: var(--color-primary);

  &:hover {
    background: var(--color-primary-hover);
  }

  &:focus {
    box-shadow: var(--focus-ring);
  }

  &--large {
    padding: var(--space-4);
  }
}
```

### Alternative PostCSS

Si vous devez supporter des navigateurs plus anciens, configurez PostCSS :

```js
// postcss.config.js
module.exports = {
  plugins: [
    require('postcss-nesting'),
    require('autoprefixer'),
  ],
};
```

## Classes CSS

### BEM (Block Element Modifier)

```css
/* Block */
.card { }

/* Element (double underscore) */
.card__header { }
.card__body { }
.card__footer { }

/* Modifier (double dash) */
.card--elevated { }
.card--outlined { }
.card--clickable { }

/* Combinaison */
.card__header--sticky { }
```

### Exemples Complets

```css
/* Button */
.btn { }
.btn__icon { }
.btn__label { }
.btn--primary { }
.btn--secondary { }
.btn--sm { }
.btn--lg { }
.btn--loading { }

/* Form Field */
.form-field { }
.form-field__label { }
.form-field__input { }
.form-field__error { }
.form-field--required { }
.form-field--disabled { }
```

## Composants React/Vue

### Nommage des Fichiers

```
components/
├── Button/
│   ├── Button.tsx        # Composant principal
│   ├── Button.styles.css # Styles
│   ├── Button.test.tsx   # Tests
│   └── index.ts          # Export
├── Card/
│   ├── Card.tsx
│   ├── CardHeader.tsx    # Sous-composant
│   ├── CardBody.tsx
│   └── index.ts
```

### Nommage des Props

```tsx
interface ButtonProps {
  // Apparence
  variant: 'primary' | 'secondary' | 'ghost';
  size: 'sm' | 'md' | 'lg';

  // Contenu
  children: React.ReactNode;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;

  // États
  disabled?: boolean;
  loading?: boolean;
  active?: boolean;

  // Événements (on + PascalCase)
  onClick?: () => void;
  onFocus?: () => void;

  // Accessibilité (camelCase)
  ariaLabel?: string;
  ariaDescribedBy?: string;
}
```

### Compound Components

```tsx
// Export nommé
export { Card, CardHeader, CardBody, CardFooter };

// Ou attaché au composant parent
Card.Header = CardHeader;
Card.Body = CardBody;
Card.Footer = CardFooter;

// Usage
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>
```

## Storybook Stories

```tsx
// ComponentName.stories.tsx
export default {
  title: 'Category/ComponentName',  // Ex: Atoms/Button
  component: Button,
};

// Story nommée en PascalCase
export const Primary: Story = { args: { variant: 'primary' } };
export const Secondary: Story = { args: { variant: 'secondary' } };
export const AllVariants: Story = { render: () => <VariantsGrid /> };
```

## Git Commits

### Format Conventional Commits

```
type(scope): message

feat(button): add loading state
fix(input): correct focus ring color
style(tokens): update primary palette
docs(readme): add installation guide
refactor(card): extract CardHeader component
test(button): add accessibility tests
```

### Types

| Type | Usage |
|------|-------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `style` | Changement visuel (tokens, CSS) |
| `docs` | Documentation |
| `refactor` | Refactoring sans changement fonctionnel |
| `test` | Ajout/modification de tests |
| `chore` | Maintenance, dépendances |

## Résumé

| Élément | Convention | Exemple |
|---------|------------|---------|
| Token CSS | kebab-case | `--color-primary-500` |
| Classe CSS | BEM + kebab | `.card__header--sticky` |
| Composant | PascalCase | `Button`, `CardHeader` |
| Fichier composant | PascalCase | `Button.tsx` |
| Props | camelCase | `leftIcon`, `onClick` |
| Story | PascalCase | `Primary`, `AllVariants` |
| Commit | lowercase | `feat(button): add...` |
