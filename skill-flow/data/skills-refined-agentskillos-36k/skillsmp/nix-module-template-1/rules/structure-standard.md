## Standard Structure

**Impact:** CRITICAL

Modules must follow the standard pattern: separate option declarations (`options`) from configuration implementation (`config`). Usage should always be guarded by a single `cfg.enable` flag.

**Incorrect:**

**Mixing logic**
Defining variables at the top level without options, or implementing config without an enable guard.

**Correct:**

**Standard Pattern**

```nix
{ config, lib, ... }:
let
  cfg = config.path.to.module;
in
{
  options.path.to.module = {
    enable = lib.mkEnableOption "Description";
  };

  config = lib.mkIf cfg.enable {
    # ...
  };
}
```
