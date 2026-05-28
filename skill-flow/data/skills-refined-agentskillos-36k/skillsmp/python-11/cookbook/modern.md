# Modern Python Cookbook

Key features from Python 3.8 through 3.14, split by version.

## Contents
- 3.8 to 3.10: `modern-3.8-3.10.md`
- 3.11 to 3.12: `modern-3.11-3.12.md`
- 3.13 to 3.14: `modern-3.13-3.14.md`

## Quick Reference

| Version | Key Feature | Example |
|---------|-------------|---------|
| 3.8 | Walrus `:=` | `if (n := len(x)) > 10:` |
| 3.8 | Positional-only `/` | `def f(x, /):` |
| 3.9 | Dict merge `\|` | `d1 \| d2` |
| 3.9 | Built-in generics | `list[int]` |
| 3.10 | Pattern matching | `match x: case ...:` |
| 3.10 | Union `\|` | `int \| str` |
| 3.11 | Exception groups | `except* ValueError:` |
| 3.11 | TaskGroup | `async with TaskGroup():` |
| 3.12 | Type params | `def f[T](x: T):` |
| 3.12 | `type` statement | `type Alias = ...` |
| 3.13 | Free-threaded | No GIL option |
| 3.13 | `@deprecated` | Deprecation decorator |
| 3.14 | t-strings | `t"Hello {name}"` |
| 3.14 | `uuid7()` | Time-sortable UUIDs |
