# oh-my-zsh (OMZ) as a plugin/snippet source

## Default stance for this repo

- Do not source `oh-my-zsh.sh` at runtime.
- Keep a local clone of OMZ and selectively vendor/copy bits you want (plugins, aliases, completion snippets).
- Prefer explicit loading via your chosen mechanism (manual sourcing or a plugin manager like sheldon).

## What to take from OMZ

- A plugin's actual implementation is usually `plugins/<name>/<name>.plugin.zsh` plus any `functions/` and completion files.
- Many OMZ "plugins" are just aliases/functions and can be sourced directly.

## Guardrails

- Avoid copying OMZ's full initialization; it can introduce extra latency and hidden side effects.
- Pin the OMZ clone to a known revision if you depend on specific behavior.
- When vendoring completion files, ensure they land on `fpath` before `compinit`.

## If you later decide to use full OMZ

- If you explicitly choose full OMZ, switch to the classic model (set `ZSH=...`, set `plugins=(...)`, then `source $ZSH/oh-my-zsh.sh`) and re-check completion/plugin ordering and startup time.
