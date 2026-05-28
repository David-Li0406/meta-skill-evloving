---
name: mounted
description: Use this skill to report which CCB providers are mounted, indicating that a session exists and the daemon is online, with output in JSON format.
---

# Mounted Providers

Reports which CCB providers are considered "mounted" for the current project.

## Definition

`mounted = has_session && daemon_on`

## Execution

```bash
ccb-mounted
```