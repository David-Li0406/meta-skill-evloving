---
name: workbench-work-items
description: Use this skill for managing work items in the Workbench CLI, including creating, updating, linking, and closing items while tracking their execution status.
---

## Key settings

- `.workbench/config.json`: paths.itemsDir, paths.doneDir, ids.width, prefixes, git.branchPattern.
- Status values: draft, ready, in-progress, blocked, done, dropped.

## Core workflows

1. Ensure planning artifacts exist (specs, ADRs, architecture docs) before major work.
2. Create a work item and set its initial status.
3. Link related specs, ADRs, files, PRs, or issues.
4. Update status and close work items when done.

## Commands

Create a task:
```bash
workbench item new --type task --title "<task_title>" --status draft --priority medium --owner <owner>
```

Update status:
```bash
workbench item status <task_id> <new_status> --note "<status_update_note>"
```

Close and move to done:
```bash
workbench item close <task_id> --move
```

Link docs or PRs:
```bash
workbench item link <task_id> --spec <spec_path> --adr <adr_path> --pr <pull_request_url>
```

## Output

- Work items in `<items_directory>` (active) and `<done_directory>` (closed).
- Linked docs and external artifacts tracked in front matter.

## Guardrails

- Use a work item for every meaningful change and link the supporting docs.
- Keep status accurate so reports and boards stay reliable.
- If a decision happens during work, update/create the ADR and link it.