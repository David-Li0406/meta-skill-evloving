
<p align="center">
  <img src="rwl.png" alt="Ralph Wiggum Loop" width="300">
</p>

# gumloop

**The Ralph Wiggum loop**

Run AI coding agents in autonomous loops until task completion.

Based on [Geoffrey Huntley's methodology](https://ghuntley.com/ralph/) — a simple bash loop with context engineering.

## Why?

LLM context fills up but never clears. As an agent works, stale information accumulates until reasoning degrades.

**The fix:** Kill the agent after each task. Loop handles continuation. Progress lives in git.

```
Iteration 1: Fresh context → work → commit → EXIT (context freed)
Iteration 2: Fresh context → work → commit → EXIT (context freed)
Iteration 3: Fresh context → work → commit → EXIT (context freed)
```

Each iteration starts clean. Progress persists in files and git, not in the agent's memory.

## Requirements

- Bash
- Git
- A coding agent CLI (**installed and authenticated by you**)

### Supported Agents

gumloop wraps these coding agent CLIs. **You must install and authenticate them yourself** — gumloop does not do this for you.

| Agent | Install | Authenticate |
|-------|---------|--------------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | `npm install -g @anthropic-ai/claude-code` | `claude` (follow prompts) |
| [Codex](https://github.com/openai/codex) | `npm install -g @openai/codex` | `export OPENAI_API_KEY=...` |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `npm install -g @google/gemini-cli` | `gemini` (follow prompts) |
| [OpenCode](https://github.com/opencode-ai/opencode) | See repo | See repo |
| [Amp](https://ampcode.com/) | See website | See website |
| [Aider](https://aider.chat/) | `pip install aider-chat` | `export ANTHROPIC_API_KEY=...` |

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/adriancodes/gumloop/main/install.sh | bash
```

Or manually:

```bash
curl -fsSL https://raw.githubusercontent.com/adriancodes/gumloop/main/gumloop -o ~/.local/bin/gumloop
chmod +x ~/.local/bin/gumloop
```

## Quick Start

```bash
# Navigate to your project (must be a git repo)
cd my-project

# Create a prompt template (optional)
gumloop --init

# Run once - ask a question
gumloop -p "What does this codebase do?"

# Run once - make a change
gumloop -p "Add input validation to the login form"

# Loop until done - let it work autonomously
gumloop -p "Fix all failing tests" --choo-choo

# Loop with a cap
gumloop -p "Refactor the API layer" --choo-choo 10

# Loop with verification
gumloop -p "Fix bugs" --choo-choo --verify "npm test"
```

## Usage

### Basic Commands

```bash
gumloop -p "Your prompt here"           # Run once with inline prompt
gumloop --prompt-file PROMPT.md         # Run once with prompt file
gumloop --choo-choo                     # Loop until no changes detected
gumloop --choo-choo 20                  # Loop, max 20 iterations
```

### Options

| Flag | Description |
|------|-------------|
| `-p, --prompt <TEXT>` | Inline prompt text |
| `--prompt-file <FILE>` | Use a prompt file (default: PROMPT.md) |
| `--cli <AGENT>` | Choose agent: claude, codex, gemini, opencode, amp, aider |
| `--choo-choo [N]` | Loop mode, optionally with max iterations |
| `--no-push` | Don't push to remote after iterations |
| `--stuck-threshold <N>` | Exit after N iterations without commits (default: 3) |
| `--verify <CMD>` | Run verification command after each iteration |
| `--init [FILE]` | Create a PROMPT.md template |
| `--recover [N]` | Discard uncommitted changes, or reset last N commits |
| `--update` | Update gumloop to latest version |
| `--uninstall` | Remove gumloop from system |
| `--version` | Show version |
| `--help` | Show help with Ralph ASCII art |

### Choosing an Agent

```bash
gumloop --cli claude -p "Fix the bug"       # Claude Code (default)
gumloop --cli codex -p "Fix the bug"        # OpenAI Codex
gumloop --cli gemini -p "Fix the bug"       # Google Gemini CLI
gumloop --cli opencode -p "Fix the bug"     # OpenCode
gumloop --cli amp -p "Fix the bug"          # Sourcegraph Amp
gumloop --cli aider -p "Fix the bug"        # Aider
```

## Examples

### One-off tasks

```bash
# Explore a codebase
gumloop -p "Explain the architecture of this project"

# Quick fix
gumloop -p "Fix the TypeScript error in src/utils.ts"

# Add a feature
gumloop -p "Add a dark mode toggle to the settings page"

# Write tests
gumloop -p "Write unit tests for the auth module"
```

### Autonomous loops

```bash
# Fix all test failures
gumloop -p "Run tests. Fix the most critical failure. Commit." --choo-choo

# Migrate a codebase
gumloop -p "Convert one JavaScript file to TypeScript. Commit." --choo-choo 50

# Clear tech debt
gumloop -p "Find and fix one TODO comment. Commit." --choo-choo

# Improve test coverage
gumloop -p "Find untested code. Write one test. Commit." --choo-choo 20
```

### Using a prompt file

Create `PROMPT.md`:

```markdown
Study the codebase. Find the most important bug to fix.
Fix it completely. Run tests. Commit with a descriptive message.

Rules:
99999. Search before implementing - don't duplicate existing code.
99999. No placeholders or TODOs. Implement completely.
99999. Run tests before committing.
```

Then run:

```bash
gumloop --prompt-file PROMPT.md --choo-choo
```

## How It Works

1. **Fresh start** — Agent loads only the prompt (small, deterministic)
2. **Read state from disk** — Git history, modified files
3. **One task** — Implement, test, commit
4. **Check for changes** — If no git changes, work is complete
5. **Loop** — Back to step 1 with fresh context (if `--choo-choo`)

### Completion Detection

The loop stops when:
- No git changes detected (agent has nothing left to do)
- Max iterations reached (if specified)
- Stuck detected: N iterations with changes but no commits (default: 3)
- User presses Ctrl+C

Adjust stuck threshold:
```bash
gumloop --choo-choo --stuck-threshold 5   # Exit after 5 stuck iterations
```

### Run Metrics

When complete, gumloop shows statistics including why the loop exited:

```
┌─────────────────────────────────────┐
│           RUN COMPLETE              │
├─────────────────────────────────────┤
│  Agent:       claude                │
│  Iterations:  3                     │
│  Commits:     2                     │
│  Duration:    1m 45s                │
├─────────────────────────────────────┤
│  Exit: ✅ Complete (no changes)
└─────────────────────────────────────┘
```

Exit reasons: `Complete (no changes)`, `Max iterations`, `Stuck (N iterations without commit)`, `Single run`

## Safety

### Built-in protections

- Refuses to run in dangerous directories: `~`, `/`, `/etc`, `/usr`, `/var`, `/tmp`
- Requires a git repository
- Warns before `--choo-choo` mode in home subdirectories

### Git is your safety net

```bash
git diff                  # See what changed
git reset --hard          # Undo everything
git reset --hard HEAD~3   # Undo last 3 commits
git stash                 # Temporarily save changes
```

### For overnight/unattended runs

Use external sandboxing: [E2B](https://e2b.dev/), [Fly Sprites](https://fly.io/), [Modal](https://modal.com/), or a dedicated VM.

## Tuning Your Prompts

Ralph will fail. That's expected. Add guardrails when you see patterns:

```markdown
# PROMPT.md

Study the codebase. Find the most important thing to implement.
Implement it. Run tests. Commit and exit.

## Rules
- Before implementing, search to confirm it's not already done.
- No placeholders or TODOs. Implement completely.
- Always run the test suite before committing.
- Keep commits atomic - one logical change per commit.
```

Build your prompt through observation — when you see the agent make a mistake, add a rule to prevent it.

## Advanced Techniques

### Priority Numbering

LLMs pay more attention to items later in a prompt. Use high numbers for critical rules:

```markdown
1. Study the codebase.
2. Choose one task to implement.
3. Implement it completely.

99999. Search before implementing to avoid duplicating existing code.
999999. Run tests before committing.
9999999. Never commit if tests fail.
```

**Why it works:** The agent processes instructions sequentially. Higher-numbered rules appear later and get more "attention weight." When adding new critical rules, use more digits to ensure they're processed last.

### Two-Mode Operation

Split planning and execution into separate prompts for complex projects.

**Planning mode** — analyze gaps, create task list:
```bash
gumloop --prompt-file PROMPT_plan.md --choo-choo 5
```

```markdown
# PROMPT_plan.md
1. Study specs/ to understand requirements.
2. Study src/ to understand current implementation.
3. Compare: what's specified vs what exists?
4. Update IMPLEMENTATION_PLAN.md with prioritized gaps.
5. Do NOT implement anything. Planning only.
```

**Building mode** — execute one task per iteration:
```bash
gumloop --prompt-file PROMPT_build.md --choo-choo 20
```

```markdown
# PROMPT_build.md
1. Read IMPLEMENTATION_PLAN.md for priorities.
2. Pick the highest priority incomplete task.
3. Implement it completely.
4. Run tests. Fix any failures.
5. Mark complete in plan. Commit. Exit.
```

**When to switch:** Use plan mode at the start or when the agent goes off track. Plans are disposable — regenerate rather than fight a stale plan.

### Backpressure

Use the `--verify` flag to run automated checks after each iteration:

```bash
gumloop --choo-choo --verify "npm test"              # Run tests
gumloop --choo-choo --verify "tsc --noEmit"          # Type check
gumloop --choo-choo --verify "npm test && npm run lint"  # Multiple checks
```

| Check | Command | Catches |
|-------|---------|---------|
| Types | `tsc --noEmit` | Type errors |
| Tests | `npm test` | Logic errors |
| Lint | `eslint .` | Style violations |
| Build | `npm run build` | Compilation failures |

Also add backpressure to your prompt:
```markdown
Run tests before committing. If tests fail, fix them first.
Never commit code that doesn't compile.
```

**Strong backpressure** (tests, types) gives binary pass/fail signals. **Weak backpressure** ("make sure it works") is subjective and easily ignored.

### Project Structure

For larger projects, organize files to help the agent:

```
project/
├── PROMPT.md              # Instructions (keep lean ~5K tokens)
├── AGENTS.md              # How to build/test/run (~50 lines)
├── IMPLEMENTATION_PLAN.md # Task list (maintained by agent)
├── specs/                 # Requirements docs
│   ├── auth.md
│   └── api.md
└── src/
```

**AGENTS.md** — Operational info only:
```markdown
## Build
npm install && npm run build

## Test
npm test

## Patterns
- Components in src/components/
- Tests co-located with source
```

**IMPLEMENTATION_PLAN.md** — Agent-maintained task tracker:
```markdown
## In Progress
- [ ] Add login form validation

## High Priority
- [ ] Implement password reset flow

## Done
- [x] Set up authentication routes
```

### Context Budgeting

Keep prompts lean — they're loaded every iteration:

```
200K context window
-  2K  system prompt
-  5K  PROMPT.md
- 10K  reference docs
- 50K  working room (files, tool output)
─────────────────────
133K  reasoning headroom
```

**Guidelines:**
- PROMPT.md under 5K tokens
- Exit before 100K total context used
- One task per iteration (multiple tasks = accumulated context)
- Store progress in files, not instructions ("Check IMPLEMENTATION_PLAN.md" not "Continue from step 5")

## Uninstall

```bash
gumloop --uninstall
```

Or manually:

```bash
rm ~/.local/bin/gumloop
```

## Philosophy

> "Ralph is a Bash loop."

> "Deterministically bad in an undeterministic world."

> "LLMs are a mirror of operator skill."

Simple loop. Context rotation. Git persistence. That's it.

## Links

- [ghuntley.com/ralph](https://ghuntley.com/ralph/) — Origin of the technique
- [ghuntley.com/loop](https://ghuntley.com/loop/) — Context engineering deep dive
- [ghuntley.com/cursed](https://ghuntley.com/cursed/) — Advanced patterns

## License

MIT
