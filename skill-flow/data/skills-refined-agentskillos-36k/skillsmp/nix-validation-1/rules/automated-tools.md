## Automated Tools

**Impact:** CRITICAL

Use `nixfmt`, `statix`, and `deadnix` to maintain code health. Integrate them via `treefmt` or `pre-commit` hooks to prevent bad code from entering the repo.

**Incorrect:**

**Unformatted Code**
Committing code with inconsistent indentation or unused variables (`let x = 1; in y`).

**Correct:**

**Automated Pipeline**

```bash
# Before commit
nixfmt --check .
statix check .
deadnix .
```

(Or use configured `treefmt`).
