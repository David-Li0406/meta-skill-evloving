# Fixing Compilation Errors After Absorb

After `stackit absorb`, compilation errors may occur when absorbed changes depend on files/changes that didn't get cleanly absorbed into the same commit.

> **CRITICAL:** Always run stackit commands with `command stackit ... --no-interactive`. For commands that require confirmation, also include the `--yes` or `-y` flag.

## Why This Happens

`stackit absorb` uses heuristics to assign each change to the "best matching" commit. Sometimes:
- A function definition goes to commit A
- The function usage goes to commit B
- Commit B now fails to build because the function isn't defined yet

This is normal and fixable by moving the dependency to the earlier commit.

## Workflow Checklist

Copy this checklist and track your progress:

```
Absorb Fix Progress:
- [ ] Step 1: Identify build/test commands
- [ ] Step 2: Build and test each branch
- [ ] Step 3: Identify failed branches
- [ ] Step 4: Find missing dependencies
- [ ] Step 5: Apply fixes
- [ ] Step 6: Verify entire stack
```

## Step 1: Identify Build/Test Commands

**Find the project's build and test commands:**

1. Check README.md or CONTRIBUTING.md for build/test instructions:
   ```bash
   grep -i "build\|compile\|test" README.md CONTRIBUTING.md
   ```

2. Look for common build configuration files (Makefile, package.json, etc.)

3. If not found, ask the user:
   - "What command should I use to build the project?"
   - "What command should I use to run tests?"

## Step 2: Build and Test Each Branch

Starting from the **bottom** of the stack (earliest branch), build and test each branch:

```bash
# Get list of branches in stack order
command stackit log --no-interactive

# For each branch (bottom to top):
git checkout <branch-name>
<build-command>
<test-command>
```

**Mark which branches fail** - you'll need this for Step 3.

## Step 3: Identify Failed Branches

For each failed branch, analyze the error:

```bash
# Example: Build failed on branch "add-validation"
git checkout add-validation

# Run build and capture error
<build-command> 2>&1 | tee build-error.log

# Common error patterns:
# - "undefined: functionName" → function defined in later commit
# - "cannot find module" → import added in later commit
# - "type not defined" → type definition in later commit
```

**Write down:**
- Branch name
- What's missing (function, type, file, import, etc.)
- Error message

## Step 4: Find Missing Dependencies

For each missing item, search upstack branches for where it's defined:

```bash
# Get child branch name
command stackit children --no-interactive

# Check what changes exist in child that aren't in current
git diff <current-branch>..<child-branch>

# Or search for specific item
git log <current-branch>..<child-branch> --all -S "functionName"
```

**Look for:**
- Function definitions
- Type definitions
- New files
- Import statements
- Configuration changes

## Step 5: Apply Fixes

For each missing dependency, move it to the failing branch:

### Option A: Cherry-pick specific commit

```bash
# If the needed change is in a single commit
git cherry-pick <commit-hash>

# Resolve conflicts if needed
git add .
git cherry-pick --continue
```

### Option B: Manual copy

```bash
# If change is spread across commits, manually apply:
# 1. View the change in child branch
git diff <current-branch>..<child-branch> -- path/to/file.go

# 2. Apply the specific parts needed
# Edit the file manually, or:
git show <child-branch>:path/to/file.go > path/to/file.go

# 3. Commit the fix
git add path/to/file.go
command stackit modify --no-interactive  # Amends current branch's commit
```

### Option C: Interactive rebase (advanced)

```bash
# Reorder commits to move dependencies earlier
git rebase -i <parent-branch>

# In editor, reorder commits so dependencies come first
# Save and close

# Resolve conflicts
git add .
git rebase --continue
```

## Step 6: Verify Entire Stack

After fixing all branches, verify the entire stack builds:

```bash
# Build all branches in order
command stackit foreach --no-interactive "<build-command>"

# Test all branches
command stackit foreach --no-interactive "<test-command>"
```

**Expected output:**
```
Branch: add-auth
✓ Build succeeded
✓ Tests passed

Branch: add-validation
✓ Build succeeded
✓ Tests passed

Branch: add-api-endpoints
✓ Build succeeded
✓ Tests passed
```

## Validation Loop

For each branch:
1. Run build command
2. **If fails:**
   - Analyze error message
   - Find missing dependency (Step 4)
   - Apply fix (Step 5)
   - Re-run build
   - Repeat until build succeeds
3. **If passes:**
   - Mark checklist item complete
   - Move to next branch

**Only consider fix complete when all branches build and test successfully.**

## Prevention Tips

To avoid this in the future:

1. **Keep changes focused**: Absorb works best when changes are closely related
2. **Absorb frequently**: Smaller sets of changes = fewer dependency issues
3. **Check as you go**: Run build after absorb to catch issues early
4. **Use modify for small fixes**: `command stackit modify --no-interactive` is safer for targeted changes

## Example Walkthrough

**Scenario:** After absorb, `add-validation` branch fails to build.

**Error:** `undefined: validateUser`

**Steps:**
```bash
# 1. Find where validateUser is defined
git log add-validation..add-api-endpoints --all -S "validateUser"
# → Found in commit abc123 on add-api-endpoints

# 2. Check the change
git show abc123
# → Shows validateUser function definition

# 3. Cherry-pick it
git checkout add-validation
git cherry-pick abc123

# 4. Verify fix
<build-command>
# ✓ Build succeeded

# 5. Restack children (they're now based on old version)
command stackit restack --no-interactive

# 6. Verify entire stack
command stackit foreach --no-interactive "<build-command>"
# ✓ All branches succeed
```

## Success Criteria

- ✓ All branches build without errors
- ✓ All branches pass tests
- ✓ Stack structure is clean (`command stackit log --no-interactive` shows proper tree)
- ✓ No git conflicts or issues
