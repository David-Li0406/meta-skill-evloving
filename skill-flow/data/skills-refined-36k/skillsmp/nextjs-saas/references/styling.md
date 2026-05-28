# Styling Architecture

## Stack Overview

```
Tailwind CSS v4     - Utility-first styling
CSS Modules         - Component-scoped styles (REQUIRED for non-trivial components)
CSS Variables       - Dynamic theming
Shadcn/ui           - Pre-built components
```

## Critical Rule: No Inline Styles

**Never use inline `style={{ }}` props.** Always create a companion `.module.css` file for each component that needs custom styling.

```typescript
// BAD - Never do this
<div style={{ backgroundColor: 'var(--brand-primary)' }}>

// BAD - Never do this
<div style={{ width: collapsed ? '60px' : '280px' }}>

// GOOD - Use CSS Modules
<div className={styles.brandBackground}>

// GOOD - Use data attributes for state
<div className={styles.sidebar} data-collapsed={collapsed}>
```

## File Structure Convention

Every component with custom styles should have a companion CSS Module:

```
components/
├── dashboard/
│   ├── sidebar.tsx
│   ├── sidebar.module.css      # Always pair with .tsx
│   ├── header.tsx
│   ├── header.module.css
│   └── nav-links.tsx
│       nav-links.module.css
├── shared/
│   ├── tenant-switcher.tsx
│   ├── tenant-switcher.module.css
│   ├── brand-button.tsx
│   └── brand-button.module.css
```

## Tailwind CSS v4 Setup

### Installation

```bash
pnpm add tailwindcss @tailwindcss/postcss
```

### PostCSS Config

```javascript
// postcss.config.mjs
export default {
  plugins: {
    '@tailwindcss/postcss': {}
  }
}
```

### Global CSS with Variables

```css
/* app/globals.css */
@import "tailwindcss";

/* Theme variables */
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
  --secondary: 210 40% 96.1%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  --border: 214.3 31.8% 91.4%;
  --radius: 0.5rem;

  /* Sidebar */
  --sidebar-width: 280px;
  --sidebar-width-collapsed: 60px;
  --sidebar-background: 0 0% 98%;
  --sidebar-foreground: 240 5.3% 26.1%;

  /* Brand (dynamic, set via JS) */
  --brand-primary: #3b82f6;
  --brand-secondary: #64748b;
  --brand-font: 'Inter', sans-serif;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --primary: 210 40% 98%;
  --primary-foreground: 222.2 47.4% 11.2%;
  --sidebar-background: 240 5.9% 10%;
  --sidebar-foreground: 240 4.8% 95.9%;
}

* {
  border-color: hsl(var(--border));
}

body {
  background-color: hsl(var(--background));
  color: hsl(var(--foreground));
}
```

### Utility Function

```typescript
// lib/utils.ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## CSS Modules Pattern

### Basic Component with Module

```typescript
// components/shared/brand-button.tsx
import { cn } from '@/lib/utils'
import styles from './brand-button.module.css'

interface BrandButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary'
  className?: string
}

export function BrandButton({
  children,
  variant = 'primary',
  className
}: BrandButtonProps) {
  return (
    <button
      className={cn(styles.button, className)}
      data-variant={variant}
    >
      {children}
    </button>
  )
}
```

```css
/* components/shared/brand-button.module.css */
.button {
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  font-weight: 500;
  transition: background-color 0.2s, transform 0.1s;
}

.button[data-variant="primary"] {
  background-color: var(--brand-primary);
  color: white;
}

.button[data-variant="secondary"] {
  background-color: var(--brand-secondary);
  color: white;
}

.button:hover {
  filter: brightness(1.1);
}

.button:active {
  transform: scale(0.98);
}
```

### Stateful Component with Module

```typescript
// components/dashboard/sidebar.tsx
'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { navItems } from '@/config/navigation'
import styles from './sidebar.module.css'

export function Sidebar() {
  const pathname = usePathname()
  const [collapsed, setCollapsed] = useState(false)

  useEffect(() => {
    const stored = localStorage.getItem('sidebar-collapsed')
    if (stored === 'true') setCollapsed(true)
  }, [])

  useEffect(() => {
    localStorage.setItem('sidebar-collapsed', String(collapsed))
  }, [collapsed])

  return (
    <aside className={styles.sidebar} data-collapsed={collapsed}>
      <div className={styles.header}>
        <span className={styles.logo}>My App</span>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setCollapsed(!collapsed)}
          className={styles.toggleButton}
        >
          {collapsed ? <ChevronRight /> : <ChevronLeft />}
        </Button>
      </div>

      <nav className={styles.nav}>
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={styles.navItem}
            data-active={pathname === item.href}
          >
            <item.icon className={styles.navIcon} />
            <span className={styles.navLabel}>{item.title}</span>
          </Link>
        ))}
      </nav>
    </aside>
  )
}
```

```css
/* components/dashboard/sidebar.module.css */
.sidebar {
  display: flex;
  flex-direction: column;
  width: var(--sidebar-width);
  background-color: hsl(var(--sidebar-background));
  border-right: 1px solid hsl(var(--border));
  transition: width 0.2s ease;
}

.sidebar[data-collapsed="true"] {
  width: var(--sidebar-width-collapsed);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 3.5rem;
  padding: 0 1rem;
  border-bottom: 1px solid hsl(var(--border));
}

.logo {
  font-weight: 600;
  font-size: 1.125rem;
  transition: opacity 0.2s, width 0.2s;
}

.sidebar[data-collapsed="true"] .logo {
  opacity: 0;
  width: 0;
  overflow: hidden;
}

.toggleButton {
  flex-shrink: 0;
}

.nav {
  flex: 1;
  padding: 0.5rem;
  overflow-y: auto;
}

.navItem {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius);
  color: hsl(var(--sidebar-foreground));
  text-decoration: none;
  transition: background-color 0.15s;
  position: relative;
}

.navItem:hover {
  background-color: hsl(var(--sidebar-accent));
}

.navItem[data-active="true"] {
  background-color: hsl(var(--sidebar-accent));
  font-weight: 500;
}

.navItem[data-active="true"]::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 1.5rem;
  background-color: hsl(var(--primary));
  border-radius: 0 2px 2px 0;
}

.navIcon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

.navLabel {
  transition: opacity 0.2s, width 0.2s;
  white-space: nowrap;
}

.sidebar[data-collapsed="true"] .navLabel {
  opacity: 0;
  width: 0;
  overflow: hidden;
}
```

## Dynamic Theming with CSS Variables

### Brand Context (Sets Variables via JS)

```typescript
// contexts/brand-context.tsx
'use client'

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from 'react'

interface BrandSettings {
  primaryColor: string
  secondaryColor: string
  fontFamily: string
}

const defaultBrand: BrandSettings = {
  primaryColor: '#3b82f6',
  secondaryColor: '#64748b',
  fontFamily: 'Inter',
}

const BrandContext = createContext<{
  brand: BrandSettings
  updateBrand: (settings: Partial<BrandSettings>) => void
} | undefined>(undefined)

export function BrandProvider({ children }: { children: ReactNode }) {
  const [brand, setBrand] = useState<BrandSettings>(defaultBrand)

  useEffect(() => {
    const stored = localStorage.getItem('brand-settings')
    if (stored) {
      try {
        setBrand({ ...defaultBrand, ...JSON.parse(stored) })
      } catch {
        // Invalid JSON
      }
    }
  }, [])

  // Apply CSS variables - this is the ONLY place we touch the DOM directly
  useEffect(() => {
    const root = document.documentElement
    root.style.setProperty('--brand-primary', brand.primaryColor)
    root.style.setProperty('--brand-secondary', brand.secondaryColor)
    root.style.setProperty('--brand-font', brand.fontFamily)
  }, [brand])

  const updateBrand = (settings: Partial<BrandSettings>) => {
    const updated = { ...brand, ...settings }
    setBrand(updated)
    localStorage.setItem('brand-settings', JSON.stringify(updated))
  }

  return (
    <BrandContext.Provider value={{ brand, updateBrand }}>
      {children}
    </BrandContext.Provider>
  )
}

export function useBrand() {
  const context = useContext(BrandContext)
  if (!context) {
    throw new Error('useBrand must be used within a BrandProvider')
  }
  return context
}
```

### Using Brand Variables in CSS Modules

```css
/* components/shared/brand-card.module.css */
.card {
  background-color: hsl(var(--card));
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
  padding: 1.5rem;
}

.cardHeader {
  border-bottom: 2px solid var(--brand-primary);
  padding-bottom: 0.75rem;
  margin-bottom: 1rem;
}

.cardTitle {
  font-family: var(--brand-font);
  font-weight: 600;
  color: var(--brand-primary);
}

.cardAction {
  background-color: var(--brand-primary);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  border: none;
  cursor: pointer;
}

.cardAction:hover {
  filter: brightness(1.1);
}
```

## Dark Mode

### Theme Context

```typescript
// contexts/theme-context.tsx
'use client'

import { createContext, useContext, useEffect, useState } from 'react'

type Theme = 'light' | 'dark' | 'system'

const ThemeContext = createContext<{
  theme: Theme
  setTheme: (theme: Theme) => void
  resolvedTheme: 'light' | 'dark'
} | undefined>(undefined)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<Theme>('system')
  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light')

  useEffect(() => {
    const stored = localStorage.getItem('theme') as Theme | null
    if (stored) setThemeState(stored)
  }, [])

  useEffect(() => {
    const root = document.documentElement

    const applyTheme = (isDark: boolean) => {
      root.classList.toggle('dark', isDark)
      setResolvedTheme(isDark ? 'dark' : 'light')
    }

    if (theme === 'system') {
      const media = window.matchMedia('(prefers-color-scheme: dark)')
      applyTheme(media.matches)

      const listener = (e: MediaQueryListEvent) => applyTheme(e.matches)
      media.addEventListener('change', listener)
      return () => media.removeEventListener('change', listener)
    } else {
      applyTheme(theme === 'dark')
    }
  }, [theme])

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme)
    localStorage.setItem('theme', newTheme)
  }

  return (
    <ThemeContext.Provider value={{ theme, setTheme, resolvedTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) throw new Error('useTheme must be used within ThemeProvider')
  return context
}
```

### Theme Toggle with CSS Module

```typescript
// components/shared/theme-toggle.tsx
'use client'

import { Moon, Sun, Monitor } from 'lucide-react'
import { useTheme } from '@/contexts/theme-context'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import styles from './theme-toggle.module.css'

export function ThemeToggle() {
  const { theme, setTheme, resolvedTheme } = useTheme()

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className={styles.trigger}>
          <Sun className={styles.sunIcon} />
          <Moon className={styles.moonIcon} />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => setTheme('light')}>
          <Sun className={styles.menuIcon} />
          Light
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme('dark')}>
          <Moon className={styles.menuIcon} />
          Dark
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme('system')}>
          <Monitor className={styles.menuIcon} />
          System
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

```css
/* components/shared/theme-toggle.module.css */
.trigger {
  position: relative;
}

.sunIcon {
  height: 1rem;
  width: 1rem;
  transition: transform 0.3s, opacity 0.3s;
}

.moonIcon {
  position: absolute;
  height: 1rem;
  width: 1rem;
  transition: transform 0.3s, opacity 0.3s;
}

:global(.dark) .sunIcon {
  transform: rotate(90deg) scale(0);
  opacity: 0;
}

:global(.dark) .moonIcon {
  transform: rotate(0deg) scale(1);
  opacity: 1;
}

:global(:not(.dark)) .sunIcon {
  transform: rotate(0deg) scale(1);
  opacity: 1;
}

:global(:not(.dark)) .moonIcon {
  transform: rotate(-90deg) scale(0);
  opacity: 0;
}

.menuIcon {
  margin-right: 0.5rem;
  height: 1rem;
  width: 1rem;
}
```

## Common Utility Classes in globals.css

```css
/* app/globals.css - add after variables */

/* Glass effects */
.glass-card {
  background: hsl(var(--card) / 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid hsl(var(--border) / 0.5);
  border-radius: var(--radius);
}

/* Animations */
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.2s ease-out;
}

.animate-slide-up {
  animation: slide-up 0.3s ease-out;
}
```

## Summary: Styling Decision Tree

```
Need styling for a component?
│
├─ Simple layout/spacing only?
│   └─ Use Tailwind utilities (flex, p-4, gap-2, etc.)
│
├─ State-dependent styles (collapsed, active, variant)?
│   └─ Create .module.css + use data-* attributes
│
├─ Brand/theme colors?
│   └─ Use CSS variables in .module.css (var(--brand-primary))
│
├─ Complex animations or pseudo-elements?
│   └─ Create .module.css
│
└─ Never use inline style={{ }} props
```
