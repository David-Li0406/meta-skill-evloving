---
name: rust-coding-style
description: Rust coding style and decision defaults for API design, errors, structure, naming, ownership, async boundaries, performance tools, and testing choices. Use when writing or reviewing Rust code and when choosing between design options.
---

# Rust Coding Style

Apply these rules when writing or reviewing Rust code. Keep decisions consistent and terse.

## Examples
- "Pick an error strategy for this new Rust binary."
- "Decide API shape and module layout for this Rust crate."

## Guidelines

## Control flow and logging
- Never use a fallback branch unless explicitly instructed.
- Never ignore a `match` branch unless explicitly instructed. For unhandled events, use `tracing` with at least `warn!` and include a `{:?}` debug of the event.

## Placeholders and stubs
- When placing placeholders or stubs, use `todo!()`. Do not create empty files.

## Language
- Do not use the word "plumbing".

## Error handling
- New app: prefer `thiserror`.
- IO-only code: prefer `std::io::Result`.
- Existing `eyre`/`anyhow`: stick with it.
- New library: prefer `thiserror`.
- Within a codebase, keep the existing error crate unless you have a strong reason to change.

## API design
- Public API: return `Result<T, E>` and avoid panics.
- Prefer newtypes over type aliases for invariants.
- Use `impl Trait` in return position for iterator APIs.
- For many optional params: use a builder.
- Config load API: prefer free function `fn load(path: impl AsRef<Path>) -> Result<Config, Error>`.
- Iterator exposure: prefer `fn iter(&self) -> impl Iterator<Item = &Item>`.
- Optional config fields: use `#[serde(default)]` and concrete fields; avoid `Option<T>` in the struct.
- Validation on construction: prefer builder with `build() -> Result<Self, Error>`.

## Code structure
- Small module: use `mod.rs`; large module: use `mod/` with `mod.rs`.
- Default to feature-based grouping in Rust (e.g., `src/foo/mod.rs`).
- Only use layer-based grouping for legacy or mandated layouts.
- Use `mod.rs` to curate public APIs rather than re-exporting entire trees, unless the mods are private.

## Naming
- Use singular for a thing/type, plural for a collection/module.
- File naming: `client.rs` for a single client type, `clients/` for a collection.

## API style: free functions vs structs
- Prefer `struct` + `impl` when there is shared state, configuration, or invariants.
- Prefer struct if a function has only the struct as parameter, and tie closely to the struct's purpose.
- Prefer free functions for stateless operations.
- Avoid OOP-style class hierarchies; use traits for behavior and composition.
- Use a builder when construction has multiple stages or invariant checks.

## Ownership and lifetimes
- Prefer owning types in public APIs; borrow internally where possible.
- Avoid exposing explicit lifetimes unless they simplify the API.

## Async boundaries
- Keep async at the edges; core logic stays sync when possible.
- Prefer explicit `async fn` in public APIs; avoid boxed futures unless needed.
- Use `tokio` only when async IO or concurrency pays for the complexity.

## Performance
- Prefer `cargo criterion` over `cargo bench`.
- Use `cargo flamegraph` for CPU hotspots.
- Use `perf` + flamegraph for low-level profiling on Linux.
- Use `samply` for sampling + flamegraphs on macOS/Linux.
- Use `tokio-console` for async task/latency insight.
- Use `cargo llvm-lines` for codegen size hotspots.
- Use `cargo bloat` for binary size breakdown.

## Testing
- In-file unit tests for local behavior and edge cases.
- `tests/` for integration tests across modules/crates.
- Shell integration tests for CLI workflows.
- Smoke tests for minimal end-to-end coverage.
- Mock tests when dependencies are expensive or flaky.
- Fuzz tests for parsers, serializers, and input handling.
- Use Podman Compose for containerized integration tests.
