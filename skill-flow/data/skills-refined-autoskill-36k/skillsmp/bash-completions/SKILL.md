---
name: bash-completions
description: Instructions for adding to bash auto completions in the AutomateLinux project.
---

# Bash Auto-Completions

This project uses a modular system for bash auto-completions. Each major command has its own completion script located in `./terminal/completions/`.

## 1. Create the Completion Script

Create a new `.bash` file in the `./terminal/completions/` directory.

### Basic Template
```bash
_my_command_completion() {
    local cur prev
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Define words to complete
    local opts="start stop restart status"

    if [[ ${cur} == * ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}

complete -F _my_command_completion my_command
```

## 2. Register the Script

All completion scripts must be explicitly sourced in `./terminal/completions/completion.sh` to be active in the terminal.

Add a line to source your new file:

```bash
# In ./terminal/completions/completion.sh
. $(theRealPath my_new_completion.bash)
```

> [!NOTE]
> The `theRealPath` utility ensures the script is sourced correctly regardless of the current working directory.

## 3. Apply Changes

To see your new completions in action, either open a new terminal or source your `bashrc`:

```bash
sb  # Shorthand for sourcing ~/.bashrc
```

## Existing Examples
For more complex logic (like handling sub-commands or dynamic arguments), refer to:
- [daemon.bash](file:///home/yaniv/coding/automateLinux/terminal/completions/daemon.bash): Handles `d` and `daemon` commands.
- [cd.bash](file:///home/yaniv/coding/automateLinux/terminal/completions/cd.bash): Handles directory history navigation.
