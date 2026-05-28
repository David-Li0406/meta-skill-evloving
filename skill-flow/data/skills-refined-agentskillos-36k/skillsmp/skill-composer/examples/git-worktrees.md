# Example: Using Git Worktrees

**Source**: https://github.com/obra/superpowers/tree/main/skills/using-git-worktrees
**Pattern**: Workflow automation with safety verification
**Use case**: Creating isolated development environments for parallel feature work

## Key Sections from SKILL.md

### Core Principle

```markdown
Systematic directory selection + safety verification = reliable isolation
```

**Announce at start**: "I'm using the using-git-worktrees skill to set up an isolated workspace."

### Directory Selection Process (3 Steps)

**1. Check Existing Directories**
```bash
ls -d .worktrees 2>/dev/null     # Preferred (hidden)
ls -d worktrees 2>/dev/null      # Alternative
```
**If found**: Use that directory. If both exist, `.worktrees` wins.

**2. Check CLAUDE.md**
```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```
**If preference specified**: Use it without asking.

**3. Ask User**

If no directory exists and no CLAUDE.md preference, ask with two options:
1. `.worktrees/` (project-local, hidden)
2. `~/.config/superpowers/worktrees/<project-name>/` (global location)

### Safety Verification

**For Project-Local Directories**:

MUST verify .gitignore before creating worktree:
```bash
grep -q "^\.worktrees/$" .gitignore || grep -q "^worktrees/$" .gitignore
```

**If NOT in .gitignore**:
Per Jesse's rule "Fix broken things immediately":
1. Add appropriate line to .gitignore
2. Commit the change
3. Proceed with worktree creation

**Why critical**: Prevents accidentally committing worktree contents to repository.

**For Global Directory**:
No .gitignore verification needed - outside project entirely.

### Creation Steps (5 Steps)

**1. Detect Project Name**
```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

**2. Create Worktree**
```bash
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**3. Run Project Setup** (Auto-detect)
```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
```

**4. Verify Clean Baseline**
Run tests to ensure worktree starts clean.

**If tests fail**: Report failures, ask whether to proceed.

**5. Report Location**
```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

### Quick Reference Table

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify .gitignore) |
| `worktrees/` exists | Use it (verify .gitignore) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md → Ask user |
| Directory not in .gitignore | Add it immediately + commit |
| Tests fail during baseline | Report failures + ask |

### Common Mistakes

**Skipping .gitignore verification**
- Problem: Worktree contents get tracked
- Fix: Always grep .gitignore before creating project-local worktree

**Assuming directory location**
- Problem: Creates inconsistency
- Fix: Follow priority: existing > CLAUDE.md > ask

**Proceeding with failing tests**
- Problem: Can't distinguish new bugs from pre-existing
- Fix: Report failures, get explicit permission

### Example Workflow

```
You: I'm using the using-git-worktrees skill to set up an isolated workspace.

[Check .worktrees/ - exists]
[Verify .gitignore - contains .worktrees/]
[Create worktree: git worktree add .worktrees/auth -b feature/auth]
[Run npm install]
[Run npm test - 47 passing]

Worktree ready at /Users/jesse/myproject/.worktrees/auth
Tests passing (47 tests, 0 failures)
Ready to implement auth feature
```

### Red Flags

**Never:**
- Create worktree without .gitignore verification (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous

**Always:**
- Follow directory priority: existing > CLAUDE.md > ask
- Verify .gitignore for project-local
- Auto-detect and run project setup
- Verify clean test baseline

### Integration

**Called by:**
- **brainstorming** (Phase 4) - REQUIRED when design is approved
- Any skill needing isolated workspace

**Pairs with:**
- **finishing-a-development-branch** - REQUIRED for cleanup
- **executing-plans** or **subagent-driven-development** - Work happens in worktree

## Analysis

**What makes this work**:

1. **Systematic 3-step selection**: Existing > CLAUDE.md > Ask
2. **Safety verification**: .gitignore check before creation
3. **Auto-detection**: Automatically identifies project type
4. **Baseline verification**: Tests must pass before proceeding
5. **Quick reference table**: Common situations and actions
6. **Integration section**: Shows how skill connects to others

## Unique Features

**Announce at Start**:
Explicit instruction to announce skill usage: "I'm using the using-git-worktrees skill..."

**Jesse's Rule Reference**:
"Per Jesse's rule 'Fix broken things immediately'" - references specific principle.

**Priority Order**:
Three-step priority: existing directories > CLAUDE.md preference > ask user.

**Safety as Principle**:
"Fix broken things immediately" - add to .gitignore before creating worktree.

**Auto-Detection**:
Checks for package.json, Cargo.toml, requirements.txt to determine setup commands.

**Baseline Verification**:
Runs tests to ensure starting point is clean.

**Integration Section**:
Explicitly states which skills call this skill and which skills pair with it.

## Pattern Type

**Workflow automation with safety** - Systematic selection + verification + setup.

## Key Takeaways

1. **Priority order simplifies decisions** - Existing > CLAUDE.md > Ask
2. **Safety verification prevents accidents** - .gitignore check before creation
3. **Auto-detection reduces configuration** - Detect project type automatically
4. **Baseline verification essential** - Must start with passing tests
5. **Quick reference tables help** - Common situations and actions
6. **Integration sections valuable** - Shows skill relationships
7. **Announce skill usage** - Makes workflow transparent
8. **Fix broken things immediately** - Don't proceed with missing .gitignore
