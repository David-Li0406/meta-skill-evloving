---
name: documentation-standards
description: Use this skill when writing markdown documentation, creating skills, or authoring content that may be converted to PDF, ensuring compliance with LLM-optimized architecture standards.
---

# Documentation Standards

## Overview

Standards for writing markdown documentation optimized for both LLM consumption and conversion to professional PDFs using Pandoc. Ensures consistency across all documentation.

## When to Use This Skill

Use when:
- Writing markdown documentation (README, skills, guides, specifications)
- Creating new skills that include markdown content
- Authoring content that may be converted to PDF
- Reviewing documentation for standards compliance

## Core Principles

### 1. LLM-Optimized Documentation Architecture

**Machine-Readable Priority**: OpenAPI 3.1.0 specs, JSON Schema, YAML specifications take precedence over human documentation.

**Why**: Structured formats provide unambiguous contracts that both humans and LLMs can consume reliably. Human docs supplement, don't replace, machine-readable specs.

**Application**:
- Workflow specifications → OpenAPI 3.1.1 YAML in specifications/
- Data schemas → JSON Schema with examples
- Configuration → YAML with validation schemas
- Human docs → Markdown referencing canonical machine-readable specs

### 2. Hub-and-Spoke Progressive Disclosure

**Pattern**: Central hubs (like CLAUDE.md, INDEX.md) link to detailed spokes (skills, docs directories).

**Structure**:
```
CLAUDE.md (Hub - Essentials Only)
    ↓ links to
Skills (Spokes - Progressive Disclosure)
    ├── SKILL.md (Overview + Quick Start)
    └── references/ (Detailed Documentation)
```

**Rules**:
- Hubs contain essentials only (what + where to find more)
- Spokes contain progressive detail (load as needed)
- Single source of truth per topic (no duplication)

### 3. Markdown Section Numbering

**Critical Rule**: Never manually number markdown headings.

❌ **Wrong**:
```markdown
## 1. Introduction
### 1.1 Background
### 1.2 Objectives
## 2. Implementation
```

✅ **Correct**:
```markdown
## Introduction
### Background
### Objectives
## Implementation
```

**Rationale**:
- Pandoc's `--number-sections` flag auto-numbers all sections when generating PDFs.
- Manual numbering creates duplication: "1. 1. Introduction" in rendered output.
- Auto-numbering is consistent and updates automatically when sections reorganize.