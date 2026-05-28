# powerlevel10k (p10k)

## Key integration rules

- If using p10k "instant prompt", keep its generated block at the very top of `.zshrc`.
- Source `~/.p10k.zsh` after plugin/framework initialization so segments are available.

## Common failure modes

- Prompt flashes or slow first paint: instant prompt block not first, or early startup runs external commands.
- Missing icons: terminal font not set to a Nerd Font.

## Suggested approach

- Keep prompt config (`~/.p10k.zsh`) separate from plugin manager configuration.
- Avoid prompt-time external commands; prefer async segments or cached results.
