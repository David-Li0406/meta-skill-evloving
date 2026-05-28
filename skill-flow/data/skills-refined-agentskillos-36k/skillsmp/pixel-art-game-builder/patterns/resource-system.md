# Resource System Pattern

How to structure currencies, caps, and regeneration in idle games.

## Core Concept

Resources are the backbone of idle games. Most games have 2-4 main resources with different purposes.

## Common Resource Archetypes

### Primary Currency (Credits/Gold/Coins)

- **Purpose**: Main spending currency
- **Cap**: Usually unlimited
- **Sources**: Passive income, active clicking, selling items
- **Uses**: Buying upgrades, unlocking content

```typescript
interface PrimaryCurrency {
  value: number;        // No cap
  totalEarned: number;  // Lifetime total (for milestones)
}
```

### Energy/Stamina

- **Purpose**: Gate active actions (prevent infinite clicking)
- **Cap**: Fixed, can be upgraded
- **Regeneration**: Time-based (e.g., 1 per 10 seconds)
- **Uses**: Actions like scanning, crafting, exploring

```typescript
interface Energy {
  current: number;
  max: number;
  regenRate: number;  // Per second
}
```

### Premium Currency (Gems/Crystals)

- **Purpose**: Special purchases, time skips
- **Cap**: Usually unlimited
- **Sources**: Achievements, rare drops, (monetization)
- **Uses**: Instant energy, rare items, cosmetics

### Special Tokens

- **Purpose**: Specific game mechanics
- **Examples**: Prestige points, event tokens, faction reputation

## Resource Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│                    TIME (Passive)                    │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│                     INCOME                           │
│   (owned items × multipliers × bonuses)             │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│                    CREDITS                           │
└─────────────────┬───────────────────────────────────┘
                  │
        ┌─────────┼─────────┬─────────┐
        ▼         ▼         ▼         ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
   │ UPGRADES│ │  ITEMS  │ │ SECTORS │ │EMPLOYEES│
   └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

## Design Patterns

### Pattern 1: Balanced Duo

Two resources that balance each other:

```typescript
// Energy gates actions
// Credits enable permanent progress

function scan() {
  if (energy < scanCost) return; // Can't spam
  spendEnergy(scanCost);
  const item = generateItem();
  // Later: spend credits to catalog
}
```

### Pattern 2: Multi-Currency Economy

Different currencies for different progression paths:

```typescript
// Credits: standard progress
// Gems: premium/convenience
// Prestige Points: meta-progression

interface GameResources {
  credits: number;
  gems: number;
  prestigePoints: number;
  prestigeMultiplier: number;
}
```

### Pattern 3: Regenerating + Capped

Energy-like resources with smart regeneration:

```typescript
function regenerateEnergy(deltaSeconds: number, state: GameState) {
  const regen = state.baseRegen * state.regenMultiplier;
  const newEnergy = Math.min(
    state.energy + regen * deltaSeconds,
    state.maxEnergy
  );
  return newEnergy;
}
```

## Implementation Tips

### 1. Always Store Lifetime Totals

```typescript
interface Credits {
  current: number;
  totalEarned: number;  // For achievements, milestones
  totalSpent: number;   // For analytics
}
```

### 2. Use Multipliers, Not Additions

```typescript
// ❌ Bad: Hard to balance
totalIncome = baseIncome + bonus1 + bonus2 + bonus3;

// ✓ Good: Predictable scaling
totalIncome = baseIncome * multiplier1 * multiplier2;
```

### 3. Cap Verification

```typescript
function addEnergy(amount: number, state: GameState): GameState {
  return {
    ...state,
    energy: Math.min(state.energy + amount, state.maxEnergy),
  };
}

function spendEnergy(amount: number, state: GameState): GameState | null {
  if (state.energy < amount) return null; // Transaction failed
  return {
    ...state,
    energy: state.energy - amount,
  };
}
```

### 4. Display Format

```typescript
// Different formats for different resources
formatCredits(123456);  // "123.5K" - abbreviated
formatEnergy(45, 100);  // "45/100" - with cap
formatTime(3661);       // "1h 1m" - duration
```

## Anti-Patterns to Avoid

### ❌ Too Many Resources

- Players get confused with 5+ currencies
- Stick to 2-4 main resources

### ❌ Unspendable Accumulation

- If a resource only goes up, it feels meaningless
- Every resource needs meaningful sinks

### ❌ Hard Walls

- "You need exactly 1000 gems" with no way to earn 1
- Always provide multiple paths

### ❌ Negative Resources

- Never go below 0
- Always validate before spending

## TypeScript Types

```typescript
interface Resource {
  current: number;
  max?: number;         // Optional cap
  regenRate?: number;   // Per second, if regenerating
}

interface GameResources {
  credits: Resource;
  energy: Resource;
  gems?: Resource;
}

type ResourceAction =
  | { type: 'ADD'; resource: keyof GameResources; amount: number }
  | { type: 'SPEND'; resource: keyof GameResources; amount: number }
  | { type: 'SET_MAX'; resource: keyof GameResources; max: number };
```
