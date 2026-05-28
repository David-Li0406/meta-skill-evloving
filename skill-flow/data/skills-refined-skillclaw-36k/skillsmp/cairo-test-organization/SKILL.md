---
name: cairo-test-organization
description: Explain Cairo test organization for unit vs integration tests, tests directory layout, and shared helpers; use when a request involves structuring tests across files or crates in Cairo.
---

# Cairo Test Organization

## Overview
Explain how to structure unit and integration tests in Cairo projects.

## Quick Use
- Read `references/test-organization.md` before answering.
- Put unit tests alongside code in `src` with `#[cfg(test)]`.
- Put integration tests in a top-level `tests/` directory.

## Response Checklist
- Unit tests can access private functions via module scoping.
- Integration tests compile as separate crates per file and use the public API.
- Use `tests/lib.cairo` to make the tests folder a single crate with shared helpers.

## Example Requests
- "Where do integration tests live in Cairo projects?"
- "How do I share helpers across integration tests?"
- "Can unit tests call private functions?"

## Cairo by Example
- [Testing](https://cairo-by-example.xyz/testing)
- [Unit testing](https://cairo-by-example.xyz/testing/unit_testing)
- [Integration testing](https://cairo-by-example.xyz/testing/integration_testing)
- [Dev-dependencies](https://cairo-by-example.xyz/testing/dev_dependencies)
