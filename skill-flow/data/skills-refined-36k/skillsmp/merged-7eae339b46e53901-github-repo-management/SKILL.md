---
name: github-repo-management
description: Use this skill for optimizing repository structures, managing multi-repo workflows, and orchestrating cross-repository synchronization and automation.
---

# GitHub Repository Management Skill

## Overview

This skill focuses on repository structure optimization and multi-repo management through swarm coordination. It handles repository structure analysis, template management, cross-repository synchronization, architecture recommendations, and development workflow optimization.

## Quick Start

```bash
# List organization repositories
gh repo list org --limit 100 --json name,description,languages

# Create a new repository
gh repo create my-new-repo --public --description "Description"

# Clone multiple repositories
for repo in repo1 repo2 repo3; do
  gh repo clone org/$repo
done

# View repository info
gh repo view owner/repo --json name,description,topics
```

## When to Use

- Analyzing and optimizing repository structures
- Creating standardized project templates
- Coordinating changes across multiple repositories
- Cross-repository synchronization and dependency management
- Architecture analysis and recommendations

## Core Capabilities

| Capability | Description |
|------------|-------------|
| Structure optimization | Implement best practices for repository organization |
| Multi-repo coordination | Synchronize operations and manage dependencies across repositories |
| Template management | Create and maintain consistent project templates |
| Architecture analysis | Provide recommendations for scalable and maintainable structures |
| Workflow coordination | Optimize development processes across multiple repositories |

## Usage Examples

### 1. Repository Structure Analysis

```javascript
// Initialize architecture analysis swarm
mcp__claude-flow__swarm_init({ topology: "mesh", maxAgents: 4 })
mcp__claude-flow__agent_spawn({ type: "analyst", name: "Structure Analyzer" })
mcp__claude-flow__agent_spawn({ type: "architect", name: "Repository Architect" })
mcp__claude-flow__agent_spawn({ type: "optimizer", name: "Structure Optimizer" })
mcp__claude-flow__agent_spawn({ type: "coordinator", name: "Multi-Repo Coordinator" })

// Orchestrate structure optimization
mcp__claude-flow__task_orchestrate({
    task: "Analyze and optimize repository structure for scalability and maintainability",
    strategy: "adaptive",
    priority: "medium"
})
```

### 2. Cross-Repository Synchronization

```bash
# List organization repositories
REPOS=$(gh repo list org --limit 100 --json name --jq '.[].name')

# Update common files across repositories
for repo in $REPOS; do
  echo "Updating $repo..."

  # Clone repo
  gh repo clone org/$repo /tmp/$repo -- --depth=1

  # Update workflow file
  mkdir -p /tmp/$repo/.github/workflows
  cat > /tmp/$repo/.github/workflows/ci.yml << 'EOF'
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with: { node-version: '20' }
      - run: npm install && npm test
EOF

  # Commit and create PR
  cd /tmp/$repo
  git checkout -b standardize-ci
  git add .github/workflows/ci.yml
  git commit -m "ci: Standardize CI workflow"
  git push origin standardize-ci
  gh pr create --title "ci: Standardize CI workflow" --body "Organization-wide standardization"

  cd -
  rm -rf /tmp/$repo
done
```

### 3. Create Repository Template

```bash
# Create template repository
gh repo create claude-project-template \
  --public \
  --description "Standardized template for Claude Code projects" \
  --template

# Clone and setup structure
gh repo clone owner/claude-project-template
cd claude-project-template

# Create directory structure
mkdir -p .claude/commands/{github,sparc,swarm}
mkdir -p src tests docs config

# Create core files
cat > package.json << 'EOF'
{
  "name": "claude-project-template",
  "version": "1.0.0",
  "description": "Claude Code project with ruv-swarm integration",
  "engines": { "node": ">=20.0.0" },
  "dependencies": {
    "ruv-swarm": "^1.0.11"
  }
}
EOF

cat > CLAUDE.md << 'EOF'
# Claude Code Configuration

## Quick Start
```bash
npx claude-flow init --sparc
npm install
npx claude-flow start --ui
```

## Features
- ruv-swarm integration
- SPARC development modes
- GitHub workflow automation
EOF

# Commit and push
git add -A
git commit -m "feat: Create standardized project template"
git push
```

### 4. Synchronized Dependency Update

```bash
# Create tracking issue
TRACKING_ISSUE=$(gh issue create \
  --repo org/main-repo \
  --title "Dependency Update: typescript@5.0.0" \
  --body "Tracking issue for updating TypeScript across all repositories" \
  --label "dependencies,tracking" \
  --json number -q .number)

# Get all repos with TypeScript
TS_REPOS=$(gh repo list org --limit 100 --json name | jq -r '.[].name' | \
  while read -r repo; do
    if gh api repos/org/$repo/contents/package.json 2>/dev/null | \
       jq -r '.content' | base64 -d | grep -q '"typescript"'; then
      echo "$repo"
    fi
  done)

# Update each repository
echo "$TS_REPOS" | while read -r repo; do
  gh repo clone org/$repo /tmp/$repo -- --depth=1
  cd /tmp/$repo

  npm install --save-dev typescript@5.0.0

  if npm test; then
    git checkout -b update-typescript-5
    git add package.json package-lock.json
    git commit -m "chore: Update TypeScript to 5.0.0

Part of #$TRACKING_ISSUE"

    git push origin HEAD
    gh pr create \
      --title "Update TypeScript to 5.0.0" \
      --body "Updates TypeScript to version 5.0.0

Tracking: #$TRACKING_ISSUE" \
      --label "dependencies"
  else
    gh issue comment $TRACKING_ISSUE \
      --body "Failed to update $repo - tests failing"
  fi
  cd -
  rm -rf /tmp/$repo
done
```

## Best Practices

### 1. Structure Optimization
- Consistent directory organization across repositories
- Standardized configuration files and formats
- Clear separation of concerns and responsibilities
- Scalable architecture for future growth

### 2. Template Management
- Reusable project templates for consistency
- Standardized issue and PR templates
- Workflow templates for common operations
- Documentation templates for clarity

### 3. Multi-Repository Coordination
- Cross-repository dependency management
- Synchronized version and release management
- Consistent coding standards and practices
- Automated cross-repo validation

### 4. Documentation Architecture
- Comprehensive architecture documentation
- Clear integration guides and examples
- Maintainable and up-to-date documentation
- User-friendly onboarding materials

## Monitoring and Analysis

### Architecture Health Metrics
- Repository structure consistency score
- Documentation coverage percentage
- Cross-repository integration success rate
- Template adoption and usage statistics

### Automated Analysis
- Structure drift detection
- Best practices compliance checking
- Performance impact analysis
- Scalability assessment and recommendations

---

## Version History

- **1.0.0** (2025-01-02): Initial release - merged from github-multi-repo and github-repo-architect skills.