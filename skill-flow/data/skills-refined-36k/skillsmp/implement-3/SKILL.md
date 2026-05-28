---
name: implement
description: Task orchestration skill. Manages full workflow from analysis → implementation → verification → commit. Use for feature dev, bug fixes, and all code work.
---

# Implement Skill

Unified workflow orchestration. Manages entire cycle from task analysis to Git commit.

## Workflow

```
/implement "task description"
    │
    ├─ Phase 1: Analysis
    │   ├─ Understand requirements (reference Plan docs)
    │   ├─ Identify affected files
    │   ├─ Determine task type (feat/fix/refactor)
    │   └─ Create branch
    │
    ├─ Phase 2: Implementation
    │   ├─ Follow Clean Architecture
    │   ├─ Follow naming conventions
    │   └─ Intermediate commits per feature unit
    │
    ├─ Phase 3: Verification (/verify)
    │   ├─ pnpm build
    │   ├─ pnpm lint
    │   └─ On failure: fix → re-verify (Self-Healing Loop)
    │
    └─ Phase 4: Finalize
        ├─ Final commit
        ├─ Update CLAUDE.md / ai-context (if needed)
        └─ (Optional) PR creation guide
```

## Phase 1: Analysis

### Check Plan Documents

Always check Plan docs before implementation:
- `.claude/plans/implementation-plan.md`
- `PLAN.md` (detailed plan)

### Determine Task Type

| Type | Branch Prefix | Description |
|------|---------------|-------------|
| New feature | `feat/` | Add new functionality |
| Bug fix | `fix/` | Fix bugs |
| Refactoring | `refactor/` | Code improvement (no feature change) |
| Documentation | `docs/` | Documentation |
| Style | `style/` | Code formatting |
| Test | `test/` | Add/modify tests |

### Create Branch

```bash
git checkout -b {type}/{kebab-case-description}
# Example: feat/meeting-summary, fix/tag-duplicate
```

### Analysis Checklist

- [ ] Understand requirements clearly (reference Plan docs)
- [ ] Identify affected files/modules
- [ ] Verify Clean Architecture layers
- [ ] Break down work units (commit units)

## Phase 2: Implementation

### Follow Architecture

```
Presentation → Application → Domain → Infrastructure
components/   application/   repositories/   storage/
hooks/                       types/          lib/
app/
```

### Naming Conventions

| Type | Pattern |
|------|---------|
| Component | `PascalCase.tsx` |
| Hooks | `use{Name}.ts` |
| Repository interface | `{entity}.repository.ts` |
| Repository impl | `{entity}.{provider}.ts` |
| UseCase | `{action}-{entity}.usecase.ts` |
| Prompt | `{purpose}.prompt.ts` |
| Types | `{entity}.types.ts` |

### Feature Unit Commits

Commit at meaningful units during implementation:

```bash
git add <related files>
git commit -m "{type}: {description}"
```

**Commit Message Rules** (Conventional Commits):
```
feat: implement meeting summary API
fix: fix tag duplicate creation bug
refactor: clean up Claude SDK wrapper
```

**Commit Unit Criteria**:
- One logical change = one commit
- Unit that can be independently rolled back
- Not too small (not per file)
- Not too large (not entire feature at once)

## Phase 3: Verification

### Call /verify Skill

Always call `/verify` after implementation:

```
/verify
    ├─ pnpm build    # Build check
    ├─ pnpm lint     # Lint check
    └─ On failure → fix → re-verify
```

### Self-Healing Loop

```
Implement → /verify → Failure?
                        │
                        ├─ YES → Analyze error → Fix → Re-verify
                        │
                        └─ NO → Verification complete
```

**Key**: On verification failure, fix and re-verify without user intervention.
Alert user after 3+ failures on same error.

## Phase 4: Finalize

### Document Update Check

| Change Type | Update Target |
|-------------|---------------|
| New domain term | `ai-context/domain/glossary.json` |
| Entity change | `ai-context/domain/entities.json` |
| Business rule | `ai-context/domain/rules.json` |
| New directory | Create `CLAUDE.md` in that directory |

### Final Commit

```bash
git add .
git commit -m "{type}: {overall task summary}"
```

### PR Guide (Optional)

```bash
git push -u origin {branch-name}
gh pr create --title "{title}" --body "{description}"
```

## Example

### Input
```
/implement PLAN.md Phase 3 - Implement meeting summary feature
```

### Execution Flow

```
1. Analysis
   - Check Plan: Phase 3 requirements
   - Type: feat (new feature)
   - Branch: feat/meeting-summary
   - Affects: application/, storage/, lib/ai/

2. Implementation
   - summarize-meeting.usecase.ts
   - meeting-summary.prompt.ts
   - meeting.supabase.ts extension
   - Commit: "feat: implement meeting summary UseCase"

3. Verification
   - Call /verify
   - pnpm build ✓
   - pnpm lint ✓

4. Finalize
   - Update ai-context (if needed)
   - Final commit
```

## Important Notes

- **No Co-Authored-By**: Never add Claude/AI markers
- **No git -C**: Execute directly in working directory
- **Branch protection**: No direct commits to main
- **Build check**: Always run /verify before commit
- **Reference Plan**: Always check Plan docs before implementation
