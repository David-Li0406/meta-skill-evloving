# Skill Creator Guidelines

**Version 1.0.0**  
nix  
January 2026

> **Note:**  
> This document is mainly for agents and LLMs to follow when creating,  
> maintaining, or refactoring AI agent skills. Humans may also find  
> it useful, but guidance here is optimized for automation and  
> consistency by AI-assisted workflows.

---

## Abstract

Standard structure for Nix modules enabling configuration via options and config merging.

---

## Table of Contents

1. [Structure](#1-structure) — **CRITICAL**
   - 1.1 [Standard Structure](#11-standard-structure)
2. [Templates](#2-templates) — **HIGH**
   - 2.1 [Home Manager Module](#21-home-manager-module)
   - 2.2 [nix-darwin Module](#22-nix-darwin-module)
   - 2.3 [NixOS System Module](#23-nixos-system-module)

---

## 1. Structure

**Impact: CRITICAL**

General module structure and composition.

### 1.1 Standard Structure

**Impact: MEDIUM**

Modules must follow the standard pattern: separate option declarations (`options`) from configuration implementation (`config`). Usage should always be guarded by a single `cfg.enable` flag.

**Incorrect:**

**Mixing logic**

Defining variables at the top level without options, or implementing config without an enable guard.

**Correct:**

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

**Standard Pattern**

---

## 2. Templates

**Impact: HIGH**

Specific templates for NixOS, Home Manager, and Darwin.

### 2.1 Home Manager Module

**Impact: MEDIUM**

For user-level applications and dotfiles.

**Incorrect:**

**System-level syntax**

Using `environment.systemPackages` or `networking.hostName`.

**Correct:**

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

**User Application**

### 2.2 nix-darwin Module

**Impact: MEDIUM**

For macOS system configurations.

**Incorrect:**

**Linux assumptions**

Using `services.xserver` or other Linux-only options.

**Correct:**

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

**MacOS Defaults**

### 2.3 NixOS System Module

**Impact: MEDIUM**

For system-level services (systemd, hardware, networking).

**Incorrect:**

**Home-manager syntax**

Using `home.packages` inside a NixOS module (unless wrapping home-manager).

**Correct:**

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

**Systemd Service**

---

