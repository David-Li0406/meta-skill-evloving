---
name: audit
description: Review AI-drafted issues for human approval
argument-hint: [issue-number] (optional)
allowed-tools: Bash, AskUserQuestion, Read, Grep, Glob
disable-model-invocation: true
agent: audit-agent
---

# Issue Audit Command

This command helps review issues labeled `ai-drafted` and either approve them for implementation or request changes.

## Dynamic Context

**Current AI-drafted issues:**
!`gh issue list --label ai-drafted --json number,title --limit 10 2>/dev/null || echo "Could not fetch issues"`

## Context

Issues with `ai-drafted` label were groomed by the `/groom` command. They have:

- Expanded Description
- Acceptance Criteria
- Out of Scope

But the AI's decisions haven't been verified by a human yet.

## Arguments

**Issue number:** $ARGUMENTS

## Instructions

### Step 1: Fetch Issues

If an issue number was provided above (not empty):

- Skip to Step 2 with that issue number

If no issue number was provided:

1. Fetch issues with `ai-drafted` label:

    ```bash
    gh issue list --label ai-drafted --json number,title --limit 20
    ```

2. If no issues found, inform the user and exit.

3. Use AskUserQuestion to let the user select which issues to audit (set multiSelect: true)

### Step 2: Review Each Issue

For each selected issue:

1. **Fetch full issue details:**

    ```bash
    gh issue view <number> --json number,title,body,labels
    ```

2. **Present the issue content** clearly formatted:
    - Title
    - Description
    - Acceptance Criteria
    - Out of Scope
    - Any other sections

3. **Optionally research context** if user asks:
    - Use Grep/Glob/Read to verify technical details
    - Check if acceptance criteria are realistic
    - Verify scope boundaries make sense

4. **Use the review checklist** from `.claude/skills/audit/templates/review-criteria.md`:
    - Description quality
    - Acceptance criteria testability
    - Out of scope clarity
    - Technical accuracy
    - Completeness

5. **Use AskUserQuestion for a verdict** with these options (in this order):
    - **Approve**: Remove `ai-drafted` label, issue is ready for implementation
    - **Approve with edits**: Make minor changes, then remove `ai-drafted`
    - **Send back for re-grooming**: Move back to `needs-details`, remove `ready` and `ai-drafted`
    - **Skip**: Review later, no changes

### Step 3: Apply Updates

Based on user's verdict:

**Approve:**

```bash
gh issue edit <number> --remove-label ai-drafted
```

**Approve with edits:**

- Ask user what changes to make
- Update issue body: `gh issue edit <number> --body "<updated body>"`
- Remove label: `gh issue edit <number> --remove-label ai-drafted`

**Send back for re-grooming:**

```bash
gh issue edit <number> --remove-label ai-drafted --remove-label ready --add-label needs-details
```

Optionally add a comment explaining what needs to change:

```bash
gh issue comment <number> --body "Sent back for re-grooming: <reason>"
```

**Skip:**

- No changes, move to next issue

### Step 4: Summary

After all issues are processed, provide a summary:

- Number of issues approved
- Number sent back for re-grooming
- Number skipped
- Links to updated issues

## Notes

- This is a lighter-weight review than `/groom` - no subagents needed
- Focus on verifying the AI's decisions were sound
- Check that acceptance criteria are testable and complete
- Verify out-of-scope items make sense
- If something looks wrong, ask clarifying questions before deciding
