---
name: nushell
description: Write and debug Nushell scripts, pipelines, and commands. Also build Nushell plugins in Rust. Use when working with .nu files, writing Nushell code, converting bash to Nushell, creating custom Nushell commands/plugins, or when the user mentions nushell.
---

# Nushell

## The Paradigm Shift: Text Streams → Structured Data

Nushell fundamentally reimagines shell design. Traditional Unix shells pass unstructured text between commands, requiring grep/awk/sed to parse strings. Nushell passes structured, typed data—tables, records, lists—eliminating brittle text parsing.

Stop parsing strings, start solving problems.

```nu
# POSIX: Parse text, hope format doesn't change
ps aux | grep 'nu' | awk '{print $2, $11}'

# Nushell: Query structured data directly
ps | where name =~ 'nu' | select pid name
```

The same verbs (`where`, `select`, `sort-by`, `group-by`) work universally across all data sources—filesystem, processes, JSON APIs, CSV files. Learn once, apply everywhere.

## Core Philosophy

- Structured data: Commands output tables/records/lists, not raw text
- Type safety: Data has types; errors caught early
- Immutability: Variables immutable by default (`mut` for mutable)
- Cross-platform: Internal commands work identically on Linux/macOS/Windows
- Separation of concerns: Commands produce data; pipeline transforms it; renderer displays it

## Essential Syntax

```nu
# Variables (immutable by default)
let name = "value"
mut counter = 0
$counter += 1

# String interpolation
$"Hello ($name), count: ($counter)"

# Pipeline input variable
"text" | { $in | str upcase }    # $in holds pipeline input

# Conditionals
if $condition { ... } else { ... }

# Loops
for item in $list { ... }
while $condition { ... }

# Pattern matching
match $value {
    "a" => { ... }
    "b" | "c" => { ... }
    _ => { ... }
}

# Closures
{|x| $x * 2 }

# Custom commands with typed parameters
def greet [name: string, --loud (-l)] {
    if $loud { $name | str upcase } else { $name }
}
```

## Pipeline Architecture: Input → Filter → Output

```nu
# Input (source): generates data
ls                              # Produces table of files

# Filter: transforms data
| where size > 1mb              # Keep rows matching condition
| select name size              # Choose columns
| sort-by size --reverse        # Order by column

# Output (sink): consumes data
| first 5                       # Take top 5
| save large-files.json         # Write to file (or display)
```

## Data Types

| Type      | Example                          | Notes                                  |
| --------- | -------------------------------- | -------------------------------------- |
| string    | `"hello"`                        | Interpolation: `$"value: ($var)"`      |
| int       | `42`, `0xff`                     | Hex, octal (`0o755`), binary (`0b101`) |
| float     | `3.14`                           |                                        |
| bool      | `true` / `false`                 |                                        |
| list      | `[1, 2, 3]`                      | Access: `$list.0` or \`$list           |
| record    | `{name: "x", value: 1}`          | Access: `$rec.name`                    |
| table     | `[[col1, col2]; [a, 1], [b, 2]]` | List of records                        |
| duration  | `1hr + 30min`                    | Semantic units                         |
| filesize  | `10mb`                           | Semantic units                         |
| datetime  | `2024-01-15`                     | Native date operations                 |
| range     | `1..10` or `1..<10`              | Inclusive / exclusive                  |
| closure   | \`{                              | x                                      |
| cell-path | `$table.0.name`                  | Path into data structures              |
| nothing   | `null`                           |                                        |

## Common Commands Quick Reference

Files & Navigation:

```nu
ls **/*.rs                    # Recursive glob (no find needed!)
cd ~/projects
open file.json                # Auto-parses by extension
save output.json              # Saves structured data
```

Data Manipulation:

```nu
where condition               # Filter rows
select col1 col2              # Choose columns
get column                    # Extract as list (not table)
sort-by column                # Sort
group-by column               # Aggregate
each {|x| transform $x}       # Transform items
update col { new_value }      # Modify column
```

Text Processing:

```nu
lines                         # Split text into lines
split row ","                 # Split string
parse "{name}: {value}"       # Extract with pattern
from json / to json           # Format conversion
```

## External Commands: Bridging Worlds

```nu
# External commands run automatically, output captured as text
git status

# Use ^ to force external version (bypass internal command)
^ls -la                       # System ls, not Nushell ls

# Capture stdout, stderr, and exit_code with complete
let result = (git push | complete)
if $result.exit_code != 0 {
    print $"Error: ($result.stderr)"
}

# Parse external output into structured data
docker ps --format json | from json
```

## Bash to Nushell Translation

| Bash                      | Nushell                                    |
| ------------------------- | ------------------------------------------ |
| `$VAR`                    | `$env.VAR` (env) or `$var` (local)         |
| `export VAR=x`            | `$env.VAR = "x"`                           |
| `$(cmd)`                  | `(cmd)`                                    |
| `cmd \| grep pattern`     | `cmd \| where col =~ pattern`              |
| `cmd \| awk '{print $1}'` | `cmd \| get column` or `cmd \| select col` |
| `cmd \| wc -l`            | `cmd \| length`                            |
| `[ -f file ]`             | `("file" \| path exists)`                  |
| `for i in ...; do`        | `for i in ... { }`                         |
| `VAR=x cmd`               | `with-env {VAR: x} { cmd }`                |
| `cmd > file`              | `cmd \| save file`                         |
| `cmd 2>&1`                | `cmd \| complete`                          |

## Error Handling

```nu
# Try/catch
try {
    risky-operation
} catch {|e|
    print $"Error: ($e.msg)"
}

# Optional chaining (safe navigation)
$record.field?                # Returns null if missing
$record | get -i field        # Same with command
```

## Critical: Pipeline Input vs Parameters

Pipeline input (`$in`) is NOT interchangeable with function parameters:

```nu
# ✗ WRONG - treats $in as first parameter
def my-func [list: list, value: any] {
    $list | append $value
}

# ✓ CORRECT - declares pipeline signature
def my-func [value: any]: list -> list {
    $in | append $value
}

# Usage
[1 2 3] | my-func 4  # Works correctly
```

Why this matters:

- Pipeline input can be lazily evaluated (streaming)
- Parameters are eagerly evaluated (loaded into memory)
- Different calling conventions entirely

### Type Signatures

```nu
def func [x: int] { ... }                    # params only
def func []: string -> int { ... }           # pipeline only
def func [x: int]: string -> int { ... }     # both
```

## Row Conditions vs Closures

Many commands accept either a row condition or a closure:

```nu
# Row condition - auto expands $it
$table | where size > 100           # Expands to: $it.size > 100
$table | where name =~ "test"

# Closure - explicit parameter
$table | where {|row| $row.size > 100}
$list | where {$in > 10}

# Closures can be stored and reused (call with do)
let big_files = {|row| $row.size > 1mb}
ls | where {|f| do $big_files $f}
```

## Common Gotchas

1. Parentheses for subexpressions: `(ls | length)` not `ls | length` in expressions
2. Closures need parameter: `each {|it| $it.name }` not `each { $it.name }`
3. `$in` for pipeline input: `"text" | { $in | str upcase }`
4. External output is text: Pipe through `lines` or `from json` to structure
5. Semicolons separate statements on same line, not for line endings
6. `^` prefix: Force system command over Nushell builtin
7. `each` on records: Only runs once! Use `items` or `transpose` instead
8. Optional fields: Use `$record.field?` to avoid errors on missing fields

## References

- [commands.md](references/commands.md) - Command reference and POSIX translations
- [data-types.md](references/data-types.md) - Structured data handling (records, tables, lists, type conversions)
- [pipelines.md](references/pipelines.md) - Advanced pipeline patterns, functional programming, streaming
- [interop.md](references/interop.md) - External command integration, `complete`, `extern`
- [scripting.md](references/scripting.md) - Custom commands, modules, `main`, control flow
- [production.md](references/production.md) - Testing, validation, logging, error handling patterns

Plugin Development (for building Nushell plugins in Rust):

- [plugins.md](references/plugins.md) - Complete guide to building Nushell plugins
- Template: `scripts/init_plugin.py` and `assets/plugin-template/`

## Running Nushell

```bash
nu                           # Interactive shell
nu script.nu                 # Run script
nu -c 'command'              # One-liner
```

## Nushell Book Lookup

```bash
curl -s "https://raw.githubusercontent.com/nushell/nushell.github.io/main/book/<filename>"
```

| Filename                        | Description                                                                            |
| ------------------------------- | -------------------------------------------------------------------------------------- |
| `3rdpartyprompts.md`            | Configuring third-party prompt tools (Starship, Oh My Posh)                            |
| `advanced.md`                   | Dataframes, metadata, parallelism, and exploration tools                               |
| `aliases.md`                    | Creating command shortcuts and custom replacements                                     |
| `background_jobs.md`            | Thread-based background job management                                                 |
| `cheat_sheet.md`                | Quick reference for Nushell syntax and commands                                        |
| `coloring_and_theming.md`       | Customizing interface colors and visual themes                                         |
| `coming_from_bash.md`           | Bash to Nushell command equivalents                                                    |
| `coming_from_cmd.md`            | CMD.EXE to Nushell migration guide                                                     |
| `coming_from_powershell.md`     | PowerShell to Nushell syntax differences                                               |
| `coming_to_nu.md`               | Mapping other languages/shells to Nushell                                              |
| `configuration.md`              | Startup config files, env vars, and settings                                           |
| `control_flow.md`               | Conditionals, loops, and error handling                                                |
| `creating_errors.md`            | Custom error messages with `error make`                                                |
| `custom_commands.md`            | Defining reusable commands with `def`                                                  |
| `custom_completions.md`         | Tab completions for command arguments                                                  |
| `dataframes.md`                 | Fast columnar data processing with Polars                                              |
| `default_shell.md`              | Setting Nushell as your default terminal shell                                         |
| `design_notes.md`               | Internal design and architecture explanations                                          |
| `directory_stack.md`            | Directory stack for switching between paths                                            |
| `environment.md`                | Managing environment variables                                                         |
| `explore.md`                    | Table pager (like `less`) for interactively navigating structured data                 |
| `externs.md`                    | Using `extern` to define signatures for external commands (completions, type checking) |
| `getting_started.md`            | First steps with Nushell                                                               |
| `hooks.md`                      | Configuring hooks that run at predefined shell events (prompt, env changes)            |
| `how_nushell_code_gets_run.md`  | Strict separation of parsing and evaluation stages (no `eval`)                         |
| `installation.md`               | Installing Nushell on various platforms                                                |
| `line_editor.md`                | Reedline configuration: keybindings, history, menus, editing modes                     |
| `loading_data.md`               | Opening and parsing files (JSON, CSV, etc.)                                            |
| `metadata.md`                   | How Nu attaches metadata/tags to pipeline values for better errors                     |
| `modules.md`                    | Modules as containers for commands, aliases, and constants                             |
| `modules/creating_modules.md`   | Creating modules: exports, file/directory organization, submodules                     |
| `modules/using_modules.md`      | Importing modules: installation, import patterns, selective imports, hiding            |
| `moving_around.md`              | Filesystem navigation: `ls`, `cd`, `mkdir`, `mv`, `cp`, `rm`, globs                    |
| `navigating_structured_data.md` | Cell-paths, `get`, `select`, and optional operators for nested data                    |
| `nu_as_a_shell.md`              | Shell features: configuration, env vars, I/O, hooks, line editing                      |
| `nu_fundamentals.md`            | Core concepts and mental model                                                         |
| `nushell_map.md`                | Command equivalents: SQL, PowerShell, Bash, .NET LINQ                                  |
| `nushell_map_functional.md`     | Command equivalents: Clojure, OCaml/Elm, Haskell                                       |
| `nushell_map_imperative.md`     | Command equivalents: Python, Kotlin, C++, Rust                                         |
| `nushell_operator_map.md`       | Operator equivalents: SQL, Python, C#, PowerShell, Bash                                |
| `operators.md`                  | Math, logic, string operators, precedence, and spread operator (`...`)                 |
| `overlays.md`                   | Activating/deactivating layers of commands, aliases, env vars (like venvs)             |
| `parallelism.md`                | Parallel execution with `par-each`                                                     |
| `pipelines.md`                  | Pipeline system extending Unix pipes to structured data types                          |
| `plugins.md`                    | Installing, registering, and managing plugins (separate executables)                   |
| `programming_in_nu.md`          | Custom commands, variables, operators, scripts, modules, overlays                      |
| `quick_tour.md`                 | Rapid introduction to key features                                                     |
| `regular_expressions.md`        | Regex implementation using rust-lang/regex crate                                       |
| `running_externals.md`          | Running external commands with caret (`^`) sigil override                              |
| `scripts.md`                    | Scripts with parameters, custom commands, subcommands, shebangs                        |
| `sorting.md`                    | Sorting data with `sort-by` and custom comparators                                     |
| `special_variables.md`          | Special variables: `$nu`, `$env`, `$in`, `$it` for config and pipeline data            |
| `standard_library.md`           | Stdlib: assertions, help, JSON/XML handling, logging (pre-loaded)                      |
| `stdout_stderr_exit_codes.md`   | Handling output streams and exit codes                                                 |
| `style_guide.md`                | Code formatting and naming conventions                                                 |
| `table_of_contents.md`          | Comprehensive documentation index for the Nushell book                                 |
| `testing.md`                    | Writing tests with stdlib assertions: Nupm, standalone scripts, frameworks             |
| `thinking_in_nu.md`             | Mental model shift: fundamental concepts distinguishing Nu from other shells           |
| `types_of_data.md`              | All data types: basic (int, string) and structured (list, table, record)               |
| `variables.md`                  | Variables: `let` (immutable), `mut` (mutable), `const` (constant)                      |
| `working_with_lists.md`         | List creation, modification, iteration, filtering, and type conversion                 |
| `working_with_records.md`       | Records (key-value maps): creation, modification, iteration, access                    |
| `working_with_strings.md`       | String formats, manipulation, parsing, comparison, and conversion                      |
| `working_with_tables.md`        | Tables: sorting, selecting, extracting, and modifying data                             |
