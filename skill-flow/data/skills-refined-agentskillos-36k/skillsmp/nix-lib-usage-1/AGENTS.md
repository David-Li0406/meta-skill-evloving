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

Guide for avoiding high-scope 'with' and using 'inherit' or inline prefixes for cleaner code.

---

## Table of Contents

1. [High-Scope With](#1-high-scope-with) — **CRITICAL**
   - 1.1 [High-Scope With](#11-high-scope-with)
2. [Inherit Pattern](#2-inherit-pattern) — **HIGH**
   - 2.1 [Inherit Pattern](#21-inherit-pattern)
3. [Inline Prefix](#3-inline-prefix) — **MEDIUM**
   - 3.1 [Inline Prefix](#31-inline-prefix)

---

## 1. High-Scope With

**Impact: CRITICAL**

Patterns regarding the use of `with` scope.

### 1.1 High-Scope With

**Impact: MEDIUM**

Avoid using `with lib;` at the top of a module or file. It breaks static analysis, IDE autocompletion, and makes the origin of symbols unclear. Use it ONLY for tight, single-line scopes.

**Incorrect:**

```nix
{ config, lib, ... }:
with lib;  # Bad!
{
  # types, mkIf, etc. are now magical
}
```

**Global With**

**Correct:**

```nix
environment.systemPackages = with pkgs; [ git vim curl ];
```

**Safe With**

Single-line usage for lists is acceptable.

For modules, use `inherit` or inline prefix instead.

---

## 2. Inherit Pattern

**Impact: HIGH**

Using `inherit` to bring lib functions into scope.

### 2.1 Inherit Pattern

**Impact: MEDIUM**

When using 3 or more `lib` functions, use `inherit (lib) ...` in a `let` block. This keeps the scope clean while reducing verbosity.

**Incorrect:**

**Repetitive Prefixing**

Writing `lib.mkIf`, `lib.mkOption`, `lib.types` repeatedly when usage is heavy.

**Correct:**

```nix
let
  inherit (lib) mkIf mkEnableOption mkOption types;
in
{
  options.foo = mkOption { type = types.str; };
}
```

**Clean Inherit**

---

## 3. Inline Prefix

**Impact: MEDIUM**

Using inline `lib.` prefix for occasional usage.

### 3.1 Inline Prefix

**Impact: MEDIUM**

When using only 1 or 2 `lib` functions, just use the `lib.` prefix inline. It's explicit and avoids the boilerplate of a let block.

**Incorrect:**

**Over-optimization**

Creating a `let inherit` block just for one usage of `mkDefault`.

**Correct:**

```nix
config.foo = lib.mkDefault "bar";
```

**Direct Access**

---

