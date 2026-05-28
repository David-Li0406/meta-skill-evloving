# 11 — Async Rust (Futures, Pin, Cancellation Safety)

[CONTRACT: CTR-1101] `.await` Is a Suspension Point.
- `.await` may yield control; execution may resume later or never resume.
- Dropping the future is cancellation; destructors run for captured state.
- REJECT IF: code assumes uninterrupted execution across `.await`.
[PROVENANCE] Rust Reference: await expressions; async blocks; drop semantics apply to future state.

[INVARIANT: INV-1101] Mechanical Cancellation Safety.
- Definition: the future is drop-safe at every `.await` without violating invariants of shared state.
- REJECT IF: any `.await` occurs while an invariant is temporarily broken.
- ENFORCE BY: maintain invariants at yield points; split operations into "prepare" and "commit"; confine side effects to post-win paths.
[PROVENANCE] Rust Reference: `.await` suspension; destructors run on drop of the future.
[VERIFICATION] Tests that cancel at every await boundary (timeouts, manual drop); Miri for unsafe state captured across awaits.

[HAZARD: RSK-1101] Lock/Guard Held Across `.await`.
- FAILURE MODE: deadlocks; starvation; cancellation drops the future while holding a lock, violating INV-1101.
- REJECT IF: a lock guard spans `.await` unless explicitly part of the contract and proven safe.
- ENFORCE BY: drop guards before `.await`; use owned data; restructure to avoid holding locks across async boundaries.
[PROVENANCE] `.await` yields; drop during cancellation runs destructors for guards.
[VERIFICATION] Cancellation tests; Loom when combined with custom sync protocols.

[HAZARD: RSK-1102] Lateral State Corruption in Multi-Branch Selection.
- TRIGGER: `select`-style constructs (`tokio::select!`, `futures::select!`, manual polling of multiple futures).
- FAILURE MODE: losing branches are cancelled after partial progress; shared state mutated pre-win; invariants diverge across branches.
- REJECT IF: a selection branch mutates shared state before it is committed as the winner.
- ENFORCE BY:
  - branch-local preparation (no shared mutation) until selection resolves
  - transactional commit (idempotent updates; compare-and-swap protocols)
  - explicit cancellation handlers that restore invariants
[PROVENANCE] Async cancellation is drop of non-selected futures; shared state invariants must hold at drop points.
[VERIFICATION] Deterministic tests that force branch win/loss permutations; property tests for idempotency of commit logic.

[CONTRACT: CTR-1104] Cancellation-Safe State Mutation (Atomic Phase Pattern).
- Idempotency stores with external side effects (e.g., persist to DB) MUST use a three-phase pattern to prevent data loss on cancellation.
- REJECT IF: idempotency marker (mark) is set before side effect (persist) completes.
- ENFORCE BY: check → persist → mark pattern (only mark after successful persist).
[PROVENANCE] APM2 Implementation Standard; async cancellation is drop of the future.
[VERIFICATION] Tests that induce failure during persistence and verify the ID remains unmarked.

[CONTRACT: CTR-1102] Capture Mode Controls Ownership and `Send`.
- `async { ... }` captures by inferred borrow/move modes.
- `async move { ... }` moves captured values into the future.
- REJECT IF: capture mode changes without auditing:
  - lifetime/borrow escape
  - drop order changes
  - `Send`/`Sync`/`Unpin` changes of the returned future
[PROVENANCE] Rust Reference: async block capture semantics.
[VERIFICATION] Compile-time assertions for `Send` futures where required; tests that exercise drop order and cancellation.

[CONTRACT: CTR-1103] Pinning and Projection.
- REJECT IF: unsafe pin projection is implemented without an explicit pinned-field invariant.
- ENFORCE BY: proven pin-projection patterns; avoid self-references; keep pinned surface minimal.
[PROVENANCE] std `Pin` contract; Rustonomicon pin guidance.
[VERIFICATION] Miri for unsafe pin code; tests that move values to ensure pin requirements are enforced.

## References (Normative Anchors)

- Rust Reference: Await expressions: https://doc.rust-lang.org/reference/expressions/await-expr.html
- Rust Reference: Async blocks: https://doc.rust-lang.org/reference/expressions/block-expr.html
- std `Pin`: https://doc.rust-lang.org/std/pin/struct.Pin.html
- Rustonomicon: https://doc.rust-lang.org/nomicon/
