---
name: feature-workflow
description: TDD-based feature workflow with 7 phases - loads directly into session (no installation)
---

# Feature Workflow

7-phase TDD feature implementation workflow. Loads directly into session - no file installation required.

## 🔴 4 CORE PRINCIPLES (ALWAYS ENFORCED)

**These 4 principles are MANDATORY throughout the entire workflow. Violations are BLOCKED.**

### 1️⃣ USE SUBAGENT (Task Tool)
```
❌ BLOCKED: Direct Edit/Write without subagent
✅ REQUIRED: Task(subagent_type="...") for ALL implementation
```
| Task Type | Subagent |
|-----------|----------|
| Backend/API | `backend-architect` |
| Frontend/UI | `frontend-architect` |
| Tests | `quality-engineer` |
| Types | `typescript-pro` |
| Exploration | `Explore` |

### 2️⃣ USE LSP (Not grep/glob)
```
❌ BLOCKED: grep, glob, Grep, Glob for symbol search
✅ REQUIRED: LSP tool for code navigation
```
| Task | LSP Operation |
|------|---------------|
| Find definition | `goToDefinition` |
| File symbols | `documentSymbol` |
| Project search | `workspaceSymbol` |
| Find references | `findReferences` |
| Find implementations | `goToImplementation` |

### 3️⃣ USE TDD (Tests First)
```
❌ BLOCKED: Implementation before tests
✅ REQUIRED: Write tests → Run (RED) → Implement → Run (GREEN)
```
- Phase 2 (Tests) MUST complete before Phase 3 (Implementation)
- Tests should FAIL initially (red phase)
- Implementation makes tests PASS (green phase)

### 4️⃣ USE PARALLEL (Concurrent Execution)
```
❌ INEFFICIENT: Sequential subagent calls
✅ REQUIRED: Parallel Task calls when no dependencies
```
```
# GOOD: Single message with multiple Task calls
Task(types) + Task(query-keys)  ← Parallel (no dependency)

# GOOD: Sequential only when dependent
Task(api) → Task(hooks)  ← Sequential (hooks needs api)
```

### Self-Check (BEFORE EVERY ACTION)
```
□ Am I using Task tool with subagent? → If NO, STOP
□ Am I using LSP for code navigation? → If grep/glob, STOP
□ Did I write tests first? → If NO, go back to Phase 2
□ Can these tasks run in parallel? → If YES, single message with multiple Task calls
```

---

## Usage

```bash
/feature-workflow:feature-workflow "feature description"
```

## ⚡ MANDATORY: DELEGATE TO feature-dev

**When this skill is invoked, IMMEDIATELY delegate to feature-dev:feature-dev**

```
/feature-workflow:feature-workflow "Implement user settings page"
     │
     ▼
Skill(feature-dev:feature-dev, args="Implement user settings page")
     │
     ▼
feature-dev orchestrates → feature-workflow phases 1-7
```

### Delegation Rule
```python
# ALWAYS delegate - no exceptions
if skill_invoked == "feature-workflow":
    Skill("feature-dev:feature-dev", args=user_request)
```

## How It Works

1. **Delegate** to feature-dev:feature-dev (MANDATORY)
2. **Auto-detect** project type (vite.config, go.mod, pubspec.yaml, etc.)
3. **Apply** 4 core principles + 7-phase workflow
4. **Enforce** throughout the session

## 7-Phase Workflow (STRICT ORDER)

### Phase 1: Git Worktree Setup
- Create isolated feature branch
- Setup worktree in `.worktrees/`
- Verify dependencies

**Gate**: Worktree exists, correct branch

### Phase 2: TDD - Write Tests First
- Write E2E/integration tests BEFORE implementation
- Tests should initially fail (red phase)

**Gate**: Test files created

### Phase 3: Implementation (SUBAGENT MANDATORY!)

**🚨 SUBAGENT DELEGATION IS REQUIRED - NOT OPTIONAL**

ALWAYS use Task tool with subagents for implementation. Direct implementation without subagents is BLOCKED.

```
❌ BLOCKED: Direct file editing without subagent
✅ REQUIRED: Task(subagent_type="backend-architect" | "frontend-architect" | ...)
```

#### Subagent Selection by Task
| Task Type | Subagent | When to Use |
|-----------|----------|-------------|
| API/Backend | `backend-architect` | Handlers, services, repositories |
| UI/Frontend | `frontend-architect` | Components, pages, hooks |
| Tests | `quality-engineer` | Test files, test utilities |
| Types/Schemas | `typescript-pro` | Type definitions, schemas |
| Performance | `performance-engineer` | Optimization tasks |
| Security | `security-engineer` | Auth, validation |

#### Parallel Execution Pattern
```
Phase 3 Implementation:
├─ [Parallel] Task(types) + Task(query-keys)
├─ [Sequential] Task(api) → Task(hooks) (dependency)
└─ [Parallel] Task(page) + Task(components)
```

#### LSP-First Within Subagents
| Task | Use This | ❌ NOT This |
|------|----------|------------|
| Find definition | `LSP goToDefinition` | grep/glob |
| File symbols | `LSP documentSymbol` | cat/read |
| Project search | `LSP workspaceSymbol` | grep |
| Find references | `LSP findReferences` | grep |

**Gate**: Implementation complete via subagents, no direct edits

### Phase 4: Build & Verification
- TypeScript/Go/Dart compilation
- Lint checks
- Unit tests

**Gate**: Build passes, lint clean

### Phase 5: Local Testing
- Test with real backend
- E2E scenarios pass

**Gate**: E2E tests pass

### Phase 6: Code Review (Ralph-Loop!)
```bash
/ralph-loop "Code review for {feature}..." --max-iterations 10
```
- Automatically fixes Critical/Important issues
- Continues until `meaningfulUnprocessedCount = 0`

**Gate**: No meaningful review issues

### Phase 7: Commit & Push
- Stage all changes
- Descriptive commit message
- Push to remote

**Gate**: Clean commit, pushed

## Phase Enforcement (MANDATORY)

```
❌ BLOCKED:
- Starting Phase 3 without completing Phase 2
- Skipping to Phase 6 from Phase 2
- Committing (Phase 7) before code review (Phase 6)
- Direct file editing in Phase 3 (MUST use subagents)

✅ ALLOWED:
- Sequential progression: 1→2→3→4→5→6→7
- Fixing issues within current phase
- Parallel subagent execution in Phase 3
```

## 🚨 SUBAGENT ENFORCEMENT (CRITICAL)

**Phase 3 REQUIRES subagent delegation. This is NOT optional.**

### Self-Check Before Implementation
```
Before ANY file edit in Phase 3, ask:
□ Am I using Task tool with a subagent? → If NO, STOP
□ Did I select the appropriate subagent_type? → Match task to agent
□ Can multiple tasks run in parallel? → Launch parallel Task calls
```

### Enforcement Rule
```python
if phase == 3 and action == "edit_file":
    if not using_subagent:
        BLOCK("Use Task tool with subagent_type for implementation")
```

## Supported Project Types

| Type | Stack | Key Features |
|------|-------|--------------|
| react-vite | React + Vite + pnpm | Playwright E2E, TanStack Query |
| nextjs | Next.js + pnpm | App Router, Server Components |
| go-gin | Go + Gin + fx | Handler→Service→Repo, Swagger |
| flutter | Flutter + BLoC | Clean Architecture |

## Checkpoint Indicators

| Symbol | Status |
|--------|--------|
| `[P1:_]` | Pending |
| `[P1:*]` | In Progress |
| `[P1:V]` | Verified |
| `[P1:X]` | Failed |

## Integration with Skills

- `feature-dev:feature-dev` - **DELEGATED TO** (orchestrates the 7 phases)
- `superpowers:using-git-worktrees` - Worktree setup (Phase 1)
- `superpowers:test-driven-development` - TDD approach (Phase 2)
- `superpowers:code-reviewer` - Code review (Phase 6)
- `ralph-loop:ralph-loop` - Autonomous review loop (Phase 6)
- `code-patterns` - LSP-first enforcement (Phase 3)
