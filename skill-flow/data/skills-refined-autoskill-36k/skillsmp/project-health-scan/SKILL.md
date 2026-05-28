---
name: project_health_scan
description: Generates a comprehensive health diagnostic report of the codebase, analyzing architecture, file structure, and technical debt.
---

# Project Health Scan Skill

**Goal**: Get a bird's-eye view of the project, identifying architectural risks and confusion points.

## Instructions

As a senior software architect, review the current codebase. Do not modify code immediately, but generate a "Project Health Diagnostic Report".

### 1. Analysis Focus Areas

- **Architecture Patterns**: Is the current architecture clear? Any mixed architectures causing confusion?
- **File Structure**: Are naming and directory structures semantic? "God classes" or oversized files?
- **Technical Debt**: Outdated dependencies, deprecated calls, or anti-patterns.
- **Major Risks**: Modules most prone to bugs.

### 2. Output Format

Output the report in Markdown table format, sorted by "Urgency".

| Urgency | Category | File/Module | Issue Description | Suggested Action |
|:-------:|:---------|:------------|:------------------|:-----------------|
| High    |          |             |                   |                  |

### 3. Execution

- Use `ls -R` or `list_dir` to map the structure.
- Read key files (`main`, `config`, core logic).
- Produce the report as a new artifact or a markdown file.
