# Procedural Sprites Pattern

How to generate varied pixel art sprites programmatically using seeds.

## Core Concept

Instead of creating hundreds of individual sprites, generate them procedurally from a seed value. Same seed = same sprite, always.

## Benefits

- **Consistency**: Item "sword-001" always looks the same
- **Variety**: Unlimited visual variations
- **Memory Efficient**: Generate on-demand, cache results
- **No Asset Files**: Pure code generation

## Seeded Random

The foundation of procedural generation:

```typescript
/**
 * Create a seeded random number generator
 * Same seed always produces same sequence
 */
function seededRandom(seed: string): () => number {
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

// Usage
const rng = seededRandom('item-sword-001');
rng(); // 0.7234... (always same for this seed)
rng(); // 0.1892... (always same sequence)
```

## Color Derivation

Generate a 4-color palette from one primary color:

```typescript
interface SpritePalette {
  base: string;       // Primary color
  highlight: string;  // Lighter (L+20%)
  shadow: string;     // Darker (L-25%)
  outline: string;    // Darkest (L-40%)
}

function generatePalette(primaryHex: string): SpritePalette {
  const hsl = hexToHSL(primaryHex);

  return {
    base: primaryHex,
    highlight: hslToHex(hsl.h, hsl.s - 10, Math.min(100, hsl.l + 20)),
    shadow: hslToHex(hsl.h, hsl.s + 10, Math.max(0, hsl.l - 25)),
    outline: hslToHex(hsl.h, hsl.s + 5, Math.max(0, hsl.l - 40)),
  };
}
```

## Shape Generation Strategies

### Strategy 1: Blob (Organic)

Good for: memories, emotions, abstract concepts

```typescript
function drawBlob(ctx: CanvasRenderingContext2D, palette: SpritePalette, rng: () => number) {
  const cx = 8, cy = 8; // Center

  for (let y = 0; y < 16; y++) {
    for (let x = 0; x < 16; x++) {
      const dx = x - cx;
      const dy = y - cy;
      const dist = Math.sqrt(dx * dx + dy * dy);
      const angle = Math.atan2(dy, dx);

      // Vary radius based on angle and randomness
      const radius = 4 + Math.sin(angle * 3 + rng() * 2) * 1.5;

      if (dist < radius) {
        ctx.fillStyle = dist < radius - 1 ? palette.base : palette.outline;
        ctx.fillRect(x, y, 1, 1);
      }
    }
  }

  // Add highlight
  ctx.fillStyle = palette.highlight;
  ctx.fillRect(6, 5, 2, 2);
}
```

### Strategy 2: Crystal (Geometric)

Good for: concepts, ideas, rare items

```typescript
function drawCrystal(ctx: CanvasRenderingContext2D, palette: SpritePalette, rng: () => number) {
  const cx = 8, cy = 8;

  // Draw random facets
  ctx.fillStyle = palette.base;
  for (let i = 0; i < 6; i++) {
    const angle = (i / 6) * Math.PI * 2 + rng() * 0.5;
    const r = 3 + rng() * 2;
    const x = Math.floor(cx + Math.cos(angle) * r);
    const y = Math.floor(cy + Math.sin(angle) * r);
    ctx.fillRect(x, y, 2, 2);
  }

  // Center highlight
  ctx.fillStyle = palette.highlight;
  ctx.fillRect(7, 7, 2, 2);
}
```

### Strategy 3: Waveform (Sound)

Good for: sounds, music, audio items

```typescript
function drawWaveform(ctx: CanvasRenderingContext2D, palette: SpritePalette, rng: () => number) {
  ctx.fillStyle = palette.base;

  for (let x = 2; x < 14; x++) {
    const amplitude = 2 + rng() * 3;
    const freq = 0.5 + rng() * 0.3;
    const y = Math.floor(8 + Math.sin(x * freq + rng() * 2) * amplitude);
    const height = Math.floor(amplitude * 0.8);

    // Draw vertical bar
    for (let dy = -height; dy <= height; dy++) {
      if (y + dy >= 2 && y + dy < 14) {
        ctx.fillRect(x, y + dy, 1, 1);
      }
    }
  }
}
```

### Strategy 4: Clock (Time)

Good for: time-related items, temporal concepts

```typescript
function drawClock(ctx: CanvasRenderingContext2D, palette: SpritePalette, rng: () => number) {
  const cx = 8, cy = 8;

  // Circle outline
  ctx.fillStyle = palette.outline;
  for (let a = 0; a < Math.PI * 2; a += 0.3) {
    const x = Math.floor(cx + Math.cos(a) * 5);
    const y = Math.floor(cy + Math.sin(a) * 5);
    ctx.fillRect(x, y, 1, 1);
  }

  // Hour hand
  const hourAngle = rng() * Math.PI * 2;
  ctx.fillStyle = palette.base;
  for (let r = 0; r < 3; r++) {
    const x = Math.floor(cx + Math.cos(hourAngle) * r);
    const y = Math.floor(cy + Math.sin(hourAngle) * r);
    ctx.fillRect(x, y, 1, 1);
  }

  // Minute hand
  const minAngle = rng() * Math.PI * 2;
  ctx.fillStyle = palette.highlight;
  for (let r = 0; r < 4; r++) {
    const x = Math.floor(cx + Math.cos(minAngle) * r);
    const y = Math.floor(cy + Math.sin(minAngle) * r);
    ctx.fillRect(x, y, 1, 1);
  }
}
```

## Shape Selection by Category

```typescript
type Category = 'physical' | 'memory' | 'concept' | 'emotion' | 'time' | 'sound' | 'unknown';

const CATEGORY_SHAPES: Record<Category, DrawFunction> = {
  physical: drawPhysicalShape,  // Recognizable objects
  memory: drawBlob,             // Soft, cloud-like
  concept: drawCrystal,         // Geometric, sharp
  emotion: drawBlob,            // Organic, pulsing
  time: drawClock,              // Circular, hands
  sound: drawWaveform,          // Sound waves
  unknown: drawGlitch,          // Fragmented, noisy
};

function generateSprite(item: Item): HTMLCanvasElement {
  const canvas = document.createElement('canvas');
  canvas.width = 16;
  canvas.height = 16;

  const ctx = canvas.getContext('2d')!;
  ctx.imageSmoothingEnabled = false;

  const palette = generatePalette(item.primaryColor);
  const rng = seededRandom(item.id);
  const drawFn = CATEGORY_SHAPES[item.category];

  drawFn(ctx, palette, rng);

  return canvas;
}
```

## Physical Object Templates

For recognizable objects, use templates:

```typescript
interface SpriteTemplate {
  pixels: Array<{ x: number; y: number; color: 'base' | 'highlight' | 'shadow' | 'outline' }>;
}

const TEMPLATES: Record<string, SpriteTemplate> = {
  sock: {
    pixels: [
      // Body
      { x: 6, y: 3, color: 'base' }, { x: 7, y: 3, color: 'base' },
      { x: 5, y: 4, color: 'base' }, { x: 6, y: 4, color: 'base' },
      // ... more pixels
      // Highlight
      { x: 7, y: 4, color: 'highlight' },
      // Shadow
      { x: 4, y: 11, color: 'shadow' },
    ],
  },
  key: { /* ... */ },
  coin: { /* ... */ },
};

function drawTemplate(
  ctx: CanvasRenderingContext2D,
  template: SpriteTemplate,
  palette: SpritePalette
) {
  template.pixels.forEach(({ x, y, color }) => {
    ctx.fillStyle = palette[color];
    ctx.fillRect(x, y, 1, 1);
  });
}
```

## Caching Strategy

Don't regenerate sprites constantly:

```typescript
const spriteCache = new Map<string, HTMLCanvasElement>();

function getSprite(item: Item): HTMLCanvasElement {
  const cacheKey = `${item.id}-${item.primaryColor}`;

  if (!spriteCache.has(cacheKey)) {
    spriteCache.set(cacheKey, generateSprite(item));
  }

  return spriteCache.get(cacheKey)!;
}

// Clear cache when memory is a concern
function clearSpriteCache() {
  spriteCache.clear();
}
```

## Rendering Best Practices

### Always Disable Smoothing

```typescript
// On canvas context
ctx.imageSmoothingEnabled = false;

// In CSS
.sprite {
  image-rendering: pixelated;
  image-rendering: crisp-edges; /* Firefox */
}
```

### Scale Integer Multiples

```typescript
// Good: 16 × 4 = 64
const displaySize = SPRITE_SIZE * 4;

// Bad: 16 × 3.5 = 56 (blurry)
```

### Use 12×12 Usable Area

Leave 2px margin for glow effects:

```
  0 1 2 3 4 5 6 7 8 9 A B C D E F
0 M M M M M M M M M M M M M M M M
1 M M M M M M M M M M M M M M M M
2 M M . . . . . . . . . . . . M M
3 M M . . . . . . . . . . . . M M
  ...  (12×12 usable zone)  ...
D M M . . . . . . . . . . . . M M
E M M M M M M M M M M M M M M M M
F M M M M M M M M M M M M M M M M
```

## Animation

Simple 2-frame animation:

```typescript
function createAnimatedSprite(item: Item): HTMLCanvasElement[] {
  const frame1 = generateSprite(item);

  // Frame 2: shift content down by 1px
  const frame2 = document.createElement('canvas');
  frame2.width = 16;
  frame2.height = 16;
  const ctx2 = frame2.getContext('2d')!;
  ctx2.imageSmoothingEnabled = false;
  ctx2.drawImage(frame1, 0, 1);

  return [frame1, frame2];
}
```

## Glow Effects by Rarity

```css
.sprite-common { /* No glow */ }

.sprite-uncommon {
  animation: glow-uncommon 2s ease-in-out infinite;
}

@keyframes glow-uncommon {
  0%, 100% { filter: drop-shadow(0 0 2px #39ff14); }
  50% { filter: drop-shadow(0 0 4px #39ff14); }
}

.sprite-rare {
  animation: glow-rare 2s ease-in-out infinite;
}

.sprite-legendary {
  animation: glow-legendary 2s ease-in-out infinite;
}

@keyframes glow-legendary {
  0%, 100% {
    filter: drop-shadow(0 0 5px #ffd93d) drop-shadow(0 0 10px #ffd93d);
  }
  50% {
    filter: drop-shadow(0 0 8px #ffd93d) drop-shadow(0 0 15px #ffd93d);
  }
}
```
