---
name: github-workflow-automation-and-management
description: Use this skill for comprehensive automation and management of GitHub workflows, releases, and code reviews with AI swarm coordination.
---

# GitHub Workflow Automation and Management

## Behavioral Classification

**Type**: Autonomous Execution

This skill automates GitHub workflows, release management, and code reviews with minimal user intervention, utilizing AI swarm coordination for enhanced efficiency.

---

## Overview

This skill encompasses intelligent automation for GitHub actions, release orchestration, and code review processes. It leverages AI swarms to optimize workflows, manage releases, and conduct thorough code reviews.

**Core Capabilities:**
1. **Workflow Automation** - Generates optimized workflows, detects languages, and creates build pipelines.
2. **Release Management** - Orchestrates releases with semantic versioning, automated testing, and deployment strategies.
3. **Code Review** - Executes multi-agent code reviews, enforces quality gates, and generates intelligent comments.

---

## Quick Start

### Workflow Automation

```bash
# Generate optimized workflow from codebase analysis
npx ruv-swarm actions generate-workflow \
  --analyze-codebase \
  --detect-languages \
  --create-optimal-pipeline
```

### Release Management

```bash
# Plan and create a release
gh release create v2.0.0 \
  --draft \
  --generate-notes \
  --title "Release v2.0.0"

# Orchestrate with swarm
npx claude-flow github release-create \
  --version "2.0.0" \
  --build-artifacts \
  --deploy-targets "npm,docker,github"
```

### Code Review

```bash
# Initialize review swarm for PR
gh pr view 123 --json files,diff | npx ruv-swarm github review-init --pr 123

# Post review status
gh pr comment 123 --body "🔍 Multi-agent code review initiated"
```

---

## Sub-Documentation

For detailed information, see the following files:

| Document | Contents |
|----------|----------|
| [Workflow Templates](./templates.md) | Production-ready workflow templates |
| [Swarm Coordination](./swarm.md) | AI swarm orchestration, specialized agents |
| [Quality Gates](./quality-gates.md) | Status checks, thresholds, metrics tracking |
| [Advanced Workflows](./advanced.md) | Multi-package, staged rollout, hotfix procedures |
| [Troubleshooting](./troubleshooting.md) | Common issues and solutions |

---

## Quick Reference

### Essential Commands

```bash
# Get last release tag
LAST_TAG=$(gh release list --limit 1 --json tagName -q '.[0].tagName')

# Create draft release
gh release create v2.0.0 --draft --generate-notes

# Version bump
npm version patch  # or minor, major

# Deploy to npm
npm run build && npm publish
```

### Specialized Review Agents

| Agent | Focus |
|-------|-------|
| **Security** | Vulnerabilities, secrets, auth |
| **Performance** | Complexity, queries, memory |
| **Architecture** | Patterns, coupling, SOLID |
| **Style** | Formatting, naming, docs |
| **Accessibility** | WCAG, screen readers, contrast |

---

## Best Practices

- Define clear review criteria and thresholds for quality gates.
- Optimize workflows for performance and security.
- Utilize swarm coordination for efficient task management.

---

## Related Skills

- `github-release-management` - Release orchestration
- `github-code-review` - Code review automation
- `github-project-management` - Project coordination

---

## Support & Documentation

- **GitHub CLI Docs**: https://cli.github.com/manual/
- **GitHub Actions**: https://docs.github.com/en/actions
- **Claude-Flow**: https://github.com/ruvnet/claude-flow

---

**Last Updated:** 2026-01-24
**Version:** 1.0.0