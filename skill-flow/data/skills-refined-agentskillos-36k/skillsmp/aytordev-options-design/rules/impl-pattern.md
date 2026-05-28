## Standard Option Pattern

**Impact:** HIGH

Follow the standard pattern: Define options under `options.aytordev...`, enable logic with `mkIf cfg.enable`, and use a `let cfg = ...` binding for brevity.

**Incorrect:**

**Mixing options and config**
Defining options but applying configuration unconditionally without checking `cfg.enable`.

**Correct:**

**Standard Boilerplate**

```nix
{ config, lib, ... }:
let
  cfg = config.aytordev.programs.myApp;
in
{
  options.aytordev.programs.myApp = {
    enable = lib.mkEnableOption "My App";
  };

  config = lib.mkIf cfg.enable {
    # implementation
  };
}
```
