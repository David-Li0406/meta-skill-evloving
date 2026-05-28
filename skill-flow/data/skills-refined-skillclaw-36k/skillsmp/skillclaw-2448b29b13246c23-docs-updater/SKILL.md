---
name: docs-updater
description: Use this skill when you need to keep documentation synchronized with code changes, such as updating API docs, maintaining architecture diagrams, or generating documentation from code.
---

# Docs Updater

Keep documentation in sync with code. This skill generates concise, user-friendly summaries and ensures that all relevant documentation is updated according to code changes.

## Context Files (Read First)

For current state, read from `Docs/context/`:
- `Docs/context/conventions.md` - Documentation standards
- `Docs/context/repo-structure.md` - File organization
- `Docs/ai/CHANGELOG.md` - Recent changes to sync

## Quick Summary Format

Every document should start with a **TL;DR section** for human readers:

```markdown
# Document Title

> **TL;DR:** [1-2 sentence summary of what this covers]
>
> **Key Points:**
> - [Most important fact 1]
> - [Most important fact 2]
> - [Most important fact 3]
>
> **Quick Links:** [Table](#tables) | [RPC](#rpc-functions) | [Edge Functions](#edge-functions)
```

## Documentation Files

| File | Purpose | Update Trigger |
|------|---------|----------------|
| `CLAUDE.MD` | AI context | Major architecture changes |
| `README.md` | Project overview | Feature/setup changes |
| `Docs/01-PRD.md` | Requirements | Vision changes |
| `Docs/02-DESIGN.md` | Architecture | System design changes |
| `Docs/03-API.md` | API contracts | DB/RPC/Edge changes |
| `Docs/04-DEV-WORKFLOW.md` | Development process | Workflow or CI/CD changes |
| `Docs/05-DEV.md` | Bible lookups | RPC function changes |
| `Docs/06-AI-ARCHITECTURE.md` | AI system | AI feature changes |
| `Docs/07-ADMIN-GUIDE.md` | Admin panel | Admin changes |
| `Docs/08-WIDGET.md` | Widget docs | Widget API or features changes |
| `Docs/13-SUBSCRIPTION-SYSTEM.md` | Plans/quotas | Subscription changes |

## Cron/Scheduled Invocation

This skill supports automated execution for documentation audits.

### Invocation Modes

**Manual:** `claude /docs-updater "check api docs are current"`

**Scheduled (cron):** Set up with CI/CD or cron job:
```bash
# Weekly docs audit (Sundays at midnight)
0 0 * * 0 claude --skill docs-updater --task "audit" --output report.md

# Pre-release docs check
claude --skill docs-updater --task "release-check" --output docs-status.md
```

### Supported Tasks

| Task | Description | Output |
|------|-------------|--------|
| `audit` | Check all docs for staleness | Markdown report |
| `release-check` | Pre-release documentation verification | Pass/fail + issues |
| `sync-schemas` | Update docs from database schema | Updated doc files |
| `generate-api` | Generate API docs from Edge Functions | API documentation |

### Audit Report Format

```markdown
# Audit Report
- [List of documents checked]
- [Summary of findings]
```