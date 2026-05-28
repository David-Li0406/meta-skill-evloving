---
name: create-mr
description: Create a GitLab merge request using conversation context
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash(git:*)
  - Bash(glab mr create:*)
  - Bash(glab repo view:*)
  - Bash(code --wait:*)
  - Bash(~/.claude/skills/create-mr/scripts/glab-mr-helper.sh:*)
---

# Create Merge Request

Create a GitLab merge request using the context already present in this Claude session.

## glab CLI Reference

The `glab` CLI is GitLab's official command-line tool. Key commands:

```bash
# Create MR with title and description
glab mr create --title "Title" --description "Body" --target-branch main --remove-source-branch --yes

# View project info (includes project ID)
glab repo view

# List open MRs (useful for finding parent MRs)
glab mr list --state opened
```

For complex API operations (finding parent MRs, creating blocking relationships), use the helper script at `~/.claude/skills/create-mr/scripts/glab-mr-helper.sh`.

## Steps

### 1. Check if branch is pushed to origin

```bash
git branch --show-current | sed 's|^|origin/|g' | xargs git rev-parse --verify
```

If this fails, push the branch:

```bash
git push -u origin $(git branch --show-current)
```

### 2. Determine target branch

```bash
git merge-target || echo 'main'
```

### 3. Generate title and description

Review the commits and diffs:

```bash
# Get target branch
TARGET=$(git merge-target || echo 'main')

# See all commits
git log --oneline $TARGET..HEAD

# See full commit messages
git log $TARGET..HEAD

# See the complete diff
git diff $TARGET...HEAD
```

#### Title Guidelines

- Max 80 characters
- Imperative mood ("Add feature" not "Added feature")
- Concise but descriptive

#### Description Guidelines

Brian's preferred MR description format:

1. **Context first**: Explain the problem or need that motivated this change
2. **Approach**: Describe what you did and why you chose this approach
3. **Testing**: How was this tested? Include manual testing steps if applicable
4. **Conversation context**: Reference relevant discussion from this Claude session

Check for MR templates:
- `.gitlab/merge_request_templates/Default.md`
- `.gitlab/merge_request_templates/default.md`

If a template exists, follow its structure.

### 4. Open MR content in editor

Write the draft to a file in the current directory:

```bash
# Filename: mr-<sanitized-branch-name>.md
# Format:
# Title here
#
# Description starts here
# and continues...
```

Open with VS Code and wait for edits:

```bash
code --wait mr-branch-name.md
```

After Brian saves and closes:
- Parse title from first line (strip leading `#` if present)
- Parse description from remaining content
- If file is empty/whitespace only, abort
- Delete the temp file after parsing

### 5. Create the merge request

```bash
glab mr create \
  --title "Title from editor" \
  --description "Description from editor" \
  --target-branch "$TARGET" \
  --remove-source-branch \
  --yes
```

Extract the MR URL and number from output.

### 6. Handle stacked MRs (blocking dependencies)

**When the target branch is not `main`**, this is a stacked MR. Set up blocking:

Use the helper script:

```bash
~/.claude/skills/create-mr/scripts/glab-mr-helper.sh set-blocking <this-mr-number> <target-branch>
```

This script:
1. Finds the open MR where source branch = our target branch (the parent MR)
2. Creates a blocking relationship so the parent must merge first

**Why this matters**: GitLab's "merge trains" work better when MRs have explicit dependencies. The blocking relationship prevents merging this MR before its parent.

If the parent MR can't be found or the blocking setup fails, warn but don't fail the whole operation.

### 7. Generate Slack review request

Output for Brian to copy:

```
Please review my MR to [$TITLE]($MR_URL)
```

## Key Points

- Leverage conversation context from this Claude session
- The MR description should reflect the reasoning and discussion, not just commits
- Always confirm with Brian before creating the MR
- Handle errors gracefully and report them clearly

## Example Workflow

```
Claude: "I see you're on branch feature/add-validation. Let me check if it's pushed..."
Claude: "Branch is pushed. Target branch is 'develop'."
Claude: "Based on our work, here's the proposed MR:

Title: Add input validation to user registration

Description:
## Summary
Implement comprehensive input validation...

Does this look good? Should I proceed?"

Brian: "yes"

Claude: [creates MR, sets up blocking if needed, shows Slack message]
```
