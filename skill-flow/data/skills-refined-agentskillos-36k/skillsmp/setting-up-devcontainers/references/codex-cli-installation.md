# Codex CLI Installation Reference

Quick reference for installing OpenAI Codex CLI in devcontainers.

## Installation via Volta

```dockerfile
# In Dockerfile ({{VOLTA_ENV_BLOCK}} placeholder)
ENV VOLTA_HOME="/home/vscode/.volta"
ENV PATH="$VOLTA_HOME/bin:$PATH"

USER $USERNAME

# {{CODEX_INSTALL_BLOCK}} placeholder
RUN curl -fsSL https://get.volta.sh | bash \
    && $VOLTA_HOME/bin/volta install node@22.21 \
    && $VOLTA_HOME/bin/volta install @openai/codex
```

## Directory Structure

```
~/.codex/
├── config.toml          # CLI configuration
├── sessions/            # Session data
└── skills/              # User skills (copied from marketplace)
```

## Skills Location

Codex loads skills from these directories (priority order):

1. `.codex/skills` - Repository root
2. `~/.codex/skills` - User directory (where we sync)
3. `/etc/codex/skills` - System-wide

## Skill Format

```yaml
---
name: skill-name
description: What and when description
metadata:
  short-description: Optional
---

Instructions for the agent...
```

## Volume Persistence

Mount `~/.codex/` as a named volume to persist:
- Configuration (`config.toml`)
- Session data
- Synced skills

```json
{
  "mounts": [
    "source=codex-config-${NAME},target=/home/vscode/.codex,type=volume"
  ]
}
```

## Syncing Skills from Marketplace

Codex ignores symlinked directories, so skills must be copied:

```bash
# sync-codex-skills.sh
for skill_path in plugins/*/skills/*/; do
    [ -f "$skill_path/SKILL.md" ] || continue
    skill_name=$(basename "$skill_path")
    rm -rf "$CODEX_SKILLS_DIR/$skill_name"
    cp -r "$skill_path" "$CODEX_SKILLS_DIR/$skill_name"
done
```

## Authentication

Run `codex` and select "Sign in with ChatGPT" to authenticate.

## Useful Aliases

```bash
alias codex-f='codex --full-auto'
```

## References

- [Codex CLI Documentation](https://developers.openai.com/codex/cli)
- [Codex Skills](https://developers.openai.com/codex/skills/)
- [Volta](https://volta.sh)
