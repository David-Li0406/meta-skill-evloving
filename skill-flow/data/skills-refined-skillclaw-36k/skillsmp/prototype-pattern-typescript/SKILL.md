---
name: prototype-pattern-typescript
description: TypeScript guidance and examples for Prototype: cloning without coupling, explicit clone semantics, presets/registries, and pitfalls like deep copy ambiguity, circular refs, and external resources.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Prototype (TypeScript)

## Intent

Create new objects by cloning existing instances so callers avoid concrete constructors and expensive setup.

## When to use

- Expensive initialization or setup you want to avoid repeating.
- You repeatedly create similar objects from presets.
- You need copies without knowing the concrete class behind an interface.
- Object creation is driven by runtime configuration or templates.
- Variants are derived from a baseline with small tweaks.
- You want to centralize creation logic in `clone()`.
- You need a registry of ready-to-copy prototypes.

## When NOT to use

- External resources cannot be safely cloned (files, sockets, db handles).
- Circular references make cloning ambiguous or unsafe.
- Deep copy requirements are unclear or inconsistent.
- Construction is cheap and simple.
- Object graphs are small and better built directly.
- Shared mutable references would be surprising to callers.
- You cannot define a clear clone contract.

## Minimal TypeScript shape

```ts
interface Prototype<T> {
  clone(): T;
}
```

## Example 1: Shape clone (TypeScript)

```ts
interface Shape extends Prototype<Shape> {
  x: number;
  y: number;
  color: string;
}

class Circle implements Shape {
  constructor(
    public x: number,
    public y: number,
    public color: string,
    public radius: number
  ) {}

  clone(): Circle {
    return new Circle(this.x, this.y, this.color, this.radius);
  }
}

class Rectangle implements Shape {
  constructor(
    public x: number,
    public y: number,
    public color: string,
    public width: number,
    public height: number
  ) {}

  clone(): Rectangle {
    return new Rectangle(this.x, this.y, this.color, this.width, this.height);
  }
}

const circle = new Circle(10, 20, "red", 5);
const circleCopy = circle.clone();
```

## Example 2: Prototype registry (TypeScript)

```ts
interface Prototype<T> {
  clone(): T;
}

class Circle implements Prototype<Circle> {
  constructor(
    public x: number,
    public y: number,
    public color: string,
    public radius: number
  ) {}

  clone(): Circle {
    return new Circle(this.x, this.y, this.color, this.radius);
  }
}

class PrototypeRegistry<T extends Prototype<T>> {
  private items = new Map<string, T>();

  register(name: string, prototype: T): void {
    this.items.set(name, prototype);
  }

  create(name: string): T {
    const proto = this.items.get(name);
    if (!proto) throw new Error(`Unknown prototype: ${name}`);
    return proto.clone();
  }
}

const registry = new PrototypeRegistry<Circle>();
registry.register("defaultCircle", new Circle(0, 0, "blue", 10));
registry.register("largeRedCircle", new Circle(0, 0, "red", 50));

const c1 = registry.create("defaultCircle");
const c2 = registry.create("largeRedCircle");
```

## Deep vs shallow cloning (TypeScript)

```ts
type Style = { border: { color: string; width: number } };

class Box implements Prototype<Box> {
  constructor(public width: number, public style: Style) {}

  clone(): Box {
    return new Box(this.width, { border: { ...this.style.border } });
  }
}

const original = new Box(10, { border: { color: "black", width: 1 } });
const copy = original.clone();
```

## TypeScript adaptations

- Copy constructor pattern: `constructor(source: Widget)` can simplify cloning.
- Structural typing pitfalls: spreading a class drops prototypes and methods.
- Handle Dates/Maps/Sets explicitly in `clone()` to preserve semantics.

## Common pitfalls

- JSON clone breaks classes, Dates, Maps/Sets, and methods.
- Forgetting to override `clone()` in subclasses.
- Mutating shared references after a shallow copy.
- Clone leaks half-built state or skips validation.
- Copying resources that should not be duplicated.
- Inconsistent clone behavior across types.
- Overusing deep cloning where shallow copy is enough.
- Not documenting clone contract (deep vs shallow).

## Checklist for refactors

- Define the clone contract (deep vs shallow per field).
- Decide which fields are shared vs copied.
- Add explicit `clone()` to each concrete class.
- Avoid JSON-based cloning for class instances.
- Add a registry only if reuse/presets exist.
- Ensure clone preserves invariants and validation.
- Add tests for cloned object independence.
- Document non-cloneable resources.

## Output expectations

When invoked, produce:
- A clone contract and concrete clone implementations.
- A registry if requested and justified.
- A migration plan from constructors to cloning.
