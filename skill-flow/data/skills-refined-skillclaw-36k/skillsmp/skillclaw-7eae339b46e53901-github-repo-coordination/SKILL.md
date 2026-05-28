---
name: github-repo-coordination
description: Use this skill for optimizing repository structures and coordinating operations across multiple repositories within an organization.
---

# Skill body

## Overview

This skill facilitates repository structure optimization and multi-repo management through swarm coordination. It is designed for analyzing repository structures, managing templates, synchronizing operations, and providing architecture recommendations.

## Quick Start

```bash
# List organization repositories
gh repo list org --limit 100 --json name,description,languages

# Search across repositories
gh search code "pattern" --repo org/repo1 --repo org/repo2

# Clone multiple repos
for repo in repo1 repo2 repo3; do
  gh repo clone org/$repo
done

# Check repository info
gh api repos/org/repo --jq '{name, default_branch, languages, topics}'
```

## When to Use

- Coordinating changes and updates across multiple repositories
- Analyzing and optimizing repository structures
- Creating standardized project templates
- Implementing cross-repository synchronization
- Providing architecture analysis and recommendations

## Core Capabilities

| Capability | Description |
|------------|-------------|
| Structure optimization | Implement best practices for repository organization |
| Multi-repo coordination | Synchronize operations across repositories |
| Template management | Create and manage consistent project templates |
| Architecture analysis | Provide recommendations for scalable project architecture |
| Workflow coordination | Optimize development processes across multiple repositories |

## Usage Examples

### 1. Cross-Repo Swarm Initialization

```bash
# List organization repositories
REPOS=$(gh repo list org --limit 100 --json name,description,languages \
  --jq '.[] | select(.name | test("frontend|backend|shared"))')

# Get repository details
REPO_DETAILS=$(echo "$REPOS" | jq -r '.name' | while read -r repo; do
  gh api repos/org/$repo --jq '{name, default_branch, languages, topics}'
done | jq -s '.')

# Initialize swarm with repository context
npx ruv-swarm github multi-repo-init \
  --repo-details "$REPO_DETAILS" \
  --repos "org/frontend,org/backend,org/shared" \
  --topology hierarchical \
  --shared-memory \
  --sync-strategy eventual
```

### 2. Repository Structure Analysis

```bash
# List repository contents
ls -la

# Find all config files
find . -name "*.json" -o -name "*.yml" -o -name "*.yaml" | head -20

# Analyze package dependencies
cat package.json | jq '.dependencies'
```