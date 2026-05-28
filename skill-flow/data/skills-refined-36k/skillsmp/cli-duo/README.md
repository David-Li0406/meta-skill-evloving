# CLI Duo

Coordinate two AI CLIs working in the same repository without stepping on each other.

## Features

- Register local AI CLIs (command, default repo, notes)
- Create collaboration sessions with two modes:
  - **subordinate**: spawn a secondary git worktree so the second CLI can work safely
  - **engineer-judge**: assign engineer/judge roles and swap them per round
- Swap roles, inspect sessions, and clean up worktrees

## Quickstart

```bash
# Register two CLIs
duo cli register -n claude -c "claude" -d "Claude local CLI"
duo cli register -n cursor -c "cursor" -d "Cursor CLI"

# Create subordinate session with a safe worktree
duo pair create -s landing-refactor -p claude -b cursor -m subordinate -r ~/projects/app --confirm

# Engineer/Judge collaboration
duo pair create -s review-loop -p claude -b cursor -m engineer-judge -R 2
duo pair swap -s review-loop  # Swap roles after each round
```

## Commands (high level)

- `duo cli register|list|remove` – manage known CLIs
- `duo pair create|list|info|swap|end` – manage collaboration sessions

See `SKILL.md` for assistant-facing usage and `duo --help` for full CLI flags.
