# 24 — Hazard Catalog (Quick Scan; Fail-Closed)

[CONTRACT: CTR-2401] Hazard Scan Protocol.
- Step 1: identify triggered domains (unsafe, concurrency, async, parsing, FFI, cfg, macros/build).
- Step 2: map triggers to rule IDs in this catalog.
- Step 3: apply rule-specific reject conditions; reject on missing proof/verification.
- Step 4: run required tools per Chapter 17.

## Unsafe and Memory

[HAZARD: RSK-2401] `unsafe` Without Local Safety Contract.
- TRIGGER: `unsafe { ... }`, `unsafe fn`, `unsafe trait`, `unsafe impl`.
- APPLY: CTR-0901 (surface classification), CTR-0902 (`// SAFETY:` format), INV-0902 (obligation checklist).
- REJECT IF: any unsafe block lacks a `// SAFETY:` comment in post-condition form.

[HAZARD: RSK-2402] Reference Creation From Unknown Memory.
- TRIGGER: `&*ptr`, `&mut *ptr`, `slice::from_raw_parts`, `str::from_utf8_unchecked`, references to packed fields.
- APPLY: INV-0004 (reference validity), INV-0801 (alignment), RSK-0901 (invalid references), RSK-0801 (packed).
- REJECT IF: any `&T`/`&mut T` can be created without proving alignment, initialization, provenance, and aliasing exclusivity.

[HAZARD: RSK-2403] Pointer Provenance Loss.
- TRIGGER: pointer cast to integer, integer arithmetic, cast back, dereference.
- APPLY: INV-0006 (strict provenance), RSK-0902 (roundtrip hazard).
- REJECT IF: integer-derived pointers are dereferenced without provenance-preserving APIs.

[HAZARD: RSK-2404] Manual Init/Drop Primitives.
- TRIGGER: `transmute`, `mem::zeroed`, `MaybeUninit::assume_init`, `ManuallyDrop`, `ptr::read`, `Vec::set_len`, `from_raw_parts`.
- APPLY: INV-0001/0002/0008, INV-0802/0804, RSK-0903.
- REJECT IF: any checklist item in INV-0902 is unproven.

[HAZARD: RSK-1304] Ghost Key Prevention in TTL Queues.
- TRIGGER: insertion-order queues (VecDeque) used for TTL-based eviction in HashMaps.
- APPLY: RSK-1304.
- REJECT IF: queue stores only keys without timestamps for TTL-based stores.

## Drops and Panics

[HAZARD: RSK-2405] Drop Scope and Drop Order Changes.
- TRIGGER: moving `;`, changing block tails, reordering locals, refactors that alter lifetimes of temporaries.
- APPLY: RSK-0301 (semicolon), RSK-0302 (temporaries), INV-0803 (drop order).
- REJECT IF: observable drop timing can change without a compatibility decision and a regression test.

[HAZARD: RSK-2406] Panic Surface Regression.
- TRIGGER: `unwrap`, `expect`, `panic!`, `todo!`, `unreachable!`, indexing, `str` slicing.
- APPLY: CTR-0702 (panic audit), RSK-0701 (panic-as-DoS).
- REJECT IF: new reachable panic site exists on an untrusted path.

[HAZARD: RSK-2407] Panicking `Drop`.
- TRIGGER: fallible work in `Drop`, `unwrap`/indexing in `drop`.
- APPLY: RSK-0702 (panicking drop), INV-0701 (unwind safety).
- REJECT IF: `Drop::drop` can panic.

## Concurrency and Atomics

[HAZARD: RSK-2408] Relaxed Ordering Without Weak-Memory Analysis.
- TRIGGER: `Ordering::Relaxed` on non-metric atomics.
- APPLY: RSK-1001 (weak-memory reorder), CTR-1002 (atomic protocol).
- REJECT IF: `Relaxed` participates in publish/consume of non-atomic data.

[HAZARD: RSK-2409] Custom Synchronization Without Happens-Before Graph.
- TRIGGER: lock-free structures, custom locks/onces/channels, atomic state machines.
- APPLY: CTR-1003 (HB graph required), RSK-1002 (reclamation).
- REJECT IF: HB graph is absent.

[HAZARD: RSK-2504] Defensive Duration and Interval Handling.
- TRIGGER: use of `duration_since()`; modulo/division on interval variables.
- APPLY: RSK-2504.
- REJECT IF: `checked_duration_since()` is missing or intervals lack zero-guards.

## Async

[HAZARD: RSK-2410] Invariant Broken Across `.await`.
- TRIGGER: `.await` inside a critical section; shared state mutated before restore; guards held across await.
- APPLY: INV-1101 (cancellation safety), RSK-1101 (locks across await).
- REJECT IF: any `.await` occurs while invariants are temporarily violated.

[HAZARD: RSK-2411] Multi-Branch Selection Corrupts Shared State.
- TRIGGER: `select`-style constructs; branch-local work mutates shared state before winning.
- APPLY: RSK-1102 (lateral state corruption).
- REJECT IF: losing branch cancellation can leave shared state partially updated.

[CONTRACT: CTR-1104] Cancellation-Safe State Mutation.
- TRIGGER: idempotency markers set alongside external side effects (DB/File persist).
- APPLY: CTR-1104.
- REJECT IF: idempotency marker is set BEFORE the side effect completes.

## cfg, Features, Build Matrix

[HAZARD: RSK-2412] Dark Code (Untested Configurations).
- TRIGGER: `#[cfg]`, feature-gated modules, platform-specific branches.
- APPLY: INV-2001 (cfg rewriting), RSK-2001 (dark code rot), CTR-2002 (API stability across cfg).
- REJECT IF: new branches lack CI coverage.

[HAZARD: RSK-2413] `cfg_attr` Alters ABI/Layout/Lints Per Configuration.
- TRIGGER: `cfg_attr` applying `repr`, linking attributes, lint levels, `path`, `inline`.
- APPLY: RSK-2002.
- REJECT IF: configuration-specific semantics lack dedicated tests.

[HAZARD: RSK-2414] `cfg!()` Misused as a Compilation Gate.
- APPLY: RSK-2003.
- REJECT IF: `cfg!()` guards code that must not exist on unsupported targets.

## Parsing, I/O, and Resource Caps

[HAZARD: RSK-2415] Untrusted Lengths and Overflow.
- TRIGGER: `len * size_of::<T>()` from inputs; unbounded `reserve`; recursion without depth limits.
- APPLY: RSK-1601 (parsing DoS), RSK-1302 (size math), RSK-1901 (resource exhaustion).
- REJECT IF: boundary code lacks explicit caps and checked arithmetic.

[INVARIANT: INV-2401] I/O Partial Progress Handling.
- APPLY: INV-1601.
- REJECT IF: protocol code assumes full reads/writes without looping or framing.

## Text and Encoding

[HAZARD: RSK-2416] Invalid UTF-8 `str` Construction.
- TRIGGER: `from_utf8_unchecked`, `str::from_raw_parts`-style patterns, FFI string conversions.
- APPLY: INV-1401 (UTF-8 validity), INV-2301 (FFI pointer validity).
- REJECT IF: UTF-8 validity is not proven at the boundary.

[HAZARD: RSK-2417] Normalization/Confusable Risk in Security Comparisons.
- APPLY: RSK-1402.
- REJECT IF: security-relevant comparisons occur without explicit normalization/case policy.

## Build-Time Execution Surfaces

[HAZARD: RSK-2418] Build Scripts and Proc Macros Expand the Trusted Computing Base.
- TRIGGER: `build.rs`, proc-macro crates, code generation.
- APPLY: RSK-0202/0203 (build surfaces), RSK-2204 (build-time execution).
- REJECT IF: network I/O or ambient environment dependence exists without declared inputs.

## FFI

[HAZARD: RSK-2419] ABI and Unwind Contract Violations.
- TRIGGER: `extern "C"` boundaries; missing `catch_unwind`; missing `"C-unwind"` where required.
- APPLY: CTR-2303 (unwinding contract), INV-2301 (pointer validity).
- REJECT IF: unwind can cross a non-unwinding ABI boundary.

## Verification Escalation

[VERIFICATION] Mandatory Gates by Trigger.
- Unsafe/raw pointers/layout: Miri (RSK-2401..2404).
- Custom sync/atomics: Loom (RSK-2408..2409).
- Parsing/untrusted inputs: fuzzing + property tests (RSK-2415).
- cfg/features: build matrix (`--no-default-features`, defaults, `--all-features`, curated) (RSK-2412..2414).
- FFI: integration tests that exercise the boundary under `panic=unwind` where applicable (RSK-2419).
