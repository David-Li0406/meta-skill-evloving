# 10 — Concurrency, Atomics, Memory Ordering (Protocol-First)

[INVARIANT: INV-1001] Data Race Freedom.
- REJECT IF: any memory location can be accessed concurrently with at least one write without synchronization (lock or atomic protocol).
- ENFORCE BY: ownership transfer; locks; atomics with a named protocol; avoid `static mut`.
[PROVENANCE] Rust Reference: data races are Undefined Behavior (UB).
[VERIFICATION] Loom for custom synchronization; stress tests under contention; sanitizer builds when available.

[CONTRACT: CTR-1001] `Send`/`Sync` Are Public Contracts.
- REJECT IF: a public type’s auto-trait behavior changes unintentionally (field changes can flip `Send`/`Sync`).
- REJECT IF: `unsafe impl Send/Sync` exists without explicit invariants and a protocol description.
- ENFORCE BY: compile-time assertions in tests for expected auto-traits; keep `unsafe impl` close to the type definition; document the synchronization protocol.
[PROVENANCE] Rust Reference: auto traits; UB list includes data races.

[CONTRACT: CTR-1002] Atomic Protocol Required (No "Sprinkled Atomics").
- REJECT IF: atomic operations exist without a named protocol describing what is synchronized with what.
- Protocol must define:
  - protected data (the non-atomic memory whose visibility is controlled)
  - publication event(s) (store/fence) and consumption event(s) (load/fence)
  - required happens-before edges
  - allowed reorderings (if any)
- ENFORCE BY: code comments colocated with atomics; keep the protocol small; prefer existing primitives.
[PROVENANCE] std atomic docs describe orderings; Rust Reference defines data-race UB and basic semantics.

[HAZARD: RSK-1001] Relaxed Ordering on Weak Memory (ARM/PowerPC) Miscompiles Protocols.
- TRIGGER: `Ordering::Relaxed` used for anything other than independent counters/metrics.
- FAILURE MODE: reordering breaks publish/consume; readers observe partially initialized state.
- REJECT IF: `Relaxed` is used to synchronize access to non-atomic data.
- REJECT IF: `Relaxed` is used for flags that gate access to other memory without a weak-memory reordering analysis.
- ENFORCE BY: Acquire/Release for handoff; SeqCst only for global total-order requirements.
[PROVENANCE] std atomic ordering semantics; weak-memory architectures permit reordering absent Acquire/Release.
[VERIFICATION] Loom model tests that explore reorderings and interleavings.

## Matrix: Atomic Orderings (Minimum Use Rules)

```text
Ordering; Load semantics; Store semantics; RMW semantics; Allowed use; Reject condition
Relaxed; atomic only; atomic only; atomic only; counters/metrics; using to publish/consume non-atomic data
Acquire; acquires; n/a; acquire on load; consuming a release-published state; using without a matching release publish
Release; n/a; releases; release on store; publishing initialized data; using without a defined consumer
AcqRel; acquires; releases; both; RMW state machines; missing happens-before argument
SeqCst; total order + acq/rel; total order + acq/rel; total order + acq/rel; global invariants requiring one order; using as a substitute for protocol definition
```

[CONTRACT: CTR-1003] Happens-Before Graph Required for Custom Synchronization.
- REJECT IF: a custom primitive (lock-free structure, custom mutex, once-cell, channel) lacks an explicit happens-before graph.
- Graph must list:
  - nodes: atomic ops, lock ops, fences, critical reads/writes
  - edges: program-order, synchronizes-with, and derived happens-before
  - invariant: which writes must be visible at which reads
- ENFORCE BY: write the graph in a code-fenced block adjacent to the implementation.
[PROVENANCE] Memory ordering defines visibility via happens-before; Rust Reference defines data-race UB and concurrency fundamentals.
[VERIFICATION] Loom; stress tests; Miri for unsafe aliasing interactions in lock-free code.

```text
HB template (fill per primitive)
Nodes:
  A1: Thread A: write data (non-atomic)
  A2: Thread A: store_release FLAG=1
  B1: Thread B: load_acquire FLAG
  B2: Thread B: read data (non-atomic)
Edges:
  A1 -> A2 (program order)
  A2 -> B1 (synchronizes-with if B1 observes A2)
  B1 -> B2 (program order)
Guarantee:
  A1 happens-before B2, therefore B2 observes initialized data
```

[HAZARD: RSK-1002] Lock-Free Memory Reclamation (ABA and Use-After-Free).
- TRIGGER: lock-free structures that free nodes while other threads may still hold pointers.
- FAILURE MODE: ABA; deref of freed memory; data race UB.
- REJECT IF: memory reclamation strategy is absent (epoch-based, hazard pointers, reference counting) or unverified.
[PROVENANCE] Rust Reference: data races and invalid dereference are UB; lock-free reclamation is not automatic.
[VERIFICATION] Loom; Miri for unsafe pointer validity; targeted stress tests.

[HAZARD: RSK-1003] Locks Across Suspension Points (Async Interaction).
- TRIGGER: holding a lock/guard across `.await`.
- FAILURE MODE: deadlocks; starvation; cancellation drops the future while holding a lock.
- REJECT IF: a lock/guard spans `.await` unless explicitly required and proven cancellation-safe.
[PROVENANCE] Rust Reference: `.await` is a suspension point; dropping a future runs destructors.
[VERIFICATION] Async cancellation tests; Loom where the sync protocol can be modeled.

## References (Normative Anchors)

- Rust Reference: Behavior considered undefined (data races): https://doc.rust-lang.org/reference/behavior-considered-undefined.html
- std atomics: https://doc.rust-lang.org/std/sync/atomic/
- Rustonomicon (unsafe concurrency): https://doc.rust-lang.org/nomicon/
- Rust Reference: Await expressions: https://doc.rust-lang.org/reference/expressions/await-expr.html
