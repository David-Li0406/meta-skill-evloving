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

Guide for validating Nix code using automated tools and manual evaluation patterns.

---

## Table of Contents

1. [Automated Tools](#1-automated-tools) — **CRITICAL**
   - 1.1 [Automated Tools](#11-automated-tools)
2. [Manual Checks](#2-manual-checks) — **HIGH**
   - 2.1 [Manual Checks](#21-manual-checks)
3. [Common Errors](#3-common-errors) — **MEDIUM**
   - 3.1 [Common Errors](#31-common-errors)

---

## 1. Automated Tools

**Impact: CRITICAL**

Formatting, linting, and dead code removal.

### 1.1 Automated Tools

**Impact: MEDIUM**

Use `nixfmt`, `statix`, and `deadnix` to maintain code health. Integrate them via `treefmt` or `pre-commit` hooks to prevent bad code from entering the repo.

**Incorrect:**

**Unformatted Code**

Committing code with inconsistent indentation or unused variables (`let x = 1; in y`).

**Correct:**

```bash
# Before commit
nixfmt --check .
statix check .
deadnix .
```

**Automated Pipeline**

(Or use configured `treefmt`).

---

## 2. Manual Checks

**Impact: HIGH**

Dry-run evaluations and builds.

### 2.1 Manual Checks

**Impact: MEDIUM**

Use `nix eval` and `nix build --dry-run` to validate logic before pushing. This catches option type errors and evaluation failures that linters miss.

**Incorrect:**

**Blind Push**

Pushing changes without checking if the module actually evaluates.

**Correct:**

```bash
# Check if it builds (without actually building)
nix build .#nixosConfigurations.host.config.system.build.toplevel --dry-run

# Check syntax fast
nix-instantiate --parse file.nix > /dev/null
```

**Dry Run**

---

## 3. Common Errors

**Impact: MEDIUM**

Diagnosing and fixing common syntax/evaluation issues.

### 3.1 Common Errors

**Impact: MEDIUM**

Recognize common errors like missing semicolons, undefined variables (often missing `lib` argument), or infinite recursion in `rec` sets.

**Incorrect:**

```nix
rec {
  # Self-reference cycle
  x = y;
  y = x;
}
```

**Infinite Recursion**

**Correct:**

```nix
{
  x = "value";
  y = "value"; # Or use let binding
}
```

**Broken Cycle**

---

