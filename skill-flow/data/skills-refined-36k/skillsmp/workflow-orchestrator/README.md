---
type: directory-documentation
directory: .claude/skills/workflow-orchestrator
title: Workflow Orchestrator
sibling_claude: CLAUDE.md
parent: null
children:
  - ARCHIVED/README.md
---

# Workflow Orchestrator

> **Main coordinator skill for the 6-phase workflow system - provides algorithmic guidance for Claude Code**

The Workflow Orchestrator is the main coordinator skill that guides Claude Code through workflow phases. Unlike other skills, it contains no executable scripts - instead, it provides algorithmic guidance for context detection, skill loading, and phase transitions. This is a **conceptual skill** that directs Claude's behavior.

## Key Concept

**No executable scripts** - Orchestration logic is too dynamic for static scripts. Requires Claude's natural language understanding and real-time context detection.

**What SKILL.md provides:**
- Algorithms (Python pseudocode) for Claude to implement mentally
- Decision trees for phase determination
- Skill loading patterns (progressive loading for token efficiency)
- Context management guidance (80K warning, 100K checkpoint)

## Core Algorithms

### 1. Context Detection

**Purpose:** Determine where user is in workflow (main repo vs worktree, which phase)

**Algorithm:**
```python
def detect_context():
    repo_root = git_rev_parse_show_toplevel()
    current_dir = pwd()
    current_branch = git_branch_show_current()

    is_worktree = (current_dir != repo_root)

    # Find TODO file
    if is_worktree:
        todo_files = glob('../TODO_*.md')  # Look in parent
    else:
        todo_files = glob('TODO_*.md')  # Look in current

    workflow_type = parse_workflow_type(todo_files[0]) if todo_files else None

    return {
        'repo_root': repo_root,
        'current_dir': current_dir,
        'current_branch': current_branch,
        'is_worktree': is_worktree,
        'workflow_type': workflow_type
    }
```

### 2. Skill Loading Logic

**Purpose:** Load only skills needed for current phase (token efficiency)

**Decision tree:**
```python
context = detect_context()

# Phase 0: Always load tech-stack-adapter first
if not SESSION_CONFIG_LOADED:
    load_skill('tech-stack-adapter')
    SESSION_CONFIG = run_detect_stack()

# Phase determination
if context['is_worktree']:
    # Phase 2-3: In feature/release/hotfix worktree
    if not spec_exists():
        load_skill('speckit-author')
    elif not quality_gates_passed():
        load_skill('quality-enforcer')
        load_skill('git-workflow-manager')
    else:
        load_skill('git-workflow-manager')
        create_pr()

elif 'contrib' in context['current_branch']:
    # Phase 1 or 4: In main repo on contrib branch
    if not planning_exists():
        load_skill('bmad-planner')
    else:
        load_skill('git-workflow-manager')
        create_worktree()

elif context['current_branch'] == 'develop':
    # Phase 5: In main repo on develop
    load_skill('git-workflow-manager')
    create_release()
```

### 3. Context Management

**Purpose:** Prevent Claude Code from exceeding context limits

**Thresholds:**
- **80K tokens:** Warning - complete current task before checkpoint
- **100K tokens:** Checkpoint - save state to TODO file, run `/init` then `/compact`

**Algorithm:**
```python
def check_context_usage():
    current_tokens = get_token_count()

    if current_tokens >= 100000:
        save_state_to_todo()
        commit_changes()
        display_message("""
        ✓ State saved to TODO file

        Context usage: 100K tokens (checkpoint threshold)

        Please run:
        1. /init (updates memory files)
        2. /compact (compresses memory buffer)
        3. Continue working (context preserved in TODO file)
        """)
        return 'checkpoint'

    elif current_tokens >= 80000:
        display_message("""
        ⚠️  Context usage: 80K tokens (approaching 100K checkpoint)

        Recommendation: Complete current task before checkpoint
        """)
        return 'warning'

    return 'normal'
```

## Progressive Skill Loading

**Goal:** Minimize context usage by loading only what's needed

**Pattern:**
```python
# ❌ Bad: Load everything upfront
load_all_skills()  # Wastes ~50K tokens on unused skills

# ✅ Good: Load as needed
if user_needs_planning():
    load_skill('bmad-planner')  # ~5K tokens
elif user_needs_specs():
    load_skill('speckit-author')  # ~5K tokens
```

**Token savings:**
- Loading all 9 skills upfront: ~60K tokens
- Progressive loading (2-3 skills per phase): ~10-15K tokens
- **Savings: ~45-50K tokens (75% reduction)**

## Workflow Phase Map

```
Phase 0: Session Start
├── Load: tech-stack-adapter
└── Action: Detect project configuration

Phase 1: Planning (main repo, contrib branch)
├── Load: bmad-planner
└── Action: Create planning/ documents

Phase 2: Implementation (worktree)
├── 2.1: Load: git-workflow-manager → Create worktree
├── 2.2: User: cd ../german_feature_<slug>
├── 2.3: Load: speckit-author → Create specs
└── 2.4: User: Implement feature

Phase 3: Quality (worktree)
├── Load: quality-enforcer, git-workflow-manager
├── Action: Run quality gates
└── Action: Calculate semantic version

Phase 4: Integration (main repo, contrib branch)
├── 4.1: Load: git-workflow-manager → Create PR (feature → contrib)
├── 4.2: User: Merge in GitHub UI
├── 4.3: Load: speckit-author (optional) → Update BMAD as-built
├── 4.4: Load: git-workflow-manager → Daily rebase contrib onto develop
└── 4.5: Action: Create PR (contrib → develop)

Phase 5: Release (main repo)
├── Load: git-workflow-manager, quality-enforcer
├── Action: Create release branch
├── Action: Final QA
├── Action: Create PR (release → main)
├── Action: Tag release
├── Action: Back-merge to develop
└── Action: Cleanup release branch

Phase 6: Hotfix (hotfix worktree)
├── Load: git-workflow-manager, quality-enforcer
├── Load: speckit-author (optional for complex fixes)
├── Action: Create hotfix worktree from main
├── Action: Implement minimal fix
├── Action: Run quality gates
├── Action: Create PR (hotfix → main)
├── Action: Tag hotfix
└── Action: Back-merge to develop
```

## Decision Criteria

**How orchestrator decides what to do:**

1. **Where am I?** - Main repo or worktree? What branch?
2. **What exists?** - planning/? specs/? TODO file? Quality gates passed?
3. **What's next?** - Follow phase map based on answers above
4. **What skills do I need?** - Load only skills for current phase
5. **Am I approaching context limit?** - Warn at 80K, checkpoint at 100K

## Usage Example

**When user says "next step?":**

```python
# 1. Load tech-stack-adapter (if not loaded)
if not SESSION_CONFIG:
    config = detect_stack()
    SESSION_CONFIG = config

# 2. Detect current context
context = detect_context()

# 3. Load appropriate skills based on context
if context['is_worktree']:
    if no_spec():
        load_and_run('speckit-author', 'create_specifications.py')
    elif no_quality():
        load_and_run('quality-enforcer', 'run_quality_gates.py')
    else:
        load_and_run('git-workflow-manager', 'create_pr')
elif 'contrib' in context['branch']:
    load_and_run('bmad-planner', 'create_planning.py')

# 4. Execute phase-appropriate action

# 5. Check context usage
check_context_usage()
```

## Integration with Other Skills

**All skills are coordinated by workflow-orchestrator:**

- **tech-stack-adapter:** Loaded first (Phase 0)
- **bmad-planner:** Loaded in Phase 1
- **git-workflow-manager:** Loaded in Phases 2, 3, 4, 5, 6
- **speckit-author:** Loaded in Phase 2.3, Phase 4 (optional)
- **quality-enforcer:** Loaded in Phase 3, Phase 5, Phase 6
- **workflow-utilities:** Loaded as needed by other skills
- **agentdb-state-manager:** Loaded for complex queries (optional)

## Constants and Rationale

| Constant | Value | Rationale |
|----------|-------|-----------|
| Context warning threshold | 80K tokens | Gives time to complete current task |
| Context checkpoint threshold | 100K tokens | 73% of 136K effective capacity |
| Progressive skill loading | 2-3 skills per phase | Minimize context, load only what's needed |

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete orchestration algorithms
- **[CLAUDE.md](CLAUDE.md)** - Claude Code integration guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

**See also:**
- [WORKFLOW.md](../../WORKFLOW.md) - Complete 6-phase workflow guide
- All other skills coordinated by this orchestrator

## Contributing

This skill is part of the workflow system. To update:

1. Modify algorithms in `SKILL.md`
2. Update version in frontmatter
3. Document changes in `CHANGELOG.md`
4. Run validation: `python .claude/skills/workflow-utilities/scripts/validate_versions.py`

## License

Part of the german repository workflow system.
