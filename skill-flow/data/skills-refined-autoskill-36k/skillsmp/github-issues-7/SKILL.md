---
name: github-issues
description: Create and organize GitHub issues effectively. Use when creating issues, drafting issue descriptions, organizing work into batches/epics, using issue types (Task, Batch, Bug, Epic), working with sub-issues, or planning project work breakdown. Covers issue formatting, avoiding repetition, proper sections, and GitHub API usage for issue types and sub-issues.
---

# GitHub Issues

## Issue Description Format

Keep issues concise. The default structure has two sections:

```markdown
Depends on #123

### Description

[Context, problem statement, relevant code links, clarifications in flowing prose]

### Acceptance Criteria

[Clear definition of done]
```

If an issue depends on another, add `Depends on #123` at the very top, above the description.

### Writing Style

Write in prose paragraphs, not bullet lists. Embed references as inline links within the text rather than listing them in a separate section. See the [evidence-based-responses](../evidence-based-responses/SKILL.md) skill for guidance on linking to evidence.

Avoid repetition. Say things once. If context is provided in the description, don't repeat it elsewhere.

Implementation details, when included, are suggestions rather than requirements. The developer who picks up the issue may implement it differently. Frame suggestions with language like "One approach would be..." or "Consider..."

Use proper GitHub markdown formatting. See the [markdown-output](../markdown-output/SKILL.md) skill for collapsible sections, code blocks, and alerts.

### Additional Sections

Add these only when genuinely needed:

- **Out of Scope**: When there's likely confusion about issue boundaries
- **Background**: Only if context is complex enough to warrant separation from description

Omit sections that would be empty. Never include "N/A" or "None" placeholders.

### Bad Patterns

- Repeating information across multiple sections
- Empty sections or "N/A" placeholders
- Prefixes like `WI-#` in issue titles
- Implementation details presented as hard requirements
- References listed separately instead of linked inline

## Issue Types

GitHub supports issue types to categorize work. Common types:

| Type | Purpose |
|------|---------|
| Task | A specific piece of work |
| Batch | A group of related tasks |
| Epic | A group of batches (larger initiative) |
| Bug | An unexpected problem or behavior |

Issue type IDs are repository-specific. Query the repository's available types before creating issues. See [references/api-reference.md](references/api-reference.md) for the GraphQL query.

The `gh issue create` CLI does not support setting issue types directly. Use the GraphQL API to create issues with a type, or create via CLI then update the type via GraphQL.

## Sub-Issues

Prefer sub-issues over listing tasks in the issue description body. Sub-issues provide:

- Progress tracking (completed count)
- Individual assignment and status
- Proper linking in GitHub's UI

Workflow:

1. Create the parent issue (Epic or Batch) first
2. Create child issues
3. Link children as sub-issues via the API

See [references/api-reference.md](references/api-reference.md) for REST and GraphQL examples.

## Before Creating Issues

Clarify with the user:

- Desired granularity (how big should each task be?)
- Whether to include implementation suggestions or keep issues high-level
- Which issue types are available in the target repository
