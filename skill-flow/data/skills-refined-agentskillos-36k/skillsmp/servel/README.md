# Servel Skill

Agent skill for [Servel](https://servel.dev) — self-hosted deployment platform via Docker Swarm.

## Installation

```bash
npx skills add K-NRS/servel-skill
# or
bunx skills add K-NRS/servel-skill
```

### Manual Installation

Download the skill file and place it in your agent's configuration directory:

```bash
curl -O https://raw.githubusercontent.com/K-NRS/servel-skill/main/SKILL.md
```

| Agent | Location |
|-------|----------|
| **Antigravity** | `.agent/skills/servel/SKILL.md` |
| **Claude Code** | `~/.claude/skills/servel/SKILL.md` |
| **Codex** | `$CODEX_HOME/skills/servel/SKILL.md` or `.codex/skills/servel/SKILL.md` |
| **Cursor** | `.cursor/rules/servel.md` or append to `.cursorrules` |
| **Gemini CLI** | `~/.gemini/skills/servel/SKILL.md` |
| **GitHub Copilot** | `.github/copilot-instructions.md` |
| **Goose** | `~/.config/goose/skills/servel/SKILL.md` or `.goose/skills/servel/SKILL.md` |
| **Kiro CLI** | `~/.kiro/skills/servel/SKILL.md` |
| **OpenCode** | `~/.opencode/skills/servel/SKILL.md` or `.opencode/skills/servel/SKILL.md` |
| **Qoder** | `~/.qoder/skills/servel/SKILL.md` or `.qoder/skills/servel/SKILL.md` |
| **Trae** | `.trae/rules/servel.md` |
| **Windsurf** | `.windsurfrules` |
| **Cline** | `.clinerules` |
| **Aider** | `CONVENTIONS.md` |

**Example (Claude Code):**
```bash
mkdir -p ~/.claude/skills/servel
curl -o ~/.claude/skills/servel/SKILL.md https://raw.githubusercontent.com/K-NRS/servel-skill/main/SKILL.md
```

**Example (Cursor):**
```bash
mkdir -p .cursor/rules
curl -o .cursor/rules/servel.md https://raw.githubusercontent.com/K-NRS/servel-skill/main/SKILL.md
```

**Example (Gemini CLI):**
```bash
mkdir -p ~/.gemini/skills/servel
curl -o ~/.gemini/skills/servel/SKILL.md https://raw.githubusercontent.com/K-NRS/servel-skill/main/SKILL.md
```

## What This Skill Does

Teaches AI agents to use Servel for deployment and infrastructure management:

- Deploy applications with `servel deploy` (auto-detects project type)
- Manage 44+ infrastructure types (databases, queues, caches, platforms)
- Link infrastructure to apps (auto-injects connection strings)
- Preview deployments with auto-cleanup
- Backup and restore databases
- Configure domains with automatic SSL
- Manage encrypted secrets
- Development mode with file sync

## Links

- [Servel Website](https://servel.dev)
- [Documentation](https://servel.dev/docs)
- [Infrastructure Hub](https://hub.servel.dev) — Explore 44+ pre-defined infrastructures
- [Configuration Schema](https://servel.dev/docs/configuration)

## License

MIT
