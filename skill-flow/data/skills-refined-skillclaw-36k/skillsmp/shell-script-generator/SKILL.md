---
name: shell-script-generator
description: Generate clean shell scripts following best practices.
metadata:
  author: garnertb
  version: "1.1"
---

# Shell Script Creator

Generate shell scripts following best practices.

## Script Setup

- Start scripts with shebang: (eg: `#!/bin/bash`)
- Good idea to include `[[ "$TRACE" ]] && set -x`
- `source` all dependencies before setting the `-e` or `+e` flags.
- Include usage, description, and optional examples using `#/` comment prefix:
  ```bash
  #!/bin/bash
  #/ Usage: my-script [options] <required_arg>
  #/
  #/ Brief description of the script's purpose.
  #/
  #/ OPTIONS:
  #/   -h | --help      Show this message.
  #/   -o <arg>         An option.
  ```
- Scripts must accept both `-h` and `--help` arguments, print usage, and exit:
  ```bash
  if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    grep '^#/' <"$0" | cut -c 4-
    exit 2
  fi
  ```

## Error Handling

- Fail fast, use `set -eo pipefail` (or `set -o errexit`) to cause the script to
  exit when a command fails.
  - Use `|| true` on programs that you intentionally let exit non-zero.
  - Note that ignoring an exit status with `|| true` is not a good practice,
    though it can be used in test scripts, if necessary.
- Set the exit code of a pipeline to that of the rightmost command that failed.
- Disallow unset variables.
- Usually use all three protections `set -o errexit -o nounset -o pipefail`
  - Use of `nounset` does require some extra code to either explicitly define
    variables (e.g. `FOO=`) or provide a default value, which may be blank:
    (e.g. `${FOO:-}`).
- Avoid manually checking exit status with `$?`.

## Variables and Quoting

- Always double quote variables, including subshells. No naked `$` signs.
- Use Bash variable substitution if possible before awk/sed.
- Generally use double quotes unless it makes more sense to use single quotes.
- When expecting or exporting environment, consider namespacing variables when
  subshells may be involved.
- Use lowercase for local/internal variables, uppercase for inherited/exported
  environment variables.
- Use `${var}` for interpolation only when required (e.g., `${greeting}world`).
- Use variables sparingly. Short paths and constants can be repeated for
  readability and easy search/replace.

## Conditionals and Control Flow

- For simple conditionals, try using `&&` and `||`.
- Put `then`, `do`, etc on same line, not newline.
- Skip `[[ ... ]]` in your if-expression if you can test for exit code instead.
- Use `test` or `[` for portable conditionals; use `[[` for advanced Bash
  features like glob matching.
- Test for exit code vs output:
  ```bash
  # Test for exit code (-q mutes output)
  if grep -q 'foo' somefile; then ...; fi
  # Test for output (-m1 limits to one result)
  if [[ "$(grep -m1 'foo' somefile)" ]]; then ...; fi
  ```
- Prefer `$[x+y]` or `$((x+y))` for mathematical expressions.
- Use `for` loops with `seq` or C-style syntax:
  ```bash
  for i in $(seq 0 9); do ...; done
  for ((n=0; n<10; n++)); do ...; done
  ```

## Output and Formatting

- Don't be afraid of `printf`, it's more powerful than `echo`.
- Use hard tabs. Heredocs ignore leading tabs, allowing better indentation.
- Use `<<heredocs` for multi-line strings:
  - `<<eof` allows interpolation; `<<'eof'` or `<<"eof"` disables it.
  - `<<-eof` strips leading tabs for better indentation.

## File Descriptors

- Let Bash choose the file descriptor for you when possible.
- File descriptors `1` (stdout) and `2` (stderr) are standard; others (3+) are
  free but shared by subprocesses—coordinate usage to avoid conflicts.

## Functions and Code Organization

- Put complex one-liners of `sed`, `perl`, etc in a standalone function with a
  descriptive name.
- Use functions sparingly; prefer small, simple, sequential scripts.
- In large systems or for any CLI commands, add a description to functions.
  - Use `declare desc="description"` at the top of functions, even above
    argument declaration.
  - This can be queried/extracted using reflection. For example:
  ```
  eval $(type FUNCTION_NAME | grep 'declare desc=') && echo "$desc"
  ```
- Define function arguments clearly:
  ```bash
  regular_func() {
    declare arg1="$1" arg2="$2" arg3="$3"
    # ...
  }
  ```
- For variadic arguments:
  ```bash
  variadic_func() {
    local arg1="$1"; shift
    local arg2="$1"; shift
    local rest="$@"
    # ...
  }
  ```

## File Naming

- Use `.sh` or `.bash` extension if file is meant to be included/sourced. Never
  on executable script.

## Design Principles

- Design for simplicity and obvious usage.
  - Avoid option flags and parsing, try optional environment variables instead.
  - Use subcommands for necessary different "modes".

## Portability

- Be conscious of the need for portability. Bash to run in a container can make
  more assumptions than Bash made to run on multiple platforms.
- Ensure scripts support both macOS and Linux environments.
- Avoid Bash arrays; they are not portable.
