---
name: strategy-pattern-typescript
description: TypeScript guidance for Strategy with interchangeable algorithms, context delegation, client selection, runtime swapping, removing switch/if ladders, DI or registry selection, per-algorithm tests, and disambiguation vs State/Command/Template Method.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Strategy Pattern (TypeScript)

## Intent

Encapsulate a family of algorithms behind a common interface so the client can select and swap behavior without changing the context.

## When to use

- Route planning variants (driving, walking, transit, cycling).
- Pricing, tax, or discount policies that vary by customer or region.
- Export formats (CSV, JSON, XML) with shared context API.
- Search ranking/scoring options that change by feature flag.
- Authorization policies that are interchangeable by tenant.
- Retry/backoff policies that are algorithmic and configurable.
- Parsing strategies for different input formats.
- Feature-flagged behavior that should not introduce switch ladders.

## When NOT to use

- Only a few stable variants exist and conditionals are clear.
- The behavior changes based on lifecycle state transitions (State).
- You need to queue/log/undo requests (Command).
- You need a fixed algorithm skeleton with overridable steps (Template Method).
- Differences are data-only and can be captured as configuration.
- The context would still branch to select variants everywhere.
- It would introduce over-abstraction and add little value.
- The strategies require heavy shared state that belongs in the context.

## Mental model

Context owns the workflow and delegates the variable part to a strategy; the client selects the strategy; strategies do not manage the context lifecycle.

## Recommended TS shapes

- OO: `interface RouteStrategy { buildRoute(input): Route }`.
- Functional: `type StrategyFn = (input) => output`.
- Registry: `Record<StrategyKey, Strategy>` with selection and validation.

## Example 1: Navigation routing strategies

Select driving/walking/transit at runtime without context conditionals.

## Example 2: Pricing/discount policy strategies

Isolate dependencies and validate inputs before applying a strategy.

## Example 3: Export format strategies

Select by key; unknown key yields a typed error.

## Testing strategy (pragmatic)

- Per-strategy unit tests with shared fixtures.
- Contract tests to ensure each strategy satisfies the same interface.
- Selection tests (valid/invalid keys).
- Edge cases for parameter validation without extra libraries.

## Common pitfalls

- Too many tiny strategies with unclear responsibilities.
- Selection logic leaking into the context.
- Inconsistent interfaces across strategies.
- Strategies mutating global state or shared singletons.
- Hidden shared dependencies not passed via constructor.
- Overusing inheritance where composition is simpler.
- Premature optimization with strategy objects on hot paths.
- Missing default strategy or unknown-key handling.
- Mixing data configuration and algorithm selection.
- Allowing strategies to mutate context invariants.

## Checklist for refactors

- Identify the conditional hotspot in the context.
- Extract a clean strategy interface.
- Move each branch into its own strategy.
- Provide a selection mechanism (DI or registry).
- Remove context branching once selection is externalized.
- Validate selection keys and inputs.
- Add per-strategy tests and shared fixtures.
- Document strategy keys, defaults, and selection rules.

## Output expectations

When invoked, produce: interface, concrete strategies, selection mechanism (DI/registry), removal of conditionals, and runnable TS examples tailored to the user input.
