---
name: factory-method-pattern-typescript
description: Provide TypeScript guidance, examples, and when to use Factory Method to reduce coupling to concretes and support product variants across environments.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Factory Method (TypeScript)

## Intent

Define a creation hook so subclasses or modules decide which concrete product to instantiate, keeping callers decoupled from concrete types.

## When to use

- You need to add new product variants without changing callers.
- Creation logic is complex or varies by environment/tenant.
- A base workflow should remain stable while product types change.
- You want to avoid large switch statements across the codebase.
- Library or framework users should extend creation behavior safely.

## When NOT to use

- A single constructor or small switch is stable and unlikely to change.
- There is no meaningful variation in product types.
- A simple factory function is sufficient.
- Indirection would obscure debugging or ownership.

## Minimal TypeScript shape

```ts
interface Product {
  use(): void;
}

abstract class Creator {
  protected abstract createProduct(): Product;

  run(): void {
    const product = this.createProduct();
    product.use();
  }
}
```

## Example 1: Transport logistics (TypeScript)

Before (small snippet):
```ts
function planDelivery(mode: "truck" | "ship") {
  const transport = mode === "truck" ? new Truck() : new Ship();
  transport.deliver();
}
```

After (Factory Method):
```ts
interface Transport {
  deliver(): void;
}

class Truck implements Transport {
  deliver() {
    console.log("Deliver by land");
  }
}

class Ship implements Transport {
  deliver() {
    console.log("Deliver by sea");
  }
}

abstract class Logistics {
  planDelivery(): void {
    const transport = this.createTransport();
    transport.deliver();
  }

  protected abstract createTransport(): Transport;
}

class RoadLogistics extends Logistics {
  protected createTransport(): Transport {
    return new Truck();
  }
}

class SeaLogistics extends Logistics {
  protected createTransport(): Transport {
    return new Ship();
  }
}

const logistics = new RoadLogistics();
logistics.planDelivery();
```

## Example 2: Cross-platform UI (TypeScript)

```ts
interface Button {
  render(): void;
}

class WindowsButton implements Button {
  render() {
    console.log("Render Windows button");
  }
}

class WebButton implements Button {
  render() {
    console.log("Render Web button");
  }
}

abstract class Dialog {
  open(): void {
    const button = this.createButton();
    button.render();
  }

  protected abstract createButton(): Button;
}

class WindowsDialog extends Dialog {
  protected createButton(): Button {
    return new WindowsButton();
  }
}

class WebDialog extends Dialog {
  protected createButton(): Button {
    return new WebButton();
  }
}

new WebDialog().open();
```

## TypeScript adaptations

- DI container variant (conceptual): bind the factory method to an interface and inject concrete creators per environment.

Registry/map-based factory (code):
```ts
type TransportKind = "truck" | "ship";

type TransportFactory = () => Transport;

const registry: Record<TransportKind, TransportFactory> = {
  truck: () => new Truck(),
  ship: () => new Ship(),
};

function createTransport(kind: TransportKind): Transport {
  return registry[kind]();
}
```

Cached/pool instances (code):
```ts
const cache = new Map<TransportKind, Transport>();

function getTransport(kind: TransportKind): Transport {
  const existing = cache.get(kind);
  if (existing) return existing;
  const created = createTransport(kind);
  cache.set(kind, created);
  return created;
}
```

## Common pitfalls

- Using Factory Method when a simple factory function is enough.
- Letting creators return overly concrete types instead of interfaces.
- Hiding too much logic in constructors without clear product boundaries.
- Deep inheritance hierarchies instead of composition or registries.
- Forgetting to centralize variant selection logic.

## Checklist for refactors

- Identify product interface and stable behavior in callers.
- Extract creation logic into a creator hook or factory method.
- Replace switch statements with polymorphic creators or registries.
- Add new product types without modifying existing creators.
- Ensure DI or configuration selects the creator at runtime.
- Add tests for each product variant.

## Output expectations

When invoked, produce:
- Recommended structure for creators and products.
- A small, tailored TypeScript example.
- A migration plan from direct instantiation to factory method.
