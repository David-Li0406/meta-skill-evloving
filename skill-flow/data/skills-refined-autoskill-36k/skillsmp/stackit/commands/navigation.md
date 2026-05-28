# Navigation Commands

Commands for moving through your stack and viewing stack state.

> **CRITICAL:** Always run these commands with `command stackit ... --no-interactive`.

## Core Navigation

| Command | Description |
|---------|-------------|
| `command stackit log --no-interactive` | Display the branch tree visualization |
| `command stackit log full --no-interactive` | Show tree with GitHub PR status and CI checks |
| `command stackit checkout [branch] --no-interactive` | Switch to a specific branch |

## Movement Commands

| Command | Description |
|---------|-------------|
| `command stackit up --no-interactive` | Move to the child branch |
| `command stackit down --no-interactive` | Move to the parent branch |
| `command stackit top --no-interactive` | Move to the top of the stack |
| `command stackit bottom --no-interactive` | Move to the bottom of the stack |
| `command stackit trunk --no-interactive` | Return to the main/trunk branch |

## Information Commands

| Command | Description |
|---------|-------------|
| `command stackit children` | Show children of current branch |
| `command stackit parent` | Show parent of current branch |
| `command stackit info --no-interactive` | Show detailed branch info |

## Quick Tips

- Always run `command stackit log --no-interactive` first to understand your position
- Use `command stackit checkout <branch> --no-interactive` to switch to a specific branch
- `command stackit log full --no-interactive` shows PR status - useful before submitting
