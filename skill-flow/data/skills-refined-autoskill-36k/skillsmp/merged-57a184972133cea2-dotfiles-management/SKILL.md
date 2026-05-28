---
name: dotfiles-management
description: Use this skill to manage dotfiles in `~/dotfiles` using dotter, including deployment, organization, and security practices.
---

# Dotfiles Management Skill

Manage dotfiles stored in `~/dotfiles` using dotter, a symlink manager and templater.

## Structure

- `~/dotfiles/` - Main dotfiles repository
- `~/dotfiles/.dotter/` - Dotter configuration
  - `global.toml` - Package definitions (files to deploy)
  - `local.toml` - Machine-specific package selection
  - `cache.toml` - Deployment state cache
- `~/dotfiles/bin/` - Custom scripts (symlinked to `~/bin/`)
- `~/dotfiles/config/` - Config files (symlinked to `~/.config/`)

## Machines

Files should work cross-platform (Linux and macOS) unless specifically targeting one.

## Security Guidelines

- Never store secrets, API keys, or credentials in dotfiles.
- Check for sensitive data before adding new files.
- Use environment variables or separate secret management for credentials.

## Core Commands

```bash
# Deploy all configured files
dotter deploy

# Preview changes without applying
dotter deploy --dry-run

# Undeploy all managed files
dotter undeploy

# Watch for changes and auto-deploy
dotter watch
```

## Workflow: Add New Dotfile

1. **Add Source File**: Place the configuration file in `~/dotfiles`:
   ```bash
   cp ~/.config/app/config.toml ~/dotfiles/.config/app/config.toml
   ```

2. **Define in global.toml**: Add a new package or extend an existing one in `~/dotfiles/.dotter/global.toml`:
   ```toml
   [myapp.files]
   ".config/app/config.toml" = "~/.config/app/config.toml"
   ```

3. **Enable Package (if new)**: Add package to `~/dotfiles/.dotter/local.toml`:
   ```toml
   packages = ["doom", "myapp"]
   ```

4. **Deploy**:
   ```bash
   cd ~/dotfiles && dotter deploy
   ```

## Workflow: Remove Dotfile

1. **Undeploy first**: `dotter undeploy`
2. **Remove from global.toml**: Delete the file mapping.
3. **Remove package from local.toml** (if removing entire package).
4. **Redeploy**: `dotter deploy`
5. **Clean up source** (optional): Remove file from dotfiles repo.

## Package Organization

Group related files into packages:
```toml
[shell.files]
".zshrc" = "~/.zshrc"
".zprofile" = "~/.zprofile"

[nvim.files]
".config/nvim" = "~/.config/nvim"

[git.files]
".gitconfig" = "~/.gitconfig"
```

## Templating

Dotter supports Handlebars templating for machine-specific values:
```toml
[package.variables]
email = "default@example.com"

[variables]
email = "work@company.com"
```
In template files, use `\{{email}}` syntax.

## Troubleshooting

**Conflict with existing file**:
```bash
dotter deploy --force
```

**Check deployment status**:
```bash
dotter deploy --dry-run --verbose
```

**View what's currently deployed**:
```bash
cat ~/dotfiles/.dotter/cache.toml
```

## Best Practices

- Keep packages granular and focused.
- Use descriptive package names.
- Commit changes to dotfiles repo after modifications.
- Test with `--dry-run` before deploying.
- Use templating for machine-specific values (email, paths).

## Proactive Suggestions

When modifying config files, suggest:
- Adding them to dotfiles if not already tracked.
- Cross-platform compatibility improvements.
- Security checks for sensitive data.