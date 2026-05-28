# Strategy Pattern Examples (TypeScript)

Each example is runnable in Node with ts-node.

## Example 1: Navigation routing strategies

```ts
type RouteInput = { from: string; to: string };

type Route = { distanceKm: number; etaMinutes: number; mode: string };

interface RouteStrategy {
  buildRoute(input: RouteInput): Route;
}

class DrivingStrategy implements RouteStrategy {
  buildRoute(input: RouteInput): Route {
    return { distanceKm: 10, etaMinutes: 15, mode: `drive ${input.from}->${input.to}` };
  }
}

class WalkingStrategy implements RouteStrategy {
  buildRoute(input: RouteInput): Route {
    return { distanceKm: 8, etaMinutes: 90, mode: `walk ${input.from}->${input.to}` };
  }
}

class TransitStrategy implements RouteStrategy {
  buildRoute(input: RouteInput): Route {
    return { distanceKm: 12, etaMinutes: 40, mode: `transit ${input.from}->${input.to}` };
  }
}

class Navigator {
  constructor(private strategy: RouteStrategy) {}

  setStrategy(strategy: RouteStrategy) {
    this.strategy = strategy;
  }

  plan(input: RouteInput): Route {
    return this.strategy.buildRoute(input);
  }
}

const navigator = new Navigator(new DrivingStrategy());
console.log(navigator.plan({ from: "A", to: "B" }));

navigator.setStrategy(new WalkingStrategy());
console.log(navigator.plan({ from: "A", to: "B" }));
```

## Example 2: Pricing/discount policy strategies

```ts
type Order = { subtotal: number; customerTier: "basic" | "pro"; promoCode?: string };

type PriceResult = { total: number; applied: string };

class PricingError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "PricingError";
  }
}

interface PricingStrategy {
  calculate(order: Order): PriceResult;
}

class B2BStrategy implements PricingStrategy {
  calculate(order: Order): PriceResult {
    const discount = order.customerTier === "pro" ? 0.15 : 0.05;
    return { total: order.subtotal * (1 - discount), applied: "b2b" };
  }
}

class PromoCodeStrategy implements PricingStrategy {
  private validCodes = new Map<string, number>([["SAVE10", 0.1]]);

  calculate(order: Order): PriceResult {
    if (!order.promoCode) throw new PricingError("Missing promo code");
    const discount = this.validCodes.get(order.promoCode);
    if (!discount) throw new PricingError("Invalid promo code");
    return { total: order.subtotal * (1 - discount), applied: "promo" };
  }
}

class PricingService {
  constructor(private strategy: PricingStrategy) {}

  setStrategy(strategy: PricingStrategy) {
    this.strategy = strategy;
  }

  price(order: Order): PriceResult {
    if (order.subtotal <= 0) throw new PricingError("Subtotal must be positive");
    return this.strategy.calculate(order);
  }
}

const pricing = new PricingService(new B2BStrategy());
console.log(pricing.price({ subtotal: 100, customerTier: "pro" }));

pricing.setStrategy(new PromoCodeStrategy());
try {
  console.log(pricing.price({ subtotal: 100, customerTier: "basic", promoCode: "NOPE" }));
} catch (e) {
  console.log((e as Error).message);
}
```

## Example 3: Export format strategies

```ts
type Row = { id: string; name: string };

type ExportFormat = "csv" | "json" | "xml";

type ExportResult = { contentType: string; body: string };

class ExportError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ExportError";
  }
}

interface ExportStrategy {
  export(rows: Row[]): ExportResult;
}

class CsvStrategy implements ExportStrategy {
  export(rows: Row[]): ExportResult {
    const header = "id,name";
    const lines = rows.map((r) => `${r.id},${r.name}`);
    return { contentType: "text/csv", body: [header, ...lines].join("\n") };
  }
}

class JsonStrategy implements ExportStrategy {
  export(rows: Row[]): ExportResult {
    return { contentType: "application/json", body: JSON.stringify(rows) };
  }
}

class XmlStrategy implements ExportStrategy {
  export(rows: Row[]): ExportResult {
    const body = rows
      .map((r) => `<row><id>${r.id}</id><name>${r.name}</name></row>`)
      .join("");
    return { contentType: "application/xml", body: `<rows>${body}</rows>` };
  }
}

const exportRegistry: Record<ExportFormat, ExportStrategy> = {
  csv: new CsvStrategy(),
  json: new JsonStrategy(),
  xml: new XmlStrategy(),
};

class Exporter {
  constructor(private registry: Record<ExportFormat, ExportStrategy>) {}

  export(format: string, rows: Row[]): ExportResult {
    const strategy = this.registry[format as ExportFormat];
    if (!strategy) throw new ExportError(`Unknown export format: ${format}`);
    return strategy.export(rows);
  }
}

const exporter = new Exporter(exportRegistry);
console.log(exporter.export("csv", [{ id: "1", name: "Ada" }]));
try {
  exporter.export("yaml", [{ id: "2", name: "Linus" }]);
} catch (e) {
  console.log((e as Error).message);
}
```

## Disambiguation snippet

```ts
// Strategy vs State: Strategy is selected externally; State changes with lifecycle.
// Strategy vs Command: Strategy is an algorithm; Command is a request object you can queue/log/undo.
// Strategy vs Template Method: Template Method varies steps via inheritance; Strategy swaps algorithms via composition.
// Strategy vs config: config tweaks one algorithm; Strategy swaps distinct implementations.

type Strategy = { run(input: unknown): unknown };

type State = { handle(ctx: unknown): void };

type Command = { execute(): void };
```
