# Refactoring Patterns Recognized

This file lists patterns that `refactor.py` attempts to recognize and safely transform.

1. Interpolation changes
   - `%` formatting -> `str.format()` -> `f-strings` (where safe)
2. Remove unused imports
   - Detect `import` or `from ... import ...` statements with zero usages in file
3. Simplify boolean expressions
   - `if x == True` -> `if x`
4. Small function extraction suggestions
   - When a contiguous block is > 20 lines and has few external locals, suggest extraction (not auto-apply)

Patterns are intentionally conservative. The skill will not rename symbols or change public APIs without explicit user approval.
