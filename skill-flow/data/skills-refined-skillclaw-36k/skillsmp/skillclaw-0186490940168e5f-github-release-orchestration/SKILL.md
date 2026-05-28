---
name: github-release-orchestration
description: Use this skill for orchestrating complex software releases, including automated versioning, changelog generation, and multi-platform deployment across multiple repositories.
---

# Skill body

## Overview

This skill orchestrates complex software releases using automated processes. It handles release planning, version coordination, changelog generation, artifact building, progressive deployment, and multi-repository release management.

## Quick Start

```bash
# List releases
gh release list

# Create a release
gh release create v1.0.0 --title "Release v1.0.0" --notes "Release notes..."

# Get last release tag
LAST_TAG=$(gh release list --limit 1 --json tagName -q '.[0].tagName')

# Get commits since last release
gh api repos/owner/repo/compare/${LAST_TAG}...HEAD --jq '.commits[].commit.message'

# Generate changelog
gh pr list --state merged --base main --json number,title,labels,mergedAt \
  --jq ".[] | select(.mergedAt > \"$(gh release view $LAST_TAG --json publishedAt -q .publishedAt)\")"

# Download release assets
gh release download v1.0.0

# Delete release
gh release delete v1.0.0 --yes
```

## When to Use

- Planning and coordinating major software releases
- Automating versioning and changelog generation
- Building artifacts for multiple platforms
- Implementing progressive deployment strategies
- Managing releases across multiple repositories

## Core Capabilities

| Capability | Description |
|------------|-------------|
| Automated pipelines | Comprehensive testing and validation |
| Version coordination | Multi-package version sync |
| Changelog generation | Semantic commit analysis and contributor attribution |
| Artifact building | Cross-platform compilation and optimization |
| Progressive deployment | Staged rollout and rollback capabilities |

## Usage Examples

### 1. Coordinated Release Preparation

```javascript
// Initialize release management swarm
mcp__claude-flow__swarm_init({ topology: "hierarchical", maxAgents: 6 })
mcp__claude-flow__agent_spawn({ type: "coordinator", name: "Release Coordinator" })
mcp__claude-flow__agent_spawn({ type: "tester", name: "QA Engineer" })
mcp__claude-flow__agent_spawn({ type: "reviewer", name: "Release Reviewer" })
mcp__claude-flow__agent_spawn({ type: "coder", name: "Version Manager" })
mcp__claude-flow__agent_spawn({ type: "analyst", name: "Deployment Analyst" })

// Orchestrate release preparation
mcp__claude-flow__task_orchestrate({
    task: "Prepare release v1.0.72 with comprehensive testing and validation",
    strategy: "sequential",
    priority: "critical"
})
```

### 2. Release Planning

```bash
# Get commit history since last release
LAST_TAG=$(gh release list --limit 1 --json tagName -q '.[0].tagName')
COMMITS=$(gh api repos/owner/repo/compare/${LAST_TAG}...HEAD --jq '.commits')

# Plan release with commit analysis
npx ruv-swarm github release-plan \
  --commits "$COMMITS" \
  --analyze-commits \
  --suggest-version \
  --identify-breaking \
  --generate-timeline
```