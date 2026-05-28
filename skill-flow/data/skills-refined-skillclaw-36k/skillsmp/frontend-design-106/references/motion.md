# Motion Reference

## Contents
- Animation Classes
- Keyframe Definitions
- Stagger Patterns
- Hover Transitions
- Performance Notes

## Animation Classes

Defined in `app/globals.css`:

| Class | Duration | Easing | Use |
|-------|----------|--------|-----|
| `animate-fadeIn` | 0.6s | ease-out | Page elements on load |
| `animate-slideIn` | 0.8s | ease-out | Lateral entrance |
| `animate-pulse-slow` | 3s infinite | ease-in-out | Emphasis on icons, stats |
| `animate-float` | 6s infinite | ease-in-out | Floating icons |
| `shimmer` | 2s infinite | ease-out | Loading states, card bars |

### Delay Utilities

```tsx
.delay-100 { animation-delay: 0.1s; }
.delay-200 { animation-delay: 0.2s; }
.delay-300 { animation-delay: 0.3s; }
.delay-400 { animation-delay: 0.4s; }
```

## Keyframe Definitions

### fadeIn

```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### float

```css
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
```

### gradient (for text-gradient)

```css
@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

## Stagger Patterns

### Index-Based Delay

```tsx
{items.map((item, index) => (
  <div
    key={index}
    className="animate-fadeIn"
    style={{ animationDelay: `${(index + 1) * 0.1}s` }}
  >
    {/* Content */}
  </div>
))}
```

### CSS nth-child (Service Cards)

Defined in globals.css for automatic staggering:

```css
.service-card:nth-child(1) { animation-delay: 0.1s; }
.service-card:nth-child(2) { animation-delay: 0.2s; }
/* ... up to 9 */
```

### Manual Delay Classes

```tsx
<div className="animate-fadeIn">First</div>
<div className="animate-fadeIn delay-100">Second</div>
<div className="animate-fadeIn delay-200">Third</div>
<div className="animate-fadeIn delay-300">Fourth</div>
```

## Hover Transitions

### Service Card Hover

```css
.service-card {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.service-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}
```

### CTA Button Shimmer

```css
.cta-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.cta-button:hover::before {
  left: 100%;
}
```

### Standard Transition Classes

```tsx
// Fast color transitions
className="hover:text-green-400 transition-colors"

// All properties with scale
className="transform hover:scale-105 transition-all"

// Specific duration
className="transition-all duration-300"
```

## Performance Notes

### WARNING: Animation on Large Lists

**The Problem:**
```tsx
// BAD - 100 items all animating
{items.map((item, index) => (
  <div className="animate-fadeIn" style={{ animationDelay: `${index * 0.1}s` }}>
```

**Why This Breaks:** Browser calculates 100 animations. Jank on mobile.

**The Fix:** Cap stagger to first 9-12 items or use `will-change: transform` sparingly.

### transform vs margin Animation

Always animate `transform` or `opacity`, never `margin`, `padding`, `top`, `left`:

```tsx
// GOOD - GPU accelerated
className="transform hover:-translate-y-2"

// BAD - triggers layout
style={{ marginTop: isHovered ? '-8px' : '0' }}
```

### Loading Spinner

```tsx
<div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
```

Uses Tailwind's built-in `animate-spin` (60fps rotation).