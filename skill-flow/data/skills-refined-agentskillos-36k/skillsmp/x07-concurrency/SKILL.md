---
name: x07-concurrency
description: Canonical deterministic concurrency patterns in X07 (defasync + task.* + chan.bytes.*), including the determinism constraints.
metadata:
  short-description: Deterministic async patterns
  version: 0.1.0
  kind: docs
---

# x07-concurrency

X07 concurrency is deterministic and virtual (no OS threads); blocking points are explicit.

## Canonical patterns

- Use `defasync` + `task.*` + `chan.bytes.*` for deterministic concurrency.
- Avoid implicit sources of nondeterminism (OS clocks, random, network) in solve worlds.
- Keep scheduling decisions explicit and data-driven (inputs → outputs), so runs are replayable.

For the built-in reference guide, use `x07 guide` and search for `defasync` / `task.` / `chan.bytes.`.
