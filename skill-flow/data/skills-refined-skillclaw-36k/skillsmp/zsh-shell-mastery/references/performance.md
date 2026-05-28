# Zsh performance checklist

## Quick profiling

- Time an interactive shell:

```sh
time zsh -i -c exit
```

- If you suspect login-specific slowness:

```sh
time zsh -l -i -c exit
```

## Common causes

- External commands in `.zshenv` or early `.zshrc` (especially `brew shellenv`).
- Re-running `compinit` every shell without caching.
- Heavy git prompt segments doing synchronous calls.
- Overlapping frameworks/managers (e.g., OMZ + another manager) loading duplicates.

## Practical fixes

- Move expensive env initialization to `.zprofile` (login only).
- Cache completion dump (`compinit -C`) and avoid multiple `compinit` calls.
- Ensure prompt "instant prompt" blocks are first when using p10k.
- De-duplicate PATH and `fpath` early.
