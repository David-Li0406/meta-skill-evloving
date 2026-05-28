---
name: ruby-style-guide
description: Ruby code style conventions. Use when writing, reviewing, or refactoring Ruby code.
---

# Ruby Style Guide

Apply these conventions when writing or modifying Ruby code.

## Guidelines

- When writing a Ruby script or CLI, always use [Thor](https://github.com/rails/thor).
- Prefer double quotes for strings; use single quotes only when the string contains double quotes, in shell commands with interpolation, or when following existing code patterns.
- Use parallel assignment for instance variables when initializing from local variables with matching names; split across two lines when assigning 3 or more.
- Indent private methods by 2 additional spaces after the `private` keyword.
- Prefer `case when` over `if elsif` for multiple conditional branches.
- Put `if` and `unless` on a separate line, except when using `return` or `raise` without arguments or with one short argument: `return if failed?`, `return false if failed?`, `raise unless succeeded?`, `raise error unless succeeded?`
- Use guard clauses for early returns.
- Use safe navigation operator (`&.`) for nil checks.
- Add a blank line after multi-line block headers before the block body.
- Use multi-line, leading-dot chaining when calling more than one method in a row.
- Prefer chaining over temporary variables when it stays readable; `then` and `tap` are often helpful.
- Prefer numbered parameters (`_1`, `_2`) for small blocks; use `it` only when numbered params don't work.
- Prefer endless method definitions for simple, single-expression methods.
