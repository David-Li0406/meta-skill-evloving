## Collection Types

**Impact:** HIGH

Use `listOf`, `attrsOf`, and `enum` to validate collections. `enum` is especially useful for constrained string choices.

**Incorrect:**

**Untyped lists**
`type = types.listOf types.any;` (unless truly necessary).

**Correct:**

**Typed collections**

```nix
{
  logLevel = lib.mkOption {
    type = lib.types.enum [ "debug" "info" "error" ];
    default = "info";
  };
  packages = lib.mkOption {
    type = lib.types.listOf lib.types.package;
    default = [];
  };
}
```
