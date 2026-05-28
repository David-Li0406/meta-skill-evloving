---
name: github-issue-swarm-coordination
description: Use this skill for intelligent management of GitHub issues through automated swarm coordination, enabling task decomposition, progress tracking, and multi-agent collaboration.
---

# Skill body

## Overview

This skill facilitates intelligent management of GitHub issues by transforming them into swarm tasks. It enables automated task decomposition, agent coordination, and comprehensive progress tracking, making it ideal for complex issues requiring multi-agent collaboration.

## Quick Start

```bash
# Create an issue
gh issue create --title "Bug: Login fails" --body "Steps to reproduce..." --label "bug"

# List open issues
gh issue list --state open

# View issue details
gh issue view 54

# Add comment to issue
gh issue comment 54 --body "Progress update..."

# Close issue
gh issue close 54 --reason completed

# Get issue details for swarm initialization
gh issue view 456 --json title,body,labels,assignees,comments

# List issues ready for swarm processing
gh issue list --label "swarm-ready"

# Add swarm label to trigger processing
gh issue edit 456 --add-label "swarm-ready"

# Post swarm status comment
gh issue comment 456 --body "Swarm initialized for this issue"
```

## When to Use

- Creating issues with smart templates and automated labeling
- Tracking issue progress with swarm coordination
- Decomposing complex issues into manageable tasks
- Multi-agent collaboration on bug investigations and feature requests
- Coordinating project milestones and managing technical debt

## Core Capabilities

| Capability | Description |
|------------|-------------|
| Smart templates | Automated issue creation with templates |
| Progress tracking | Swarm-coordinated updates |
| Multi-agent collaboration | Complex issue resolution |
| Task decomposition | Breaking down issues into subtasks |
| Automated triage | Efficient labeling and organization |
| Lifecycle management | Comprehensive tracking of issue status |

## Usage Examples

### 1. Create Issue with Swarm Tracking

```javascript
// Initialize issue management swarm
mcp__claude-flow__swarm_init({ topology: "star", maxAgents: 3 })
mcp__claude-flow__agent_spawn({ type: "coordinator", name: "Issue Coordinator" })
mcp__claude-flow__agent_spawn({ type: "researcher", name: "Requirements Analyst" })
mcp__claude-flow__agent_spawn({ type: "coder", name: "Implementation Planner" })

// Set up automated tracking
mcp__claude-flow__task_orchestrate({
    task: "Monitor and coordinate issue progress with automated updates",
    strategy: "adaptive",
    priority: "medium"
})
```

### 2. Issue-to-Swarm Conversion

```bash
# Get complete issue context
ISSUE=$(gh issue view 456 --json title,body,labels,assignees,comments,projectItems)

# Analyze issue complexity
BODY=$(echo "$ISSUE" | jq -r '.body')
LABEL_COUNT=$(echo "$ISSUE" | jq '.labels | length')
COMMENT_COUNT=$(echo "$ISSUE" | jq '.comments | length')

# Determine swarm topology based on complexity
if [ $LABEL_COUNT -gt 3 ] || [ ${#BODY} -gt 1000 ]; then
  TOPOLOGY="hierarchical"
  MAX_AGENTS=8
elif echo "$BODY" | grep -qE "(\[ \]|1\.|step)" ; then
  TOPOLOGY="mesh"
  MAX_AGENTS=5
else
  TOPOLOGY="ring"
  MAX_AGENTS=3
fi

echo "Issue #456: Using $TOPOLOGY topology with $MAX_AGENTS agents"

# Initialize swarm comment
gh issue comment 456 --body "## Swarm Initialized

**Topology**: $TOPOLOGY
**Agents**: $MAX_AGENTS

Processing issue for task decomposition..."
```