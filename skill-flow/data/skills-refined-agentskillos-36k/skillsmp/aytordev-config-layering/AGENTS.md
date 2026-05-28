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

Guide for understanding hierarchy and file structure in aytordev's system.

---

## Table of Contents

1. [Hierarchy](#1-hierarchy) — **CRITICAL**
   - 1.1 [7-Level Hierarchy](#11-7-level-hierarchy)
2. [Structure](#2-structure) — **HIGH**
   - 2.1 [Host Configuration Structure](#21-host-configuration-structure)
   - 2.2 [User Configuration Structure](#22-user-configuration-structure)
3. [Implementation](#3-implementation) — **MEDIUM**
   - 3.1 [Override Precedence](#31-override-precedence)

---

## 1. Hierarchy

**Impact: CRITICAL**

The 7-level configuration hierarchy definition.

### 1.1 7-Level Hierarchy

**Impact: MEDIUM**

Understand the strict priority order from lowest (1) to highest (7). Higher levels always override lower levels.

**Incorrect:**

**Mixing Levels**

Defining user-specific programs in a shared common module, making it hard to opt-out for other users.

**Correct:**

**Strict Layering**

1.  **Common modules** - Cross-platform base functionality

2.  **Platform modules** - OS-specific (nixos/darwin)

3.  **Home modules** - User-space programs

4.  **Suite modules** - Grouped functionality with defaults

5.  **Archetype modules** - High-level use case profiles

6.  **Host configs** - Host-specific overrides

7.  **User configs** - User-specific customizations (Highest Priority)

---

## 2. Structure

**Impact: HIGH**

Setup of Host and User configuration paths.

### 2.1 Host Configuration Structure

**Impact: MEDIUM**

Host configurations live in `systems/{arch}/{hostname}/`. They define the hardware and system-level settings specific to a single machine.

**Incorrect:**

**Host logic in modules**

Checking `networking.hostName == "foo"` inside a generic module. Use the host config file instead.

**Correct:**

```nix
{ pkgs, ... }:
{
  imports = [ ./hardware.nix ];
  networking.hostName = "khanelimain";
}
```

**Standard Path**

`systems/x86_64-linux/khanelimain/default.nix` imports specific modules and sets host-specific values.

### 2.2 User Configuration Structure

**Impact: MEDIUM**

User configurations live in `homes/{arch}/{user@host}/`. They define the highest priority personal preferences and user-specific packages.

**Incorrect:**

**Shared Home Manager**

Using a single `home.nix` for all users on all machines.

**Correct:**

```nix
{ pkgs, ... }:
{
  # Only this user on this machine gets these packages
  home.packages = [ pkgs.spotify ];
}
```

**Per-User-Per-Host**

`homes/x86_64-linux/khanelimain@khanelimain/default.nix` allows granular control.

---

## 3. Implementation

**Impact: MEDIUM**

Practical implementation and override precedence.

### 3.1 Override Precedence

**Impact: MEDIUM**

Use `lib.mkDefault` in lower layers (modules) to allow effortless overrides in higher layers (host/user configs). Avoid `lib.mkForce` unless absolutely necessary.

**Incorrect:**

**Hardcoded Module Values**

`programs.git.userName = "Default";` in a module prevents the user from overriding it without `mkForce`.

**Correct:**

```nix
# In module (Low Priority)
programs.git.userName = lib.mkDefault "Default Name";

# In host/user config (High Priority)
programs.git.userName = "Real Name";
```

**Overridable Defaults**

Define defaults in modules, specific values in configs.

---

