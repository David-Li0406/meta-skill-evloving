---
name: github-pr-create
description: Create a GitHub pull request with AI-generated title and description based on the diff
---

# GitHub Pull Request Skill

Creates a draft pull request with a comprehensive title and description generated from the diff between the current branch and the base branch. Includes rich content like examples and diagrams where appropriate.

## Workflow

### 1. Determine Base Branch

Get the default branch and check for ancestor branches:

```bash
git symbolic-ref refs/remotes/origin/HEAD --short | sed 's|origin/||'
```

If there's an ancestor branch that isn't the default branch, ask the user which to use as the base.

### 2. Verify Changes Exist

Get the diff between base branch and HEAD:

```bash
git log --patch {base_branch}..HEAD
```

If no changes are detected, inform the user and stop.

### 3. Gather Issue Context (Optional)

If the user provides an issue number or URL earlier in the conversation or now:

```bash
gh issue view {issue_number} --json url,number,title,body,comments
```

The issue's title, body, and comments contain the reasoning and motivation for the change. This context must be incorporated into the PR's "Why" section to echo the problem being solved.

### 4. Analyze the Diff

Examine the diff to identify what rich content would help reviewers:

| Change Type | Rich Content to Include |
|-------------|------------------------|
| HTTP endpoints, REST APIs, RPC methods | Request/response examples |
| Library/SDK public API changes | Before/after code examples |
| Architectural changes (new components, changed data flow) | Mermaid diagram |
| Test file changes | Brief test coverage summary |

### 5. Generate PR Content

**Title:**
- Max 50 characters
- Start with a capital letter
- No trailing period
- Use imperative mood (Add, Fix, Update, not Adds, Fixes, Updates)

**What section:**
- Describe what has changed
- Use imperative mood
- Be direct, eliminate filler words

**Why section:**
- Describe why the change is being made
- If linked to an issue, echo the reasoning from the issue (the problem, motivation, or request)
- Be concise, avoid generic statements
- Think like a journalist

**Examples section (when applicable):**

For API changes, include request/response examples:
```
### Example

**Request:**
POST /api/resource
Content-Type: application/json

{
  "field": "value"
}

**Response:**
HTTP 201 Created

{
  "id": "abc123",
  "field": "value"
}
```

For library/SDK changes, show usage:
```
### Example

// Before
let result = old_function(arg);

// After
let result = new_function(arg, options)?;
```

**Diagram section (when applicable):**

For architectural changes, include a Mermaid diagram:
```
### Architecture

flowchart LR
    A[Component A] --> B[New Component]
    B --> C[Dependency]

    style B fill:#ccffcc,stroke:#00ff00
```

Use green (#ccffcc) for added components, red (#ffcccc) for removed.

### 6. Present Draft for Review

Present the generated content:

```
## Pull Request Draft

**Base branch:** {base_branch}

### Title
{title}

### What
{what}

### Why
{why}

{examples_section_if_applicable}

{diagram_section_if_applicable}

Would you like me to create the PR with this content, or would you like to make changes?
```

Wait for user confirmation before proceeding.

### 7. Get Reviewers

Fetch potential reviewers:

```bash
gh api '/repos/{owner}/{repo}/contributors' --jq '.[].login'
```

For organizations, also fetch teams:

```bash
gh api '/orgs/{owner}/teams' --jq '.[] | "{owner}/" + .slug'
```

Ask the user to select reviewers.

### 8. Create the Pull Request

After user confirmation:

```bash
gh pr create \
  --draft \
  --base "{base_branch}" \
  --title "{title}" \
  --body "{full_body}" \
  --reviewer "{reviewers}"
```

The body should include:
- `### What` section
- `### Why` section
- `### Example` section (if applicable)
- `### Architecture` section with Mermaid diagram (if applicable)
- `Close #{issue_number}` (if linked to an issue)

### 9. Request Copilot Review

```bash
gh pr edit --add-reviewer 'copilot-pull-request-reviewer[bot]'
```

### 10. Report Result

Output the created PR URL.
