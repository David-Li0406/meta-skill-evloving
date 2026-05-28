# managing-dependencies

A skill for evaluating packages and managing dependencies securely.

Works with [Claude Code](https://claude.ai/code), [Codex CLI](https://github.com/openai/codex), and other agents supporting the [Agent Skills](https://agentskills.io) format.

## Installation

```
/plugin marketplace add andrew/managing-dependencies
```

Or copy `SKILL.md` to your skills directory manually:

```bash
# Claude Code
mkdir -p ~/.claude/skills/managing-dependencies
cp SKILL.md ~/.claude/skills/managing-dependencies/

# Codex CLI
mkdir -p ~/.codex/skills/managing-dependencies
cp SKILL.md ~/.codex/skills/managing-dependencies/

# Project-specific (Claude Code)
mkdir -p .claude/skills/managing-dependencies
cp SKILL.md .claude/skills/managing-dependencies/

# Project-specific (Codex CLI)
mkdir -p .codex/skills/managing-dependencies
cp SKILL.md .codex/skills/managing-dependencies/
```

## What it does

Provides guidance for:
- Evaluating packages before adding them
- Detecting typosquatting and dependency confusion
- Managing lockfiles and version constraints
- Running security audits
- Reviewing dependency changes in PRs

## Usage

The skill activates automatically when you ask Claude Code about dependencies, packages, or supply chain security. Examples:

- "Should I add lodash or write this myself?"
- "Review the lockfile changes in this PR"
- "Audit this project's dependencies"
- "Is this package trustworthy?"

## License

[CC0 1.0](LICENSE) - Public domain
