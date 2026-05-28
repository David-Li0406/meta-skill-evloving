---
name: docs-generator
description: Autonomously analyzes a repository, detects architectural and coding patterns, and generates/updates a docs/ folder with a root CLAUDE.md as table of contents. Use when asked to generate documentation, create CLAUDE.md, document architecture, or bootstrap docs for a project.
allowed-tools: Read, Bash, Grep, Glob, Task, Write, Edit
---

# Documentation Generator

Autonomous documentation generation: audit existing docs → deeply analyze code → detect patterns → generate structured docs.

**Core principle**: Documentation must reflect what the code *actually does*, not theoretical patterns. Every claim should have evidence from the codebase.

## Usage

```bash
/docs-generator
```

## Output Structure

```
project-root/
├── CLAUDE.md                              # TOC + project summary + quick-start
├── docs/
│   ├── architecture/                      # Knowledge base (why, not how)
│   │   ├── 01-overview.md
│   │   ├── 02-directory-structure.md
│   │   ├── 03-core-components.md
│   │   └── 04-data-flow.md
│   ├── standards/                         # Coding standards
│   │   ├── naming-conventions.md          # General standards at root
│   │   ├── error-handling.md
│   │   ├── backend/                       # Subfolder only if applicable
│   │   └── frontend/                      # Subfolder only if applicable
│   └── onboarding/                        # Getting started (how)
│       ├── 01-setup.md
│       └── 02-first-contribution.md
```

## Workflow

Execute phases sequentially. Each phase builds on previous results.

### Phase 0: Existing Documentation Audit

**Before any analysis**, inventory and evaluate existing documentation.

**Actions:**

1. Check for existing docs:
   - `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`
   - `docs/` folder contents
   - Inline code comments (especially module-level)

2. For each existing doc, evaluate:
   - **Keep**: Well-written, accurate, valuable
   - **Update**: Good structure but outdated/incomplete
   - **Replace**: Inaccurate or poorly organized
   - **Missing**: Topics not covered

3. Create audit report:

```
Existing Documentation Audit:

KEEP (preserve as-is):
- [file]: [reason]

UPDATE (preserve structure, refresh content):
- [file]: [what needs updating]

REPLACE (rewrite entirely):
- [file]: [why]

MISSING (create new):
- [topic]: [why needed]
```

**Goal**: Preserve good existing documentation. Don't regenerate what's already well-documented.

### Phase 1: Deep Code Understanding

Launch `feature-dev:code-explorer` agent to analyze repository deeply.

**Agent prompt:**
```
Analyze this repository to understand how the code actually works. Don't just scan config files—read source code implementations.

Goals:
1. Understand what the codebase does and HOW it does it
2. Trace primary execution paths from entry points through the codebase
3. Identify the core abstractions and patterns that define the architecture
4. Map component relationships through actual imports and dependencies

Analysis approach:
1. **Entry points**: Find main entry points (main.ts, index.js, app.py, main.go, etc.) and trace execution
2. **Core modules**: Identify the most-imported/most-referenced modules—these are architectural pillars
3. **Data flow**: Trace how data moves from input → processing → output
4. **Abstractions**: Find base classes, interfaces, traits that define contracts
5. **Dependencies**: Map what depends on what (internal module graph)

Output a structured report with:
- Primary execution flow (which modules call which)
- Core abstractions with their responsibilities and directory locations
- Module dependency graph (what imports what)
- Key design patterns observed
- Infrastructure/config discovered
```

### Phase 2: Architecture Documentation Design

Launch `feature-dev:code-architect` agent to design architecture documentation grounded in actual code.

**Agent prompt:**
```
Based on the deep code analysis, design architecture documentation that reflects what the code ACTUALLY does.

Requirements:
1. **Grounded in code**: Architectural claims must reflect actual code structure
2. **Illustrative examples**: Include simplified code snippets that demonstrate patterns (not verbatim sensitive code)
3. **Accurate diagrams**: Mermaid diagrams should represent real code organization
4. **Inferred rationale**: Deduce "why" from code structure—don't assume or guess

Design:
1. **Pattern identification**:
   - Architecture style: What pattern does the code follow? (based on directory structure, import patterns)
   - Design patterns: What patterns are actually used?
   - Infrastructure: What's actually configured?

2. **Diagram design**:
   - High-level system overview
   - Data flow diagram showing how data moves through modules
   - Module relationships derived from import graph

3. **Decision documentation**:
   - Infer rationale from code structure
   - Note trade-offs visible in the implementation
   - Document boundaries as they actually exist

Output:
- Architecture style classification with rationale
- Mermaid diagrams representing system structure
- Simplified illustrative code examples for key patterns
- Architectural decisions with inferred rationale
```

### Phase 3: Standards Detection

Analyze codebase for actual conventions. Consult `./references/detection-patterns.md` for comprehensive detection patterns.

**Key areas to analyze:**

1. **Naming conventions**: File naming, variable/function naming, class/component naming
2. **Code patterns**: Error handling, logging, testing, API design
3. **Config-driven standards**: ESLint, Prettier, rustfmt, etc.
4. **Inconsistencies**: Note variations that should be standardized

**For each detected pattern:**
- Describe the pattern clearly
- Create illustrative do/don't examples
- Note whether it's consistently followed

### Phase 3.5: Documentation Reconciliation

Before generating, reconcile detected patterns with existing documentation.

**Compare:**
1. Patterns detected in Phase 3 vs what existing docs say
2. Architecture observed in Phases 1-2 vs existing architecture docs
3. Commands/setup in config files vs existing onboarding docs

**Decide for each doc:**
- **Preserve**: Existing doc is accurate and well-written
- **Merge**: Existing doc has good content, add missing info
- **Replace**: Existing doc is significantly wrong or outdated

**Output reconciliation plan:**
```
Documentation Reconciliation:

docs/architecture/01-overview.md:
  Status: MERGE
  Keep: System diagram, high-level description
  Add: New module discovered in Phase 1
  Update: Data flow section (outdated)

docs/standards/error-handling.md:
  Status: REPLACE
  Reason: Documents try/catch but code uses Result types throughout
```

### Phase 4: Documentation Generation

Generate documentation using templates from `./references/`, incorporating evidence from previous phases.

#### Step 4.1: Architecture Docs

Generate `docs/architecture/` (numbered, knowledge base style):

| File | Content |
|------|---------|
| `01-overview.md` | High-level system overview with mermaid diagram |
| `02-directory-structure.md` | Repo layout with rationale for organization |
| `03-core-components.md` | Main modules/services and responsibilities |
| `04-data-flow.md` | How data moves through system and why |

Use `./references/architecture-templates.md` for structure.

**Key principles**:
- Explain "why" (decisions, rationale, constraints), NOT "how to" (tutorials)
- Reference directories/modules (stable), not line numbers (unstable)
- Use simplified examples that illustrate patterns without exposing sensitive code

#### Step 4.2: Standards Docs

Generate `docs/standards/`:

- Root level: General/cross-cutting standards
  - `naming-conventions.md`
  - `error-handling.md`
  - `testing.md`
  - `logging.md`

- Subfolders only for specific domains (if detected):
  - `backend/` — API design, database patterns
  - `frontend/` — Component patterns, state management, styling

Use `./references/standards-templates.md` for structure.

**Format**: Clearly distinguish:
- **Detected** (what the code actually does) — with file references
- **Recommended** (best practices, whether followed or suggested)

#### Step 4.3: Onboarding Docs

Generate `docs/onboarding/` (numbered, tutorial style):

| File | Content |
|------|---------|
| `01-setup.md` | Environment setup, prerequisites, installation |
| `02-first-contribution.md` | Making your first change, PR workflow |

Use `./references/onboarding-templates.md` for structure.

**Key principle**: Full tutorials that LINK to (not repeat) architecture/standards content.

#### Step 4.4: Root CLAUDE.md

Generate `CLAUDE.md` at repository root using `./references/claude-md-template.md`.

**Required sections (in order):**

1. **CRITICAL section** (near top): Instruct agents to ALWAYS consult docs before acting
2. **Project summary**: 2-3 lines describing the project
3. **Quick-start commands**: Discovered from config files
4. **Table of contents**: Links to all docs

**Command discovery priority:**
1. `justfile` → use `just <command>`
2. `package.json` with `packageManager` field → use that package manager
3. `Makefile` → use `make <target>`
4. Default to detected package manager conventions

## Naming Conventions

- All doc filenames: **kebab-case** (`error-handling.md`, not `errorHandling.md`)
- Architecture files: **numbered prefix** (`01-overview.md`)
- Onboarding files: **numbered prefix** (`01-setup.md`)
- Standards files: **no numbered prefix** (`naming-conventions.md`)

## Reference Files

| File | Purpose |
|------|---------|
| `./references/claude-md-template.md` | Template for root CLAUDE.md |
| `./references/architecture-templates.md` | Templates for architecture docs |
| `./references/standards-templates.md` | Templates for standards docs |
| `./references/onboarding-templates.md` | Templates for onboarding guides |
| `./references/detection-patterns.md` | Config → framework mapping, grep patterns |

## Verification Checklist

After generation, verify:

**Structure:**
- [ ] Structure matches expected layout
- [ ] All filenames use kebab-case
- [ ] Architecture files have numbered prefixes and explain "why"
- [ ] Onboarding files have numbered prefixes and are full tutorials
- [ ] Standards files have no numbered prefix
- [ ] Subfolders only exist where domain-specific content detected

**Content quality:**
- [ ] CLAUDE.md has CRITICAL section at top
- [ ] Quick-start commands use correct package manager
- [ ] Mermaid diagrams are valid

**Quality:**
- [ ] Examples are illustrative (not verbatim sensitive code)
- [ ] Standards docs are skimmable with clear do/don't examples
- [ ] Standards docs distinguish "detected" vs "recommended"
- [ ] Architecture docs explain structure and rationale

**Preservation:**
- [ ] Existing good documentation preserved (per Phase 0 audit)
- [ ] Outdated documentation identified and replaced
- [ ] Onboarding docs link to (not duplicate) other docs
