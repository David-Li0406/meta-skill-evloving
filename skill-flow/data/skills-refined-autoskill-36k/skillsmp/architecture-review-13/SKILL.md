---
name: architecture-review
description: |
  Deep codebase analysis and architecture documentation for JavaScript/TypeScript ecosystems.
  Uses multi-agent analysis to understand structure, data flow, dependencies, patterns, and anomalies.
  Generates comprehensive documentation with mermaid diagrams.
---

# Architecture Review Skill

## Overview

This skill performs deep architecture analysis of JavaScript/TypeScript codebases, generating comprehensive documentation. It's designed for Node.js backends (Express, Fastify, Hono, NestJS), React/React Native frontends, and common JS tooling.

## Core Principles

1. **Discovery-first** - Detect stack and conventions before analyzing
2. **Depth over speed** - Thorough analysis, not quick scanning
3. **Surface the weird stuff** - Anomaly detection is key value
4. **Persistent history** - Track architectural changes over time
5. **Extensible design** - Scripts can run independently

## User Commands

| Command | Action |
|---------|--------|
| "Update the architecture docs" | Full multi-agent analysis |
| "Quick architecture scan" | Scripts only, skip deep agent analysis |
| "Compare to last review" | Generate diff report |
| "Focus on [area]" | Deep dive on specific domain |
| "Show architecture history" | Display timeline of changes |

---

## Phase 0: Discovery & Setup

### 1. Check for Existing Context

First, check if `.architecture-review/` directory exists:

```bash
ls -la .architecture-review/ 2>/dev/null
```

If it exists, read the config to understand previous context:

```bash
cat .architecture-review/config.json 2>/dev/null
```

### 2. Stack Detection

Run entry point detector to identify framework:

```bash
python3 {{SKILL_PATH}}/scripts/entry_point_detector.py .
```

### 3. Grounding Questions (First Run Only)

If this is the first architecture review, ask the user these grounding questions:

1. **What does this project do?** (1-2 sentences describing the purpose)
2. **What are the major features or modules?** (List main functional areas)
3. **Are there areas of the codebase that confuse you or feel messy?**
4. **Any known technical debt or legacy code areas?**

Save responses to `.architecture-review/config.json`:

```json
{
  "project_description": "...",
  "major_features": ["..."],
  "known_problem_areas": ["..."],
  "framework": "...",
  "last_review": "...",
  "created": "..."
}
```

### 4. Create Persistence Structure

```bash
mkdir -p .architecture-review/{scan-results,docs,history}
```

---

## Phase 1: Automated Scanning

Run all 7 analysis scripts and save their outputs. These can run in parallel.

### Scripts to Run

```bash
# File structure analysis
python3 {{SKILL_PATH}}/scripts/file_tree_analyzer.py . > .architecture-review/scan-results/file_tree.json

# Entry points
python3 {{SKILL_PATH}}/scripts/entry_point_detector.py . > .architecture-review/scan-results/entry_points.json

# Dependencies
python3 {{SKILL_PATH}}/scripts/dependency_mapper.py . > .architecture-review/scan-results/dependencies.json

# Dead code
python3 {{SKILL_PATH}}/scripts/dead_code_detector.py . > .architecture-review/scan-results/dead_code.json

# API surface
python3 {{SKILL_PATH}}/scripts/api_surface_extractor.py . > .architecture-review/scan-results/api_surface.json

# Configuration
python3 {{SKILL_PATH}}/scripts/config_extractor.py . > .architecture-review/scan-results/config.json

# Components (React/RN only)
python3 {{SKILL_PATH}}/scripts/component_census.py . > .architecture-review/scan-results/components.json
```

### Verify Scans

After running, read and verify each scan result:

```bash
cat .architecture-review/scan-results/file_tree.json | head -50
```

---

## Phase 2: Multi-Agent Deep Analysis

For full architecture reviews, spawn 5 parallel analysis agents. Each agent receives relevant script outputs and reference documentation.

### Agent 1: Structure Agent

**Purpose:** Analyze directory conventions, separation of concerns, module boundaries

**Input:**
- `file_tree.json`
- `entry_points.json`
- Reference: `ARCHITECTURE_PATTERNS.md`, `FRAMEWORK_CONVENTIONS.md`

**Questions to Answer:**
1. What organizational pattern is used (feature-based, layer-based, etc.)?
2. Are directory conventions consistent with the framework?
3. Are module boundaries clear and well-defined?
4. Are there misplaced files or confusing organization?

### Agent 2: Data Flow Agent

**Purpose:** Analyze state management, API communication, data persistence patterns

**Input:**
- `components.json` (if React)
- `api_surface.json`
- `dependencies.json`
- Reference: `ARCHITECTURE_PATTERNS.md`

**Questions to Answer:**
1. How does data flow through the application?
2. What state management approach is used?
3. How is API communication structured?
4. Are there data flow anti-patterns (prop drilling, etc.)?

### Agent 3: Dependency Agent

**Purpose:** Analyze internal coupling, circular dependencies, external dependency health

**Input:**
- `dependencies.json`
- `file_tree.json`

**Questions to Answer:**
1. What are the most connected/coupled modules?
2. Are there circular dependencies?
3. Are external dependencies well-chosen and up-to-date?
4. Is there over-reliance on specific packages?

### Agent 4: Patterns Agent

**Purpose:** Identify architectural patterns in use, assess consistency, detect anti-patterns

**Input:**
- All scan results
- Reference: `ARCHITECTURE_PATTERNS.md`, `FRAMEWORK_CONVENTIONS.md`

**Questions to Answer:**
1. What architectural patterns are being used?
2. Are patterns applied consistently?
3. Are there anti-patterns present?
4. What patterns should be introduced or removed?

### Agent 5: Anomaly Agent (CRITICAL)

**Purpose:** Find orphaned files, dead exports, abandoned features, inconsistencies

This agent is the key differentiator. It finds the weird stuff that makes this skill valuable.

**Input:**
- `dead_code.json`
- `dependencies.json`
- `file_tree.json`
- `config.json` (user's known problem areas)

**Questions to Answer:**
1. What files appear orphaned or unused?
2. What exports are never imported?
3. Are there signs of abandoned features?
4. What inconsistencies or anomalies stand out?
5. Where does the code not match its apparent intent?

---

## Phase 3: Report Generation

### Synthesize Agent Outputs

Combine insights from all 5 agents into coherent documentation.

### Generate ARCHITECTURE.md

Use the template at `{{SKILL_PATH}}/templates/ARCHITECTURE.md` and fill in:

1. **Executive Summary** - Key stats and one-paragraph description
2. **High-Level Diagram** - Mermaid diagram following `MERMAID_GUIDELINES.md`
3. **Directory Structure** - Annotated tree from file_tree.json
4. **Entry Points** - From entry_points.json
5. **Data Flow** - From Data Flow Agent
6. **Components** - From components.json (if React)
7. **API Surface** - From api_surface.json
8. **Dependencies** - From dependencies.json
9. **Patterns** - From Patterns Agent
10. **Anomalies** - From Anomaly Agent and dead_code.json
11. **Recommendations** - Synthesized suggestions

### Generate ARCHITECTURE_TLDR.md

Use template at `{{SKILL_PATH}}/templates/ARCHITECTURE_TLDR.md`:

- One-paragraph description
- Simple mermaid diagram (5-10 nodes max)
- Stack summary
- Top 5 key components
- 3 notable patterns
- Red flags (if any)
- 3 recommended next steps

### Save Documentation

```bash
cp generated_docs/ARCHITECTURE.md .architecture-review/docs/
cp generated_docs/ARCHITECTURE_TLDR.md .architecture-review/docs/
```

### Create History Snapshot

```bash
DATE=$(date +%Y-%m-%d)
mkdir -p .architecture-review/history/$DATE
cp -r .architecture-review/scan-results .architecture-review/history/$DATE/
cp .architecture-review/docs/ARCHITECTURE.md .architecture-review/history/$DATE/
```

Create summary.json for quick comparison:

```json
{
  "date": "YYYY-MM-DD",
  "total_files": 0,
  "total_loc": 0,
  "components": 0,
  "routes": 0,
  "circular_deps": 0,
  "orphaned_files": 0,
  "todos": 0
}
```

---

## Phase 4: Comparison (If Previous Review Exists)

If `.architecture-review/history/` has previous snapshots:

### Generate COMPARISON_REPORT.md

Use template at `{{SKILL_PATH}}/templates/COMPARISON_REPORT.md`:

1. Load previous summary.json
2. Compare metrics
3. Diff file lists
4. Identify new/removed/changed components
5. Track anomaly resolution

```bash
cp generated_docs/COMPARISON_REPORT.md .architecture-review/docs/
```

---

## Quick Scan Mode

When user requests "Quick architecture scan":

1. Run Phase 1 (Automated Scanning) only
2. Skip Phase 2 (Multi-Agent Analysis)
3. Generate basic summary from scan results
4. Do not generate full ARCHITECTURE.md

Output a concise summary:

```
## Quick Scan Results

- **Files:** X total, Y components, Z utilities
- **Framework:** Next.js App Router
- **Entry Points:** X detected
- **Routes:** X API endpoints
- **Issues:** X orphaned files, Y circular deps, Z TODOs
```

---

## Focus Mode

When user requests "Focus on [area]":

1. Run relevant subset of scripts
2. Spawn single deep-dive agent for that area
3. Generate focused report

Areas and their focus:
- **components** - Deep component_census analysis
- **api** - Deep api_surface analysis
- **dependencies** - Deep dependency_mapper analysis
- **dead code** - Deep dead_code_detector analysis
- **config** - Deep config_extractor analysis

---

## Output Locations

All outputs go to `.architecture-review/`:

```
.architecture-review/
├── config.json              # Project context and settings
├── scan-results/            # Latest JSON outputs from scripts
│   ├── file_tree.json
│   ├── entry_points.json
│   ├── dependencies.json
│   ├── dead_code.json
│   ├── api_surface.json
│   ├── config.json
│   └── components.json
├── docs/                    # Generated documentation
│   ├── ARCHITECTURE.md
│   ├── ARCHITECTURE_TLDR.md
│   └── COMPARISON_REPORT.md
└── history/                 # Historical snapshots
    └── YYYY-MM-DD/
        ├── scan-results/
        ├── ARCHITECTURE.md
        └── summary.json
```

---

## Reference Files

When analyzing, consult these reference documents:

- `{{SKILL_PATH}}/references/ARCHITECTURE_PATTERNS.md` - Pattern detection guidance
- `{{SKILL_PATH}}/references/FRAMEWORK_CONVENTIONS.md` - Framework-specific conventions
- `{{SKILL_PATH}}/references/MERMAID_GUIDELINES.md` - Diagram generation rules

---

## Important Notes

1. **Always run stack detection first** - Don't assume the framework
2. **The Anomaly Agent is key** - This surfaces the value for vibe-coded projects
3. **Keep diagrams simple** - 5-10 nodes for high-level views
4. **Preserve history** - Always create snapshots for comparison
5. **Be thorough but focused** - Document what matters, not everything
6. **This skill documents, it doesn't fix** - Recommendations only, no auto-fixes

---

## What This Skill Does NOT Do

- Security analysis (use security-audit skill)
- Performance profiling
- Code quality scoring
- Automatic refactoring
- Test coverage analysis

This skill explains architecture. It doesn't judge code quality or fix problems.
