# Dark Mode Implementation

Guide complet pour implémenter le dark mode dans votre design system.

## Approches d'implémentation

```
┌─────────────────────────────────────────────────────────────────────┐
│                     DARK MODE STRATEGIES                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. CSS Media Query (Auto)                                          │
│     └── @media (prefers-color-scheme: dark)                         │
│                                                                      │
│  2. Data Attribute (Manual Toggle)                                  │
│     └── [data-theme="dark"]                                         │
│                                                                      │
│  3. Class-based (Legacy)                                            │
│     └── .dark-mode                                                  │
│                                                                      │
│  4. Hybrid (Auto + Manual Override)                                 │
│     └── Combine media query with data attribute                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Approche Recommandée : Hybrid

### 1. Définir les tokens sémantiques

```css
/* ══════════════════════════════════════════════════════════════════
   LIGHT MODE (Default)
   ══════════════════════════════════════════════════════════════════ */

:root {
  /* Background */
  --color-background: #ffffff;
  --color-background-secondary: #fafafa;
  --color-background-tertiary: #f4f4f5;
  --color-background-elevated: #ffffff;

  /* Foreground (Text) */
  --color-foreground: #18181b;
  --color-foreground-secondary: #3f3f46;
  --color-foreground-muted: #71717a;
  --color-foreground-subtle: #a1a1aa;

  /* Borders */
  --color-border: #e4e4e7;
  --color-border-strong: #d4d4d8;
  --color-border-subtle: #f4f4f5;

  /* Interactive */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-primary-light: #dbeafe;

  /* Status colors (WCAG AA compliant by default) */
  --color-success: #16a34a;         /* 4.5:1 - WCAG AA compliant */
  --color-success-bg: #22c55e;      /* Use for backgrounds with dark text */
  --color-success-light: #dcfce7;
  --color-warning: #eab308;
  --color-warning-light: #fef9c3;
  --color-error: #dc2626;           /* 4.5:1 - WCAG AA compliant */
  --color-error-bg: #ef4444;        /* Use for backgrounds with dark text */
  --color-error-light: #fee2e2;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);

  /* Focus Ring */
  --ring-color: var(--color-primary);
  --ring-offset-color: var(--color-background);
}

/* ══════════════════════════════════════════════════════════════════
   DARK MODE
   ══════════════════════════════════════════════════════════════════ */

/* Auto: respects system preference */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-background: #0a0a0b;
    --color-background-secondary: #18181b;
    --color-background-tertiary: #27272a;
    --color-background-elevated: #27272a;

    --color-foreground: #fafafa;
    --color-foreground-secondary: #d4d4d8;
    --color-foreground-muted: #a1a1aa;
    --color-foreground-subtle: #71717a;

    --color-border: #3f3f46;
    --color-border-strong: #52525b;
    --color-border-subtle: #27272a;

    --color-primary: #3b82f6;
    --color-primary-hover: #60a5fa;
    --color-primary-light: #1e3a8a;

    --color-success-light: #14532d;
    --color-warning-light: #422006;
    --color-error-light: #450a0a;

    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.3);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.5);

    --ring-offset-color: var(--color-background);
  }
}

/* Manual: data attribute override */
[data-theme="dark"] {
  --color-background: #0a0a0b;
  --color-background-secondary: #18181b;
  --color-background-tertiary: #27272a;
  --color-background-elevated: #27272a;

  --color-foreground: #fafafa;
  --color-foreground-secondary: #d4d4d8;
  --color-foreground-muted: #a1a1aa;
  --color-foreground-subtle: #71717a;

  --color-border: #3f3f46;
  --color-border-strong: #52525b;
  --color-border-subtle: #27272a;

  --color-primary: #3b82f6;
  --color-primary-hover: #60a5fa;
  --color-primary-light: #1e3a8a;

  --color-success-light: #14532d;
  --color-warning-light: #422006;
  --color-error-light: #450a0a;

  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.3);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.5);

  --ring-offset-color: var(--color-background);
}
```

### 2. JavaScript Toggle

```tsx
// hooks/useTheme.ts
import { useEffect, useState } from 'react';

type Theme = 'light' | 'dark' | 'system';

export function useTheme() {
  const [theme, setTheme] = useState<Theme>(() => {
    // Check localStorage first
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('theme') as Theme;
      if (stored) return stored;
    }
    return 'system';
  });

  useEffect(() => {
    const root = document.documentElement;

    if (theme === 'system') {
      root.removeAttribute('data-theme');
      localStorage.removeItem('theme');
    } else {
      root.setAttribute('data-theme', theme);
      localStorage.setItem('theme', theme);
    }
  }, [theme]);

  return { theme, setTheme };
}

// Usage
function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <select
      value={theme}
      onChange={(e) => setTheme(e.target.value as Theme)}
      aria-label="Select theme"
    >
      <option value="system">System</option>
      <option value="light">Light</option>
      <option value="dark">Dark</option>
    </select>
  );
}
```

### 3. Éviter le Flash (FOUC)

```html
<!-- Dans <head>, avant tout CSS -->
<script>
  (function() {
    const theme = localStorage.getItem('theme');
    if (theme === 'dark' || theme === 'light') {
      document.documentElement.setAttribute('data-theme', theme);
    }
  })();
</script>
```

## Composants Dark Mode

### Card

```css
.card {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

/* Elevated card (modal, dropdown) */
.card--elevated {
  background-color: var(--color-background-elevated);
  box-shadow: var(--shadow-lg);
}
```

### Button Variants

```css
.btn--primary {
  background-color: var(--color-primary);
  color: white;
}

.btn--primary:hover {
  background-color: var(--color-primary-hover);
}

.btn--secondary {
  background-color: var(--color-background-tertiary);
  color: var(--color-foreground);
  border: 1px solid var(--color-border);
}

.btn--ghost {
  background-color: transparent;
  color: var(--color-foreground);
}

.btn--ghost:hover {
  background-color: var(--color-background-tertiary);
}
```

### Input

```css
.input {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  color: var(--color-foreground);
}

.input::placeholder {
  color: var(--color-foreground-subtle);
}

.input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}
```

### Alert

```css
.alert--success {
  background-color: var(--color-success-light);
  border: 1px solid var(--color-success);
  color: var(--color-foreground);
}

/* En dark mode, --color-success-light devient #14532d (vert très sombre) */
```

## Images et Media

### Image Adaptative

```css
/* Inverser les images pour le dark mode */
[data-theme="dark"] img.invertible {
  filter: invert(1) hue-rotate(180deg);
}

/* Ou utiliser picture avec srcset */
```

```html
<picture>
  <source srcset="/logo-dark.svg" media="(prefers-color-scheme: dark)" />
  <img src="/logo-light.svg" alt="Logo" />
</picture>
```

### Graphiques et Charts

```css
/* Adapter les couleurs des graphiques */
:root {
  --chart-grid: #e4e4e7;
  --chart-text: #71717a;
}

[data-theme="dark"] {
  --chart-grid: #3f3f46;
  --chart-text: #a1a1aa;
}
```

## React Context Provider

```tsx
// context/ThemeContext.tsx
import { createContext, useContext, useEffect, useState, ReactNode } from 'react';

type Theme = 'light' | 'dark' | 'system';
type ResolvedTheme = 'light' | 'dark';

interface ThemeContextValue {
  theme: Theme;
  resolvedTheme: ResolvedTheme;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('system');
  const [resolvedTheme, setResolvedTheme] = useState<ResolvedTheme>('light');

  useEffect(() => {
    // Get initial theme from localStorage
    const stored = localStorage.getItem('theme') as Theme | null;
    if (stored) setTheme(stored);
  }, []);

  useEffect(() => {
    const root = document.documentElement;

    const updateResolvedTheme = () => {
      if (theme === 'system') {
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setResolvedTheme(systemDark ? 'dark' : 'light');
        root.removeAttribute('data-theme');
      } else {
        setResolvedTheme(theme);
        root.setAttribute('data-theme', theme);
      }
    };

    updateResolvedTheme();

    // Listen for system preference changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', updateResolvedTheme);

    return () => mediaQuery.removeEventListener('change', updateResolvedTheme);
  }, [theme]);

  useEffect(() => {
    if (theme === 'system') {
      localStorage.removeItem('theme');
    } else {
      localStorage.setItem('theme', theme);
    }
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, resolvedTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
```

## Theme Toggle Component

```tsx
// components/ThemeToggle.tsx
import { useTheme } from '@/context/ThemeContext';
import { SunIcon, MoonIcon, ComputerIcon } from '@/icons';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  const options = [
    { value: 'light', icon: SunIcon, label: 'Light' },
    { value: 'dark', icon: MoonIcon, label: 'Dark' },
    { value: 'system', icon: ComputerIcon, label: 'System' },
  ] as const;

  return (
    <div role="radiogroup" aria-label="Theme selection" className="theme-toggle">
      {options.map(({ value, icon: Icon, label }) => (
        <button
          key={value}
          role="radio"
          aria-checked={theme === value}
          onClick={() => setTheme(value)}
          className={`theme-toggle__option ${theme === value ? 'active' : ''}`}
        >
          <Icon aria-hidden="true" />
          <span className="sr-only">{label}</span>
        </button>
      ))}
    </div>
  );
}
```

```css
.theme-toggle {
  display: inline-flex;
  gap: var(--space-1);
  padding: var(--space-1);
  background-color: var(--color-background-tertiary);
  border-radius: var(--radius-lg);
}

.theme-toggle__option {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  border-radius: var(--radius-md);
  color: var(--color-foreground-muted);
  cursor: pointer;
  transition: background-color 0.15s, color 0.15s;
}

.theme-toggle__option:hover {
  color: var(--color-foreground);
}

.theme-toggle__option.active {
  background-color: var(--color-background);
  color: var(--color-foreground);
  box-shadow: var(--shadow-sm);
}
```

## Tailwind Config (Dark Mode)

```js
// tailwind.config.js
module.exports = {
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        background: 'var(--color-background)',
        foreground: 'var(--color-foreground)',
        border: 'var(--color-border)',
        // ... autres tokens
      },
    },
  },
};
```

## Testing Dark Mode

```tsx
// __tests__/DarkMode.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeProvider, useTheme } from '@/context/ThemeContext';

function TestComponent() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  return (
    <div>
      <span data-testid="theme">{theme}</span>
      <span data-testid="resolved">{resolvedTheme}</span>
      <button onClick={() => setTheme('dark')}>Set Dark</button>
    </div>
  );
}

describe('Dark Mode', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('defaults to system theme', () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );
    expect(screen.getByTestId('theme')).toHaveTextContent('system');
  });

  it('switches to dark mode', async () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    await userEvent.click(screen.getByText('Set Dark'));

    expect(screen.getByTestId('theme')).toHaveTextContent('dark');
    expect(document.documentElement).toHaveAttribute('data-theme', 'dark');
  });

  it('persists theme to localStorage', async () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    await userEvent.click(screen.getByText('Set Dark'));

    expect(localStorage.getItem('theme')).toBe('dark');
  });
});
```

## Checklist Dark Mode

- [ ] Tokens sémantiques définis (background, foreground, border)
- [ ] Light mode comme défaut avec fallbacks
- [ ] Support media query `prefers-color-scheme`
- [ ] Support data-attribute pour toggle manuel
- [ ] Script anti-FOUC dans `<head>`
- [ ] Elevated backgrounds pour les overlays
- [ ] Shadows adaptés (plus prononcées en dark)
- [ ] Focus rings visibles dans les deux modes
- [ ] Images adaptatives si nécessaire
- [ ] Tests pour les deux modes
- [ ] Persistance localStorage
- [ ] Option "System" pour suivre l'OS
