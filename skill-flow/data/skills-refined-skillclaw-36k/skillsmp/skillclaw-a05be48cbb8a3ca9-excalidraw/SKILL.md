---
name: excalidraw
description: Use this skill when working with *.excalidraw or *.excalidraw.json files, user mentions diagrams/flowcharts, or requests architecture visualization. It delegates all Excalidraw operations to subagents to prevent context exhaustion from verbose JSON.
---

# Excalidraw Subagent Delegation

## Overview

**Core principle:** Main agents NEVER read Excalidraw files directly. Always delegate to subagents to isolate context consumption.

Excalidraw files are JSON with high token cost but low information density. Single files range from 4k-22k tokens (largest can exceed read tool limits). Reading multiple diagrams quickly exhausts context budget (7 files = 67k tokens = 33% of budget).

## The Problem

Excalidraw JSON structure:
- Each shape has 20+ properties (x, y, width, height, strokeColor, seed, version, etc.)
- Most properties are visual metadata (positioning, styling, roughness)
- Actual content: text labels and element relationships (<10% of file)
- **Signal-to-noise ratio is extremely low**

Example: 14-element diagram = 596 lines, 16K, ~4k tokens. 79-element diagram = 2,916 lines, 88K, ~22k tokens (exceeds read limit).

## When to Use

**Trigger on ANY of these:**
- File path contains `.excalidraw` or `.excalidraw.json`
- User requests: "explain/update/create diagram", "show architecture", "visualize flow"
- User mentions: "flowchart", "architecture diagram", "Excalidraw file"
- Architecture/design documentation tasks involving visual artifacts

**Use delegation even for:**
- "Small" files (smallest is 4k tokens - still significant)
- "Quick checks" (checking component names still loads full JSON)
- Single file operations (isolation prevents context pollution)
- Modifications (don't need full format understanding in main context)

## Delegation Pattern

### Main Agent Responsibilities

**NEVER:**
- ❌ Use Read tool on *.excalidraw files
- ❌ Parse Excalidraw JSON in main context
- ❌ Load multiple diagrams for comparison
- ❌ Inspect file to "understand the format"

**ALWAYS:**
- ✅ Delegate ALL Excalidraw operations to subagents
- ✅ Provide clear task description to subagent
- ✅ Request text-only summaries (not raw JSON)
- ✅ Keep diagram analysis isolated from main work

### Subagent Task Templates

#### Read/Understand Operation
```
Task: Extract and explain the components in [file.excalidraw.json]

Approach:
1. Read the Excalidraw JSON
2. Extract only text elements (ignore positioning and styling)
```