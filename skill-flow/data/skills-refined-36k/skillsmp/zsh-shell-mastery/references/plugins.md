# Common plugins and load order

## zsh-autocomplete

- Generally wants to run after the completion system is initialized.
- If you see completion weirdness, start by isolating: disable other completion plugins and ensure a single `compinit`.

## zsh-autosuggestions

- Typically loaded after completions/keybindings are in place.
- If suggestions don't show, verify `ZSH_AUTOSUGGEST_STRATEGY` and that no widget overrides are clobbering it.

## zsh-syntax-highlighting

- Should be sourced last (or very late), after other widgets are defined.

## General ordering heuristic

1. Framework/plugin-manager init
2. `fpath` setup
3. `compinit`
4. Completion enhancers (that require compinit)
5. Autosuggestions
6. Syntax highlighting
7. Prompt config (unless prompt framework requires earlier)
