---
name: shell-scripting
description: Guide for writing robust shell scripts following best practices to use bash with proper options, quote variables, use modern syntax, include debugging support, and provide help.
---

## What I do

Provide comprehensive guidelines for writing maintainable and robust shell scripts, including:

- Use bash with proper error handling options
- Modern syntax and best practices
- Debugging support
- Help functionality
- A standard script template

## When to use me

Use this skill when you need to write, review, or improve shell scripts. It covers best practices for bash scripting to ensure scripts are reliable, debuggable, and maintainable.

## Best Practices

1. **Use bash**: Stick to bash for portability and collaboration. Avoid zsh, fish, or other shells unless absolutely necessary.

2. **Shebang**: Always start with `#!/usr/bin/env bash`, even if not making the script executable.

3. **File extension**: Use `.sh` or `.bash` extension for clarity.

4. **Error handling**:
   - `set -o errexit`: Exit on command failure
   - `set -o nounset`: Fail on unset variables (use `"${VARNAME-}"` for optional variables)
   - `set -o pipefail`: Treat pipeline failures as errors

5. **Debugging**: Use `set -o xtrace` conditionally: `if [[ "${TRACE-0}" == "1" ]]; then set -o xtrace; fi` to enable with `TRACE=1 ./script.sh`

6. **Conditions**: Use `[[ ]]` instead of `[ ]` or `test` for better functionality.

7. **Variable quoting**: Always quote variable accesses with double quotes: `"$VAR"`. Exception: left-hand side of `[[ ]]` conditions.

8. **Functions**: Use `local` for function variables.

9. **Help handling**: Check for help flags like `-h`, `--help`, `help`, `h`, `-help` and print usage.

10. **Error output**: Redirect errors to stderr: `echo 'Error message' >&2`

11. **Options**: Prefer long options like `--silent` over `-s` for clarity.

12. **Working directory**: Change to script directory: `cd "$(dirname "$0")"`

13. **Linting**: Use shellcheck and heed its warnings.

## Template

```
#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
    echo 'Usage: ./script.sh arg-one arg-two

This is an awesome bash script to make your life better.

'
    exit
fi

cd "$(dirname "$0")"

main() {
    echo do awesome stuff
}

main "$@"
```

Follow these practices to write maintainable, robust shell scripts.
