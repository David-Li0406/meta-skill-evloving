# Animation Specifications Reference

## Animation Principles for Games

### Timing Standards

| Animation Type | Duration | Easing |
|----------------|----------|--------|
| Micro-interaction | 100-200ms | ease-out |
| UI transition | 200-300ms | ease-in-out |
| Page transition | 300-500ms | ease-in-out |
| Character action | 400-800ms | custom bezier |
| Celebration/Win | 1000-2000ms | spring/bounce |
| Loading indicator | Loop | linear |

### Easing Functions

```css
/* Recommended easings for game feel */
--ease-snappy: cubic-bezier(0.2, 0, 0, 1);
--ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
--ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
--ease-dramatic: cubic-bezier(0.7, 0, 0.3, 1);

/* Spring physics approximation */
--spring-gentle: cubic-bezier(0.175, 0.885, 0.32, 1.275);
--spring-bouncy: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

## Sprite Animation Specs

### Frame Rate Guidelines

| Animation Type | FPS | Total Frames |
|----------------|-----|--------------|
| Idle loop | 8-12 | 4-8 |
| Walk cycle | 12-16 | 6-8 |
| Action (quick) | 16-24 | 4-6 |
| Action (dramatic) | 12-16 | 8-12 |
| Particle effect | 24-30 | 8-16 |

### Sprite Animation CSS

```css
.simulin-idle {
  width: 64px;
  height: 64px;
  background: url('simulin-sheet.png');
  animation: idle 0.8s steps(4) infinite;
}

@keyframes idle {
  from { background-position: 0 0; }
  to { background-position: -256px 0; }
}

/* Ping-pong animation */
.simulin-breathe {
  animation: breathe 1.6s steps(4) infinite alternate;
}
```

### Animation State Machine

```
┌─────────┐    move     ┌─────────┐
│  IDLE   │ ──────────► │  WALK   │
└────┬────┘             └────┬────┘
     │                       │
     │ action               │ action
     ▼                       ▼
┌─────────┐             ┌─────────┐
│ ACTION  │             │ ACTION  │
└────┬────┘             └────┬────┘
     │                       │
     │ complete             │ complete
     ▼                       ▼
   IDLE ◄─────────────────► WALK
```

## Lottie Animations

### When to Use Lottie

✅ Good for:
- Complex vector animations
- UI celebrations (confetti, stars)
- Loading states
- Animated icons
- Character expressions

❌ Avoid for:
- Full character sprites
- Pixel art
- Continuous game loops
- Performance-critical animations

### Lottie Integration

```tsx
import Lottie from 'lottie-react';
import winAnimation from './animations/win-celebration.json';

const WinCelebration = () => (
  <Lottie
    animationData={winAnimation}
    loop={false}
    autoplay={true}
    style={{ width: 200, height: 200 }}
    onComplete={() => console.log('Animation done')}
  />
);
```

### Lottie Export Settings

From After Effects:
- 30fps (or 60 for smooth)
- Body Movin plugin
- Enable "Glyphs" for text
- "Include guide layers" OFF
- Compress with lottie-compress

Target file sizes:
- Simple icon: <10KB
- Medium complexity: <50KB
- Complex celebration: <150KB

## CSS Animation Patterns

### Coin/Currency Pop

```css
@keyframes coin-pop {
  0% { 
    transform: scale(0) rotate(-180deg);
    opacity: 0;
  }
  50% { 
    transform: scale(1.2) rotate(10deg);
  }
  100% { 
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
}

.coin-reward {
  animation: coin-pop 0.4s var(--spring-bouncy) forwards;
}
```

### Card Flip

```css
.card {
  perspective: 1000px;
}

.card-inner {
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.card.flipped .card-inner {
  transform: rotateY(180deg);
}

.card-front, .card-back {
  backface-visibility: hidden;
}

.card-back {
  transform: rotateY(180deg);
}
```

### Shimmer/Loading

```css
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--bg-dim) 25%,
    var(--bg-bright) 50%,
    var(--bg-dim) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
```

### Trouble Pulse (Hex Grid)

```css
@keyframes trouble-pulse {
  0%, 100% { 
    box-shadow: 0 0 0 0 rgba(255, 100, 100, 0.4);
  }
  50% { 
    box-shadow: 0 0 20px 10px rgba(255, 100, 100, 0);
  }
}

.hex-trouble {
  animation: trouble-pulse 2s ease-in-out infinite;
}
```

## Audio Sync Points

For animations that need sound:

```javascript
const animationWithSound = {
  keyframes: [
    { time: 0, event: 'start' },
    { time: 0.2, event: 'impact', sound: 'coin_land.mp3' },
    { time: 0.4, event: 'settle' },
    { time: 0.6, event: 'complete', sound: 'cha_ching.mp3' }
  ]
};
```

Document sync points in animation specs for audio team.
