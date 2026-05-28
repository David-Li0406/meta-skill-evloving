## Common Errors

**Impact:** MEDIUM

Recognize common errors like missing semicolons, undefined variables (often missing `lib` argument), or infinite recursion in `rec` sets.

**Incorrect:**

**Infinite Recursion**

```nix
rec {
  # Self-reference cycle
  x = y;
  y = x;
}
```

**Correct:**

**Broken Cycle**

```nix
{
  x = "value";
  y = "value"; # Or use let binding
}
```
