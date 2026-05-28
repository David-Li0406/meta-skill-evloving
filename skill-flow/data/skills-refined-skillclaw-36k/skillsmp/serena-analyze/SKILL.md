---
name: serena-analyze
description: Analyze codebase structure using Serena's symbolic tools. Use for understanding project architecture, generating structure overviews, mapping dependencies between components, and onboarding to new codebases.
context: fork
agent: Explore
---

# Serena Analyze Skill

Analyze codebase structure and architecture using Serena MCP's semantic code understanding tools.

## Core Principles

1. **Efficient exploration**: Use symbolic tools to understand structure without reading entire files
2. **Top-down approach**: Start with overview, drill down only where needed
3. **Map relationships**: Understand how components connect and depend on each other
4. **Summarize findings**: Provide clear, actionable insights

## Serena MCP Tools

### Structure Analysis
- `mcp__serena__get_symbols_overview`: Get all top-level symbols in a file (classes, functions, etc.)
- `mcp__serena__find_symbol`: Get details of specific symbol with optional body
- `mcp__serena__find_referencing_symbols`: Map dependencies and usages

### Navigation
- `mcp__serena__list_dir`: Explore directory structure
- `mcp__serena__find_file`: Locate files by name pattern
- `mcp__serena__search_for_pattern`: Find patterns across codebase

### Context
- `mcp__serena__read_file`: Read file when detailed understanding needed
- `mcp__serena__read_memory`: Check existing project knowledge

## Analysis Workflow

1. **Project overview**: Use `list_dir` to understand directory structure
2. **Identify entry points**: Find main files, exports, public APIs
3. **Map components**: Use `get_symbols_overview` on key files
4. **Trace relationships**: Use `find_referencing_symbols` for dependency mapping
5. **Document findings**: Summarize architecture and patterns

## Analysis Types

### Architecture Overview
- Directory structure analysis
- Module/package organization
- Entry points and public APIs
- Configuration patterns

### Component Deep-Dive
- Class/function structure
- Internal dependencies
- Interface definitions
- Design patterns used

### Dependency Mapping
- Import/export relationships
- Call graphs
- Data flow paths
- Circular dependency detection

### Codebase Onboarding
- Key files to understand
- Core abstractions
- Naming conventions
- Common patterns

## Response Format

```
## Overview

[High-level summary of findings]

## Structure

[Directory/component organization]

## Key Components

| Component | Location | Purpose |
|-----------|----------|---------|
| ...       | ...      | ...     |

## Relationships

[Dependency diagram or description]

## Patterns Identified

- [Pattern 1]
- [Pattern 2]

## Recommendations (if applicable)

- [Suggestion 1]
- [Suggestion 2]
```

## Task: $ARGUMENTS

Analyze the codebase to answer:

$ARGUMENTS

Use Serena's symbolic tools to efficiently understand structure without reading unnecessary code.
