---
name: oop-specialist
description: Apply object-oriented design principles (SOLID/GRASP) when writing or reviewing code in this TypeScript + Next.js codebase. Use when designing/refactoring services, libraries, domain models, and module boundaries; triggers on high coupling, low cohesion, duplicated business rules, and unclear responsibilities.
---

# OOP Specialist

Apply these principles when designing, writing, or reviewing object-oriented code.

## Core Constraints (Heuristics)

- Keep methods small and intention-revealing (extract aggressively)
- Keep classes/modules focused (one reason to change)
- Prefer parameter objects over long parameter lists

## SOLID Principles

| Principle | Rule                       | Violation Sign                                  |
| --------- | -------------------------- | ----------------------------------------------- |
| **SRP**   | One reason to change       | Class name includes "And" or "Manager"          |
| **OCP**   | Extend, don't modify       | Adding features requires changing existing code |
| **LSP**   | Subtypes substitute base   | Overridden method raises unexpected errors      |
| **ISP**   | Small, specific interfaces | Implementing empty/stub methods                 |
| **DIP**   | Depend on abstractions     | Instantiating dependencies directly             |

## GRASP Principles

- **Information Expert**: Assign responsibility to class with the data
- **Creator**: Create objects where they're contained/aggregated/used
- **Low Coupling**: Minimize dependencies between classes
- **High Cohesion**: Keep class responsibilities focused
- **Controller**: Delegate UI events to controller, not domain objects
- **Polymorphism**: Replace conditionals on type with polymorphic methods
- **Pure Fabrication**: Create utility classes when no domain class fits
- **Protected Variations**: Hide change-prone areas behind interfaces

## Key Heuristics

### Tell, Don't Ask

```ts
// Bad: pull data out, decide elsewhere
if (order.status === "pending" && order.totalCents > 10_000) {
  order.applyDiscountPercent(10);
}

// Good: tell the object what to do
order.applyDiscountIfEligible();
```

### Composition Over Inheritance

Use inheritance only when child "is-a" parent. Prefer composition for "has-a" or "uses-a" relationships.

```ts
type Item = { id: string; priceCents: number };
type PricingStrategy = { priceTotalCents: (items: Item[]) => number };

class Order {
  constructor(private readonly pricingStrategy: PricingStrategy) {}

  totalCents(items: Item[]) {
    return this.pricingStrategy.priceTotalCents(items);
  }
}
```

### DRY (Don't Repeat Yourself)

Extract duplicated logic. Three occurrences = extract immediately.

## Design Patterns Quick Reference

| Pattern             | Use When                                      |
| ------------------- | --------------------------------------------- |
| **Factory**         | Object creation logic is complex or varies    |
| **Builder**         | Constructing complex objects step-by-step     |
| **Strategy**        | Algorithms vary and should be interchangeable |
| **State**           | Behavior changes based on internal state      |
| **Facade**          | Simplifying a complex subsystem interface     |
| **Template Method** | Algorithm structure fixed, steps vary         |
| **Null Object**     | Avoiding nil checks with default behavior     |

## Functional Patterns

Prefer `map`, `filter`/`select`, `reduce` over manual iteration:

```ts
// Bad
const results: string[] = [];
for (const item of items) {
  if (item.active) results.push(item.name);
}

// Good
const results = items.filter((i) => i.active).map((i) => i.name);
```

## Clean Architecture Layers

```
┌─────────────────────────────────────┐
│  Frameworks & Drivers (outer)       │  ← Next.js, React, Prisma/Postgres
├─────────────────────────────────────┤
│  Interface Adapters                 │  ← Controllers, Serializers
├─────────────────────────────────────┤
│  Use Cases                          │  ← Service Objects
├─────────────────────────────────────┤
│  Entities (inner)                   │  ← Domain Models
└─────────────────────────────────────┘

Dependencies point INWARD only.
```

In this repo, a practical mapping is:

- **Frameworks & drivers**: Next.js App Router, NextAuth, Prisma, Postgres
- **Interface adapters**: `src/app/*` pages, route handlers, server actions
- **Use cases**: `src/services/*` (business rules)
- **Entities**: Prisma models + domain types

## References

For detailed patterns and examples:

- **SOLID examples**: See [references/solid.md](references/solid.md)
- **Design patterns**: See [references/design-patterns.md](references/design-patterns.md)
- **GRASP detailed**: See [references/grasp.md](references/grasp.md)
