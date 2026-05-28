---
name: builder-pattern-typescript
description: TypeScript guidance and examples for Builder: step-by-step construction, optional director, immutable product, and avoiding telescoping constructors.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Builder (TypeScript)

## Intent

Separate construction from representation so complex objects can be built step-by-step while keeping the final product immutable.

## When to use

- Telescoping constructor or too many optional parameters.
- Construction order matters or has conditional steps.
- You need multiple representations from the same construction steps.
- You want fluent, readable setup with method chaining.
- Validation or defaults must be centralized during construction.
- You need to reuse construction routines across products.
- You want to keep the product immutable after build.

## When NOT to use

- Object literal + schema validation is enough.
- Only a few optional params and order does not matter.
- Construction is trivial or unlikely to change.
- A simple factory function is sufficient.
- Builder would add indirection without benefit.
- The product is already immutable and easy to instantiate.

## Minimal TypeScript shape

```ts
interface Builder<T> {
  reset(): this;
  build(): T;
}

class ProductBuilder implements Builder<Product> {
  private draft: ProductDraft = { /* ... */ };

  withFoo(value: string): this {
    this.draft.foo = value;
    return this;
  }

  build(): Product {
    return Object.freeze({ ...this.draft });
  }

  reset(): this {
    this.draft = { /* ... */ };
    return this;
  }
}
```

## Example 1: House builder (TypeScript)

```ts
type Heating = "gas" | "electric" | "none";

type House = Readonly<{
  floors: number;
  hasPool: boolean;
  hasGarden: boolean;
  heating: Heating;
}>;

class HouseBuilder {
  private floors = 1;
  private hasPool = false;
  private hasGarden = false;
  private heating: Heating = "none";

  withFloors(floors: number): this {
    this.floors = floors;
    return this;
  }

  addPool(): this {
    this.hasPool = true;
    return this;
  }

  addGarden(): this {
    this.hasGarden = true;
    return this;
  }

  setHeating(type: Heating): this {
    this.heating = type;
    return this;
  }

  build(): House {
    const house: House = {
      floors: this.floors,
      hasPool: this.hasPool,
      hasGarden: this.hasGarden,
      heating: this.heating,
    };
    return Object.freeze(house);
  }
}

const house = new HouseBuilder()
  .withFloors(2)
  .addGarden()
  .setHeating("gas")
  .build();
```

## Example 2: Car + Manual (TypeScript)

Director routine:
```ts
type Car = Readonly<{ model: string; seats: number; hasSportPackage: boolean }>; 

type Manual = Readonly<{ title: string; steps: string[] }>;

interface CarBuilder {
  reset(): this;
  setModel(model: string): this;
  setSeats(seats: number): this;
  enableSportPackage(): this;
  build(): Car;
}

interface ManualBuilder {
  reset(): this;
  setModel(model: string): this;
  setSeats(seats: number): this;
  enableSportPackage(): this;
  build(): Manual;
}

class Director {
  makeSportsCar(builder: { reset(): any; setModel(m: string): any; setSeats(s: number): any; enableSportPackage(): any; build(): any; }) {
    builder.reset().setModel("Sports").setSeats(2).enableSportPackage();
    return builder.build();
  }

  makeSUV(builder: { reset(): any; setModel(m: string): any; setSeats(s: number): any; enableSportPackage(): any; build(): any; }) {
    builder.reset().setModel("SUV").setSeats(5);
    return builder.build();
  }
}
```

Client direct calls (no director):
```ts
const custom = new CarProductBuilder()
  .setModel("Custom")
  .setSeats(4)
  .build();
```

## TypeScript adaptations

- Fluent builder with method chaining (preferred).
- Director as reusable construction routines (optional).
- Type-safety tips: keep product readonly, use narrow unions for options, avoid leaking partial drafts.

## Common pitfalls

- Leaking partially built product before `build()`.
- Builder becomes a god object with too many responsibilities.
- Too many steps without clear grouping.
- Mutable product returned instead of immutable snapshot.
- Skipping validation in build step.
- Duplicating construction logic across builders.
- Using Builder when a simple config object suffices.

## Checklist for refactors

- Identify construction steps and their order.
- Decide if a director adds reuse across products.
- Define a clear product type with readonly fields.
- Keep builder mutable, product immutable.
- Replace telescoping constructors with fluent steps.
- Centralize validation in `build()`.
- Provide sensible defaults and reset behavior.
- Add tests for key build variants.

## Output expectations

When invoked, produce:
- A builder API and product types.
- A tailored TypeScript example.
- A migration plan from constructors/config to builder.
