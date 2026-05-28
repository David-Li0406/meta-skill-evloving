# Casino & Card Game Implementation Reference

## Seeded Random Number Generation

```typescript
class SeededRNG {
  constructor(private seed: number = Date.now()) {}
  
  next(): number {
    let t = this.seed += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  }
  
  nextInt(min: number, max: number): number {
    return Math.floor(this.next() * (max - min + 1)) + min;
  }
  
  shuffle<T>(array: T[]): T[] {
    const result = [...array];
    for (let i = result.length - 1; i > 0; i--) {
      const j = this.nextInt(0, i);
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  }
}
```

## Deck Management

```typescript
class Deck {
  private cards: Card[] = [];
  private discardPile: Card[] = [];
  
  constructor(private rng: SeededRNG) { this.reset(); }
  
  reset(): void {
    this.cards = [];
    const suits = ['hearts', 'diamonds', 'clubs', 'spades'] as const;
    for (const suit of suits) {
      for (let rank = 1; rank <= 13; rank++) {
        this.cards.push({ suit, rank });
      }
    }
    this.cards = this.rng.shuffle(this.cards);
  }
  
  draw(count = 1): Card[] {
    if (this.cards.length < count) {
      this.cards = [...this.cards, ...this.rng.shuffle(this.discardPile)];
      this.discardPile = [];
    }
    return this.cards.splice(0, count);
  }
}
```

## Poker Hand Evaluation

```typescript
type HandRank = 'high-card' | 'pair' | 'two-pair' | 'three-of-a-kind' | 
               'straight' | 'flush' | 'full-house' | 'four-of-a-kind' |
               'straight-flush' | 'royal-flush';

function evaluatePokerHand(cards: Card[]): { rank: HandRank; value: number } {
  const sorted = [...cards].sort((a, b) => b.rank - a.rank);
  const isFlush = cards.every(c => c.suit === cards[0].suit);
  const ranks = sorted.map(c => c.rank);
  
  const isStraight = ranks.every((r, i) => i === 0 || ranks[i-1] - r === 1);
  const groups = groupByRank(sorted);
  const counts = groups.map(g => g.length).sort((a, b) => b - a);
  
  if (isFlush && isStraight && ranks[0] === 13) return { rank: 'royal-flush', value: 1000 };
  if (isFlush && isStraight) return { rank: 'straight-flush', value: 900 };
  if (counts[0] === 4) return { rank: 'four-of-a-kind', value: 800 };
  if (counts[0] === 3 && counts[1] === 2) return { rank: 'full-house', value: 700 };
  if (isFlush) return { rank: 'flush', value: 600 };
  if (isStraight) return { rank: 'straight', value: 500 };
  if (counts[0] === 3) return { rank: 'three-of-a-kind', value: 400 };
  if (counts[0] === 2 && counts[1] === 2) return { rank: 'two-pair', value: 300 };
  if (counts[0] === 2) return { rank: 'pair', value: 200 };
  return { rank: 'high-card', value: 100 };
}
```

## Betting System

```typescript
type BetType = 'fold' | 'call' | 'raise' | 'all-in';

interface Pot {
  id: string;
  currentFill: number;
  thresholds: number[];
  payoutMultipliers: Record<BetType, number[]>;
}

function resolveBet(bet: { potId: string; betType: BetType; amount: number }, pot: Pot) {
  if (bet.betType === 'fold') return { won: false, payout: 0 };
  
  const thresholdIndex = pot.thresholds.findIndex((t, i) => 
    pot.currentFill >= t && (i === pot.thresholds.length - 1 || pot.currentFill < pot.thresholds[i + 1])
  );
  
  if (thresholdIndex < 0) return { won: false, payout: 0 };
  
  const multiplier = pot.payoutMultipliers[bet.betType][thresholdIndex];
  return { won: true, payout: Math.floor(bet.amount * multiplier) };
}
```

## Video Poker Paytable

```typescript
const JACKS_OR_BETTER_PAYTABLE: Record<string, number[]> = {
  'royal-flush':      [250, 500, 750, 1000, 4000],
  'straight-flush':   [50, 100, 150, 200, 250],
  'four-of-a-kind':   [25, 50, 75, 100, 125],
  'full-house':       [9, 18, 27, 36, 45],
  'flush':            [6, 12, 18, 24, 30],
  'straight':         [4, 8, 12, 16, 20],
  'three-of-a-kind':  [3, 6, 9, 12, 15],
  'two-pair':         [2, 4, 6, 8, 10],
  'jacks-or-better':  [1, 2, 3, 4, 5],
};
```

---

*Casino Implementation Reference - Game Engineering Team*
