---
name: memento-pattern-typescript
description: TypeScript guidance and examples for snapshot/restore undo and rollback while preserving encapsulation; clarifies originator/memento/caretaker roles, Command+Memento undo flows, and memory trade-offs versus Command/Prototype/Event Sourcing.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Memento Pattern (TypeScript)

## Intent

Capture and restore an object's internal state without exposing its internals, enabling undo/redo and rollback with clear ownership of snapshots.

## When to use

- You need undo/redo for complex state changes.
- Transaction-like rollback is required after partial failures.
- Encapsulation matters; external code must not access internal fields.
- Multiple independent instances need their own history.
- You want metadata-only history in a caretaker (timestamp/label).
- Snapshot timing should be controlled outside the originator.
- You need deterministic restoration for tests and audits.

## When NOT to use

- Immutable state already allows keeping prior values cheaply.
- A differential log or event sourcing is more appropriate.
- Snapshots are too large or too frequent for memory limits.
- External resources (files/handles/network) cannot be restored safely.
- You only need a simplified API (Facade is enough).
- State is trivial and can be recomputed quickly.
- Undo/redo is not a real requirement (avoid extra complexity).

## Mental model

Originator owns state and knows how to snapshot/restore; Caretaker owns timing/history; Memento is an immutable snapshot object.

## Recommended TS shapes

- Classic: originator creates opaque `Memento` objects; caretaker stores them and never reads payload.
- Strict: memento exposes only metadata + `restore(originator)`; payload stays private.
- Command+Memento: commands capture pre-state mementos and call `undo()` by restoring.

## Example 1: Text editor snapshot (classic caretaker stack)

Use an editor originator with a history caretaker storing opaque mementos (text, cursor, selection) and metadata only.

## Example 2: Command + Memento undo/redo

Commands capture a pre-mutation memento, execute mutations, and undo by restoring; caretaker manages undo/redo stacks.

## Example 3: Transactional rollback for a service aggregate

Use mementos to rollback a Cart/OrderDraft when validation fails mid-update.

## Testing strategy (pragmatic)

- Round-trip tests: snapshot -> mutate -> restore -> equals original.
- Ensure caretakers cannot access payload fields.
- Test bounded history behavior and snapshot frequency policies.

## Common pitfalls

- Mutable references inside mementos causing shared-state leaks.
- Snapshotting too often (memory blowup) or too rarely (coarse undo).
- Unbounded history growth with no caps/eviction.
- Caretaker peeking into snapshot data (breaks encapsulation).
- Restoring stale external references (files, sockets).
- Non-deterministic mutations between snapshot and restore.
- Forgetting to snapshot before mutation.
- Treating mementos as serialization format for external APIs.

## Checklist for refactors

- Identify the originator and its state boundary.
- Define a snapshot contract (what is captured, what is not).
- Keep mementos immutable and opaque to caretakers.
- Wire snapshot-before-mutation points.
- Add a caretaker history with size limits or checkpoints.
- Ensure restore is deterministic and tested.
- Decide whether Command+Memento is needed for undo/redo flows.
- Document snapshot frequency and memory impact.

## Output expectations

When invoked, produce: a memento API (originator + memento + caretaker), snapshot timing, bounded history strategy, and minimal TS examples tailored to the user input.
