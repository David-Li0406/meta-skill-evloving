# Bash Style Guide

[Basics](#basics) · [Syntax](#syntax) · [Naming](#naming) · [Functions](#functions) · [Variables](#variables) · [Scope](#scope) · [Quoting](#quoting) · [Arguments](#arguments) · [Tests](#tests) · [Control flow](#control-flow) · [I/O](#io) · [Cleanup](#cleanup) · [Development](#development)

---

## Basics

### Script header

Include filename, author, date, and purpose at the top of scripts.

```bash
#!/usr/bin/env bash
# script-name.sh — Brief description of purpose
# Author: Name
# Date: 2024-01-15
```

---

### Shebang

Use `#!/usr/bin/env bash` for portability.

---

### Strict mode

Start scripts with `set -euo pipefail` to catch errors early: `-e` exits on error, `-u` errors on undefined variables, `-o pipefail` catches failures in pipelines.

---

### Main function

Encapsulate script logic in a `main` function called at the end.

```bash
function main() {
  # script logic here
}

main "${@}"
```

---

### Dual-purpose scripts

Use `BASH_SOURCE` to detect if the script is being sourced or executed.

```bash
[[ "${0}" == "${BASH_SOURCE[0]}" ]] && main "${@}"
```

---

## Syntax

### Expansions

---

#### Command substitution

Use `$(...)`, not backticks.

| Use                 | Avoid                  |
| ------------------- | ---------------------- |
| `result=$(command)` | `` result=`command` `` |

---

#### Variable expansion

Use `${var}`, not `$var`. Braces prevent ambiguity in concatenation.

| Use                  | Avoid              |
| -------------------- | ------------------ |
| `${filename}_backup` | `$filename_backup` |
| `${array[0]}`        | `$array[0]`        |

---

#### Parameter expansions

Use parameter expansions instead of external commands for simple string operations.

| Use          | Avoid                               |
| ------------ | ----------------------------------- |
| `${var%.*}`  | `echo "$var" \| sed 's/\.[^.]*$//'` |
| `${var##*/}` | `basename "$var"`                   |

---

### Command existence

Use `command -v`, not `which`. `which` is not POSIX and behaves inconsistently across systems.

| Use              | Avoid       |
| ---------------- | ----------- |
| `command -v git` | `which git` |

---

### Keyword placement

Place `then` and `do` on the same line as `if`, `for`, and `while`.

| Use                  | Avoid                    |
| -------------------- | ------------------------ |
| `if [[ ... ]]; then` | `if [[ ... ]]`<br>`then` |
| `for x in ...; do`   | `for x in ...`<br>`do`   |

---

### Bypass aliases

Prepend `\` to invoke the original command, bypassing aliases and builtins.

| Use             | Avoid          |
| --------------- | -------------- |
| `\time command` | `time command` |

---

### Heredoc quoting

Quote heredoc tags to prevent variable interpolation.

| Use       | Avoid   |
| --------- | ------- |
| `<<'EOF'` | `<<EOF` |

---

### Heredoc naming

Use descriptive heredoc tags instead of generic `EOF`.

| Use             | Avoid     |
| --------------- | --------- |
| `<<'SQL_QUERY'` | `<<'EOF'` |

---

### Eval dangers

Avoid `eval`; it introduces security risks and makes code hard to debug.

```bash
# Use: safe alternative with arrays
files=("${user_input}")
ls "${files[@]}"

# Avoid: allows command injection
eval "ls ${user_input}"
```

---

## Naming

### Function naming

Use `snake_case` for function names.

| Use              | Avoid          |
| ---------------- | -------------- |
| `get_user_input` | `GetUserInput` |
| `process_file`   | `processFile`  |

---

### Variable naming

Use `ALL_CAPS` for globals and constants, `lower_case` for locals.

| Use                   | Avoid                 |
| --------------------- | --------------------- |
| `local file_path`     | `local FILE_PATH`     |
| `readonly CONFIG_DIR` | `readonly config_dir` |

---

### Descriptive names

Use descriptive variable names, not abbreviations.

| Use            | Avoid |
| -------------- | ----- |
| `file_listing` | `fl`  |
| `user_count`   | `uc`  |

---

### Underscore prefix

Avoid `_var` names; the underscore prefix is reserved for system variables.

| Use         | Avoid        |
| ----------- | ------------ |
| `temp_file` | `_temp_file` |
| `local_var` | `_local_var` |

---

### Magic numbers

Replace magic numbers with named constants.

| Use                                           | Avoid      |
| --------------------------------------------- | ---------- |
| `readonly TIMEOUT=30`<br>`sleep "${TIMEOUT}"` | `sleep 30` |

---

### Error code constants

Prefix error code constants with `E_`.

```bash
readonly E_NOTFOUND=65
readonly E_PERMISSION=77
```

---

### Library namespacing

Prefix library functions with a namespace using `::`.

| Use              | Avoid           |
| ---------------- | --------------- |
| `mylib::my_func` | `mylib_my_func` |

## Functions

### Function syntax

Use `function name() { }` with both the keyword and parentheses.

| Use                      | Avoid                  |
| ------------------------ | ---------------------- |
| `function my_func() { }` | `my_func() { }`        |
| `function my_func() { }` | `function my_func { }` |

---

### Function placement

Define all functions after constants but before executable code.

---

### Local variables

Declare function variables with `local` to avoid polluting global scope.

| Use                  | Avoid          |
| -------------------- | -------------- |
| `local name="value"` | `name="value"` |

---

### Argument declaration

Assign positional parameters to named local variables at the top.

```bash
function process_file() {
  local input_file="${1}"
  local output_file="${2}"
  # ...
}
```

---

### Variadic functions

Use `shift` to separate the first argument from the rest.

```bash
function variadic_func() {
  local first="${1}"
  shift
  local rest=("${@}")
}
```

---

### Functions over aliases

Prefer functions over aliases for reusable commands.

```bash
# Use
function ll() {
  ls -la "${@}"
}

# Avoid
alias ll='ls -la'
```

---

### Extract complex commands

Wrap complex `sed`, `awk`, or `perl` one-liners in named functions.

```bash
# Use
function extract_emails() {
  grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' "${1}"
}
extract_emails input.txt

# Avoid
grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' input.txt
```

---

### Extract complex conditions

Wrap complex test conditions in named predicate functions.

| Use                       | Avoid                                                      |
| ------------------------- | ---------------------------------------------------------- |
| `if is_valid_input; then` | `if [[ -n "$x" && "$x" =~ ^[0-9]+$ && "$x" -gt 0 ]]; then` |

## Variables

### Declaration and assignment

Separate `local` declaration from command substitution to preserve exit codes. `local` always returns 0, masking command failures.

| Use                         | Avoid              |
| --------------------------- | ------------------ |
| `local var`<br>`var=$(cmd)` | `local var=$(cmd)` |

---

### Integer variables

Use `local -i` to declare integer variables. This enforces arithmetic context and catches non-numeric assignments.

| Use                | Avoid           |
| ------------------ | --------------- |
| `local -i count=0` | `local count=0` |

---

### Constants

Declare constants with `readonly`.

| Use                      | Avoid           |
| ------------------------ | --------------- |
| `readonly MAX_RETRIES=3` | `MAX_RETRIES=3` |

---

## Scope

### Outer scope assignments

Avoid assigning to outer scope variables from functions; document when unavoidable.

```bash
# Use (when unavoidable, document it)
# Sets: RESULT
function set_result() {
  RESULT="value"
}

# Avoid
function set_result() {
  RESULT="value" # modifies outer scope silently
}
```

---

### Subprocess variable scope

Variables modified inside pipelines or subshells don't affect the parent scope.

```bash
count=0
echo "a b c" | while read -r word; do
  ((count++)) # modified in subshell
done
echo "${count}" # still 0
```

---

### Subshell namespacing

Use unique variable names when code may run in subshells to avoid conflicts.

| Use                   | Avoid       |
| --------------------- | ----------- |
| `mylib_temp_file`     | `temp_file` |
| `backup_script_count` | `count`     |

---

### Temporary directory changes

Use a subshell for temporary `cd` to avoid affecting the parent shell.

| Use                      | Avoid                              |
| ------------------------ | ---------------------------------- |
| `(cd /some/dir && make)` | `cd /some/dir`<br>`make`<br>`cd -` |

---

### Process substitution

Use process substitution or `readarray` to avoid subshell scope issues.

```bash
# Use
while IFS= read -r line; do
  process "${line}"
done < <(command)

# Or
readarray -t lines < <(command)

# Avoid
command | while IFS= read -r line; do
  process "${line}"
done
```

---

## Quoting

### Quote expansions

Always quote variable and command expansions.

| Use             | Avoid         |
| --------------- | ------------- |
| `"${variable}"` | `${variable}` |
| `"$(command)"`  | `$(command)`  |

---

### Single quotes

Prefer single quotes over backslash escaping for literal strings.

| Use             | Avoid          |
| --------------- | -------------- |
| `'Hello World'` | `Hello\ World` |

---

### Intentional word splitting

Only omit quotes when word splitting is intentional.

```bash
# Intentional: split OPTIONS into separate arguments
OPTIONS="-l -a -h"
ls ${OPTIONS}

# Unintentional: always quote variables
filename="my file.txt"
cat "${filename}" # not: cat $filename
```

---

### Arrays over splitting

Use arrays instead of relying on word splitting for lists.

```bash
# Use
files=("file one.txt" "file two.txt")
cp "${files[@]}" dest/

# Avoid
files="file one.txt file two.txt"
cp ${files} dest/ # breaks on spaces
```

---

### Array expansion

Quote array expansions to preserve elements with spaces.

| Use             | Avoid         |
| --------------- | ------------- |
| `"${array[@]}"` | `${array[@]}` |

---

## Arguments

### Long options

Prefer long options for readability in scripts.

| Use                   | Avoid |
| --------------------- | ----- |
| `--recursive --force` | `-rf` |

---

### Parameter validation

Validate required parameters at the script level, not inside functions.

```bash
# Use (validate in main, before calling functions)
function main() {
  [[ -z "${1:-}" ]] && {
    echo "Usage: $0 <file>" >&2
    exit 1
  }
  process_file "${1}"
}

# Avoid (validation inside each function)
function process_file() {
  [[ -z "${1:-}" ]] && {
    echo "Missing file" >&2
    exit 1
  }
}
```

---

### Argument arrays

Build command arguments in arrays to handle quoting safely.

```bash
args=()
args+=(--flag)
args+=(--option "value")
command "${args[@]}"
```

---

## Tests

### Arithmetic

Use `((...))` for statements and `$((...))` for expressions.

| Use                           | Avoid                      |
| ----------------------------- | -------------------------- |
| `((i++))`                     | `let i++`                  |
| `$((x + 1))`                  | `expr $x + 1`              |
| `$((x + 1))`                  | `$[x + 1]`                 |
| `for ((i=1; i<=10; i++)); do` | `for i in $(seq 1 10); do` |
| `for i in {1..10}; do`        | `for i in $(seq 1 10); do` |

---

### Double brackets

Use `[[...]]`, not `[...]` (safer, supports globs and regex).

| Use                  | Avoid              |
| -------------------- | ------------------ |
| `[[ -f "${file}" ]]` | `[ -f "${file}" ]` |

---

### Equality operator

Use `==` for equality, not `=`.

| Use                         | Avoid                      |
| --------------------------- | -------------------------- |
| `[[ "${var}" == "value" ]]` | `[[ "${var}" = "value" ]]` |

---

### Literal matching

Quote the right-hand side to match literally instead of as a pattern. Unquoted RHS is treated as a glob pattern.

| Use                    | Avoid                |
| ---------------------- | -------------------- |
| `[[ ${a} == "${b}" ]]` | `[[ ${a} == ${b} ]]` |

---

### Explicit tests

Use explicit `-n` and `-z` tests for string checks.

| Use                 | Avoid              |
| ------------------- | ------------------ |
| `[[ -n "${var}" ]]` | `[[ "${var}" ]]`   |
| `[[ -z "${var}" ]]` | `[[ ! "${var}" ]]` |

---

### Exit code tests

Test command exit codes directly instead of capturing output.

| Use                               | Avoid                                   |
| --------------------------------- | --------------------------------------- |
| `if grep -q 'pattern' file; then` | `if [[ $(grep 'pattern' file) ]]; then` |

---

### Test command pitfalls

When using `[`: quote all expansions, escape `<` and `>`, use `&&`/`||` instead of `-a`/`-o`.

| Use                        | Avoid                  |
| -------------------------- | ---------------------- |
| `[ "${a}" = "${b}" ]`      | `[ $a = $b ]`          |
| `[ "${a}" \< "${b}" ]`     | `[ ${a} < ${b} ]`      |
| `[ "${a}" ] && [ "${b}" ]` | `[ "${a}" -a "${b}" ]` |

---

## Control flow

### Default case

Always include a default `*)` case in `case` statements.

```bash
case "${action}" in
  start) start_service ;;
  stop) stop_service ;;
  *)
    echo "Unknown action" >&2
    exit 1
    ;;
esac
```

---

### Negated conditions

Avoid `if ! condition` with an else branch; invert the logic instead.

```bash
# Use
if is_valid; then
  handle_valid
else
  handle_invalid
fi

# Avoid
if ! is_valid; then
  handle_invalid
else
  handle_valid
fi
```

---

### Intentional failures

Use `|| true` to allow commands to fail without triggering `set -e`.

| Use                           | Avoid               |
| ----------------------------- | ------------------- |
| `grep pattern file \|\| true` | `grep pattern file` |

---

### Simple conditionals

Use `&&`/`||` for simple one-line conditionals.

| Use                                | Avoid                                        |
| ---------------------------------- | -------------------------------------------- |
| `[[ -f "${f}" ]] && source "${f}"` | `if [[ -f "${f}" ]]; then source "${f}"; fi` |

---

### Check return values

Always check command return values with `$?` or `if`.

```bash
if ! cp source dest; then
  echo "Copy failed" >&2
  exit 1
fi
```

---

### Pipeline status

Use `PIPESTATUS` to check the exit code of each command in a pipeline.

```bash
cmd1 | cmd2 | cmd3
echo "${PIPESTATUS[@]}" # e.g., "0 1 0"
```

---

### Meaningful exit codes

Return distinct exit codes for different failure modes.

```bash
readonly E_SUCCESS=0
readonly E_INVALID_ARGS=1
readonly E_FILE_NOT_FOUND=2
readonly E_PERMISSION_DENIED=3
```

---

### Document exit codes

Document the meaning of each exit code for script users.

```bash
# Exit codes:
#   0 - Success
#   1 - Invalid arguments
#   2 - File not found
#   3 - Permission denied
```

---

### Standard exit codes

Follow conventions from `/usr/include/sysexits.h` when applicable.

---

## I/O

### Error messages

Send error messages to stderr.

| Use                | Avoid          |
| ------------------ | -------------- |
| `echo "error" >&2` | `echo "error"` |

---

### Stdout for data

Reserve stdout for machine-parsable output; use stderr for human messages.

```bash
function get_users() {
  echo "Fetching users..." >&2  # progress to stderr
  cat /etc/passwd | cut -d: -f1 # data to stdout
}
```

---

### Temporary files

Use `mktemp` to create temporary files securely.

| Use             | Avoid                |
| --------------- | -------------------- |
| `tmp=$(mktemp)` | `tmp=/tmp/myfile.$$` |

---

### File extensions

Use no extension for executables; use `.sh` or `.bash` for sourced libraries.

---

### Root file writes

Use `sudo tee` to write to files requiring root permissions. Redirection happens before `sudo`, in the unprivileged shell.

| Use                              | Avoid                       |
| -------------------------------- | --------------------------- |
| `echo "x" \| sudo tee /etc/file` | `sudo echo "x" > /etc/file` |

---

### SUID/SGID prohibition

Never use SUID/SGID on shell scripts; use `sudo` for privilege escalation.

---

### Absolute paths

Prefer absolute paths; prefix relative paths with `./`.

| Use                  | Avoid          |
| -------------------- | -------------- |
| `/usr/local/bin/app` | `app`          |
| `./local-script`     | `local-script` |

---

### Wildcard safety

Prefix wildcards with `./` to prevent filenames starting with `-` being parsed as options.

| Use          | Avoid      |
| ------------ | ---------- |
| `rm ./*.txt` | `rm *.txt` |

---

### File globbing

Use globs or `find -print0` instead of parsing `ls` output.

| Use                    | Avoid                      |
| ---------------------- | -------------------------- |
| `for f in ./*.txt; do` | `for f in $(ls *.txt); do` |

---

### Filename pattern matching

Use globs or `case` to filter filenames, not `grep`.

```bash
# Use
for file in ./*.txt; do
  process "${file}"
done

case "${filename}" in
  *.log) rotate_log "${filename}" ;;
  *.tmp) rm "${filename}" ;;
esac

# Avoid
ls | grep '\.txt$' | while read -r file; do
  process "${file}"
done
```

---

### Direct file input

Pass files directly to commands or use redirection.

| Use                   | Avoid                      |
| --------------------- | -------------------------- |
| `grep pattern < file` | `cat file \| grep pattern` |
| `grep pattern file`   | `cat file \| grep pattern` |

---

### Line-by-line reading

Use `while read` to iterate over lines. `for` splits on whitespace, not newlines.

| Use                           | Avoid                         |
| ----------------------------- | ----------------------------- |
| `while IFS= read -r line; do` | `for line in $(cat file); do` |

---

## Cleanup

### Exit trap

Use `trap` to run cleanup code on exit.

```bash
function cleanup() {
  rm -f "${tmp_file}"
}
trap cleanup EXIT
```

---

### Preserve exit code

Save the exit code at the start of trap handlers to preserve it.

```bash
function cleanup() {
  local exit_code="${?}"
  rm -f "${tmp_file}"
  exit "${exit_code}"
}
```

---

### Restore shell options

Restore modified `shopt` options when done.

```bash
shopt -s nullglob
# ... use nullglob ...
shopt -u nullglob
```

---

## Development

### Code comments

Comment non-obvious code to explain intent.

```bash
# Strip ANSI color codes from output before logging
clean_output="${output//\x1b\[[0-9;]*m/}"
```

---

### Function documentation

Document functions with their purpose, arguments, outputs, and return values.

```bash
# Compress and archive log files older than N days.
# Arguments:
#   $1 - Directory containing log files
#   $2 - Age threshold in days (default: 30)
# Outputs:
#   Writes archive path to stdout
# Returns:
#   0 on success, 1 on invalid arguments, 2 on compression failure
function archive_logs() {
  # ...
}
```

---

### Syntax check

Validate syntax with `bash -n` before running.

```bash
bash -n script.sh
```

---

### Debug tracing

Support optional debug tracing with a `TRACE` environment variable.

```bash
[[ "${TRACE}" ]] && set -x
```

---

## Sources

Compiled by [Christopher Boone](https://cboone.github.io). Based on some of each of the following:

- [BashGuide/Practices](https://mywiki.wooledge.org/BashGuide/Practices) — Greg's Wiki
- [Bash Best Practices](https://bertvv.github.io/cheat-sheets/Bash.html) — Bert Van Vreckem
- [bash-best-practices](https://github.com/imoisharma/bash_best_practices) — Moi Sharma
- [ShellCheck](https://www.shellcheck.net/) — optional checks enabled in `.shellcheckrc`
- [Unofficial Shell Scripting Stylesheet](https://tldp.org/LDP/abs/html/unofficialst.html) — ABS Guide
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
