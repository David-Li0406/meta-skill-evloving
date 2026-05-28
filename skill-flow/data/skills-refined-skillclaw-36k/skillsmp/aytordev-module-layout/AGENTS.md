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

Guide for understanding the modules directory structure and placement in aytordev's system.

---

## Table of Contents

1. [Structure](#1-structure) — **CRITICAL**
   - 1.1 [Directory Structure](#11-directory-structure)
2. [Placement](#2-placement) — **HIGH**
   - 2.1 [Home Module Categories](#21-home-module-categories)
   - 2.2 [Module Placement](#22-module-placement)
3. [Discovery](#3-discovery) — **MEDIUM**
   - 3.1 [Auto-Discovery](#31-auto-discovery)

---

## 1. Structure

**Impact: CRITICAL**

Top-level directory layout (nixos/darwin/home/common).

### 1.1 Directory Structure

**Impact: MEDIUM**

Adhere strictly to the top-level directory structure to ensure cross-platform compatibility and correct module loading.

**Incorrect:**

**Mixed Platforms**

Putting macOS modules in `modules/nixos/` or system services in `modules/home/`.

**Correct:**

**Strict Isolation**

- `modules/nixos/`: NixOS system-level (Linux only)

- `modules/darwin/`: macOS system-level (nix-darwin)

- `modules/home/`: Home Manager user-space (cross-platform)

- `modules/common/`: Shared functionality (imported by others)

---

## 2. Placement

**Impact: HIGH**

Where to place specific module types and Home module categories.

### 2.1 Home Module Categories

**Impact: MEDIUM**

Organize user modules (Home Manager) into specific categories: `programs` (graphical/terminal), `services`, `desktop`, or `suites`.

**Incorrect:**

**Flat Structure**

Dumping everything into `modules/home/programs/` without distinguishing between GUI and CLI tools.

**Correct:**

```nix
modules/home/
├── programs/
│   ├── graphical/        # GUI: browsers, editors, tools
│   └── terminal/         # CLI: editors, shells, tools
├── services/             # User services
├── desktop/              # Desktop environment config
└── suites/               # Grouped functionality
```

**Categorized Tree**

### 2.2 Module Placement

**Impact: MEDIUM**

Place modules in the correct subdirectory based on their type. Incorrect placement confuses the auto-discovery mechanism.

**Incorrect:**

**Random Location**

Putting `docker.nix` in the root of `modules/nixos/` instead of `modules/nixos/services/docker/`.

**Correct:**

**Semantic Paths**

- System service (Linux) -> `modules/nixos/services/docker/`

- System service (macOS) -> `modules/darwin/services/yabai/`

- User application -> `modules/home/programs/terminal/tools/git/`

- Cross-platform shared -> `modules/common/ai-tools/`

---

## 3. Discovery

**Impact: MEDIUM**

Auto-discovery and recursive imports.

### 3.1 Auto-Discovery

**Impact: MEDIUM**

Modules are automatically imported via `importModulesRecursive`. You do not need manual imports for standard modules; just enable them via options.

**Incorrect:**

**Manual Imports**

`imports = [ ../../some-module/default.nix ];` when the module is already part of the auto-discovery tree.

**Correct:**

**Option Enablement**

Place the file in the correct directory, then enable it:

`aytordev.programs.foo.enable = true;`

(Only use manual imports for `modules/common/` from platform-specific modules).

---

