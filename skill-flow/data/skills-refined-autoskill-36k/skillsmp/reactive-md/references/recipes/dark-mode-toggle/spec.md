---
title: Dark Mode Toggle
author: @design-team
status: approved
date: 2025-12-14
---

# Dark Mode Toggle

## Problem Statement

Users working in low-light environments experience eye strain with our current light-only interface. Many modern apps support dark mode, and users expect it.

**User Research Findings**:
- 82% of surveyed users want dark mode
- 65% use dark mode on other apps after 6 PM
- Accessibility: dark mode helps users with light sensitivity

## Proposed Solution

A toggle in the header that switches between light and dark themes using CSS custom properties for consistent theming across the entire interface.

---

## Load Theme Styles

```css live
@import "./styles.css";
```

The theme system uses CSS custom properties defined in `styles.css`. The `.dark-theme` class overrides these variables to switch colors.

### Live Style Tweaking

No Storybook needed! Just add a `css live` block to create instant "knobs" for your spec. Try changing the value below and watch the demos update:

```css live
.dark-theme { --color-bg: teal; }
```
---

## The Toggle Component

An animated toggle with sun/moon icons:

```jsx live
import ThemeToggle from './ThemeToggle.jsx';

function ToggleDemo() {
  const [dark, setDark] = React.useState(false);
  
  return (
    <div 
      className={`theme-bg theme-transition p-8 rounded-lg ${dark ? 'dark-theme' : ''}`}
    >
      <div className="flex items-center justify-between max-w-xs mx-auto">
        <span className="font-medium">
          {dark ? 'Dark Mode' : 'Light Mode'}
        </span>
        <ThemeToggle dark={dark} onToggle={() => setDark(!dark)} />
      </div>
    </div>
  );
}
```

---

## Full Page Preview

See how the toggle affects an entire interface using CSS variables:

```jsx live
import ThemeToggle from './ThemeToggle.jsx';
import { Home, Settings, User, Bell, Search, Menu } from 'lucide-react';

function PagePreview() {
  const [dark, setDark] = React.useState(false);
  
  return (
    <div className={`theme-bg theme-transition rounded-lg overflow-hidden ${dark ? 'dark-theme' : ''}`}>
      {/* Header */}
      <div className="flex justify-between items-center p-4 border-b theme-card theme-transition" style={{ borderColor: 'var(--color-border)' }}>
        <div className="flex items-center gap-4">
          <Menu className="w-5 h-5" />
          <h1 className="text-xl font-bold">Dashboard</h1>
        </div>
        <div className="flex items-center gap-3">
          <div 
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg theme-transition"
            style={{ backgroundColor: 'var(--color-bg-secondary)' }}
          >
            <Search className="w-4 h-4" />
            <input 
              type="text" 
              placeholder="Search..." 
              className="bg-transparent border-none outline-none w-32"
              style={{ color: 'var(--color-text)' }}
            />
          </div>
          <button 
            className="p-2 rounded-lg theme-transition"
            style={{ backgroundColor: 'var(--color-bg-secondary)' }}
          >
            <Bell className="w-5 h-5" />
          </button>
          <ThemeToggle dark={dark} onToggle={() => setDark(!dark)} />
        </div>
      </div>
      
      {/* Content */}
      <div className="p-6 grid grid-cols-3 gap-4">
        {[
          { icon: Home, title: 'Overview', value: '1,234' },
          { icon: User, title: 'Users', value: '567' },
          { icon: Settings, title: 'Settings', value: '89' },
        ].map(({ icon: Icon, title, value }) => (
          <div 
            key={title} 
            className="p-4 rounded-lg theme-card theme-transition border"
            style={{ 
              backgroundColor: 'var(--color-card)',
              borderColor: 'var(--color-border)'
            }}
          >
            <div className="flex items-center gap-2 mb-2 theme-text-muted">
              <Icon className="w-4 h-4" />
              <span>{title}</span>
            </div>
            <div className="text-2xl font-bold">{value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## System Preference Detection

Respect the user's OS-level preference with a three-way toggle:

```jsx live
import { Monitor, Sun, Moon } from 'lucide-react';

function SystemPreference() {
  const [mode, setMode] = React.useState('system'); // 'light', 'dark', 'system'
  
  // In real implementation, would use window.matchMedia('(prefers-color-scheme: dark)')
  const systemPrefersDark = true; // Simulated for demo
  const effectiveDark = mode === 'system' ? systemPrefersDark : mode === 'dark';
  
  return (
    <div className={`theme-bg theme-transition p-6 rounded-lg ${effectiveDark ? 'dark-theme' : ''}`}>
      <h3 className="font-semibold mb-4">Theme Preference</h3>
      
      <div className="flex gap-2">
        {[
          { value: 'light', icon: Sun, label: 'Light' },
          { value: 'dark', icon: Moon, label: 'Dark' },
          { value: 'system', icon: Monitor, label: 'System' },
        ].map(({ value, icon: Icon, label }) => (
          <button
            key={value}
            onClick={() => setMode(value)}
            className="flex items-center gap-2 px-4 py-2 rounded-lg theme-transition"
            style={{
              backgroundColor: mode === value ? 'var(--color-accent)' : 'var(--color-bg-secondary)',
              color: mode === value ? 'white' : 'var(--color-text)'
            }}
          >
            <Icon className="w-4 h-4" />
            {label}
          </button>
        ))}
      </div>
      
      <p className="mt-4 text-sm theme-text-muted">
        {mode === 'system' 
          ? `Following system preference (currently ${systemPrefersDark ? 'dark' : 'light'})`
          : `Using ${mode} mode`
        }
      </p>
    </div>
  );
}
```

---

## Implementation Notes

### Persistence Strategy

```javascript
// Save preference
localStorage.setItem('theme', 'dark');

// Load preference with system fallback
const saved = localStorage.getItem('theme');
const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const isDark = saved ? saved === 'dark' : systemDark;

// Apply theme
document.documentElement.classList.toggle('dark-theme', isDark);
```

### CSS Variables Approach

The theme uses CSS custom properties for flexibility:

- **`:root`** - Defines light theme colors
- **`.dark-theme`** - Overrides with dark colors
- **`theme-*` classes** - Apply variables to components
- **Transitions** - Smooth 0.3s color changes

This approach allows:
1. Easy theme customization (just change variable values)
2. Consistent colors across all components
3. No JavaScript required for styling

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Dark mode adoption | > 40% of users |
| User satisfaction (survey) | > 4.5/5 |
| Time spent in app after 6 PM | +15% |

---
*Created with [Reactive MD](https://marketplace.visualstudio.com/items?itemName=million-views.reactive-md)*
