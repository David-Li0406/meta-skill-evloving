---
name: workbench-docs
description: Use this skill when creating or updating specs, ADRs, runbooks, guides, or general documentation, and when syncing backlinks or change notes with the Workbench CLI.
---

## Key settings

- `.workbench/config.json`: paths.docsRoot, paths.templatesDir, ids.width, prefixes, git.defaultBaseBranch, github.owner, github.repository.
- Use `workbench config show --format json` to verify effective settings.

## Core workflows

1. Planning phase: create specs and architecture docs before major changes.
2. Doing phase: keep docs updated as implementation decisions change.
3. Keep doc front matter and backlinks in sync.
4. Summarize doc changes when publishing.

## Commands

Create a doc:
```bash
workbench doc new --type doc --title "<title>" --path <path> --work-item <work_item>
```

Create a spec:
```bash
workbench doc new --type spec --title "<title>" --path <path> --work-item <work_item>
```

Create an architecture doc:
```bash
workbench doc new --type doc --title "System design" --path <path> --work-item <work_item>
```

Create an ADR:
```bash
workbench doc new --type adr --title "<decision>" --path <path> --work-item <work_item>
```

Link a doc to work items:
```bash
workbench doc link --type spec --path <path> --work-item <work_item>
```

Unlink a doc from work items:
```bash
workbench doc unlink --type adr --path <path> --work-item <work_item>
```

Sync front matter and backlinks:
```bash
workbench doc sync --all --dry-run
workbench doc sync --all
```

Summarize doc changes:
```bash
workbench doc summarize --staged --update-index
```

## Output

- Markdown docs with Workbench front matter and backlinks.
- Updated work item references in docs and work items.

## Guardrails

- Keep doc types aligned with folder intent (product, architecture, decisions, runbooks).
- Always link docs to relevant work items with `--work-item` or `workbench item link`.
- For major changes, write a spec before implementation.
- When decisions change, update or create the ADR.
- Prefer `workbench doc` commands; `workbench spec` and `workbench adr` are deprecated.