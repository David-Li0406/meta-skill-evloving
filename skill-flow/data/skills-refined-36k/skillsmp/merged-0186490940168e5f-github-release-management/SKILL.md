---
name: github-release-management
description: Use this skill for orchestrating and automating complex software releases, including version coordination, changelog generation, artifact building, and deployment across multiple repositories.
---

# GitHub Release Management Skill

## Overview

This skill automates and orchestrates complex software releases using AI swarms. It handles release planning, version coordination, changelog generation, artifact building, progressive deployment, and multi-repo release coordination.

## Quick Start

```bash
# List releases
gh release list

# Create a release
gh release create v1.0.0 --title "Release v1.0.0" --notes "Release notes..."

# View release
gh release view v1.0.0

# Download release assets
gh release download v1.0.0

# Delete release
gh release delete v1.0.0 --yes
```

## When to Use

- Planning and coordinating major software releases
- Automating changelog generation and versioning
- Building and deploying artifacts across multiple platforms
- Implementing progressive deployment strategies
- Coordinating releases across multiple repositories
- Managing hotfixes and rollback procedures

## Core Capabilities

| Capability | Description |
|------------|-------------|
| Automated pipelines | Comprehensive testing and validation |
| Version coordination | Multi-package version sync |
| Changelog generation | Semantic commit analysis and contributor attribution |
| Artifact building | Cross-platform compilation and optimization |
| Deployment orchestration | Staged deployment with rollback capabilities |
| Multi-repo release coordination | Coordinated releases across multiple repositories |

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

### 2. Generate Changelog

```bash
# Get all merged PRs between versions
PRS=$(gh pr list --state merged --base main --json number,title,labels,author,mergedAt \
  --jq ".[] | select(.mergedAt > \"$(gh release view v1.0.0 --json publishedAt -q .publishedAt)\")")

# Get contributors
CONTRIBUTORS=$(echo "$PRS" | jq -r '[.author.login] | unique | join(", ")')

# Get commit messages
COMMITS=$(gh api repos/owner/repo/compare/v1.0.0...HEAD --jq '.commits[].commit.message')

# Generate categorized changelog
CHANGELOG=$(npx ruv-swarm github changelog \
  --prs "$PRS" \
  --commits "$COMMITS" \
  --contributors "$CONTRIBUTORS" \
  --from v1.0.0 \
  --to HEAD \
  --categorize \
  --add-migration-guide)

echo "$CHANGELOG" > CHANGELOG.md
```

### 3. Create Release with Assets

```bash
# Generate changelog from PRs and commits
CHANGELOG=$(gh api repos/owner/repo/compare/${LAST_TAG}...HEAD \
  --jq '.commits[].commit.message' | \
  npx ruv-swarm github generate-changelog)

# Create release draft
gh release create v2.0.0 \
  --draft \
  --title "Release v2.0.0" \
  --notes "$CHANGELOG" \
  --target main

# Build and upload assets
npm run build
gh release upload v2.0.0 dist/*.tar.gz dist/*.zip

# Publish release
gh release edit v2.0.0 --draft=false

# Create announcement issue
gh issue create \
  --title "Released v2.0.0" \
  --body "$CHANGELOG" \
  --label "announcement,release"
```

### 4. Multi-Repo Release Coordination

```bash
# Coordinate releases across repos
REPOS=("frontend:v2.0.0" "backend:v2.1.0" "cli:v1.5.0")

for entry in "${REPOS[@]}"; do
  IFS=':' read -r repo version <<< "$entry"

  # Create release in each repo
  gh release create "$version" \
    --repo "org/$repo" \
    --title "Release $version" \
    --generate-notes

  echo "Released $repo $version"
done

# Link releases
npx ruv-swarm github multi-release-link \
  --releases "${REPOS[@]}" \
  --create-summary
```

### 5. Rollback Procedure

```bash
# Immediate rollback
npx ruv-swarm github rollback \
  --to-version v1.9.9 \
  --reason "Critical bug in v2.0.0" \
  --preserve-data \
  --notify-users
```

## Release Strategies

### Semantic Versioning

```javascript
const versionStrategy = {
    major: "Breaking changes or architecture overhauls",
    minor: "New features, GitHub integration, swarm enhancements",
    patch: "Bug fixes, documentation updates, dependency updates",
    coordination: "Cross-package version alignment"
}
```

### Progressive Deployment

```yaml
# Staged rollout configuration
deployment:
  strategy: progressive
  stages:
    - name: canary
      percentage: 5
      duration: 1h
      metrics:
        - error-rate < 0.1%
        - latency-p99 < 200ms

    - name: partial
      percentage: 25
      duration: 4h
      validation: automated-tests

    - name: full
      percentage: 100
      approval: required
```

## Best Practices

### 1. Comprehensive Testing
- Multi-package test coordination
- Integration test validation
- Performance regression detection
- Security vulnerability scanning

### 2. Documentation Management
- Automated changelog generation
- Release notes with detailed changes
- Migration guides for breaking changes
- API documentation updates

### 3. Deployment Coordination
- Staged deployment with validation
- Rollback mechanisms and procedures
- Performance monitoring during deployment
- User communication and notifications

### 4. Version Management
- Semantic versioning compliance
- Cross-package version coordination
- Dependency compatibility validation
- Breaking change documentation

## Monitoring and Metrics

### Release Quality Metrics
- Test coverage percentage
- Integration success rate
- Deployment time metrics
- Rollback frequency

### Automated Monitoring
- Performance regression detection
- Error rate monitoring
- User adoption metrics
- Feedback collection and analysis

---

## Version History

- **1.0.0** (2025-01-02): Initial release - converted from release-manager and release-swarm agents