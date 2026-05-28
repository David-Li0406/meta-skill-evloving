# Chezmoi commands & workflows

This file is a *practical* quick reference for `chezmoi` operations in a dotfiles repo.

## Mental model

- **Source directory**: where your chezmoi-managed files live (in this repo).
- **Target directory**: where files are applied (usually `$HOME`).
- **State**: chezmoi knows differences between source and target.

## Common workflows

### 1) Edit a managed file (repo-first)

- Edit the source file in this repo directly (recommended for agent + human collaboration)
- `chezmoi apply` (apply changes)

Optional convenience when starting from a target path:
- `chezmoi edit ~/.zshrc` (edits the *source* file via mapping)

### 2) Add a new file to be managed

- `chezmoi add ~/.config/foo/config.toml`
- Optionally verify/edit the created source:
  - `chezmoi edit ~/.config/foo/config.toml`
- `chezmoi apply`

### 3) See what would change

- `chezmoi diff`
- `chezmoi apply --dry-run --verbose`

### 4) Apply only some changes

- `chezmoi apply ~/.zshrc`
- `chezmoi apply --include dotfiles` (if tags/filters are used)

### 5) Inspect how chezmoi maps source/target

- `chezmoi source-path ~/.zshrc`
- `chezmoi target-path <source-path>`

### 6) External templates / execution

- `chezmoi execute-template < template.tmpl`
- `chezmoi execute-template --data "{\"key\":\"value\"}" < file.tmpl` (JSON)

## Day-to-day commands

- `chezmoi status`
- `chezmoi diff`
- `chezmoi apply`
- `chezmoi verify` (detect drift)
- `chezmoi doctor` (diagnostic)

## Init / onboarding patterns

- Local repo: `chezmoi init --source <path-to-repo>`
- Remote repo: `chezmoi init <user>/<repo>`

## Useful flags

- `--dry-run` / `-n`: don’t write
- `--verbose` / `-v`: show operations
- `--force`: overwrite conflicts (use sparingly)
- `--debug`: debugging output

## Safety notes

- Prefer `chezmoi diff` before applying.
- Prefer `chezmoi apply --dry-run -v` on new machines.
- Avoid executing templates that run shell commands unless you trust the source.
