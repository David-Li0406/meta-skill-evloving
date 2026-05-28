---
name: git-pr
description: Create a pull request with contextual title and description
argument-hint: [title] [body] [base] [--draft]
---

# Git PR

## Overview

Create a pull request using the GitHub CLI with a descriptive title and appropriately-sized description. The PR description is automatically scaled based on the scope and impact of the changes.

## Arguments

### Definitions

- **`[title]`** (optional): PR title. Auto-generated if not provided.
- **`[body]`** (optional): PR body/description. Auto-generated if not provided.
- **`[base]`** (optional): Target branch for the PR. Defaults to main/master.
- **`[--draft]`** (optional): Create as draft PR. Defaults to false.

### Values

\$ARGUMENTS

## Core Principles

- PR size dictates description length - small changes get small descriptions
- Title should clearly convey the primary change
- Description focuses on WHY and context, not WHAT (diff shows the what)
- Use `gh pr create` for PR creation
- Always include AI attribution at the end of the body

## Instructions

1. Verify current branch is not the base branch
2. Push current branch to remote if needed
3. Fetch the latest remote base branch: `git fetch origin <base>`
4. Run `git log origin/<base>..HEAD --oneline` to get commits in this PR
5. Run `git diff origin/<base>...HEAD --stat` to assess change scope
6. Determine PR size category:
   - **Trivial**: <10 lines, single file, style/typo fix
   - **Small**: <50 lines, focused change
   - **Medium**: 50-200 lines, feature or significant fix
   - **Large**: >200 lines, major feature or refactor
7. Construct PR content based on size:

   **Trivial/Small**: Brief description with attribution

   ```
   gh pr create --title "Fix typo in README" --body "Corrects spelling error

   🤖 Generated with [Claude Code](https://claude.com/product/claude-code)"
   ```

   **Medium/Large**: Structured description with attribution

   ```
   gh pr create --title "<title>" --body "## Summary
   <1-2 sentence overview>

   ## Details
   - <Key change 1 with context>
   - <Key change 2 with context>

   🤖 Generated with [Claude Code](https://claude.com/product/claude-code)"
   ```

8. Execute `gh pr create` with constructed content
9. Return JSON output with PR details

## Output Guidance

Return JSON with PR details:

```json
{
  "success": true,
  "pr_number": "{{pr_number}}",
  "url": "{{url}}",
  "title": "{{title}}",
  "base": "{{base}}",
  "head": "{{head}}",
  "draft": "{{draft}}"
}
```

<!--
Placeholders:
- {{pr_number}}: PR number assigned by GitHub
- {{url}}: Full URL to the PR
- {{title}}: PR title used
- {{base}}: Target branch (e.g., main)
- {{head}}: Source branch name
- {{draft}}: Boolean indicating if created as draft
-->
