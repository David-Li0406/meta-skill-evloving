---
name: state-pattern-typescript
description: TypeScript guidance for State with context + state objects, explicit transitions/guards, eliminating switch/if explosions, testing transition validity, serialization strategies, and disambiguation vs Strategy/FSM/workflow.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# State Pattern (TypeScript)

## Intent

Model behavior that changes based on a finite set of internal states by delegating to state objects and making transitions explicit.

## When to use

- You want to document and enforce a lifecycle.
- Object behavior varies by state and changes over time.
- Switch/if ladders keyed by state are spreading across methods.
- You need explicit transition rules with guards.
- Payment/order lifecycles require valid transitions and clear errors.
- UI component modes or wizard steps change allowed actions.
- Retry/backoff modes or connection states need clean transitions.
- The workflow is in-process (not a long-lived orchestration).

## When NOT to use

- Only a few states exist and logic is stable.
- You just need to swap algorithms without transitions (Strategy).
- You need persisted, long-running orchestration across systems.
- Table-driven transitions are enough and behavior is trivial.
- State is just validation rules with no behavior change.
- The state graph explodes with too many variants.
- You can model it as data + pure functions without polymorphism.
- Team prefers a declarative FSM library and can adopt it safely.

## Mental model

Context holds current state and delegates actions to it; states can request transitions; transitions enforce invariants.

## Recommended TS shapes

- OO state objects: `State { onPublish(ctx): void }`.
- Event-driven actions: `dispatch(action: Action)` where each state handles its own action switch.
- Serialization: `stateKey` on context + `fromKey(...)` factory to rehydrate state objects.

## Example 1: Document lifecycle (Draft -> Moderation -> Published)

Show role checks and illegal transitions with explicit errors.

## Example 2: Order/Payment lifecycle (guards + side-effects)

Show `Pending`, `Authorized`, `Captured`, `Refunded`, `Failed` with typed errors.

## Example 3: Connection state machine (retry/backoff)

Use singleton stateless states and a `stateKey` serializer.

## Testing strategy (pragmatic)

- Transition matrix tests (valid and invalid moves).
- Per-state behavior tests with minimal context fakes.
- Invariant tests for shared context state.
- Serialization round-trip for stateKey factories.

## Common pitfalls

- State explosion with too many variants.
- Duplicated transition logic across states.
- God-context with too much shared mutable state.
- Leaky context API (states can do too much).
- Unserializable state objects in persistence flows.
- Side-effects in state constructors.
- Missing guard tests for illegal transitions.
- Hidden transitions that bypass the state interface.
- Mixing validation logic with behavior rules in multiple places.
- Recreating state objects in hot paths unnecessarily.

## Checklist for refactors

- Extract a state interface with explicit actions.
- Move state-specific branches into state classes.
- Centralize transitions through the context.
- Guard illegal transitions with typed errors.
- Add a transition matrix test suite.
- Decide on a serialization strategy (stateKey + factory).
- Document actions and expected transitions.
- Keep context invariants clear and enforced.

## Output expectations

When invoked, produce: a state diagram/table, state interface, concrete states, transition rules/guards, and runnable TS examples tailored to the user input.
