---
name: python
description: "Develop Python applications using modern patterns, uv, functional-first design, and production-first practices. Activate when working with .py files, pyproject.toml, uv commands, or user mentions Python, itertools, functools, pytest, mypy, ruff, async, or functional programming patterns."
---

# Python Development

Functional-first, production-first Python 3.14+ with uv, type safety, immutability.

## Activation Triggers
- .py files, pyproject.toml, uv commands
- Python, typing, asyncio, pytest, mypy, ruff, dataclasses, itertools, functools

## Workflow

```
1. MODEL    -> types, invariants, boundaries
2. COMPOSE  -> pure functions, pipelines, small modules
3. VALIDATE -> parse at edges, return errors early
4. TEST     -> pytest, fixtures, async tests
5. HARDEN   -> ruff + format + mypy + regression tests
```

## Core Principles
- Functional core, imperative shell
- Immutability by default; copy-on-write
- Explicit types and error paths
- Small composable units
- Production defaults: logging, config, timeouts, retries

## When to Use
- New or refactored Python modules
- Async I/O, data pipelines, CLI tooling
- Type-heavy APIs, validation, parsing
- Test strategy or flaky tests

## When Not to Use
- Non-Python runtimes
- Browser E2E tests (use Playwright)

## Quick Start

```bash
uv init my-project && cd my-project
uv add requests pydantic httpx
uv add --dev pytest pytest-asyncio mypy ruff

uv run python script.py
uv run pytest
```

## Quality Gates

```bash
uv run ruff check src/
uv run ruff format --check src/
uv run mypy src/
uv run pytest
```

## Must / Must Not
- MUST: type hints on public APIs; validate inputs at boundaries; prefer pathlib
- MUST NOT: mutable default args; bare except; mix sync/async in one call chain

## Notes

Core patterns, async examples, and anti-patterns live in `reference.md` and the cookbooks.

## Research Tools

```
# gh search code for real-world examples
gh search code "asyncio.TaskGroup(" --language=python
gh search code "class.*Protocol):" --language=python
gh search code "async with httpx.AsyncClient(" --language=python
```

## References

- [reference.md](reference.md) - Data structures, best practices, idioms, error handling
- [patterns.md](cookbook/patterns.md) - Functional patterns
- [async.md](cookbook/async.md) - Async/await deep dive
- [testing.md](cookbook/testing.md) - pytest patterns & fixtures
- [design-patterns.md](cookbook/design-patterns.md) - Builder, DI, Factory, Strategy, Repository
- [modern.md](cookbook/modern.md) - Python 3.8-3.14 key features
