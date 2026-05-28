## Inline Prefix

**Impact:** MEDIUM

When using only 1 or 2 `lib` functions, just use the `lib.` prefix inline. It's explicit and avoids the boilerplate of a let block.

**Incorrect:**

**Over-optimization**
Creating a `let inherit` block just for one usage of `mkDefault`.

**Correct:**

**Direct Access**

```nix
config.foo = lib.mkDefault "bar";
```
