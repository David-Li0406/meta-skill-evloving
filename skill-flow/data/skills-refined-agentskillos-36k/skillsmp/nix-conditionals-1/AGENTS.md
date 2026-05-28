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

Guide for writing idiomatic conditional configuration in Nix using lib functions.

---

## Table of Contents

1. [Config Blocks](#1-config-blocks) — **CRITICAL**
   - 1.1 [mkIf - Conditional Config Blocks](#11-mkif---conditional-config-blocks)
   - 1.2 [mkMerge - Combine Conditionals](#12-mkmerge---combine-conditionals)
2. [Lists](#2-lists) — **HIGH**
   - 2.1 [optionals - Conditional List Items](#21-optionals---conditional-list-items)
3. [Strings](#3-strings) — **MEDIUM**
   - 3.1 [optionalString - Conditional Strings](#31-optionalstring---conditional-strings)

---

## 1. Config Blocks

**Impact: CRITICAL**

Conditional configuration blocks and merging logic.

### 1.1 mkIf - Conditional Config Blocks

**Impact: MEDIUM**

Use `lib.mkIf` for conditional configuration blocks. It pushes the condition down to the leaves of the configuration, allowing accurate merging. Avoid Python-style `if condition then { ... } else { ... }` for top-level config blocks, as it breaks module merging.

**Incorrect:**

**Top-level if-else**

Wraps the entire config set in a conditional, preventing other modules from merging into it unless the condition matches perfectly for everyone.

**Correct:**

```nix
config = lib.mkIf cfg.enable {
  programs.git.enable = true;
};
```

**mkIf**

Use `lib.mkIf` to guard the configuration.

### 1.2 mkMerge - Combine Conditionals

**Impact: MEDIUM**

Use `lib.mkMerge` to combine multiple conditional blocks into a single definition. This is clearer than repeating `config = ...` multiple times or nesting if-else structures deeply.

**Incorrect:**

**Nested spaghetti**

Deeply nested `mkIf` calls or split config definitions that are hard to read.

**Correct:**

```nix
config = lib.mkMerge [
  # Always applied
  { programs.bash.enable = true; }

  # Conditional A
  (lib.mkIf cfg.enableGit { programs.git.enable = true; })

  # Conditional B
  (lib.mkIf cfg.enableVim { programs.vim.enable = true; })
];
```

**Clean Merge**

---

## 2. Lists

**Impact: HIGH**

Conditional list items.

### 2.1 optionals - Conditional List Items

**Impact: MEDIUM**

Use `lib.optionals` (plural) to conditionally include a list of items. It returns an empty list `[]` if the condition is false, making it safe to concatenate `++`.

**Incorrect:**

**Ternary for lists**

`pkgs = [ item1 ] ++ (if cond then [ item2 ] else []);` is verbose.

**Correct:**

```nix
home.packages = [ pkgs.coreutils ]
  ++ lib.optionals cfg.enableTools [ pkgs.ripgrep pkgs.fd ];
```

**optionals**

---

## 3. Strings

**Impact: MEDIUM**

Conditional string generation.

### 3.1 optionalString - Conditional Strings

**Impact: MEDIUM**

Use `lib.optionalString` to generate a string only if a condition is true. Returns `""` otherwise. Ideal for shell scripts or config files.

**Incorrect:**

**If-then-else null**

`str = if cond then "text" else null;` usually throws a type error because you can't concatenate null strings.

**Correct:**

```nix
shellInit = ''
  export EDITOR=vim
'' + lib.optionalString cfg.enableAliases ''
  alias ll='ls -la'
'';
```

**optionalString**

---

