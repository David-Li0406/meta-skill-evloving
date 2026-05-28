---
name: sync-plan-issue
description: Create or update GitHub issue with current plan summary. Lists open issues for selection or creates new. Triggers on "sync plan to github", "update issue with plan", "share plan", "create issue from plan". Use after planning is complete and ready to share publicly. Do NOT use when plan is still in draft/exploration phase, working on private/sensitive features (issues are public), or issue has manually curated description to preserve.
---

# Sync Plan to GitHub Issue

Update or create a GitHub issue with a structured plan summary based on Linear Method + Shape Up best practices.

## Prerequisites

- Active plan in conversation OR plan file in `.local/plans/` OR PRD in `.local/prds/wip/`
- GitHub CLI authenticated (`gh auth status`)
- Git repo with GitHub remote

## Workflow

### 1. Verify GitHub access

```bash
gh auth status
gh repo view --json nameWithOwner -q '.nameWithOwner'
```

If auth fails, stop and inform user.

### 2. Extract plan from context

Find the plan from (in order):

1. **Current conversation**: Look for recent output with plan structure (Problem/Solution/Tasks), explicit "Plan:" headers, or plan mode output
2. **Plan files**: Check `.local/plans/`
3. **PRD files**: Check `.local/prds/wip/`

If ambiguous, ask user to confirm which plan to sync.

Extract these elements:
- **Problem**: What's broken/missing and why it matters
- **Appetite**: Time/scope constraint
- **Solution**: High-level approach
- **Scope**: Files/components affected
- **Tasks**: Ordered steps
- **Rabbit holes**: Known risks (optional)
- **No-gos**: Explicit exclusions (optional)

### 3. List open issues

```bash
gh issue list --state open --limit 20 --json number,title,labels
```

Parse output and present as options using `AskUserQuestion`:
- `#123: Issue title`
- `#456: Another issue`
- `Create new issue`

### 4. Get user selection

Use `AskUserQuestion`:
- Header: "Target issue"
- Options: parsed issues + "Create new"
- If "Create new", ask for title in follow-up question

### 5. Format plan summary

Apply template from `references/plan-template.md`. Required sections:
- Problem, Appetite, Solution
- Scope table, Tasks checklist
- Synced timestamp footer

Optional sections (include when relevant):
- Rabbit Holes, No-Gos

### 6. Update or create issue

**Update existing**:
```bash
# Get current body
body=$(gh issue view "$issue_number" --json body -q '.body')

# If body contains "## Plan Summary", replace that section
# Otherwise append with --- separator

gh issue edit "$issue_number" --body "$updated_body"
```

**Create new**:
```bash
gh issue create --title "$title" --body "$formatted_plan"
```

### 7. Confirm

Output:
- Issue URL
- What was updated/created

## Template Rules (from Linear + Shape Up)

**Problem first**: Without a problem, can't judge if solution is good. State what's broken/painful, not just what you're building.

**Appetite constrains scope**: How much time is this worth? Prevents gold-plating.

**Plain language tasks**: No user stories. Verb + object. Concrete deliverables.

**Explicit no-gos**: What you're NOT doing. Prevents scope creep.

**Rabbit holes**: Known risks, temptations that could derail. Call them out.

## Error Handling

| Error | Action |
|-------|--------|
| No plan found | Ask user to describe plan or point to file |
| Auth failed | `gh auth login` instructions |
| Issue not found | Re-list issues, ask again |
| Body too long | Truncate tasks, summarize scope |

## Reference Files

- `references/plan-template.md` - Full template with guidelines, good/bad examples
