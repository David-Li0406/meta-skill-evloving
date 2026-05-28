---
name: github-issues
description: Activates when user requests to add, create, or file GitHub issues. Parses issue requests and creates well-structured issues via `gh` CLI with proper titles, context, and acceptance criteria.
---

# GitHub Issues Skill

Create well-structured GitHub issues from user requests using the `gh` CLI.

## Activation

Trigger when the user says things like:
- "add issues: 1. ... 2. ..."
- "create issues for..."
- "file these issues..."
- "add these to github..."

## Prerequisites

- Must be in a git repo with a GitHub remote
- `gh` CLI must be authenticated

If not in a repo or no remote, inform the user and suggest running `/bootstrap` first.

## Issue Format

Each issue must be **atomic** and **actionable**. Follow these principles:

### Titles
- Use clear, imperative voice
- Start with a verb: "Add", "Implement", "Fix", "Create", "Update"
- Be specific: "Add hash comparison for file deduplication" not "Add hashing"

### Body Structure

```markdown
## Context
Brief explanation of why this issue exists and how it fits into the project.

## Acceptance Criteria
- [ ] Specific, testable requirement
- [ ] Another concrete deliverable
- [ ] What "done" looks like

## Notes
Any additional context, constraints, or implementation hints.
```

## Workflow

### 1. Parse User Input

Extract issue ideas from the user's request. They may provide:
- A numbered list: "1. Add auth 2. Create dashboard 3. Fix bug"
- A comma-separated list: "auth, dashboard, bug fix"
- Prose: "I need authentication, a dashboard, and that bug fixed"

### 2. Expand Each Issue

For each item, generate:
- **Title**: Imperative, specific, starts with verb
- **Context**: 1-2 sentences on purpose
- **Acceptance Criteria**: 2-4 checkbox items defining "done"
- **Notes**: Only if there are implementation details worth capturing

If an item is too vague, ask the user for clarification before proceeding.

### 3. Review with User

Before creating, show the user all expanded issues:

```
I'll create these issues:

1. **Add user authentication via OAuth**
   - Context: Users need to log in to access personalized features
   - Criteria: OAuth flow, session management, logout

2. **Create dashboard component**
   - Context: Central hub for user data visualization
   - Criteria: Layout, data fetching, responsive design

Create these issues? [Yes/Edit/Cancel]
```

Use AskUserQuestion to confirm, or let them adjust.

### 4. Create Issues

```bash
gh issue create --title "Add user authentication via OAuth" --body "$(cat <<'EOF'
## Context
Users need to log in to access personalized features and save their preferences.

## Acceptance Criteria
- [ ] OAuth flow with provider (GitHub/Google)
- [ ] Session management (login persists across page loads)
- [ ] Logout functionality clears session
- [ ] Unauthenticated users redirected to login

## Notes
Consider using existing auth library rather than rolling our own.
EOF
)"
```

### 5. Summary

After creating all issues, provide a summary:

```
Created 3 issues:
- #12: Add user authentication via OAuth
- #13: Create dashboard component
- #14: Fix timezone display bug

View at: https://github.com/user/repo/issues
```

## Issue Quality Guidelines

### Good Issues
- Completable in a single focused session
- Clear definition of done
- Independent (minimal dependencies on other issues)
- Testable acceptance criteria

### Bad Issues (break these down)
- "Build the frontend" → Too broad
- "Various fixes" → Too vague
- "Research and implement auth" → Split into research + implementation

## Examples

**User input:** "add issues: 1. dark mode 2. fix that scroll bug 3. add tests"

**Expanded:**

1. **Implement dark mode theme toggle**
   - Context: Users want to switch between light and dark themes
   - Criteria: Toggle component, theme persistence, system preference detection

2. **Fix scroll position reset on navigation**
   - Context: Page scrolls to top unexpectedly when navigating between routes
   - Criteria: Scroll position maintained, works with browser back button

3. **Add unit tests for core utilities**
   - Context: No test coverage exists for utility functions
   - Criteria: Tests for date formatting, string helpers, validation functions
