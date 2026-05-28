# Prestige Loop Pattern

How to implement reset mechanics and meta-progression for long-term engagement.

## Core Concept

Prestige (also called "rebirth", "ascension", "new game+") is a mechanic where players reset their progress in exchange for permanent bonuses. This creates a satisfying loop of accelerating progress.

## Why Prestige Works

1. **Renewed Goals**: Fresh start with new challenges
2. **Faster Progress**: Each run is quicker than the last
3. **Meaningful Choice**: When to prestige is a strategic decision
4. **Long-term Engagement**: Extends gameplay exponentially

## Basic Prestige Formula

```typescript
/**
 * Calculate prestige currency earned
 *
 * Common formula: sqrt(totalEarned / threshold)
 * - Low threshold = more prestige points, faster meta-progression
 * - High threshold = fewer points, longer runs
 */
function calculatePrestigePoints(totalCreditsEarned: number, threshold: number): number {
  if (totalCreditsEarned < threshold) return 0;
  return Math.floor(Math.sqrt(totalCreditsEarned / threshold));
}

// Examples:
// 10,000 credits, threshold 1000 → 3 prestige points
// 100,000 credits, threshold 1000 → 10 prestige points
// 1,000,000 credits, threshold 1000 → 31 prestige points
```

## Prestige Multiplier

```typescript
/**
 * Convert prestige points to bonus
 *
 * @param points - Total prestige points accumulated
 * @param bonusPerPoint - Bonus per point (0.1 = +10% per point)
 */
function calculatePrestigeMultiplier(points: number, bonusPerPoint: number = 0.1): number {
  return 1 + (points * bonusPerPoint);
}

// Examples:
// 10 points × 0.1 = 2.0× multiplier (100% bonus)
// 50 points × 0.1 = 6.0× multiplier (500% bonus)
// 100 points × 0.1 = 11.0× multiplier (1000% bonus)
```

## What Resets vs. What Persists

### Resets (Temporary Progress)

- Primary currency (credits)
- Owned items / collection
- Regular upgrades
- Play time (for this run)
- Energy (resets to max)

### Persists (Permanent Progress)

- Prestige currency
- Prestige upgrades
- Total prestige count
- Achievements
- Cosmetics
- Lifetime statistics

```typescript
interface PrestigeState {
  // Persists
  prestigePoints: number;
  totalPrestiges: number;
  prestigeUpgrades: Record<string, number>;
  lifetimeStats: {
    totalCreditsEarned: number;
    totalItemsCollected: number;
    totalPlayTime: number;
  };
}

interface RunState {
  // Resets
  credits: number;
  creditsThisRun: number;
  ownedItems: string[];
  upgrades: Record<string, number>;
  playTimeThisRun: number;
}
```

## Prestige Timing Strategy

### When Should Players Prestige?

Create a decision point, not an obvious answer:

```typescript
interface PrestigeInfo {
  currentPoints: number;        // Points earned this run
  pendingPoints: number;        // Points if prestiged now
  totalAfterPrestige: number;   // Total points after prestige
  currentMultiplier: number;    // Current bonus
  nextMultiplier: number;       // Bonus after prestige
  recommendation: string;       // UI hint
}

function getPrestigeInfo(state: GameState): PrestigeInfo {
  const pending = calculatePrestigePoints(state.creditsThisRun, THRESHOLD);
  const total = state.prestigePoints + pending;

  const currentMult = calculatePrestigeMultiplier(state.prestigePoints);
  const nextMult = calculatePrestigeMultiplier(total);
  const improvement = ((nextMult / currentMult) - 1) * 100;

  let recommendation = '';
  if (pending === 0) {
    recommendation = 'Keep playing to earn prestige points';
  } else if (improvement < 10) {
    recommendation = 'Small gain. Continue for bigger bonus?';
  } else if (improvement < 50) {
    recommendation = 'Decent gain. Good time to prestige.';
  } else {
    recommendation = 'Major gain! Prestige recommended.';
  }

  return {
    currentPoints: state.prestigePoints,
    pendingPoints: pending,
    totalAfterPrestige: total,
    currentMultiplier: currentMult,
    nextMultiplier: nextMult,
    recommendation,
  };
}
```

## Prestige Upgrades

Special upgrades bought with prestige currency:

```typescript
interface PrestigeUpgrade {
  id: string;
  name: string;
  description: string;
  cost: number;            // Prestige points
  maxLevel: number;
  effect: PrestigeEffect;
}

type PrestigeEffect =
  | { type: 'income_multiplier'; value: number }
  | { type: 'start_with_credits'; value: number }
  | { type: 'start_with_upgrade'; upgradeId: string }
  | { type: 'permanent_item'; itemId: string }
  | { type: 'energy_bonus'; value: number };

const PRESTIGE_UPGRADES: PrestigeUpgrade[] = [
  {
    id: 'head_start',
    name: 'Head Start',
    description: 'Start each run with bonus credits',
    cost: 5,
    maxLevel: 10,
    effect: { type: 'start_with_credits', value: 1000 },
  },
  {
    id: 'eternal_income',
    name: 'Eternal Income',
    description: '+25% income per level (permanent)',
    cost: 10,
    maxLevel: 5,
    effect: { type: 'income_multiplier', value: 0.25 },
  },
];
```

## Multiple Prestige Layers

For very long games, add layers of prestige:

```
Layer 1: Prestige (resets run progress)
  ↓ Earns: Prestige Points
  ↓ Buys: Prestige Upgrades

Layer 2: Ascension (resets prestige progress)
  ↓ Earns: Ascension Tokens
  ↓ Buys: Ascension Powers

Layer 3: Transcendence (resets everything)
  ↓ Earns: Transcendence Essence
  ↓ Buys: Permanent Multipliers
```

```typescript
interface MetaProgression {
  // Layer 1
  prestigePoints: number;
  prestigeUpgrades: Record<string, number>;
  totalPrestiges: number;

  // Layer 2
  ascensionTokens: number;
  ascensionPowers: Record<string, number>;
  totalAscensions: number;

  // Layer 3 (if needed)
  transcendenceEssence: number;
}
```

## UI Patterns

### Prestige Button

```tsx
function PrestigeButton() {
  const info = usePrestigeInfo();

  return (
    <div className="prestige-panel">
      <h3>Prestige</h3>
      <p>Pending: +{info.pendingPoints} points</p>
      <p>
        Multiplier: {info.currentMultiplier.toFixed(1)}×
        → {info.nextMultiplier.toFixed(1)}×
      </p>
      <p className="hint">{info.recommendation}</p>
      <button
        disabled={info.pendingPoints === 0}
        onClick={prestige}
      >
        Prestige Now
      </button>
    </div>
  );
}
```

### Confirmation Modal

Always confirm prestige actions:

```tsx
function PrestigeConfirmModal({ onConfirm, onCancel }) {
  return (
    <Modal>
      <h2>Prestige?</h2>
      <p>You will lose:</p>
      <ul>
        <li>All credits</li>
        <li>All items</li>
        <li>All upgrades</li>
      </ul>
      <p>You will gain:</p>
      <ul>
        <li>+{pendingPoints} prestige points</li>
        <li>{newMultiplier}× income multiplier</li>
      </ul>
      <button onClick={onCancel}>Cancel</button>
      <button onClick={onConfirm}>Confirm Prestige</button>
    </Modal>
  );
}
```

## Anti-Patterns

### ❌ Prestige Too Early

If players can meaningfully prestige in 5 minutes, it feels like a chore. Aim for 1-2 hours minimum for first prestige.

### ❌ Prestige Required Too Late

If players play 20 hours before first prestige, they'll quit. Balance the threshold.

### ❌ No Meaningful Choice

If there's always a "correct" time to prestige, it's not interesting. Create trade-offs.

### ❌ Lost Progress Feels Bad

Make sure the bonus is worth the reset. Show players exactly what they're gaining.

## Balancing Tips

1. **First Prestige**: Should happen around 2-4 hours of play
2. **Subsequent Prestiges**: Each should be faster than the last
3. **Point Threshold**: Adjust so players earn 1-5 points first prestige
4. **Bonus Per Point**: 5-10% per point is a good starting range
5. **Test The Loop**: Play through multiple prestiges yourself
