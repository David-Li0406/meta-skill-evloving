# Workflow

## Step 1: Invocation

The skill is typically invoked via handoff from sdd-update after spec completion:

```
Skill(foundry:foundry-pr) "Create PR for spec my-feature-2025-11-03-001"
```

## Step 2: Context Gathering

The skill gathers context from multiple sources:

**Spec Metadata**
```json
{
  "title": "Add user authentication",
  "description": "Implement OAuth 2.0 authentication...",
  "objectives": ["Support GitHub and Google OAuth providers", ...]
}
```

**Completed Tasks**
- File paths modified
- Changes made in each file
- Task completion status

**Commit History**
- Commit messages and SHAs
- Task associations
- Development progression

**Journal Entries**
- Technical decisions
- Implementation notes
- Challenges overcome

**Git Diff**
- Actual code changes
- File-level summary if diff is large

## Step 3: AI Analysis

The agent analyzes all gathered context to:
- Understand the feature's purpose and scope
- Identify key changes and their impact
- Extract important decisions from journals
- Synthesize technical details from diffs

## Step 4: Draft Generation

The agent generates a comprehensive PR description following best practices (see `references/template.md`).

## Step 5: User Review

The agent shows the draft and asks for user approval:

```
Agent: "Here's the PR description I've generated:

[shows full PR with title and body]

Would you like me to create this PR, or would you like me to revise it?"
```

## Step 6: PR Creation

Once approved, the skill calls the MCP tool `mcp__plugin_foundry_foundry-mcp__pr action="create"`, which gathers spec context, journals, git diffs, and generates the PR description automatically (or performs a dry-run preview when requested).

The skill then:
1. Pushes the branch to the remote (if needed)
2. Calls the GitHub CLI via the PR workflow (no additional confirmation)
3. Updates spec metadata with the PR URL and number
