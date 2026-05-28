# V3 DX Philosophy

Core principles extracted from CLAUDE.md and V3 research.

## Minimal Validation + Trust Environments

**Core Principle:** Fast iteration, environments handle safety

### What This Means

**Do:**
- Quick checks (<5s) for critical errors only
- Push changes to CI/dev environment
- Let automated systems validate
- Trust the pipeline

**Don't:**
- Run full test suites locally
- Validate every edge case before commit
- Wait for perfect before pushing
- Duplicate environment validation

### Examples

**Good (V3):**
```typescript
// Quick check: Feature-Key exists?
if (!branchName.startsWith('feature-')) {
  throw "Branch must start with 'feature-'"
}

// Commit and push
git commit -m "feat: Add X"
git push

// CI validates in parallel
// Dev environment auto-deploys
// Test there, not locally
```

**Bad (V2 - deprecated):**
```typescript
// Over-validation
checkBranchName()
validateCommitMessage()
runLinters()
runTests()
checkCoverage()
validateDependencies()
// ... 10 more checks

// 5 minutes later...
git commit
git push
```

## Progressive Disclosure

**Core Principle:** <500 lines main, details on demand

### Structure

```
Main SKILL.md (<500 lines)
├── Core workflow (what to do)
├── Integration points (how it connects)
├── Best practices (do/don't)
└── References to resources/

resources/ (unlimited)
├── examples/ (how to use)
├── patterns/ (detailed approaches)
└── reference/ (API docs, troubleshooting)
```

### Why

- **Scannable:** Read main file in <2 minutes
- **Efficient:** Only load details when needed
- **Maintainable:** Update details without changing workflow
- **Token-efficient:** Don't load 2000 lines for every skill

### Example

**Main SKILL.md:**
```markdown
### 3. Execute Action
1. Check prerequisites
2. Run core operation
3. Update state

See resources/examples/simple-case.md for walkthrough.
```

**resources/examples/simple-case.md:**
```markdown
# Simple Case Walkthrough

Given: User has feature branch checked out
When: User says "commit my work"
Then: sync-feature-branch skill executes

Step 1: Check prerequisites
- ✓ Branch name: feature-ANALYTICS
- ✓ Beads issue exists: bd-abc
- ✓ Changes staged: Yes

Step 2: Run operation
... detailed 200-line example ...
```

## Natural Language → Skills

**Core Principle:** Skills auto-activate on trigger phrases

### Pattern

```
User says natural language
  ↓
UserPromptSubmit hook fires
  ↓
Hook injects skill reminder
  ↓
Claude auto-invokes skill
  ↓
Skill executes workflow
```

### Examples

| User Says | Hook Detects | Skill Invoked |
|-----------|--------------|---------------|
| "commit my work" | COMMIT_DETECTED | sync-feature-branch |
| "create PR" | PR_CREATE_DETECTED | create-pull-request |
| "fix the PR" | PR_FIX_DETECTED | fix-pr-feedback |
| "create skill" | SKILL_CREATE_DETECTED | skill-creator |

### Implementation

**skill-rules.json:**
```json
{
  "skill-name": {
    "triggers": ["commit my work", "save progress"],
    "intents": ["User wants to commit changes"],
    "examples": ["User: 'commit my work'"]
  }
}
```

**UserPromptSubmit hook:**
```bash
if [[ "$user_prompt" =~ "commit my work" ]]; then
  echo "COMMIT_DETECTED: Use sync-feature-branch skill"
fi
```

## Fast Iteration

**Core Principle:** <30 seconds for common operations

### Time Budgets

| Operation | V3 Target | V2 Actual |
|-----------|-----------|-----------|
| Commit | <30s | 2-5 min |
| Create PR | <10s | 1-2 min |
| Fix PR issue | <2min | 5-10 min |
| Create skill | <5min | 15-30 min |

### How to Achieve

1. **Parallelism:** CI runs while you continue work
2. **Async validation:** Don't wait for results
3. **Quick checks only:** <5s for critical errors
4. **Trust environments:** Dev/staging catch issues

### Example

**V3 Commit Flow:**
```
0:00 - User: "commit my work"
0:02 - Quick lint check
0:15 - Git commit
0:25 - Git push
0:30 - User continues work
[Background: CI running, dev deploying]
```

**V2 Commit Flow (deprecated):**
```
0:00 - User runs sync command
0:30 - Full lint
1:30 - Run tests
2:30 - Check coverage
3:00 - Validate schema
4:00 - Git commit
4:30 - Git push
5:00 - Wait for CI
```

## Beads Integration

**Core Principle:** Feature-Key tracking for all work

### Pattern

```
Create Beads issue
  ↓
Branch: feature-<KEY>
  ↓
Commits: Feature-Key: <KEY>
  ↓
PR: Links to Beads issue
  ↓
Merge: Closes Beads issue
```

### Required Fields

**Commit trailer:**
```
Feature-Key: ANALYTICS_DASHBOARD
Agent: claude-code
Role: backend-engineer
```

**Beads issue:**
```typescript
{
  title: "ANALYTICS_DASHBOARD",
  issue_type: "feature",
  priority: 2,
  status: "in_progress"
}
```

## Serena Integration

**Core Principle:** Symbol-aware code operations

### Pattern

```
Search with Serena
  ↓
Navigate to symbols
  ↓
Edit with symbol tools
  ↓
Verify with Serena
```

### Tool Selection

| Task | Use Serena | Not Bash |
|------|-----------|----------|
| Search code | search_for_pattern | grep -r |
| Find files | list_dir | find . -name |
| Read symbol | find_symbol | cat + manual parsing |
| Edit code | replace_symbol_body | sed/awk |
| Insert code | insert_after_symbol | cat >> file |

## Trust Patterns

**Core Principle:** Don't reinvent, use proven approaches

### Sources of Truth

1. **Tech lead 300k LOC case study** - Proven at scale
2. **Existing skills** - Battle-tested in production
3. **V3 research docs** - Analyzed and validated
4. **CLAUDE.md** - Canonical workflow reference

### When Designing Skills

**Ask:**
1. Does an existing skill do something similar?
2. What pattern did tech lead use?
3. Is there a V3 reference doc?
4. Can I simplify by trusting environments?

**Example:**

**Before (reinventing):**
```markdown
## Workflow
1. Validate branch name against regex
2. Check git status for clean tree
3. Run linters
4. Run tests
5. Check Beads issue exists
6. Validate commit message format
7. ... 10 more steps
```

**After (trusting patterns):**
```markdown
## Workflow
1. Check Feature-Key (quick, <1s)
2. Quick lint (fast, <5s)
3. Commit with trailer
4. Push to remote

See sync-feature-branch skill for proven approach.
```

## Anti-Patterns

### ❌ Over-Validation

**Don't:**
- Run full test suite before commit
- Validate every possible error
- Check things environments will check
- Wait for perfect

**Why:** Slows iteration, duplicates CI work

### ❌ Walls of Text

**Don't:**
- Put 2000 lines in main SKILL.md
- Document every edge case
- Inline all examples
- Skip progressive disclosure

**Why:** Overwhelming, hard to scan, token-inefficient

### ❌ Explicit Commands

**Don't:**
- Force users to type `/sync-i --force`
- Require complex flag combinations
- Make users remember syntax
- Skip natural language

**Why:** V3 uses natural language → auto-activation

### ❌ Reinventing Patterns

**Don't:**
- Create new commit format
- Invent new branch naming
- Build custom validation
- Ignore existing skills

**Why:** Breaks integration, wastes time, unpredictable

## V3 vs V2

| Aspect | V2 (Deprecated) | V3 (Current) |
|--------|-----------------|--------------|
| **Commands** | `/sync-i --force` | "commit my work" |
| **Validation** | Full local suite | Quick checks only |
| **Timing** | 2-5 minutes | <30 seconds |
| **Skills** | Explicit invocation | Auto-activation |
| **Docs** | Walls of text | Progressive disclosure |
| **Philosophy** | Validate everything | Trust environments |

## Key Takeaways

1. **Fast > Perfect:** <30s for common ops, trust CI for validation
2. **Scannable > Comprehensive:** <500 lines main, details in resources/
3. **Natural > Explicit:** "commit my work" > `/sync-i --force`
4. **Trust > Validate:** Environments handle safety, don't duplicate
5. **Patterns > Reinvention:** Use proven approaches, don't start from scratch

---

**Related:**
- docs/DX_PARITY_V3/SKILL_ACTIVATION_SYSTEM_SPEC.md
- docs/DX_PARITY_V3/TECH_LEAD_300K_LOC_CASE_STUDY.md
- CLAUDE.md (V3 DX Workflow)
