---
name: coding-best-practices
description: Use this skill when writing or editing code, tests, or Python scripts to ensure maintainability and clarity.
---

# coding-best-practices

## General Coding Practices

- Keep lines short and avoid horizontal alignment.
- Avoid adding comments; use intention-revealing names instead. Remove stale comments and docstrings that don't add value.
- Prefer stateless/pure functions, separating I/O operations from business logic.
- Aim for one level of abstraction per function and keep them short.
- If a function requires many arguments, consider using an object or splitting it into multiple functions.
- Avoid mutable global state to prevent unintended side effects.
- Prefer reusing and extending existing code, but ensure to test it thoroughly.
- Avoid unnecessary breaklines; keep related code vertically dense.

## Python-Specific Practices

- Use `isort` and `black` for formatting, installing them with pip if not already installed.
- Always add type hints, especially for non-obvious types. Prefer `|` over `Union[]` and `| None` over `Optional`.
- Run a type checker (e.g., `mypy`) and fix all errors after writing the code.
- Extract logic into staticmethods and classmethods whenever possible.
- Avoid try-except blocks that swallow exceptions; prefer logging, re-raising, or handling specific exceptions.
- Do not set up logging in libraries; leave that to the application using the library.

## Software Testing Practices

- Avoid excessive mocking; prefer simple integration tests over many mocked unit tests.
- Print local variables to stdout in tests, focusing on inputs and outputs for easier debugging.
- Validate using models (e.g., Pydantic) instead of numerous field-by-field assertions.
- Use the `tmp_path` fixture for testing file operations to ensure automatic cleanup.
- When reading Excel/CSV files, use `pd.read_excel(..., dtype=str, keep_default_na=False)` to avoid type coercion issues.
- Do not bend production code to make tests easier unless it benefits the production code itself.

## Dependencies Management

- Prefer adding dependencies without version constraints unless necessary.
- Do not use try-except for missing imports; assume users will install all needed dependencies.
- Place imports at the top of the file and use `pip install -e ./path` for local packages to avoid confusion.

## Validation Logic

- When writing validation logic, prefer early returns on errors.