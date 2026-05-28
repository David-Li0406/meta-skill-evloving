---
name: mastering-github-cli
description: Use this skill when you need to perform GitHub operations via the command line, including repository searches, CI/CD monitoring, and workflow automation.
---

# Mastering GitHub CLI

Command-line interface for GitHub operations: search, monitoring, resource creation, workflow authoring, and automation.

## Contents

- [Quick Start](#quick-start)
- [Command Reference](#command-reference)
- [Workflow Authoring](#workflow-authoring)
- [Scripts](#scripts)
- [Validation Checklist](#validation-checklist)
- [When Not to Use](#when-not-to-use)

---

## Quick Start

### Find repos with specific files/directories

```bash
gh search code "path:.skilz" --json repository --jq '.[].repository.fullName'
gh search code --filename SKILL.md
gh search code --filename Dockerfile --language python
```

### Monitor CI/CD

```bash
gh run list --workflow=CI --status=failure --limit 10
gh run watch 12345 --exit-status      # Block until complete
gh run view 12345 --log-failed        # Failed logs only
gh pr checks 123 --watch              # PR CI status
```

### Create resources

```bash
gh pr create --title "Feature" --body "Description" --reviewer @user
gh issue create --title "Bug" --label bug,urgent --assignee @me
gh repo fork owner/repo --clone
```

### Trigger and monitor workflow

```bash
gh workflow run deploy.yml -f environment=staging
sleep 5
RUN_ID=$(gh run list --workflow=deploy.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$RUN_ID" --exit-status
```

---

## Command Reference

| Task | Command | Reference |
|------|---------|-----------|
| Find repos with file | `gh search code --filename FILE` | [search.md](references/search.md) |
| Find repos with directory | `gh search code "path:DIR"` | [search.md](references/search.md) |
| List failed runs | `gh run list --status=failure` | [monitoring.md](references/monitoring.md) |
| Watch run | `gh run watch RUN_ID` | [monitoring.md](references/monitoring.md) |