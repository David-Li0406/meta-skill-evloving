---
name: truenas-docker-ops
description: Playbook for anything on the TrueNAS host — consult before touching services, data, or containers. Covers SSH entry, container interaction, and data/layout notes so you can operate safely on TrueNAS.
---

# TrueNAS Docker Operations

## Essentials

- Connect: `ssh truenas` (auth pre-configured)
- Stacks managed via Ansible in `ansiblonomicon` repo folder (in `ansible/stacks/`)
- Deployed compose files: `/mnt/performance/docker/stacks/<stack>/compose.yaml`
- Container configs: `/mnt/performance/docker/<stack>/`
- Large media data: `/mnt/capacity/watch/<container>/`
- Network/IP assignments: see individual compose files or `ansible/inventory/group_vars/truenas.yml` in ansiblonomicon

## Common Commands

| Task              | Command                                                               |
| ----------------- | --------------------------------------------------------------------- |
| List containers   | `ssh truenas docker ps`                                               |
| Filter containers | `ssh truenas docker ps \| grep <name>`                                |
| View compose      | `ssh truenas cat /mnt/performance/docker/stacks/<stack>/compose.yaml` |
| View logs         | `ssh truenas docker logs <container>`                                 |
| Exec command      | `ssh truenas docker exec -i <container> <command>`                    |
| Inspect           | `ssh truenas docker inspect <container>`                              |

## Deployment

Stacks are deployed via Ansible, not manually:

```bash
# From ansiblonomicon repo
poe truenas           # Full playbook
poe truenas -t stacks # Just stacks
```

but you can run ad-hoc commands against the docker containers/compose files on the truenas host. Changes will not be preserved unless they are made to the ansiblonomicon repo.

## Anypod Data Layout

- Host data root: `/mnt/capacity/watch/anypod/data` (binds to `/data` in container)
  - Media downloads: `media/<feed_id>/`
  - Transcripts: `transcripts/<feed_id>/`
  - DB: `/data/db/anypod.db`
- DB tables (anypod.db):
  - `feed` (PK `id`; feed metadata, source info, timestamps, counters)
  - `download` (PK `feed_id`, `id`; per-episode info, status, transcript fields)
  - `appstate` (PK `id`; `last_yt_dlp_update`, other global state)

## Helper Scripts

### Python (handles nested heredoc/quoting)

`scripts/docker_exec_python.sh <container> '<python_code>'`

```bash
scripts/docker_exec_python.sh anypod '
import sqlite3, json
conn = sqlite3.connect("/data/db/anypod.db")
conn.row_factory = sqlite3.Row
rows = conn.execute("SELECT * FROM feed").fetchall()
print(json.dumps([dict(r) for r in rows], indent=2))
conn.close()
'
```

> **Note**: Default interpreter is `/app/.venv/bin/python` (works for anypod). Override with `CONTAINER_PYTHON`:
>
> ```bash
> CONTAINER_PYTHON=/usr/bin/python3 scripts/docker_exec_python.sh your-container 'print("hi")'
> ```

### SQLite

`scripts/docker_exec_sqlite.sh <container> <db_path> '<sql_query>'`

```bash
scripts/docker_exec_sqlite.sh anypod /data/db/anypod.db '
SELECT feed_id, status, COUNT(*) AS count
FROM download
GROUP BY feed_id, status;
'
```

## When to Use Scripts vs Direct

- **Scripts**: Multi-line Python/SQL, complex quoting
- **Direct `docker exec`**: Simple commands, logs, inspection

## Quick Examples

```bash
# Is anypod running?
ssh truenas docker ps | grep anypod

# View anypod compose
ssh truenas cat /mnt/performance/docker/stacks/anypod/compose.yaml

# Query anypod DB
scripts/docker_exec_sqlite.sh anypod /data/db/anypod.db "SELECT * FROM feed;"
```
