---
name: rust-refactor-verify
description: Expert workflow for refactoring large Rust codebases, modularizing monolithic files, and establishing a robust quality gate using Clippy, formatting, and a comprehensive test suite (unit + integration). Use when Claude needs to: (1) Split large .rs files into modules, (2) Fix multiple Clippy warnings systematically, (3) Set up integration tests, or (4) Configure Git hooks (Husky) for quality enforcement.
---

# Rust Refactor & Verify Skill

This skill provides a systematic workflow for improving Rust codebase quality and maintainability.

## Core Workflows

### 1. Systematic Modularization
When a file (like `app.rs` or `main.rs`) exceeds 500+ lines, it should be split:
1.  **Identify Logical Boundaries**: Group fields and methods into functional areas (e.g., `state`, `ui`, `input`, `logic`).
2.  **Create Module Directory**: `mkdir src/<module_name>`.
3.  **Split Files**:
    -   `state.rs`: Struct definition and `new()` implementation.
    -   `logic.rs` / `input.rs`: Action handlers and update logic.
    -   `render.rs`: UI-specific code.
    -   `mod.rs`: Re-export common types and implement high-level `run` loop.
4.  **Fix Imports**: Update `crate::...` paths and ensure `pub` visibility where needed.
5.  **Verify**: Run `cargo check` frequently during the split.

### 2. The Quality Gate (Clippy & Fmt)
Always run the full quality suite before committing:
```bash
cargo fmt --all && cargo clippy --all-targets --all-features -- -D warnings
```
-   **systematic_fix**: Don't just fix one warning. Look for patterns (e.g., `manual_flatten` across the whole repo).
-   **idiomatic_rust**: Prefer `.clamp()`, `.map_while()`, and `impl Default` where Clippy suggests.

### 3. Testing Strategy
-   **Unit Tests**: Place in the same file within a `mod tests` block. Focus on internal logic.
-   **Integration Tests**: Place in `tests/*.rs`. Focus on public API and component interaction.
    -   *Crucial*: Always check for required environment setup (like log directories) in tests.

### 4. Git Hooks (Husky)
Enforce quality via `.husky/hooks/`:
-   **pre-commit**: `cargo test` + `cargo fmt --check` + `cargo clippy`.
-   **commit-msg**: Enforce Conventional Commits (`feat:`, `fix:`, `refactor:`, etc.).

## Best Practices
-   **Atomic Changes**: One refactor unit per commit.
-   **Regression Testing**: Run the full test suite after every module split.
-   **Avoid `as any` or `@ts-ignore` style hacks**: Use proper Rust type safety (traits, enums).

### 5. Efficient Exploration
-   **Search**: Prefer `rg` (ripgrep) over `grep`.
-   **Find**: Prefer `fd` (or `fdfind`) over `find`.
-   **Platform Agnostic**: Use standard bash-compatible flags and avoid PowerShell-specific syntax to ensure consistency across environments.
