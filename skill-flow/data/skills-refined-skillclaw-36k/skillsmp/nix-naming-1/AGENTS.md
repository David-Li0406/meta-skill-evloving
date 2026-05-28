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

Guide for consistent naming conventions in Nix (camelCase variables, kebab-case files).

---

## Table of Contents

1. [Variables](#1-variables) — **CRITICAL**
   - 1.1 [Variable Naming](#11-variable-naming)
2. [Files](#2-files) — **HIGH**
   - 2.1 [File Naming](#21-file-naming)
3. [Organization](#3-organization) — **MEDIUM**
   - 3.1 [Attribute Organization](#31-attribute-organization)

---

## 1. Variables

**Impact: CRITICAL**

Naming conventions for variables and constants.

### 1.1 Variable Naming

**Impact: MEDIUM**

Use `camelCase` for standard variables and `UPPER_CASE` for constants.

**Incorrect:**

**Mixed styles**

`user_name = "..."` (snake_case) or `UserName = "..."` (PascalCase).

**Correct:**

```nix
let
  userName = "khaneliman";
  enableAutoStart = true;
  MAX_RETRIES = 5;
in
# ...
```

**camelCase**

---

## 2. Files

**Impact: HIGH**

Naming conventions for files and directories.

### 2.1 File Naming

**Impact: MEDIUM**

Use `kebab-case` for all files and directories. This is standard in the Nix community and avoids case-sensitivity issues on some filesystems.

**Incorrect:**

**Camel or Snake**

`modules/home/myApp/default.nix` or `my_service.nix`.

**Correct:**

```nix
modules/home/programs/my-app/default.nix
modules/nixos/services/my-service.nix
```

**kebab-case**

---

## 3. Organization

**Impact: MEDIUM**

Code structure and organization within modules.

### 3.1 Attribute Organization

**Impact: MEDIUM**

Organize module attributes logically: `imports`, `options`, then `config`. Inside `config`, group settings by module. Ideally use the `cfg` pattern.

**Incorrect:**

**Scattered configs**

Interleaving options and config, or scattering `home.packages` throughout the file.

**Correct:**

```nix
{
  imports = [ ... ];

  options.namespace.module = { ... };

  config = lib.mkIf cfg.enable {
    programs.git = { ... };
    home.packages = [ ... ];
  };
}
```

**Structured**

---

