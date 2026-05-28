---
name: visual-polish
description: UI and visual polish checklist for game presentation
category: visual
depends-on: []
---

# Visual Polish Skill

> "The last 10% of polish takes 90% of the time – but it's worth it."

## When to Use This Skill

Use when:

- Finalizing visual presentation
- Creating UI elements and HUD
- Adding feedback animations
- Implementing transitions

## Polish Checklist

### Core Visuals

- [ ] **Lighting is balanced** - No blown highlights, no crushed shadows
- [ ] **Colors match GDD palette** - Consistent art direction
- [ ] **Materials look correct** - PBR values appropriate for materials
- [ ] **Silhouette is readable** - Objects identifiable from outline
- [ ] **Framing guides the eye** - Important elements draw attention

### Animation & Feedback

- [ ] **Buttons have hover states** - Visual feedback on interaction
- [ ] **Transitions are smooth** - No jarring cuts
- [ ] **Loading states exist** - User knows something is happening
- [ ] **Error states are clear** - Problems are visible and understandable
- [ ] **Success feedback exists** - Positive reinforcement

### UI Presentation

- [ ] **Typography is readable** - Appropriate sizes, weights, line heights
- [ ] **Contrast meets accessibility** - WCAG AA minimum (4.5:1 for text)
- [ ] **Spacing is consistent** - Grid/spacing system used
- [ ] **Alignment is intentional** - Elements line up properly
- [ ] **Hierarchy is clear** - Most important elements stand out

### Performance Polish

- [ ] **No visible frame drops** - 60 FPS maintained
- [ ] **Loading times are acceptable** - Assets optimized
- [ ] **Memory usage is stable** - No leaks or growing allocation
- [ ] **Mobile tested** - Works on target mobile devices

## UI Component Polish Template

```tsx
import { useState } from 'react';
import { html } from '@react-three/drei';
import { motion, AnimatePresence } from 'framer-motion';

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
  loading?: boolean;
}

export function PolishedButton({
  label,
  onClick,
  variant = 'primary',
  disabled = false,
  loading = false,
}: ButtonProps) {
  const [isHovered, setIsHovered] = useState(false);

  const baseStyles = {
    padding: '12px 24px',
    borderRadius: '8px',
    fontWeight: 600,
    fontSize: '16px',
    border: 'none',
    cursor: disabled ? 'not-allowed' : 'pointer',
    transition: 'all 0.2s ease',
    opacity: disabled ? 0.5 : 1,
  };

  const variantStyles = {
    primary: {
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white',
      boxShadow: isHovered ? '0 8px 20px rgba(102, 126, 234, 0.4)' : '0 4px 10px rgba(102, 126, 234, 0.3)',
      transform: isHovered ? 'translateY(-2px)' : 'translateY(0)',
    },
    secondary: {
      background: 'white',
      color: '#667eea',
      border: '2px solid #667eea',
      boxShadow: isHovered ? '0 4px 15px rgba(102, 126, 234, 0.2)' : 'none',
    },
    danger: {
      background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
      color: 'white',
      boxShadow: isHovered ? '0 8px 20px rgba(245, 87, 108, 0.4)' : '0 4px 10px rgba(245, 87, 108, 0.3)',
    },
  };

  return (
    <motion.button
      style={{ ...baseStyles, ...variantStyles[variant] }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={!disabled && !loading ? onClick : undefined}
      whileTap={{ scale: disabled || loading ? 1 : 0.95 }}
      disabled={disabled || loading}
    >
      <AnimatePresence mode="wait">
        {loading ? (
          <motion.span
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <LoadingSpinner />
          </motion.span>
        ) : (
          <motion.span
            key="label"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            {label}
          </motion.span>
        )}
      </AnimatePresence>
    </motion.button>
  );
}
```

## Visual Feedback Patterns

### Hover Feedback

```tsx
<mesh
  onPointerOver={(e) => {
    e.object.scale.setScalar(1.1);
    document.body.style.cursor = 'pointer';
  }}
  onPointerOut={(e) => {
    e.object.scale.setScalar(1.0);
    document.body.style.cursor = 'default';
  }}
>
  <boxGeometry />
  <meshStandardMaterial color="orange" />
</mesh>
```

### Click Feedback

```tsx
function InteractiveMesh() {
  const meshRef = useRef<THREE.Mesh>(null);

  const handleClick = () => {
    // Scale animation
    if (meshRef.current) {
      gsap.to(meshRef.current.scale, {
        x: 1.2,
        y: 1.2,
        z: 1.2,
        duration: 0.1,
        yoyo: true,
        repeat: 1,
      });
    }
  };

  return (
    <mesh ref={meshRef} onClick={handleClick}>
      <sphereGeometry />
      <meshStandardMaterial color="blue" />
    </mesh>
  );
}
```

### Progress Feedback

```tsx
function ProgressBar({ progress }: { progress: number }) {
  return (
    <div className="progress-container">
      <div
        className="progress-bar"
        style={{
          width: `${Math.min(100, Math.max(0, progress * 100))}%`,
          transition: 'width 0.3s ease',
        }}
      />
    </div>
  );
}
```

## Color Guidelines

### Accessible Color Combinations

| Background | Text       | Ratio  | WCAG Level |
| ---------- | ---------- | ------ | ---------- |
| #FFFFFF    | #000000    | 21:1   | AAA        |
| #F5F5F5    | #333333    | 12.6:1 | AAA        |
| #667EEA    | #FFFFFF    | 4.5:1  | AA         |
| #F5576C    | #FFFFFF    | 4.2:1  | AA         |

### Common Mistakes

- ❌ Red/green as only differentiators (colorblindness)
- ❌ Light text on light background
- ❌ Pure colors (#FF0000, #00FF00) - too harsh
- ❌ Too many colors in one view

## Typography Guidelines

```css
/* Font scale - modular scale */
.text-xs { font-size: 0.75rem; }    /* 12px */
.text-sm { font-size: 0.875rem; }   /* 14px */
.text-base { font-size: 1rem; }     /* 16px */
.text-lg { font-size: 1.125rem; }   /* 18px */
.text-xl { font-size: 1.25rem; }    /* 20px */
.text-2xl { font-size: 1.5rem; }    /* 24px */
.text-3xl { font-size: 1.875rem; }  /* 30px */
.text-4xl { font-size: 2.25rem; }   /* 36px */

/* Weights */
.font-light { font-weight: 300; }
.font-normal { font-weight: 400; }
.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }
```

## Spacing System

```css
/* 8px base unit */
.space-1 { padding: 0.25rem; }  /* 4px */
.space-2 { padding: 0.5rem; }   /* 8px */
.space-3 { padding: 0.75rem; }  /* 12px */
.space-4 { padding: 1rem; }     /* 16px */
.space-5 { padding: 1.25rem; }  /* 20px */
.space-6 { padding: 1.5rem; }   /* 24px */
.space-8 { padding: 2rem; }     /* 32px */
.space-10 { padding: 2.5rem; }  /* 40px */
.space-12 { padding: 3rem; }    /* 48px */
```

## Anti-Patterns

❌ **DON'T:**

- Use placeholder colors (magenta, lime green)
- Skip hover states on interactive elements
- Use too many fonts (>2 typefaces)
- Inconsistent spacing
- No feedback for user actions
- Text on busy backgrounds without contrast

✅ **DO:**

- Use colors from GDD palette
- Provide visual feedback for all interactions
- Limit fonts to 1-2 typefaces
- Follow spacing system consistently
- Test for color blindness
- Ensure text readability

## Checklist

Before considering visual polish complete:

- [ ] All interactive elements have hover/click states
- [ ] Loading states exist for async operations
- [ ] Error messages are clear and actionable
- [ ] Success feedback is provided
- [ ] Colors meet accessibility standards
- [ ] Typography is consistent and readable
- [ ] Spacing follows system
- [ ] Transitions are smooth (200-300ms)
- [ ] Performance tested on target devices
- [ ] Visual style matches GDD

## Reference

- [WCAG Color Contrast](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [Type Scale Calculator](https://type-scale.com/)
- [skills/postfx-effects.md](postfx-effects.md) — Post-processing polish
