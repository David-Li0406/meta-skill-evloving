<!--
Embedded Cartographer Command: explore
Standalone version for plugin-free operation
-->
---
allowed-tools: Task, Glob, Grep, Read, Write, Bash(test:*), Bash(find:*), AskUserQuestion
argument-hint: <domain or path>
description: Deep domain analysis to enrich atlas references
---

## Context

Arguments: `/explore <TARGET>`
- **<domain>** - Domain name from atlas
- **<path>** - Direct path to explore

Current directory: !`pwd`

## Workflow

### 1. Pre-flight

**Verify atlas exists:**
```bash
test -f ".claude/skills/atlas/references/schema.yaml" && echo "EXISTS" || echo "NOT_FOUND"
```

**Load schema:**
- Read domain information
- Get current documentation state

### 2. Resolve Target

**If domain name:**
- Look up in schema
- Get path and existing docs

**If path:**
- Verify exists
- Check if covered by existing domain

### 3. Deep Analysis

Perform detailed exploration:

**File Inventory:**
- List ALL files with purposes
- Count lines, identify key exports

**Internal Structure:**
- Identify sub-areas
- Document relationships

**Dependencies:**
- Trace imports (what this imports)
- Trace importers (what imports this)

**Common Tasks:**
- Identify typical operations
- Document step-by-step workflows

**Patterns:**
- Domain-specific conventions
- Anti-patterns to avoid

### 4. Generate Enriched Reference

Create detailed reference file:

```markdown
# {Domain Name}

> **Location**: `{path}`
> **File Count**: {count}

## Purpose

{detailed description}

## File Inventory

| File | Lines | Purpose | Key Exports |
|------|-------|---------|-------------|
{all files}

## Internal Structure

{sub-areas with descriptions}

## Dependencies

### Imports From
{domains this imports}

### Imported By
{domains that import this}

## Common Tasks

### {Task Name}
{steps and files involved}

## Domain-Specific Patterns

{conventions and anti-patterns}
```

### 5. Update Atlas

- Update domain reference file
- Update schema with new counts/key files
- Update SKILL.md if new keywords found

### 6. Report

```markdown
## Domain Exploration Complete

**Target:** {name} (`{path}`)

**Analysis:**
- Files documented: {count}
- Sub-areas: {count}
- Dependencies: {count}
- Tasks documented: {count}

**Files updated:**
{list}
```
