---
name: motion-v
description: Use this skill when adding animations with Motion Vue (motion-v) to create hardware-accelerated, production-ready animations for Vue 3 and Nuxt applications.
---

# Motion Vue (motion-v)

Animation library for Vue 3 and Nuxt. Provides a motion component API, gesture animations, scroll-linked effects, layout transitions, and composables.

## When to Use

**Use Motion Vue for:**

- Simple declarative animations (fade, slide, scale)
- Gesture-based interactions (hover, tap, drag)
- Scroll-linked animations
- Layout animations and shared element transitions
- Spring physics animations

**Consider alternatives:**

- **GSAP** - For complex timelines, SVG morphing, and scroll-triggered sequences.
- **@vueuse/motion** - For a simpler API with fewer features and a smaller bundle size.
- **CSS animations** - For simple transitions without JavaScript.

## Installation

```bash
# Vue 3
pnpm add motion-v

# Nuxt 3
pnpm add motion-v @vueuse/nuxt
```

```ts
// nuxt.config.ts - Nuxt 3 setup
export default defineNuxtConfig({
  modules: ['motion-v/nuxt'],
})
```

## Quick Reference

| Working on...                | Load file                 |
| ---------------------------- | ------------------------- |
| Motion component, gestures   | references/components.md  |
| useMotionValue, useScroll    | references/composables.md |
| Animation examples, patterns | references/examples.md    |

## Core Concepts

### Motion Component

Render any HTML/SVG element with animation capabilities:

```vue
<script setup lang="ts">
import { Motion } from 'motion-v'
</script>

<template>
  <Motion.div
    :initial="{ opacity: 0, y: 20 }"
    :animate="{ opacity: 1, y: 0 }"
    :exit="{ opacity: 0, y: -20 }"
    :transition="{ duration: 0.3 }"
  >
    Animated content
  </Motion.div>
</template>
```

### Gesture Animations

```vue
<Motion.button
  :whileHover="{ scale: 1.05 }"
  :whilePress="{ scale: 0.95 }"
  :transition="{ type: 'spring', stiffness: 400 }"
>
  Click me
</Motion.button>
```