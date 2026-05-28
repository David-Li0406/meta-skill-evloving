---
type: directory-documentation
directory: .claude/skills/speckit-author
title: SpecKit Author
sibling_claude: CLAUDE.md
parent: null
children:
  - ARCHIVED/README.md
---

# SpecKit Author

## Overview

SpecKit Author is an interactive tool for creating detailed technical specifications and implementation plans for software features. It runs as a Python script in feature/release/hotfix worktrees and generates two key documents:

1. **spec.md** - Detailed technical specification
2. **plan.md** - Implementation task breakdown

## What Problem Does It Solve?

When starting a new feature, developers need to:
- Understand requirements and architecture
- Break down work into manageable tasks
- Align implementation with planning documents
- Track tasks in TODO files

SpecKit automates this process through interactive Q&A, generating consistent, well-structured specifications that integrate with the repository's workflow system.

## How It Works

### Phase 2: Creating Specifications

**In a feature worktree, run:**
```bash
python .claude/skills/speckit-author/scripts/create_specifications.py \
  feature my-feature username
```

**The script will:**
1. **Detect context** - Check for BMAD planning documents in `../planning/my-feature/`
2. **Ask questions** - Conduct interactive Q&A about implementation preferences
3. **Generate specs** - Create `spec.md` and `plan.md` from templates
4. **Update TODO** - Parse tasks from `plan.md` and update `TODO_*.md`
5. **Commit changes** - Save everything to the feature branch

### Phase 4: Updating Planning (Optional)

**After implementation, from main repo:**
```bash
python .claude/skills/speckit-author/scripts/update_asbuilt.py \
  planning/my-feature specs/my-feature
```

**The script will:**
1. **Compare** - Analyze differences between planning and implementation
2. **Gather metrics** - Ask about effort, performance, and lessons learned
3. **Update planning** - Add "As-Built" sections to planning documents
4. **Create feedback loop** - Help improve future planning accuracy

## Directory Structure

```
.claude/skills/speckit-author/
├── scripts/
│   ├── create_specifications.py  # Main SpecKit tool
│   ├── update_asbuilt.py         # As-built updates
│   └── __init__.py
├── templates/
│   ├── spec.md.template          # Specification template
│   └── plan.md.template          # Implementation plan template
├── SKILL.md                      # Detailed technical documentation
├── CLAUDE.md                     # Claude Code integration guide
├── README.md                     # This file
└── ARCHIVED/                     # Deprecated files
```

## Key Features

### With BMAD Planning (Recommended)

If you created BMAD planning documents in Phase 1:
- SpecKit reads `requirements.md`, `architecture.md`, and `epics.md`
- Asks 5-8 implementation-specific questions
- Generates specs aligned with your planning
- Organizes tasks by epics

**Benefits:**
- Consistency between planning and implementation
- Faster spec creation (fewer questions)
- Better task organization
- Traceability (spec.md references FR-001, plan.md references E-001)

### Without BMAD Planning

If starting without planning documents:
- SpecKit asks 10-15 comprehensive questions
- Gathers requirements, tech stack, and testing preferences
- Generates complete specs from scratch
- Recommends creating BMAD planning for next feature

**Benefits:**
- Still get structured specifications
- Interactive Q&A guides you through requirements
- Consistent format across features
- Can add BMAD planning later

## Generated Files

### specs/<feature>/spec.md

**Technical specification including:**
- Overview and purpose
- Requirements reference (links to BMAD if available)
- Implementation context (Q&A responses)
- Detailed component specifications
- Code examples and patterns
- Testing strategy
- Deployment considerations

### specs/<feature>/plan.md

**Implementation plan including:**
- Task breakdown (organized by phase or epic)
- Task format for each item:
  - Task ID (impl_001, test_001, doc_001)
  - Description
  - Estimated time
  - Priority
  - Files to modify
  - Steps to complete
  - Acceptance criteria
  - Dependencies
  - Verification commands

### specs/<feature>/CLAUDE.md

**Context for Claude Code:**
- Purpose of this spec directory
- File descriptions
- Usage instructions
- Links to related documentation

### specs/<feature>/README.md

**Human-readable overview:**
- Feature summary
- File descriptions
- Related planning and source code

## Integration with Workflow

SpecKit is part of the 5-phase workflow:

**Phase 1:** BMAD Planning (main repo, contrib branch)
- Create `planning/<feature>/` with requirements, architecture, epics

**Phase 2:** SpecKit Specifications (feature worktree) ← **You are here**
- Run `create_specifications.py`
- Generate `specs/<feature>/spec.md` and `plan.md`
- Update `TODO_*.md` with tasks

**Phase 3:** Quality Assurance (feature worktree)
- Run quality gates (tests, coverage, linting)
- Calculate semantic version

**Phase 4:** Integration (main repo, contrib branch)
- Merge PR
- Run `update_asbuilt.py` to update planning with reality
- Create feedback loop

**Phase 5:** Release (main repo, release branch)
- Final QA and documentation
- Tag release

## Example Session

```bash
$ cd /Users/user/german_feature_my-feature

$ python .claude/skills/speckit-author/scripts/create_specifications.py \
    feature my-feature stharrold

Working in worktree: /Users/user/german_feature_my-feature
Branch: feature/20251024T143000Z_my-feature
✓ Auto-detected TODO file: ../TODO_feature_20251024_my-feature.md

======================================================================
SpecKit Interactive Specification Tool
======================================================================

✓ Detected BMAD planning context: ../planning/my-feature/

BMAD Summary:
  - Requirements: 15 functional requirements, 5 user stories
  - Architecture: Python/FastAPI stack, PostgreSQL
  - Epics: 3 epics (Data Layer, API Layer, Testing)

Implementation Questions:
----------------------------------------------------------------------

Database migrations strategy?
  1) Alembic (recommended)
  2) Manual SQL migrations
  3) None needed
> 1

Include end-to-end (E2E) tests? (Y/n) > n

Include performance/load tests? (Y/n) > n

Task granularity preference?
  1) Small tasks (1-2 hours each)
  2) Medium tasks (half-day each)
  3) Large tasks (full-day each)
> 1

Follow epic priority order from epics.md? (Y/n) > Y

======================================================================
Generating specifications...
======================================================================
✓ Created specs/my-feature/spec.md (1247 chars)
✓ Created specs/my-feature/plan.md (1583 chars)
✓ Updated TODO file: ../TODO_feature_20251024_my-feature.md

✓ Committed changes to branch

Next steps:
  1. Review spec.md and plan.md
  2. Implement tasks from plan.md
  3. Update TODO task status as you complete each task
  4. Refer to ../planning/my-feature/ for BMAD context
```

## Benefits

### For Developers

- **Saves time** - No need to manually create specification documents
- **Consistency** - All features follow the same structure
- **Clarity** - Clear task breakdown with acceptance criteria
- **Traceability** - Links between planning, specs, and implementation

### For Teams

- **Shared understanding** - Everyone reads the same spec format
- **Better estimates** - Task breakdown improves planning accuracy
- **Knowledge transfer** - New team members can read specs to understand features
- **Historical record** - As-built updates document what actually happened

### For Claude Code

- **Token efficiency** - Call script once instead of reproducing logic
- **Standardization** - Specs follow consistent format
- **Context** - spec.md provides implementation guidance
- **Task tracking** - plan.md tasks automatically update TODO_*.md

## Tips

1. **Run BMAD planning first** - Better specs with less Q&A
2. **Review generated specs** - Templates are starting points, customize as needed
3. **Update TODO as you work** - Mark tasks complete as you finish them
4. **Use as-built updates** - Improve future planning accuracy
5. **Keep specs current** - Update spec.md if implementation deviates significantly

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete technical documentation
- **[CLAUDE.md](CLAUDE.md)** - Claude Code integration guide
- **[../../WORKFLOW.md](../../WORKFLOW.md)** - Full 5-phase workflow
- **[../bmad-planner/README.md](../bmad-planner/README.md)** - BMAD planning tool
- **[../workflow-orchestrator/README.md](../workflow-orchestrator/README.md)** - Workflow coordination

## Version

SpecKit Author v5.0.0 - Interactive callable tool implementation
