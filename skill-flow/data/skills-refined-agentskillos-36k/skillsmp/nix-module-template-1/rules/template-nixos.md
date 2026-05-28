## NixOS System Module

**Impact:** HIGH

For system-level services (systemd, hardware, networking).

**Incorrect:**

**Home-manager syntax**
Using `home.packages` inside a NixOS module (unless wrapping home-manager).

**Correct:**

**Systemd Service**

```nix
{ config, lib, pkgs, ... }:
let
  cfg = config.services.myService;
in
{
  options.services.myService.enable = lib.mkEnableOption "My Service";

  config = lib.mkIf cfg.enable {
    systemd.services.my-service = {
      wantedBy = [ "multi-user.target" ];
      serviceConfig.ExecStart = "${pkgs.myService}/bin/start";
    };
  };
}
```
