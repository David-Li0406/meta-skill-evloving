# 25 — Time, Monotonicity, Determinism (Clock Protocols)

[CONTRACT: CTR-2501] Time Is an External Input.
- REJECT IF: core logic reads wall-clock time implicitly (`SystemTime::now`) without an explicit contract.
- ENFORCE BY: inject time sources (clock trait, parameters) at boundaries; treat timestamps as data, not ambient state.
[PROVENANCE] std `SystemTime` is a wall-clock abstraction; behavior depends on the environment.

[INVARIANT: INV-2501] Duration Measurement Uses a Monotonic Clock.
- REJECT IF: durations/timeouts are measured using wall-clock time.
- ENFORCE BY: `Instant` (monotonic) for elapsed time and timeouts; convert to wall-clock only for display/audit when required.
[PROVENANCE] std docs: `Instant` is monotonic; `SystemTime` is not guaranteed monotonic.
[VERIFICATION] Tests with a fake monotonic clock; property tests for timeout state machines.

[HAZARD: RSK-2501] `SystemTime` Can Move Backward or Jump Forward.
- TRIGGER: using `SystemTime` for elapsed time, ordering, or timeout logic.
- FAILURE MODE:
  - negative/failed `duration_since` computations
  - premature expiry or unbounded waits
  - broken ordering invariants ("time went backwards")
- REJECT IF: code assumes `SystemTime` monotonicity.
- ENFORCE BY: handle `duration_since` errors explicitly; use `Instant` for elapsed; treat wall-clock as untrusted input.
[PROVENANCE] std docs: `SystemTime` can be adjusted by the OS (NTP/manual changes); `duration_since` can error.
[VERIFICATION] Tests that simulate backward/forward jumps in a fake wall clock.

[HAZARD: RSK-2502] Cross-Process Ordering Based on Wall-Clock Time.
- FAILURE MODE: distributed ordering drift; replay/causality bugs; inconsistent timeout behavior across nodes.
- REJECT IF: protocol correctness depends on comparing wall-clock timestamps across nodes without an explicit clock synchronization assumption and mitigation strategy.
- ENFORCE BY:
  - define ordering via protocol sequence numbers, logical clocks, or server-assigned monotonic counters
  - use time only as advisory metadata unless synchronization is part of the contract
[PROVENANCE] `SystemTime` carries no global correctness guarantee across machines; ordering requires protocol-defined semantics.
[VERIFICATION] Simulation tests with skewed clocks; property tests for ordering invariants under skew.

[INVARIANT: INV-2502] Protocol Counters and Attempts Are Monotonic.
- REJECT IF: restart attempts / sequence numbers can decrease or reset across terminal states, restarts, or replays.
- ENFORCE BY: persist last-seen counter in terminal states; require strict increase (`next > previous`); never derive ordering counters from wall-clock time.
[VERIFICATION] Reducer/state-machine tests that cover terminal->restart transitions; crash/restart simulation with persisted state; property tests for monotonicity.

[CONTRACT: CTR-2502] Timestamp Semantics Must Be Specified.
- REJECT IF: an API accepts/returns "timestamp" without specifying:
  - time source (wall-clock vs monotonic)
  - epoch/units/serialization format
  - monotonicity expectations
  - clock-skew handling (if distributed)
- ENFORCE BY: distinct types (`WallTime`, `MonoTime`, `Duration`); explicit serialization format; explicit conversion boundaries.
[PROVENANCE] `Instant` is not serializable across processes; `SystemTime` serialization requires an epoch and format contract.

[HAZARD: RSK-2503] Mixed Clock Domains (`Instant` + `SystemTime`) Without a Boundary.
- FAILURE MODE: incorrect comparisons; invalid conversions; latent bugs under suspend/resume and clock adjustments.
- REJECT IF: code compares or subtracts values from different clock domains without an explicit conversion contract.
- ENFORCE BY: keep clock domains separate in types and modules; convert only at defined boundaries.
[PROVENANCE] std types represent different semantics; only `Duration` is a clock-independent value.

[HAZARD: RSK-2504] Defensive Duration and Interval Handling.
- OS clocks can jump backwards, and intervals can be zero.
- REJECT IF: `duration_since()` is used without the `checked_` variant.
- REJECT IF: modulo operations on intervals lack a zero-guard.
- ENFORCE BY: use `checked_duration_since().unwrap_or(Duration::ZERO)`; guard division/modulo by checking `interval > 0`.
[PROVENANCE] std Instant::duration_since (can panic on some platforms/versions if time goes backwards); APM2 Implementation Standard.
[VERIFICATION] Code audit for unchecked duration math and zero-interval modulo.

[CONTRACT: CTR-2503] Deterministic Tests Require a Controllable Clock.
- REJECT IF: tests depend on real time passing (sleep-based flakiness) when a controllable clock is feasible.
- ENFORCE BY: fake clock injection; deterministic schedulers; time-free unit tests with explicit durations.
[PROVENANCE] Wall-clock time introduces nondeterminism; deterministic verification requires controlled inputs.
[VERIFICATION] Property tests for time-dependent logic; runtime-specific time control APIs when available.

## References (Normative Anchors)

- std `SystemTime`: https://doc.rust-lang.org/std/time/struct.SystemTime.html
- std `Instant`: https://doc.rust-lang.org/std/time/struct.Instant.html
- std `Duration`: https://doc.rust-lang.org/std/time/struct.Duration.html
