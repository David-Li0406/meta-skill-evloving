## High-Scope With

**Impact:** CRITICAL

Avoid using `with lib;` at the top of a module or file. It breaks static analysis, IDE autocompletion, and makes the origin of symbols unclear. Use it ONLY for tight, single-line scopes.

**Incorrect:**

**Global With**

```nix
{ config, lib, ... }:
with lib;  # Bad!
{
  # types, mkIf, etc. are now magical
}
```

**Correct:**

**Safe With**
Single-line usage for lists is acceptable.

```nix
environment.systemPackages = with pkgs; [ git vim curl ];
```

For modules, use `inherit` or inline prefix instead.
