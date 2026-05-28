---
name: visitor-pattern-typescript
description: TypeScript guidance for Visitor to separate algorithms from object structure via accept/visitor double dispatch, add new operations without modifying elements, and handle trade-offs when adding new element types; includes TS method naming realities and disambiguation vs Strategy/Command/Mediator/union-switch.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Visitor Pattern (TypeScript)

## Intent

Separate algorithms from object structures by moving operations into visitors and using `accept(visitor)` for double dispatch.

## When to use

- AST formatting/evaluation passes.
- Exports to multiple formats (XML/JSON/CSV).
- Validation passes across stable node structures.
- Metrics/analytics aggregation over node trees.
- Permissions/policy evaluation over hierarchical structures.
- Code generation over a stable IR.
- Rendering/layout over UI node trees.
- Diffing/printing composite structures.

## When NOT to use

- Element hierarchy changes frequently.
- You only need one operation.
- Strategy selection is the real need.
- Mediator/Observer style coordination is needed.
- A discriminated union with exhaustive switch is simple and sufficient.
- You cannot modify elements to add `accept`.
- Performance is ultra-hot and visitor indirection hurts.
- Visitor explosion creates too many tiny visitors.

## Mental model

Elements accept a visitor; the visitor has one method per concrete element; `accept` calls the correct method (double dispatch).

## Recommended TS shapes

- `interface Visitor<R = void> { visitX(x: X): R }` per element type.
- `interface Visitable<R = void> { accept(v: Visitor<R>): R }`.
- Keep traversal outside visitors unless it is part of the operation.

## Example 1: Shapes export + area/perimeter

Elements: Dot, Circle, Rectangle, CompoundShape. Visitors: XmlExportVisitor, AreaVisitor.

## Example 2: Expression AST evaluation + pretty-printing

Nodes: Literal, Add, Multiply, Negate. Visitors: EvalVisitor, PrintVisitor.

## Example 3: Policy check over organization graph

Nodes: Team, User, ServiceAccount. Visitor returns decision and collects diagnostics.

## Testing strategy (pragmatic)

- Verify each element calls the correct visitor method (trace array).
- Contract tests for visitor interface completeness.
- Snapshot-ish tests for output visitors (printer/exporter).

## Common pitfalls

- Adding new element types breaks every visitor.
- Mixing traversal and operation incorrectly.
- Visitors with hidden mutable global state.
- Violating encapsulation to access private fields.
- Circular dependencies between visitors and elements.
- Too many tiny visitors with unclear responsibility.
- Forgetting to update `accept` when subclassing.
- Returning void everywhere, making testing harder.
- Downcasting in client code instead of using accept.
- Using Visitor where Strategy would be simpler.

## Checklist for refactors

- Identify repeated type-switch logic in clients.
- Define a visitor interface and element accept method.
- Implement accept per element type.
- Move operation branches into a visitor class.
- Add another operation as a new visitor.
- Remove client branching and `instanceof` checks.
- Add trace tests for double dispatch.
- Keep visitor methods cohesive and small.

## Output expectations

When invoked, produce: Visitor interface, Visitable elements with accept, 2-3 concrete visitors, and tests/examples showing no client `instanceof`/`switch` branching.
