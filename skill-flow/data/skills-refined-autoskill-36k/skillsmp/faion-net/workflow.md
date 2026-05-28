# SDD Workflow

## Overview

```
IDEA DISCOVERY (optional):
  /faion-idea-discovery → brainstorm → validate pain → evaluate niche → idea-validation.md
                    ↓
NEW PROJECT:
  bootstrap → constitution.md → TASK_000_setup → Execute setup
                    ↓
PRODUCT RESEARCH (optional):
  /faion-product-research → market, competitors, personas, validation, pricing
                    ↓
GTM MANIFEST (optional):
  /faion-gtm-manifest → go-to-market strategy from research data
                    ↓
FEATURE DEVELOPMENT (with quality gates):
  backlog/ → [confidence-check] → grooming → todo/ → [parallelize] → in-progress/ → done/
     ↓                               ↓         ↓                          ↓            ↓
  spec.md                      + design    ready                    executing    [reflexion]
                               + tasks                                            archived
                    ↓
MLP PLANNING (optional):
  /faion-mlp-planning → gap analysis → update specs → WOW moments → impl order
```

## Phase 1-2: Select Project

```bash
find . -maxdepth 2 -name ".aidocs" -type d 2>/dev/null | sed 's|/.aidocs||;s|./||'
```

AskUserQuestion: "З яким проектом працюємо?" + "+ Новий проект"

## Phase 3: New Project

If new project:
1. Ask project name (kebab-case)
2. Ask if codebase exists:
   - **No codebase** → Call `faion-project-bootstrap` skill
   - **Has codebase** → Call `faion-writing-constitutions` skill (analysis mode)

**After bootstrap:**
- Constitution: `.aidocs/constitution.md`
- Roadmap: `.aidocs/roadmap.md`
- Setup task: `.aidocs/features/todo/00-setup/tasks/todo/TASK_000_project_setup.md`

## Phase 4: Select Feature

```bash
ls -d .aidocs/features/{in-progress,todo,backlog,done}/*/ 2>/dev/null
```

AskUserQuestion: "Що хочеш зробити?" options:
- In-progress features (continue work)
- Todo features (start execution)
- Backlog features (needs grooming)
- "+ Нова фіча" (add to backlog)
- "Backlog grooming" → `faion-backlog-grooming` skill
- "Product research" → `faion-product-research` skill
- "GTM Manifest" → `faion-gtm-manifest` skill
- "Idea discovery" → `faion-idea-discovery` skill
- "MLP Planning" → `faion-mlp-planning` skill
- "Standalone tasks"
- "Product docs"

## Phase 5: Feature Grooming

1. Call `faion-backlog-grooming` skill with feature
2. Skill handles: spec refinement → design → tasks
3. Moves feature from backlog/ to todo/

## Phase 6: Feature Execution

1. Move to in-progress/
2. Execute tasks using faion-task-executor-agent agent

## Phase 7: Feature Completion

1. Move feature from in-progress/ to done/
2. Update roadmap.md status
3. Offer next feature
