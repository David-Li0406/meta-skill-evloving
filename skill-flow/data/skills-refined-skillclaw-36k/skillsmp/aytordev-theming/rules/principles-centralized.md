## Centralized SOT (Source Of Truth)

**Impact:** CRITICAL

The `aytordev.theme` module is the single source of truth for all theming data. It abstracts the underlying colors (Kanagawa) and provides a unified API for all other modules to consume. Never hardcode colors or imports in individual modules.

**Incorrect:**

**Fragmented definitions**
Importing `colors.nix` directly in module files or defining local color variables like `blue = "#..."`.

**Correct:**

**Provider Consumption**
Consume `config.aytordev.theme` to access all theme data. This ensures consistent polarity and variant switching across the entire system.

```nix
{ config, lib, ... }:
let
  cfg = config.aytordev.theme;
in
{
  # Access palette through the central config
  programs.foo.color = cfg.palette.accent.hex;
}
```
