---
name: github-issue-swarm-management
description: Use this skill for intelligent management of GitHub issues through swarm coordination, enabling automated task decomposition, progress tracking, and multi-agent collaboration.
---

# GitHub Issue Swarm Management Skill

## Overview

This skill facilitates intelligent management of GitHub issues by transforming them into swarm tasks. It enables automated task decomposition, agent coordination, and comprehensive progress tracking, making it ideal for complex issues, bug investigations, and feature requests.

## Quick Start

```bash
# Create an issue
gh issue create --title "<issue_title>" --body "<issue_body>" --label "<labels>"

# List open issues
gh issue list --state open

# View issue details
gh issue view <issue_number>

# Add comment to issue
gh issue comment <issue_number> --body "<comment_body>"

# Close issue
gh issue close <issue_number> --reason completed

# Initialize swarm for an issue
gh issue comment <issue_number> --body "## Swarm Initialized"
```

## When to Use

- For complex issues requiring multi-step task decomposition.
- When managing bug investigations that need systematic debugging.
- For feature requests that require architecture and implementation coordination.
- To handle technical debt with multiple components.
- For coordinating child issues under a parent epic.

## Core Capabilities

| Capability | Description |
|------------|-------------|
| Smart templates | Automated issue creation with templates. |
| Progress tracking | Swarm-coordinated updates and visual progress indicators. |
| Multi-agent collaboration | Complex issue resolution with specialized agents. |
| Automated triage | Intelligent labeling and organization of issues. |
| Task decomposition | Breaking down issues into manageable subtasks. |

## Usage Examples

### 1. Issue-to-Swarm Conversion

```bash
# Get complete issue context
ISSUE=$(gh issue view <issue_number> --json title,body,labels,assignees,comments)

# Analyze issue complexity and determine swarm topology
# (Add logic to determine topology based on issue complexity)

# Initialize swarm comment
gh issue comment <issue_number> --body "## Swarm Initialized"
```

### 2. Task Decomposition

```bash
# Extract tasks from issue body
TASKS=$(echo "$ISSUE_BODY" | grep -E '^\s*-\s*\[ \]' | sed 's/.*\[ \]//')

# Create subtask checklist and update issue
gh issue edit <issue_number> --body "$UPDATED_BODY"
```

### 3. Progress Tracking

```bash
# Track issue progress
track_progress() {
  local ISSUE_NUM=$1
  # Logic to calculate and post progress updates
}
track_progress <issue_number>
```

### 4. Automated Triage

```bash
# Triage unlabeled issues
triage_issues() {
  # Logic to analyze and label issues based on content
}
triage_issues
```

### 5. Issue Comment Commands

Use these commands in issue comments:

```markdown
<!-- Analyze issue and suggest approach -->
/swarm analyze

<!-- Decompose into subtasks -->
/swarm decompose

<!-- Assign specific agent type -->
/swarm assign @coder

<!-- Start swarm processing -->
/swarm start

<!-- Check progress -->
/swarm progress
```

## Best Practices

### 1. Swarm Coordination
- Always initialize swarm for complex issues.
- Assign specialized agents based on issue type.
- Use memory for progress coordination.

### 2. Automated Progress Tracking
- Regular automated updates with swarm coordination.
- Visual progress indicators and completion tracking.

### 3. Smart Labeling and Organization
- Consistent labeling strategy across repositories.
- Priority-based issue sorting and assignment.

## Metrics and Analytics

### Automatic tracking of:
- Issue creation and resolution times.
- Agent productivity metrics.
- Project milestone progress.

### Reporting features:
- Weekly progress summaries.
- Agent performance analytics.

---

## Version History

- **1.0.0** (2026-01-02): Initial release - merged from GitHub issue tracker and swarm issue management skills.