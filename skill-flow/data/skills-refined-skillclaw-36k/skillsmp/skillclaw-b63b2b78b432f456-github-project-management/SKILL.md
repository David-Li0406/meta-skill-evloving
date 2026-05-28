---
name: github-project-management
description: Use this skill when you need to manage GitHub projects effectively through swarm-coordinated issue tracking, project board automation, and sprint planning.
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
```
</details>

### 2. Project Board Management

<details>
<summary><strong>Automated Board Synchronization</strong></summary>

#### Sync Project Board with Issues

```bash
# Sync project board with issues
npx ruv-swarm github board-sync \
  --project-id "$PROJECT_ID" \
  --sync-mode "bidirectional"
```
</details>

### 3. Sprint Planning

<details>
<summary><strong>Setup Sprint Planning</strong></summary>

#### Create and Manage Sprints

```bash
# Create a new sprint
gh sprint create --title "Sprint 1" --start-date "2023-01-01" --end-date "2023-01-14"
```
</details>

## Prerequisites

- GitHub CLI (gh) installed and authenticated
- ruv-swarm or claude-flow MCP server configured
- Repository access permissions

## Tools Required

- mcp__github__*
- mcp__claude-flow__*
- Bash
- Read
- Write
- TodoWrite

## Related Skills

- github-pr-workflow
- github-release-management
- sparc-orchestrator

## Estimated Time

30-45 minutes