# 26 — APM2 Safe Patterns and Anti-Patterns (Token-Efficient Index)

This chapter replaces the legacy APM2 safe patterns catalog.

Goal: keep project-specific guidance compact and point to deeper contracts in Chapters 07/09/10/12/15/16/19/20/24/25.

## Safe Patterns (Defaults)

[CONTRACT: CTR-2601] Shared Mutable State Uses Standard Primitives.
- REJECT IF: shared mutable state uses ad-hoc interior mutability or custom synchronization without a protocol (CTR-1002).
- ENFORCE BY: `Arc<RwLock<T>>` for read-heavy state; `Arc<Mutex<T>>` otherwise; explicit lock ordering; no guards across `.await` (RSK-1003).

[CONTRACT: CTR-2602] Type-Safe Identifiers (No Raw `String`/`Uuid` for IDs).
- REJECT IF: distinct ID domains share the same primitive type in public APIs (mix-up risk).
- ENFORCE BY: newtypes (`struct ProcessId(Uuid);`) + `FromStr/TryFrom` for parsing; keep constructors validated.

[CONTRACT: CTR-2603] Construction Is Validated (Builders/Typestate).
- APPLY: CTR-1205.
- REJECT IF: invalid states are constructible in safe code.

[CONTRACT: CTR-2604] Secrets Use Secret Types (Non-Loggable by Default).
- REJECT IF: secrets (tokens/keys/passwords) are stored in `String`, `Vec<u8>`, or types that `Debug`/`Display` the value.
- ENFORCE BY: `secrecy::SecretString`/`SecretVec` + `ExposeSecret` only at the boundary; keep secrets out of structured logs.

[CONTRACT: CTR-2605] State Machines Are Explicit Enums With Total Transition Logic.
- REJECT IF: state is modeled as booleans/ints without a closed set of states and explicit transitions.
- ENFORCE BY: enum state machine + exhaustive matches; helper predicates (`is_running`, `has_exited`) are `#[must_use]` (CTR-0704).

[CONTRACT: CTR-2606] Errors Are Typed and Actionable.
- APPLY: CTR-0701/0703.
- ENFORCE BY: `thiserror`-derived enums are acceptable for internal/public error typing; avoid stringly-typed branching.

[CONTRACT: CTR-2607] State Files Use Atomic Write Protocol.
- APPLY: CTR-1502.
- ENFORCE BY: write-to-temp + rename; fsync when durability is required; preserve permissions/ownership.

[CONTRACT: CTR-2608] Retry Loops Have Backoff and a Circuit Breaker.
- REJECT IF: retry loops can spin indefinitely or amplify failures (restart loops, external calls).
- ENFORCE BY: exponential backoff + cap + "circuit open" state with cooldown; record failure history; require explicit reset conditions.

[CONTRACT: CTR-2609] Paths Are Treated as an Input Boundary.
- REJECT IF: untrusted identifiers are joined into paths without strict validation (path traversal).
- ENFORCE BY: validate/parse IDs into constrained types; never `join(user_input)`; prefer mapping IDs to safe filenames.

[CONTRACT: CTR-2610] Canonical Representation Is Defined at Boundaries.
- REJECT IF: critical values have multiple semantic encodings (e.g., "null hash" as `None` vs `[0;32]`) without normalization.
- ENFORCE BY: one canonical encoding; normalize at boundary (parse/serialize); test round-trips.

[CONTRACT: CTR-2611] Sensitive Directories Are Created With Restrictive Permissions at Create-Time.
- REJECT IF: sensitive dirs are created with default perms then chmodded (TOCTOU window).
- ENFORCE BY: on Unix, `DirBuilderExt::mode(0o700)`; on files, ensure 0600 where applicable.

[CONTRACT: CTR-2612] Deterministic Ordering Before Hashing/Signing.
- REJECT IF: signatures/hashes depend on iteration order of maps/sets or input collection order.
- ENFORCE BY: sort by a stable key before serialization; specify ordering in the contract.

[CONTRACT: CTR-2613] Portability Is Enforced With `#[cfg]` Gates + CI Coverage.
- APPLY: INV-2001 and RSK-2001.
- REJECT IF: platform-specific code is not gated and tested in the build matrix.

[CONTRACT: CTR-2614] Backend Implementations Must Match Edge-Case Semantics.
- REJECT IF: memory/mock backends silently accept states the persistent backend rejects (or vice versa).
- ENFORCE BY: shared conformance tests; identical overwrite/error semantics; fuzz/property tests for equivalence.

[INVARIANT: INV-2615] Counters and Attempts Are Monotonic.
- APPLY: INV-2502 for monotonic counter semantics.
- REJECT IF: restart attempts / sequence numbers can decrease or reset across terminal states.
- ENFORCE BY: store last-seen attempt in terminal states; require `attempt > previous`.

[CONTRACT: CTR-2616] Hash Chain Integrity.
- REJECT IF: hash chains do not commit to ALL related state (lifecycle events, data payloads).
- ENFORCE BY: combine all relevant event hashes into the final committed hash.
[PROVENANCE] APM2 Implementation Standard.

## Anti-Patterns (Lessons Learned)

### ANTI-1

[HAZARD: RSK-2616] Shell Argument Escaping for Complex Strings.
- REJECT IF: prompts/markdown/complex strings are passed as shell/CLI arguments.
- ENFORCE BY: write to a temp file and redirect stdin; quote paths using the project’s shell escaping helpers; prefer `std::process::Command` with explicit argv when possible.

### ANTI-2

[HAZARD: RSK-2617] Predictable Temp File Names (`temp_dir().join(format!(...))`).
- REJECT IF: temp paths are derived from PID/time/user input in shared temp directories.
- ENFORCE BY: `tempfile::NamedTempFile` / `TempDir` (random name, 0600/0700, RAII cleanup); persist only when necessary and then clean up explicitly.

### ANTI-3

[HAZARD: RSK-2618] Incomplete Struct/Enum Field Updates.
- REJECT IF: adding a field/variant does not update constructors, matches, serialization, and invariants.
- ENFORCE BY: exhaustive matches (avoid `_ =>` for owned enums); clippy patterns; tests that construct and round-trip every variant.
