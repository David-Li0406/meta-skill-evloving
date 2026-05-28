---
name: update-helm-index
description: Automate Helm Chart repository index updates. Package charts, update index.yaml, verify integrity, create Git commits. Use when user mentions 'helm index', 'update index', 'publish chart', 'update artifact hub', or 'tgz package'.
---

# Update Helm Index

## Quick Start

### Use Automation Scripts (Recommended)

```bash
# Preview mode (recommended for first use)
bash .claude/skills/update-helm-index/scripts/update-index.sh --dry-run

# Execute update
bash .claude/skills/update-helm-index/scripts/update-index.sh

# Auto-push to remote
bash .claude/skills/update-helm-index/scripts/update-index.sh --auto-push
```

See [scripts/README.md](scripts/README.md) for details.

---

## MCP Tool Integration

### serena - Codebase Analysis

Use serena to analyze Chart structure before updating:

```bash
# List charts/ directory
mcp__serena__list_dir --relative_path "charts" --recursive false

# Find Chart.yaml versions
mcp__serena__find_symbol --name_path_pattern "Chart.yaml" --relative_path "charts"

# Search for existing .tgz files
mcp__serena__search_for_pattern --substring_pattern "\.tgz$" --relative_path "." --restrict_search_to_code_files false
```

### context7 - Latest Documentation

Query Helm latest usage:

```bash
# Resolve Helm library ID
mcp__plugin_context7_context7__resolve-library-id --libraryName "helm" --query "helm package command"

# Query documentation
mcp__plugin_context7_context7__query-docs --libraryId "/helm/helm" --query "How to package a chart and update repository index?"
```

### sequential thinking - Complex Decisions

Use when encountering issues:

- Plan multi-chart update strategy
- Diagnose index update failures
- Analyze version conflicts

### Remote Index Check

Compare local and published versions:

```bash
# Fetch remote index.yaml
curl -s https://helm-chart.anubis.cafe/index.yaml -o /tmp/remote-index.yaml

# Compare with local index
diff -u index.yaml /tmp/remote-index.yaml

# Check specific chart versions
yq '.charts.booklore[].version' /tmp/remote-index.yaml
```

---

## Update Workflow

Copy this checklist and track progress:

```markdown
Task Progress:
- [ ] 1. Environment Check
  - Run `bash scripts/check-env.sh`
  - Verify Helm, Git, directory permissions
- [ ] 2. Analyze Chart State
  - Use serena to find updated Chart.yaml
  - Check existing .tgz files
  - Compare with remote index.yaml
- [ ] 3. Package Charts
  - Run `helm package charts/*`
  - Verify generated .tgz files
- [ ] 4. Update Index
  - Run `helm repo index . --url https://helm-chart.anubis.cafe`
  - Verify index.yaml syntax
- [ ] 5. Verify Results
  - Run `bash scripts/health-check.sh`
  - Confirm digest correctness
  - Compare with remote index
- [ ] 6. Git Commit
  - Add *.tgz and index.yaml
  - Create clear commit message
```

---

## When to Use

Trigger keywords:
- "update helm index"
- "publish new chart version"
- "update helm index"
- "package chart"
- "publish to artifact hub"
- "update tgz package"

---

## Detailed Documentation

- [workflows.md](workflows.md) - Complete 6-step workflow, scenarios
- [troubleshooting.md](troubleshooting.md) - Troubleshooting, verification commands
- [MCP-GUIDE.md](MCP-GUIDE.md) - Detailed MCP tool usage guide

---

## Remember

- Update index for every new release
- Index file must match actual .tgz packages
- Use clear Git commit messages
- Verify results before pushing
- Artifact Hub syncs automatically
- Check remote index before publishing to avoid conflicts
