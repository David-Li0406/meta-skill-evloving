# Pop-CLI Final Review Checklist

Detailed checklist for comprehensive code review in the pop-cli project.

## Table of Contents

1. [Code Quality](#code-quality)
2. [CLI Patterns](#cli-patterns)
3. [Feature Gates](#feature-gates)
4. [Testing](#testing)
5. [Documentation](#documentation)
6. [Dependencies](#dependencies)
7. [Security](#security)
8. [Performance](#performance)
9. [Git & PR Standards](#git--pr-standards)
10. [Crate-Specific Checks](#crate-specific-checks)

---

## Code Quality

### Error Handling

```rust
// BAD - panic in library code
let value = config.get("key").unwrap();

// GOOD - propagate with context
let value = config.get("key")
    .ok_or_else(|| anyhow::anyhow!("Missing required config key"))?;

// GOOD - thiserror for structured errors
#[derive(thiserror::Error, Debug)]
pub enum ContractError {
    #[error("Failed to build contract at {path}: {source}")]
    BuildFailed {
        path: PathBuf,
        #[source]
        source: std::io::Error,
    },
}
```

**Checklist:**
- [ ] No `unwrap()` in `pop-contracts`, `pop-chains`, `pop-common` crates
- [ ] `unwrap()`/`expect()` in `pop-cli` only at top-level CLI entry points
- [ ] All `?` propagations have sufficient context
- [ ] Error messages describe what failed AND include relevant data
- [ ] Custom error types use `thiserror` derive

### Code Style

**Formatting:**
- Hard tabs (`.rustfmt.toml` configured)
- Max line width: 100 characters
- Nightly rustfmt features enabled

**Naming:**
- Types: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `SCREAMING_SNAKE_CASE`
- Feature flags: `kebab-case` in Cargo.toml

**Checklist:**
- [ ] `cargo +nightly fmt --all -- --check` passes
- [ ] No trailing whitespace
- [ ] Consistent import ordering (std, external, internal)
- [ ] No dead code warnings

---

## CLI Patterns

### Testable CLI Interactions

```rust
// BAD - direct cliclack calls (not testable)
pub async fn execute() -> Result<()> {
    cliclack::intro("Starting...")?;
}

// GOOD - accept Cli trait for testability
pub async fn execute(cli: &mut impl Cli) -> Result<()> {
    cli.intro("Starting...")?;
}
```

**Checklist:**
- [ ] All commands accept `&mut impl Cli` parameter
- [ ] No direct `cliclack::` calls in command logic
- [ ] `MockCli` tests verify prompts and outputs
- [ ] Interactive prompts have sensible defaults for non-interactive mode

### User Feedback

```rust
// Use appropriate feedback methods
cli.intro("Building contract")?;           // Start of workflow
cli.info("Compiling...")?;                  // Progress info
cli.warning("Using default config")?;       // Non-critical notice
cli.success("Contract built")?;             // Operation succeeded
cli.error("Build failed")?;                 // Operation failed
cli.outro("Done!")?;                        // End of workflow
```

**Checklist:**
- [ ] Long operations show progress (spinner/messages)
- [ ] Errors are user-friendly (not raw Rust errors)
- [ ] Success messages confirm what was done
- [ ] Warnings explain implications and alternatives

### Serialization for Telemetry

```rust
#[derive(Serialize)]
pub struct BuildArgs {
    pub profile: String,
    #[serde(skip_serializing)]  // Don't send paths
    pub path: Option<PathBuf>,
    #[serde(skip_serializing)]  // Don't send sensitive data
    pub signing_key: Option<String>,
}
```

**Checklist:**
- [ ] Command args derive `Serialize` for telemetry
- [ ] `#[serde(skip_serializing)]` on paths, secrets, large data
- [ ] No PII or sensitive data in telemetry

---

## Feature Gates

### Feature Configuration

```rust
// Correct feature gating
#[cfg(feature = "chain")]
pub mod bench;

#[cfg(any(feature = "chain", feature = "contract"))]
pub mod up;

// Feature-specific dependencies in Cargo.toml
[features]
chain = ["pop-chains"]
contract = ["pop-contracts"]
default = ["chain", "contract", "telemetry"]
```

**Checklist:**
- [ ] New modules properly gated with `#[cfg(feature = "...")]`
- [ ] Feature combinations tested (chain-only, contract-only, both)
- [ ] Dependencies are feature-gated when appropriate
- [ ] Default features make sense for typical users
- [ ] No circular feature dependencies

### Workspace Dependencies

```toml
# In workspace Cargo.toml - define version once
[workspace.dependencies]
tokio = { version = "1.40", features = ["full"] }

# In crate Cargo.toml - inherit from workspace
[dependencies]
tokio = { workspace = true }
```

**Checklist:**
- [ ] New dependencies added to workspace `[workspace.dependencies]`
- [ ] Crate `Cargo.toml` uses `workspace = true`
- [ ] No duplicate version specifications

---

## Testing

### Unit Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_valid_input() {
        let result = parse_address("5GrwvaEF...");
        assert!(result.is_ok());
    }

    #[test]
    fn rejects_invalid_input() {
        let result = parse_address("invalid");
        assert!(matches!(result, Err(ParseError::InvalidFormat(_))));
    }
}
```

**Checklist:**
- [ ] Tests cover happy path and error cases
- [ ] Edge cases tested (empty input, boundary values)
- [ ] Test names describe what they verify
- [ ] No `#[ignore]` without documented reason

### Integration Tests

```rust
// In tests/contract.rs
#[cfg(all(feature = "contract", feature = "integration-tests"))]
mod contract_tests {
    #[tokio::test]
    async fn build_and_deploy_contract() {
        // Full workflow test
    }
}
```

**Checklist:**
- [ ] New commands have integration tests in `crates/pop-cli/tests/`
- [ ] Tests use `MockCli` for user interactions
- [ ] Async tests use `#[tokio::test]`
- [ ] Integration tests feature-gated with `integration-tests`

### MockCli Usage

```rust
#[tokio::test]
async fn prompts_for_confirmation() {
    let mut cli = MockCli::new()
        .expect_intro("Deploy contract")
        .expect_confirm("Proceed?", true)
        .expect_success("Deployed!");

    deploy(&mut cli).await.unwrap();
    cli.verify();  // Ensures all expected calls occurred
}
```

---

## Documentation

### Doc Comments

```rust
/// Builds a smart contract from the given path.
///
/// # Arguments
/// * `path` - Path to contract directory containing Cargo.toml
/// * `release` - If true, builds with optimizations
///
/// # Errors
/// Returns error if cargo-contract is not installed or build fails.
///
/// # Example
/// ```no_run
/// let artifact = build_contract(Path::new("./my_contract"), true)?;
/// ```
pub fn build_contract(path: &Path, release: bool) -> Result<Artifact> {
```

**Checklist:**
- [ ] All public items have `///` doc comments
- [ ] Complex functions include `# Arguments`, `# Errors`, `# Example`
- [ ] `cargo doc --no-deps` builds without warnings
- [ ] Links to related types use `[Type]` syntax

### README & CHANGELOG

**Checklist:**
- [ ] New features documented in README if user-facing
- [ ] CHANGELOG.md entry added under "Unreleased"
- [ ] Breaking changes clearly marked
- [ ] Migration guide provided for breaking changes

---

## Dependencies

### Security

```bash
# Check for known vulnerabilities
cargo deny check advisories

# Check for unmaintained crates
cargo deny check bans
```

**Checklist:**
- [ ] No security advisories in dependencies
- [ ] Dependencies are actively maintained
- [ ] Minimum necessary permissions (no `*` feature wildcards)

### Version Requirements

**Checklist:**
- [ ] MSRV (1.91.1) compatibility maintained
- [ ] `Cargo.lock` updated and committed
- [ ] No yanked crate versions

---

## Security

### Input Validation

```rust
// Validate external input at boundaries
pub fn execute_command(user_input: &str) -> Result<()> {
    // BAD - shell injection
    let output = Command::new("sh")
        .arg("-c")
        .arg(format!("echo {}", user_input))
        .output()?;

    // GOOD - use args properly
    let output = Command::new("echo")
        .arg(user_input)  // Properly escaped
        .output()?;
}
```

**Checklist:**
- [ ] No shell injection vulnerabilities
- [ ] User input sanitized before use
- [ ] File paths validated (no path traversal)
- [ ] URLs validated before fetching

### Secrets & Credentials

**Checklist:**
- [ ] No hardcoded API keys, passwords, or secrets
- [ ] Secrets read from environment or secure config
- [ ] Passwords masked in CLI output
- [ ] No secrets in telemetry or logs

---

## Performance

### Async Patterns

```rust
// BAD - blocking in async context
async fn fetch_data() {
    std::thread::sleep(Duration::from_secs(1));  // Blocks!
}

// GOOD - use async sleep
async fn fetch_data() {
    tokio::time::sleep(Duration::from_secs(1)).await;
}

// GOOD - spawn blocking work
async fn heavy_computation() {
    tokio::task::spawn_blocking(|| {
        expensive_sync_work()
    }).await?;
}
```

**Checklist:**
- [ ] No blocking calls in async functions
- [ ] `tokio::spawn_blocking` for CPU-heavy work
- [ ] Reasonable timeouts on network requests
- [ ] Background tasks don't block CLI

### Resource Management

**Checklist:**
- [ ] Temp files cleaned up on success AND failure
- [ ] Port conflicts handled gracefully
- [ ] Docker resources released properly
- [ ] Large allocations avoided where possible

---

## Git & PR Standards

### Commit Messages

```
feat(contracts): add workspace build support

Enables building all contracts in a Cargo workspace with a single command.
Previously required building each contract individually.

Closes #860

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Types:**
| Type | Use For |
|------|---------|
| `feat` | New functionality |
| `fix` | Bug fixes |
| `refactor` | Code restructuring (no behavior change) |
| `docs` | Documentation only |
| `test` | Test additions/changes |
| `ci` | CI/CD changes |
| `chore` | Maintenance (deps, configs) |

**Scopes:**
- `cli` - pop-cli crate
- `contracts` - pop-contracts crate
- `chains` - pop-chains crate
- `common` - pop-common crate
- `telemetry` - pop-telemetry crate
- Or specific command: `build`, `up`, `call`, `new`, `bench`, `test`

### PR Guidelines

**Checklist:**
- [ ] PR title follows conventional commit format
- [ ] Description explains what and why
- [ ] Related issues linked
- [ ] All CI checks passing
- [ ] No unrelated changes included
- [ ] Rebased on latest main (no merge commits)

---

## Crate-Specific Checks

### pop-cli

- [ ] Commands registered in `commands/mod.rs`
- [ ] Help text accurate and helpful
- [ ] Subcommands properly nested
- [ ] Exit codes meaningful (0 success, non-zero failure)

### pop-contracts

- [ ] Contract metadata parsing handles all versions
- [ ] Build artifacts discovered correctly
- [ ] Workspace contracts supported
- [ ] cargo-contract version compatibility checked

### pop-chains

- [ ] Chain specs generated correctly
- [ ] Network deployment handles port conflicts
- [ ] zombienet integration stable
- [ ] Runtime versions detected properly

### pop-common

- [ ] Git operations handle auth failures gracefully
- [ ] Docker availability checked before use
- [ ] Binary caching works across platforms
- [ ] Template sources validated

---

## Quick Commands Reference

```bash
# Full validation suite
cargo +nightly fmt --all -- --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --workspace
cargo test --features integration-tests
cargo doc --no-deps
cargo deny check

# Fix formatting
cargo +nightly fmt --all

# Update dependencies
cargo update
cargo deny check advisories
```
