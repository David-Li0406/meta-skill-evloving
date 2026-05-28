# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

gumloop is a bash CLI that runs AI coding agents (Claude, Codex, Gemini, OpenCode, Amp, Aider) in autonomous loops. Based on Geoffrey Huntley's "Ralph Wiggum" methodology: fresh context per iteration, progress persists in git.

Core insight: LLM context has malloc but no free. Loop termination IS the free(). Each iteration: fresh context → one task → commit → exit → repeat.

## Commands

```bash
# Run once (default)
./gumloop -p "Fix the tests"
./gumloop --prompt-file PROMPT.md

# Loop mode (until no changes or max iterations)
./gumloop --choo-choo -p "Fix all bugs"
./gumloop --choo-choo 20

# Select agent
./gumloop --cli claude                    # Claude Code (default)
./gumloop --cli codex                     # OpenAI Codex
./gumloop --cli gemini                    # Google Gemini
./gumloop --cli opencode                  # OpenCode
./gumloop --cli amp                       # Sourcegraph Amp
./gumloop --cli aider                     # Aider

# Other options
./gumloop --no-push                       # Skip git push
./gumloop --stuck-threshold 5             # Exit after 5 iterations without commits
./gumloop --verify "npm test"             # Run tests after each iteration
./gumloop --init                          # Create PROMPT.md template
./gumloop --recover                       # Discard uncommitted changes
./gumloop --recover 3                     # Reset last 3 commits
./gumloop --update                        # Update to latest version
./gumloop --uninstall                     # Remove gumloop
./install.sh                              # Install to ~/.local/bin/
```

## Architecture

Single bash script (`gumloop`) that:
1. Parses args (--cli, --choo-choo, -p/--prompt, --prompt-file, --no-push, --stuck-threshold, --verify, etc.)
2. Safety checks (refuses dangerous paths, requires git)
3. Configures CLI flags based on agent type
4. Runs agent (once without --choo-choo, loops with --choo-choo)
5. Tracks commits per iteration for progress detection
6. Detects stuck loops (changes but no commits)
7. Runs optional verification command (--verify)
8. Outputs metrics (iterations, commits, duration, exit reason)

Key files:
- `gumloop` - The CLI executable (bash)
- `test.sh` - Test suite (run with `./test.sh`)
- `SKILL.md` - Claude.ai skill definition for slash commands
- `references/` - Documentation for the technique (not code)

## CLI Flag Mapping

When choo-choo mode is enabled:
- claude: `-p --dangerously-skip-permissions`
- codex: `--full-auto`
- gemini: `--yolo`
- opencode: `-q`
- amp: `--dangerously-allow-all`
- aider: `--yes-always --no-pretty`

## Safety Model

Built-in protections:
- Refuses: `~`, `/`, `/etc`, `/usr`, `/var`, `/tmp`, `/bin`, `/sbin`, `/lib`
- Requires git repository
- Warns + confirms for --choo-choo in home subdirectories

Git is the safety net: `git reset --hard` recovers from any iteration.

## The Technique (for modifying this repo)

When working on gumloop itself, understand:
- Prompts should be lean (loaded every iteration, consumes context budget)
- One task per iteration (multiple tasks = context accumulation)
- Progress stored in files/git, not agent memory
- Guardrails use high numbers (99999) for priority
- Plans are disposable, prompts are refined through observation
