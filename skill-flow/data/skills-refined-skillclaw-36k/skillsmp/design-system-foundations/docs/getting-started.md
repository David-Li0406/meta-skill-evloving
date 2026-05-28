# Getting Started with Design System Foundations

Ce guide explique comment utiliser le skill Design System Foundations pour créer ou auditer un design system industriel.

## Prérequis

- Compréhension de base des design systems
- Accès à une maquette (Figma, Sketch, Adobe XD)
- Projet frontend initialisé (React, Vue, Angular, ou vanilla)

## Dépendances Requises

### Utilitaire `cn()` pour React/TypeScript

Les exemples de composants React utilisent une fonction utilitaire `cn()` pour fusionner les classes CSS conditionnellement. Installez les dépendances nécessaires :

```bash
npm install clsx tailwind-merge
```

Créez le fichier utilitaire :

```typescript
// src/utils/cn.ts (ou lib/utils.ts)
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Combine les classes CSS avec support Tailwind
 * Gère les conflits de classes et les conditions
 *
 * @example
 * cn('px-4 py-2', isLarge && 'px-6 py-3', className)
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

#### Usage dans les composants

```tsx
import { cn } from '@/utils/cn';

// Classes conditionnelles
<button className={cn(
  'btn btn--primary',
  isDisabled && 'btn--disabled',
  className
)}>

// Override de styles via props
<Card className={cn('card', 'custom-class')} />
```

#### Alternative sans Tailwind

Si vous n'utilisez pas Tailwind CSS, vous pouvez simplifier :

```typescript
// Version simple avec clsx uniquement
import { clsx, type ClassValue } from 'clsx';
export const cn = (...inputs: ClassValue[]) => clsx(inputs);

// Ou version vanilla (sans dépendances)
export function cn(...classes: (string | boolean | undefined)[]) {
  return classes.filter(Boolean).join(' ');
}
```

## Workflow Recommandé

### 1. Extraction des Foundations

Commencer par les primitives du design system :

```
1. Colors    → Extraire la palette depuis la maquette
2. Typography → Définir les familles et l'échelle
3. Spacing   → Établir le système 8pt
4. Shadows   → Créer les niveaux d'élévation
```

**Questions à poser au skill :**
- "Comment extraire les couleurs de ma maquette Figma ?"
- "Quelle échelle typographique utiliser ?"
- "Comment créer un système d'espacement 8pt ?"

### 2. Création des Atoms

Les éléments de base indivisibles :

```
1. Buttons   → Définir variants (primary, secondary, ghost)
2. Inputs    → Créer les champs de formulaire
3. Labels    → Tags, chips, badges
4. Icons     → Système d'icônes avec tailles
5. Badges    → Indicateurs de statut
```

**Questions à poser au skill :**
- "Quels variants de bouton créer ?"
- "Comment structurer mes inputs pour l'accessibilité ?"

### 3. Assemblage des Molecules

Combiner les atomes en composants fonctionnels :

```
1. Forms     → Groupes de champs avec validation
2. Cards     → Conteneurs structurés
3. Navigation → Navbar, sidebar, tabs
4. Modals    → Dialogs avec gestion du focus
5. Alerts    → Notifications et toasts
```

**Questions à poser au skill :**
- "Comment structurer un formulaire multi-step ?"
- "Comment gérer le focus dans une modal ?"

### 4. Construction des Templates

Assembler les molécules en structures de pages :

```
1. Hero Sections → Landing page blocks
2. Layouts      → Dashboard, auth, marketing
3. Pages        → Templates de pages types
```

**Questions à poser au skill :**
- "Comment créer un dashboard layout responsive ?"
- "Quel template pour une page de liste ?"

## Structure de Fichiers Recommandée

```
design-system/
├── tokens/
│   ├── colors.css
│   ├── typography.css
│   ├── spacing.css
│   └── shadows.css
├── components/
│   ├── atoms/
│   │   ├── Button/
│   │   ├── Input/
│   │   └── ...
│   ├── molecules/
│   │   ├── Card/
│   │   ├── Form/
│   │   └── ...
│   └── templates/
│       ├── DashboardLayout/
│       └── ...
└── docs/
    └── storybook/
```

## Tokens CSS Minimum

```css
:root {
  /* Colors */
  --color-primary: #2563eb;
  --color-secondary: #64748b;
  --color-success: #22c55e;
  --color-warning: #eab308;
  --color-error: #ef4444;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-size-base: 1rem;

  /* Spacing */
  --space-unit: 0.25rem;
  --space-4: 1rem;

  /* Shadows */
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);

  /* Radius */
  --radius-md: 0.5rem;
}
```

## Common Pitfalls

### ❌ Erreurs Fréquentes à Éviter

#### 1. Tokens trop spécifiques

```css
/* ❌ Mauvais - trop couplé */
--button-primary-background: #2563eb;
--card-header-text-color: #1e293b;

/* ✅ Bon - tokens sémantiques réutilisables */
--color-primary: #2563eb;
--color-foreground: #1e293b;
```

#### 2. Nommage incohérent

```css
/* ❌ Mauvais - mix de conventions */
--primaryColor: blue;
--secondary_color: gray;
--ACCENT-COLOR: red;

/* ✅ Bon - kebab-case cohérent */
--color-primary: blue;
--color-secondary: gray;
--color-accent: red;
```

#### 3. Hardcoded values dans les composants

```css
/* ❌ Mauvais - valeurs en dur */
.button {
  padding: 8px 16px;
  background: #2563eb;
  border-radius: 6px;
}

/* ✅ Bon - utiliser les tokens */
.button {
  padding: var(--space-2) var(--space-4);
  background: var(--color-primary);
  border-radius: var(--radius-md);
}
```

#### 4. Oublier les fallbacks

```css
/* ❌ Risqué - pas de fallback */
.element {
  color: var(--color-text);
}

/* ✅ Sécurisé - avec fallback */
.element {
  color: var(--color-text, #171717);
}
```

#### 5. Trop de variants de couleurs

```css
/* ❌ Mauvais - explosion combinatoire */
--color-blue-50, --color-blue-100, ..., --color-blue-900
--color-green-50, --color-green-100, ..., --color-green-900
/* = 90+ tokens de couleurs */

/* ✅ Bon - palette limitée + sémantique */
--color-primary, --color-primary-hover, --color-primary-light
--color-success, --color-success-bg, --color-success-light
/* = 15-20 tokens max */
```

#### 6. Ignorer l'accessibilité dès le départ

```css
/* ❌ Mauvais - contraste insuffisant */
.badge--success {
  background: #22c55e;
  color: white; /* 3.1:1 - FAIL */
}

/* ✅ Bon - WCAG AA dès le début */
.badge--success {
  background: #16a34a;
  color: white; /* 4.5:1 - PASS */
}
```

#### 7. Animation de propriétés coûteuses

```css
/* ❌ Mauvais - trigger layout */
.element { transition: width 0.3s, height 0.3s; }

/* ✅ Bon - GPU accelerated */
.element { transition: transform 0.3s, opacity 0.3s; }
```

---

## Migration Guide

### Migrer depuis un CSS Legacy

#### Étape 1 : Inventaire

```bash
# Lister toutes les couleurs utilisées
grep -roh '#[0-9a-fA-F]\{3,6\}' src/ | sort | uniq -c | sort -rn

# Lister les font-sizes
grep -roh 'font-size:.*px' src/ | sort | uniq -c
```

#### Étape 2 : Mapping vers tokens

```css
/* Ancien code */
.header { color: #1a1a1a; }
.text { color: #333333; }
.muted { color: #666666; }

/* Nouveau : créer le mapping */
:root {
  --color-foreground: #1a1a1a;
  --color-foreground-secondary: #333333;
  --color-foreground-muted: #666666;
}

/* Migration progressive */
.header { color: var(--color-foreground, #1a1a1a); }
```

#### Étape 3 : Script de migration

```js
// migrate-colors.js
const mappings = {
  '#1a1a1a': 'var(--color-foreground)',
  '#333333': 'var(--color-foreground-secondary)',
  '#2563eb': 'var(--color-primary)',
};

// Remplacer dans les fichiers CSS
Object.entries(mappings).forEach(([old, newToken]) => {
  // sed -i "s/${old}/${newToken}/g" src/**/*.css
});
```

### Migrer depuis Bootstrap

```css
/* Bootstrap → Design System */
.btn-primary     → .btn.btn--primary
.btn-lg          → .btn.btn--lg
.card            → .card
.form-control    → .input

/* Tokens Bootstrap → Custom */
$primary         → --color-primary
$spacer          → --space-4
$border-radius   → --radius-md
```

### Migrer depuis Tailwind

```jsx
/* Tailwind classes → Design System */
// Avant
<button className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded">

// Après
<Button variant="primary">

/* Ou migration progressive avec tokens */
<button className="bg-[var(--color-primary)] px-[var(--space-4)]">
```

### Coexistence temporaire

```css
/* Phase de migration : les deux systèmes coexistent */
:root {
  /* Legacy (à supprimer) */
  --old-primary: #3490dc;

  /* Nouveau */
  --color-primary: #2563eb;
}

/* Composant migré */
.btn-new {
  background: var(--color-primary);
}

/* Composant legacy (à migrer) */
.btn-old {
  background: var(--old-primary);
}
```

---

## Troubleshooting

### Les tokens CSS ne fonctionnent pas

**Symptôme** : Les variables CSS ne s'appliquent pas.

```css
/* Problème : tokens définis dans le mauvais scope */
.component {
  --color-primary: blue; /* Scope local uniquement */
}

/* Solution : définir dans :root */
:root {
  --color-primary: blue;
}
```

### Contraste insuffisant

**Symptôme** : WCAG audit échoue.

```bash
# Vérifier le contraste
# Tool: https://webaim.org/resources/contrastchecker/

# Si ratio < 4.5:1 pour texte normal
# - Foncer le background, ou
# - Utiliser du texte foncé sur fond clair
```

### Fonts ne chargent pas

**Symptôme** : Police system au lieu de la custom.

```css
/* Vérifier font-display et le path */
@font-face {
  font-family: 'Inter';
  font-display: swap; /* Important ! */
  src: url('/fonts/inter.woff2') format('woff2');
}

/* Vérifier dans DevTools > Network > Font */
```

### Z-index chaos

**Symptôme** : Éléments qui se chevauchent incorrectement.

```css
/* Problème : valeurs arbitraires */
.modal { z-index: 9999; }
.dropdown { z-index: 99999; }

/* Solution : échelle définie */
:root {
  --z-dropdown: 100;
  --z-modal: 200;
  --z-tooltip: 300;
  --z-notification: 400;
}
```

### Espacement incohérent

**Symptôme** : UI désalignée, gaps irréguliers.

```css
/* Problème : mix de valeurs */
margin: 12px; /* pas dans l'échelle 8pt */
padding: 7px;

/* Solution : utiliser l'échelle */
margin: var(--space-3); /* 12px */
padding: var(--space-2); /* 8px */
```

### Animations saccadées

**Symptôme** : Animations < 60fps.

```css
/* Problème : animation de propriétés coûteuses */
transition: all 0.3s; /* Inclut width, height, etc. */

/* Solution : être explicite */
transition:
  transform 0.3s ease-out,
  opacity 0.3s ease-out;
```

### Dark mode partiel

**Symptôme** : Certains éléments ne switchent pas.

```css
/* Problème : couleurs hardcodées */
.card {
  background: white; /* Ne change pas */
}

/* Solution : utiliser tokens sémantiques */
.card {
  background: var(--color-background);
}

[data-theme="dark"] {
  --color-background: #1a1a1a;
}
```

### Build trop lourd

**Symptôme** : Bundle CSS > 100kb.

```bash
# Analyser le CSS
npx css-stats style.css

# Solutions :
# 1. PurgeCSS pour supprimer le CSS non utilisé
# 2. Tree-shaking des composants
# 3. Subsetting des polices
```

---

## Prochaines Étapes

1. Configurer Storybook pour la documentation
2. Mettre en place les tests d'accessibilité
3. Créer un changelog par composant
4. Définir le versioning sémantique
5. Mettre en place les visual regression tests
6. Documenter les guidelines de contribution
