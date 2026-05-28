---
name: aytordev-config-layering
description: "aytordev 7-level configuration hierarchy and customization strategy. Guide for understanding hierarchy and file structure in aytordev's system."
license: Complete terms in LICENSE.txt
metadata:
  author: aytordev
  version: "1.0.0"
---

# Configuration Layering

aytordev 7-level configuration hierarchy and customization strategy. Use when deciding where to put customizations, understanding override precedence, or working with host/user specific configs.

## Rule Categories by Priority

| Priority | Category       | Impact   | Prefix      |
| -------- | -------------- | -------- | ----------- |
| 1        | Hierarchy      | CRITICAL | `hierarchy` |
| 2        | Structure      | HIGH     | `structure` |
| 3        | Implementation | MEDIUM   | `impl`      |

## Quick Reference

### 1. Hierarchy (CRITICAL)

- `hierarchy-levels` - 7-Level Hierarchy

### 2. Structure (HIGH)

- `structure-host` - Host Configuration Structure
- `structure-user` - User Configuration Structure

### 3. Implementation (MEDIUM)

- `impl-precedence` - Override Precedence

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
