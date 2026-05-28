---
name: run-tests
description: Run the test suite and report results
license: MIT OR Apache-2.0
---

# Run Tests

Execute the skilo test suite and analyze results.

## Test Commands

```bash
# Run all tests
cargo test

# Run tests with output
cargo test -- --nocapture

# Run a specific test
cargo test test_name

# Run tests in a specific module
cargo test skill::validator
```

## Test Organization

Tests are organized as follows:

| Location         | Description                    |
|------------------|--------------------------------|
| `src/*/tests.rs` | Unit tests inline with modules |
| `tests/`         | Integration tests              |

## Writing Tests

When adding new functionality:

1. Add unit tests for individual functions
2. Add integration tests for CLI commands
3. Use `tempfile` for tests that need filesystem access
4. Use `assert_cmd` for testing CLI behavior

## Example

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        assert!(true);
    }
}
```
