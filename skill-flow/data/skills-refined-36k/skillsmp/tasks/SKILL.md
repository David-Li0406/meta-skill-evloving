---
name: tasks
description: Open the tasks database in DB Browser for SQLite GUI
allowed-tools: Bash
---

# Tasks Skill

Opens the local `tasks.db` SQLite database in DB Browser for SQLite for visual browsing and querying.

## Usage

When this skill is invoked, run:

```bash
open -a "DB Browser for SQLite" /Users/mattgioe/aiq/tasks.db
```

Then confirm to the user that the database has been opened in DB Browser for SQLite.

## Quick Stats

Before opening, show a quick summary:

```bash
sqlite3 /Users/mattgioe/aiq/tasks.db "SELECT status, COUNT(*) as count FROM tasks GROUP BY status ORDER BY count DESC"
```
