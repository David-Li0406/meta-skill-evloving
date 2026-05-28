---
name: zsh-shell-mastery
description: Zsh shell configuration and troubleshooting for rc/startup files (.zshenv, .zprofile, .zshrc, .zlogin, .zlogout), prompt/theme setup (powerlevel10k), frameworks (oh-my-zsh), plugin managers (sheldon), and common plugins (zsh-autocomplete, autosuggestions, syntax-highlighting). Use when editing or diagnosing Zsh startup order, environment variables, PATH, completions/compinit/fpath, plugin load order, performance, or interactive UX.
---

# Zsh Shell Mastery

## Working style

- Prefer minimal, predictable Zsh: small core + explicit plugins.
- Treat startup file responsibilities as strict boundaries.
- Optimize for: correctness (startup order), latency (fast prompt), portability (macOS/Linux), and debuggability.
- Treat oh-my-zsh as a source of vendored plugins/aliases/snippets (not as a framework to be sourced at runtime) unless explicitly requested.
- For chezmoi-specific workflows (source vs target mapping, templating, secrets), defer to the existing `chezmoi-management` skill; this skill focuses on Zsh semantics and config design.

## Chezmoi integration (important)

- Edit Zsh and related configs in the *chezmoi source* (this repo), not directly in `~`.
- Some files may be chezmoi go-templates; treat `{{ ... }}` blocks as template logic and avoid breaking it.
- After edits, apply/verify via chezmoi (see `chezmoi-management` skill for the exact workflow).
- Remember chezmoi source naming: `dot_zshrc` -> `~/.zshrc`, `private_dot_config/sheldon` -> `~/.config/sheldon`, etc.

## Workflow decision tree

1. **Environment variables / PATH / locales / toolchain env?** Read `references/startup-files.md`, then edit `.zshenv` (minimal!) or `.zprofile`.
2. **Interactive behavior (aliases, keybinds, completions, prompt, plugins)?** Edit `.zshrc`.
3. **Login-only interactive tweaks?** Use `.zprofile` (for env) and `.zlogin` (rare).
4. **Performance regressions?** Read `references/performance.md` and profile startup.
5. **Framework/plugin-manager specific change?** Read the matching reference:
   - oh-my-zsh (vendored snippets/plugins): `references/oh-my-zsh.md`
   - powerlevel10k: `references/powerlevel10k.md`
   - sheldon: `references/sheldon.md`
   - common plugins + load order: `references/plugins.md`

## Default guardrails

- Keep `.zshenv` idempotent and fast; avoid running external commands.
- Avoid defining aliases/functions in `.zshenv`.
- Prefer `typeset -gx VAR=...` / `export VAR=...` and defensive checks (`[[ -d ... ]]`).
- Keep `fpath`/completions deterministic; avoid multiple compinit runs.
- Document plugin load order (especially when using `zsh-autocomplete` and `zsh-syntax-highlighting`).

## Common tasks

- **Add a new env var**: choose `.zshenv` (needed everywhere) vs `.zprofile` (login shells) vs `.zshrc` (interactive only).
- **Fix PATH issues**: ensure ordering, remove duplicates, avoid `PATH=$PATH:...` patterns in multiple files.
- **Enable completions**: set `fpath` before `compinit`; run `compinit` once; cache if desired.
- **Add a plugin**: decide framework/manager, then ensure correct load order.
- **Prompt setup (p10k)**: keep "instant prompt" block first in `.zshrc`; source `~/.p10k.zsh` after plugin init.

## References

- Startup file map and ordering: `references/startup-files.md`
- oh-my-zsh patterns: `references/oh-my-zsh.md`
- powerlevel10k patterns: `references/powerlevel10k.md`
- sheldon patterns: `references/sheldon.md`
- Plugin notes and load order: `references/plugins.md`
- Performance checklist: `references/performance.md`
