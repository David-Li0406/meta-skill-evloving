## Basic Types

**Impact:** CRITICAL

Use strict types for basic options to get free validation. Use `mkEnableOption` for boolean enable flags.

**Incorrect:**

**Loose types**
`type = types.str` for a port number or path.

**Correct:**

**Strict types**

```nix
{
  enable = lib.mkEnableOption "Feature";
  port = lib.mkOption { type = lib.types.port; default = 8080; };
  path = lib.mkOption { type = lib.types.path; };
}
```
