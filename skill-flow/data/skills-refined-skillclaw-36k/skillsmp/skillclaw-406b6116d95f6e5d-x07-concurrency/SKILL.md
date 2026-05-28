---
name: x07-concurrency
description: Use this skill when you need to implement deterministic concurrency patterns in X07, ensuring that your asynchronous operations are predictable and reproducible.
---

# Skill body

X07 concurrency is deterministic and virtual (no OS threads); blocking points are explicit.

## Canonical patterns

- Use `defasync` + `task.*` + `chan.bytes.*` for deterministic concurrency.
- Avoid implicit sources of nondeterminism (OS clocks, random, network) in solve worlds.
- Keep scheduling decisions explicit and data-driven (inputs → outputs), so runs are replayable.

For the built-in reference guide, use `x07 guide` and search for `defasync` / `task.` / `chan.bytes.`.