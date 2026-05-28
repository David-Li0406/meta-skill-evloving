# Ralph Eats Beads

![Ralph Eats Beads](ralph-eats-beads.jpg)

"[Ralph Wiggum](https://ghuntley.com/ralph/)" autonomous AI coding loop, using [bd (beads)](https://github.com/steveyegge/beads) for task management with parallel tmux subagents.

Ralph ships features while you sleep, by eating all of the beads. 

For those in the know, you can think of Ralph Eats Beads as "Gas Town Lite". I find it much more powerful than a "vanilla Ralph" loop, yet much faster to start and easier to wield than [Gas Town](https://github.com/steveyegge/gastown).

## Installation

### Claude Code (Interactive)

```
/plugin marketplace add rawwerks/ralph-eats-beads
/plugin install ralph-eats-beads@ralph-eats-beads
```

### Claude CLI

```bash
claude plugin marketplace add rawwerks/ralph-eats-beads
claude plugin install ralph-eats-beads@ralph-eats-beads
```

## What It Does

The "parent" Ralph/Claude picks issues from `bd ready`, spawns parallel Ralph/Claude subagents in tmux windows to implement them, and closes issues on success. Each iteration:

1. Parent agent checks `bd ready` for available work
2. Spawns 3-5 subagent tmux windows (one per issue)
3. Each subagent implements ONE issue, commits, closes it
4. Watchdog monitors for stuck agents and nudges/kills them
5. Loop repeats until no work remains or max iterations hit

```
ralph (tmux session)
├── parent (window 0) - orchestrator
├── watchdog (window 1) - health monitor  
├── issue-1 (window 2) - subagent
├── issue-2 (window 3) - subagent
└── issue-3 (window 4) - subagent
```

## Prerequisites

- **[bd (beads)](https://github.com/steveyegge/beads)** - Issue tracker (beads)
- **tmux** - Terminal multiplexer
- **claude** - Claude CLI with `--dangerously-skip-permissions`

## Quick Start

```bash
# 1. Create issues to work on
bd create --type epic "Feature: User Auth"
bd create "Add login form" --parent <epic-id>
bd create "Add validation" --parent <epic-id>

# 2. Start Ralph (default: 10 iterations max)
./scripts/ralph.sh

# 3. Or specify max iterations
./scripts/ralph.sh 25

# 4. Watch progress
tmux attach -t ralph-<project>
```

## How Iterations Work

- **Max iterations** = how many times the parent can spawn a batch of subagents
- Each iteration handles multiple issues in parallel (3-5 concurrent)
- Loop exits early if `bd ready` returns no work
- Default timeout: 1 hour per iteration

## On Failure

- Subagent adds comment: `bd comments add <id> "Blocked: <reason>"`
- Issue stays open for next iteration or manual fix
- Watchdog kills stuck windows after 2 nudge attempts

## Planning: Converting Requirements to Issues

In a typical "Ralph eats beads" workflow, you would have already converted your plan into bd epics, issues, dependencies, and notes before running `ralph.sh`. This is the recommended approach: carefully curate the plan, collaborate with Claude/Codex/etc to convert to bd and make sure that the agent does not miss any details. I often find it helpful to ask Claude to spin up an "auditor" subagent to check that every aspect of the plan was converted to bd. I also include in my CLAUDE.md: `When exiting Plan Mode, all plans must be fully converted into bd epics, issues, dependencies, and notes`.

However, if you haven't done that step yet, you can use the **planner script** to generate bd issues from a requirements file:

```bash
# From a requirements file
./scripts/planner.sh requirements.md

# From inline text
./scripts/planner.sh <<< "Add OAuth2 authentication with Google and GitHub"

# From a pipe
cat feature-spec.md | ./scripts/planner.sh
```

The planner runs a recursive loop that:
1. Reads your requirements
2. Creates an epic and stories in bd
3. Sets up dependencies between issues
4. Iterates until the plan fully covers the requirements

Once planning is complete, run `ralph.sh` to implement.

## Files

| File | Purpose |
|------|---------|
| `scripts/ralph.sh` | Main entry point |
| `scripts/planner.sh` | Generate issues from requirements |
| `scripts/watchdog.sh` | Health monitor |
| `SKILL.md` | Full agent instructions |

## License

MIT
