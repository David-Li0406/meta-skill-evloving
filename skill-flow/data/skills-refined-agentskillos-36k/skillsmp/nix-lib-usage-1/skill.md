---
name: nix-lib-usage
description: "Nix library usage patterns: with, inherit, and inline lib prefixes. Guide for avoiding high-scope 'with' and using 'inherit' or inline prefixes for cleaner code."
license: Complete terms in LICENSE.txt
metadata:
  author: nix
  version: "1.0.0"
---

# Library Usage Patterns

Nix library usage patterns: with, inherit, and inline lib. prefixes. Use when deciding how to access lib functions, avoiding the with lib anti-pattern, or writing analysis-friendly Nix code.

## Rule Categories by Priority

| Priority | Category        | Impact   | Prefix    |
| -------- | --------------- | -------- | --------- |
| 1        | High-Scope With | CRITICAL | `with`    |
| 2        | Inherit Pattern | HIGH     | `inherit` |
| 3        | Inline Prefix   | MEDIUM   | `inline`  |

## Quick Reference

### 1. High-Scope With (CRITICAL)

- `with-usage` - High-Scope With

### 2. Inherit Pattern (HIGH)

- `inherit-usage` - Inherit Pattern

### 3. Inline Prefix (MEDIUM)

- `inline-usage` - Inline Prefix

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
