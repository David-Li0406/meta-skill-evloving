---
name: UI Visual System
description: Implement the premium visual design system for Smarter.Poker
---

# UI Visual System Skill

## Overview
Implement the premium visual design system with dark themes, neon accents, and modern poker aesthetics.

## Color System

### Primary Palette
```css
:root {
  /* Backgrounds */
  --bg-primary: #0a0a0f;
  --bg-secondary: #14141f;
  --bg-card: #1a1a2e;
  --bg-elevated: #22223a;
  
  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #a0a0b0;
  --text-muted: #6b6b7b;
  
  /* Accents */
  --accent-cyan: #00f5ff;
  --accent-gold: #ffd700;
  --accent-pink: #ff69b4;
  --accent-green: #00ff88;
  --accent-red: #ff4757;
  
  /* Gradients */
  --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --gradient-gold: linear-gradient(90deg, #8B6914 0%, #C9A227 50%, #8B6914 100%);
  --gradient-dark: linear-gradient(180deg, #1a1a2e 0%, #0a0a0f 100%);
}
```

### Glow Effects
```css
/* Neon glow */
.neon-cyan {
  box-shadow: 0 0 10px #00f5ff, 0 0 20px rgba(0, 245, 255, 0.3);
}

.neon-gold {
  box-shadow: 0 0 10px #ffd700, 0 0 20px rgba(255, 215, 0, 0.3);
}

/* Text glow */
.text-glow {
  text-shadow: 0 0 10px currentColor;
}
```

## Component Patterns

### Cards
```css
.premium-card {
  background: rgba(26, 26, 46, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
}
```

### Buttons
```css
.btn-primary {
  background: var(--gradient-primary);
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  color: white;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
}
```

### Input Fields
```css
.input-premium {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 12px 16px;
  color: white;
  transition: border-color 0.2s;
}

.input-premium:focus {
  border-color: var(--accent-cyan);
  outline: none;
}
```

## Animation Standards

### Micro-interactions
```css
/* Hover lift */
.hover-lift:hover {
  transform: translateY(-4px);
  transition: transform 0.2s ease-out;
}

/* Scale pop */
.scale-pop:active {
  transform: scale(0.95);
}

/* Fade in */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Loading States
```css
/* Pulse skeleton */
.skeleton {
  background: linear-gradient(90deg, #1a1a2e 25%, #22223a 50%, #1a1a2e 75%);
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s infinite;
}

@keyframes skeleton-pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

## Glassmorphism
```css
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

## Typography

### Font Stack
```css
font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
```

### Size Scale
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
```

## Responsive Breakpoints
```css
--mobile: 375px;
--tablet: 768px;
--desktop: 1024px;
--large: 1440px;
```

## Best Practices
1. Always use CSS custom properties for colors
2. Prefer `transform` and `opacity` for animations (GPU accelerated)
3. Use `backdrop-filter` sparingly (performance impact)
4. Test on dark backgrounds - avoid pure white text
5. Maintain 4.5:1 contrast ratio for accessibility
