---
name: aytordev-options-design
description: "aytordev option namespacing and design patterns. Guide for defining and using options in aytordev's system, enforcing the aytordev.* namespace."
license: Complete terms in LICENSE.txt
metadata:
  author: aytordev
  version: "1.0.0"
---

# Options Design

aytordev option namespacing and design patterns. Use when defining module options, accessing configuration values, or understanding the aytordev.\* namespace convention.

## Rule Categories by Priority

| Priority | Category       | Impact   | Prefix      |
| -------- | -------------- | -------- | ----------- |
| 1        | Namespace      | CRITICAL | `namespace` |
| 2        | Implementation | HIGH     | `impl`      |
| 3        | Context        | MEDIUM   | `context`   |

## Quick Reference

### 1. Namespace (CRITICAL)

- `namespace-convention` - Namespace Convention

### 2. Implementation (HIGH)

- `impl-helpers` - Option Helpers
- `impl-pattern` - Standard Option Pattern

### 3. Context (MEDIUM)

- `context-os` - osConfig Access
- `context-user` - Accessing User Context

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
