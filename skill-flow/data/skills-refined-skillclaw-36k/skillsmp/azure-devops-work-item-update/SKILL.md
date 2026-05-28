---
name: azure-devops-work-item-update
description: Update Azure DevOps work items after implementation completion by linking git commits, adding implementation summaries, and updating status to 'Ready for Testing'. Use when completing a task, finishing a user story, after git commit, or updating work item status. Ensures work items reflect actual work done and maintains traceability between code and work items.
---

# Azure DevOps Work Item Update

Automate updating Azure DevOps work items after implementation with git commit links, implementation summaries, and status updates.

## Quick Start

**Update task after commit:**
```
"Update Azure DevOps task 1234 with git commit abc123, add summary 'Implemented singleton pattern', set status to Ready for Testing"
```

**Update from git log:**
```
"Update work items referenced in last 3 commits with implementation summaries and set to Ready for Testing"
```

## Core Workflow

### Step 1: Identify Work Item and Commit

**From explicit work item ID:**
- Work item ID: 1234
- Git commit SHA: abc123def456

**From git commit message:**
- Parse commit message for work item reference
- Format: `feat(#1234): Description` or `fix: Description (#1234)`
- Extract work item ID from commit message

**From recent commits:**
```bash
git log -3 --oneline
# Extract work item IDs from commit messages
```

### Step 2: Get Current Work Item State

Query Azure DevOps for current work item:

```
mcp__azure-devops__wit_get_work_item(
  project: "ProjectName",
  id: 1234
)
```

**Capture**:
- Current state (New, Active, etc.)
- Current assigned to
- Work item type (Task, User Story, Bug, etc.)
- Title
- Current description

### Step 3: Generate Implementation Summary

Create summary from:
- Git commit message
- Files changed in commit
- Implementation notes (if provided)

**Format**:
```
Implementation Summary:
- Implemented [feature/fix description]
- Files modified: [list key files]
- Git commit: [commit SHA]
- Completed on: [date]
```

### Step 4: Link Git Commit to Work Item

Add git commit as external link:

```
mcp__azure-devops__wit_update_work_items_batch(
  project: "ProjectName",
  updates: [{
    id: 1234,
    updates: [{
      op: "add",
      path: "/relations/-",
      value: {
        rel: "Hyperlink",
        url: "https://github.com/org/repo/commit/abc123def456",
        attributes: {
          comment: "Implementation commit"
        }
      }
    }]
  }]
)
```

### Step 5: Add Implementation Comment

Add comment with implementation summary:

```
mcp__azure-devops__wit_update_work_items_batch(
  project: "ProjectName",
  updates: [{
    id: 1234,
    updates: [{
      op: "add",
      path: "/fields/System.History",
      value: "<p><b>Implementation Complete</b></p><p>[Implementation summary from Step 3]</p>"
    }]
  }]
)
```

### Step 6: Update Status to 'Ready for Testing'

Update work item state:

```
mcp__azure-devops__wit_update_work_items_batch(
  project: "ProjectName",
  updates: [{
    id: 1234,
    updates: [{
      op: "add",
      path: "/fields/System.State",
      value: "Ready for Testing"
    }]
  }]
)
```

**Note**: For User Stories, may use "Resolved" state instead based on workflow.

## Key Concepts

**Work Item Types**:
- **Task**: Individual work item, typically child of User Story
- **User Story**: Feature implementation, parent of tasks
- **Bug**: Defect fix

**State Transitions**:
- **Active** → **Ready for Testing** (Tasks)
- **Active** → **Resolved** (User Stories, Bugs)
- Custom states may vary by project

**Git Commit Linking**:
- External hyperlink relation type
- Points to GitHub/Azure Repos commit URL
- Provides traceability from work item to code changes

**Implementation Summary**:
- Added as comment (System.History field)
- HTML formatted
- Includes commit reference, files changed, description

## Available Resources

### Scripts

- **scripts/extract_work_item_from_commit.py** — Extract work item ID from git commit message
  ```bash
  python scripts/extract_work_item_from_commit.py --commit-sha abc123
  # Returns: work_item_id: 1234
  ```

- **scripts/generate_update_payload.py** — Generate Azure DevOps update payload
  ```bash
  python scripts/generate_update_payload.py \
    --work-item-id 1234 \
    --commit-sha abc123 \
    --commit-url "https://github.com/org/repo/commit/abc123" \
    --summary "Implemented singleton pattern for ConfigManager" \
    --files-changed "src/services/ConfigManager.ts,tests/ConfigManager.test.ts" \
    --target-state "Ready for Testing"
  # Returns: Formatted payload for MCP tool
  ```

- **scripts/batch_update_from_commits.py** — Update multiple work items from commit range
  ```bash
  python scripts/batch_update_from_commits.py \
    --git-range "HEAD~5..HEAD" \
    --project "ProjectName" \
    --repo-url "https://github.com/org/repo"
  # Returns: Batch payload for multiple work items
  ```

### References

- **references/state-transitions.md** — Valid state transitions by work item type
- **references/commit-message-patterns.md** — Supported commit message formats for work item extraction
- **references/update-payloads.md** — Example JSON payloads for different update scenarios

## Update Scenarios

### Scenario 1: Single Task Completion

**Situation**: Completed implementation of a task, made git commit

**Steps**:
1. Extract work item ID from commit message
2. Generate implementation summary from commit
3. Link commit to work item
4. Add implementation comment
5. Update state to "Ready for Testing"

**Example**:
```bash
# Git commit made
git commit -m "feat(#1234): Implement ConfigManager singleton"

# Update work item
python scripts/generate_update_payload.py \
  --work-item-id 1234 \
  --commit-sha $(git rev-parse HEAD) \
  --commit-url "https://github.com/org/repo/commit/$(git rev-parse HEAD)" \
  --summary "Implemented ConfigManager as singleton pattern" \
  --target-state "Ready for Testing"
```

---

### Scenario 2: User Story with Multiple Tasks

**Situation**: Completed all tasks for a user story

**Steps**:
1. Update all child tasks to "Ready for Testing"
2. Add summary comment to parent User Story
3. Link commits from all tasks
4. Update User Story to "Resolved"

**Example**:
```bash
# Get all tasks for user story
# Update each task with its commit
# Update parent user story with summary
python scripts/batch_update_from_commits.py \
  --git-range "feature/us-5678..main" \
  --project "ProjectName" \
  --parent-story 5678
```

---

### Scenario 3: Bug Fix

**Situation**: Fixed a bug, made commit

**Steps**:
1. Link commit to bug work item
2. Add fix description as comment
3. Update state to "Resolved"
4. Add "Fixed in commit" reference

**Example**:
```bash
python scripts/generate_update_payload.py \
  --work-item-id 9999 \
  --commit-sha abc123 \
  --commit-url "https://github.com/org/repo/commit/abc123" \
  --summary "Fixed null pointer exception in authentication flow" \
  --target-state "Resolved" \
  --work-item-type "Bug"
```

---

### Scenario 4: Batch Update from Branch

**Situation**: Merged feature branch, need to update all referenced work items

**Steps**:
1. Get all commits in merged branch
2. Extract work item IDs from commit messages
3. Group updates by work item
4. Batch update all work items

**Example**:
```bash
python scripts/batch_update_from_commits.py \
  --git-range "feature/epic-5..main" \
  --project "ProjectName" \
  --repo-url "https://github.com/org/repo" \
  --target-state "Ready for Testing"
```

## Output Format

**Update Payload Structure**:
```json
{
  "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
  "parameters": {
    "project": "ProjectName",
    "updates": [
      {
        "id": 1234,
        "updates": [
          {
            "op": "add",
            "path": "/relations/-",
            "value": {
              "rel": "Hyperlink",
              "url": "https://github.com/org/repo/commit/abc123",
              "attributes": {
                "comment": "Implementation commit"
              }
            }
          },
          {
            "op": "add",
            "path": "/fields/System.History",
            "value": "<p><b>Implementation Complete</b></p><p>Implemented ConfigManager as singleton pattern.</p><p>Files changed: src/services/ConfigManager.ts, tests/ConfigManager.test.ts</p><p>Git commit: abc123</p>"
          },
          {
            "op": "add",
            "path": "/fields/System.State",
            "value": "Ready for Testing"
          }
        ]
      }
    ]
  }
}
```

## Integration with Workflow

**`/implement-waves` integration**:
```markdown
## Step 6: Update Azure DevOps Work Items

After git commit and before closing wave:
- Extract work item IDs from commits
- Invoke `azure-devops-work-item-update` skill
- Link commits to work items
- Add implementation summaries
- Update status to Ready for Testing
- Verify work items updated successfully
```

**Git Workflow Integration**:
```markdown
## Post-Commit Hook

After making commit:
1. Parse commit message for work item ID
2. If work item ID found, offer to update work item
3. Generate implementation summary from commit
4. Update work item automatically
```

## Success Criteria

- ✅ Work item ID extracted correctly from commit message or provided
- ✅ Git commit linked to work item as external hyperlink
- ✅ Implementation summary added as comment
- ✅ Work item state updated to target state
- ✅ All updates applied successfully in single batch
- ✅ No duplicate links created
- ✅ State transition valid for work item type

## Tips for Effective Updates

1. **Use consistent commit message format** - Include work item ID in commits (e.g., `feat(#1234): Description`)
2. **Update immediately after commit** - Don't wait, update while context fresh
3. **Batch related updates** - Update multiple work items from feature branch in one operation
4. **Include meaningful summaries** - Describe what was actually implemented, not just "completed task"
5. **Verify state transitions** - Check valid states for work item type before updating
6. **Link all commits** - If multiple commits for one work item, link all of them
7. **Update parent user stories** - When all tasks complete, update parent story status

## Common Issues and Solutions

### Issue 1: Work Item Not Found
**Problem**: Work item ID doesn't exist
**Solution**: Verify work item ID is correct, check project name

### Issue 2: Invalid State Transition
**Problem**: Can't transition from current state to target state
**Solution**: Check `references/state-transitions.md` for valid transitions, use intermediate state if needed

### Issue 3: Duplicate Commit Links
**Problem**: Commit already linked to work item
**Solution**: Check existing relations before adding, skip if already exists

### Issue 4: Permission Denied
**Problem**: MCP server lacks permission to update work item
**Solution**: Verify Azure DevOps permissions, ensure PAT has "Work Items (Read & Write)" scope

## Validation Checklist

Before updating work item:
- [ ] Work item ID is valid and exists
- [ ] Git commit SHA is valid
- [ ] Commit URL is accessible
- [ ] Implementation summary is meaningful
- [ ] Target state is valid for work item type
- [ ] State transition is allowed
- [ ] Project name is correct

After updating work item:
- [ ] Commit link appears in work item relations
- [ ] Implementation comment visible in work item history
- [ ] Work item state changed to target state
- [ ] No errors returned from MCP tool

## Example: Complete Task Update

```bash
# Step 1: Extract work item from recent commit
git log -1 --pretty=format:"%H %s"
# Output: abc123def456 feat(#1234): Implement ConfigManager singleton

python scripts/extract_work_item_from_commit.py --commit-sha abc123def456
# Output: {"work_item_id": 1234, "commit_message": "Implement ConfigManager singleton"}

# Step 2: Generate update payload
python scripts/generate_update_payload.py \
  --work-item-id 1234 \
  --commit-sha abc123def456 \
  --commit-url "https://github.com/myorg/myrepo/commit/abc123def456" \
  --summary "Implemented ConfigManager as singleton pattern with thread-safe getInstance()" \
  --files-changed "src/services/ConfigManager.ts,tests/ConfigManager.test.ts" \
  --target-state "Ready for Testing" \
  --pretty

# Output: Formatted JSON payload

# Step 3: Apply update via MCP
mcp__azure-devops__wit_update_work_items_batch(
  project: "MyProject",
  updates: [{
    id: 1234,
    updates: [...]
  }]
)

# Output: {"count": 1, "updated": [1234]}

# Step 4: Verify update
mcp__azure-devops__wit_get_work_item(
  project: "MyProject",
  id: 1234
)

# Verify:
# - State = "Ready for Testing"
# - History contains implementation comment
# - Relations contain commit link
```

---

**Last Updated**: 2025-01-21
