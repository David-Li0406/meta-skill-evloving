## Inherit Pattern

**Impact:** HIGH

When using 3 or more `lib` functions, use `inherit (lib) ...` in a `let` block. This keeps the scope clean while reducing verbosity.

**Incorrect:**

**Repetitive Prefixing**
Writing `lib.mkIf`, `lib.mkOption`, `lib.types` repeatedly when usage is heavy.

**Correct:**

**Clean Inherit**

```nix
let
  inherit (lib) mkIf mkEnableOption mkOption types;
in
{
  options.foo = mkOption { type = types.str; };
}
```
