---
name: github-pr-swarm-manager
description: Use this skill for comprehensive management of pull requests with swarm coordination, enabling automated reviews, testing, and intelligent merge workflows.
---

# Skill body

## Overview

This skill facilitates the creation and management of pull requests (PRs) using swarm coordination. It supports automated reviews, testing integration, conflict resolution, and intelligent merge strategies, transforming PRs into efficient collaborative workflows.

**Key Capabilities:**
- PR creation and lifecycle management
- Multi-reviewer coordination with swarm agents
- Automated testing and validation integration
- Conflict resolution and intelligent merge strategies
- Real-time progress tracking and branch management

## Quick Start

```bash
# Check GitHub CLI authentication
gh auth status

# Create a PR with description
gh pr create --title "Feature: New API endpoint" --body "Implementation details..." --base main

# Review PR status
gh pr status

# List open PRs
gh pr list --state open
```

## When to Use

- **Creating and managing pull requests**: For new features, bug fixes, or any changes requiring review.
- **Coordinating multi-reviewer workflows**: When multiple perspectives are needed for complex changes.
- **Resolving merge conflicts**: To handle conflicts intelligently during the merge process.
- **Automating PR testing and validation**: To ensure code quality and functionality before merging.
- **Managing branch synchronization**: For keeping branches up-to-date and organized.

## Usage Examples

### 1. Create PR with Swarm Coordination

```javascript
// Initialize review swarm
mcp__claude-flow__swarm_init({ topology: "mesh", maxAgents: 4 })
mcp__claude-flow__agent_spawn({ type: "reviewer", name: "Code Quality Reviewer" })
mcp__claude-flow__agent_spawn({ type: "tester", name: "Testing Agent" })
mcp__claude-flow__agent_spawn({ type: "coordinator", name: "PR Coordinator" })

// Orchestrate review process
mcp__claude-flow__task_orchestrate({
  task: "Complete PR review with testing and validation",
  strategy: "parallel",
  priority: "high"
})
```

### 2. Multi-Agent PR Review

```bash
# Get PR details for swarm initialization
gh pr view 123 --json title,body,labels,files,reviews

# Get PR diff for analysis
gh pr diff 123

# Check PR status
gh pr checks 123

# Review PR with swarm-generated feedback
gh pr review 123 --comment --body "## Swarm Analysis
- Code quality: PASS
- Test coverage: 85%
- Security: No issues found"
```

### 3. Review and Manage PRs

```bash
# View PR details
gh pr view 54 --json files,additions,deletions,title,body

# Add reviewers
gh pr edit 54 --add-reviewer user1,user2

# Check PR status
gh pr checks 54
```