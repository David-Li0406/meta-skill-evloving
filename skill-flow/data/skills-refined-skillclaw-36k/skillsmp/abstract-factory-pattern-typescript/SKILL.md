---
name: abstract-factory-pattern-typescript
description: TypeScript guidance and examples for Abstract Factory to create families of related objects, keep variants consistent, and avoid coupling to concrete implementations.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Abstract Factory (TypeScript)

## Intent

Provide an interface to create families of related objects so variants stay consistent while callers remain decoupled from concretes.

## When to use

- You must guarantee compatible variants across collaborators.
- You need to swap entire variants via configuration or environment.
- A product family must change together (UI theme, platform, cloud provider).
- Callers should not know which concrete classes they receive.
- You want to add new variants without changing business logic.
- Testing needs full-family doubles (all products in a variant).

## When NOT to use

- Only one product type exists (no family).
- Strategy or Factory Method is enough for a single product.
- Variants are unlikely to change or expand.
- You can pass concretes directly without coupling concerns.
- The factory layer would add indirection without value.

## Minimal TypeScript shape

```ts
interface Button {
  render(): void;
}

interface Checkbox {
  check(): void;
}

interface UIFactory {
  createButton(): Button;
  createCheckbox(): Checkbox;
}
```

## Example 1: Furniture shop (TypeScript)

```ts
interface Chair {
  sitOn(): void;
}

interface Sofa {
  lieOn(): void;
}

interface CoffeeTable {
  put(item: string): void;
}

interface FurnitureFactory {
  createChair(): Chair;
  createSofa(): Sofa;
  createCoffeeTable(): CoffeeTable;
}

class ModernChair implements Chair {
  sitOn() {
    console.log("Sit on a modern chair");
  }
}

class ModernSofa implements Sofa {
  lieOn() {
    console.log("Lie on a modern sofa");
  }
}

class ModernCoffeeTable implements CoffeeTable {
  put(item: string) {
    console.log(`Place ${item} on a modern coffee table`);
  }
}

class VictorianChair implements Chair {
  sitOn() {
    console.log("Sit on a victorian chair");
  }
}

class VictorianSofa implements Sofa {
  lieOn() {
    console.log("Lie on a victorian sofa");
  }
}

class VictorianCoffeeTable implements CoffeeTable {
  put(item: string) {
    console.log(`Place ${item} on a victorian coffee table`);
  }
}

class ModernFurnitureFactory implements FurnitureFactory {
  createChair(): Chair {
    return new ModernChair();
  }
  createSofa(): Sofa {
    return new ModernSofa();
  }
  createCoffeeTable(): CoffeeTable {
    return new ModernCoffeeTable();
  }
}

class VictorianFurnitureFactory implements FurnitureFactory {
  createChair(): Chair {
    return new VictorianChair();
  }
  createSofa(): Sofa {
    return new VictorianSofa();
  }
  createCoffeeTable(): CoffeeTable {
    return new VictorianCoffeeTable();
  }
}

function furnishRoom(factory: FurnitureFactory) {
  const chair = factory.createChair();
  const sofa = factory.createSofa();
  const table = factory.createCoffeeTable();
  chair.sitOn();
  sofa.lieOn();
  table.put("magazine");
}

const factory = new ModernFurnitureFactory();
furnishRoom(factory);
```

## Example 2: Cross-platform UI family (TypeScript)

```ts
interface Button {
  render(): void;
}

interface Checkbox {
  toggle(): void;
}

interface UIControlFactory {
  createButton(): Button;
  createCheckbox(): Checkbox;
}

class WinButton implements Button {
  render() {
    console.log("Render Windows button");
  }
}

class WinCheckbox implements Checkbox {
  toggle() {
    console.log("Toggle Windows checkbox");
  }
}

class MacButton implements Button {
  render() {
    console.log("Render Mac button");
  }
}

class MacCheckbox implements Checkbox {
  toggle() {
    console.log("Toggle Mac checkbox");
  }
}

class WindowsUIFactory implements UIControlFactory {
  createButton(): Button {
    return new WinButton();
  }
  createCheckbox(): Checkbox {
    return new WinCheckbox();
  }
}

class MacUIFactory implements UIControlFactory {
  createButton(): Button {
    return new MacButton();
  }
  createCheckbox(): Checkbox {
    return new MacCheckbox();
  }
}

function renderSettings(factory: UIControlFactory) {
  factory.createButton().render();
  factory.createCheckbox().toggle();
}

renderSettings(new MacUIFactory());
```

## TypeScript adaptations

Function-object factory (preferred TS style):
```ts
type Variant = "modern" | "victorian";

type FurnitureFactory = {
  createChair(): Chair;
  createSofa(): Sofa;
  createCoffeeTable(): CoffeeTable;
};

const factories: Record<Variant, FurnitureFactory> = {
  modern: {
    createChair: () => new ModernChair(),
    createSofa: () => new ModernSofa(),
    createCoffeeTable: () => new ModernCoffeeTable(),
  },
  victorian: {
    createChair: () => new VictorianChair(),
    createSofa: () => new VictorianSofa(),
    createCoffeeTable: () => new VictorianCoffeeTable(),
  },
};
```

Class-based factories (brief):
```ts
abstract class BaseFactory implements FurnitureFactory {
  abstract createChair(): Chair;
  abstract createSofa(): Sofa;
  abstract createCoffeeTable(): CoffeeTable;
}
```

DI-container mapping (conceptual): register a factory per variant and inject the chosen factory by config/environment.

## Common pitfalls

- Matrix explosion: too many product types and variants without a plan.
- Leaky concretes: callers depend on concrete classes instead of interfaces.
- Missing product in a variant, causing runtime mismatch.
- Mixing products from different families in the same workflow.
- Overusing Abstract Factory when Factory Method is enough.
- Forgetting tests that assert variant compatibility.

## Checklist for refactors

- Identify the product family and its members.
- Map the matrix: product types × variants.
- Ensure every variant implements every product type.
- Create a factory interface that returns the family.
- Switch configuration to select one factory for a workflow.
- Update callers to depend on interfaces only.
- Add tests that validate cross-product compatibility.

## Output expectations

When invoked, produce:
- Recommended interfaces and concrete factories.
- A tailored TypeScript example.
- A migration plan to Abstract Factory with variant selection.
