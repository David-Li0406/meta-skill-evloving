## nix-darwin Module

**Impact:** HIGH

For macOS system configurations.

**Incorrect:**

**Linux assumptions**
Using `services.xserver` or other Linux-only options.

**Correct:**

**MacOS Defaults**

```nix
{ config, lib, ... }:
let
  cfg = config.system.defaults.custom;
in
{
  options.system.defaults.custom.enable = lib.mkEnableOption "macOS tweaks";

  config = lib.mkIf cfg.enable {
    system.defaults.dock.autohide = true;
  };
}
```
