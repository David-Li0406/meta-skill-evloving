---
name: github-pr-swarm-manager
description: Use this skill for comprehensive pull request management with swarm coordination, enabling automated reviews, testing, and intelligent merge workflows.
---

# GitHub PR Swarm Manager Skill

## Overview

This skill facilitates the complete lifecycle management of pull requests (PRs) using swarm coordination. It supports PR creation, multi-reviewer workflows, automated testing, conflict resolution, and intelligent merge strategies.

**Key Capabilities:**
- PR-based swarm creation with automatic agent assignment
- Multi-agent code review and validation
- Automated PR lifecycle management
- Intelligent merge coordination with consensus
- Batch PR operations across repositories

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

- Creating and managing pull requests
- Coordinating multi-reviewer workflows
- Resolving merge conflicts
- Automating PR testing and validation
- Managing branch synchronization
- Handling complex PRs requiring multi-perspective review

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

### 2. Review and Approve PR

```bash
# Get PR details
gh pr view 54 --json files,additions,deletions,title,body

# Approve PR
gh pr review 54 --approve --body "LGTM! All checks pass."

# Request changes
gh pr review 54 --request-changes --body "Please address the following..."

# Comment on PR
gh pr comment 54 --body "Consider refactoring this section."
```

### 3. Merge PR with Validation

```bash
# Check merge readiness
gh pr status

# Merge with squash
gh pr merge 54 --squash --delete-branch \
  --subject "feat: Complete integration" \
  --body "Comprehensive integration with swarm coordination"
```

### 4. Automated PR Validation

```bash
# Run comprehensive PR validation
validate_pr() {
  local PR_NUM=$1

  # Get PR details
  PR=$(gh pr view $PR_NUM --json state,mergeable,reviews,statusCheckRollup)

  # Check merge status
  MERGEABLE=$(echo "$PR" | jq -r '.mergeable')

  # Check CI status
  CI_STATUS=$(echo "$PR" | jq -r '.statusCheckRollup[0].conclusion // "pending"')

  # Check review status
  APPROVALS=$(echo "$PR" | jq '[.reviews[] | select(.state == "APPROVED")] | length')

  # Validation report
  cat << EOF
## PR #$PR_NUM Validation Report

### Merge Status
- Mergeable: $MERGEABLE
- CI Status: $CI_STATUS
- Approvals: $APPROVALS

### Recommendations
$([ "$MERGEABLE" == "MERGEABLE" ] && echo "- Ready for merge" || echo "- Resolve conflicts first")
$([ "$CI_STATUS" == "SUCCESS" ] && echo "- CI passing" || echo "- Wait for CI to complete")
$([ $APPROVALS -ge 2 ] && echo "- Sufficient approvals" || echo "- Need more reviews")
EOF
}

validate_pr 54
```

### 5. Batch PR Operations

```javascript
// Initialize coordination
mcp__claude-flow__swarm_init({ topology: "hierarchical", maxAgents: 5 })
mcp__claude-flow__agent_spawn({ type: "reviewer", name: "Senior Reviewer" })
mcp__claude-flow__agent_spawn({ type: "tester", name: "QA Engineer" })
mcp__claude-flow__agent_spawn({ type: "coordinator", name: "Merge Coordinator" })

// Create and manage PR
Bash("gh pr create --repo owner/repo --title '...' --head '...' --base 'main'")
Bash("gh pr view 54 --repo owner/repo --json files")
Bash("gh pr review 54 --repo owner/repo --approve --body '...'")
```

## Best Practices

### 1. Always Use Swarm Coordination
- Initialize swarm before complex PR operations
- Assign specialized agents for different review aspects
- Use memory for cross-agent coordination

### 2. Intelligent Review Strategy
- Automated conflict detection and resolution
- Multi-agent review for comprehensive coverage
- Performance and security validation integration

### 3. Progress Tracking
- Use TodoWrite for PR milestone tracking
- GitHub issue integration for project coordination
- Real-time status updates through swarm memory

## Error Handling

### Automatic retry logic for:
- Network failures during GitHub API calls
- Merge conflicts with intelligent resolution
- Test failures with automatic re-runs
- Review bottlenecks with load balancing

---

## Version History

- **1.0.0** (2026-01-02): Initial merged skill from github-swarm-pr and github-pr-manager