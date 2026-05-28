---
name: context-keeper
description: Maintains project context through progressive disclosure and enforced documentation. This skill should be used when starting work on a new project to initialize context documentation, or continuously during development to maintain up-to-date project structure and coding conventions. Triggers on project initialization, file modifications, or when the agent needs to understand project architecture.
version: 1.0.0
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
---

# Context Keeper

Maintains project context through layered documentation and enforced synchronization.

## Overview

Context Keeper implements a three-level documentation system that ensures AI agents always have accurate, up-to-date context about the codebase:

1. **USERAGENTS.md** - Project-level: structure, conventions, and directory index
2. **TECH_INFO.md** - Directory-level: file descriptions, dependencies, and changes
3. **File headers** - File-level: function descriptions, parameters, and modification dates

## When to Use This Skill

- **Project initialization**: Run `scan_project.py` to generate initial documentation
- **Before modifying code**: Read the relevant TECH_INFO.md first
- **After completing changes**: Update TECH_INFO.md and file headers
- **When project structure changes**: Update USERAGENTS.md

## Key Design Decisions

- **On-demand TECH_INFO.md generation**: Documentation is only created for directories where the AI actually works, avoiding unnecessary files
- **Event-driven maintenance**: Hooks track file modifications and automatically prompt AI to update documentation at session end
- **No git commits**: TECH_INFO.md files are excluded from version control (local context only)
- **Full directory depth**: No artificial depth limitation - documentation scales with the project
- **Language**: All generated content is in English for international teams

## Workflow

### Phase 1: Initialize Project Context

Run the scanner to generate initial documentation:

```bash
python scripts/scan_project.py <project-path>
```

The script will:
1. Detect tech stack (TypeScript, React, Go, Python, etc.)
2. Infer coding conventions based on tech stack
3. Generate `USERAGENTS.md` with project structure
4. **Note**: `TECH_INFO.md` files are NOT pre-generated - they are created on-demand when you work in a directory
5. Update `AGENTS.md/CLAUDE.md` with enforcement instructions
6. (Optional) Install hooks to automatically track changes and enforce documentation updates

Use `--dry-run` to preview changes without modifying files.

### Phase 2: On-Demand TECH_INFO.md Creation

When you start working in a directory that doesn't have `TECH_INFO.md`:

1. Check if the directory has a `TECH_INFO.md` file
2. If not, create it using the template format
3. Fill in the descriptions based on your analysis of the code in that directory

The template structure:
```markdown
# [Directory Name] - Technical Documentation

> **Directory purpose**: [Your analysis based on file contents]
> **Last updated**: YYYY-MM-DD

---

## 📁 File Inventory

| Filename | Description | Input | Output | Dependencies |
|----------|-------------|-------|--------|--------------|
| file1.ts | [Accurate description] | Type | Type | ./other-file |

---

## 🔄 Change Log

| Date | Change | Operator |
|------|--------|----------|
| YYYY-MM-DD | [What you changed] | context-keeper |
```

### Phase 3: Before Any Code Modification

Before modifying any file, follow this checklist:

```
Pre-modification checklist:
- [ ] Read USERAGENTS.md to understand project conventions
- [ ] Read target directory's TECH_INFO.md
- [ ] Understand file dependencies from TECH_INFO.md
- [ ] Review file header comments for context
```

### Phase 4: After Code Modification

After completing changes, update documentation:

```
Post-modification checklist:
- [ ] Update file header (@description, @lastModified)
- [ ] Update TECH_INFO.md file table if file added/changed
- [ ] Add change record to TECH_INFO.md
- [ ] Update USERAGENTS.md if directory structure changed
```

### Phase 5: Automatic Enforcement (via Hooks)

When the session ends, the `stop.sh` hook will:
1. Check which files were modified during the session
2. Group them by directory
3. Display a **mandatory action list** requiring you to update documentation
4. Block session completion (in `--strict` mode) until documentation is updated

This ensures documentation is never forgotten, even when using multiple skills.

## Installation & Setup

### 1. Install Dependencies

```bash
# No external dependencies required - uses Python standard library only
python3 --version  # Requires Python 3.7+
```

### 2. Initialize Documentation

```bash
# Generate initial USERAGENTS.md
python scripts/scan_project.py /path/to/your/project

# Preview without changes
python scripts/scan_project.py /path/to/your/project --dry-run
```

### 3. (Optional) Install Hooks

Configure hooks in your Claude Code settings:

```json
{
  "hooks": {
    "PostToolUse": "/absolute/path/to/context-keeper/hooks/post_tool_use.sh",
    "Stop": "/absolute/path/to/context-keeper/hooks/stop.sh --strict"
  }
}
```

**What the hooks do**:
- `PostToolUse`: Tracks file modifications (edit_file, write, create, delete)
- `Stop`: Displays mandatory documentation tasks before session end
- `--strict` flag (optional): Blocks session completion until docs are updated

## Dependencies & Runtime

- **Python 3.7+ required**: `scripts/scan_project.py` uses only the Python standard library
- **No external packages**: Safe to run in restricted environments
- **Git required**: For .gitignore parsing and tracking changes

## Documentation Templates

### TECH_INFO.md Template

See `references/tech_info_template.md` for the standard template.

### File Header Template

```typescript
/**
 * @file filename.ts
 * @description Function description
 * @module ModuleName
 * @dependencies ./dependency1, ./dependency2
 * @lastModified YYYY-MM-DD
 */
```

### USERAGENTS.md Sections

See `references/useragents_template.md` for the standard structure.

## Coding Conventions by Tech Stack

The scanner automatically infers conventions based on detected tech stack. Common rules include:

**TypeScript/JavaScript:**
- Do not use `any` type - use `unknown` for unknown types
- All functions must have explicit return type declarations
- Use `interface` for objects, `type` for unions and complex types
- Enable all strict mode checks

**React:**
- Use function components and Hooks only
- PascalCase for component files
- Use React.memo() for optimization
- Use useMemo/useCallback to avoid unnecessary re-renders

**Go:**
- Follow Go official coding standards (Effective Go)
- Always handle errors explicitly
- Use gofmt for formatting

**Python:**
- Follow PEP 8 coding standards
- Use type hints
- Use f-strings and pathlib

**Common (all projects):**
- Do not use native fetch directly - use wrapped HTTP utility
- Do not hardcode sensitive information
- All async operations must have proper error handling

## Enforcement Mechanism

The skill adds mandatory instructions to `AGENTS.md/CLAUDE.md`:

1. **Pre-read requirement**: Agent must read USERAGENTS.md and relevant TECH_INFO.md before any modification
2. **Post-update requirement**: Agent must update documentation after any modification
3. **Structure sync**: Agent must check if USERAGENTS.md needs updating after task completion
4. **Hook enforcement**: Stop hook displays mandatory action list when files were modified

## File Structure

```
project/
├── AGENTS.md          # Contains enforcement instructions
├── USERAGENTS.md      # Project-level context (auto-generated)
├── .context-keeper/
│   └── pending.txt    # Tracks modified files (created by hooks)
├── src/
│   ├── TECH_INFO.md   # Directory-level documentation (created on-demand)
│   ├── components/
│   │   ├── TECH_INFO.md
│   │   └── Button.tsx # With file header comments
│   └── utils/
│       ├── TECH_INFO.md
│       └── http.ts
└── .gitignore         # Contains TECH_INFO.md and .context-keeper/
```

## Notes

- `TECH_INFO.md` files are added to `.gitignore` by default (local context only)
- `USERAGENTS.md` can be committed if desired for team sharing
- The scanner can be re-run to refresh documentation
- On-demand generation means only directories you actually work in will have documentation
- Hooks ensure documentation is updated even when using multiple skills
