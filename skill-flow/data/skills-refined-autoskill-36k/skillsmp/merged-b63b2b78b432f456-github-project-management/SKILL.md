---
name: github-project-management
description: Use this skill for comprehensive GitHub project management, including swarm-coordinated issue tracking, project board automation, and sprint planning.
---

# GitHub Project Management

## Overview

A comprehensive skill for managing GitHub projects using AI swarm coordination. This skill combines intelligent issue management, automated project board synchronization, and swarm-based coordination for efficient project delivery.

## Quick Start

### Basic Issue Creation with Swarm Coordination

```bash
# Create a coordinated issue
gh issue create \
  --title "Feature: Advanced Authentication" \
  --body "Implement OAuth2 with social login..." \
  --label "enhancement,swarm-ready"

# Initialize swarm for issue
npx claude-flow@alpha hooks pre-task --description "Feature implementation"
```

### Project Board Quick Setup

```bash
# Get project ID
PROJECT_ID=$(gh project list --owner @me --format json | \
  jq -r '.projects[0].id')

# Initialize board sync
npx ruv-swarm github board-init \
  --project-id "$PROJECT_ID" \
  --sync-mode "bidirectional"
```

---

## Core Capabilities

### 1. Issue Management & Triage

<details>
<summary><strong>Automated Issue Creation</strong></summary>

#### Single Issue with Swarm Coordination

```javascript
// Initialize issue management swarm
mcp__claude-flow__swarm_init { topology: "star", maxAgents: 3 }
mcp__claude-flow__agent_spawn { type: "coordinator", name: "Issue Coordinator" }
mcp__claude-flow__agent_spawn { type: "researcher", name: "Requirements Analyst" }
mcp__claude-flow__agent_spawn { type: "coder", name: "Implementation Planner" }

// Create comprehensive issue
mcp__github__create_issue {
  owner: "org",
  repo: "repository",
  title: "Integration Review: Complete system integration",
  body: `## 🔄 Integration Review

  ### Overview
  Comprehensive review and integration between components.

  ### Objectives
  - [ ] Verify dependencies and imports
  - [ ] Ensure API integration
  - [ ] Check hook system integration
  - [ ] Validate data systems alignment

  ### Swarm Coordination
  This issue will be managed by coordinated swarm agents for optimal progress tracking.`,
  labels: ["integration", "review", "enhancement"],
  assignees: ["username"]
}

// Set up automated tracking
mcp__claude-flow__task_orchestrate {
  task: "Monitor and coordinate issue progress with automated updates",
  strategy: "adaptive",
  priority: "medium"
}
```

#### Batch Issue Creation

```bash
# Create multiple related issues using gh CLI
gh issue create \
  --title "Feature: Advanced GitHub Integration" \
  --body "Implement comprehensive GitHub workflow automation..." \
  --label "feature,github,high-priority"

gh issue create \
  --title "Bug: Merge conflicts in integration branch" \
  --body "Resolve merge conflicts..." \
  --label "bug,integration,urgent"

gh issue create \
  --title "Documentation: Update integration guides" \
  --body "Update all documentation..." \
  --label "documentation,integration"
```

</details>

<details>
<summary><strong>Issue-to-Swarm Conversion</strong></summary>

#### Transform Issues into Swarm Tasks

```bash
# Get issue details
ISSUE_DATA=$(gh issue view 456 --json title,body,labels,assignees,comments)

# Create swarm from issue
npx ruv-swarm github issue-to-swarm 456 \
  --issue-data "$ISSUE_DATA" \
  --auto-decompose \
  --assign-agents

# Batch process multiple issues
ISSUES=$(gh issue list --label "swarm-ready" --json number,title,body,labels)
npx ruv-swarm github issues-batch \
  --issues "$ISSUES" \
  --parallel

# Update issues with swarm status
echo "$ISSUES" | jq -r '.[].number' | while read -r num; do
  gh issue edit $num --add-label "swarm-processing"
done
```

#### Issue Comment Commands

Execute swarm operations via issue comments:

```markdown
<!-- In issue comment -->

/swarm analyze
/swarm decompose 5
/swarm assign @agent-coder
/swarm estimate
/swarm start
```

</details>

<details>
<summary><strong>Automated Issue Triage</strong></summary>

#### Auto-Label Based on Content

```javascript
// .github/swarm-labels.json
{
  "rules": [
    {
      "keywords": ["bug", "error", "broken"],
      "labels": ["bug", "swarm-debugger"],
      "agents": ["debugger", "tester"]
    },
    {
      "keywords": ["feature", "implement", "add"],
      "labels": ["enhancement", "swarm-feature"],
      "agents": ["architect", "coder", "tester"]
    },
    {
      "keywords": ["slow", "performance", "optimize"],
      "labels": ["performance", "swarm-optimizer"],
      "agents": ["analyst", "optimizer"]
    }
  ]
}
```

#### Automated Triage System

```bash
# Analyze and triage unlabeled issues
npx ruv-swarm github triage \
  --unlabeled \
  --analyze-content \
  --suggest-labels \
  --assign-priority

# Find and link duplicate issues
npx ruv-swarm github find-duplicates \
  --threshold 0.8 \
  --link-related \
  --close-duplicates
```

</details>

<details>
<summary><strong>Task Decomposition & Progress Tracking</strong></summary>

#### Break Down Issues into Subtasks

```bash
# Get issue body
ISSUE_BODY=$(gh issue view 456 --json body --jq '.body')

# Decompose into subtasks
SUBTASKS=$(npx ruv-swarm github issue-decompose 456 \
  --body "$ISSUE_BODY" \
  --max-subtasks 10 \
  --assign-priorities)

# Update issue with checklist
CHECKLIST=$(echo "$SUBTASKS" | jq -r '.tasks[] | "- [ ] " + .description')
UPDATED_BODY="$ISSUE_BODY

## Subtasks
$CHECKLIST"

gh issue edit 456 --body "$UPDATED_BODY"

# Create linked issues for major subtasks
echo "$SUBTASKS" | jq -r '.tasks[] | select(.priority == "high")' | while read -r task; do
  TITLE=$(echo "$task" | jq -r '.title')
  BODY=$(echo "$task" | jq -r '.description')

  gh issue create \
    --title "$TITLE" \
    --body "$BODY

Parent issue: #456" \
    --label "subtask"
done
```

#### Automated Progress Updates

```bash
# Get current issue state
CURRENT=$(gh issue view 456 --json body,labels)

# Get swarm progress
PROGRESS=$(npx ruv-swarm github issue-progress 456)

# Update checklist in issue body
UPDATED_BODY=$(echo "$CURRENT" | jq -r '.body' | \
  npx ruv-swarm github update-checklist --progress "$PROGRESS")

# Edit issue with updated body
gh issue edit 456 --body "$UPDATED_BODY"

# Post progress summary as comment
SUMMARY=$(echo "$PROGRESS" | jq -r '
"## 📊 Progress Update

**Completion**: \(.completion)%
**ETA**: \(.eta)

### Completed Tasks
\(.completed | map("- ✅ " + .) | join("\n"))

### In Progress
\(.in_progress | map("- 🔄 " + .) | join("\n"))

### Remaining
\(.remaining | map("- ⏳ " + .) | join("\n"))

---
🤖 Automated update by swarm agent"')

gh issue comment 456 --body "$SUMMARY"

# Update labels based on progress
if [[ $(echo "$PROGRESS" | jq -r '.completion') -eq 100 ]]; then
  gh issue edit 456 --add-label "ready-for-review" --remove-label "in-progress"
fi
```

</details>

<details>
<summary><strong>Stale Issue Management</strong></summary>

#### Auto-Close Stale Issues with Swarm Analysis

```bash
# Find stale issues
STALE_DATE=$(date -d '30 days ago' --iso-8601)
STALE_ISSUES=$(gh issue list --state open --json number,title,updatedAt,labels \
  --jq ".[] | select(.updatedAt < \"$STALE_DATE\")")

# Analyze each stale issue
echo "$STALE_ISSUES" | jq -r '.number' | while read -r num; do
  # Get full issue context
  ISSUE=$(gh issue view $num --json title,body,comments,labels)

  # Analyze with swarm
  ACTION=$(npx ruv-swarm github analyze-stale \
    --issue "$ISSUE" \
    --suggest-action)

  case "$ACTION" in
    "close")
      gh issue comment $num --body "This issue has been inactive for 30 days and will be closed in 7 days if there's no further activity."
      gh issue edit $num --add-label "stale"
      ;;
    "keep")
      gh issue edit $num --remove-label "stale" 2>/dev/null || true
      ;;
    "needs-info")
      gh issue comment $num --body "This issue needs more information. Please provide additional context or it may be closed as stale."
      gh issue edit $num --add-label "needs-info"
      ;;
  esac
done

# Close issues that have been stale for 37+ days
gh issue list --label stale --state open --json number,updatedAt \
  --jq ".[] | select(.updatedAt < \"$(date -d '37 days ago' --iso-8601)\") | .number" | \
  while read -r num; do
    gh issue close $num --comment "Closing due to inactivity. Feel free to reopen if this is still relevant."
  done
```

</details>

### 2. Project Board Automation

<details>
<summary><strong>Board Initialization & Configuration</strong></summary>

#### Connect Swarm to GitHub Project

```bash
# Get project details
PROJECT_ID=$(gh project list --owner @me --format json | \
  jq -r '.projects[] | select(.title == "Development Board") | .id')

# Initialize swarm with project
npx ruv-swarm github board-init \
  --project-id "$PROJECT_ID" \
  --sync-mode "bidirectional" \
  --create-views "swarm-status,agent-workload,priority"

# Create project fields for swarm tracking
gh project field-create $PROJECT_ID --owner @me \
  --name "Swarm Status" \
  --data-type "SINGLE_SELECT" \
  --single-select-options "pending,in_progress,completed"
```

#### Board Mapping Configuration

```yaml
# .github/board-sync.yml
version: 1
project:
  name: "AI Development Board"
  number: 1

mapping:
  # Map swarm task status to board columns
  status:
    pending: "Backlog"
    assigned: "Ready"
    in_progress: "In Progress"
    review: "Review"
    completed: "Done"
    blocked: "Blocked"

  # Map agent types to labels
  agents:
    coder: "🔧 Development"
    tester: "🧪 Testing"
    analyst: "📊 Analysis"
    designer: "🎨 Design"
    architect: "🏗️ Architecture"

  # Map priority to project fields
  priority:
    critical: "🔴 Critical"
    high: "🟡 High"
    medium: "🟢 Medium"
    low: "⚪ Low"

  # Custom fields
  fields:
    - name: "Agent Count"
      type: number
      source: task.agents.length
    - name: "Complexity"
      type: select
      source: task.complexity
    - name: "ETA"
      type: date
      source: task.estimatedCompletion
```

</details>

<details>
<summary><strong>Task Synchronization</strong></summary>

#### Real-time Board Sync

```bash
# Sync swarm tasks with project cards
npx ruv-swarm github board-sync \
  --map-status '{
    "todo": "To Do",
    "in_progress": "In Progress",
    "review": "Review",
    "done": "Done"
  }' \
  --auto-move-cards \
  --update-metadata

# Enable real-time board updates
npx ruv-swarm github board-realtime \
  --webhook-endpoint "https://api.example.com/github-sync" \
  --update-frequency "immediate" \
  --batch-updates false
```

#### Convert Issues to Project Cards

```bash
# List issues with label
ISSUES=$(gh issue list --label "enhancement" --json number,title,body)

# Add issues to project
echo "$ISSUES" | jq -r '.[].number' | while read -r issue; do
  gh project item-add $PROJECT_ID --owner @me --url "https://github.com/$GITHUB_REPOSITORY/issues/$issue"
done

# Process with swarm
npx ruv-swarm github board-import-issues \
  --issues "$ISSUES" \
  --add-to-column "Backlog" \
  --parse-checklist \
  --assign-agents
```

</details>

<details>
<summary><strong>Smart Card Management</strong></summary>

#### Auto-Assignment

```bash
# Automatically assign cards to agents
npx ruv-swarm github board-auto-assign \
  --strategy "load-balanced" \
  --consider "expertise,workload,availability" \
  --update-cards
```

#### Intelligent Card State Transitions

```bash
# Smart card movement based on rules
npx ruv-swarm github board-smart-move \
  --rules '{
    "auto-progress": "when:all-subtasks-done",
    "auto-review": "when:tests-pass",
    "auto-done": "when:pr-merged"
  }'
```

#### Bulk Operations

```bash
# Bulk card operations
npx ruv-swarm github board-bulk \
  --filter "status:blocked" \
  --action "add-label:needs-attention" \
  --notify-assignees
```

</details>

<details>
<summary><strong>Custom Views & Dashboards</strong></summary>

#### View Configuration

```javascript
// Custom board views
{
  "views": [
    {
      "name": "Swarm Overview",
      "type": "board",
      "groupBy": "status",
      "filters": ["is:open"],
      "sort": "priority:desc"
    },
    {
      "name": "Agent Workload",
      "type": "table",
      "groupBy": "assignedAgent",
      "columns": ["title", "status", "priority", "eta"],
      "sort": "eta:asc"
    },
    {
      "name": "Sprint Progress",
      "type": "roadmap",
      "dateField": "eta",
      "groupBy": "milestone"
    }
  ]
}
```

#### Dashboard Configuration

```javascript
// Dashboard with performance widgets
{
  "dashboard": {
    "widgets": [
      {
        "type": "chart",
        "title": "Task Completion Rate",
        "data": "completed-per-day",
        "visualization": "line"
      },
      {
        "type": "gauge",
        "title": "Sprint Progress",
        "data": "sprint-completion",
        "target": 100
      },
      {
        "type": "heatmap",
        "title": "Agent Activity",
        "data": "agent-tasks-per-day"
      }
    ]
  }
}
```

</details>

### 3. Sprint Planning & Tracking

<details>
<summary><strong>Sprint Management</strong></summary>

#### Initialize Sprint with Swarm Coordination

```bash
# Manage sprints with swarms
npx ruv-swarm github