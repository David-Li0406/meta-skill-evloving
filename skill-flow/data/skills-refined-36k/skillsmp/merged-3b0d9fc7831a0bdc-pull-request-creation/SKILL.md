---
name: pull-request-creation
description: Use this skill when you need to create a pull request with a standardized workflow, including quality checks and integration with tracking systems.
---

# Pull Request Creation Workflow

**Mission**: Ensure every pull request (PR) is created with complete context, quality checks, and proper tracking.

---

## Workflow Overview

This skill provides a comprehensive workflow for creating pull requests, including:

1. **Identify Target Branch**: Determine the branch to merge into.
2. **Run Quality Checks**: Execute configurable quality checks (linting, building, testing).
3. **Identify Tracking**: Check for JIRA tickets or git issue references in commits.
4. **Create Pull Request**: Create a PR linked to tracking systems with a comprehensive description.
5. **Handle Images**: Upload local images and embed them in PR description/comments.
6. **Merge Confirmation**: Prompt user for merge target after PR creation.

---

## Step 1: Identify Target Branch

**Purpose**: Determine the correct base branch for the PR.

**Detection Methods**:

| Method | Description | Command |
|--------|-------------|----------|
| Ask user | Prompt for target branch | N/A (interactive) |
| Detect default | Get repository default branch | `git symbolic-ref refs/remotes/origin/HEAD` |
| Read config | Check for configured default | Read `.git/config` |

---

## Step 2: Run Quality Checks

**Purpose**: Verify code quality before creating the PR.

**Configurable Checks**:

| Check Type | Command |
|------------|---------|
| Linting | `npm run lint` (JavaScript) / `poetry run ruff check` (Python) |
| Building | `npm run build` (JavaScript) |
| Testing | `npm run test` (JavaScript) / `poetry run pytest` (Python) |
| Type Checking | `npm run typecheck` (JavaScript) / `poetry run mypy .` (Python) |

**Quality Check Execution**:
```bash
# Example for linting check
if [ "$RUN_LINTING" = "true" ]; then
  npm run lint
fi
```

---

## Step 3: Identify Tracking System

**Purpose**: Determine if the PR should link to a JIRA ticket or git issue.

**Detection Methods**:

| Source | Detection Pattern | Example |
|--------|------------------|---------|
| Commit messages | Regex for JIRA ticket key | `[IBIS-123] Fix bug` |
| PLAN.md | Search for JIRA references | `JIRA Reference: IBIS-456` |
| Branch name | Parse ticket key from branch | `IBIS-101-add-feature` |

---

## Step 4: Check Git Status

**Purpose**: Verify all changes are committed and the branch is ready for PR.

**Git Status Checks**:
```bash
# Check if working tree is clean
GIT_STATUS=$(git status --porcelain)
if [ -n "$GIT_STATUS" ]; then
  echo "Warning: You have uncommitted changes."
fi
```

---

## Step 5: Create Pull Request

**Purpose**: Create the PR with a comprehensive description linked to the tracking system.

**PR Creation Command**:
```bash
gh pr create --base "$TARGET_BRANCH" --title "feat: <summary> [${TRACKING_ID}]" --body "$(cat <<'EOF'
## Summary
<Bullet points describing changes>

## Tracking Reference
- Ticket: ${TRACKING_ID}

## Quality Checks
- Linting: ${LINT_RESULT}
- Build: ${BUILD_RESULT}
- Tests: ${TEST_RESULT}
EOF
)"
```

---

## Step 6: Handle Images in PR

**Purpose**: Upload local images to hosting platform or reference in PR.

**Image Handling Strategy**:
```bash
if [ "$INCLUDE_IMAGES" = "y" ]; then
  for image in "${IMAGES[@]}"; do
    # Upload or embed image logic here
  done
fi
```

---

## Step 7: Merge Confirmation

**Purpose**: Ask the user to confirm the merge target after successful PR creation.

**Implementation**:
```bash
read -p "Would you like to proceed with merging this PR? (y/n): " MERGE_CONFIRMATION
if [ "$MERGE_CONFIRMATION" = "y" ]; then
  gh pr merge "$PR_NUMBER"
fi
```

---

## Best Practices

- **Target Branch**: Don't hardcode to `dev` - ask the user or detect the default.
- **Quality Checks**: Make them configurable - not all projects need all checks.
- **Tracking Links**: Always include JIRA/git issue references for traceability.
- **PR Descriptions**: Use a consistent format with summary, changes, and quality checks.

---

## Common Issues

### Target Branch Not Specified
**Solution**: Prompt user for target branch if auto-detection fails.

### Quality Checks Fail
**Solution**: Offer to fix automatically or ask if the user wants to continue anyway.

### Tracking Not Detected
**Solution**: Create a standalone PR without tracking reference or ask the user to provide one.

---

## Relevant Commands

```bash
# Get current branch
git branch --show-current

# Create PR
gh pr create --base <target> --title "Title" --body "Description"
```

---

## Relevant Skills

Skills that use this PR creation framework:
- `git-pr-creator`: PR creation with JIRA integration and image uploads.
- `nextjs-pr-workflow`: Next.js-specific PR workflow with linting and building.