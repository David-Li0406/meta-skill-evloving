---
name: nix-option-types
description: "Nix module option types and definition patterns. Guide for selecting and defining Nix option types properly."
license: Complete terms in LICENSE.txt
metadata:
  author: nix
  version: "1.0.0"
---

# Option Types

Nix module option types and definition patterns. Use when defining options with mkOption, choosing types, or creating submodules.

## Rule Categories by Priority

| Priority | Category         | Impact   | Prefix       |
| -------- | ---------------- | -------- | ------------ |
| 1        | Basic Types      | CRITICAL | `basic`      |
| 2        | Collection Types | HIGH     | `collection` |
| 3        | Submodules       | HIGH     | `submodule`  |
| 4        | Package Options  | MEDIUM   | `package`    |

## Quick Reference

### 1. Basic Types (CRITICAL)

- `basic-types` - Basic Types

### 2. Collection Types (HIGH)

- `collection-types` - Collection Types

### 3. Submodules (HIGH)

- `submodule-pattern` - Submodule Pattern

### 4. Package Options (MEDIUM)

- `package-options` - Package Options

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
