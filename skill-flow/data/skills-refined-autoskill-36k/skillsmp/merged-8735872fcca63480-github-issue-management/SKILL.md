---
name: github-issue-management
description: Use this skill to manage the lifecycle of GitHub Issues, including creation, triage, milestones, and duplicate detection.
---

# GitHub Issue Management

## What is it?

This skill manages the **lifecycle of GitHub Issues**. It handles creation, triage (assignment), milestones, exploration (reading/searching), and duplicate detection.

## Success Criteria

- Issues are created with appropriate titles and descriptive bodies.
- Milestones are used to group issues into actionable releases or sprints.
- `type` (Bug, Feature, Task) is correctly assigned when the feature is enabled.
- Duplicate issues are detected and managed effectively.
- Sub-issues are linked using numeric parent numbers and either string Node IDs (MCP) or numeric Database IDs (REST).
- Search queries are specific to avoid hitting rate limits.

## Why use it?

- **Complete issue lifecycle management**: Handle creation, updates, assignment, and closure in one place.
- **Advanced planning capabilities**: Use milestones, sub-issues, and dependencies for complex project tracking.
- **Efficient triage**: Quickly assign issues, set types, and organize work.
- **Powerful search and discovery**: Find relevant issues across repositories with targeted queries.
- **AI-powered assistance**: Leverage Copilot assignment for automated issue resolution.

## When to use this skill

- "Create a bug report for X."
- "What are the open issues assigned to me?"
- "Create a milestone for V1.0."
- "Add issue #42 to the 'Beta' milestone."
- "Break this task down into sub-issues."
- "Detect duplicates for issue #123."
- "Assign Copilot to fix issue #123."

## What this skill can do

- **Create/Update**: Open new issues, close completed ones, update descriptions following standard issue templates.
- **Planning**: Create and list milestones, assign issues to milestones.
- **Triage**: Assign users, assign Copilot, and label incoming issues.
- **Explore**: Search specific issues, read comments, list issue types.
- **Hierarchy**: Create and manage sub-issues (tracking lists).
- **Dependencies**: Manage explicit blocking relationships using REST API.
- **Duplicate Detection**: Identify and manage duplicate issues effectively.

## What this skill will NOT do

- Create Pull Requests (use `github-pr-flow`).
- Modify code (use `github-pr-flow`).
- Create repositories.

## How to use this skill

1. **Identify Intent**: Are we creating, reading, or modifying?
2. **Select Tool**: Use the appropriate tool for the action (e.g., MCP or REST API).
3. **Execute**: Call the corresponding function based on the identified intent.

### Quick Example: Create a Bug Report

```javascript
// Create a bug report with proper structure
issue_write({
  method: "create",
  owner: "<owner>",
  repo: "<repo>",
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

- **Issue Structure**: Follow standard patterns from issue templates when creating issues (Bug Report, Feature Request, Task/Chore).
- **Issue Type**: Attempt to specify a `type` (e.g., "Bug", "Feature", "Task") when creating issues if supported.
- **Sub-issues**: Use `sub_issue_write` to link parent/child issues.
- **Milestones**: Use API calls to list/create and assign milestones.
- **Reading Issues**: Use `issue_read` to retrieve issue details, comments, and sub-issues.
- **Duplicate Detection**: Implement checks to identify existing issues before creating new ones.

## Examples

Refer to the documentation for compliant issue management examples and issue structure patterns.

## Limitations

- Cannot see deleted issues.
- Rate limits apply to search queries.

## Troubleshooting

- **Sub-issue Linking Fails**: Ensure you are using the **Database ID** (numeric integer) for the child issue.
- **Milestone Not Found**: Milestones must be referenced by their integer **number** in API calls.
- **Issue Type Errors**: If you receive a 404 when listing issue types, the feature is not enabled in the repository.