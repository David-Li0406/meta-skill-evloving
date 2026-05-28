---
name: game-ui-animations
description: Game UI and HUD animation patterns for React Three Fiber games
category: development
depends-on: [r3f-fundamentals]
---

# Game UI Animations Skill

> "Smooth, responsive UI animations provide critical game feel feedback."

## When to Use This Skill

Use when:
- Creating HUD elements (kill feed, score updates, notifications)
- Adding entry/exit animations for UI panels
- Implementing smooth value transitions (timer countdown, health bars)
- Building notification systems
- Creating interactive menu transitions

## Quick Start

```tsx
import { motion, AnimatePresence } from 'motion/react';

// Kill feed entry animation
function KillFeedEntry({ kill, onExit }) {
  return (
    <AnimatePresence>
      <motion.div
        initial={{ x: 100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        exit={{ x: -100, opacity: 0 }}
        transition={{ duration: 0.3, ease: 'easeOut' }}
        onAnimationComplete={onExit}
      >
        {kill.killer} splatted {kill.victim}
      </motion.div>
    </AnimatePresence>
  );
}
```

## Decision Framework

| Need                          | Use                                      |
| ----------------------------- | ---------------------------------------- |
| Simple entry/exit animations  | CSS transitions with Tailwind classes    |
| Complex choreography          | Motion (Framer Motion) variants           |
| Continuous value updates      | CSS transforms with requestAnimationFrame |
| 3D UI attached to camera      | R3F Html component + CSS animations       |
| High-frequency updates        | Transform only (no layout triggers)       |

## Progressive Guide

### Level 1: CSS-Only Animations (Fastest)

For simple, high-performance HUD elements:

```tsx
// Tailwind + custom CSS for kill feed
function KillFeedItem({ killer, victim }) {
  return (
    <div className="kill-feed-item animate-slide-in">
      <span className="killer-name">{killer}</span>
      <span className="skull-icon">💀</span>
      <span className="victim-name">{victim}</span>
    </div>
  );
}

/* CSS - Add to global styles */
@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

.kill-feed-item {
  animation: slideIn 0.3s ease-out;
  will-change: transform, opacity; /* GPU hint */
}

.kill-feed-item.exiting {
  animation: fadeOut 0.3s ease-out forwards;
}
```

**When to use**: Simple entry/exit, predictable timing, no user interaction

### Level 2: Motion (Framer Motion) for Complex UI

For interactive, state-driven animations:

```tsx
import { motion, AnimatePresence } from 'motion/react';

function KillFeed({ kills }) {
  return (
    <div className="kill-feed">
      <AnimatePresence mode="popLayout">
        {kills.map((kill) => (
          <motion.div
            key={kill.id}
            layout
            initial={{ x: 100, opacity: 0, scale: 0.8 }}
            animate={{ x: 0, opacity: 1, scale: 1 }}
            exit={{ x: -100, opacity: 0, scale: 0.8 }}
            transition={{
              type: 'spring',
              stiffness: 300,
              damping: 25
            }}
            className="kill-entry"
          >
            <span className="killer">{kill.killer}</span>
            <span>⚔️</span>
            <span className="victim">{kill.victim}</span>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
```

**When to use**: List reordering, spring physics, gesture interactions

### Level 3: Timer and Progress Bar Animations

Smooth countdown animations:

```tsx
import { useState, useEffect } from 'react';

function MatchTimer({ duration, remaining }) {
  const progress = remaining / duration;

  return (
    <div className="match-timer">
      <motion.div
        className="timer-bar"
        style={{
          scaleX: progress,
          transformOrigin: 'left'
        }}
        transition={{ ease: 'linear', duration: 1 }}
      />
      <span className="timer-text">
        {Math.floor(remaining / 60)}:{(remaining % 60).toString().padStart(2, '0')}
      </span>
    </div>
  );
}

/* CSS */
.timer-bar {
  width: 100%;
  height: 4px;
  background: #ff6b35;
  will-change: transform; /* GPU acceleration for scaleX */
}
```

### Level 4: Health/Ink Bar with Color Transition

```tsx
function InkTankIndicator({ current, max }) {
  const percentage = (current / max) * 100;

  // Color transitions from blue (full) to red (low)
  const color = percentage > 50
    ? '#3b82f6' // blue
    : percentage > 25
    ? '#f59e0b' // orange
    : '#ef4444'; // red

  return (
    <div className="ink-tank">
      <motion.div
        className="ink-level"
        style={{ backgroundColor: color }}
        animate={{ width: `${percentage}%` }}
        transition={{ type: 'spring', stiffness: 200, damping: 20 }}
      />
      <span className="ink-text">{Math.floor(current)} / {max}</span>
    </div>
  );
}
```

### Level 5: Notification System with Stacking

```tsx
function NotificationSystem({ notifications }) {
  return (
    <div className="notifications">
      <AnimatePresence>
        {notifications.map((notification, index) => (
          <motion.div
            key={notification.id}
            initial={{ y: -50, opacity: 0 }}
            animate={{
              y: index * 60, // Stack based on index
              opacity: 1
            }}
            exit={{ y: -50, opacity: 0 }}
            transition={{
              type: 'spring',
              stiffness: 400,
              damping: 30
            }}
            className={`notification ${notification.type}`}
          >
            {notification.message}
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
```

## Performance Best Practices

### GPU-Accelerated Properties Only

```css
/* ✅ GOOD - GPU accelerated */
.smooth-animation {
  transform: translateX(100px);
  opacity: 0.5;
  will-change: transform, opacity;
}

/* ❌ BAD - Triggers layout */
.bad-animation {
  left: 100px;
  width: 50px;
  height: 50px;
}
```

### Animation Performance Checklist

- [ ] Only animate `transform` and `opacity` for 60fps
- [ ] Use `will-change` sparingly (only for currently animating elements)
- [ ] Avoid animating `width`, `height`, `left`, `top`
- [ ] Use `transform: translateZ(0)` or `will-change` to force GPU layer
- [ ] Remove `will-change` after animation completes
- [ ] Use CSS animations for simple, repetitive animations
- [ ] Use Motion for complex, interactive animations
- [ ] Batch DOM reads/writes to avoid layout thrashing

### will-change Pattern

```css
/* Before animation starts */
.animating {
  will-change: transform, opacity;
}

/* After animation completes - clean up */
.finished {
  will-change: auto;
}
```

## Game UI Animation Patterns

### Kill Feed Pattern

```tsx
function KillFeed() {
  const [kills, setKills] = useState<Kill[]>([]);

  const addKill = (kill: Kill) => {
    setKills(prev => [...prev, kill]);
    // Auto-remove after 5 seconds
    setTimeout(() => {
      setKills(prev => prev.filter(k => k.id !== kill.id));
    }, 5000);
  };

  return (
    <div className="kill-feed">
      <AnimatePresence mode="popLayout">
        {kills.slice(-5).map((kill) => ( // Show last 5
          <motion.div
            key={kill.id}
            initial={{ x: 100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -100, opacity: 0 }}
            transition={{ duration: 0.25 }}
          >
            {kill.killer} 💀 {kill.victim}
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}
```

### Score Update Pattern

```tsx
function TeamScore({ score, delta }) {
  return (
    <div className="team-score">
      <span className="score-value">{score}</span>
      {delta !== 0 && (
        <motion.span
          key={score} // Re-trigger animation on score change
          initial={{ y: 0, opacity: 1 }}
          animate={{ y: -20, opacity: 0 }}
          exit={{ opacity: 0 }}
          className="score-delta"
          transition={{ duration: 0.5 }}
        >
          {delta > 0 ? '+' : ''}{delta}
        </motion.span>
      )}
    </div>
  );
}
```

### Low Warning Pattern

```css
/* Pulsing red animation for low ink/health */
@keyframes pulse-red {
  0%, 100% {
    box-shadow: 0 0 5px rgba(239, 68, 68, 0.5);
  }
  50% {
    box-shadow: 0 0 20px rgba(239, 68, 68, 0.8);
  }
}

.low-warning {
  animation: pulse-red 1s ease-in-out infinite;
}
```

## Anti-Patterns

❌ **DON'T:**

- Use `setInterval` for animations (use `requestAnimationFrame` or CSS)
- Animate layout properties (`width`, `height`, `left`, `top`)
- Leave `will-change` on elements permanently
- Create new animation controllers on every render
- Use heavy JS animation libraries for simple transitions
- Forget to cleanup AnimatePresence children

✅ **DO:**

- Use CSS animations for repetitive, predictable effects
- Animate only `transform` and `opacity` for 60fps
- Use Motion's `AnimatePresence` for enter/exit
- Set unique keys for animated list items
- Use `layout` prop for smooth reordering
- Clean up animations in useEffect return

## Code Patterns

### Staggered List Animation

```tsx
function StaggeredList({ items }) {
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const item = {
    hidden: { opacity: 0, x: -20 },
    show: { opacity: 1, x: 0 }
  };

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
    >
      {items.map((item) => (
        <motion.div key={item.id} variants={item}>
          {item.content}
        </motion.div>
      ))}
    </motion.div>
  );
}
```

### R3F Html + CSS Animation

```tsx
import { Html } from '@react-three/drei';

function PlayerLabel({ name }) {
  return (
    <Html position={[0, 2, 0]} center>
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        className="player-label"
      >
        {name}
      </motion.div>
    </Html>
  );
}

/* CSS */
.player-label {
  background: rgba(0, 0, 0, 0.7);
  padding: 4px 8px;
  border-radius: 4px;
  color: white;
  font-size: 12px;
  pointer-events: none;
  will-change: transform; /* GPU acceleration for scale */
}
```

## Checklist

Before implementing game UI animations:

- [ ] Using GPU-accelerated properties (transform, opacity)
- [ ] CSS animations for simple, repetitive effects
- [ ] Motion for complex, interactive animations
- [ ] Proper cleanup with AnimatePresence
- [ ] Unique keys for animated list items
- [ ] will-change applied only during animation
- [ ] Animation duration feels responsive (≤ 300ms for UI feedback)
- [ ] Tested on target frame rate (60fps)

## Reference

- [Motion documentation](https://motion.dev/docs/react-animation) — Framer Motion v2
- [R3F Html component](https://drei.pmnd.rs/docs/rendering/html) — 3D positioned HTML
- [CSS GPU Acceleration Guide](https://www.smashingmagazine.com/2016/12/gpu-animation-doing-it-right/) — Performance best practices
- [MDN Performance Fundamentals](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Fundamentals) — Web performance guide
