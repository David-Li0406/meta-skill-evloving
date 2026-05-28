---
name: aytordev-module-layout
description: "aytordev directory structure and module placement. Guide for understanding the modules directory structure and placement in aytordev's system."
license: Complete terms in LICENSE.txt
metadata:
  author: aytordev
  version: "1.0.0"
---

# Module Layout

aytordev directory structure and module placement. Use when creating new modules, deciding where files belong, or understanding the modules/ organization. Covers platform separation (nixos/darwin/home/common) and auto-discovery.

## Rule Categories by Priority

| Priority | Category  | Impact   | Prefix      |
| -------- | --------- | -------- | ----------- |
| 1        | Structure | CRITICAL | `structure` |
| 2        | Placement | HIGH     | `placement` |
| 3        | Discovery | MEDIUM   | `discovery` |

## Quick Reference

### 1. Structure (CRITICAL)

- `structure-directories` - Directory Structure

### 2. Placement (HIGH)

- `placement-home` - Home Module Categories
- `placement-types` - Module Placement

### 3. Discovery (MEDIUM)

- `discovery-auto` - Auto-Discovery

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
