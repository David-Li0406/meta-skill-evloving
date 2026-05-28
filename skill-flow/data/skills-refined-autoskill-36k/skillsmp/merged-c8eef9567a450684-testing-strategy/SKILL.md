---
name: testing-strategy
description: Use this skill when you need to implement testing strategies, unit/integration tests, TDD, or test coverage.
---

# Testing Strategy Skill

## Applicable Scope
- Rust unit/integration testing
- Tauri command and service layer testing
- Frontend critical process validation

## Critical Rules
- Prioritize adding tests when behavior changes
- Use `#[tokio::test]` for asynchronous tests
- Execute frontend test commands only when scripts are present

## Rust Test Template
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn should_sum_materials() {
        let total = 10.0 + 20.0;
        assert_eq!(total, 30.0);
    }
}
```

## Common Commands
```bash
cargo test
cargo test --all
```

## Frontend Validation
- If no test scripts are available, run `npm run lint` and perform manual testing of critical processes
- For important interactions, provide repeatable steps

## TDD Process
1. Write a failing test
2. Implement the minimal code to pass the test
3. Refactor while keeping the tests passing

## Checklist
- [ ] Behavior changes have corresponding tests or clear manual testing steps
- [ ] Asynchronous tests use `tokio::test`
- [ ] Run `cargo test` successfully