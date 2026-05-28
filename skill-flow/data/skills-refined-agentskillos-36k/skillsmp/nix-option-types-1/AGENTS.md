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

Guide for selecting and defining Nix option types properly.

---

## Table of Contents

1. [Basic Types](#1-basic-types) — **CRITICAL**
   - 1.1 [Basic Types](#11-basic-types)
2. [Collection Types](#2-collection-types) — **HIGH**
   - 2.1 [Collection Types](#21-collection-types)
3. [Submodules](#3-submodules) — **HIGH**
   - 3.1 [Submodule Pattern](#31-submodule-pattern)
4. [Package Options](#4-package-options) — **MEDIUM**
   - 4.1 [Package Options](#41-package-options)

---

## 1. Basic Types

**Impact: CRITICAL**

Essential types like boolean, string, int, path.

### 1.1 Basic Types

**Impact: MEDIUM**

Use strict types for basic options to get free validation. Use `mkEnableOption` for boolean enable flags.

**Incorrect:**

**Loose types**

`type = types.str` for a port number or path.

**Correct:**

```nix
{
  enable = lib.mkEnableOption "Feature";
  port = lib.mkOption { type = lib.types.port; default = 8080; };
  path = lib.mkOption { type = lib.types.path; };
}
```

**Strict types**

---

## 2. Collection Types

**Impact: HIGH**

Lists, attribute sets, enums.

### 2.1 Collection Types

**Impact: MEDIUM**

Use `listOf`, `attrsOf`, and `enum` to validate collections. `enum` is especially useful for constrained string choices.

**Incorrect:**

**Untyped lists**

`type = types.listOf types.any;` (unless truly necessary).

**Correct:**

```nix
{
  logLevel = lib.mkOption {
    type = lib.types.enum [ "debug" "info" "error" ];
    default = "info";
  };
  packages = lib.mkOption {
    type = lib.types.listOf lib.types.package;
    default = [];
  };
}
```

**Typed collections**

---

## 3. Submodules

**Impact: HIGH**

Complex nested configurations.

### 3.1 Submodule Pattern

**Impact: MEDIUM**

Use `types.submodule` for complex nested configurations (like creating a list of accounts or services with their own options).

**Incorrect:**

**Attrs of attrs**

`type = types.attrsOf types.attrs;` allows invalid configuration structure.

**Correct:**

```nix
users = lib.mkOption {
  type = lib.types.attrsOf (lib.types.submodule {
    options = {
      uid = lib.mkOption { type = lib.types.int; };
      shell = lib.mkOption { type = lib.types.path; };
    };
  });
};
```

**Submodule**

---

## 4. Package Options

**Impact: MEDIUM**

Handling package definitions.

### 4.1 Package Options

**Impact: MEDIUM**

Use `lib.mkPackageOption` for options that accept a package. It automatically searches `pkgs` and generates a good default description.

**Incorrect:**

**Manual Default**

`type = types.package; default = pkgs.git;` works but is less standard.

**Correct:**

```nix
package = lib.mkPackageOption pkgs "git" { };
```

**Helper**

---

