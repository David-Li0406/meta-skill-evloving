# File Naming Conventions

Chezmoi encodes file attributes in source filenames using prefixes and suffixes.

## Prefixes (Applied in Order)

| Prefix | Effect | Example |
|--------|--------|---------|
| `after_` | Run script after updating destination | `run_after_setup.sh` |
| `before_` | Run script before updating destination | `run_before_install.sh` |
| `create_` | Create file only if missing, never overwrite | `create_dot_gitconfig` |
| `dot_` | Rename to leading dot | `dot_bashrc` → `.bashrc` |
| `empty_` | Ensure file exists even if empty | `empty_dot_gitkeep` |
| `encrypted_` | Decrypt file from source state | `encrypted_private_dot_ssh/id_rsa` |
| `exact_` | Remove unmanaged files in directory | `exact_dot_config/nvim` |
| `executable_` | Add executable permissions | `executable_dot_local/bin/script` |
| `literal_` | Stop parsing prefixes (escape mechanism) | `literal_dot_literal_file` |
| `modify_` | Script that modifies existing file | `modify_dot_bashrc` |
| `once_` | Run script only once per content hash | `run_once_install-packages.sh` |
| `onchange_` | Run script only when content changes | `run_onchange_reload-config.sh` |
| `private_` | Remove group/world permissions (0600/0700) | `private_dot_netrc` |
| `readonly_` | Remove write permissions | `readonly_dot_config` |
| `remove_` | Remove file/symlink/empty directory | `remove_dot_old_config` |
| `run_` | Execute as script | `run_install.sh` |
| `symlink_` | Create symlink instead of file | `symlink_dot_vimrc` |

## Suffixes

| Suffix | Effect |
|--------|--------|
| `.tmpl` | Process as Go template |
| `.literal` | Stop parsing suffixes |

## Common Combinations

| Target Type | Source Example |
|-------------|----------------|
| Hidden file | `dot_bashrc` |
| Hidden template | `dot_bashrc.tmpl` |
| Private hidden file | `private_dot_netrc` |
| Executable script | `executable_dot_local/bin/my-script` |
| Encrypted private file | `encrypted_private_dot_ssh/id_rsa` |
| Exact directory | `exact_dot_config/nvim/` |
| Symlink | `symlink_dot_vimrc` |
| Template symlink | `symlink_dot_vimrc.tmpl` |
| Create-only file | `create_dot_local_config` |
| Run-once script | `run_once_before_install.sh` |
| Run-onchange script | `run_onchange_after_reload.sh` |

## Special Files

All special files are optional. Located at source root.

| File | Purpose |
|------|---------|
| `.chezmoiroot` | Specifies subdirectory as source root |
| `.chezmoi.toml.tmpl` | Config file template (for `chezmoi init`) |
| `.chezmoiignore` | Patterns to ignore (supports templates) |
| `.chezmoiremove` | Files to remove on apply |
| `.chezmoiexternal.toml` | External files/archives/repos to include |
| `.chezmoiversion` | Minimum chezmoi version required |

## Special Directories

| Directory | Purpose |
|-----------|---------|
| `.chezmoidata/` | Static data files (JSON/YAML/TOML) merged into template data |
| `.chezmoitemplates/` | Reusable template partials |
| `.chezmoiscripts/` | Scripts that don't create directories in target |
| `.chezmoiexternals/` | External configuration files |

## Ignore Patterns

Create `.chezmoiignore` (supports templates):

```text
# Always ignore
README.md
LICENSE
.git

# Ignore on non-macOS
{{- if ne .chezmoi.os "darwin" }}
Library/
.Brewfile
{{- end }}

# Ignore on non-Linux
{{- if ne .chezmoi.os "linux" }}
.config/systemd/
{{- end }}
```

**Pattern syntax** (similar to `.gitignore`):
- `*` matches anything except `/`
- `**` matches anything including `/`
- `!pattern` excludes from ignore (takes priority)
- `#` starts a comment

## File Attribute Commands

```bash
chezmoi chattr +template ~/.bashrc     # Convert to template
chezmoi chattr +encrypted ~/.netrc     # Convert to encrypted
chezmoi chattr +executable ~/.local/bin/script  # Make executable
chezmoi chattr +private ~/.ssh/config  # Make private (0600)
chezmoi chattr +create ~/.local.conf   # Make create-only
```
