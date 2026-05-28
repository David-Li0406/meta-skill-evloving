---
name: pixel-art-game-builder
description: >
  Expert skill for building pixel art idle/incremental games with procedural sprite generation,
  React/TypeScript/Zustand architecture, and contemplative game design. Use when creating pixel art games,
  implementing idle game mechanics, generating procedural sprites via Canvas API, building collection-based games,
  or implementing incremental game economies. Triggers on requests for pixel art, idle games, sprite generation,
  incremental games, collection games, or contemplative game experiences.
---

# Pixel Art Game Builder

Expert guide for architecting and building pixel art idle/incremental games with procedural sprite generation.

## Quick Navigation

| Need | Go to |
|------|-------|
| Start a new project | [Quick Start](#quick-start) |
| Copy working code | [templates/](templates/) |
| Understand patterns | [patterns/](patterns/) |
| See full example | [examples/](examples/) |
| Deep reference | [references/](references/) |
| CSS/Tailwind setup | [assets/](assets/) |

## Core Design Philosophy

**Three pillars:** Minimal. Luminous. Contemplative.

- **Constraint = Creativity**: Limited palette (12 colors), low resolution (16×16 sprites)
- **Space speaks**: Dark backgrounds, few elements = immensity feeling
- **Light guides**: Important elements glow (higher rarities shine more)
- **Movement breathes**: Slow, organic animations (minimum 500ms cycles)
- **Zero pressure**: NO timers, NO deadlines, NO FOMO, NO negative messages

## Quick Start

```bash
npm create vite@latest my-idle-game -- --template react-ts
cd my-idle-game
npm install zustand immer
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Then copy files from [assets/](assets/) for CSS and Tailwind config.

## Critical Implementation Rules

### Pixel Art Sprites (16×16)

```javascript
// MANDATORY for pixel-perfect rendering
ctx.imageSmoothingEnabled = false;
```

```css
/* CSS for any sprite element */
.sprite { image-rendering: pixelated; }
```

- **4 colors max per sprite**: base, highlight, shadow, outline
- **12×12 usable zone** (2px margin for glow effects)
- **Scale 4×** when displaying (16×16 → 64×64)
- **NO antialiasing, NO gradients**

### Color Palette (12 colors only)

```typescript
const PALETTE = {
  deepBlack: '#0a0a0f',      // Main background
  spaceGray: '#1a1a2e',      // Panels
  borderGray: '#2d2d44',     // Borders
  neonCyan: '#00fff5',       // Primary actions, RARE
  softMagenta: '#ff6bcb',    // Notifications, EPIC
  cosmicGold: '#ffd93d',     // Rewards, LEGENDARY
  validGreen: '#39ff14',     // Success, UNCOMMON
  alertRed: '#ff4757',       // Alerts (rare use)
  mysteryPurple: '#6c5ce7',  // Hidden/secret
  mainWhite: '#e8e8e8',      // Body text, COMMON
  secondaryGray: '#a0a0a0',  // Disabled
  interactiveCyan: '#7fefef' // Links
};

const RARITY_COLORS = {
  common: PALETTE.secondaryGray,
  uncommon: PALETTE.validGreen,
  rare: PALETTE.neonCyan,
  epic: PALETTE.softMagenta,
  legendary: PALETTE.cosmicGold,
};
```

### Game Loop Pattern (100ms tick)

```typescript
useEffect(() => {
  const interval = setInterval(() => {
    const now = Date.now();
    const delta = (now - lastTick) / 1000;

    // Update resources
    addCredits(incomePerSecond * delta);
    regenerateEnergy(delta);

    setLastTick(now);
  }, 100);
  return () => clearInterval(interval);
}, [incomePerSecond, lastTick]);
```

### State Management (Zustand + Immer)

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

const useGameStore = create<GameState>()(
  persist(
    immer((set, get) => ({
      credits: 0,
      energy: 100,
      addCredits: (amount) => set((s) => { s.credits += amount }),
    })),
    { name: 'game-save' }
  )
);
```

## Templates (Copy & Use)

Ready-to-use code in [templates/](templates/):

| Template | Description |
|----------|-------------|
| `game-loop.tsx` | Hook for 100ms game tick with delta time |
| `save-system.ts` | Zustand persist pattern with migration |
| `progression.ts` | Scaling formulas (exponential costs, diminishing returns) |
| `sprite-renderer.tsx` | Canvas component with pixel-perfect rendering |

## Patterns (Understand & Adapt)

Conceptual guides in [patterns/](patterns/):

| Pattern | Description |
|---------|-------------|
| `resource-system.md` | Structure currencies, caps, regeneration |
| `upgrade-tree.md` | Linear upgrades, skill trees, prestige unlocks |
| `prestige-loop.md` | Reset mechanics, meta-progression, permanent bonuses |
| `procedural-sprites.md` | Generate varied sprites from seeds |

## Examples

Working code in [examples/](examples/):

| Example | Description |
|---------|-------------|
| `minimal-idle-game.tsx` | Complete ~150 line idle game with resources, upgrades, save |

## Deep References

Detailed documentation in [references/](references/):

| Reference | When to use |
|-----------|-------------|
| `architecture.md` | Full project structure, types, stores |
| `sprite-system.md` | Canvas API, color derivation, caching |
| `game-mechanics.md` | Economy, scanning, progression formulas |
| `ui-patterns.md` | Components, layouts, animations |
| `content-structure.md` | Data structure for items, sectors, upgrades |

## Design Pillars (Non-Negotiable)

1. **Immediate Clarity**: Every button has text label, max 3 actions visible
2. **Progressive Depth**: New content unlocks over time
3. **Emotional Collection**: Every item has narrative description ≤140 chars
4. **Zero Pressure**: NO timers, NO deadlines, NO FOMO
5. **Mobile First**: Touch targets ≥44px, breakpoints 320/768/1024px

## Writing Style

- **Voice**: Calm, melancholic, subtle humor
- **Rules**: ≤140 chars, NO "!", NO CAPS, NO imperatives

**Templates:**
- Funny: "[Object]. [Absurd observation]. [Punchline]."
- Tender: "[Object]. [Human detail]. [Universal truth]."
- Weird: "[Object]. [Strange property]. [Acceptance]."

## Performance Targets

| Metric | Target |
|--------|--------|
| Bundle size | <200KB gzipped |
| FPS idle | ≥30 |
| Memory | <100MB |

## DO's and DON'Ts

**DO ✓**
- Pixel-perfect rendering (`imageSmoothingEnabled = false`)
- 4-color sprites maximum
- 12-color palette only
- ≥44px touch targets
- Cache generated sprites
- Support reduced-motion

**DON'T ✗**
- Antialiasing on sprites
- Gradients in pixel art
- Icon-only buttons
- Stats in item descriptions
- Timers or countdowns
- Negative failure messages
- Nested modals
