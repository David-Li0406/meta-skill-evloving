# Upgrade Tree Pattern

How to design upgrades, skill trees, and permanent progression.

## Core Concept

Upgrades provide permanent progression and give players goals to work toward. Good upgrade design creates meaningful choices.

## Upgrade Types

### 1. Linear Upgrades (Most Common)

Multiple levels of the same effect:

```typescript
interface LinearUpgrade {
  id: string;
  name: string;
  baseCost: number;
  costMultiplier: number;  // 1.5 = 50% more per level
  maxLevel: number;
  effectPerLevel: number;
}

// Example: Income Boost
// Level 0: base
// Level 1: +10% income (cost: 100)
// Level 2: +20% income (cost: 150)
// Level 3: +30% income (cost: 225)
```

### 2. One-Time Purchases

Unique unlocks that happen once:

```typescript
interface OneTimeUpgrade {
  id: string;
  name: string;
  cost: number;
  effect: string;
  unlockCondition?: UnlockCondition;
}

// Example: Auto-Clicker
// Cost: 10000
// Effect: Automatically clicks once per second
```

### 3. Tiered Unlocks

Upgrades that unlock better versions:

```typescript
interface TieredUpgrade {
  id: string;
  tiers: Array<{
    level: number;
    name: string;
    cost: number;
    effect: string;
  }>;
}

// Example: Scanner
// Tier 1: Basic Scanner (scans 1 item)
// Tier 2: Bulk Scanner (scans 2 items)
// Tier 3: Triple Scanner (scans 3 items)
```

## Cost Formulas

### Exponential (Standard)

```typescript
// Most common for idle games
// Creates satisfying progression curve
function exponentialCost(baseCost: number, level: number, multiplier: number = 1.5): number {
  return Math.floor(baseCost * Math.pow(multiplier, level));
}

// Level 0: 100
// Level 1: 150
// Level 5: 759
// Level 10: 5766
```

### Polynomial (Aggressive)

```typescript
// Faster scaling, good for late-game upgrades
function polynomialCost(baseCost: number, level: number, exponent: number = 2): number {
  return Math.floor(baseCost * Math.pow(level + 1, exponent));
}

// Level 0: 100
// Level 1: 400
// Level 5: 3600
// Level 10: 12100
```

### Linear (Gentle)

```typescript
// Predictable, good for early-game
function linearCost(baseCost: number, level: number, increment: number): number {
  return baseCost + (increment * level);
}

// Level 0: 100
// Level 1: 150
// Level 5: 350
// Level 10: 600
```

## Upgrade Categories

Organize upgrades into logical groups:

```typescript
type UpgradeCategory =
  | 'income'    // Increase earning rate
  | 'energy'    // Energy capacity/regen
  | 'scan'      // Scanning efficiency
  | 'rarity'    // Better drop rates
  | 'offline'   // Offline earnings
  | 'special';  // Unique mechanics
```

### Category Examples

```typescript
const UPGRADES: Record<UpgradeCategory, Upgrade[]> = {
  income: [
    { id: 'basic_amp', name: 'Basic Amplifier', effectPerLevel: 0.1, maxLevel: 10 },
    { id: 'master_amp', name: 'Master Amplifier', effectPerLevel: 0.5, maxLevel: 1 },
  ],
  energy: [
    { id: 'quick_charge', name: 'Quick Charger', effectPerLevel: 0.2, maxLevel: 5 },
    { id: 'energy_cell', name: 'Energy Cell', effectPerLevel: 50, maxLevel: 8 },
  ],
  rarity: [
    { id: 'lucky_scan', name: 'Lucky Scanner', effectPerLevel: 0.05, maxLevel: 5 },
    { id: 'rare_detect', name: 'Rare Detector', effectPerLevel: 0.03, maxLevel: 5 },
  ],
};
```

## Unlock Conditions

Gate upgrades behind progression:

```typescript
type UnlockCondition =
  | { type: 'none' }
  | { type: 'level'; upgradeId: string; level: number }
  | { type: 'items_owned'; count: number }
  | { type: 'credits_earned'; amount: number }
  | { type: 'upgrade_purchased'; upgradeId: string };

function isUpgradeUnlocked(upgrade: Upgrade, state: GameState): boolean {
  const condition = upgrade.unlockCondition;
  if (!condition || condition.type === 'none') return true;

  switch (condition.type) {
    case 'level':
      return (state.upgrades[condition.upgradeId] || 0) >= condition.level;
    case 'items_owned':
      return state.ownedItems.length >= condition.count;
    case 'credits_earned':
      return state.totalCreditsEarned >= condition.amount;
    default:
      return true;
  }
}
```

## Skill Tree Pattern

For complex progression with branches:

```typescript
interface SkillNode {
  id: string;
  name: string;
  description: string;
  cost: number;
  requires: string[];  // IDs of prerequisite nodes
  effect: Effect;
}

// Validate tree connectivity
function canPurchase(nodeId: string, purchasedNodes: Set<string>, tree: SkillNode[]): boolean {
  const node = tree.find(n => n.id === nodeId);
  if (!node) return false;
  if (purchasedNodes.has(nodeId)) return false;

  return node.requires.every(reqId => purchasedNodes.has(reqId));
}
```

## Effect Application

### Multiplicative Stacking

```typescript
// Recommended: Predictable, easy to balance
function calculateTotalMultiplier(state: GameState): number {
  let multiplier = 1.0;

  // Each upgrade multiplies
  multiplier *= 1 + (state.upgrades.basic_amp || 0) * 0.1;  // +10% per level
  multiplier *= 1 + (state.upgrades.master_amp || 0) * 0.5; // +50% if purchased

  return multiplier;
}
```

### Additive Then Multiplicative

```typescript
// More complex, allows fine-tuning
function calculateIncome(state: GameState): number {
  // Base from owned items
  let base = state.ownedItems.reduce((sum, item) => sum + item.baseIncome, 0);

  // Additive bonuses first
  const additiveBonus = calculateAdditiveBonus(state);
  base += additiveBonus;

  // Then multiplicative
  const multiplier = calculateMultiplier(state);
  return base * multiplier;
}
```

## UI Best Practices

### Show Current and Next

```typescript
interface UpgradeDisplay {
  name: string;
  currentLevel: number;
  maxLevel: number;
  currentEffect: string;   // "Currently: +30% income"
  nextEffect: string;      // "Next: +40% income"
  cost: number;
  canAfford: boolean;
  isMaxed: boolean;
}
```

### Buy Multiple

```typescript
// Allow buying multiple levels at once
function buyMaxLevels(upgradeId: string, state: GameState): number {
  const upgrade = getUpgrade(upgradeId);
  const currentLevel = state.upgrades[upgradeId] || 0;
  let credits = state.credits;
  let levelsBought = 0;

  while (currentLevel + levelsBought < upgrade.maxLevel) {
    const cost = calculateCost(upgrade, currentLevel + levelsBought);
    if (credits < cost) break;
    credits -= cost;
    levelsBought++;
  }

  return levelsBought;
}
```

## Anti-Patterns

### ❌ Useless Upgrades

Every upgrade should feel impactful. If +1% doesn't feel meaningful, make it +5%.

### ❌ Mandatory Path

If one upgrade is always the "correct" choice, remove the other options.

### ❌ Dead Ends

Always provide something new to work toward. If players max everything, add prestige.

### ❌ Unclear Effects

"Improves efficiency" → "Increases income by 10% per level"
