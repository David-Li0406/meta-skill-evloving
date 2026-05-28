# sheldon (plugin manager)

Repo: https://github.com/rossmacarthur/sheldon

## When to prefer sheldon

- You want explicit, reproducible plugin loading with minimal framework magic.
- You want one manager for plugins, snippets, and local sources.

## Practical integration

- Keep sheldon init in `.zshrc` (interactive only).
- Ensure completion-related plugins are loaded before you run `compinit` (unless a plugin explicitly requires the opposite).

## Chezmoi mapping reminder

- In this repo, sheldon's config typically lives under the chezmoi source path `private_dot_config/sheldon` which maps to `~/.config/sheldon` on the machine.
- When changing sheldon config, edit the repo source path, then apply via chezmoi (defer to `chezmoi-management` skill for the workflow).

## Pattern: explicit load ordering

- Put plugins into groups in your config (core env helpers, completions, UX, prompt) and document the ordering.
- For local plugins/snippets, prefer absolute paths or clearly defined base dirs.

## Debugging

- If a plugin isn't loading, check generated init script content and verify the file exists on disk.
- If completions break, verify `fpath` contents and ensure `compinit` runs once.
