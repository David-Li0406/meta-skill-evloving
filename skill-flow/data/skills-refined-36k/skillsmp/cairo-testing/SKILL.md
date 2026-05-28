---
name: cairo-testing
description: Explain how to write and run Cairo tests, including `#[test]`, assert macros, `#[should_panic]`, `#[ignore]`, and `#[available_gas]`; use when a request involves writing or running unit tests in Cairo.
---

# Cairo Testing

## Overview
Guide writing test functions, using assertion macros, and running tests with Scarb.

## Quick Use
- Read `references/testing.md` before answering.
- Put tests in a `#[cfg(test)]` module in `src` files.
- Use the right assert macro for the expected condition.

## Response Checklist
- Add `#[test]` above each test function.
- Use `assert!`, `assert_eq!`, `assert_ne!`, or comparison macros as needed.
- Assert message arguments must be string literals, not variables (e.g., `assert!(x, "msg")` not `assert!(x, msg)`).
- Use `#[should_panic(expected: "...")]` for panic-based tests.
- Use `#[ignore]` for slow tests and `scarb test --include-ignored` when needed.
- Add `#[available_gas(n)]` for recursion or long loops.

## Example Requests
- "How do I write a basic test in Cairo?"
- "How do I assert a panic message?"
- "How do I run a single test?"

## Cairo by Example
- [Testing](https://cairo-by-example.xyz/testing)
- [Unit testing](https://cairo-by-example.xyz/testing/unit_testing)
- [Integration testing](https://cairo-by-example.xyz/testing/integration_testing)
- [Dev-dependencies](https://cairo-by-example.xyz/testing/dev_dependencies)
- [Scarb Tests](https://cairo-by-example.xyz/scarb/test)
- [Attributes: cfg](https://cairo-by-example.xyz/attribute/cfg)
