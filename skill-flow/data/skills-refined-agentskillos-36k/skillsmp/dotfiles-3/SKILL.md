---
name: dotfiles
description: Manage dotfiles in ~/.dotfiles using dotter, including cross-platform config, security guidance, and deployment workflow.
---

# Dotfiles Management Skill

Manage dotfiles stored in `~/.dotfiles` using dotter.

## Structure

- `~/.dotfiles/` - Main dotfiles repository
- `~/.dotfiles/.dotter/global.toml` - Dotter configuration with symlink mappings
- `~/.dotfiles/bin/` - Custom scripts (symlinked to `~/bin/`)
- `~/.dotfiles/config/` - Config files (symlinked to `~/.config/`)

## Machines

- **Gali10** - Linux machine
- **Gali11** - macOS machine

Files should work cross-platform (Linux and macOS) unless specifically targeting one.

## Security Guidelines

- Never store secrets, API keys, or credentials in dotfiles
- Check for sensitive data before adding new files
- Use environment variables or separate secret management for credentials

## Workflow

1. Edit files in `~/.dotfiles/`
2. Add new files to `~/.dotfiles/.dotter/global.toml`
3. Run `dotter deploy` to create symlinks
4. User handles git commits (never commit automatically)

## Dotter Config Format

```toml
[default.files]
"source/path" = "~/destination/path"
```

## Proactive Suggestions

When modifying config files, suggest:
- Adding them to dotfiles if not already tracked
- Cross-platform compatibility improvements
- Security checks for sensitive data
