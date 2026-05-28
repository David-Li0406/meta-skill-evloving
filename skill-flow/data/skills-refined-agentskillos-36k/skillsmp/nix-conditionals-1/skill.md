---
name: nix-conditionals
description: "Nix conditional patterns: mkIf, optionals, optionalString, mkMerge. Guide for writing idiomatic conditional configuration in Nix using lib functions."
license: Complete terms in LICENSE.txt
metadata:
  author: nix
  version: "1.0.0"
---

# Conditional Patterns

Nix conditional patterns: mkIf, optionals, optionalString, mkMerge. Use when writing conditional configuration, avoiding if-then-else, or combining multiple conditional blocks.

## Rule Categories by Priority

| Priority | Category      | Impact   | Prefix           |
| -------- | ------------- | -------- | ---------------- |
| 1        | Config Blocks | CRITICAL | `mkif`           |
| 2        | Lists         | HIGH     | `optionals`      |
| 3        | Strings       | MEDIUM   | `optionalstring` |

## Quick Reference

### 1. Config Blocks (CRITICAL)

- `mkif-usage` - mkIf - Conditional Config Blocks
- `mkmerge-usage` - mkMerge - Combine Conditionals

### 2. Lists (HIGH)

- `optionals-usage` - optionals - Conditional List Items

### 3. Strings (MEDIUM)

- `optionalstring-usage` - optionalString - Conditional Strings

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
