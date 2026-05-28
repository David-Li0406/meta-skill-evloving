---
name: flyweight-pattern-typescript
description: TypeScript guidance for Flyweight with intrinsic/extrinsic split, immutable flyweights, Map-based factory/pool, and RAM-vs-CPU trade-offs.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Flyweight (TypeScript)

## Intent

Reduce memory use by sharing immutable intrinsic state across many objects while passing extrinsic context separately.

## When to use

- Measured memory pressure is a bottleneck (heap/metrics show it).
- Many similar objects share duplicated immutable data.
- You can separate intrinsic vs extrinsic state cleanly.
- You can pass per-instance context into methods instead of storing it.
- Large collections are long-lived and memory-heavy.
- You can tolerate a factory/pool lookup per use.
- You need to de-duplicate shared state for performance.

## When NOT to use

- You have no profiling evidence (premature optimization).
- Shared state is mutable or frequently changing.
- Key space is unbounded and would leak memory.
- CPU overhead of pooling outweighs RAM savings.
- Object counts are small.
- Deep copy ambiguity makes sharing unsafe.
- You can’t define a stable intrinsic key.

## Mental model

Intrinsic = shared and immutable; Extrinsic = context passed in.

## Recommended TS shapes

- Immutable flyweight class/value object.
- FlyweightFactory using Map keyed by intrinsic state.
- Context stored externally (lightweight structs/arrays).

## Example 1: TextStyle flyweight (tokens)

```ts
type StyleKey = string;

type Style = Readonly<{ font: string; weight: number; color: string }>;

class TextStyle {
  constructor(public readonly style: Style) {}
}

class TextStyleFactory {
  private pool = new Map<StyleKey, TextStyle>();

  get(style: Style): TextStyle {
    const key = `${style.font}|${style.weight}|${style.color}`;
    const existing = this.pool.get(key);
    if (existing) return existing;
    const created = new TextStyle(Object.freeze(style));
    this.pool.set(key, created);
    return created;
  }
}

type Token = { text: string; x: number; y: number; style: TextStyle };

const factory = new TextStyleFactory();
const style = factory.get({ font: "Inter", weight: 400, color: "#333" });
const tokens: Token[] = [
  { text: "Hello", x: 0, y: 0, style },
  { text: "World", x: 60, y: 0, style },
];
```

## Example 2: ParticleType flyweight

```ts
type ParticleTypeKey = string;

type ParticleTypeData = Readonly<{ sprite: string; size: number; color: string }>;

class ParticleType {
  constructor(public readonly data: ParticleTypeData) {}
  render(x: number, y: number): string {
    return `${this.data.sprite}@${x},${y}`;
  }
}

class ParticleTypeFactory {
  private pool = new Map<ParticleTypeKey, ParticleType>();

  get(data: ParticleTypeData): ParticleType {
    const key = `${data.sprite}|${data.size}|${data.color}`;
    const existing = this.pool.get(key);
    if (existing) return existing;
    const created = new ParticleType(Object.freeze(data));
    this.pool.set(key, created);
    return created;
  }
}

type Particle = { type: ParticleType; x: number; y: number; vx: number; vy: number };

const factory = new ParticleTypeFactory();
const smokeType = factory.get({ sprite: "smoke", size: 8, color: "gray" });
const particle: Particle = { type: smokeType, x: 10, y: 20, vx: 1, vy: -1 };
```

## Testing strategy (pragmatic)

- Assert same key returns the same instance.
- Validate immutability of intrinsic state.
- Test behavior with different extrinsic inputs.

## Common pitfalls

- Mutable intrinsic state shared across instances.
- Bad keying causing accidental collisions.
- Pool leaks due to unbounded key space.
- Premature optimization without profiling.
- Mixing extrinsic state into the flyweight.
- Overengineering factory logic.
- Hiding identity differences when they matter.
- Skipping tests for reuse/immutability.

## Checklist for refactors

- Measure memory pressure first.
- Identify intrinsic duplicates and extrinsic context.
- Define a stable intrinsic key.
- Ensure flyweights are immutable.
- Pass extrinsic data explicitly.
- Add pool bounds/eviction if keys can grow.
- Test for reuse and correctness.
- Document trade-offs and usage constraints.

## Output expectations

When invoked, produce:
- Intrinsic/extrinsic split and keys.
- Factory/pool design with bounds if needed.
- Tests for reuse and immutability.
