---
name: Responsive Scaling
description: Implement viewport-based scaling for cross-device visual parity
---

# Responsive Scaling Skill

## Overview
Ensure visual parity across all device sizes using the Universal Scaling Standard.

## Scaling Patterns

### Pattern A: Content Zoom (vw-based)
Use for high-density layouts (dashboards, complex UIs):
```css
.content-container {
  font-size: clamp(14px, 1.5vw, 18px);
  --spacing-unit: clamp(8px, 1vw, 16px);
}
```

### Pattern B: Spatial Viewport
Use for spatial layouts (lobby, orb navigation):
```css
.lobby-item {
  width: 30vw;
  height: 30vw;
  max-width: 300px;
  max-height: 300px;
}
```

### Pattern C: Fixed Aspect (3:4 Portrait)
Use for game canvases (poker table, training):
```css
.game-canvas {
  width: 100%;
  max-width: 600px;
  aspect-ratio: 3 / 4;
}

/* Inner elements scale with container */
.game-element {
  font-size: calc(var(--canvas-width) * 0.03);
}
```

## Training Game Scaling

### Design Canvas: 600x800 (3:4)
```jsx
function TrainingGame({ width }) {
  const scale = width / 600;  // 600 = design width
  
  return (
    <div style={{ 
      width: '100%', 
      maxWidth: 600,
      aspectRatio: '3/4',
      transform: `scale(${scale})`,
      transformOrigin: 'top left'
    }}>
      {/* All child elements designed for 600x800 */}
    </div>
  );
}
```

### Position Calculation
```javascript
// Design-time position (out of 600x800)
const designPos = { x: 150, y: 400 };

// Runtime position
const runtimePos = {
  x: designPos.x * scale,
  y: designPos.y * scale
};
```

## Breakpoint System

```css
/* Mobile first */
.component {
  padding: 12px;
  font-size: 14px;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .component {
    padding: 16px;
    font-size: 16px;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .component {
    padding: 24px;
    font-size: 18px;
  }
}

/* Large (1440px+) */
@media (min-width: 1440px) {
  .component {
    padding: 32px;
  }
}
```

## useScale Hook
```javascript
function useScale(designWidth = 600) {
  const [scale, setScale] = useState(1);
  const containerRef = useRef(null);
  
  useEffect(() => {
    const updateScale = () => {
      if (containerRef.current) {
        const containerWidth = containerRef.current.offsetWidth;
        setScale(Math.min(containerWidth / designWidth, 1));
      }
    };
    
    updateScale();
    window.addEventListener('resize', updateScale);
    return () => window.removeEventListener('resize', updateScale);
  }, [designWidth]);
  
  return { scale, containerRef };
}
```

## Best Practices

### 1. Inline Styles for Mission-Critical
```jsx
// Use inline styles for position-critical elements
<div style={{ 
  left: `${pos.x * scale}px`, 
  top: `${pos.y * scale}px` 
}} />
```

### 2. Test Key Widths
- 375px (iPhone SE)
- 414px (iPhone Pro)
- 768px (iPad)
- 1024px (iPad Pro)
- 1440px (Desktop)
- 1920px (Full HD)

### 3. Avoid Fixed Pixel Values
```css
/* BAD */
.element { width: 200px; }

/* GOOD */
.element { width: 33%; max-width: 200px; }
```

### 4. Touch Targets
Minimum 44px × 44px for mobile interaction:
```css
.button {
  min-height: 44px;
  min-width: 44px;
}
```
