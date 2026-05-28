# Python Style Guide (Opinionated subset)

This file contains compact style guidance used by the python-refactor skill. It's intentionally small — the skill treats these as heuristics, not hard rules.

- Prefer f-strings over `%` or `str.format()` for string interpolation.
- Keep functions under ~80-120 lines; consider extraction when longer.
- Prefer single responsibility per function.
- Remove unused imports and unused local variables when detected.
- Use explicit exception types rather than bare `except:`.
- Prefer list/dict comprehensions where readable.

Run tests and verify behavior after automated changes.
