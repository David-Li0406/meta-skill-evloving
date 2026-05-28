---
name: observer-pattern-typescript
description: TypeScript guidance for Observer with dynamic subscribe/unsubscribe, typed event payloads, sync vs async dispatch, lifecycle/memory leak avoidance, ordering/error isolation, and disambiguation vs Mediator, Pub/Sub, EventEmitter, and Event Sourcing.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Observer Pattern (TypeScript)

## Intent

Notify many subscribers when a publisher's state changes, while decoupling producers from consumers and managing subscription lifecycles explicitly.

## When to use

- Dynamic subscribers come and go at runtime.
- You need one-to-many fan-out notifications.
- Side effects like logging, metrics, cache invalidation, or UI refresh should be optional.
- Plugin hooks or extension points should not couple to core logic.
- Domain events should trigger secondary behaviors without tight coupling.
- Multiple independent listeners should react to the same event.
- Producers must not depend on concrete subscriber classes.
- You want a simple in-process event mechanism without a broker.

## When NOT to use

- You need durable cross-process delivery (use Pub/Sub or a broker).
- You need orchestration/transactions across handlers (use Mediator or an explicit workflow).
- The interaction is tightly coordinated among peers (Mediator fits better).
- Only one consumer exists and a direct call is simpler.
- Event storms require backpressure/throttling you can't implement safely.
- You need strict ordering with compensation across handlers (prefer explicit pipelines).
- Handlers must run exactly once across restarts (use a queue/broker).
- You're modeling undo/rollback snapshots (use Memento).

## Mental model

Publisher owns the subscriber list and emits events; subscribers react to payloads; subscriptions are a lifecycle contract with explicit unsubscribe.

## Recommended TS shapes

- Callback-based: `subscribe(fn): () => void` (preferred for small scopes).
- Interface-based: `Subscriber<T> { update(event: T): void }` for explicit contracts.
- Typed event bus: `EventBus<EventMap>` with `on/off/emit` for multi-event systems.

## Example 1: Store back-in-stock notifications (classic Observer)

Store is the publisher; customers subscribe per SKU and can unsubscribe at runtime.

## Example 2: Typed in-process EventBus

Use a typed `EventMap` and `on/off/emit` to ensure payload safety and listener isolation.

## Example 3: Domain events in a service

Core service emits domain events; observers handle email/logging/metrics without coupling.

## Testing strategy (pragmatic)

- Assert listener counts and unsubscribe behavior.
- Verify order guarantees if you claim them.
- Ensure one failing listener doesn't block others.
- Test sync vs async dispatch explicitly.

## Common pitfalls

- Memory leaks from forgotten unsubscriptions.
- Re-entrancy loops (listener triggers another event recursively).
- Event storms without throttling or batching.
- Exceptions in one handler stopping others.
- Mutable payloads shared across listeners.
- Implicit ordering assumptions not documented.
- Async race conditions when listeners mutate shared state.
- Mixing domain rules into observers instead of keeping them focused.
- Creating global singleton event buses that grow unbounded.
- Silent listener failures without logging or tracing.

## Checklist for refactors

- Identify events and their payloads.
- Define a typed event map or subscriber interface.
- Add a subscription API with an unsubscribe return value.
- Decide sync vs async dispatch and document it.
- Guard notify to isolate listener failures.
- Document ordering guarantees (or lack thereof).
- Add tests for subscribe/unsubscribe lifecycle.
- Keep payloads readonly and small.

## Output expectations

When invoked, produce: event catalog, payload types, subscription API, lifecycle rules (unsubscribe + ordering + sync/async), and runnable TS examples tailored to the user input.
