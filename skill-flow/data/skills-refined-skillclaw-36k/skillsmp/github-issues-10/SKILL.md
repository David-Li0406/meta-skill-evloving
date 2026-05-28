---
name: github-issues
description: "GitHub issues management and best practices. Use when auditing issue quality, creating issue templates, adding acceptance criteria, improving issue workflows, or coaching teams on issue hygiene. Also use for setting up labels, reviewing stale issues, writing user stories, creating bug reports, or when issues lack clear titles, descriptions, or definitions of done. Essential for repository maintainers and project managers."
---

# GitHub Issues Management

## Overview

Good issues drive good software. Bad issues waste everyone's time. This skill guides systematic improvement of GitHub issue management - from individual issue quality to repository-wide workflows.

**Core principle:** Every issue should be actionable. If someone can't start working from the issue alone, it's not ready.

## The Issue Management Process

### Phase 1: Issue Quality Audit

Assess current state of issues:

1. **Title Quality**
   - Is it specific and actionable?
   - Does it describe the outcome, not just the task?
   - Can someone understand it without reading the body?

2. **Description Completeness**
   - Sufficient context provided?
   - Steps to reproduce (for bugs)?
   - User story format (for features)?

3. **Acceptance Criteria**
   - Clear definition of "done"?
   - Testable conditions?
   - Checkbox format for tracking?

4. **Metadata**
   - Appropriate labels?
   - Assigned to someone?
   - Milestone set?
   - Related issues linked?

### Phase 2: Template Implementation

Create templates in `.github/ISSUE_TEMPLATE/`:

1. **Bug Report** (`bug_report.md`)
   - Description, steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Acceptance criteria

2. **Feature Request** (`feature_request.md`)
   - User story format
   - Detailed description
   - Acceptance criteria
   - Additional context

3. **Documentation** (`documentation.md`)
   - What needs documenting
   - Target audience
   - Acceptance criteria

4. **Config File** (`config.yml`)
   - Blank issue prevention
   - External links (discussions, security)

### Phase 3: Workflow Setup

Implement issue lifecycle management:

1. **Labels**
   - Type: bug, enhancement, documentation
   - Priority: priority-1, priority-2, priority-3
   - Status: needs-triage, in-progress, blocked
   - Effort: good-first-issue, help-wanted

2. **Automation**
   - Auto-label based on content
   - Stale issue management
   - Required fields validation
   - Project board integration

## Red Flags - STOP and Fix

### Issue Title Red Flags
```
❌ "Bug fix"                    → "Fix login timeout on slow connections"
❌ "Update"                     → "Update API docs with auth examples"
❌ "Feature"                    → "Add dark mode toggle to settings"
❌ "Problem with X"             → "X crashes when input exceeds 1MB"
❌ "Doesn't work"               → "Payment form rejects valid credit cards"
```

### Issue Body Red Flags
```
❌ Empty or minimal description
❌ No steps to reproduce for bugs
❌ No acceptance criteria
❌ Screenshots of text (use code blocks)
❌ "See Slack conversation" (context should be in issue)
❌ Multiple unrelated problems in one issue
```

### Repository Red Flags
```
❌ No issue templates
❌ No labels defined
❌ Many issues without labels
❌ Many issues without assignees
❌ Stale issues (>30 days, no activity)
❌ Duplicate issues not linked/closed
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "The title is obvious" | Not to someone new. Be explicit. |
| "We discussed it in Slack" | Slack disappears. Issues persist. |
| "Acceptance criteria slow us down" | Unclear scope slows you down more. |
| "Labels are overhead" | Labels enable filtering and triage. |
| "We'll clean up issues later" | Later never comes. Maintain as you go. |
| "Everyone knows what this means" | New team members don't. Be explicit. |

## Issue Quality Checklist

Before creating/approving an issue:

**Title:**
- [ ] Specific and actionable
- [ ] Describes outcome, not just task
- [ ] Understandable without reading body

**Description:**
- [ ] Sufficient context for someone new
- [ ] User story format for features
- [ ] Steps to reproduce for bugs
- [ ] No external dependencies (Slack, email)

**Acceptance Criteria:**
- [ ] Clear definition of "done"
- [ ] Testable conditions
- [ ] Checkbox format: `- [ ] Criteria`

**Metadata:**
- [ ] Appropriate labels applied
- [ ] Assignee set (or needs-triage label)
- [ ] Related issues linked
- [ ] Milestone if applicable

## Quick Patterns

### Good Issue Title Format

```
[Type]: [Specific action] [Context]

Examples:
✅ "Fix: Login button unresponsive on mobile Safari"
✅ "Add: Dark mode toggle to user settings"
✅ "Docs: Add API authentication examples"
✅ "Perf: Reduce dashboard load time from 5s to <1s"
```

### User Story Format

```markdown
## User Story
As a [type of user],
I want [goal/desire],
So that [benefit/value].

## Description
[Detailed explanation of the feature]

## Acceptance Criteria
- [ ] [Specific, testable condition]
- [ ] [Another condition]
- [ ] Documentation updated
- [ ] Tests added
```

### Bug Report Format

```markdown
## Description
[Clear description of the bug]

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [e.g., macOS 14.0]
- Browser: [e.g., Chrome 120]
- Version: [e.g., 1.2.3]

## Acceptance Criteria
- [ ] Bug no longer occurs
- [ ] Regression test added
- [ ] Root cause documented
```

### Acceptance Criteria Examples

```markdown
## Good Acceptance Criteria

Feature: User Authentication
- [ ] Users can log in with email and password
- [ ] Failed login shows specific error message
- [ ] Session expires after 24 hours of inactivity
- [ ] "Remember me" extends session to 30 days
- [ ] Password reset email sent within 30 seconds

Bug Fix: Payment Processing
- [ ] Payments complete successfully with valid cards
- [ ] Appropriate error shown for declined cards
- [ ] No duplicate charges on retry
- [ ] Transaction logged for audit

## Bad Acceptance Criteria

❌ "It works"
❌ "Users are happy"
❌ "No bugs"
❌ "Fast enough"
❌ "Looks good"
```

## Quick Commands

```bash
# List issues without labels
gh issue list --search "no:label"

# List issues without assignees
gh issue list --search "no:assignee"

# List stale issues (no updates in 30 days)
gh issue list --search "updated:<$(date -v-30d +%Y-%m-%d)"

# List issues by label
gh issue list --label "bug"
gh issue list --label "priority-1"

# Add label to issue
gh issue edit 42 --add-label "needs-triage"

# Create label
gh label create "priority-1" --description "High priority" --color "b60205"

# List all labels
gh label list

# Check if templates exist
ls -la .github/ISSUE_TEMPLATE/

# Validate issue template YAML
cat .github/ISSUE_TEMPLATE/config.yml
```

## Recommended Labels

| Label | Description | Color | Hex |
|-------|-------------|-------|-----|
| `bug` | Something isn't working | Red | #d73a4a |
| `enhancement` | New feature or request | Cyan | #a2eeef |
| `documentation` | Documentation only | Blue | #0075ca |
| `good first issue` | Good for newcomers | Purple | #7057ff |
| `help wanted` | Extra attention needed | Green | #008672 |
| `priority-1` | Critical priority | Dark Red | #b60205 |
| `priority-2` | Medium priority | Yellow | #fbca04 |
| `priority-3` | Low priority | Light Green | #0e8a16 |
| `needs-triage` | Needs categorization | Gray | #ededed |
| `blocked` | Waiting on external | Orange | #f9a825 |
| `duplicate` | Duplicate issue | Light Gray | #cfd3d7 |
| `wontfix` | Will not be addressed | White | #ffffff |

## Issue Audit Output Format

When auditing, report like this:

```markdown
# GitHub Issues Audit: my-org/my-repo

**Date:** 2026-01-23
**Total Open Issues:** 45

## Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| With acceptance criteria | 12 | 27% |
| With labels | 38 | 84% |
| With assignees | 15 | 33% |
| Stale (>30 days) | 18 | 40% |

## Issues Needing Attention

### Missing Acceptance Criteria (33 issues)
- #42: Add user authentication
- #51: Improve performance
- #67: Refactor payment module

### Vague Titles (8 issues)
| Issue | Current | Suggested |
|-------|---------|-----------|
| #23 | "Bug fix" | "Fix login timeout on mobile" |
| #34 | "Update docs" | "Add API auth examples to README" |

### Stale Issues (18 issues)
- #12: Last activity 45 days ago
- #19: Last activity 62 days ago
- Consider: close, reassign, or add update

## Recommendations

1. **Create issue templates** - Add .github/ISSUE_TEMPLATE/
2. **Add missing labels** - 7 issues unlabeled
3. **Define acceptance criteria format** - Document in CONTRIBUTING.md
4. **Implement stale bot** - Auto-warn after 30 days
```

## References

Detailed templates and examples in `references/`:
- `issue-templates.md` - Complete template examples
- `acceptance-criteria.md` - How to write good AC
- `github-actions.md` - Automation workflows
