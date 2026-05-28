# Architecture Reference

Complete technical architecture for pixel art idle games.

## Project Structure

```
project-name/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
│
├── public/
│   ├── favicon.ico
│   └── manifest.json
│
└── src/
    ├── main.tsx                    # Entry point
    ├── App.tsx                     # Root component
    ├── index.css                   # Tailwind + global styles
    │
    ├── types/                      # TypeScript interfaces
    │   ├── index.ts
    │   ├── objects.ts              # LostObject, Category, Rarity
    │   ├── game.ts                 # GameState, GameConfig
    │   ├── sectors.ts              # Sector
    │   ├── upgrades.ts             # Upgrade
    │   ├── employees.ts            # Employee
    │   └── narrative.ts            # Ending, Fragment
    │
    ├── data/                       # Static game data
    │   ├── index.ts
    │   ├── objects.ts              # All collectible objects
    │   ├── sectors.ts              # Game sectors/zones
    │   ├── upgrades.ts             # Purchasable upgrades
    │   ├── employees.ts            # Hireable employees
    │   └── config.ts               # Game constants
    │
    ├── stores/                     # Zustand stores
    │   ├── index.ts
    │   ├── gameStore.ts            # Main game state
    │   ├── uiStore.ts              # UI state (modals, tabs)
    │   └── settingsStore.ts        # User settings
    │
    ├── services/                   # Business logic (pure functions)
    │   ├── index.ts
    │   ├── gameEngine.ts           # Core calculations
    │   ├── saveManager.ts          # Persistence
    │   ├── scanService.ts          # Object selection
    │   ├── incomeService.ts        # Revenue calculations
    │   ├── progressionService.ts   # Unlock logic
    │   └── narrativeService.ts     # Endings & fragments
    │
    ├── hooks/                      # Custom React hooks
    │   ├── index.ts
    │   ├── useGameLoop.ts          # Main tick loop
    │   ├── useOfflineProgress.ts   # Offline earnings
    │   ├── useAutoSave.ts          # Auto-save interval
    │   └── useSpriteRenderer.ts    # Canvas sprite generation
    │
    ├── components/
    │   ├── Layout/
    │   │   ├── Header.tsx          # Credits, energy display
    │   │   ├── TabBar.tsx          # Bottom navigation
    │   │   └── MainContent.tsx     # Tab content container
    │   │
    │   ├── Tabs/
    │   │   ├── ScanTab.tsx
    │   │   ├── CollectionTab.tsx
    │   │   ├── UpgradesTab.tsx
    │   │   ├── SectorsTab.tsx
    │   │   └── EmployeesTab.tsx
    │   │
    │   ├── Objects/
    │   │   ├── ObjectCard.tsx
    │   │   ├── ObjectModal.tsx
    │   │   ├── ObjectSprite.tsx
    │   │   └── ObjectGrid.tsx
    │   │
    │   ├── UI/
    │   │   ├── Button.tsx
    │   │   ├── Modal.tsx
    │   │   ├── ProgressBar.tsx
    │   │   ├── ResourceDisplay.tsx
    │   │   ├── Toast.tsx
    │   │   └── Tooltip.tsx
    │   │
    │   └── Modals/
    │       ├── DiscoveryModal.tsx
    │       ├── ReturnModal.tsx
    │       ├── EndingModal.tsx
    │       └── OfflineModal.tsx
    │
    ├── rendering/                  # Sprite generation
    │   ├── spriteFactory.ts
    │   ├── spriteCache.ts
    │   ├── colorUtils.ts
    │   ├── primitives.ts
    │   ├── physicalShapes.ts
    │   ├── abstractShapes.ts
    │   └── particles.ts
    │
    ├── utils/
    │   ├── index.ts
    │   ├── format.ts               # Number formatting
    │   ├── random.ts               # Seeded random
    │   ├── time.ts                 # Time calculations
    │   └── color.ts                # HSL utilities
    │
    └── constants/
        ├── index.ts
        ├── palette.ts              # 12 colors
        └── timing.ts               # Animation durations
```

## Core TypeScript Interfaces

### LostObject (Collectible Item)

```typescript
type Category = 'physical' | 'memory' | 'concept' | 'emotion' | 'time' | 'sound' | 'unknown';
type Rarity = 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary';
type Emotion = 'funny' | 'tender' | 'weird' | 'melancholic' | 'profound';

interface LostObject {
  id: string;                    // "physical_001"
  name: string;                  // Max 30 chars
  description: string;           // Max 140 chars
  
  category: Category;
  rarity: Rarity;
  emotion: Emotion;
  sectorId: string;
  
  baseIncome: number;            // Credits/sec
  scanCost: number;              // Energy cost
  catalogCost: number;           // Credits cost
  
  canReturn: boolean;
  ownerHint?: string;
  returnReward?: number;
  
  isFragment: boolean;
  fragmentOrder?: number;        // 1-5
  
  // Visual
  visualShapeId?: string;        // For physical objects
  primaryColor: string;          // Hex
  secondaryColor?: string;
}
```

### GameState

```typescript
interface GameState {
  // Resources
  credits: number;
  energy: number;
  maxEnergy: number;
  
  // Objects
  discoveredObjectIds: string[];
  cataloguedObjectIds: string[];
  returnedObjectIds: string[];
  pendingCatalogIds: string[];
  
  // Progression
  unlockedSectorIds: string[];
  currentSectorId: string;
  purchasedUpgrades: Record<string, number>;  // upgradeId → level
  hiredEmployeeIds: string[];
  
  // Narrative
  keepScore: number;
  returnScore: number;
  foundFragmentIds: string[];
  isPhase5Active: boolean;
  endingReached: 'A' | 'B' | 'C' | null;
  
  // Meta
  playTimeSeconds: number;
  totalCreditsEarned: number;
  lastSaveTimestamp: string;
  saveVersion: number;
  
  // Settings
  autoScanEnabled: boolean;
  soundEnabled: boolean;
}
```

### Sector

```typescript
interface Sector {
  id: string;
  name: string;
  description: string;
  
  unlockCost: number;
  unlockCondition: {
    type: 'sector_completion' | 'objects_catalogued';
    targetId?: string;
    percentage?: number;
    count?: number;
  };
  
  baseScanCost: number;
  rarityDistribution: Record<Rarity, number>;  // Weights
  categoryDistribution: Record<Category, number>;
  
  ambientColor: string;
  starDensity: number;
}
```

### Upgrade

```typescript
interface Upgrade {
  id: string;
  name: string;
  description: string;
  
  category: 'income' | 'energy' | 'scan' | 'employee' | 'offline' | 'special';
  
  baseCost: number;
  costMultiplier: number;        // 1.5 per level
  maxLevel: number;
  
  effect: {
    type: string;                // "income_multiplier", "energy_regen", etc.
    value: number;               // Per level
    isPercentage: boolean;
  };
  
  unlockCondition?: {
    type: 'objects_catalogued' | 'upgrade_purchased';
    value: number | string;
  };
}
```

## Zustand Store Pattern

```typescript
// src/stores/gameStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface GameActions {
  // Resources
  addCredits: (amount: number) => void;
  spendCredits: (amount: number) => boolean;
  addEnergy: (amount: number) => void;
  spendEnergy: (amount: number) => boolean;
  
  // Objects
  discoverObject: (objectId: string) => void;
  catalogObject: (objectId: string) => void;
  returnObject: (objectId: string) => void;
  
  // Progression
  unlockSector: (sectorId: string) => void;
  purchaseUpgrade: (upgradeId: string) => void;
  hireEmployee: (employeeId: string) => void;
  
  // Game loop
  tick: (deltaSeconds: number) => void;
  
  // Save
  resetGame: () => void;
  loadSave: (save: GameState) => void;
}

const INITIAL_STATE: GameState = {
  credits: 0,
  energy: 100,
  maxEnergy: 100,
  discoveredObjectIds: [],
  cataloguedObjectIds: [],
  returnedObjectIds: [],
  pendingCatalogIds: [],
  unlockedSectorIds: ['sector_01'],
  currentSectorId: 'sector_01',
  purchasedUpgrades: {},
  hiredEmployeeIds: [],
  keepScore: 0,
  returnScore: 0,
  foundFragmentIds: [],
  isPhase5Active: false,
  endingReached: null,
  playTimeSeconds: 0,
  totalCreditsEarned: 0,
  lastSaveTimestamp: new Date().toISOString(),
  saveVersion: 1,
  autoScanEnabled: false,
  soundEnabled: true,
};

export const useGameStore = create<GameState & GameActions>()(
  persist(
    immer((set, get) => ({
      ...INITIAL_STATE,
      
      addCredits: (amount) => set((state) => {
        state.credits += amount;
        state.totalCreditsEarned += amount;
      }),
      
      spendCredits: (amount) => {
        const state = get();
        if (state.credits < amount) return false;
        set((s) => { s.credits -= amount; });
        return true;
      },
      
      tick: (deltaSeconds) => set((state) => {
        state.playTimeSeconds += deltaSeconds;
        // Income calculation happens in useGameLoop hook
      }),
      
      // ... other actions
    })),
    {
      name: 'game-save',
      version: 1,
    }
  )
);
```

## Service Pattern

Services are pure functions with no side effects:

```typescript
// src/services/incomeService.ts
import { GameState } from '../types';
import { getObjectById } from '../data/objects';
import { getUpgradeById } from '../data/upgrades';

export function calculateTotalIncome(state: GameState): number {
  return state.cataloguedObjectIds.reduce((total, objectId) => {
    const object = getObjectById(objectId);
    if (!object) return total;
    return total + calculateObjectIncome(state, object);
  }, 0);
}

export function calculateObjectIncome(state: GameState, object: LostObject): number {
  let income = object.baseIncome;
  
  // Apply upgrade multipliers
  income *= getUpgradeMultiplier(state);
  
  // Apply employee bonuses
  income *= getEmployeeMultiplier(state, object.category);
  
  // Apply sector mastery bonus
  income *= getSectorMasteryBonus(state, object.sectorId);
  
  // Apply collection milestone
  income *= getCollectionMilestoneMultiplier(state);
  
  return income;
}

function getUpgradeMultiplier(state: GameState): number {
  let multiplier = 1.0;
  
  const basicAmp = state.purchasedUpgrades['basic_amplifier'] || 0;
  multiplier *= 1 + (basicAmp * 0.1);  // +10% per level
  
  // ... other upgrades
  
  return multiplier;
}
```

## Hook Pattern

```typescript
// src/hooks/useGameLoop.ts
import { useEffect, useRef } from 'react';
import { useGameStore } from '../stores/gameStore';
import { calculateTotalIncome } from '../services/incomeService';

export function useGameLoop() {
  const lastTickRef = useRef(Date.now());
  const { addCredits, addEnergy, tick } = useGameStore();
  const state = useGameStore();
  
  useEffect(() => {
    const TICK_INTERVAL = 100; // 10 updates per second
    
    const interval = setInterval(() => {
      const now = Date.now();
      const deltaMs = now - lastTickRef.current;
      const deltaSeconds = deltaMs / 1000;
      
      // Update game time
      tick(deltaSeconds);
      
      // Calculate and add income
      const income = calculateTotalIncome(state);
      addCredits(income * deltaSeconds);
      
      // Regenerate energy
      const energyRegen = calculateEnergyRegen(state);
      addEnergy(energyRegen * deltaSeconds);
      
      lastTickRef.current = now;
    }, TICK_INTERVAL);
    
    return () => clearInterval(interval);
  }, [state, addCredits, addEnergy, tick]);
}
```

## Configuration Files

### vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    target: 'es2020',
    minify: 'terser',
    sourcemap: false,
  },
  server: {
    port: 3000,
  },
});
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noEmit": true,
    "isolatedModules": true,
    "skipLibCheck": true,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "exclude": ["node_modules"]
}
```

## Implementation Order

1. **Foundation** (Days 1-3): Setup, types, constants, stores
2. **Data** (Days 4-5): Static data for sectors, upgrades, employees, objects
3. **Services** (Days 6-8): Income, scanning, progression logic
4. **Game Loop** (Days 9-10): Hooks for ticks, offline, auto-save
5. **UI Base** (Days 11-14): Core components, layout, scan tab
6. **UI Complete** (Days 15-18): All tabs, modals
7. **Sprites** (Days 19-21): Procedural generation, effects
8. **Narrative** (Days 22-24): Endings, fragments
9. **Polish** (Days 25-28): Performance, mobile, accessibility
10. **Launch** (Days 29-30): Build, deploy, monitoring
