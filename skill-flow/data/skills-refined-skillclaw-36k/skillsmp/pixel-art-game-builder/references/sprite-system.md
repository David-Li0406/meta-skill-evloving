# Sprite System Reference

Complete guide for procedural pixel art sprite generation via Canvas API.

## Sprite Specifications

| Property | Value |
|----------|-------|
| Source size | 16×16 px |
| Display size | 64×64 px |
| Scale factor | 4× |
| Usable zone | 12×12 px (center) |
| Margin | 2px (for glow effects) |
| Max colors | 4 per sprite |
| Animation frames | 2-4 max |

## Grid Layout (16×16)

```
    0 1 2 3 4 5 6 7 8 9 A B C D E F
   ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
 0 │M│M│M│M│M│M│M│M│M│M│M│M│M│M│M│M│  M = Margin (2px)
 1 │M│M│M│M│M│M│M│M│M│M│M│M│M│M│M│M│      Reserved for glow
 2 │M│M│ │ │ │ │ │ │ │ │ │ │ │ │M│M│
 3 │M│M│ │ │ │ │ │ │ │ │ │ │ │ │M│M│
 4 │M│M│ │ │ │ │ │ │ │ │ │ │ │ │M│M│
 5 │M│M│ │ │ │ │ │ │ │ │ │ │ │ │M│M│  Usable zone = 12×12
 6 │M│M│ │ │ │ │ │ │ │ │ │ │ │ │M│M│  (columns 2-D, rows 2-D)
 7 │M│M│ │ │ │ │ │ │◉│ │ │ │ │ │M│M│
 8 │M│M│ │ │ │ │ │ │ │ │ │ │ │ │M│M│  ◉ = Center (7.5, 7.5)
 9 │M│M│ │ │ │ │ │ │ │ │ │ │ │ │M│M│
 A │M│M│ │ │ │ │ │ │ │ │ │ │ │ │M│M│
 B │M│M│ │ │ │ │ │ │ │ │ │ │ │ │M│M│
 C │M│M│ │ │ │ │ │ │ │ │ │ │ │ │M│M│
 D │M│M│ │ │ │ │ │ │ │ │ │ │ │ │M│M│
 E │M│M│M│M│M│M│M│M│M│M│M│M│M│M│M│M│
 F │M│M│M│M│M│M│M│M│M│M│M│M│M│M│M│M│
   └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
```

## Color Derivation

```typescript
// Generate 4-color palette from primary color
export function hexToHSL(hex: string): { h: number; s: number; l: number } {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h = 0, s = 0;
  const l = (max + min) / 2;

  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
      case g: h = ((b - r) / d + 2) / 6; break;
      case b: h = ((r - g) / d + 4) / 6; break;
    }
  }
  return { h: h * 360, s: s * 100, l: l * 100 };
}

export function hslToHex(h: number, s: number, l: number): string {
  s /= 100;
  l /= 100;
  const a = s * Math.min(l, 1 - l);
  const f = (n: number) => {
    const k = (n + h / 30) % 12;
    const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
    return Math.round(255 * color).toString(16).padStart(2, '0');
  };
  return `#${f(0)}${f(8)}${f(4)}`;
}

export function generateSpritePalette(primaryColor: string) {
  const hsl = hexToHSL(primaryColor);
  return {
    base: primaryColor,
    highlight: hslToHex(hsl.h, Math.max(0, hsl.s - 10), Math.min(100, hsl.l + 20)),
    shadow: hslToHex(hsl.h, Math.min(100, hsl.s + 10), Math.max(0, hsl.l - 25)),
    outline: hslToHex(hsl.h, Math.min(100, hsl.s + 5), Math.max(0, hsl.l - 40)),
  };
}

// Example: generateSpritePalette('#00fff5')
// → { base: '#00fff5', highlight: '#66fffa', shadow: '#00b3ac', outline: '#006663' }
```

## Sprite Factory

```typescript
// src/rendering/spriteFactory.ts
import { LostObject } from '../types';
import { CATEGORY_SHAPES } from './categoryShapes';
import { PHYSICAL_SHAPES } from './physicalShapes';

const SPRITE_SIZE = 16;
const SCALE = 4;

export function createSprite(object: LostObject): HTMLCanvasElement {
  const canvas = document.createElement('canvas');
  canvas.width = SPRITE_SIZE;
  canvas.height = SPRITE_SIZE;
  
  const ctx = canvas.getContext('2d')!;
  ctx.imageSmoothingEnabled = false;  // CRITICAL
  
  const palette = generateSpritePalette(object.primaryColor);
  
  // Clear with transparency
  ctx.clearRect(0, 0, SPRITE_SIZE, SPRITE_SIZE);
  
  // Draw based on category
  if (object.category === 'physical' && object.visualShapeId) {
    const drawFn = PHYSICAL_SHAPES[object.visualShapeId];
    if (drawFn) drawFn(ctx, palette);
  } else {
    const drawFn = CATEGORY_SHAPES[object.category];
    drawFn(ctx, palette, object.id);
  }
  
  return canvas;
}

export function createAnimatedSprite(object: LostObject): HTMLCanvasElement[] {
  const frames: HTMLCanvasElement[] = [];
  
  // Frame 1: Normal
  frames.push(createSprite(object));
  
  // Frame 2: Offset Y+1
  const frame2 = createSprite(object);
  const ctx2 = frame2.getContext('2d')!;
  const imageData = ctx2.getImageData(0, 0, SPRITE_SIZE, SPRITE_SIZE);
  ctx2.clearRect(0, 0, SPRITE_SIZE, SPRITE_SIZE);
  ctx2.putImageData(imageData, 0, 1);
  frames.push(frame2);
  
  return frames;
}
```

## Drawing Primitives

```typescript
// src/rendering/primitives.ts

export function drawPixel(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  color: string
) {
  ctx.fillStyle = color;
  ctx.fillRect(Math.floor(x), Math.floor(y), 1, 1);
}

export function drawRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  color: string
) {
  ctx.fillStyle = color;
  ctx.fillRect(Math.floor(x), Math.floor(y), w, h);
}

export function drawOutlinedRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  fillColor: string,
  outlineColor: string
) {
  // Fill
  drawRect(ctx, x, y, w, h, fillColor);
  
  // Outline (1px border)
  ctx.fillStyle = outlineColor;
  // Top
  ctx.fillRect(x, y, w, 1);
  // Bottom
  ctx.fillRect(x, y + h - 1, w, 1);
  // Left
  ctx.fillRect(x, y, 1, h);
  // Right
  ctx.fillRect(x + w - 1, y, 1, h);
}

export function drawCircle(
  ctx: CanvasRenderingContext2D,
  cx: number,
  cy: number,
  r: number,
  color: string
) {
  ctx.fillStyle = color;
  for (let y = -r; y <= r; y++) {
    for (let x = -r; x <= r; x++) {
      if (x * x + y * y <= r * r) {
        ctx.fillRect(Math.floor(cx + x), Math.floor(cy + y), 1, 1);
      }
    }
  }
}

export function drawDithered(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  color1: string,
  color2: string
) {
  for (let py = 0; py < h; py++) {
    for (let px = 0; px < w; px++) {
      const isCheckerboard = (px + py) % 2 === 0;
      ctx.fillStyle = isCheckerboard ? color1 : color2;
      ctx.fillRect(x + px, y + py, 1, 1);
    }
  }
}
```

## Physical Object Shapes

```typescript
// src/rendering/physicalShapes.ts
import { SpritePalette } from '../types';

type DrawFunction = (
  ctx: CanvasRenderingContext2D,
  palette: SpritePalette
) => void;

export const PHYSICAL_SHAPES: Record<string, DrawFunction> = {
  sock: (ctx, { base, highlight, shadow, outline }) => {
    // Sock shape (in 12×12 usable zone, offset by 2)
    const ox = 2, oy = 2;
    
    // Main body
    ctx.fillStyle = base;
    ctx.fillRect(ox + 4, oy + 1, 4, 8);
    ctx.fillRect(ox + 3, oy + 2, 6, 6);
    
    // Foot part
    ctx.fillRect(ox + 1, oy + 7, 8, 3);
    ctx.fillRect(ox + 2, oy + 10, 6, 1);
    
    // Highlight (top)
    ctx.fillStyle = highlight;
    ctx.fillRect(ox + 5, oy + 2, 2, 1);
    
    // Shadow (bottom)
    ctx.fillStyle = shadow;
    ctx.fillRect(ox + 2, oy + 9, 5, 1);
    
    // Outline
    ctx.fillStyle = outline;
    // Top
    ctx.fillRect(ox + 4, oy + 0, 4, 1);
    // Bottom
    ctx.fillRect(ox + 2, oy + 11, 6, 1);
    // Left edge
    ctx.fillRect(ox + 0, oy + 7, 1, 3);
    ctx.fillRect(ox + 1, oy + 10, 1, 1);
    // Right edge
    ctx.fillRect(ox + 9, oy + 7, 1, 3);
    ctx.fillRect(ox + 8, oy + 10, 1, 1);
  },
  
  key: (ctx, { base, highlight, shadow, outline }) => {
    const ox = 2, oy = 2;
    
    // Key head (circle)
    drawCircle(ctx, ox + 4, oy + 3, 2, base);
    drawPixel(ctx, ox + 4, oy + 2, highlight);
    
    // Key shaft
    ctx.fillStyle = base;
    ctx.fillRect(ox + 3, oy + 5, 2, 6);
    
    // Key teeth
    ctx.fillStyle = base;
    ctx.fillRect(ox + 5, oy + 8, 2, 1);
    ctx.fillRect(ox + 5, oy + 10, 2, 1);
    
    // Outline
    ctx.fillStyle = outline;
    ctx.fillRect(ox + 2, oy + 1, 1, 1);
    ctx.fillRect(ox + 6, oy + 1, 1, 1);
  },
  
  // Add more shapes: coin, ring, umbrella, etc.
};
```

## Abstract Category Shapes

```typescript
// src/rendering/categoryShapes.ts
import { seededRandom } from '../utils/random';

export const CATEGORY_SHAPES = {
  memory: (ctx, palette, seed) => {
    // Wavy, cloud-like shape
    const rng = seededRandom(seed);
    const ox = 2, oy = 2;
    
    ctx.fillStyle = palette.base;
    for (let y = 0; y < 12; y++) {
      for (let x = 0; x < 12; x++) {
        const noise = Math.sin(x * 0.5 + rng() * 3) * Math.cos(y * 0.5 + rng() * 3);
        if (noise > -0.3) {
          ctx.fillRect(ox + x, oy + y, 1, 1);
        }
      }
    }
  },
  
  concept: (ctx, palette, seed) => {
    // Geometric, crystalline
    const rng = seededRandom(seed);
    const ox = 2, oy = 2;
    const cx = 6, cy = 6;
    
    // Draw random triangular facets
    ctx.fillStyle = palette.base;
    for (let i = 0; i < 6; i++) {
      const angle = (i / 6) * Math.PI * 2 + rng() * 0.5;
      const r = 3 + rng() * 2;
      const x = Math.floor(cx + Math.cos(angle) * r);
      const y = Math.floor(cy + Math.sin(angle) * r);
      ctx.fillRect(ox + x, oy + y, 2, 2);
    }
    
    // Center
    ctx.fillStyle = palette.highlight;
    ctx.fillRect(ox + 5, oy + 5, 2, 2);
  },
  
  emotion: (ctx, palette, seed) => {
    // Organic blob, pulsing
    const rng = seededRandom(seed);
    const ox = 2, oy = 2;
    const cx = 6, cy = 6;
    
    ctx.fillStyle = palette.base;
    for (let y = 0; y < 12; y++) {
      for (let x = 0; x < 12; x++) {
        const dx = x - cx;
        const dy = y - cy;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const angle = Math.atan2(dy, dx);
        const radius = 4 + Math.sin(angle * 3 + rng() * 2) * 1.5;
        
        if (dist < radius) {
          ctx.fillRect(ox + x, oy + y, 1, 1);
        }
      }
    }
  },
  
  time: (ctx, palette, seed) => {
    // Clock-like, spiraling
    const rng = seededRandom(seed);
    const ox = 2, oy = 2;
    const cx = 6, cy = 6;
    
    // Circle outline
    ctx.fillStyle = palette.outline;
    for (let a = 0; a < Math.PI * 2; a += 0.3) {
      const x = Math.floor(cx + Math.cos(a) * 5);
      const y = Math.floor(cy + Math.sin(a) * 5);
      ctx.fillRect(ox + x, oy + y, 1, 1);
    }
    
    // Hands
    ctx.fillStyle = palette.base;
    const hourAngle = rng() * Math.PI * 2;
    const minAngle = rng() * Math.PI * 2;
    
    // Hour hand
    for (let r = 0; r < 3; r++) {
      const x = Math.floor(cx + Math.cos(hourAngle) * r);
      const y = Math.floor(cy + Math.sin(hourAngle) * r);
      ctx.fillRect(ox + x, oy + y, 1, 1);
    }
    
    // Minute hand
    ctx.fillStyle = palette.highlight;
    for (let r = 0; r < 4; r++) {
      const x = Math.floor(cx + Math.cos(minAngle) * r);
      const y = Math.floor(cy + Math.sin(minAngle) * r);
      ctx.fillRect(ox + x, oy + y, 1, 1);
    }
  },
  
  sound: (ctx, palette, seed) => {
    // Waveform
    const rng = seededRandom(seed);
    const ox = 2, oy = 2;
    
    ctx.fillStyle = palette.base;
    for (let x = 0; x < 12; x++) {
      const amplitude = 2 + rng() * 3;
      const freq = 0.5 + rng() * 0.3;
      const y = Math.floor(6 + Math.sin(x * freq + rng() * 2) * amplitude);
      
      // Draw vertical bar
      const height = Math.floor(amplitude * 0.8);
      for (let dy = -height; dy <= height; dy++) {
        ctx.fillRect(ox + x, oy + y + dy, 1, 1);
      }
    }
  },
  
  unknown: (ctx, palette, seed) => {
    // Glitchy, fragmented
    applyGlitchEffect(ctx, palette, seed);
  },
  
  physical: (ctx, palette, seed) => {
    // Default for physical without specific shape
    const ox = 2, oy = 2;
    drawOutlinedRect(ctx, ox + 2, oy + 2, 8, 8, palette.base, palette.outline);
    ctx.fillStyle = palette.highlight;
    ctx.fillRect(ox + 3, oy + 3, 2, 2);
  },
};
```

## Glitch Effect (Unknown Category)

```typescript
// src/rendering/glitchEffect.ts
export function applyGlitchEffect(
  ctx: CanvasRenderingContext2D,
  palette: SpritePalette,
  seed: string
) {
  const rng = seededRandom(seed);
  const ox = 2, oy = 2;
  
  // Base shape (question mark like)
  ctx.fillStyle = palette.base;
  ctx.fillRect(ox + 4, oy + 2, 4, 2);
  ctx.fillRect(ox + 6, oy + 4, 2, 2);
  ctx.fillRect(ox + 5, oy + 6, 2, 2);
  ctx.fillRect(ox + 5, oy + 9, 2, 2);
  
  // Horizontal glitch lines
  ctx.fillStyle = palette.highlight;
  for (let i = 0; i < 3; i++) {
    const y = Math.floor(rng() * 12);
    const offset = Math.floor(rng() * 4) - 2;
    const width = Math.floor(rng() * 6) + 2;
    
    // Read and shift a horizontal slice
    const imageData = ctx.getImageData(ox, oy + y, 12, 1);
    ctx.putImageData(imageData, ox + offset, oy + y);
  }
  
  // Random noise pixels
  for (let i = 0; i < 5; i++) {
    const x = Math.floor(rng() * 12);
    const y = Math.floor(rng() * 12);
    const colors = [palette.base, palette.highlight, palette.shadow];
    ctx.fillStyle = colors[Math.floor(rng() * colors.length)];
    ctx.fillRect(ox + x, oy + y, 1, 1);
  }
}
```

## Sprite Cache

```typescript
// src/rendering/spriteCache.ts
const cache = new Map<string, HTMLCanvasElement[]>();

export function getCachedSprite(objectId: string): HTMLCanvasElement[] | null {
  return cache.get(objectId) || null;
}

export function cacheSprite(objectId: string, frames: HTMLCanvasElement[]) {
  cache.set(objectId, frames);
}

export function clearCache() {
  cache.clear();
}

export function getOrCreateSprite(object: LostObject): HTMLCanvasElement[] {
  const cached = getCachedSprite(object.id);
  if (cached) return cached;
  
  const frames = createAnimatedSprite(object);
  cacheSprite(object.id, frames);
  return frames;
}
```

## React Sprite Component

```tsx
// src/components/Objects/ObjectSprite.tsx
import { useRef, useEffect, useState } from 'react';
import { LostObject } from '../../types';
import { getOrCreateSprite } from '../../rendering/spriteCache';
import { RARITY_COLORS } from '../../constants/palette';

interface Props {
  object: LostObject;
  size?: number;
  animated?: boolean;
}

export function ObjectSprite({ object, size = 64, animated = true }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [frameIndex, setFrameIndex] = useState(0);
  const framesRef = useRef<HTMLCanvasElement[]>([]);
  
  // Load sprite frames
  useEffect(() => {
    framesRef.current = getOrCreateSprite(object);
  }, [object.id]);
  
  // Animation loop
  useEffect(() => {
    if (!animated || framesRef.current.length <= 1) return;
    
    const interval = setInterval(() => {
      setFrameIndex(i => (i + 1) % framesRef.current.length);
    }, 500); // 500ms per frame
    
    return () => clearInterval(interval);
  }, [animated]);
  
  // Render current frame
  useEffect(() => {
    const canvas = canvasRef.current;
    const frame = framesRef.current[frameIndex];
    if (!canvas || !frame) return;
    
    const ctx = canvas.getContext('2d')!;
    ctx.imageSmoothingEnabled = false;
    ctx.clearRect(0, 0, size, size);
    ctx.drawImage(frame, 0, 0, size, size);
  }, [frameIndex, size]);
  
  const glowColor = RARITY_COLORS[object.rarity];
  const needsGlow = object.rarity !== 'common';
  
  return (
    <canvas
      ref={canvasRef}
      width={size}
      height={size}
      className="sprite"
      style={{
        imageRendering: 'pixelated',
        filter: needsGlow ? `drop-shadow(0 0 4px ${glowColor})` : undefined,
      }}
    />
  );
}
```

## Glow Effects by Rarity

```css
/* Glow keyframes */
@keyframes glow-uncommon {
  0%, 100% { filter: drop-shadow(0 0 2px #39ff14); }
  50% { filter: drop-shadow(0 0 4px #39ff14); }
}

@keyframes glow-rare {
  0%, 100% { filter: drop-shadow(0 0 3px #00fff5); }
  50% { filter: drop-shadow(0 0 6px #00fff5); }
}

@keyframes glow-epic {
  0%, 100% { filter: drop-shadow(0 0 4px #ff6bcb); }
  50% { filter: drop-shadow(0 0 8px #ff6bcb); }
}

@keyframes glow-legendary {
  0%, 100% { 
    filter: drop-shadow(0 0 5px #ffd93d) drop-shadow(0 0 10px #ffd93d); 
  }
  50% { 
    filter: drop-shadow(0 0 8px #ffd93d) drop-shadow(0 0 15px #ffd93d); 
  }
}

.sprite-uncommon { animation: glow-uncommon 2s ease-in-out infinite; }
.sprite-rare { animation: glow-rare 2s ease-in-out infinite; }
.sprite-epic { animation: glow-epic 2s ease-in-out infinite; }
.sprite-legendary { animation: glow-legendary 2s ease-in-out infinite; }
```

## Seeded Random for Consistency

```typescript
// src/utils/random.ts
export function seededRandom(seed: string): () => number {
  let h = 0;
  for (let i = 0; i < seed.length; i++) {
    h = Math.imul(31, h) + seed.charCodeAt(i) | 0;
  }
  
  return () => {
    h = Math.imul(h ^ (h >>> 15), h | 1);
    h ^= h + Math.imul(h ^ (h >>> 7), h | 61);
    return ((h ^ (h >>> 14)) >>> 0) / 4294967296;
  };
}
```
