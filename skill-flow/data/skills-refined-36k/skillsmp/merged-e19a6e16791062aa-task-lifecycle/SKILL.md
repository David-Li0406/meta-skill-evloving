---
name: task-lifecycle
description: Use this skill when managing tasks in the repository with GitHub workflows and maintaining PR hygiene.
---

## Start a task

1) Run GitHub Actions workflow **Start Task**.
2) Merge the PR.
3) In Windsurf, run `/plan-task` for the created task folder (it consumes `brief.md` and turns it into an executable `plan.md`).

Optional (no GitHub UI clicks): dispatch Start Task locally:

```bash
python .github/scripts/dispatch_workflow.py --workflow start-task.yml --ref main --input task_id=<task_id> --input title="<task_title>" --input auto_merge=true --input delete_branch=false
```

## Finish a task

1) Merge the task’s implementation PR(s).
2) Run GitHub Actions workflow **Finish Task**.
3) Merge the PR.

Optional (no GitHub UI clicks): dispatch Finish Task locally:

```bash
python .github/scripts/dispatch_workflow.py --workflow finish-task.yml --ref main --input task_id=<task_id> --input auto_merge=true
```

## Conventions

- Canonical task index: `orga/tasks/TASKS.md`
- Active tasks: `orga/tasks/active/`
- Archived tasks: `orga/tasks/archive/`
- Canonical planner-to-task briefs: `orga/domain/task-briefs/` (copied into each task folder as `brief.md`)

See `docs/task-workflow.md` for details.