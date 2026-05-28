---
name: github-projects
description: manage GitHub Projects (V2), including board organization, fields, and item tracking
metadata:
  category: github
---

# GitHub Projects (V2)

## What is it?

This skill enables agents to interact with **GitHub Projects (V2)** boards. It covers the management of projects, custom fields (Status, Priority, Iterations), and items (Issues, Pull Requests, and Drafts).

## Success Criteria

- Project, Field, and Item IDs are resolved dynamically before modifications.
- Items are correctly added to the target project.
- Field updates (especially single-select options like Status) use valid option IDs.
- Draft issues are used for placeholders when a full issue is not yet needed.

## Why use it?

- **Visual project management**: Organize work on GitHub Projects V2 boards
- **Custom field management**: Handle Status, Priority, Iterations, and custom properties
- **Dynamic workflows**: Automatically move items across board columns
- **Comprehensive tracking**: Manage Issues, PRs, and draft items in one place
- **Cross-repository planning**: Link and organize work from multiple repositories

## When to use this skill

- "Add this issue to the 'Q4 Roadmap' project."
- "Move PR #50 to the 'In Review' status on the board."
- "Create a new project for this organization."
- "Update the 'Priority' of this project item to 'High'."
- "List the items in project #1."

## What this skill can do

- **Project Management**: List, Create, Edit, and Delete projects for an owner (user or org).
- **Field Discovery**: List fields in a project and their available options (for selects).
- **Item Management**: Add Issues/PRs, Create Drafts, Edit fields, Archive, or Delete items.
- **Linking**: Link projects to repositories or teams.

## What this skill will NOT do

- Manage Projects (Classic) - this skill is for V2 only.
- Configure project-level automation rules beyond field updates.
- Manage repo-level labels (use `github-issues`).

## How to use this skill

1. **Discovery**: Always start by listing projects (`gh project list --owner <login>`) to find the `project-id`.
2. **Field Mapping**: Use `gh project field-list` to find the `field-id` and available `option-id`s for single-select fields.
3. **Item Operations**:
    - To add: `gh project item-add`.
    - To update: `gh project item-edit` using the specific IDs found during discovery.

## Tool usage rules

- **Statelessness**: NEVER hardcode IDs. Project IDs and Field IDs can vary across organizations and projects.
- **CLI First**: Use the `gh project` commands as they are optimized for V2.
- **GraphQL Fallback**: For complex filtering or bulk operations not supported by the CLI, use `gh api graphql` (see [references/GRAPHQL_FALLBACK.md](references/GRAPHQL_FALLBACK.md)).
- **Identifiers**:
  - `project-id` is usually a string (e.g., `PVT_...`).
  - `field-id` and `item-id` are also unique global identifiers.

## Examples

See [references/examples.md](references/examples.md) for concrete CLI and API examples.

## Limitations

- `gh project item-edit` only supports updating a single field per invocation for non-draft items.
- Token must have the `project` scope.
- Draft issues cannot be converted to full issues via this skill (requires `issue_write` + `item-add`).
