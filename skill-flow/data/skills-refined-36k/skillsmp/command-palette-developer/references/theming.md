# Command Palette Theming

Complete guide to implementing dark/light/system themes with CSS variables, Tailwind integration, and runtime switching.

## Theme System Architecture

### Three Theme Modes

1. **Light Mode** - Light backgrounds, dark text (default web standard)
2. **Dark Mode** - Dark backgrounds, light text (reduces eye strain)
3. **System Mode** - Follows OS preference via `prefers-color-scheme`

### Implementation Strategy

Use CSS variables for theme values + HTML data attribute for theme switching:

```html
<html data-theme="dark">
  <!-- Palette inherits theme -->
</html>
```

No re-renders required - CSS variables update instantly.

## CSS Variable Foundation

### Core Palette Variables

```css
:root {
  /* Backgrounds */
  --palette-bg: #ffffff;
  --palette-bg-secondary: #f9fafb;
  --palette-selection-bg: #eff6ff;
  --palette-hover-bg: #f3f4f6;

  /* Text */
  --palette-text: #111827;
  --palette-text-muted: #6b7280;
  --palette-text-placeholder: #9ca3af;

  /* Borders */
  --palette-border: #e5e7eb;
  --palette-separator: #f3f4f6;

  /* Accents */
  --palette-accent: #3b82f6;
  --palette-accent-hover: #2563eb;

  /* Shadows */
  --palette-shadow: rgba(0, 0, 0, 0.1);
  --palette-shadow-lg: rgba(0, 0, 0, 0.15);

  /* Shortcuts/Badges */
  --palette-shortcut-bg: #f3f4f6;
  --palette-shortcut-text: #374151;
  --palette-shortcut-border: #d1d5db;
}

[data-theme="dark"] {
  /* Backgrounds */
  --palette-bg: #1f2937;
  --palette-bg-secondary: #111827;
  --palette-selection-bg: #374151;
  --palette-hover-bg: #2d3748;

  /* Text */
  --palette-text: #f9fafb;
  --palette-text-muted: #9ca3af;
  --palette-text-placeholder: #6b7280;

  /* Borders */
  --palette-border: #374151;
  --palette-separator: #2d3748;

  /* Accents */
  --palette-accent: #60a5fa;
  --palette-accent-hover: #3b82f6;

  /* Shadows */
  --palette-shadow: rgba(0, 0, 0, 0.3);
  --palette-shadow-lg: rgba(0, 0, 0, 0.5);

  /* Shortcuts/Badges */
  --palette-shortcut-bg: #374151;
  --palette-shortcut-text: #d1d5db;
  --palette-shortcut-border: #4b5563;
}
```

### Usage in Components

```tsx
<div
  className="command-palette"
  style={{
    background: 'var(--palette-bg)',
    border: '1px solid var(--palette-border)',
    boxShadow: '0 20px 25px var(--palette-shadow-lg)',
  }}
>
  <input
    className="command-input"
    style={{
      background: 'var(--palette-bg)',
      color: 'var(--palette-text)',
    }}
    placeholder="Search..."
  />
</div>
```

## Tailwind Integration

### Tailwind Config Extension

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // Use class-based dark mode
  theme: {
    extend: {
      colors: {
        palette: {
          bg: 'var(--palette-bg)',
          'bg-secondary': 'var(--palette-bg-secondary)',
          selection: 'var(--palette-selection-bg)',
          hover: 'var(--palette-hover-bg)',
          text: 'var(--palette-text)',
          'text-muted': 'var(--palette-text-muted)',
          border: 'var(--palette-border)',
          accent: 'var(--palette-accent)',
        },
      },
    },
  },
};
```

### Using Tailwind Classes

```tsx
<div className="bg-palette-bg border border-palette-border">
  <input className="text-palette-text placeholder:text-palette-text-muted" />
  <div className="bg-palette-selection text-palette-text">Selected Item</div>
</div>
```

### Dark Mode Utilities

```tsx
<div className="bg-white dark:bg-gray-900">
  <span className="text-gray-900 dark:text-gray-100">Text</span>
</div>
```

## Theme Provider Implementation

### ThemeProvider Component

```typescript
// providers/ThemeProvider.tsx
import { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'light' | 'dark' | 'system';
type ResolvedTheme = 'light' | 'dark';

interface ThemeContextValue {
  theme: Theme;
  resolvedTheme: ResolvedTheme;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<Theme>(() => {
    // Load from localStorage or default to system
    return (localStorage.getItem('theme') as Theme) || 'system';
  });

  const [resolvedTheme, setResolvedTheme] = useState<ResolvedTheme>('light');

  // Resolve system theme
  useEffect(() => {
    const getSystemTheme = (): ResolvedTheme => {
      return window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
    };

    const updateResolvedTheme = () => {
      const resolved = theme === 'system' ? getSystemTheme() : theme;
      setResolvedTheme(resolved);
      document.documentElement.setAttribute('data-theme', resolved);

      // Also set class for Tailwind dark mode
      if (resolved === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    };

    updateResolvedTheme();

    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => {
      if (theme === 'system') {
        updateResolvedTheme();
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme]);

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme);
    localStorage.setItem('theme', newTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, resolvedTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}
```

### Theme Switcher UI

```tsx
function ThemeSwitcher() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="theme-switcher">
      <button
        onClick={() => setTheme('light')}
        className={theme === 'light' ? 'active' : ''}
      >
        <SunIcon /> Light
      </button>
      <button
        onClick={() => setTheme('dark')}
        className={theme === 'dark' ? 'active' : ''}
      >
        <MoonIcon /> Dark
      </button>
      <button
        onClick={() => setTheme('system')}
        className={theme === 'system' ? 'active' : ''}
      >
        <ComputerIcon /> System
      </button>
    </div>
  );
}
```

## Per-Palette Theme Overrides

### Custom Palette Themes

Allow individual palettes to have custom color schemes:

```tsx
interface PaletteTheme {
  bg?: string;
  text?: string;
  accent?: string;
  // ... other overrides
}

function CommandPalette({ customTheme }: { customTheme?: PaletteTheme }) {
  const style = customTheme ? {
    '--palette-bg': customTheme.bg,
    '--palette-text': customTheme.text,
    '--palette-accent': customTheme.accent,
  } : {};

  return (
    <div className="command-palette" style={style as React.CSSProperties}>
      {/* Palette content */}
    </div>
  );
}
```

### Brand-Specific Palettes

```tsx
const brandTheme: PaletteTheme = {
  bg: '#0a0e27',
  text: '#ffffff',
  accent: '#6366f1', // Brand purple
  selectionBg: '#1e293b',
};

<CommandPalette customTheme={brandTheme} />
```

## Color Contrast & Accessibility

### WCAG AA Compliance

Ensure sufficient contrast ratios:
- **Normal text (14-18px):** 4.5:1 minimum
- **Large text (≥18px or ≥14px bold):** 3:1 minimum
- **Interactive elements:** 3:1 minimum against background

### Testing Tools

```typescript
// Calculate contrast ratio
function getContrastRatio(color1: string, color2: string): number {
  const l1 = getLuminance(color1);
  const l2 = getLuminance(color2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

// Verify theme compliance
function validateThemeContrast(theme: Record<string, string>) {
  const bgContrast = getContrastRatio(theme['--palette-bg'], theme['--palette-text']);
  if (bgContrast < 4.5) {
    console.warn('Insufficient text contrast');
  }
}
```

### Safe Color Palettes

**Light theme:**
```css
--palette-bg: #ffffff;        /* White */
--palette-text: #111827;      /* Gray-900 */
/* Contrast ratio: 17.1:1 ✓ */
```

**Dark theme:**
```css
--palette-bg: #1f2937;        /* Gray-800 */
--palette-text: #f9fafb;      /* Gray-50 */
/* Contrast ratio: 13.4:1 ✓ */
```

## Reduced Motion Support

### Respecting User Preferences

```css
@media (prefers-reduced-motion: reduce) {
  .command-palette {
    animation: none !important;
    transition: none !important;
  }

  .command-item {
    transition: none !important;
  }

  .palette-enter,
  .palette-exit {
    animation: none !important;
  }
}
```

### JavaScript Detection

```typescript
function useReducedMotion(): boolean {
  const [prefersReduced, setPrefersReduced] = useState(
    () => window.matchMedia('(prefers-reduced-motion: reduce)').matches
  );

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    const handleChange = () => setPrefersReduced(mediaQuery.matches);
    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  return prefersReduced;
}

// Usage
function Palette() {
  const reducedMotion = useReducedMotion();

  return (
    <motion.div
      animate={{ opacity: 1 }}
      transition={{ duration: reducedMotion ? 0 : 0.2 }}
    >
      {/* Content */}
    </motion.div>
  );
}
```

## High Contrast Mode

### Windows High Contrast

```css
@media (prefers-contrast: high) {
  :root {
    --palette-bg: #000000;
    --palette-text: #ffffff;
    --palette-border: #ffffff;
    --palette-selection-bg: #1a73e8;
  }

  .command-palette {
    border-width: 2px; /* Thicker borders */
  }

  .command-item[aria-selected="true"] {
    outline: 2px solid var(--palette-accent);
  }
}
```

## Theme Transition Animations

### Smooth Theme Switching

```css
html {
  /* Only transition theme colors, not layout properties */
  transition:
    background-color 200ms ease-in-out,
    color 200ms ease-in-out;
}

@media (prefers-reduced-motion: reduce) {
  html {
    transition: none;
  }
}
```

### Preventing FOUC (Flash of Unstyled Content)

```html
<!-- In <head> before any stylesheets -->
<script>
  // Set theme immediately, before first paint
  (function() {
    const theme = localStorage.getItem('theme') || 'system';
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
    const resolvedTheme = theme === 'system' ? systemTheme : theme;
    document.documentElement.setAttribute('data-theme', resolvedTheme);
    if (resolvedTheme === 'dark') {
      document.documentElement.classList.add('dark');
    }
  })();
</script>
```

## Theme Utilities

### Generated Theme Utilities

```typescript
// utilities/theme-utils.ts

export function getSystemTheme(): 'light' | 'dark' {
  return window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light';
}

export function createThemeVariables(config: ThemeConfig): React.CSSProperties {
  return {
    '--palette-bg': config.bg,
    '--palette-text': config.text,
    '--palette-accent': config.accent,
    // ... map all theme values
  } as React.CSSProperties;
}

export function applyTheme(theme: 'light' | 'dark'): void {
  document.documentElement.setAttribute('data-theme', theme);
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}
```

## Custom Theme Builder

### Theme Configuration Interface

```typescript
interface ThemeConfig {
  name: string;
  light: ThemeColors;
  dark: ThemeColors;
}

interface ThemeColors {
  bg: string;
  bgSecondary: string;
  text: string;
  textMuted: string;
  border: string;
  accent: string;
  accentHover: string;
}

const customTheme: ThemeConfig = {
  name: 'Brand Theme',
  light: {
    bg: '#ffffff',
    bgSecondary: '#f8fafc',
    text: '#0f172a',
    textMuted: '#64748b',
    border: '#e2e8f0',
    accent: '#6366f1',
    accentHover: '#4f46e5',
  },
  dark: {
    bg: '#0f172a',
    bgSecondary: '#020617',
    text: '#f8fafc',
    textMuted: '#94a3b8',
    border: '#334155',
    accent: '#818cf8',
    accentHover: '#a5b4fc',
  },
};
```

## Additional Resources

- **Design Principles:** `references/design-principles.md`
- **Layouts:** `references/layouts.md`
- **State Management:** `references/state-management.md`
- **Utilities:** `utilities/theme-utils.ts`
