---
name: create-issue
description: Commands for creating new issues and managing priority on the Guidr GitHub Projects board. Includes issue templates for features, bugs, documentation, and technical debt.
---

# Create Issue Skill

Commands for creating new issues and managing priority on the Guidr GitHub Projects board.

## Create a New Issue

```bash
# Create a basic issue
gh issue create --title "Add user authentication" --body "Implement user login and registration"

# Create with more details
gh issue create \
  --title "Add push notifications" \
  --body "Implement push notifications for guides" \
  --assignee @me

# Create with labels
gh issue create \
  --title "Fix session timer bug" \
  --body "Timer continues running after pause" \
  --label "bug,mobile"

# Create with milestone
gh issue create \
  --title "Redesign home screen" \
  --body "Improve UI/UX for home screen" \
  --milestone "v1.1.0"
```

## Add to Project and Set Priority

```bash
# Add issue to Guidr project (after creation)
gh issue edit 123 --add-project "Guidr"

# Set initial status
gh issue edit 123 --add-project "Guidr" --project-field "Status" --project-value "Todo"

# Set priority (if project has priority field)
gh issue edit 123 --add-project "Guidr" --project-field "Priority" --project-value "High"
```

## Issue Labels

Useful labels for categorization:

```bash
# Common labels
--label "bug"              # Bug fix
--label "feature"          # New feature
--label "enhancement"      # Enhancement to existing feature
--label "documentation"    # Documentation
--label "mobile"           # Mobile-specific
--label "web"              # Web-specific
--label "api"              # API-specific
--label "performance"      # Performance improvement
--label "blocked"          # Blocked by something
--label "help-wanted"      # Help needed
```

## Create from Template

```bash
# Create a feature request
gh issue create \
  --title "Feature: [brief description]" \
  --body "## Description
Describe the feature here

## Use Case
Why is this needed?

## Implementation Notes
Any technical considerations?"

# Create a bug report
gh issue create \
  --title "Bug: [brief description]" \
  --body "## Description
What's the bug?

## Steps to Reproduce
1. ...
2. ...

## Expected Behavior
What should happen?

## Actual Behavior
What happens instead?

## Environment
Platform, version, etc."
```

## Set Up for Claude Code

When creating an issue you'll work on:

```bash
# Create and assign to yourself
gh issue create --title "Implementation task" --body "Details" --assignee @me

# Get the issue number from output, then:
gh issue edit <number> --add-project "Guidr" --project-field "Status" --project-value "In Progress"
```

## Common Issue Types

### Feature Requests
```bash
gh issue create \
  --title "feat: add offline support" \
  --body "Allow users to access guides offline by caching content locally" \
  --label "feature,mobile"
```

### Bug Reports
```bash
gh issue create \
  --title "fix: session timer glitch on pause" \
  --body "Timer continues running after pause button clicked" \
  --label "bug,critical"
```

### Documentation
```bash
gh issue create \
  --title "docs: add API authentication guide" \
  --body "Document how to authenticate with the API" \
  --label "documentation"
```

### Technical Debt
```bash
gh issue create \
  --title "refactor: simplify session state management" \
  --body "Current implementation is complex. Refactor to use cleaner patterns" \
  --label "refactor,technical-debt"
```

## Project Board

**Board URL**: https://github.com/users/stevendejongnl/projects/3

New issues start in **Todo** status and can be prioritized from there.

## Tips

- Use clear, descriptive titles
- Include acceptance criteria in the body
- Label issues appropriately for filtering
- Add to project immediately for visibility
- Assign to yourself if you plan to work on it
