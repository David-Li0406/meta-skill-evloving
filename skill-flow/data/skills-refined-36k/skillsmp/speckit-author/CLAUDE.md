---
type: claude-context
directory: .claude/skills/speckit-author
purpose: SpecKit Author provides **interactive callable tools** for creating and managing specifications in feature/release/hotfix worktrees. It implements the SpecKit phase of the workflow, generating detailed specifications (spec.md) and implementation plans (plan.md) through interactive Q&A sessions.
parent: null
sibling_readme: README.md
children:
  - ARCHIVED/CLAUDE.md
  - scripts/CLAUDE.md
  - templates/CLAUDE.md
related_skills:
  - workflow-orchestrator
  - bmad-planner
  - workflow-utilities
  - git-workflow-manager
  - agentdb-state-manager
---

# Claude Code Context: speckit-author

## Purpose

SpecKit Author provides **interactive callable tools** for creating and managing specifications in feature/release/hotfix worktrees. It implements the SpecKit phase of the workflow, generating detailed specifications (spec.md) and implementation plans (plan.md) through interactive Q&A sessions.

> **Note**: As of v5.12.0, workflow tasks are now stored in `specs/*/tasks.md` instead of TODO_*.md files. Workflow state is tracked via AgentDB. See `agentdb-state-manager` for the current system.

## Directory Structure

```
.claude/skills/speckit-author/
├── scripts/                      # Interactive callable tools
│   ├── create_specifications.py  # Main SpecKit tool (Phase 2)
│   ├── update_asbuilt.py         # As-built updates (Phase 4)
│   └── __init__.py              # Package initialization
├── templates/                    # Markdown templates
│   ├── spec.md.template          # Technical specification template (297 lines)
│   └── plan.md.template          # Implementation plan template (367 lines)
├── SKILL.md                      # Complete skill documentation
├── CLAUDE.md                     # This file
├── README.md                     # Human-readable overview
└── ARCHIVED/                     # Deprecated files
```

## Key Scripts

### create_specifications.py

**Purpose:** Interactive tool to create spec.md and plan.md in worktrees

**When to use:** Phase 2.3 (after creating feature worktree, before implementation)

**Invocation:**
```bash
# From feature worktree
python .claude/skills/speckit-author/scripts/create_specifications.py \
  feature my-feature stharrold \
  --todo-file ../TODO_feature_20251024_my-feature.md
```

**What it does:**
1. Detects BMAD planning context (../planning/<slug>/)
2. Conducts interactive Q&A (5-15 questions)
3. Generates spec.md and plan.md from templates
4. Creates specs/<slug>/ directory with CLAUDE.md, README.md, ARCHIVED/
5. Updates TODO_*.md with tasks from plan.md
6. Commits changes to feature branch

**Key features:**
- Adapts Q&A based on BMAD availability
- Auto-detects TODO file
- Parses plan.md tasks and updates TODO frontmatter
- Creates compliant directory structure
- Error handling and validation

### update_asbuilt.py

**Purpose:** Update BMAD planning with as-built implementation details

**When to use:** Phase 4.4 (after PR merge to contrib branch)

**Invocation:**
```bash
# From main repo on contrib branch
python .claude/skills/speckit-author/scripts/update_asbuilt.py \
  planning/my-feature specs/my-feature
```

**What it does:**
1. Reads as-built specs from specs/<slug>/
2. Compares with original BMAD planning
3. Conducts interactive Q&A about deviations and metrics
4. Updates planning/ files with "As-Built" sections
5. Commits changes to contrib branch

**Key features:**
- Auto-detects technology deviations
- Gathers epic completion metrics
- Documents lessons learned
- Creates feedback loop for future planning

## Usage by Claude Code

### When Called by Workflow Orchestrator (Phase 2.3)

**Context:** In feature worktree, need to create specifications

**Orchestrator calls:**
```python
import subprocess

result = subprocess.run([
    'python',
    '.claude/skills/speckit-author/scripts/create_specifications.py',
    'feature',  # workflow_type
    'my-feature',  # slug
    'stharrold',  # gh_user
    '--todo-file', '../TODO_feature_20251024_my-feature.md'
], check=True)
```

**Claude Code should:**
1. Recognize this is Phase 2.3
2. Call the script (don't reproduce its functionality)
3. Let the script handle:
   - Interactive Q&A with user
   - BMAD context detection
   - Template processing
   - TODO updates
   - Git commit
4. After script completes, move to Phase 2.4 (implementation)

### When Called for As-Built Updates (Phase 4.4)

**Context:** Main repo, contrib branch, after PR merge

**Orchestrator calls:**
```python
import subprocess

result = subprocess.run([
    'python',
    '.claude/skills/speckit-author/scripts/update_asbuilt.py',
    'planning/my-feature',
    'specs/my-feature'
], check=True)
```

**Claude Code should:**
1. Recognize this is Phase 4.4 (feedback loop)
2. Call the script
3. Let the script handle:
   - Deviation analysis
   - Metrics gathering
   - Planning document updates
   - Git commit

## Integration with Other Skills

**workflow-orchestrator:**
- Orchestrator calls SpecKit scripts at appropriate phases
- Phase 2.3: create_specifications.py
- Phase 4.4: update_asbuilt.py (optional)

**bmad-planner:**
- BMAD creates planning/ documents in Phase 1
- SpecKit reads planning/ context in Phase 2
- SpecKit updates planning/ with as-built in Phase 4

**workflow-utilities:**
- SpecKit uses directory_structure patterns
- TODO updates follow same YAML format

**git-workflow-manager:**
- SpecKit runs in worktrees created by git-workflow-manager
- Both handle git commits with similar message format

## Token Efficiency

**Before (Manual SpecKit):**
- Claude Code reproduces SpecKit functionality each time
- ~2,000-3,000 tokens per feature for Q&A and generation

**After (Callable Tool):**
- Claude Code calls script once
- Script handles all logic
- ~200-300 tokens to invoke script
- **Savings: ~1,700-2,700 tokens per feature**

## Templates

### spec.md.template

**Placeholders:**
- `{{TITLE}}`: Feature name (title case)
- `{{WORKFLOW_TYPE}}`: feature, release, or hotfix
- `{{SLUG}}`: Feature slug (kebab-case)
- `{{DATE}}`: Creation date (YYYY-MM-DD)
- `{{GH_USER}}`: GitHub username

**Sections:**
- Overview
- Requirements Reference (links to BMAD)
- Detailed Specification (components, implementation)
- Testing Strategy
- Deployment Considerations

### plan.md.template

**Placeholders:** Same as spec.md.template

**Sections:**
- Task Breakdown (by phase or epic)
- Task format: Task ID, Description, Steps, Acceptance Criteria, Dependencies
- Verification commands

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation with examples
- **[README.md](README.md)** - Human-readable overview

**Child Directories:**
- **[scripts/](scripts/)** - Interactive Python tools
- **[templates/](templates/)** - Markdown templates
- **[ARCHIVED/CLAUDE.md](ARCHIVED/CLAUDE.md)** - Archived files

## Related Skills

- **workflow-orchestrator** - Calls SpecKit scripts
- **bmad-planner** - Creates planning context
- **workflow-utilities** - Shared utilities
- **git-workflow-manager** - Worktree management
