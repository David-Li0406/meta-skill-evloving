<!--
Embedded Cartographer Command: chart
Standalone version for plugin-free operation
-->
---
allowed-tools: Task, Glob, Grep, Read, Write, Bash(mkdir:*), Bash(test:*), Bash(ls:*), AskUserQuestion
argument-hint: [project context]
description: Generate a complete atlas skill for codebase navigation
---

## Context

Arguments: `/chart [CONTEXT]`
- **[CONTEXT]** - Optional user-provided context about the project (type, architecture, focus areas)

Current directory: !`pwd`

## Workflow

### 1. Pre-flight Checks

**Check for existing atlas:**
```bash
test -d ".claude/skills/atlas" && echo "EXISTS" || echo "NOT_FOUND"
```

**If atlas exists:**
- Use AskUserQuestion: "Atlas already exists. How to proceed?"
  - "Use /rechart to update" → Abort with instruction
  - "Overwrite existing atlas" → Continue with warning
  - "Cancel" → Abort

**Check write permissions:**
```bash
mkdir -p .claude/skills/atlas/references && echo "WRITABLE" || echo "NO_PERMISSION"
```

### 2. Analyze Codebase

You need to analyze the codebase to understand its structure. Follow these steps:

**Step 2.1: Identify Project Type**

Check config files to detect project type:
- Read package.json, requirements.txt, go.mod, Cargo.toml
- Look for framework indicators (react, express, django, etc.)
- Check for monorepo indicators (packages/, apps/, turbo.json)

Assign type: frontend_spa | backend_api | fullstack | monorepo | cli | library

**Step 2.2: Extract Technology Stack**

Document from config files:
- Language and version
- Framework and version
- Database/ORM (if applicable)
- State management, styling (frontend)
- Testing framework, build tools

**Step 2.3: Map Directory Structure**

Explore top-level directories:
- Skip: node_modules, dist, build, .git, coverage, __pycache__
- Document: src structure, test location, config files

**Step 2.4: Identify Domains**

For each significant directory:
- Name (snake_case identifier)
- Location (path)
- Purpose (ONE clear sentence)
- File count (exact or ~approximate)
- Key files
- Confidence: high/medium/low

**Step 2.5: Detect File Patterns**

Find naming conventions:
- Component patterns: *.component.tsx, {Name}/{Name}.tsx
- Service patterns: *.service.ts
- Test patterns: *.test.ts, *.spec.ts

**Step 2.6: Identify Validation Commands**

Find commands for type checking, testing, linting, building.

### 3. Handle Low Confidence

For any LOW confidence detections:
- Use AskUserQuestion to confirm with user
- Apply user input with HIGH confidence

### 4. Generate Atlas Files

**Create schema.yaml:**
`.claude/skills/atlas/references/schema.yaml`

```yaml
# {project_name} - Codebase Schema
# Machine-readable structure for AI agent navigation
# Last Updated: {timestamp}

metadata:
  project: {project_name}
  type: {project_type}
  stack:
    language: {language}
    version: '{version}'
    framework: {framework}
    framework_version: '{framework_version}'
    # Add type-specific fields
  architecture: {architecture_description}

domains:
  {domain_name}:
    location: {path}
    count: {file_count}
    purpose: {one_sentence}
    confidence: {high|medium|low}
    key_files:
      - {file1}
      - {file2}
    documentation: {domain}/{area}.md

file_patterns:
  {pattern_name}:
    pattern: {glob}
    count: {count}
    purpose: {purpose}
    example: {example_file}

config_files:
  - {path}: {purpose}

testing:
  framework: {framework}
  location: {location}
  pattern: '{pattern}'
  coverage: {command}

validation:
  working_dir: {directory}
  commands:
    - name: {name}
      command: {command}
```

**Create SKILL.md:**
`.claude/skills/atlas/SKILL.md`

```markdown
---
name: atlas
description: >-
  **Primary codebase discovery tool for {project_name}.** ALWAYS invoke this skill FIRST
  when you need to: find files, locate components, understand where code lives.
---

# {project_name} Codebase Discovery

## Project Structure

{ascii_tree}

## Domain Router

| Keywords | Reference |
|----------|-----------|
| {keywords} | [references/{path}](references/{path}) |

## Pattern Router

| Task | Pattern Guide |
|------|---------------|
| {task} | [references/patterns/{pattern}.md](references/patterns/{pattern}.md) |

## File Location Conventions

| Type | Path Pattern |
|------|--------------|
| {type} | `{pattern}` |

## Key Technologies

- {technology_list}

## Full Structure

For complete structure: [references/schema.yaml](references/schema.yaml)
```

**Create domain references:**
For each domain, create `.claude/skills/atlas/references/{area}/{domain}.md`

**Create pattern guides:**
For detected patterns, create `.claude/skills/atlas/references/patterns/{pattern}.md`

### 5. Validate and Report

**Validate:**
- All paths exist
- No broken links
- Valid YAML

**Report:**
```markdown
## Atlas Generated Successfully

**Location:** `.claude/skills/atlas/`

**Summary:**
- Project type: {type}
- Domains identified: {count}
- File patterns detected: {count}

**Next steps:**
- Run `/atlas` to use the skill
- Run `/calibrate` to verify accuracy
```
