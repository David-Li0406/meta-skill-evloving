# Flyweight Examples (TypeScript)

## Example 1: TextStyle flyweight with many tokens

```ts
type Style = Readonly<{ font: string; weight: number; color: string }>;

type StyleKey = string;

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
const base = factory.get({ font: "Inter", weight: 400, color: "#333" });
const tokens: Token[] = Array.from({ length: 3 }).map((_, i) => ({
  text: `t${i}`,
  x: i * 10,
  y: 0,
  style: base,
}));

console.log(tokens.map((t) => t.style === base));
```

## Example 2: ParticleType flyweight with extrinsic state

```ts
type ParticleTypeData = Readonly<{ sprite: string; size: number; color: string }>;

class ParticleType {
  constructor(public readonly data: ParticleTypeData) {}
  render(x: number, y: number): string {
    return `${this.data.sprite}@${x},${y}`;
  }
}

class ParticleTypeFactory {
  private pool = new Map<string, ParticleType>();

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
const smoke = factory.get({ sprite: "smoke", size: 8, color: "gray" });

const p: Particle = { type: smoke, x: 10, y: 20, vx: 1, vy: -1 };
console.log(p.type.render(p.x, p.y));
```

## Flyweight vs cache vs Singleton (tiny sketches)

```ts
// Flyweight: shared intrinsic state + extrinsic context
class Glyph { constructor(public readonly font: string) {} }
class GlyphFactory { private pool = new Map<string, Glyph>(); get(font: string) { return this.pool.get(font) ?? (this.pool.set(font, new Glyph(font)), this.pool.get(font)!); } }

// Cache: store full results/objects
const cache = new Map<string, unknown>();

// Singleton: one instance total
class Registry { private static instance: Registry = new Registry(); static getInstance() { return Registry.instance; } }
```
