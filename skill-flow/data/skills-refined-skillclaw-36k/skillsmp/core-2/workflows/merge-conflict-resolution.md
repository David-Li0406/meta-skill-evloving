# Merge Conflict Resolution Workflow

**Purpose**: Systematic approach to resolving git merge conflicts using analysis and trade-off evaluation.

**Last Updated**: 2025-11-19

---

## Trigger Phrases
- "merge conflict"
- "resolve conflicts"
- "git conflicts"
- "conflicting changes"
- "merge failed"

---

## When to Use This Workflow

**Activate when:**
- `git merge` or `git pull` results in conflicts
- Multiple branches have divergent changes
- Need to choose between competing implementations

**Don't use for:**
- Simple file overwrites
- Clear-cut "take theirs" or "take ours" situations

---

## The Workflow

### Step 1: Assess the Conflict

```bash
# List conflicting files
git status

# Examine conflicts
git diff --check
cat conflicted-file.ts
```

### Step 2: Analyze Both Versions

**For each conflicting section:**
- Understand current branch (HEAD): What does this code do? Why?
- Understand incoming branch: What does this code do? Why?
- Identify conflict type: Logic, API, structure, or content

### Step 3: Evaluate Trade-offs

**For each version, analyze:**
- **Correctness**: Does it work? Handle edge cases?
- **Performance**: Which is faster? Scales better?
- **Maintainability**: Easier to understand? Test? Modify?
- **Compatibility**: Fewer breaking changes? Matches patterns?

### Step 4: Choose Resolution Strategy

**Strategy A: Take One Version**
```bash
git checkout --ours conflicted-file.ts   # Take current
git checkout --theirs conflicted-file.ts # Take incoming
git add conflicted-file.ts
```

**Strategy B: Merge Both**
```typescript
// Combine both approaches
function processData(input: string | string[]) {
  if (Array.isArray(input)) {
    return input.map(s => s.trim());
  }
  return input.toUpperCase();
}
```

**Strategy C: Create New Solution**
```typescript
// Better solution combining insights
function processData(input: string | string[]): string[] {
  const items = Array.isArray(input) ? input : [input];
  return items.map(s => s.trim().toUpperCase());
}
```

### Step 5: Resolve and Test

```bash
# Edit file, remove conflict markers
code conflicted-file.ts

# Test the resolution
bun test conflicted-file.test.ts

# Stage resolution
git add conflicted-file.ts
```

### Step 6: Complete Merge

```bash
# Verify all conflicts resolved
git status

# Complete merge
git merge --continue
# or git rebase --continue

# Write meaningful commit message
```

---

## Best Practices

### 1. Understand Before Resolving
Never blindly choose a version. Always read and understand both.

### 2. Test After Resolution
```bash
bun test
bun run lint
bun run build
```

### 3. Document Complex Resolutions
Explain in commit message what conflicted, why you chose this resolution, and what trade-offs were made.

### 4. Get Review for Major Conflicts
When logic changes you don't understand or architectural decisions are involved.

---

## Abort and Restart

```bash
# If resolution goes wrong
git merge --abort
# or
git rebase --abort

# Review and try again
git diff HEAD..feature-branch
```

---

## Quick Reference

```bash
# View conflicts
git status
git diff --check

# Take ours/theirs
git checkout --ours file.ts
git checkout --theirs file.ts

# Mark resolved
git add file.ts

# Continue
git merge --continue
git rebase --continue

# Abort
git merge --abort
git rebase --abort
```

---

**Key Takeaways:**
1. Understand both versions before resolving
2. Evaluate trade-offs systematically
3. Test after every resolution
4. Document complex decisions
5. Don't be afraid to ask for help
