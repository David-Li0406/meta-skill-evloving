# Examples: GitHub Issues

The following examples illustrate common issue management workflows.

## Creating a Bug Report

```javascript
// Function Call
issue_write({
  owner: "tech-corp",
  repo: "app-core",
  title: "Bug: Login fails on Safari",
  body: "Steps to reproduce: ...",
  type: "Bug"
});
```

---

## Breaking down a Task (Sub-issues)

**Important**: Both MCP and REST API require the numeric **databaseId** (not Node ID) for the `sub_issue_id` parameter.

### Step 1: Get Database ID (Required)

```bash
# Get the numeric databaseId from an issue number or URL
gh issue view <ISSUE_NUMBER_OR_URL> --json databaseId -q .databaseId
# Returns: 12345678
```

### Step 2: Add Sub-Issue

#### Via MCP

```javascript
// Use the numeric Database ID for the 'sub_issue_id' parameter.
sub_issue_write({
  owner: "tech-corp",
  repo: "app-core",
  issue_number: 101,        // Parent issue number
  sub_issue_id: 12345678,   // Child Database ID (numeric)
  method: "add",
});
```

#### Via REST API (CLI)

```bash
# Add as sub-issue using the parent number and child databaseId
gh api repos/tech-corp/app-core/issues/101/sub_issues -X POST -F sub_issue_id=12345678
```

### Edge Case: Duplicate Sub-Issues

```javascript
// Before adding, check existing sub-issues to avoid HTTP 422 error
issue_read({
  owner: "tech-corp",
  repo: "app-core",
  issue_number: 101,
  method: "get_sub_issues"
});

// Error if duplicate: "This issue is already a child of this issue"
// Solution: Verify the issue is not already a sub-issue before adding
```

### Edge Case: Issue Already Has Parent

```javascript
// If the issue is already a child of another parent, use replace_parent
sub_issue_write({
  owner: "tech-corp",
  repo: "app-core",
  issue_number: 100,        // New parent
  sub_issue_id: 12345678,   // Child Database ID
  method: "add",
  replace_parent: true      // Removes from old parent, adds to new parent
});

// Error without replace_parent: "Sub issue may only have one parent"
// Setting replace_parent: true automatically moves the issue to the new parent
```

---

## Managing Milestones

### Listing Milestones

```bash
# Get all milestones to find the numeric 'number'
gh api /repos/tech-corp/app-core/milestones
```

### Creating a Milestone

```bash
# Create a new milestone using gh api
gh api -X POST /repos/tech-corp/app-core/milestones \
  -f title="v1.0-beta" \
  -f description="Beta release" \
  -f due_on="2025-12-31T23:59:59Z"
```

### Assigning an Issue to a Milestone

```javascript
// MCP Approach (Requires numeric number)
issue_write({
  owner: "tech-corp",
  repo: "app-core",
  issue_number: 123,
  milestone: 1, // Milestone NUMBER from API/List
});
```

```bash
# CLI Approach
gh issue edit 42 --milestone "v1.0-MVP"
```

### Scripting Pattern: Create & Retrieve Metadata

When writing scripts, capture the URL/number and fetch structured details for downstream tasks. Note: the GH CLI `gh issue create` does not reliably support an `--issue-type` flag in many environments — use the REST API to set the `type` field, or create then PATCH the issue.

```bash
# Preferred: create with `type` via REST API
gh api -X POST /repos/OWNER/REPO/issues -f title="New Feature" -f body="Details..." -f type="Feature 🧩"

# Or: create then PATCH to set type (safe for CLI scripts)
NUMBER=$(gh issue create --title "New Feature" --body "Details..." --json number -q .number)
gh api -X PATCH /repos/OWNER/REPO/issues/$NUMBER -f type="Feature 🧩"

# Fetch structured JSON for Node ID and Database ID (for linking/sub-issue operations)
gh issue view $NUMBER --json id,node_id,number,url
# Get the numeric databaseId for GraphQL/REST sub-issue APIs
gh api graphql -f query='query($id:ID!){node(id:$id){... on Issue{databaseId}}}' -F id="I_kwDOABC123"
```

### Checking for Issue Type Availability

Issue types may be enabled at the repo or organization level. Check repo-level first, then org-level; if none are available, do not emulate types using labels — omit the `type` parameter and proceed without it.

```bash
# Check repo-level then org-level; use REST to set 'type' if available
if gh api repos/OWNER/REPO/issue-types --jq ".[].name" 2>/dev/null; then
  echo "Repo issue types enabled"
elif gh api orgs/OWNER/issue-types --jq ".[].name" 2>/dev/null; then
  echo "Org issue types enabled"
else
  echo "Issue Types disabled; do not emulate via labels — omit the type parameter"
fi

# Example: set type via REST on create
gh api -X POST /repos/OWNER/REPO/issues -f title="New Feature" -f body="Details" -f type="Feature 🧩"

# Or set after create (safer when using `gh issue create`):
NUMBER=$(gh issue create --title "New Feature" --body "Details" --json number -q .number)
gh api -X PATCH /repos/OWNER/REPO/issues/$NUMBER -f type="Feature 🧩"
```
