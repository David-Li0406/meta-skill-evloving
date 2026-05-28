# Shell Script Anti-Patterns

This document catalogs common shell scripting mistakes and their correct alternatives.

## Critical Security Issues

### Command Injection via eval

**Anti-pattern:**
```bash
# DANGEROUS - allows arbitrary code execution
user_input="$1"
eval "echo ${user_input}"
```

**Fix:**
```bash
# Safe - no eval needed
user_input="$1"
echo "${user_input}"
```

**Why it matters:** `eval` executes arbitrary code. Input like `$(rm -rf /)` would be executed.

### Unquoted Variables in Destructive Commands

**Anti-pattern:**
```bash
# DANGEROUS - if file="* -rf", deletes everything
rm $file
rm -rf $dir/*
```

**Fix:**
```bash
# Safe - proper quoting
rm "${file}"
rm -rf "${dir:?}"/*  # :? prevents empty $dir from becoming /
```

**Why it matters:** Word splitting and glob expansion can cause unintended deletions.

### Command Injection via Unsanitized Input

**Anti-pattern:**
```bash
# DANGEROUS - user can inject commands
grep "$user_input" file.txt
```

**Fix:**
```bash
# Safe - use -- to end options, -F for literal matching
grep -F -- "${user_input}" file.txt
```

**Why it matters:** Input like `-e . /etc/passwd` would read sensitive files.

## Important Correctness Issues

### Piping to While (Subshell Problem)

**Anti-pattern:**
```bash
# BUG - count is 0 after loop because while runs in subshell
count=0
cat file.txt | while read line; do
  (( count++ ))
done
echo "${count}"  # Always 0!
```

**Fix:**
```bash
# Correct - redirect instead of pipe
count=0
while IFS= read -r line; do
  (( count++ ))
done < file.txt
echo "${count}"  # Correct value
```

**Why it matters:** Pipes create subshells; variable changes don't persist.

### Missing IFS and -r in read

**Anti-pattern:**
```bash
# BUG - mangles whitespace and backslashes
while read line; do
  echo "${line}"
done
```

**Fix:**
```bash
# Correct - preserves whitespace and backslashes
while IFS= read -r line; do
  echo "${line}"
done
```

**Why it matters:** Without `IFS=`, leading/trailing whitespace is stripped. Without `-r`, backslashes are interpreted.

### Using [ ] Instead of [[ ]]

**Anti-pattern:**
```bash
# Fragile - breaks on special characters
if [ $var = "value" ]; then
  # ...
fi
```

**Fix:**
```bash
# Robust - handles empty/special values
if [[ "${var}" == "value" ]]; then
  # ...
fi
```

**Why it matters:** `[` is an external command with word splitting issues; `[[` is a bash builtin with better handling.

### Arithmetic with $ Instead of (( ))

**Anti-pattern:**
```bash
# Wrong - string comparison, not numeric
if [ "$count" -gt "10" ]; then
  # ...
fi
```

**Fix:**
```bash
# Correct - proper arithmetic comparison
if (( count > 10 )); then
  # ...
fi
```

**Why it matters:** Arithmetic context handles numbers properly; string context can fail unexpectedly.

### Not Checking Command Success

**Anti-pattern:**
```bash
# BUG - continues even if cd fails
cd "$dir"
rm -rf *  # Deletes from wrong directory!
```

**Fix:**
```bash
# Safe - check or use &&
cd "${dir}" || exit 1
rm -rf ./*

# Or more explicit
if ! cd "${dir}"; then
  err "Failed to cd to ${dir}"
  exit 1
fi
```

**Why it matters:** Failed commands with destructive followers can cause data loss.

## Portability Issues

### Using Bashisms in /bin/sh Scripts

**Anti-pattern:**
```bash
#!/bin/sh
# BUG - [[ ]] is bash-only
if [[ -f "${file}" ]]; then
  # ...
fi
```

**Fix:**
```bash
#!/bin/sh
# Portable - POSIX-compliant
if [ -f "${file}" ]; then
  # ...
fi

# Or use bash if you need bash features
#!/bin/bash
```

**Why it matters:** Not all systems have bash as /bin/sh.

### Using mapfile/readarray (macOS incompatible)

**Anti-pattern:**
```bash
# Fails on macOS default bash
mapfile -t lines < file.txt
```

**Fix:**
```bash
# Portable - works everywhere
lines=()
while IFS= read -r line; do
  lines+=("${line}")
done < file.txt
```

**Why it matters:** macOS ships with bash 3.2, which lacks `mapfile`.

### Using Aliases in Scripts

**Anti-pattern:**
```bash
# Unreliable - aliases aren't expanded by default in scripts
alias ll='ls -la'
ll  # Doesn't work
```

**Fix:**
```bash
# Reliable - use functions
ll() {
  ls -la "$@"
}
ll  # Works
```

**Why it matters:** Script mode disables alias expansion for predictability.

## Style and Maintainability Issues

### Using Backticks for Command Substitution

**Anti-pattern:**
```bash
# Outdated - hard to nest, hard to read
result=`command1 \`command2\``
```

**Fix:**
```bash
# Modern - clean nesting
result="$(command1 "$(command2)")"
```

**Why it matters:** Backticks are deprecated; `$()` is clearer and easier to nest.

### Global Variables in Functions

**Anti-pattern:**
```bash
process() {
  result="processed"  # Pollutes global namespace
}
```

**Fix:**
```bash
process() {
  local result="processed"
  echo "${result}"
}
```

**Why it matters:** Global variables cause hard-to-track bugs; `local` prevents pollution.

### Inconsistent Quoting

**Anti-pattern:**
```bash
# Inconsistent - some quoted, some not
echo $name
echo "${age}"
process $file
```

**Fix:**
```bash
# Consistent - always quote variables
echo "${name}"
echo "${age}"
process "${file}"
```

**Why it matters:** Inconsistent quoting leads to word-splitting bugs.

### Missing Error Messages

**Anti-pattern:**
```bash
# Silent failure - user has no idea what went wrong
if [[ ! -f "${config}" ]]; then
  exit 1
fi
```

**Fix:**
```bash
# Informative - user knows what to fix
if [[ ! -f "${config}" ]]; then
  err "Configuration file not found: ${config}"
  exit 1
fi
```

**Why it matters:** Silent failures waste debugging time.

## Temporary File Issues

### Predictable Temp File Names

**Anti-pattern:**
```bash
# DANGEROUS - predictable, race condition
tmp_file="/tmp/myapp.tmp"
echo "${data}" > "${tmp_file}"
```

**Fix:**
```bash
# Safe - unique, unpredictable
tmp_file="$(mktemp)" || exit 1
trap 'rm -f "${tmp_file}"' EXIT
echo "${data}" > "${tmp_file}"
```

**Why it matters:** Predictable names enable symlink attacks.

### No Cleanup Trap

**Anti-pattern:**
```bash
# Leaves temp files on error
tmp_file="$(mktemp)"
process "${tmp_file}"
rm "${tmp_file}"  # Never reached if process fails
```

**Fix:**
```bash
# Always cleans up
tmp_file="$(mktemp)"
trap 'rm -f "${tmp_file}"' EXIT
process "${tmp_file}"
```

**Why it matters:** Untrapped errors leave garbage; traps ensure cleanup.

## Array Handling Issues

### Unquoted Array Expansion

**Anti-pattern:**
```bash
# BUG - breaks on elements with spaces
for file in ${files[@]}; do
  process "${file}"
done
```

**Fix:**
```bash
# Correct - preserves elements
for file in "${files[@]}"; do
  process "${file}"
done
```

**Why it matters:** Unquoted expansion splits on spaces within elements.

### Using $* Instead of $@

**Anti-pattern:**
```bash
# BUG - all arguments become one string
process_all() {
  for arg in "$*"; do
    process "${arg}"
  done
}
```

**Fix:**
```bash
# Correct - preserves argument boundaries
process_all() {
  for arg in "$@"; do
    process "${arg}"
  done
}
```

**Why it matters:** `$*` joins all arguments; `$@` preserves them.

## Summary Table

| Anti-Pattern | Risk Level | Fix |
|--------------|------------|-----|
| `eval` with user input | Critical | Remove eval, use safe alternatives |
| Unquoted `rm $var` | Critical | Quote: `rm "${var}"` |
| Pipe to while | Important | Redirect: `while ... done < file` |
| `[ ]` instead of `[[ ]]` | Important | Use `[[ ]]` for tests |
| Missing `IFS= read -r` | Important | Always use `IFS= read -r` |
| Backticks | Minor | Use `$()` |
| Missing `local` | Minor | Add `local` to function variables |
| No error messages | Minor | Add informative error output |
