---
name: reverse-engineer
description: Use this skill when you need to reverse engineer existing code into SDD (Specification Driven Development) documentation, particularly for analyzing legacy code or documenting undocumented systems.
---

# Reverse Engineering to SDD Specification Guide

> **Languages**: [English](../../../../../skills/claude-code/reverse-engineer/SKILL.md) | [繁體中文](../../../../zh-TW/skills/claude-code/reverse-engineer/SKILL.md) | [简体中文](../../../../zh-CN/skills/claude-code/reverse-engineer/SKILL.md)

**Version**: 1.1.0  
**Last Updated**: 2026-01-19  
**Applicable Scope**: Claude Code Skills

> **Core Standards**: This skill implements the [Reverse Engineering Standards](../../../core/reverse-engineering-standards.md). Any AI tool can refer to the core standards for complete methodological documentation.

## Purpose

This skill guides you in reverse engineering existing code into SDD (Specification Driven Development) documentation while strictly adhering to anti-hallucination standards.

## Quick Reference

### Reverse Engineering Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│              Reverse Engineering Workflow                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣  Code Analysis (AI Automated)                               │
│      ├─ Scan code structure, APIs, and data models             │
│      ├─ Parse existing tests to extract acceptance criteria     │
│      └─ Generate draft specifications (with uncertainty labels) │
│                                                                 │
│  2️⃣  Human Input (Required)                                     │
│      ├─ Write motivation (why this feature is needed)          │
│      ├─ Add risk assessment                                       │
│      └─ Validate dependencies and business context               │
│                                                                 │
│  3️⃣  Review and Confirmation                                     │
│      ├─ Discuss with stakeholders                                 │
│      └─ Confirm [Confirmed] / [Inferred] / [Unknown] labels     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Extractable and Non-Extractable Content

| Aspect         | Extractable | Certainty | Notes                          |
|----------------|-------------|-----------|--------------------------------|
| **API Endpoints** | ✅ Yes     | [Confirmed] | Route definitions, HTTP methods |
| **Data Models**   | ✅ Yes     | [Confirmed] | Types, interfaces, structure descriptions |
| **Function Signatures** | ✅ Yes | [Confirmed] | Parameters, return types       |
| **Test Cases**    | ✅ Yes     | [Confirmed] | → Acceptance criteria          |
| **Dependencies**  | ✅ Yes     | [Confirmed] | Package references             |
| **Behavior Patterns** | ⚠️ Partially | [Inferred] | Inferred from code analysis    |
| **Motivation/Why** | ❌ No     | [Unknown] | Requires human input           |
| **Business Context** | ❌ No  | [Unknown] | Requires human input           |
| **Risk Assessment** | ❌ No   | [Unknown] | Requires domain expertise      |
| **Trade-off Decisions** | ❌ No | [Unknown] | Lacks historical context       |

## Core Principles

### 1. Anti-Hallucination Compliance

**Key**: This skill must strictly adhere to the [Anti-Hallucination Standards](../../../core/anti-hallucination.md).