# Workflow Skill Template

Template for creating workflow skills that automate multi-step processes.

## When to Use This Template

Use this template when creating a skill that:
- Automates a repetitive process (>5 steps manually)
- Has clear start and end points
- Involves multiple systems (git, Beads, Serena, CI, etc.)
- Saves measurable time (minutes → seconds)

**Examples:** sync-feature-branch, create-pull-request, fix-pr-feedback

## Template Structure

```markdown
---
name: workflow-name
description: |
  One-line purpose with MUST BE USED trigger. Use when user wants to [action], [trigger phrase], or [workflow pattern]. Invoke when seeing "[error pattern]", "[status indicator]", "[workflow blocker]", or discussing [workflow context], [operation type], or [system state]. Automatically handles [key automation]. Keywords: [keyword1], [keyword2], [keyword3], [cli-command], [operation-verb], [system-name]
tags: [workflow, [system], [operation-type]]
allowed-tools:
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(bd:*)
  - Read
  - Edit
---

# Workflow Name

One-line purpose (<time> total).

## Purpose

[What this workflow automates and why it exists]

**Philosophy:** [Core principle - e.g., "Fast commits + Trust CI"]

## When to Use This Skill

**Trigger phrases:**
- "[natural language phrase 1]"
- "[natural language phrase 2]"
- "[natural language phrase 3]"

**Automatically invoked when:**
- [Pattern 1]
- [Pattern 2]
- [Pattern 3]

## Workflow

### 1. [Check Context / Verify Prerequisites]

[What to check before starting]

```[language]
# Verification code
```

**Fail fast if:**
- [Critical prerequisite missing]
- [Blocking condition]

### 2. [Gather Information]

[Use Serena/Beads/git to get current state]

**A. [Information source 1]**
```[language]
# How to get info
```

**B. [Information source 2]**
```[language]
# How to get info
```

### 3. [Execute Core Action]

[Main workflow steps (3-7 steps typically)]

**Step 1: [Action name]**
```[language]
# Implementation
```

**Step 2: [Action name]**
```[language]
# Implementation
```

### 4. [Validate Results]

[Quick checks (<5s), trust environments for full validation]

```[language]
# Validation code
```

### 5. [Update State]

[Commit changes, update Beads, confirm to user]

```[language]
# State update code
```

**Confirm to user:**
```
✅ [What was accomplished]
✅ [Side effect 1]
✅ [Side effect 2]

Next: [What user should do next]
```

## Integration Points

### With Beads

[How this skill uses Beads CLI]

- **Check context:** `bd show <issue_id>`
- **Update status:** `bd update <issue_id> status=<status>`
- **Close on success:** `bd close <issue_id> reason="..."`
- **Create discoveries:** `bd create ...`

**Pattern:**
```bash
# Beads integration example
bd update $ISSUE_ID status=in_progress
```

### With Code Search

[How this skill uses native search]

- **Search:** `grep -r "pattern" .`
- **Find Files:** `find . -name "pattern"`
- **Navigate:** `read_file` tools

**Pattern:**
```bash
# Native search example (via Bash tool)
grep -r "TODO" src/
```

### With Git

[How this skill uses git]

- **Status:** `git status`, `git branch --show-current`
- **Changes:** `git add`, `git commit`
- **Remote:** `git push`, `gh pr create`

**Pattern:**
```bash
# Git integration example
```

### With [Other System]

[If applicable - CI, external APIs, etc.]

## Best Practices

### Do

✅ [Best practice 1]
✅ [Best practice 2]
✅ [Best practice 3]
✅ [Best practice 4]
✅ [Best practice 5]

### Don't

❌ [Anti-pattern 1]
❌ [Anti-pattern 2]
❌ [Anti-pattern 3]
❌ [Anti-pattern 4]

## What This Skill Does

✅ [Capability 1]
✅ [Capability 2]
✅ [Capability 3]
✅ [Capability 4]
✅ [Capability 5]

## What This Skill DOESN'T Do

❌ [Out of scope 1]
❌ [Out of scope 2]
❌ [Out of scope 3]
❌ [Out of scope 4]

## Examples

### Example 1: [Simple Case]

```
User: "[trigger phrase]"

AI execution:
1. [Step 1 result]
2. [Step 2 result]
3. [Step 3 result]

Outcome:
✅ [Result 1]
✅ [Result 2]
```

### Example 2: [Complex Case]

```
User: "[trigger phrase]"

AI execution:
1. [Step 1 result]
2. [Discovers problem]
3. [Handles problem]
4. [Continues workflow]

Outcome:
✅ [Result 1]
⚠️ [Warning or note]
✅ [Result 2]
```

### Example 3: [Edge Case]

```
User: "[trigger phrase]"

AI execution:
1. [Step 1 result]
2. [Error condition detected]
3. [Graceful failure or recovery]

Outcome:
❌ [What failed]
ℹ️ [Guidance to user]
```

## Troubleshooting

### [Problem 1]

**Symptom:** [Description]

**Cause:** [Root cause]

**Fix:**
```[language]
# Solution code
```

### [Problem 2]

**Symptom:** [Description]

**Cause:** [Root cause]

**Fix:**
```[language]
# Solution code
```

## Related Skills

- **[skill-name-1]**: [How it relates]
- **[skill-name-2]**: [How it relates]
- **[skill-name-3]**: [How it relates]

## Resources

**Progressive disclosure files:**
- `resources/examples/[scenario].md` - [Description]
- `resources/patterns/[pattern].md` - [Description]
- `resources/reference/[topic].md` - [Description]

---

**Last Updated:** [Date]
**Skill Type:** Workflow
**Average Duration:** [Time]
**Related Docs:**
- [Document 1]
- [Document 2]
```

## Workflow Skill Checklist

When creating a workflow skill, ensure:

- [ ] Clear trigger phrases (3-5 natural language patterns)
- [ ] Fast execution time (<1 minute ideal)
- [ ] Quick validation only (<5s), trust environments
- [ ] Proper Beads integration (check/create/update/close)
- [ ] Serena-first for code operations (not bash)
- [ ] Git operations follow conventions (Feature-Key trailers)
- [ ] Error handling (fail fast, clear messages)
- [ ] User confirmation (show what happened)
- [ ] Progressive disclosure (<500 lines main file)
- [ ] Examples (simple, complex, edge case)
- [ ] Integration points documented
- [ ] Best practices and anti-patterns listed

## Common Workflow Patterns

### Check-Execute-Update Pattern

```
1. Check prerequisites (fail fast)
2. Execute core workflow
3. Update state (Beads, git, etc.)
4. Confirm to user
```

**Use for:** Most workflow skills

### Discover-Fix-Track Pattern

```
1. Discover problems
2. Categorize by severity
3. Fix simple, ask for complex
4. Track in Beads
5. Update and confirm
```

**Use for:** PR feedback, debugging, cleanup workflows

### Gather-Transform-Commit Pattern

```
1. Gather current state
2. Transform (code changes, data processing)
3. Validate transformation
4. Commit results
5. Confirm
```

**Use for:** Code generation, refactoring, data migration

## Time Budget Guidelines

| Operation Type | Time Budget |
|----------------|-------------|
| Quick commits | <30s |
| PR creation | <10s |
| PR fixes | <2min per issue |
| Code search | <5s |
| Validation | <5s (quick checks only) |
| Full workflow | <1min ideal |

## Integration Checklist

### Beads Integration

- [ ] Call `set_context()` at start
- [ ] Check issue exists (create if missing)
- [ ] Update status during workflow
- [ ] Close on success with reason
- [ ] Create child issues for discoveries
- [ ] Link with discovered-from

### Serena Integration

- [ ] Use `search_for_pattern` instead of grep
- [ ] Use `list_dir` instead of find
- [ ] Use `get_symbols_overview` before reading files
- [ ] Use `find_symbol` for targeted reads
- [ ] Use `replace_symbol_body` for symbol edits
- [ ] Use `insert_after_symbol` for additions

### Git Integration

- [ ] Extract Feature-Key from branch name
- [ ] Include Feature-Key in commit trailers
- [ ] Add Agent and Role trailers
- [ ] Push to correct remote
- [ ] Use gh CLI for PR operations
- [ ] Handle git errors gracefully

## Testing Workflow Skills

### Test Cases

1. **Happy path:** All prerequisites met, workflow succeeds
2. **Missing prerequisites:** Fail fast with clear message
3. **Partial success:** Some steps succeed, others fail gracefully
4. **Discovery during execution:** Create child issues, continue
5. **External failures:** CI failures, network errors, API errors

### Test Execution

```bash
# 1. Test auto-activation
User says: "[trigger phrase]"
→ Verify hook detects it
→ Verify skill invoked

# 2. Test workflow
Follow skill steps
→ Check each step works
→ Verify Beads updated
→ Verify git operations succeed

# 3. Test edge cases
Missing branch name
→ Skill fails gracefully

Missing Beads issue
→ Skill creates proactively

CI failure
→ Skill completes, CI runs async
```

## Real Examples

### sync-feature-branch

**Type:** Check-Execute-Update
**Time:** 25s
**Pattern:**
1. Extract Feature-Key from branch
2. Check Beads issue exists
3. Quick lint (<5s)
4. Git commit with trailers
5. Update Beads status

### create-pull-request

**Type:** Gather-Transform-Commit
**Time:** 10s
**Pattern:**
1. Get Feature-Key and Beads context
2. Push branch if needed
3. Create PR with gh CLI
4. Link PR to Beads
5. Confirm to user

### fix-pr-feedback

**Type:** Discover-Fix-Track
**Time:** 2min per issue
**Pattern:**
1. Get PR context (comments, CI, conflicts)
2. Categorize discoveries
3. Create child Beads issues
4. Fix simple, ask for complex
5. Commit fixes with child Feature-Keys
6. Close child issues

---

**Related:**
- resources/skill-types.md - Skill type details
- resources/v3-philosophy.md - V3 principles
- sync-feature-branch/SKILL.md - Real workflow skill
