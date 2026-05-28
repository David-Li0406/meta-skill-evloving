---
name: document-project
description: Use to analyze and document any project codebase. Creates comprehensive reference documentation for AI-assisted development including architecture and patterns.
version: 1.0.0
---

# Document Project Task

## When to Use

- **Project Documentation**: Document any codebase for AI understanding
- **Architecture Assessment**: Analyze current system architecture
- **Knowledge Transfer**: Create comprehensive project documentation
- **PRD Preparation**: Generate context needed for PRD creation
- **Onboarding**: Build complete project reference for new team members

## What This Skill Does

Guides you through building comprehensive project documentation:

- **Configuration**: Load project settings from `.prism/core-config.yaml`
- **Classification**: Detect project type, structure, and technology stack
- **Scanning**: Analyze codebase (quick, deep, or exhaustive)
- **Documentation**: Generate architecture, API, and development guides
- **Indexing**: Create master index for AI retrieval

## Quick Start

1. Run the skill and specify project root directory
2. Choose scan depth (quick/deep/exhaustive)
3. Confirm project classification
4. Wait for documentation generation
5. Review generated files at `{{output_folder}}/index.md`

**Output Location**: `docs/project/` (or as configured)

## Workflow Overview

The workflow follows 10 sequential steps. For detailed instructions, see [Workflow Steps Reference](./reference/workflow-steps.md).

| Step | Name | Purpose |
|------|------|---------|
| 0 | Load Configuration | Read `.prism/core-config.yaml` |
| 1 | Check Existing | Detect existing docs, choose mode |
| 2 | Select Scan Level | Quick/Deep/Exhaustive |
| 3 | Initialize State | Create tracking file |
| 4 | Detect Structure | Classify project type |
| 5 | Scan Project | Execute selected scan depth |
| 6 | Deep-Dive Mode | (If selected) Detailed area analysis |
| 6.5 | Check Existing Docs | Avoid duplicates via Smart Connections |
| 7 | Generate Index | Create master entry point |
| 8-10 | Validate & Complete | Verify, fill gaps, finalize |

## Scan Levels

| Level | Time | What It Does |
|-------|------|--------------|
| **Quick** | 2-5 min | Pattern-based analysis, configs only |
| **Deep** | 10-30 min | Critical directories, selective file reading |
| **Exhaustive** | 30-120 min | ALL source files (excludes node_modules) |

## Project Types Detected

- **claude-code-plugin**: PRISM-style plugins with skills/commands/tasks
- **web**: React, Vue, Angular applications
- **backend**: Express, FastAPI, Rails servers
- **mobile**: React Native, Flutter apps
- **cli/library/desktop**: Various other project types

## Generated Documentation

Core files generated (as applicable):

- `index.md` - Master entry point
- `project-overview.md` - Executive summary
- `architecture.md` - Technical architecture
- `technology-stack.md` - Complete tech stack
- `development-guide.md` - Setup and workflow
- `api-contracts.md` - API endpoints
- `data-models.md` - Database schema
- `source-tree-analysis.md` - Directory structure

## Key Principles

1. **Write-as-you-go**: Write files immediately, don't accumulate
2. **Resumability**: State file tracks progress for resume
3. **Batching**: Process subfolders one at a time for token management
4. **No duplicates**: Check existing docs before creating

## Reference Documentation

- **[Workflow Steps](./reference/workflow-steps.md)** - Detailed step-by-step instructions

## Guardrails

- Always load config first (Step 0)
- Update state file after EVERY step completion
- Write documents immediately after generating content
- Purge detailed data from context after writing
- First-time startup may require explicit scan level selection
