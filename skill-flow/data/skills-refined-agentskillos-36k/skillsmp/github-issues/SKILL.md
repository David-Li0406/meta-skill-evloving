---
name: github-issues
description: manage the lifecycle of GitHub Issues, including creation, triage, milestones, search, and sub-issue hierarchy
license: Apache-2.0
metadata:
  author: staytuned
  version: "1.0"
  category: github
---

# GitHub Issues

## What is it?

This skill manages the **lifecycle of GitHub Issues**. It handles creation, triage (assignment), milestones, exploration (reading/searching), and hierarchy (sub-issues).

## Success Criteria

- Issues are created with appropriate titles and descriptive bodies.
- Milestones are used to group issues into actionable releases or sprints.
- `type` (Bug, Feature, Task) is correctly assigned when the feature is enabled.
- Sub-issues are linked using numeric parent numbers and either string Node IDs (MCP) or numeric Database IDs (REST).
- Search queries are specific to avoid hitting rate limits.

## Why use it?

- **Complete issue lifecycle management**: Handle creation, updates, assignment, and closure in one place
- **Advanced planning capabilities**: Use milestones, sub-issues, and dependencies for complex project tracking
- **Efficient triage**: Quickly assign issues, set types, and organize work
- **Powerful search and discovery**: Find relevant issues across repositories with targeted queries
- **AI-powered assistance**: Leverage Copilot assignment for automated issue resolution

## When to use this skill

- "Create a bug report for X."
- "What are the open issues assigned to me?"
- "Create a milestone for V1.0."
- "Add issue #42 to the 'Beta' milestone."
- "Break this task down into sub-issues."
- "Assign Copilot to fix issue #123."

## What this skill can do

- **Create/Update**: Open new issues, close completed ones, update descriptions following standard [issue templates](assets/ISSUE_TEMPLATE).
- **Planning**: Create and list milestones, assign issues to milestones.
- **Triage**: Assign users, Assign Copilot.
- **Explore**: Search specific issues, read comments, list issue types.
- **Hierarchy**: Create and manage sub-issues (tracking lists).
- **Dependencies**: explicit blocking relationships using REST API (see [DEPENDENCIES.md](references/DEPENDENCIES.md)).

## What this skill will NOT do

- Create Pull Requests (use `github-pr-flow`).
- Modify code (use `github-pr-flow`).
- Create repositories.

## How to use this skill

1. **Identify Intent**: Are we creating, reading, or modifying?
2. **Select Tool**: Use [MCP_TOOL_MAP](../github-kernel/references/MCP_TOOL_MAP.md).
3. **Execute**: Call the corresponding MCP tool function.

### Quick Example: Create a Bug Report

```javascript
// Create a bug report with proper structure
issue_write({
  method: "create",
  owner: "acme-corp",
  repo: "app",
  title: "Bug: Login fails on Safari",
  body: `## Description
Users cannot log in when using Safari 17.

## Steps to Reproduce
1. Open Safari 17
2. Navigate to login page
3. Enter credentials

## Expected Behavior
User should be logged in

## Actual Behavior
Login button does nothing`,
  type: "Bug"  // Set type if issue types are enabled
});
```

## Tool usage rules

- **Issue Structure**: Follow standard patterns from [issue templates](assets/ISSUE_TEMPLATE) when creating issues (Bug Report, Feature Request, Task/Chore). Prefer repository-specific templates when available.
- **Issue Type**: Attempt to specify a `type` (e.g., "Bug", "Feature", "Task") when creating issues if supported. Use `list_issue_types` to discover valid names. If listing types fails (404) or returns empty, issue types are not enabled — in that case, **do not attempt to emulate types using labels; omit the `type` parameter and proceed without it.**
  - **CLI note**: `gh issue create` often does not support a `--issue-type` flag; prefer setting `type` via the REST API (POST or PATCH with `-f type="..."`) or use MCP `issue_write` when available.
- **MCP First**: Use `issue_write`, `issue_read`, `search_issues`, `list_issue_types`.
- **Sub-issues**: Use `sub_issue_write` to link parent/child issues.
  - **MCP and REST API both require Database ID**: The `sub_issue_id` parameter requires the numeric **databaseId** (e.g., `12345678`), NOT the Node ID. You must convert the Node ID to Database ID using GraphQL first.
  - **Conversion Step** (required for both MCP and REST API): You can obtain a numeric **databaseId** from a Node ID via GraphQL, but the simplest method when you have an issue number or URL is to use `gh issue view` to retrieve `databaseId` directly.

    ```bash
    # Preferred: Get databaseId from issue number or URL
    gh issue view <ISSUE_NUMBER_OR_URL> --json databaseId -q .databaseId
    # Returns: 12345678

    # Alternative (when only Node ID available): convert Node ID -> databaseId via GraphQL
    gh api graphql -f query='query($id: ID!) { node(id: $id) { ... on Issue { databaseId } } }' -f id='<NODE_ID>' --jq '.data.node.databaseId'
    # Returns: 12345678
    ```

  - **MCP Example**:

    ```javascript
    sub_issue_write({
      owner: "OWNER",
      repo: "REPO",
      issue_number: 101,
      sub_issue_id: 12345678,  // Database ID (numeric)
      method: "add"
    });
    ```

  - **REST API (CLI) Example**:

    ```bash
    # Add as sub-issue using the parent number and child databaseId
    gh api repos/OWNER/REPO/issues/101/sub_issues -X POST -F sub_issue_id=12345678
    ```

  - **Edge Case - Duplicate Sub-Issues**:
    - **Check First**: Before adding a sub-issue, verify it's not already linked. For a robust check, use `issue_read` with `method: "get_sub_issues"`, which handles pagination. For a quick check of up to 100 items, you can use `gh issue view <parent> --json "subIssues(first:100){databaseId}"`.
    - **Error**: Attempting to add a duplicate sub-issue returns **HTTP 422** with message: "This issue is already a child of this issue"
    - **Why**: GitHub prevents adding the same issue as a sub-issue multiple times to the same parent.
    - **Solution**: Check existing sub-issues before adding new ones to avoid errors.

  - **Edge Case - Issue Already Has Parent**:
    - **Scenario**: Attempting to add an issue as a sub-issue when it's already a child of another parent.
    - **Error**: Returns **HTTP 422** with message: "Sub issue may only have one parent"
    - **Why**: Each issue can have at most ONE parent. GitHub prevents orphaning issues from their current parent.
    - **Solution**: Use the `replace_parent` parameter to move the issue to a new parent:

      ```javascript
      // MCP Example - Move issue from old parent to new parent
      sub_issue_write({
        owner: "OWNER",
        repo: "REPO",
        issue_number: 100,        // New parent
        sub_issue_id: 12345678,   // Child issue (Database ID)
        method: "add",
        replace_parent: true      // Allow parent replacement
      });
      ```

    - **Important**: Setting `replace_parent: true` will automatically remove the issue from its current parent and add it to the new parent.
- **Milestones**:
  - **Milestones**: Use `gh api` to list/create. Use `gh issue edit` (CLI) or `issue_write` (MCP) to assign.
  - **Discovery**: Use `gh api /repos/{owner}/{repo}/milestones` (via `run_command`) to list existing milestones and find their **number**.
  - **Creation**: Use `gh api -X POST /repos/{owner}/{repo}/milestones -f title="title"` to create new ones.
  - **Assignment**:
    - **MCP**: Use `issue_write` with the `milestone` parameter (integer).
    - **CLI**: Use `gh issue edit <number> --milestone "title"` for title-based assignment.
- **Issue Types**: Types are **CONDITIONAL**. Use `list_issue_types` to find valid types (e.g. "Bug 🐞"). You **MUST** use `issue_write` (MCP) with the `type` parameter (exact name) if types are available. If using `gh issue create` (CLI), note that `--issue-type` requires the exact type name. If the API returns a 404 for issue types, do not attempt to use them.
- **CLI Scripting Rule**: When using `gh issue create` in a script, it returns the issue URL string, not JSON. You must parse the URL to get the issue number, then call `gh issue view <number> --json id,number` to get the structured metadata for downstream tasks.
- **Reading Issues**: Use `issue_read` to retrieve issue details, comments, and sub-issues.
  - **Method Options**:
    - `get`: Get full issue details (default) - no pagination
    - `get_comments`: Retrieve all comments on an issue - **supports pagination**
    - `get_sub_issues`: List all sub-issues of a parent issue - **supports pagination**
  - **Parameters**: All methods require `owner`, `repo`, and `issue_number`
  - **Pagination**: Only `get_comments` and `get_sub_issues` support pagination. Use `page` and `perPage` parameters for large lists (default: 30 per page, max: 100)
  - **Example**:

    ```javascript
    // Read all comments on issue #42 with pagination
    issue_read({
      owner: "OWNER",
      repo: "REPO",
      issue_number: 42,
      method: "get_comments",
      page: 1,
      perPage: 100  // Get up to 100 comments per page
    });
    ```

- **Issue Dependencies**:
  - **Method**: Use `gh api` REST endpoints as described in [DEPENDENCIES.md](references/DEPENDENCIES.md).
  - **IDs**: Adding or removing dependencies requires the **database ID** (integer) of the blocking issue. Use `issue_read` to find the `id` field.
- **Copilot**: Use `assign_copilot_to_issue` to start an AI session on an issue.

## Examples

See [references/examples.md](references/examples.md) for compliant issue management examples.

For issue structure patterns (Bug Report, Feature Request, Task), refer to [assets/ISSUE_TEMPLATE](assets/ISSUE_TEMPLATE).

## Limitations

- Cannot see deleted issues.
- Rate limits apply to search queries.

## Troubleshooting

- **Sub-issue Linking Fails**: Ensure you are using the **Database ID** (numeric integer) for the child issue, not the Node ID or issue number, when calling `sub_issue_write`. Convert the Node ID to Database ID using the GraphQL query documented above.
- **Milestone Not Found**: Milestones must be referenced by their integer **number**, not their title, in API calls. Use `gh api` to list milestones and find the correct number.
- **Issue Type Errors**: If you receive a 404 when listing issue types, the feature is not enabled in the repository. Do not attempt to set issue types in that case.
