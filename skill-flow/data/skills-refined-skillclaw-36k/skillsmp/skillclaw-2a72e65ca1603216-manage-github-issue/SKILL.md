---
name: manage-github-issue
description: Use this skill when you want to create an implementation plan for a GitHub issue and then execute that plan to implement the issue.
---

# Skill body

## Purpose

This skill allows you to create a detailed implementation plan for a GitHub issue and then execute that plan step by step, ensuring a structured approach to issue resolution.

## Workflow

### Step 1: Verify Environment

Check that you have a GitHub remote and are on a clean, up-to-date main/master branch:

```bash
git remote -v
git status
git fetch origin
git rev-parse --abbrev-ref HEAD
git status -uno
```

**STOP if:**
- No remote exists → "This skill requires a GitHub remote. Please add one with `git remote add origin <url>` first."
- Not on main/master → "Please switch to main/master first: `git checkout main`"
- Uncommitted changes → "Please commit or stash your changes first."
- Behind remote → "Please pull latest changes: `git pull`"

### Step 2: Identify the Ticket

User will provide a GitHub issue number (e.g., `#12` or `12`). If not clear, ask which ticket to manage.

### Step 3: Create the Implementation Plan

If no plan exists, create one by reading the ticket:

```bash
gh issue view <number>
```

Understand:
- What needs to be done
- Why it's needed
- Any constraints or notes

Write a plan that:
- Lists concrete steps in order
- Names specific files/modules that will be touched
- Describes what each step accomplishes
- Makes success criteria obvious

**Plan format:**

```markdown
## Implementation Plan

### Steps

1. **<Action>** - <What this accomplishes>
   - Files: `path/to/file.py`
   - <Brief description of the change>

2. **<Action>** - <What this accomplishes>
   - Files: `path/to/other.py`
   - <Brief description of the change>

...

### Success Criteria

- [ ] <Observable outcome 1>
- [ ] <Observable outcome 2>
- [ ] <Observable outcome 3>
```

### Step 4: Add Plan to Issue

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Implementation Plan

...plan content...
EOF
)"
```

### Step 5: Setup Working Branch

**Ask the user:** "Do you want to use a worktree (allows parallel work on other tickets) or branch in place?"

#### Option A: Worktree (recommended for parallel work)

Use the `/worktree create <branch-name>` skill to create an isolated working directory.

#### Option B: Branch in place

Standard approach, switches the current repo to a new branch:

```bash
git checkout main && git pull
git checkout -b <branch-name>
```

### Step 6: Read Ticket and Plan

```bash
gh issue view <number> --comments
```

Extract:
- The original intent (Summary section)
- The implementation plan (Steps)
- The success criteria

If no implementation plan exists, STOP and tell the user to run the plan creation step first.

### Step 7: Execute the Plan

Work through each step in the plan:

1. Read the step
2. Implement it
3. Verify it works
4. Move to the next step

### Step 8: Close the Ticket

Once all steps are completed and verified, close the ticket:

```bash
gh issue close <number>
```

### Reporting Back

Tell the user the plan has been added and summarize the key steps taken during implementation.