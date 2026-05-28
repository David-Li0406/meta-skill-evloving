---
name: github-issue-creator
description: Create focused GitHub issues that serve as summaries for work. Issues describe the user goal and link to branch plans for implementation details. One issue per meaningful unit of work - avoid splitting into many small issues.
---

# GitHub Issue Creator

Create focused, user-centric GitHub issues that serve as high-level summaries. Implementation details belong in branch plans (PLAN.md), not fragmented across multiple issues.

## Philosophy

**Issues are for tracking and communication, not for decomposition.**

- **One issue = one meaningful outcome** from the user's perspective
- **Branch plans contain the implementation details** - issues just link to them
- **Engineers hate tracking 10 issues** for what should be one coherent piece of work
- **Focus on the "what" and "why"** - the "how" lives in the branch plan

## Trigger

When user asks to:
- Create a new issue or user story
- Report a bug
- Plan a feature (create issue + branch plan)

## Prerequisites

Requires GitHub CLI (`gh`) authenticated with project scope:

```bash
gh auth refresh -s project
gh auth status  # Should show 'project' in Token scopes
```

## Project Board

Issues are added to the **Viya Project Board**:
- **Organization**: ShipitSmarter
- **Project Number**: 10
- **URL**: https://github.com/orgs/ShipitSmarter/projects/10

## Process

### Step 1: Understand the Work

Ask the user:
1. **What's the user-visible outcome?** (not the technical tasks)
2. **Who benefits and how?** (the "so that" part)
3. **Is this one thing or multiple unrelated things?**

**Key question**: Can this be described in one sentence that a product manager would understand?

- "Users can export reports to PDF" ✓ (one issue)
- "Refactor auth + add PDF export + fix sidebar" ✗ (split into separate issues)

### Step 2: Determine Issue Type

| Type | When to Use | Keep it to ONE issue if... |
|------|-------------|---------------------------|
| **Bug** | Something broken | It's one bug, even if fix touches multiple files |
| **Feature** | New capability | It's one user-facing capability |
| **Task** | Technical work | It's one coherent technical goal |

**Do NOT split a feature into:**
- ❌ "Add button", "Add API endpoint", "Add database field", "Add tests"
- ✅ ONE issue: "Feature: Export reports to PDF"

### Step 3: Select Repository

| Repository | Purpose |
|------------|---------|
| `ShipitSmarter/viya-app` | Frontend Vue.js application |
| `ShipitSmarter/shipping` | Backend shipping microservice |
| `ShipitSmarter/stitch` | Integration engine |
| `ShipitSmarter/viya-core` | Shared core libraries |
| `ShipitSmarter/hooks` | Webhooks & scheduler service |
| `ShipitSmarter/rates` | Rate management |
| `ShipitSmarter/ftp` | SFTP functionality |
| `ShipitSmarter/authorizing` | Authorization service |
| `ShipitSmarter/stitch-integrations` | Carrier integrations |

### Step 4: Write the Issue

**Keep it focused on outcomes, not tasks:**

#### For Features

```markdown
## Summary

<1-2 sentences: what capability are we adding and why it matters>

## User Story

**As a** <role>,
**I want** <capability>,
**So that** <benefit>.

## Scope

<What's included and what's explicitly NOT included>

## Acceptance Criteria

- [ ] <User-visible outcome 1>
- [ ] <User-visible outcome 2>
- [ ] <User-visible outcome 3>

## Implementation

See branch plan: `docs/PLAN.md` in feature branch (or link when available)

## Notes

<Any context, constraints, or references - keep brief>
```

#### For Bugs

```markdown
## Problem

<What's broken, from user perspective>

## Steps to Reproduce

1. <step>
2. <step>
3. <step>

## Expected vs Actual

- **Expected**: <what should happen>
- **Actual**: <what happens instead>

## Environment

- URL: <if applicable>
- User/Tenant: <if relevant>

## Screenshots

<if helpful>
```

#### For Tasks

```markdown
## Goal

<What we're trying to achieve and why>

## Scope

<What's included>

## Done When

- [ ] <Outcome 1>
- [ ] <Outcome 2>

## Implementation

See branch plan: `docs/PLAN.md` in feature branch (or link when available)
```

### Step 5: Preview and Confirm

Show the user:

```
## Preview

**Repository:** ShipitSmarter/<repo>
**Title:** <title>
**Labels:** <labels>

---
<formatted body>
---

Create this issue? (yes/no/edit)
```

### Step 6: Create Issue

```bash
gh issue create \
  --repo ShipitSmarter/<repo> \
  --title "<title>" \
  --label "<labels>" \
  --body "<body>"
```

### Step 7: Add to Project Board

```bash
gh project item-add 10 --owner ShipitSmarter --url <issue-url>
```

## Branch Plans

When creating a feature issue, suggest creating a branch with a PLAN.md:

```bash
git checkout -b feature/<issue-number>-<short-name>
```

The PLAN.md in the branch should contain:
- Technical approach
- Files to modify
- Step-by-step implementation tasks
- Testing strategy

**This keeps the issue clean and focused while giving engineers detailed guidance in the branch itself.**

## Anti-Patterns to Avoid

### ❌ Don't Create Multiple Issues For One Feature

Bad:
- Issue 1: "Add export button to reports page"
- Issue 2: "Create PDF generation service"
- Issue 3: "Add export API endpoint"
- Issue 4: "Write tests for PDF export"

Good:
- ONE Issue: "Feature: Export reports to PDF"
- Branch PLAN.md contains all implementation steps

### ❌ Don't Put Implementation Details in Issues

Bad:
```markdown
## Tasks
- [ ] Create ExportService class in /services
- [ ] Add POST /api/exports endpoint
- [ ] Install pdfkit dependency
- [ ] Add ExportButton.vue component
```

Good:
```markdown
## Acceptance Criteria
- [ ] User can export any report as PDF
- [ ] Exported PDF matches screen layout
- [ ] Works for reports with up to 1000 rows
```

### ❌ Don't Create Issues for Every Subtask

If you're tempted to create 5+ issues for one feature, stop and ask:
- Is this really multiple features?
- Or is this one feature that needs a branch plan?

## Labels

| Type | Labels |
|------|--------|
| Bug | `bug` |
| Feature | `enhancement` |
| Task | (none by default) |

## Error Handling

**Repository access issues:**
- List available repositories with `gh repo list ShipitSmarter`

**Missing project scope:**
- Create issue, inform user to run `gh auth refresh -s project`

## Output

After creating:
1. Confirm with issue number and URL
2. Confirm added to project board
3. Suggest: "Create a feature branch and add a PLAN.md for implementation details"
