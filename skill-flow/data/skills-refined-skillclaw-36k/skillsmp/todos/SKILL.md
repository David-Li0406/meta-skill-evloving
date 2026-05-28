---
name: todos
description: Manage tasks, creating, updating, listing, closing.
---

# Weekly Todo

Manage a lightweight, repo-local todo list stored under `.todos/` using the `todo.py` helper.
Use this skill when asked to add, close, list, or inspect todo items.

## Quick Start

1. Initialize in the repo (creates `.todos/` and configures merge driver):

   ```
   python <path-to-skill>/scripts/todo.py init
   ```

2. Create a new todo (prints the id):

   ```
   python <path-to-skill>/scripts/todo.py new "my task title"
   ```

3. List open items:

   ```
   python <path-to-skill>/scripts/todo.py list
   ```

## Scripts

Helper scripts live in `scripts/`:

- `scripts/todo.py` is the only entrypoint.

Common usage:

```
python <path-to-skill>/scripts/todo.py init # create .todos/ + git merge driver
python <path-to-skill>/scripts/todo.py new "title" # add a new task
python <path-to-skill>/scripts/todo.py summary td-1a2b3c4d "short summary" # add a brief summary
python <path-to-skill>/scripts/todo.py dep td-child td-parent # set dependency
python <path-to-skill>/scripts/todo.py list # list open items
python <path-to-skill>/scripts/todo.py list --closed # list closed items
python <path-to-skill>/scripts/todo.py ready # list items with deps satisfied
python <path-to-skill>/scripts/todo.py close td-1a2b3c4d # close an item
```

## Storage Format

- Open items live in `.todos/todos.jsonl` (one compact JSON object per line).
- Closed items move to `.todos/closed.jsonl`.
- Each item has: `id`, `title`, `summary`, `status`, `deps`, `updated_at`.

Example record (JSONL line):

```
{"id":"td-1a2b3c4d","title":"my task title","summary":"","status":"open","deps":[],"updated_at":"2026-01-08T12:34:56Z"}
```

## Notes

- `todo.py init` adds a git merge driver for `.todos/*.jsonl` if run inside a git repo.
- `ready` shows open items whose dependencies are all closed.
