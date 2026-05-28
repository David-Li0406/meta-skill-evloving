# Skill Creator Guidelines

**Version 1.0.0**  
aytordev  
January 2026

> **Note:**  
> This document is mainly for agents and LLMs to follow when creating,  
> maintaining, or refactoring AI agent skills. Humans may also find  
> it useful, but guidance here is optimized for automation and  
> consistency by AI-assisted workflows.

---

## Abstract

Guide for defining and using options in aytordev's system, enforcing the aytordev.* namespace.

---

## Table of Contents

1. [Namespace](#1-namespace) — **CRITICAL**
   - 1.1 [Namespace Convention](#11-namespace-convention)
2. [Implementation](#2-implementation) — **HIGH**
   - 2.1 [Option Helpers](#21-option-helpers)
   - 2.2 [Standard Option Pattern](#22-standard-option-pattern)
3. [Context](#3-context) — **MEDIUM**
   - 3.1 [Accessing User Context](#31-accessing-user-context)
   - 3.2 [osConfig Access](#32-osconfig-access)

---

## 1. Namespace

**Impact: CRITICAL**

The strict aytordev.\* naming convention.

### 1.1 Namespace Convention

**Impact: MEDIUM**

ALL option definitions must live under the `aytordev.*` namespace. This prevents collisions with standard NixOS/Home Manager options.

**Incorrect:**

**Global Pollution**

Defining `programs.git.myCustomOption = ...` directly in the global namespace.

**Correct:**

```nix
options.aytordev.{category}.{module}.{option} = { ... };
```

**Namespaced**

`options.aytordev.programs.terminal.tools.git.enable = ...`

Always nest custom options under `aytordev`.

---

## 2. Implementation

**Impact: HIGH**

Standard options pattern and library helpers.

### 2.1 Option Helpers

**Impact: MEDIUM**

Use `lib.aytordev` helpers to reduce boilerplate. `mkOpt` simplifies type/default/description, and `enabled`/`disabled` sets the enable flag.

**Incorrect:**

**Verbose Options**

Manually writing `mkOption { type = ...; default = ...; description = ...; }` for simple values.

**Correct:**

```nix
inherit (lib.aytordev) mkOpt enabled;

# Quick enable
programs.git = enabled;

# Custom option
userName = mkOpt types.str "default" "User name";
```

**Concise Helpers**

### 2.2 Standard Option Pattern

**Impact: MEDIUM**

Follow the standard pattern: Define options under `options.aytordev...`, enable logic with `mkIf cfg.enable`, and use a `let cfg = ...` binding for brevity.

**Incorrect:**

**Mixing options and config**

Defining options but applying configuration unconditionally without checking `cfg.enable`.

**Correct:**

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

**Standard Boilerplate**

---

## 3. Context

**Impact: MEDIUM**

Accessing user and system context.

### 3.1 Accessing User Context

**Impact: MEDIUM**

When you need user details (name, email), access them via `config.aytordev.user`.

**Incorrect:**

**Hardcoded Users**

Using `"aytordev"` string literals in configuration files.

**Correct:**

```nix
let
  user = config.aytordev.user;
in
{
  programs.git.userName = user.fullName;
  programs.git.userEmail = user.email;
}
```

**Dynamic User**

### 3.2 osConfig Access

**Impact: MEDIUM**

When a Home Manager module needs to read the system configuration (NixOS/Darwin), use `osConfig`. Always guard access with `or` to prevent eval errors in standalone Home Manager usage.

**Incorrect:**

**Unsafe Access**

Creating a dependency on `osConfig` without a fallback, crashing the build if `osConfig` is missing.

**Correct:**

```nix
{ osConfig ? {}, ... }:

# Safely check if system-level sops is enabled
mkIf (osConfig.aytordev.security.sops.enable or false) {
  # ...
}
```

**Guarded Access**

---

