# Reward & Progression Systems Reference

## Currency System

```typescript
interface Currency {
  id: string;
  displayName: string;
  maxValue: number;
  regenerates: boolean;
  regenerationRate?: number; // Per hour
}

class CurrencyManager {
  private balances = new Map<string, number>();
  
  getBalance(id: string): number {
    return this.balances.get(id) || 0;
  }
  
  add(id: string, amount: number, max: number): boolean {
    const current = this.getBalance(id);
    this.balances.set(id, Math.min(current + amount, max));
    return true;
  }
  
  spend(id: string, amount: number): boolean {
    if (this.getBalance(id) < amount) return false;
    this.balances.set(id, this.getBalance(id) - amount);
    return true;
  }
}
```

## Experience Curves

```typescript
const XP_CURVES = {
  linear: (level: number, base: number) => base * level,
  polynomial: (level: number, base: number, power: number) => 
    Math.floor(base * Math.pow(level, power)),
  exponential: (level: number, base: number, rate: number) => 
    Math.floor(base * Math.pow(rate, level)),
};

// Simulin bonding: gentle polynomial curve
const simulinXP = (level: number) => XP_CURVES.polynomial(level, 100, 1.5);
```

## Combo Hand System

```typescript
type TriggerType = 'first_bloom' | 'perfect_read' | 'trouble_slayer' | 'growth_spurt' | 'simulin_sync';
type ComboHandType = 'pair' | 'two_pair' | 'three_of_a_kind' | 'straight' | 
                     'full_house' | 'flush' | 'four_of_a_kind' | 'straight_flush' | 'royal_flush';

const HAND_MULTIPLIERS: Record<ComboHandType, number> = {
  'pair': 2, 'two_pair': 3, 'three_of_a_kind': 5, 'straight': 10,
  'full_house': 15, 'flush': 20, 'four_of_a_kind': 25, 'straight_flush': 50, 'royal_flush': 100,
};

function evaluateComboHand(triggers: { type: TriggerType }[]): ComboHandType | null {
  const counts = new Map<TriggerType, number>();
  triggers.forEach(t => counts.set(t.type, (counts.get(t.type) || 0) + 1));
  
  const values = [...counts.values()].sort((a, b) => b - a);
  
  if (values[0] >= 4) return 'four_of_a_kind';
  if (values[0] >= 3 && values[1] >= 2) return 'full_house';
  if (values[0] >= 3) return 'three_of_a_kind';
  if (values[0] >= 2 && values[1] >= 2) return 'two_pair';
  if (values[0] >= 2) return 'pair';
  return null;
}
```

## Achievement System

```typescript
interface Achievement {
  id: string;
  name: string;
  tiers?: { threshold: number; rewards: Reward[] }[];
  rewards: Reward[];
}

class AchievementTracker {
  private progress = new Map<string, number>();
  private earned = new Set<string>();
  
  increment(id: string, amount = 1): Achievement | null {
    const current = (this.progress.get(id) || 0) + amount;
    this.progress.set(id, current);
    // Check if achievement unlocked
    return null;
  }
}
```

## Loot Tables

```typescript
class LootTable<T> {
  constructor(
    private entries: { item: T; weight: number; guaranteedAfter?: number }[],
    private rng: SeededRNG
  ) {}
  
  pull(): T {
    const totalWeight = this.entries.reduce((sum, e) => sum + e.weight, 0);
    let random = this.rng.next() * totalWeight;
    
    for (const entry of this.entries) {
      random -= entry.weight;
      if (random <= 0) return entry.item;
    }
    return this.entries[this.entries.length - 1].item;
  }
}
```

---

*Reward & Progression Reference - Game Engineering Team*
