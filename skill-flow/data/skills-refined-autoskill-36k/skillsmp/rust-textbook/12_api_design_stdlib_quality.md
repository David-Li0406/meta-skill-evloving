# 12 — API Design (Contract-First, Misuse-Resistant)

[CONTRACT: CTR-1201] Public API Contract Must Be Explicit.
- Contract includes: invariants, error semantics, panic policy, allocation behavior, thread-safety (`Send`/`Sync`), cfg/feature effects.
- REJECT IF: contract depends on implicit conventions or "obvious usage."
- ENFORCE BY: validated constructors; private fields; narrow mutation surface; doctests for non-obvious protocols.
[PROVENANCE] Rust Reference: visibility and trait/impl semantics; public behavior stability is a library contract.

[CONTRACT: CTR-1202] Borrowed vs Owned Discipline.
- REJECT IF: read-only APIs force cloning/allocation.
- REJECT IF: getters allocate, lock, or perform I/O without an explicit contract.
- ENFORCE BY: borrowed views (`&[T]`, `&str`, iterators); explicit `to_owned`/`into_*` APIs for ownership transfer; `Cow` when dual-mode is required.
[PROVENANCE] std conventions for borrowed views and `Cow`.

[HAZARD: RSK-1201] Hidden Allocation in Hot Paths.
- TRIGGER: `clone()` in loops, `format!`, `to_string()`, collecting iterators, implicit `Vec` growth.
- FAILURE MODE: latency regressions; allocator contention; tail amplification.
- REJECT IF: hidden allocations are introduced in perf-critical APIs without explicit justification.
- ENFORCE BY: pass borrowed data; preallocate; expose capacity controls; use `Cow` or small-string optimization types only with policy.
[PROVENANCE] std allocation behavior is explicit in type docs; allocation is a contract surface for foundational crates.
[VERIFICATION] Benchmarks for hot-path changes; allocation profiling in CI/perf runs where available.

[CONTRACT: CTR-1203] Visibility Enforces Invariants.
- REJECT IF: invariant-bearing types expose `pub` fields.
- REJECT IF: representation leaks prevent future changes (private types in public bounds, public enums with unstable variants).
- ENFORCE BY: `pub(crate)` internal wiring; private fields + constructors; sealed traits for extension control.
[PROVENANCE] Rust Reference: visibility rules; trait coherence impacts are observable.

[CONTRACT: CTR-1204] Feature Flags Are Additive and Tested.
- REJECT IF: a feature flips semantics without an explicit contract statement and dedicated tests.
- REJECT IF: cfg-dependent public API differs across feature sets without deliberate design.
- ENFORCE BY: additive capabilities; feature matrix in CI; avoid "surprise std" features.
[PROVENANCE] Cargo feature resolution; Rust Reference: cfg removes code from the program.
[VERIFICATION] CI: defaults, `--no-default-features`, `--all-features`, curated combinations.

[HAZARD: RSK-1202] SemVer Breaks Without Signature Changes.
- TRIGGER: new blanket impls; bound tightening; auto-trait changes; panic behavior changes; error variant changes used for matching.
- REJECT IF: such changes land without an explicit semver decision.
- ENFORCE BY: semver-check tooling where applicable; downstream compatibility tests for ecosystem crates.
[PROVENANCE] Rust Reference: implementations and overlap; method resolution depends on impl set.

[CONTRACT: CTR-1205] Construction Protocols Must Be Validated.
- REJECT IF: builders/setters allow invalid intermediate or final states unless invalidity is unobservable and internally contained.
- REJECT IF: builder validation only checks identifiers (IDs) but skips logic-affecting specs/configs.
- ENFORCE BY: builder with `build()` validation; typestate when ordering matters; `TryFrom`/`FromStr` for parsing constructors.
[PROVENANCE] Rust type system supports invalid-state elimination by construction; invalid states must not be representable at safe boundaries.

```rust
// Pattern: Builder Validation Scope
impl SpawnConfigBuilder {
    pub fn build(self) -> Result<SpawnConfig, ConfigError> {
        validate_id(&self.work_id, "work_id")?;
        // Vital: Validate specs/configs, not just IDs!
        validate_goal_spec(&self.goal_spec)?;
        Ok(SpawnConfig { ... })
    }
}
```

[CONTRACT: CTR-1206] Authoritative Apply Pattern.
- REJECT IF: security-sensitive configurations can be partially or inconsistently applied.
- ENFORCE BY: a single authoritative function that consumes a config and returns a fully prepared resource (e.g., `Command`, `Socket`).
[PROVENANCE] APM2 Implementation Standard.

```rust
// Pattern: Authoritative Apply
pub fn command_with_sandbox(mut cmd: Command, profile: &SandboxProfile) -> Result<Command, Error> {
    apply_sandbox_controls(&mut cmd, profile)?;
    Ok(cmd)
}
```

## References (Normative Anchors)

- std `Cow`: https://doc.rust-lang.org/std/borrow/enum.Cow.html
- Rust Reference: Implementations: https://doc.rust-lang.org/reference/items/implementations.html
- Rust Reference: Conditional compilation: https://doc.rust-lang.org/reference/conditional-compilation.html
