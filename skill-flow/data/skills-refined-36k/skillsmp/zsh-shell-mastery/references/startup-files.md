# Zsh startup files (what goes where)

Zsh reads different files depending on whether the shell is login/non-login and interactive/non-interactive.

## Practical responsibility split

- `.zshenv`
  - Always read (interactive and non-interactive).
  - Keep minimal: exports, `ZDOTDIR`, very small PATH bootstrap.
  - Avoid: `brew shellenv`, `pyenv init`, `ssh-agent`, `compinit`, prompt, plugins.

- `.zprofile` (login shells)
  - Best place for "session env" setup.
  - Common: `PATH` additions, `brew shellenv`, language toolchains, `GPG_TTY`, `SSH_AUTH_SOCK` wiring.

- `.zshrc` (interactive shells)
  - UX and interactive behavior.
  - Common: aliases, functions, keybindings, completion system, prompt/theme, plugin loading.

- `.zlogin` / `.zlogout`
  - Rarely needed.
  - Use only for login-only interactive side effects.

## Ordering (simplified)

- All shells: `.zshenv`
- Login shells: `.zprofile` then `.zlogin`
- Interactive shells: `.zshrc`

Note: Zsh also supports `.zshrc` vs `.zprofile` interplay when a shell is both login and interactive (both will run).

## Safe patterns

- Guard expensive work:

```zsh
[[ -o interactive ]] || return 0
```

- Use `path` array to manage PATH safely:

```zsh
typeset -U path PATH
path=(/opt/homebrew/bin $path)
export PATH
```
