---
name: template-method-pattern-typescript
description: TypeScript guidance for Template Method with a fixed algorithm skeleton, overridable steps and hooks to reduce duplication across variants, polymorphic client usage, TS enforcement patterns, and disambiguation vs Strategy/State/Command.
compatibility: Codex CLI / filesystem agents; no external tools required.
metadata:
  author: codex
  version: 0.1.0
---

# Template Method Pattern (TypeScript)

## Intent

Define a stable algorithm skeleton in a base class and let subclasses override selected steps or hooks without changing the overall order.

## When to use

- Import pipelines (CSV/PDF/DOC) with shared sequence but different parsing.
- ETL workflows with common stages and varied implementations.
- Report generation pipelines with shared fetch/deliver steps.
- Payment processing flows (validate -> authorize -> capture) with varied details.
- Background job runners with consistent lifecycle hooks.
- Notification rendering pipelines with per-channel formatting.
- Parsing/normalization flows with shared structure.
- ML/data-prep pipelines that share ordering but vary transforms.

## When NOT to use

- You need runtime swapping between algorithms (Strategy).
- Behavior changes due to lifecycle/state transitions (State).
- You need queue/log/undo or remote execution of requests (Command).
- Variations are data-only parameters or configuration.
- Only a couple of variants with low duplication; a shared function is clearer.
- Excessive subclassing would create a fragile base class.
- The base class would need too much IO knowledge.
- The workflow is not stable enough to justify a skeleton.

## Mental model

Base class owns the workflow and ordering; subclasses override variable steps; hooks provide optional extension points.

## Recommended TS shapes

- Abstract base class with `run()` template method calling `protected` steps.
- Hooks as `protected beforeX()/afterX()` no-ops.
- "Final-ish" enforcement: `public run()` calls a `private doRun()`; subclasses override only steps.

## Example 1: Document import pipeline (CSV/DOC/PDF)

Steps: load -> parse -> normalize -> validate -> persist -> report. Base provides normalization/validation.

## Example 2: Payment processing flow (Card/BankTransfer)

Steps: validate -> authorize -> capture -> receipt, with a hook around `authorize`.

## Example 3: Report generation (Summary/Detailed)

Steps: fetch -> compute -> format -> deliver. Base handles fetch + deliver; subclasses override compute/format.

## Testing strategy (pragmatic)

- Base-class contract tests using a fake subclass.
- Per-subclass tests for overridden steps.
- Verify ordering with an in-memory trace.
- Ensure hooks are optional and no-op by default.

## Common pitfalls

- Too many steps making the base hard to understand.
- Overriding the template method itself.
- Calling overridable methods from constructors.
- Leaking shared mutable state across subclasses.
- Fragile base class changes that break subclasses.
- Mixing selection logic with template orchestration.
- Tight coupling to IO inside the base class.
- Too many tiny subclasses that differ only by data.
- LSP surprises when subclasses "disable" default steps.
- Using Template Method when Strategy would be simpler.

## Checklist for refactors

- Identify duplicated workflows across implementations.
- Define clear step boundaries and names.
- Move the skeleton to a base class.
- Make variable steps `protected` or `abstract`.
- Add hooks for optional behavior.
- Migrate variants one by one.
- Remove client conditionals once subclasses exist.
- Add ordering tests and per-variant tests.

## Output expectations

When invoked, produce: base abstract class, clear step methods + hooks, 2-4 concrete subclasses, and tests/examples demonstrating ordering and overrides.
