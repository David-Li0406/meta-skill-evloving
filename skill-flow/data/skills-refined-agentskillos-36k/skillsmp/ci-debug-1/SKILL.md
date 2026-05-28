---
name: ci-debug
description: vive-specific CI debug info (jobs and local commands).
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
---

# CI Debugger (vive)

vive 固有の CI 構成とローカル再現手順。

## CI Configuration

- Workflow: `.github/workflows/ci.yml`
- Jobs:
  - `test`: `cargo test --verbose`
  - `clippy`: `cargo clippy -- -D warnings`
  - `fmt`: `cargo fmt -- --check`

## Local Reproduction

```bash
cargo test --verbose
cargo clippy -- -D warnings
cargo fmt -- --check
```
