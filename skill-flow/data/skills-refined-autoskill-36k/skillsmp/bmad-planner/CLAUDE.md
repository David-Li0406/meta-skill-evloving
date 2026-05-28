---
type: claude-context
directory: .claude/skills/bmad-planner
purpose: BMAD Planner provides an **interactive callable tool** for creating planning documents in the main repository on contrib branches. It implements Phase 1 (Planning) of the workflow, generating comprehensive requirements, architecture, and epic breakdown through a three-persona interactive Q&A system.
parent: null
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
  - scripts/CLAUDE.md
  - templates/CLAUDE.md
related_skills:
  - **workflow-orchestrator** - Calls create_planning.py script
  - **speckit-author** - Reads planning context
  - **workflow-utilities** - Shared utilities
  - **git-workflow-manager** - Branch and worktree management
---

# Claude Code Context: bmad-planner

## Purpose

BMAD Planner provides an **interactive callable tool** for creating planning documents in the main repository on contrib branches. It implements Phase 1 (Planning) of the workflow, generating comprehensive requirements, architecture, and epic breakdown through a three-persona interactive Q&A system.

## Directory Structure

```
.claude/skills/bmad-planner/
├── scripts/                      # Interactive callable tools
│   ├── create_planning.py        # Main BMAD tool (Phase 1)
│   └── __init__.py              # Package initialization
├── templates/                    # Markdown templates
│   ├── requirements.md.template  # Business requirements template (170 lines)
│   ├── architecture.md.template  # Technical architecture template (418 lines)
│   └── epics.md.template        # Epic breakdown template (245 lines)
├── SKILL.md                      # Complete skill documentation
├── CLAUDE.md                     # This file
├── README.md                     # Human-readable overview
└── ARCHIVED/                     # Deprecated files
```

## Key Scripts

### create_planning.py

**Purpose:** Interactive tool to create requirements.md, architecture.md, epics.md in main repo

**When to use:** Phase 1 (before creating feature worktree)

**Location requirement:** Must run from main repository on contrib/<gh-user> branch (NOT in worktree)

**Invocation:**
```bash
# From main repo on contrib branch
python .claude/skills/bmad-planner/scripts/create_planning.py \
  <slug> <gh_user>
```

**Example:**
```bash
python .claude/skills/bmad-planner/scripts/create_planning.py \
  my-feature stharrold
```

**What it does:**
1. Validates location (main repo, contrib branch)
2. Conducts three-persona interactive Q&A:
   - 🧠 BMAD Analyst: Requirements gathering (5-10 questions)
   - 🏗️ BMAD Architect: Architecture design (5-8 questions)
   - 📋 BMAD PM: Epic breakdown (automatic analysis)
3. Generates requirements.md, architecture.md, epics.md from templates
4. Creates planning/<slug>/ directory with CLAUDE.md, README.md, ARCHIVED/
5. Commits changes to contrib branch

**Key features:**
- Three-persona Q&A system (Analyst, Architect, PM)
- Template processing with Q&A injection
- Automatic epic breakdown generation
- Creates compliant directory structure
- Error handling and validation
- Git commit with descriptive message

## Usage by Claude Code

### When Called by Workflow Orchestrator (Phase 1)

**Context:** Main repository, contrib/<gh-user> branch, need planning documents

**Orchestrator calls:**
```python
import subprocess

result = subprocess.run([
    'python',
    '.claude/skills/bmad-planner/scripts/create_planning.py',
    'my-feature',  # slug
    'stharrold',  # gh_user
], check=True)
```

**Claude Code should:**
1. Recognize this is Phase 1 (Planning)
2. Call the script (don't reproduce its functionality)
3. Let the script handle:
   - Interactive Q&A with user (three personas)
   - Template processing
   - Directory creation
   - Git commit
4. After script completes, move to Phase 2 (create worktree, then SpecKit)

### Token Efficiency

**Before (Manual Approach):**
- Claude Code manually conducts Q&A
- Claude Code manually generates requirements.md, architecture.md, epics.md
- ~2,500 tokens per feature

**After (Callable Tool):**
- Claude Code calls script once
- Script handles all logic
- ~200 tokens to invoke script
- **Savings: ~2,300 tokens per feature (92% reduction)**

## Integration with Other Skills

**workflow-orchestrator:**
- Orchestrator calls create_planning.py at Phase 1
- BMAD creates planning/ documents before worktree creation

**speckit-author:**
- SpecKit's create_specifications.py reads planning/ context in Phase 2
- SpecKit auto-detects ../planning/<slug>/ from feature worktrees
- Adaptive Q&A: 5-8 questions (with BMAD) vs 10-15 (without BMAD)
- **Token savings: ~1,700-2,700 tokens by reusing BMAD context**

**workflow-utilities:**
- BMAD uses directory_structure patterns for compliant directories
- Planning docs follow same YAML/markdown standards

**git-workflow-manager:**
- BMAD runs before worktree creation
- Both handle git commits with similar message format

## Templates

### requirements.md.template

**Placeholders:**
- `{{TITLE}}`: Feature name (title case)
- `{{DATE}}`: Creation date (YYYY-MM-DD)
- `{{GH_USER}}`: GitHub username

**Sections:**
- Business Context (problem statement, stakeholders, success criteria)
- Functional Requirements (FR-001, FR-002, ... with acceptance criteria)
- Non-Functional Requirements (performance, security, scalability)
- User Stories and Scenarios
- Risks and Constraints

### architecture.md.template

**Placeholders:** Same as requirements.md.template

**Sections:**
- System Overview (high-level architecture diagram)
- Technology Stack (language, framework, database, tools)
- Components and Interfaces
- Data Models and API Contracts
- Container Architecture (Containerfile, podman-compose.yml)
- Security and Error Handling
- Testing Strategy
- Deployment and Observability

### epics.md.template

**Placeholders:** Same as requirements.md.template

**Sections:**
- Epic Summary Table
- Epic Definitions (E-001, E-002, ...)
- Scope, Complexity, Priority for each epic
- Dependencies and Critical Path
- Implementation Timeline
- Effort Estimates

## Output Structure

Planning documents are created in:

```
planning/
└── <slug>/
    ├── requirements.md      # From 🧠 Analyst Q&A
    ├── architecture.md      # From 🏗️ Architect Q&A
    ├── epics.md            # From 📋 PM analysis
    ├── CLAUDE.md           # Context for this planning
    ├── README.md           # Human-readable overview
    └── ARCHIVED/           # Deprecated planning documents
        ├── CLAUDE.md
        └── README.md
```

## Interactive Q&A Examples

### 🧠 BMAD Analyst (Requirements)

**Questions asked:**
- What problem does this feature solve?
- Who are the primary users?
- How will we measure success?
- Functional requirements (FR-001, FR-002, ...)
- Acceptance criteria for each FR
- Performance requirements?
- Security requirements?
- Scalability requirements?
- Constraints and assumptions?

**Output:** requirements.md with complete business context

### 🏗️ BMAD Architect (Architecture)

**Questions asked:**
- Web framework? (FastAPI / Flask / Django / None)
- Database? (SQLite / PostgreSQL / MySQL / None)
- Database migration strategy? (Alembic / Manual SQL / None)
- Testing framework? (pytest / unittest / other)
- Use containerization (Podman)?
- Container strategy? (Single / Multi-container / Custom)
- Architecture pattern? (Layered / Modular / Monolithic)
- API style? (REST / GraphQL / RPC) [if web framework]
- Authentication method? [if security required]
- Authorization method? [if security required]
- Error handling strategy?
- Logging approach?
- Deployment target?

**Output:** architecture.md with complete technical design

### 📋 BMAD PM (Epic Breakdown)

**Process (automatic, no Q&A):**
1. Read requirements.md (functional requirements count, complexity)
2. Read architecture.md (technology stack, components)
3. Analyze and generate epics:
   - E-001: Data Layer (if database used)
   - E-002: Core Business Logic (always)
   - E-003: API Layer (if web framework used)
   - E-004: Testing & Quality (always)
   - E-005: Containerization (if containers used)
4. Determine complexity, priority, dependencies
5. Estimate effort based on FR count and technology

**Output:** epics.md with complete epic breakdown

## Workflow Integration

**Phase 1 (BMAD Planning):**
- Location: Main repo, contrib branch
- Tool: create_planning.py
- Output: planning/<slug>/
- Next: Create feature worktree

**Phase 2 (SpecKit):**
- Location: Feature worktree
- Tool: create_specifications.py
- Input: ../planning/<slug>/ (auto-detected)
- Output: specs/<slug>/

**Phase 4 (As-Built Feedback):**
- Location: Main repo, contrib branch (after PR merge)
- Tool: update_asbuilt.py
- Input: specs/<slug>/
- Output: Updates planning/<slug>/ with "As-Built" sections

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation with examples
- **[README.md](README.md)** - Human-readable overview

**Child Directories:**
- **[scripts/](scripts/)** - Interactive Python tools
- **[templates/](templates/)** - Markdown templates
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived files

## Related Skills

- **workflow-orchestrator** - Calls create_planning.py script
- **speckit-author** - Reads planning context
- **workflow-utilities** - Shared utilities
- **git-workflow-manager** - Branch and worktree management
