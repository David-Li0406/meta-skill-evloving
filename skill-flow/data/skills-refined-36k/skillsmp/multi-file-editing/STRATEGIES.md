# Multi-File Editing Strategies

Detailed guidance on choosing and executing multi-file change strategies.

## Strategy Overview

| Strategy | Risk Level | Rollback Ease | Best For |
|----------|------------|---------------|----------|
| Atomic | Medium | Easy (single commit) | Small to medium changes |
| Incremental | Low | Medium (multiple commits) | Large refactors |
| Staged | Low | Easy (branch-based) | Critical system changes |

---

## Atomic Strategy

**All changes committed together as one unit.**

### When to Use

- Renaming symbols across codebase
- Adding/removing required fields
- Breaking API changes
- Changes that would leave codebase in broken state if partial

### Workflow

```markdown
## Atomic Change Workflow

1. **Plan all changes upfront**
   - [ ] List every file that needs editing
   - [ ] Determine edit order
   - [ ] Estimate total scope

2. **Create working branch**
   ```bash
   git checkout -b feature/atomic-change
   ```

3. **Make all edits without committing**
   - [ ] Edit files in dependency order
   - [ ] Keep terminal open for type checking
   - [ ] Don't commit until all changes complete

4. **Validate entire changeset**
   ```bash
   bun run typecheck
   bun test
   ```

5. **Commit atomically**
   ```bash
   git add -A
   git commit -m "refactor: Rename UserData to UserProfile"
   ```

6. **Push and merge**
```

### Example: Atomic Rename

**Goal:** Rename `getUserData` to `getUserProfile` across codebase.

```bash
# Step 1: Find all occurrences
rg -l "getUserData" --type ts
# Output:
# src/services/user.service.ts
# src/routes/user.routes.ts
# src/utils/user.utils.ts
# tests/user.service.test.ts
# tests/user.routes.test.ts
```

**Edit order:**

1. `src/services/user.service.ts` - Define function
2. `src/utils/user.utils.ts` - Utility usage
3. `src/routes/user.routes.ts` - API layer
4. `tests/user.service.test.ts` - Service tests
5. `tests/user.routes.test.ts` - Route tests

**All edits, then one commit:**

```bash
git add -A
git commit -m "refactor: Rename getUserData to getUserProfile

- Updated function name in user service
- Updated all call sites in routes and utils
- Updated test files"
```

### Atomic Strategy Checklist

- [ ] All affected files identified
- [ ] Edit order determined
- [ ] Working branch created
- [ ] All edits complete
- [ ] Type check passes
- [ ] All tests pass
- [ ] Single commit made
- [ ] PR created for review

---

## Incremental Strategy

**Changes applied and validated progressively, one file or module at a time.**

### When to Use

- Large refactors (50+ files)
- Changes that can work partially
- When you want early feedback
- Learning the codebase while refactoring

### Workflow

```markdown
## Incremental Change Workflow

1. **Break into phases**
   - [ ] Group related files into phases
   - [ ] Ensure each phase is independently valid
   - [ ] Plan validation for each phase

2. **Execute phase by phase**
   For each phase:
   - [ ] Make changes
   - [ ] Run type checker
   - [ ] Run affected tests
   - [ ] Commit phase
   - [ ] Push for CI validation

3. **Handle failures**
   - Fix issues before proceeding
   - Adjust plan if needed
   - Don't skip validation
```

### Example: Incremental Migration

**Goal:** Migrate from `moment` to `date-fns` across 50 files.

**Phase breakdown:**

```markdown
### Phase 1: Add date-fns, keep moment (2 files)
- [ ] package.json - Add date-fns
- [ ] src/utils/date.utils.ts - Create wrapper functions
- Commit: "chore: Add date-fns alongside moment"

### Phase 2: Migrate core services (8 files)
- [ ] src/services/scheduling.service.ts
- [ ] src/services/reporting.service.ts
- [ ] ... (6 more)
- Commit: "refactor: Migrate services to date-fns"

### Phase 3: Migrate API layer (12 files)
- [ ] src/routes/events.routes.ts
- [ ] ... (11 more)
- Commit: "refactor: Migrate API layer to date-fns"

### Phase 4: Migrate frontend (25 files)
- [ ] src/components/DatePicker.tsx
- [ ] ... (24 more)
- Commit: "refactor: Migrate frontend to date-fns"

### Phase 5: Migrate tests (15 files)
- [ ] tests/scheduling.service.test.ts
- [ ] ... (14 more)
- Commit: "test: Update tests for date-fns"

### Phase 6: Remove moment
- [ ] package.json - Remove moment
- [ ] Delete any remaining moment imports
- Commit: "chore: Remove moment dependency"
```

### Incremental Validation Pattern

After each phase:

```bash
# Type check
bun run typecheck

# Run affected tests
bun test --grep "scheduling|reporting"

# Or run all tests if fast enough
bun test

# Check bundle size (for frontend changes)
bun run build && du -sh dist/
```

### Incremental Strategy Checklist

- [ ] Phases defined and documented
- [ ] Each phase independently valid
- [ ] Commit after each phase
- [ ] CI passes for each commit
- [ ] Progress tracked visibly
- [ ] Team notified of progress

---

## Staged Strategy

**Large changes with review checkpoints, typically on a long-running branch.**

### When to Use

- Multi-day or multi-week refactors
- Critical system changes
- Changes needing stakeholder review
- Changes with high rollback cost

### Workflow

```markdown
## Staged Change Workflow

1. **Create feature branch**
   ```bash
   git checkout -b refactor/new-auth-system
   ```

2. **Define stages with review gates**
   - Stage 1: Foundation (requires arch review)
   - Stage 2: Core implementation (requires code review)
   - Stage 3: Integration (requires QA review)
   - Stage 4: Cleanup (final review)

3. **Work in stages**
   For each stage:
   - [ ] Implement stage
   - [ ] Self-review
   - [ ] Request stage review
   - [ ] Address feedback
   - [ ] Merge to feature branch

4. **Regular rebasing**
   ```bash
   git fetch origin main
   git rebase origin/main
   ```

5. **Final merge**
   - [ ] Full test suite passes
   - [ ] All stages reviewed
   - [ ] Stakeholder sign-off
   - [ ] Merge to main
```

### Example: Staged Authentication Rewrite

**Goal:** Replace JWT auth with session-based auth.

```markdown
### Stage 1: Foundation (Week 1)
**Reviewers:** Architecture team

Changes:
- [ ] Add session store infrastructure
- [ ] Create session types and interfaces
- [ ] Add session middleware (disabled)

Review gate:
- Architecture approved
- No production impact

Commit: "feat(auth): Add session infrastructure (disabled)"

---

### Stage 2: Core Implementation (Week 2)
**Reviewers:** Security team, Backend lead

Changes:
- [ ] Implement session creation
- [ ] Implement session validation
- [ ] Add session refresh logic
- [ ] Create migration path from JWT

Review gate:
- Security review passed
- Unit tests for all new code

Commit: "feat(auth): Implement session management core"

---

### Stage 3: Integration (Week 3)
**Reviewers:** QA team, Frontend lead

Changes:
- [ ] Update API routes to use sessions
- [ ] Update frontend auth handling
- [ ] Add feature flag for rollout

Review gate:
- QA test plan executed
- Feature flag working
- Rollback tested

Commit: "feat(auth): Integrate session auth with feature flag"

---

### Stage 4: Cleanup (Week 4)
**Reviewers:** Full team

Changes:
- [ ] Remove JWT code
- [ ] Remove feature flag
- [ ] Update documentation
- [ ] Clean up migration code

Review gate:
- All users on new system
- JWT fully deprecated
- Docs updated

Commit: "chore(auth): Remove legacy JWT authentication"
```

### Staged Strategy Checklist

- [ ] Stages defined with clear boundaries
- [ ] Review gates established
- [ ] Stakeholders identified per stage
- [ ] Rollback plan for each stage
- [ ] Regular rebase schedule set
- [ ] Communication plan in place
- [ ] Timeline communicated to team

---

## Choosing a Strategy

### Decision Matrix

| Factor | Choose Atomic | Choose Incremental | Choose Staged |
|--------|--------------|-------------------|---------------|
| File count | <20 files | 20-100 files | 50+ files |
| Duration | <1 day | 1-5 days | 1+ weeks |
| Risk level | Low-medium | Medium | High |
| Team size | 1 person | 1-2 people | Team |
| Review need | One review | Periodic reviews | Stage gates |

### Quick Decision Flow

```
Is this a critical system change?
  Yes -> Staged
  No  -> Continue

Will this take more than a day?
  Yes -> Consider Staged or Incremental
  No  -> Continue

Are there more than 20 files?
  Yes -> Incremental
  No  -> Atomic

Can partial changes break the build?
  Yes -> Atomic
  No  -> Incremental
```

---

## Hybrid Approaches

### Atomic within Incremental

Use atomic commits for each increment:

```bash
# Phase 1: Migrate date utilities (atomic commit)
git add src/utils/date.utils.ts tests/date.utils.test.ts
git commit -m "refactor: Migrate date utilities to date-fns"

# Phase 2: Migrate services (atomic commit)
git add src/services/*.ts tests/services/*.test.ts
git commit -m "refactor: Migrate services to date-fns"
```

### Incremental within Staged

Each stage can have multiple incremental commits:

```
Stage 1 (Foundation)
  |- Commit: Add session store
  |- Commit: Add session types
  |- Commit: Add session middleware
  [Stage Review]

Stage 2 (Implementation)
  |- Commit: Session creation
  |- Commit: Session validation
  |- Commit: Session refresh
  [Stage Review]
```

---

## Recovery Patterns

### Atomic Recovery

```bash
# If something goes wrong before commit
git checkout -- .

# If something goes wrong after commit
git revert HEAD
```

### Incremental Recovery

```bash
# Revert specific phase
git revert <commit-hash>

# Or reset to before the phase
git reset --hard <previous-commit>
```

### Staged Recovery

```bash
# Abandon feature branch
git checkout main
git branch -D refactor/feature-name

# Or revert to previous stage
git reset --hard <stage-n-1-commit>
```
