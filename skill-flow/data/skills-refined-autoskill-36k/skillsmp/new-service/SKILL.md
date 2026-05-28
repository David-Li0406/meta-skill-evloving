---
name: new-service
description: Create a new homelab service module following project patterns
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

Create a new NixOS service module in the homelab pattern.

## Arguments

Set SERVICE from the skill arguments:
```
SERVICE=$ARGUMENTS
```

The service name should be lowercase, e.g., "myservice".

## Process

1. Verify service does not exist: `ls homelab/$SERVICE.nix`
2. Read existing patterns:
   - Simple service: `homelab/redis.nix`
   - Service with nginx: `homelab/jellyfin.nix`
   - Service with database: `homelab/grafana.nix`
3. Create module at `homelab/$SERVICE.nix` following the template below
4. Add import to `homelab/default.nix` in alphabetical order
5. Run `nix flake check`
6. Report what files were created/modified

## Module Template

```nix
# Brief description of the service
{
  config,
  lib,
  pkgs,
  ...
}: let
  cfg = config.homelab.$SERVICE;
in {
  options.homelab.$SERVICE = {
    enable = lib.mkOption {
      type = lib.types.bool;
      default = false;
      description = "Enable $SERVICE service";
    };
  };

  config = lib.mkIf cfg.enable {
    # Service configuration here
  };
}
```

## Common Patterns

**Health check:**
```nix
homelab.healthChecks = [{
  name = "ServiceName";
  script = pkgs.writeShellApplication {
    name = "health-check-$SERVICE";
    runtimeInputs = [pkgs.systemd];
    text = ''
      systemctl is-active --quiet $SERVICE.service
    '';
  };
  timeout = 10;
}];
```

**Nginx reverse proxy:**
```nix
services.nginx.virtualHosts."$SERVICE.example.com" = {
  forceSSL = true;
  useACMEHost = "example.com";
  locations."/".proxyPass = "http://127.0.0.1:PORT";
};
```

**Prometheus scrape target:**
```nix
homelab.scrapeTargets = [{
  job = "$SERVICE";
  metricsPath = "/metrics/$SERVICE";
}];
```

## Rules

- Follow existing patterns in the codebase
- Keep module focused on one service
- Use lib.mkIf for conditional configuration
- Bind services to 127.0.0.1 by default
