---
name: neon-glass-ui
description: Dark Neon Glassmorphism design system for Ionic/Vue 3/Vite PWA apps targeting iOS/iPhone. Use this skill when building productivity apps (Pomodoro, Breathing, Tabata, Todo, Habit trackers) with a futuristic NFT-marketplace aesthetic featuring fluid gradients, glass cards, and ambient glow effects. Triggers on requests for mobile app UI, timer apps, wellness apps, or any iOS PWA with dark neon/glass styling.
---

# Neon Glass UI System for FastApps

A complete design system implementing "Dark Neon Glassmorphism" aesthetic for the **FastApps** project (Ionic 7+ / Vue 3 / Vite).

## Visual Identity

**Vibe:** Deep space, futuristic, vibrant, liquid fluid art — NFT marketplace meets productivity tools.

## FastApps Project Structure

This skill follows the FastApps architecture:

```
fastapps/
├── src/
│   ├── apps/                    # Individual app components
│   │   ├── breathing/           # Example: BreathingApp.vue
│   │   ├── tabata/              # Example: TabataApp.vue
│   │   ├── pomodoro/            # Your new app
│   │   └── _template/           # Template for new apps
│   ├── components/
│   │   └── app/                 # AppHeader, etc.
│   ├── composables/             # useAppTheme, etc.
│   ├── styles/                  # Global styles
│   │   └── neon-glass.css       # ADD: Neon Glass theme
│   ├── views/
│   ├── router/
│   └── main.js
├── public/
│   └── apps/
│       ├── apps-list.json       # Register app here
│       └── your-app/
│           └── app.yaml         # App metadata
```

## Quick Start — Adding a New App

### Step 1: Create App Component

```bash
cp -r src/apps/_template src/apps/pomodoro
mv src/apps/pomodoro/TemplateApp.vue src/apps/pomodoro/PomodoroApp.vue
```

### Step 2: Create App Metadata

`public/apps/pomodoro/app.yaml`:
```yaml
name: Pomodoro
description: Focus timer with liquid gradient visualization
emoji: 🍅
color: "linear-gradient(135deg, #FF0080 0%, #7209B7 100%)"
```

### Step 3: Register in apps-list.json

```json
{
  "apps": ["breathing", "tabata", "pomodoro"]
}
```

### Step 4: Add Route

`src/router/index.js`:
```javascript
import PomodoroApp from '../apps/pomodoro/PomodoroApp.vue'

const routes = [
  // ... existing routes
  {
    path: '/apps/pomodoro',
    name: 'PomodoroApp',
    component: PomodoroApp
  }
]
```

## Core Design Tokens

### Color Palette

```css
:root {
  /* Backgrounds (never pure black) */
  --neon-bg-deep: #0A0A12;
  --neon-bg-primary: #0D0D1A;
  --neon-bg-elevated: #1A1A2E;
  --neon-bg-card: rgba(30, 30, 50, 0.6);
  
  /* Accent Colors */
  --neon-pink: #FF0080;
  --neon-purple: #7209B7;
  --neon-blue: #4361EE;
  --neon-cyan: #00D9FF;
  --neon-teal: #06D6A0;
  --neon-orange: #FF6B35;
  --neon-red: #FF3366;
  
  /* Text */
  --neon-text-primary: #FFFFFF;
  --neon-text-secondary: #A0A0B8;
  --neon-text-tertiary: #6B6B80;
  
  /* Glass */
  --neon-glass-bg: rgba(30, 30, 50, 0.6);
  --neon-glass-border: rgba(255, 255, 255, 0.08);
}
```

## Mandatory Patterns

### 1. App Component Structure

Every app MUST use this structure with `useAppTheme`:

```vue
<template>
  <ion-page class="neon-app">
    <!-- Ambient glow background -->
    <div class="ambient-glow">
      <div class="ambient-glow__orb ambient-glow__orb--1"></div>
      <div class="ambient-glow__orb ambient-glow__orb--2"></div>
    </div>
    
    <!-- Header using FastApps component -->
    <AppHeader 
      title="App Name" 
      :show-settings="true" 
      @settings="openSettings" 
    />
    
    <ion-content :fullscreen="true" class="ion-no-border">
      <div class="app-content">
        <!-- Your content -->
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { IonPage, IonContent } from '@ionic/vue'
import AppHeader from '@/components/app/AppHeader.vue'
import { useAppTheme } from '@/composables/useAppTheme'

// Apply neon gradient theme (start color, end color)
useAppTheme('#FF0080', '#7209B7')
</script>

<style scoped>
.neon-app {
  --background: var(--neon-bg-deep);
}

.app-content {
  padding: 20px;
  padding-top: calc(env(safe-area-inset-top) + 60px);
  padding-bottom: calc(env(safe-area-inset-bottom) + 100px);
}

/* Ambient Glow - REQUIRED */
.ambient-glow {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.ambient-glow__orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
}

.ambient-glow__orb--1 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #FF0080 0%, transparent 70%);
  top: -80px;
  right: -60px;
}

.ambient-glow__orb--2 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, #4361EE 0%, transparent 70%);
  bottom: -100px;
  left: -80px;
}

ion-content {
  --background: transparent;
}
</style>
```

### 2. Glass Card Pattern

**NEVER use solid opaque backgrounds.** Always glassmorphism:

```vue
<template>
  <div class="glass-card">
    <slot></slot>
  </div>
</template>

<style scoped>
.glass-card {
  background: rgba(30, 30, 50, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 20px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}
</style>
```

### 3. Gradient Button Pattern

```css
.btn-gradient {
  background: linear-gradient(135deg, #00D9FF 0%, #4361EE 50%, #7209B7 100%);
  border: none;
  border-radius: 100px;
  padding: 16px 32px;
  color: white;
  font-weight: 600;
  font-size: 16px;
  position: relative;
  overflow: hidden;
}

.btn-gradient::after {
  content: '';
  position: absolute;
  inset: -2px;
  background: inherit;
  border-radius: inherit;
  z-index: -1;
  filter: blur(15px);
  opacity: 0.5;
}

.btn-gradient:active {
  transform: scale(0.97);
}
```

## useAppTheme Integration

The FastApps project uses `useAppTheme` composable. Use neon colors:

```javascript
// Focus/Work modes - warm colors
useAppTheme('#FF0080', '#FF6B35')  // Pink to Orange
useAppTheme('#FF3366', '#FF0080')  // Red to Pink

// Rest/Calm modes - cool colors  
useAppTheme('#4361EE', '#00D9FF')  // Blue to Cyan
useAppTheme('#06D6A0', '#00D9FF')  // Teal to Cyan

// Neutral/Default
useAppTheme('#7209B7', '#4361EE')  // Purple to Blue
```

## App-Specific Implementations

See `references/components.md` for complete code:
- **Pomodoro**: Liquid blob timer with conic gradient fill
- **Breathing**: Expanding/contracting orb with ring animations
- **Tabata**: Color-shifting background (red work / blue rest)
- **Todo**: Glass slip list items with swipe actions

## Typography Rules

```css
/* Headings */
.heading-xl {
  font-size: 32px;
  font-weight: 700;
  color: #FFFFFF;
  letter-spacing: -0.5px;
}

/* Labels */
.label-caps {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 3px;
  color: #A0A0B8;
  text-transform: uppercase;
}

/* Timer Display */
.timer-display {
  font-size: 96px;
  font-weight: 700;
  color: white;
  font-variant-numeric: tabular-nums;
}
```

## Animation Guidelines

```css
/* Timing functions */
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
--ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);

/* Durations */
--duration-fast: 150ms;
--duration-normal: 300ms;
--duration-breath: 4000ms;

/* Ambient float animation */
@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(20px, -20px) scale(1.05); }
  66% { transform: translate(-15px, 15px) scale(0.95); }
}

.ambient-glow__orb {
  animation: float 8s ease-in-out infinite;
}
```

## iOS Safe Area Handling

Always include safe area padding:

```css
.app-content {
  padding-top: calc(env(safe-area-inset-top) + 60px);
  padding-bottom: calc(env(safe-area-inset-bottom) + 100px);
  padding-left: 20px;
  padding-right: 20px;
}
```

## Checklist Before Shipping

- [ ] App uses `useAppTheme()` with neon colors
- [ ] Ambient glow orbs present in template
- [ ] No solid black or plain backgrounds
- [ ] All cards use glassmorphism
- [ ] Safe area insets applied
- [ ] Buttons have gradient + glow shadow
- [ ] Typography uses correct weights/colors
- [ ] Animations use correct easing
- [ ] App registered in `apps-list.json`
- [ ] Route added to router
- [ ] YAML metadata created
