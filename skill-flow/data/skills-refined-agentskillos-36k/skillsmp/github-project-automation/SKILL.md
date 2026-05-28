---
name: github-project-automation
description: |
  Automate GitHub Projects v2 planning from codebase analysis. Use when:
  (1) Need to create comprehensive project board with epics and user stories,
  (2) Converting codebase analysis into GitHub issues, (3) Bulk issue creation
  with labels and status synchronization, (4) Setting up kanban board with proper
  organization. Handles GitHub CLI authentication, GraphQL API for status updates,
  rate limiting, and project-issue linking.
author: Claude Code
version: 1.0.0
date: 2026-01-21
---

# GitHub Projects v2 Automation from Codebase Analysis

## Problem
Creating a comprehensive GitHub project plan manually is tedious and error-prone when you have 50+ user stories across multiple epics. Need to:
- Analyze codebase to identify features and completion status
- Create dozens of issues with proper labels
- Organize them in GitHub Projects v2
- Sync status fields based on labels
- Set up kanban views

Manual creation would take hours and miss features.

## Context / Trigger Conditions
Use this skill when:
- User asks to "build project plan from codebase"
- Need to create 30+ issues organized by epic/status
- Converting codebase analysis into GitHub project structure
- Setting up new GitHub Projects v2 board with bulk data
- Auditing existing codebase for feature completeness

**Symptoms:**
- Empty GitHub project that needs population
- Codebase with unclear feature status
- Need for comprehensive roadmap documentation

## Solution

### Phase 1: Authentication Setup

**Required GitHub CLI scopes:** `project`, `repo`

```bash
# Check current scopes
gh auth status

# Refresh with project scope (critical - NOT write:project)
gh auth refresh -h github.com -s project,repo
```

**Common Error:**
- `The scopes requested are invalid: write:project`
- **Solution:** Use `project` scope (not `write:project` or `read:project`)

### Phase 2: Codebase Analysis

Use the Task tool with `subagent_type=Explore` for comprehensive analysis:

```markdown
Analyze the codebase to identify:
1. Implemented features (code + basic functionality)
2. Partially implemented features
3. Database models and relationships
4. Core user workflows
5. Admin functionality
6. Infrastructure (testing, deployment)

Assess completion: code exists AND basic functionality works
Provide structured breakdown by domain/epic
```

**Key areas to analyze:**
- Routes (all route groups in Next.js/similar)
- Server actions or API endpoints
- Database schema
- UI components
- Test coverage

### Phase 3: Label Creation

Create epic and status labels first:

```bash
# Epic labels (blue: 0052CC)
gh label create "epic:authentication" --description "Epic description" --color "0052CC" --force
gh label create "epic:onboarding" --description "Epic description" --color "0052CC" --force
# ... repeat for all epics

# Status labels (traffic light colors)
gh label create "status:done" --description "Fully implemented" --color "0E8A16" --force
gh label create "status:in-progress" --description "Partially implemented" --color "FBCA04" --force
gh label create "status:backlog" --description "Not implemented" --color "D93F0B" --force

# Priority labels
gh label create "priority:critical" --description "Critical for MVP" --color "B60205" --force
gh label create "priority:high" --description "High priority" --color "D93F0B" --force
gh label create "priority:medium" --description "Medium priority" --color "FBCA04" --force
gh label create "priority:low" --description "Low priority" --color "0E8A16" --force

# Type labels
gh label create "type:feature" --description "New feature" --color "A2EEEF" --force
```

### Phase 4: Bulk Issue Creation

**Structure issues in JSON:**

```json
[
  {
    "epic": "epic:authentication",
    "status": "status:done",
    "priority": "priority:critical",
    "issues": [
      {
        "title": "User story title",
        "body": "**User Story:** As a...\n\n**Acceptance Criteria:**\n- [ ] ...\n\n**Status:** ✅ Implemented\n- Details"
      }
    ]
  }
]
```

**Python script for creation:**

```python
#!/usr/bin/env python3
import json
import subprocess
import time

def create_issue(title, body, labels):
    label_args = []
    for label in labels:
        label_args.extend(["-l", label])

    cmd = ["gh", "issue", "create", "--title", title, "--body", body] + label_args
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()  # Returns issue URL

# Rate limiting: 0.3-0.5s between requests
time.sleep(0.5)
```

**Rate limiting best practices:**
- 0.3-0.5 seconds between issue creations
- 0.3 seconds for project operations
- Monitor for rate limit errors and back off

### Phase 5: Add Issues to Project

**Get project ID:**

```bash
gh project list --owner USERNAME
# Returns: NUMBER  TITLE  STATUS  ID
```

**Add issues to project:**

```bash
# By project number and issue URL
gh project item-add PROJECT_NUMBER --owner OWNER \
  --url "https://github.com/OWNER/REPO/issues/ISSUE_NUMBER"
```

**Bash script for bulk addition:**

```bash
#!/bin/bash
PROJECT_NUM=4
OWNER="username"
REPO="reponame"

for issue_number in {64..151}; do
  gh project item-add $PROJECT_NUM --owner "$OWNER" \
    --url "https://github.com/$OWNER/$REPO/issues/$issue_number"
  sleep 0.3
done
```

### Phase 6: Status Field Synchronization

**Get status field IDs via GraphQL:**

```bash
gh api graphql -f query='
  query {
    node(id: "PROJECT_ID") {
      ... on ProjectV2 {
        fields(first: 20) {
          nodes {
            ... on ProjectV2SingleSelectField {
              id
              name
              options {
                id
                name
              }
            }
          }
        }
      }
    }
  }
' | jq '.data.node.fields.nodes[] | select(.name == "Status")'
```

**Update issue status via GraphQL:**

```python
def get_project_item_id(issue_number, project_number, owner):
    """Get project item ID (different from issue ID!)"""
    query = f'''query={{
      repository(owner: "{owner}", name: "repo") {{
        issue(number: {issue_number}) {{
          projectItems(first: 10) {{
            nodes {{
              id
              project {{ number }}
            }}
          }}
        }}
      }}
    }}'''

    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)

    for item in data["data"]["repository"]["issue"]["projectItems"]["nodes"]:
        if item["project"]["number"] == project_number:
            return item["id"]
    return None

def update_status(item_id, project_id, field_id, option_id):
    """Update status field using GraphQL mutation"""
    mutation = f'''
    mutation {{
      updateProjectV2ItemFieldValue(
        input: {{
          projectId: "{project_id}"
          itemId: "{item_id}"
          fieldId: "{field_id}"
          value: {{ singleSelectOptionId: "{option_id}" }}
        }}
      ) {{
        projectV2Item {{ id }}
      }}
    }}
    '''

    cmd = ["gh", "api", "graphql", "-f", f"query={mutation}"]
    subprocess.run(cmd, capture_output=True, text=True, check=True)
```

**Label-to-status mapping:**

```python
# Map issue labels to project status
LABEL_TO_STATUS = {
    "status:backlog": "TODO_OPTION_ID",
    "status:in-progress": "IN_PROGRESS_OPTION_ID",
    "status:done": "DONE_OPTION_ID",
}

# Get labels from issue
labels = get_issue_labels(issue_number)
status_label = next((l for l in labels if l in LABEL_TO_STATUS), None)
option_id = LABEL_TO_STATUS[status_label]
```

### Phase 7: Documentation

Create `docs/PROJECT_STATUS.md` with:
- Project statistics (total, done, in-progress, backlog)
- Epic-by-epic breakdown with completion percentages
- Critical blockers and gaps
- Feature status table
- Recommended sprints/roadmap
- Technical debt tracker

## Verification

Successful automation produces:
- ✅ All issues created (0 failures)
- ✅ All issues added to project
- ✅ Status fields synchronized with labels
- ✅ Project board viewable with organized kanban
- ✅ Documentation generated

**Check:**
```bash
gh project view PROJECT_NUMBER --owner OWNER
# Should show: Item count: [expected number]

gh issue list --label "epic:authentication" --json number,title,labels
# Verify labels applied correctly
```

## Example

**Full workflow for 88 issues across 11 epics:**

```bash
# 1. Authenticate
gh auth refresh -h github.com -s project,repo

# 2. Create labels (epics, statuses, priorities)
./create_labels.sh  # 25 labels created

# 3. Analyze codebase
# (Use Task tool with Explore agent)

# 4. Generate issues JSON
# (Structure 88 user stories in JSON format)

# 5. Create issues
python3 create_issues.py
# Output: 88/88 created successfully

# 6. Add to project
./add_to_project.sh
# Output: 88/88 added successfully

# 7. Sync status fields
python3 update_status.py
# Output: 88/88 updated successfully

# 8. Generate documentation
# Create docs/PROJECT_STATUS.md
```

**Result:** 48% complete (42 done, 11 in-progress, 35 backlog)

## Notes

### API Differences: gh CLI vs GraphQL

- **gh CLI:** Best for issue creation, label management, project listing
- **GraphQL:** Required for status field updates, complex queries
- **Hybrid approach:** Use both for full automation

### Project Item IDs vs Issue IDs

**Critical distinction:**
- Issue has an ID (e.g., `I_kwDOABC...`)
- Project item has a different ID (e.g., `PVTI_lAHO...`)
- Must query project items to get item ID for status updates

### Rate Limiting Strategy

- **Creation:** 0.5s between issues
- **Project ops:** 0.3s between additions
- **Status updates:** 0.3s between mutations
- **Total time:** ~1-2 minutes for 88 issues

### Built-in Project Workflows

Consider using GitHub's built-in automations:
- Auto-archive completed items
- Auto-add new issues from repo
- Status sync on PR/issue state changes

### Label Color Conventions

- **Epics:** Blue (0052CC) - consistent grouping
- **Status:** Traffic light (green=done, yellow=in-progress, red=backlog)
- **Priority:** Severity scale (red=critical → green=low)
- **Type:** Semantic colors (blue=feature, red=bug, etc.)

### Codebase Analysis Criteria

**"Done" means:**
- ✅ Code exists in codebase
- ✅ Basic functionality works
- ❌ NOT just code presence
- ❌ NOT requiring tests/docs

**"In Progress" means:**
- ⚠️ Code exists but incomplete
- ⚠️ Marked as TODO in comments
- ⚠️ Infrastructure exists but UI missing

### Common Errors

**1. Authentication scope error:**
```
error: your authentication token is missing required scopes [read:project]
```
**Solution:** Use `project` scope (not `read:project` or `write:project`)

**2. Project item not found:**
```
Issue not found in project
```
**Solution:** Ensure issue was added to project first, then get item ID

**3. Invalid option ID:**
```
Field value is not valid
```
**Solution:** Query status field to get correct option IDs

---

# MODE 2: AUTONOMOUS ISSUE IMPLEMENTATION

## Problem
After creating project plan, developers still manually implement each issue - taking 2-4 hours per medium-complexity feature.

## Context / Trigger Conditions
Use this mode when:
- User says "work on #104" or "implement #104"
- User says "work on next critical issue"
- User says "work on next payment issue" (epic-filtered)
- Ready to autonomously implement specific GitHub issues

## Solution

### Phase 1: Issue Selection

**Specific issue:**
```bash
python3 scripts/implement_issue.py 104
```

**Auto-select by priority:**
```bash
# Next critical issue
python3 scripts/implement_issue.py --auto-select --priority critical

# Next critical payment issue
python3 scripts/implement_issue.py --auto-select --priority critical --epic booking-payment

# Next issue (any priority, tries critical → high → medium → low)
python3 scripts/implement_issue.py --auto-select
```

**Manual fetching:**
```bash
# Fetch issue details only
python3 scripts/fetch_issue.py 104

# Auto-select without implementing
python3 scripts/select_issue.py --priority critical --epic payment
```

### Phase 2: Context Analysis

After selecting issue, use Task tool with Explore agent:

```markdown
# Generated prompt saved to: docs/plans/issue-{N}-context-prompt.md

Analyze the codebase for context related to implementing this issue:

[Epic-specific focus areas]
[Acceptance criteria from issue]
[Required analysis points]

Return: Files to modify, patterns to follow, dependencies
```

**Targeted search based on epic:**
- `booking-payment` → Payment actions, Stripe integration, booking models
- `authentication` → Better Auth config, auth utilities, session management
- `admin` → Verification queue, user management, analytics
- [See epic-specific templates in implement_issue.py]

### Phase 3: Plan Generation

Use the `superpowers:writing-plans` skill with context from Explore agent:

```markdown
# Implementation Plan: Issue #{number}

## Title
{title}

## Files to Modify
- apps/web/lib/actions/booking.ts (add refund logic)
- apps/web/lib/actions/payment.ts (create - Stripe refund)

## Implementation Steps
1. Add refund calculation based on cancellation policy
2. Create Stripe refund via API
3. Update payment record with refund status
4. Send refund confirmation email
5. Add comprehensive tests

## Test Requirements
- Unit tests: refund calculation logic
- Integration tests: Stripe refund API
- E2E test: full cancellation + refund flow

## Dependencies
- Stripe SDK (existing)
- Resend email (existing)
```

**Plan saved to:** `docs/plans/issue-{number}-implementation-plan.md`

### Phase 4: User Approval Gate

Present plan to user:

```
📋 Implementation Plan for #104: Refund processing

**Files to modify:**
- apps/web/lib/actions/booking.ts
- apps/web/lib/actions/payment.ts (create)

**Implementation approach:**
[5 steps listed]

**Tests required:**
[3 test types]

✅ Approve and implement?
❌ Reject or request changes?
```

**Wait for explicit user approval before proceeding.**

### Phase 5: Implementation (Post-Approval)

Execute TDD workflow per CLAUDE.md requirements:

```python
# 1. Use TDD skill
invoke_skill("superpowers:test-driven-development")

# 2. For each file:
#    - Write tests FIRST (RED - should fail)
#    - Implement to pass tests (GREEN)
#    - Refactor if needed (IMPROVE)
#    - Verify tests still pass

# 3. Run quality gates:
#    - All tests pass
#    - Test coverage ≥ 80%
#    - Type check passes
#    - Linting passes
```

**Quality Gates:**
```bash
pnpm --filter web test              # Unit tests
pnpm --filter web test:coverage     # Verify 80%+
pnpm --filter web test:e2e          # E2E (if applicable)
turbo types                         # Type check
turbo lint                          # Lint with auto-fix
```

**Error recovery:**
- If quality gate fails → Use `build-error-resolver` agent
- Retry up to 3 times
- If still failing → Report to user for guidance

### Phase 6: Commit & PR Creation

Follow CLAUDE.md git workflow:

```bash
# 1. Review changes
git status
git diff

# 2. Stage files
git add <modified-files>

# 3. Commit with proper message
git commit -m "$(cat <<'EOF'
fix: implement refund processing for booking cancellations

- Add refund calculation based on cancellation policy
- Integrate Stripe refund API
- Update payment records with refund status
- Send refund confirmation emails via Resend
- Add comprehensive test coverage (unit + integration)

Closes #104

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# 4. Push branch
git push -u origin feat/issue-104-refund-processing

# 5. Create PR
gh pr create --title "fix: implement refund processing (#104)" --body "$(cat <<'EOF'
## Summary
- Implements full refund processing workflow for cancelled bookings
- Calculates refund amount based on cancellation policy
- Integrates with Stripe refund API
- Updates payment records and sends confirmation emails

## Changes
- `apps/web/lib/actions/booking.ts`: Remove TODO, add refund logic
- `apps/web/lib/actions/payment.ts`: New file with Stripe refund integration
- Tests: Unit tests for refund calculation, integration tests for Stripe API

## Test Plan
- [x] Unit tests pass (80%+ coverage)
- [x] Integration tests pass
- [x] E2E test for full cancellation + refund flow
- [x] Type check passes
- [x] Linting passes
- [ ] Manual testing on staging (reviewer)

## Related Issues
Closes #104

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"

# 6. Add comment to issue
gh issue comment 104 --body "✅ Implementation PR created: {pr_url}"
```

## Verification

Successful implementation produces:
- ✅ Feature branch created
- ✅ Context analyzed with relevant files identified
- ✅ Implementation plan generated and approved
- ✅ TDD workflow followed (tests first)
- ✅ All quality gates passed (tests, types, lint)
- ✅ Commit created with proper message
- ✅ PR created with test plan and issue link
- ✅ Issue commented with PR link

## Example: Complete Workflow

**User command:**
```
"work on #104"
```

**Execution:**

```bash
# 1. Orchestrator script initiates workflow
python3 scripts/implement_issue.py 104

# Output:
# 📥 Fetching issue #104...
# ✅ Fetched: Refund processing
#    Epic: booking-payment, Priority: critical, Status: backlog
#
# 🌿 Creating feature branch: fix/issue-104-refund-processing
# ✅ On branch: fix/issue-104-refund-processing
#
# 📋 Generating context analysis prompt...
# ✅ Context prompt saved to: docs/plans/issue-104-context-prompt.md
#
# 📝 NEXT STEPS (for Claude Code)
# [Instructions for Claude to analyze context, plan, implement]
```

**2. Claude Code takes over:**
- Reads context prompt
- Uses Explore agent for codebase analysis
- Generates implementation plan
- **Waits for user approval**
- (After approval) Implements with TDD
- Runs quality gates
- Creates commit and PR
- Links PR to issue

**3. Final state:**
- PR #105 created: "fix: implement refund processing (#104)"
- Issue #104 has comment with PR link
- All tests passing
- Ready for code review

## Command Reference

### Implementation Commands

```bash
# Specific issue
python3 scripts/implement_issue.py 104

# Auto-select next critical
python3 scripts/implement_issue.py --auto-select --priority critical

# Auto-select by epic
python3 scripts/implement_issue.py --auto-select --epic booking-payment

# Plan only (don't implement)
python3 scripts/implement_issue.py 104 --plan-only

# Skip branch creation (use current)
python3 scripts/implement_issue.py 104 --skip-branch
```

### Utility Commands

```bash
# Fetch issue details
python3 scripts/fetch_issue.py 104

# Auto-select issue
python3 scripts/select_issue.py --priority critical
python3 scripts/select_issue.py --epic payment
python3 scripts/select_issue.py --priority high --epic authentication
```

## Notes

### Integration with Existing Skills

**Required skills:**
- `superpowers:writing-plans` - Plan generation
- `superpowers:test-driven-development` - TDD workflow
- `build-error-resolver` - Fix build/type errors

**Optional skills:**
- `code-reviewer` - Review before PR creation
- `security-reviewer` - For sensitive changes (auth, payment)

### Epic-Specific Templates

Context analysis prompts are customized per epic:
- `booking-payment` → Payment actions, Stripe, booking models
- `authentication` → Better Auth, session management
- `admin` → Verification, user management
- `ui-ux` → Components, themes, accessibility
- [See full templates in scripts/implement_issue.py]

### Approval Gate Philosophy

User approval is required because:
- Prevents unwanted changes to codebase
- Allows steering the approach before code written
- Aligns with TDD and planning best practices
- User maintains control over implementation direction
- Catches misunderstandings early

### Time Savings

**Manual process:** 2-4 hours per medium-complexity issue
- 30 min: Understanding issue and codebase context
- 30 min: Planning approach
- 60-90 min: Implementation
- 30 min: Testing and quality checks
- 15 min: Commit and PR creation

**Automated process:** 30-45 minutes total
- 5 min: Issue selection and context prompt generation
- 10 min: Context analysis (automated)
- 5 min: Plan generation (automated)
- 5 min: Plan review and approval (user)
- 15-20 min: Implementation and testing (automated)
- 2 min: Commit and PR creation (automated)

**Savings:** 1.5-3 hours per issue

### Error Recovery

**Context analysis fails:**
- Widen search scope
- Try different keywords
- Manual file identification

**Plan generation unclear:**
- Request more specific acceptance criteria
- Ask clarifying questions
- Generate multiple plan options

**Implementation errors:**
- Use build-error-resolver agent
- Retry with fixes
- After 3 failures, report to user

**Test failures:**
- Review test logic
- Check implementation against plan
- Verify mocks and fixtures correct

## References

- [GitHub Docs: Using the API to manage Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects)
- [GitHub Docs: Best practices for Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub Blog: GitHub CLI project command generally available](https://github.blog/developer-skills/github/github-cli-project-command-is-now-generally-available/)
- [GitHub Gist: Notes about ProjectV2 API](https://gist.github.com/richkuz/e8842fce354edbd4e12dcbfa9ca40ff6)
