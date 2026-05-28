## Home Manager Module

**Impact:** HIGH

For user-level applications and dotfiles.

**Incorrect:**

**System-level syntax**
Using `environment.systemPackages` or `networking.hostName`.

**Correct:**

**User Application**

```nix
{ config, lib, pkgs, ... }:
let
  cfg = config.programs.myApp;
in
{
  options.programs.myApp.enable = lib.mkEnableOption "My App";

  config = lib.mkIf cfg.enable {
    home.packages = [ pkgs.myApp ];
    xdg.configFile."myapp/config".text = "example";
  };
}
```
