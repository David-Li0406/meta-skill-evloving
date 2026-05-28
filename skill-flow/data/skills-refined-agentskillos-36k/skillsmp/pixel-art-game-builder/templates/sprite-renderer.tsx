/**
 * Sprite Renderer Component
 *
 * Canvas-based component for rendering pixel-perfect sprites.
 * Supports procedural generation from seeds for consistent sprites.
 *
 * Usage:
 *   <SpriteRenderer
 *     size={64}
 *     primaryColor="#00fff5"
 *     seed="item-001"
 *     animated={true}
 *   />
 */

import { useRef, useEffect, useState, useMemo } from 'react';

// ============================================
// TYPES
// ============================================

interface SpriteRendererProps {
  /** Display size in pixels (will be rendered at 16x16 and scaled) */
  size?: number;
  /** Primary color for the sprite (hex) */
  primaryColor: string;
  /** Optional secondary color (hex) */
  secondaryColor?: string;
  /** Seed for procedural generation (same seed = same sprite) */
  seed: string;
  /** Shape type for the sprite */
  shape?: 'blob' | 'crystal' | 'orb' | 'wave' | 'default';
  /** Enable floating animation */
  animated?: boolean;
  /** CSS class for glow effects */
  glowClass?: string;
  /** Click handler */
  onClick?: () => void;
}

interface SpritePalette {
  base: string;
  highlight: string;
  shadow: string;
  outline: string;
}

// ============================================
// CONSTANTS
// ============================================

const SPRITE_SIZE = 16;
const USABLE_OFFSET = 2; // 2px margin for glow
const USABLE_SIZE = 12; // 12x12 usable area

// ============================================
// COLOR UTILITIES
// ============================================

function hexToHSL(hex: string): { h: number; s: number; l: number } {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;

  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h = 0;
  let s = 0;
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

function hslToHex(h: number, s: number, l: number): string {
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

function generatePalette(primaryColor: string): SpritePalette {
  const hsl = hexToHSL(primaryColor);
  return {
    base: primaryColor,
    highlight: hslToHex(hsl.h, Math.max(0, hsl.s - 10), Math.min(100, hsl.l + 20)),
    shadow: hslToHex(hsl.h, Math.min(100, hsl.s + 10), Math.max(0, hsl.l - 25)),
    outline: hslToHex(hsl.h, Math.min(100, hsl.s + 5), Math.max(0, hsl.l - 40)),
  };
}

// ============================================
// SEEDED RANDOM
// ============================================

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

// ============================================
// DRAWING FUNCTIONS
// ============================================

function drawPixel(ctx: CanvasRenderingContext2D, x: number, y: number, color: string) {
  ctx.fillStyle = color;
  ctx.fillRect(Math.floor(x), Math.floor(y), 1, 1);
}

function drawBlob(ctx: CanvasRenderingContext2D, palette: SpritePalette, rng: () => number) {
  const ox = USABLE_OFFSET;
  const oy = USABLE_OFFSET;
  const cx = USABLE_SIZE / 2;
  const cy = USABLE_SIZE / 2;

  // Draw organic blob shape
  for (let y = 0; y < USABLE_SIZE; y++) {
    for (let x = 0; x < USABLE_SIZE; x++) {
      const dx = x - cx;
      const dy = y - cy;
      const dist = Math.sqrt(dx * dx + dy * dy);
      const angle = Math.atan2(dy, dx);
      const radius = 4 + Math.sin(angle * 3 + rng() * 2) * 1.5;

      if (dist < radius - 0.5) {
        drawPixel(ctx, ox + x, oy + y, palette.base);
      } else if (dist < radius) {
        drawPixel(ctx, ox + x, oy + y, palette.outline);
      }
    }
  }

  // Add highlight
  ctx.fillStyle = palette.highlight;
  ctx.fillRect(ox + 4, oy + 3, 2, 2);
}

function drawCrystal(ctx: CanvasRenderingContext2D, palette: SpritePalette, rng: () => number) {
  const ox = USABLE_OFFSET;
  const oy = USABLE_OFFSET;
  const cx = USABLE_SIZE / 2;
  const cy = USABLE_SIZE / 2;

  // Draw geometric facets
  ctx.fillStyle = palette.base;
  for (let i = 0; i < 6; i++) {
    const angle = (i / 6) * Math.PI * 2 + rng() * 0.5;
    const r = 3 + rng() * 2;
    const x = Math.floor(cx + Math.cos(angle) * r);
    const y = Math.floor(cy + Math.sin(angle) * r);
    ctx.fillRect(ox + x, oy + y, 2, 2);
  }

  // Center highlight
  ctx.fillStyle = palette.highlight;
  ctx.fillRect(ox + 5, oy + 5, 2, 2);

  // Outline
  ctx.fillStyle = palette.outline;
  ctx.fillRect(ox + 4, oy + 2, 4, 1);
  ctx.fillRect(ox + 4, oy + 9, 4, 1);
}

function drawOrb(ctx: CanvasRenderingContext2D, palette: SpritePalette, _rng: () => number) {
  const ox = USABLE_OFFSET;
  const oy = USABLE_OFFSET;
  const cx = USABLE_SIZE / 2;
  const cy = USABLE_SIZE / 2;
  const radius = 5;

  // Draw filled circle
  for (let y = -radius; y <= radius; y++) {
    for (let x = -radius; x <= radius; x++) {
      const dist = Math.sqrt(x * x + y * y);
      if (dist <= radius) {
        const color = dist <= radius - 1.5 ? palette.base : palette.outline;
        drawPixel(ctx, ox + cx + x, oy + cy + y, color);
      }
    }
  }

  // Highlight
  ctx.fillStyle = palette.highlight;
  ctx.fillRect(ox + 4, oy + 3, 2, 2);

  // Shadow
  ctx.fillStyle = palette.shadow;
  ctx.fillRect(ox + 7, oy + 8, 2, 1);
}

function drawWave(ctx: CanvasRenderingContext2D, palette: SpritePalette, rng: () => number) {
  const ox = USABLE_OFFSET;
  const oy = USABLE_OFFSET;

  // Draw waveform
  ctx.fillStyle = palette.base;
  for (let x = 0; x < USABLE_SIZE; x++) {
    const amplitude = 2 + rng() * 3;
    const freq = 0.5 + rng() * 0.3;
    const y = Math.floor(6 + Math.sin(x * freq + rng() * 2) * amplitude);
    const height = Math.floor(amplitude * 0.8);

    for (let dy = -height; dy <= height; dy++) {
      if (oy + y + dy >= USABLE_OFFSET && oy + y + dy < SPRITE_SIZE - USABLE_OFFSET) {
        drawPixel(ctx, ox + x, oy + y + dy, palette.base);
      }
    }
  }
}

function drawDefault(ctx: CanvasRenderingContext2D, palette: SpritePalette, _rng: () => number) {
  const ox = USABLE_OFFSET;
  const oy = USABLE_OFFSET;

  // Simple square with details
  ctx.fillStyle = palette.base;
  ctx.fillRect(ox + 2, oy + 2, 8, 8);

  // Highlight corner
  ctx.fillStyle = palette.highlight;
  ctx.fillRect(ox + 3, oy + 3, 2, 2);

  // Outline
  ctx.fillStyle = palette.outline;
  ctx.fillRect(ox + 2, oy + 2, 8, 1);
  ctx.fillRect(ox + 2, oy + 9, 8, 1);
  ctx.fillRect(ox + 2, oy + 2, 1, 8);
  ctx.fillRect(ox + 9, oy + 2, 1, 8);
}

const SHAPE_DRAWERS: Record<string, typeof drawDefault> = {
  blob: drawBlob,
  crystal: drawCrystal,
  orb: drawOrb,
  wave: drawWave,
  default: drawDefault,
};

// ============================================
// SPRITE GENERATION
// ============================================

function generateSprite(
  primaryColor: string,
  seed: string,
  shape: string = 'default'
): HTMLCanvasElement {
  const canvas = document.createElement('canvas');
  canvas.width = SPRITE_SIZE;
  canvas.height = SPRITE_SIZE;

  const ctx = canvas.getContext('2d')!;
  ctx.imageSmoothingEnabled = false; // CRITICAL for pixel art

  const palette = generatePalette(primaryColor);
  const rng = seededRandom(seed);
  const drawFn = SHAPE_DRAWERS[shape] || SHAPE_DRAWERS.default;

  ctx.clearRect(0, 0, SPRITE_SIZE, SPRITE_SIZE);
  drawFn(ctx, palette, rng);

  return canvas;
}

// ============================================
// CACHE
// ============================================

const spriteCache = new Map<string, HTMLCanvasElement>();

function getCacheKey(primaryColor: string, seed: string, shape: string): string {
  return `${primaryColor}-${seed}-${shape}`;
}

function getCachedSprite(
  primaryColor: string,
  seed: string,
  shape: string
): HTMLCanvasElement {
  const key = getCacheKey(primaryColor, seed, shape);

  if (!spriteCache.has(key)) {
    spriteCache.set(key, generateSprite(primaryColor, seed, shape));
  }

  return spriteCache.get(key)!;
}

// ============================================
// COMPONENT
// ============================================

export function SpriteRenderer({
  size = 64,
  primaryColor,
  seed,
  shape = 'default',
  animated = false,
  glowClass = '',
  onClick,
}: SpriteRendererProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [offsetY, setOffsetY] = useState(0);

  // Get cached sprite
  const sprite = useMemo(
    () => getCachedSprite(primaryColor, seed, shape),
    [primaryColor, seed, shape]
  );

  // Animation loop for floating effect
  useEffect(() => {
    if (!animated) {
      setOffsetY(0);
      return;
    }

    let frame = 0;
    const interval = setInterval(() => {
      frame = (frame + 1) % 40; // 40 frames = 2 second cycle at 50ms
      const newOffset = Math.sin((frame / 40) * Math.PI * 2) * 2;
      setOffsetY(newOffset);
    }, 50);

    return () => clearInterval(interval);
  }, [animated]);

  // Render sprite to canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d')!;
    ctx.imageSmoothingEnabled = false; // CRITICAL

    ctx.clearRect(0, 0, size, size);
    ctx.drawImage(sprite, 0, Math.round(offsetY * (size / SPRITE_SIZE)), size, size);
  }, [sprite, size, offsetY]);

  return (
    <canvas
      ref={canvasRef}
      width={size}
      height={size}
      className={`sprite ${glowClass}`}
      style={{
        imageRendering: 'pixelated',
        cursor: onClick ? 'pointer' : undefined,
      }}
      onClick={onClick}
      aria-label={`Sprite ${seed}`}
    />
  );
}

// ============================================
// UTILITY: Clear cache (for memory management)
// ============================================

export function clearSpriteCache() {
  spriteCache.clear();
}

// ============================================
// UTILITY: Preload sprites
// ============================================

export function preloadSprites(
  items: Array<{ primaryColor: string; seed: string; shape?: string }>
) {
  items.forEach(({ primaryColor, seed, shape = 'default' }) => {
    getCachedSprite(primaryColor, seed, shape);
  });
}
