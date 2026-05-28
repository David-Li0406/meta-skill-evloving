---
name: nix-module-template
description: "Basic Nix module structure template. Guide for creating new NixOS, Home Manager, or nix-darwin modules from scratch."
license: Complete terms in LICENSE.txt
metadata:
  author: nix
  version: "1.0.0"
---

# Module Template

Basic Nix module structure template. Use when creating new NixOS, Home Manager, or nix-darwin modules from scratch.

## Rule Categories by Priority

| Priority | Category  | Impact   | Prefix      |
| -------- | --------- | -------- | ----------- |
| 1        | Structure | CRITICAL | `structure` |
| 2        | Templates | HIGH     | `template`  |

## Quick Reference

### 1. Structure (CRITICAL)

- `structure-standard` - Standard Structure

### 2. Templates (HIGH)

- `template-darwin` - nix-darwin Module
- `template-home` - Home Manager Module
- `template-nixos` - NixOS System Module

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
