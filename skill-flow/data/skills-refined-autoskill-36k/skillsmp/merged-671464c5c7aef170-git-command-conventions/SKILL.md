---
name: git-command-conventions
description: Use this skill when running any git commands to avoid blocking on interactive pager.
---

# Git Commands

Always use `--no-pager` BEFORE the git command to avoid blocking on interactive pager:

```bash
git --no-pager <subcommand>
```

The `--no-pager` flag must come **before** the subcommand (e.g., log, diff, show), not after.