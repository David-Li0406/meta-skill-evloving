---
name: Tailwind Expert
description: Expert Tailwind CSS - configuration, plugins, patterns et bonnes pratiques
workflows:
  - id: tailwind-setup
    template: wf-creation
    phase: Production
    name: Setup Tailwind CSS
    duration: 0.5 jour
  - id: tailwind-migration
    template: wf-refonte
    phase: Migration
    name: Migration vers Tailwind
    duration: 3-7 jours
---

# Agent Tailwind Expert

## Responsabilité

Maîtriser Tailwind CSS pour créer des interfaces rapidement avec des classes utilitaires.

## Tu NE fais PAS

- ❌ Écrire du CSS vanille (Grid, Flexbox natif) → `foundations/css-moderne.md`
- ❌ Gérer les animations complexes (Framer Motion, GSAP) → `animations.md`
- ❌ Créer le design system complet (tokens, documentation) → skill `design-system-foundations`
- ❌ Gérer les composants React/Vue → `frameworks/`

## Configuration de Base

### tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class', // ou 'media'
  theme: {
    extend: {
      // Couleurs personnalisées
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
          950: '#082f49',
        },
        secondary: {
          // ...
        },
      },
      // Polices
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      // Espacements personnalisés
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      // Border radius
      borderRadius: {
        '4xl': '2rem',
      },
      // Animations
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
```

### CSS de base

```css
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    @apply scroll-smooth;
  }

  body {
    @apply bg-white text-gray-900 dark:bg-gray-900 dark:text-gray-100;
  }
}

@layer components {
  .btn {
    @apply inline-flex items-center justify-center px-4 py-2
           font-medium rounded-lg transition-colors
           focus:outline-none focus:ring-2 focus:ring-offset-2;
  }

  .btn-primary {
    @apply btn bg-primary-600 text-white
           hover:bg-primary-700
           focus:ring-primary-500;
  }

  .btn-secondary {
    @apply btn bg-gray-200 text-gray-900
           hover:bg-gray-300
           focus:ring-gray-500;
  }

  .input {
    @apply block w-full px-3 py-2
           border border-gray-300 rounded-lg
           focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
           dark:bg-gray-800 dark:border-gray-600;
  }

  .card {
    @apply bg-white rounded-xl shadow-lg p-6
           dark:bg-gray-800;
  }
}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}
```

## Classes Essentielles

### Layout

```html
<!-- Flexbox -->
<div class="flex items-center justify-between gap-4">
  <div class="flex-1">Flex grow</div>
  <div class="flex-shrink-0">Fixed</div>
</div>

<!-- Grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div>Item</div>
</div>

<!-- Grid auto-fill responsive -->
<div class="grid grid-cols-[repeat(auto-fill,minmax(250px,1fr))] gap-4">
  <div>Item</div>
</div>

<!-- Container -->
<div class="container mx-auto px-4">
  Contenu centré
</div>

<!-- Position -->
<div class="relative">
  <div class="absolute top-0 right-0">Badge</div>
</div>
```

### Espacement

```html
<!-- Margin -->
<div class="m-4 mt-8 mx-auto">Margins</div>

<!-- Padding -->
<div class="p-4 py-8 px-6">Padding</div>

<!-- Space between children -->
<div class="space-y-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<!-- Gap (flex/grid) -->
<div class="flex gap-4">Items with gap</div>
```

### Typographie

```html
<!-- Tailles -->
<p class="text-xs">Extra small</p>
<p class="text-sm">Small</p>
<p class="text-base">Base (16px)</p>
<p class="text-lg">Large</p>
<p class="text-xl">Extra large</p>
<p class="text-2xl md:text-3xl lg:text-4xl">Responsive</p>

<!-- Style -->
<p class="font-bold italic underline">Styled text</p>
<p class="text-gray-600 dark:text-gray-400">Muted</p>
<p class="leading-relaxed tracking-wide">Line height & letter spacing</p>

<!-- Troncature -->
<p class="truncate">Long text truncated...</p>
<p class="line-clamp-3">Clamp to 3 lines...</p>
```

### Couleurs et Backgrounds

```html
<!-- Text colors -->
<p class="text-primary-600 dark:text-primary-400">Primary</p>
<p class="text-gray-900 dark:text-white">Adaptatif</p>

<!-- Backgrounds -->
<div class="bg-white dark:bg-gray-900">Background</div>
<div class="bg-gradient-to-r from-blue-500 to-purple-500">Gradient</div>

<!-- Borders -->
<div class="border border-gray-200 rounded-lg">Bordered</div>
<div class="border-l-4 border-primary-500">Left border</div>
```

### États Interactifs

```html
<!-- Hover -->
<button class="bg-blue-500 hover:bg-blue-600">Hover</button>

<!-- Focus -->
<input class="focus:ring-2 focus:ring-blue-500 focus:outline-none" />

<!-- Active -->
<button class="active:scale-95">Click effect</button>

<!-- Disabled -->
<button class="disabled:opacity-50 disabled:cursor-not-allowed" disabled>
  Disabled
</button>

<!-- Group hover -->
<div class="group">
  <div class="group-hover:text-blue-500">Hover parent to change</div>
</div>

<!-- Peer (sibling) -->
<input class="peer" />
<p class="hidden peer-focus:block">Shows on input focus</p>
```

## Responsive Design

```html
<!-- Mobile first -->
<div class="
  w-full          /* mobile */
  sm:w-1/2        /* >= 640px */
  md:w-1/3        /* >= 768px */
  lg:w-1/4        /* >= 1024px */
  xl:w-1/5        /* >= 1280px */
  2xl:w-1/6       /* >= 1536px */
">
  Responsive width
</div>

<!-- Cacher/Afficher -->
<div class="hidden md:block">Desktop only</div>
<div class="block md:hidden">Mobile only</div>

<!-- Grid responsive -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
  Items
</div>
```

## Composants Réutilisables

### Avec clsx/cn

```tsx
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
}

function Button({
  variant = 'primary',
  size = 'md',
  className,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        // Base
        'inline-flex items-center justify-center font-medium rounded-lg transition-colors',
        'focus:outline-none focus:ring-2 focus:ring-offset-2',
        // Variants
        {
          'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500':
            variant === 'primary',
          'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500':
            variant === 'secondary',
          'border-2 border-primary-600 text-primary-600 hover:bg-primary-50':
            variant === 'outline',
        },
        // Sizes
        {
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        },
        className
      )}
      {...props}
    />
  );
}
```

### Patterns courants

```html
<!-- Card -->
<div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
  <img class="w-full h-48 object-cover" src="..." alt="..." />
  <div class="p-6">
    <h3 class="text-lg font-semibold">Titre</h3>
    <p class="mt-2 text-gray-600 dark:text-gray-400">Description</p>
  </div>
</div>

<!-- Avatar -->
<img
  class="w-10 h-10 rounded-full ring-2 ring-white"
  src="..."
  alt="Avatar"
/>

<!-- Badge -->
<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
  Active
</span>

<!-- Input group -->
<div class="relative">
  <input
    class="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2"
    placeholder="Search..."
  />
  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
    <SearchIcon class="h-5 w-5 text-gray-400" />
  </div>
</div>
```

## Dark Mode

```html
<!-- Toggle avec classe -->
<html class="dark">
  <body class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
    <div class="border-gray-200 dark:border-gray-700">
      Content adaptatif
    </div>
  </body>
</html>

<!-- Toggle en JS -->
<script>
  document.documentElement.classList.toggle('dark');
</script>
```

## Plugins Personnalisés

```javascript
// tailwind.config.js
const plugin = require('tailwindcss/plugin');

module.exports = {
  plugins: [
    plugin(function({ addUtilities, addComponents, theme }) {
      addUtilities({
        '.text-shadow': {
          textShadow: '0 2px 4px rgba(0,0,0,0.1)',
        },
        '.text-shadow-lg': {
          textShadow: '0 4px 8px rgba(0,0,0,0.2)',
        },
      });

      addComponents({
        '.btn-gradient': {
          background: `linear-gradient(to right, ${theme('colors.blue.500')}, ${theme('colors.purple.500')})`,
          color: '#fff',
          padding: `${theme('spacing.2')} ${theme('spacing.4')}`,
          borderRadius: theme('borderRadius.lg'),
        },
      });
    }),
  ],
};
```

## Mots-clés de routage

`Tailwind`, `Tailwind CSS`, `classes utilitaires`, `@apply`, `tailwind.config`, `dark mode`, `responsive`, `hover`, `focus`, `cn`, `clsx`, `twMerge`

## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration Tailwind | tailwind.config.js avec thème personnalisé et plugins |
| Composants Tailwind | Classes utilitaires et patterns @layer pour composants |
| Guide de styles | Documentation des conventions et helper functions (cn) |
