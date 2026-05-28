---
name: ralph-wiggum-loop
description: The Ralph Wiggum technique for autonomous AI development loops. Use when the user wants to run an agent in a loop for greenfield projects, reverse engineering, code migrations, large refactors, overnight batch work, or any task requiring persistent iteration until completion. Triggers include "ralph loop", "gumloop", "run ralph", "autonomous loop", "overnight coding", "while loop agent", "iterative development", "let it ralph", "run until done", "agentic loop", "context rotation", or when users want to set up autonomous coding that runs unattended. This skill implements Geoffrey Huntley's original philosophy: a simple bash loop with context engineering, not complex multi-agent orchestration.
---

# The Ralph Wiggum Loop

> "Ralph is a Bash loop." — Geoffrey Huntley

## The Core Insight: Context Rotation

LLM context windows are like memory with `malloc()` but no `free()`.

As an agent works, context fills:
```
Start:        [PROMPT]
Read files:   [PROMPT][file1][file2][file3]
Tool calls:   [PROMPT][file1][file2][file3][results][more_results]
Errors:       [PROMPT][file1][file2][file3][results][more_results][stack_trace]
Eventually:   [PROMPT][file1][file2][...everything...][gutter]
```

When context fills with stale information, the agent enters the **"gutter"** — poor decisions because critical information is buried. There's no way to selectively free context.

**The solution: loop termination IS the `free()`.**

```
Iteration 1: Fresh context → work → commit → EXIT (freed)
Iteration 2: Fresh context → work → commit → EXIT (freed)
Iteration 3: Fresh context → work → commit → EXIT (freed)
```

Each iteration:
1. Starts with **zero memory** from previous iteration
2. Loads only the prompt (small, deterministic)
3. Reads current state from **disk** (git, files)
4. Does **ONE task**
5. Commits progress
6. Exits → context garbage collected

**Progress persists in files and git, not in context.**

## The CLI: gumloop

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/adriancodes/gumloop/main/install.sh | bash

# Use
gumloop --choo-choo 20
```

### Commands

```bash
gumloop -p "Fix the tests"              # Run once with inline prompt
gumloop --choo-choo                     # Loop until no changes
gumloop --choo-choo 20                  # Loop, max 20 iterations
gumloop --prompt-file PROMPT_plan.md    # Use prompt file
gumloop --stuck-threshold 5             # Exit after 5 iterations without commits
gumloop --verify "npm test"             # Run tests after each iteration
gumloop --init                          # Create PROMPT.md template
gumloop --recover                       # Discard uncommitted changes
gumloop --update                        # Update to latest version
gumloop --uninstall                     # Remove gumloop
```

### Supported Agents

```bash
gumloop --cli claude                    # Claude Code (default)
gumloop --cli codex                     # OpenAI Codex
gumloop --cli gemini                    # Google Gemini
gumloop --cli opencode                  # OpenCode
gumloop --cli amp                       # Sourcegraph Amp
gumloop --cli aider                     # Aider
```

### Loop Behavior

- Without `--choo-choo`: runs once and exits
- With `--choo-choo`: loops until no git changes detected
- Stuck detection: exits after N iterations with changes but no commits
- Ctrl+C to exit cleanly at any time

## Why One Task Per Loop

Multiple tasks = context accumulation = gutter state.

One task = fresh context = sharp reasoning = atomic commits.

Your prompt should say "pick the most important task" not "do all tasks."

## The Philosophy

### Deterministically Bad

> "That's the beauty of Ralph - the technique is deterministically bad in an undeterministic world."

Ralph will fail. Failures are predictable and fixable. Better than succeeding unpredictably.

### Eventual Consistency

If the agent keeps correcting itself, it will eventually converge. Each iteration sees results of previous iterations through git and files.

### LLMs Are Mirrors

Success depends on writing good prompts. Quality of output reflects quality of input.

### Monolithic

Single process, single repository, one task per loop. NOT multi-agent orchestration or loops within loops.

## Tuning: The Playground Metaphor

> "Ralph is given instructions to construct a playground. Ralph comes home bruised because he fell off the slide, so you add a sign: 'SLIDE DOWN, DON'T JUMP.' Eventually all Ralph thinks about is the signs — that's a tuned prompt."

Start minimal. Observe failures. Add specific guardrails.

## Minimal Setup

```bash
mkdir project && cd project
git init

# Run once
gumloop -p "What does this codebase do?"

# Loop until done
gumloop -p "Fix all failing tests" --choo-choo
```

## Safety

**Built-in checks:**
- Refuses dangerous directories
- Requires git repository
- Warns before choo-choo mode in home subdirectories

**Git is your safety net:**
```bash
git reset --hard   # Instant recovery
```

**For true isolation:** E2B, Fly Sprites, Modal, dedicated VM.

## When to Use

**Good for:** Greenfield, reverse engineering, refactors, migrations, test coverage, documentation, overnight work.

**Not ideal for:** Judgment-heavy work, unclear completion criteria, highly exploratory research.

## References

- `references/context-engineering.md` — Why the loop works
- `references/workflow-patterns.md` — Two-mode, specs directories
- `references/prompt-templates.md` — Starter prompts
- `references/tuning-guide.md` — Guardrail patterns
- `references/safety.md` — Safety considerations
