# Nushell Scripting and Automation

## Configuration Files

Nushell's configuration lives in the config directory:

```nu
$nu.default-config-dir        # Shows config path
# Linux: ~/.config/nushell/
# macOS: ~/Library/Application Support/nushell/
# Windows: %APPDATA%\nushell\
```

### Startup Sequence

1. `env.nu` - Loaded first, sets environment variables
2. `config.nu` - Main configuration (aliases, commands, settings)

```nu
# env.nu - Environment setup
$env.EDITOR = "nvim"
$env.PATH = ($env.PATH | prepend "~/.local/bin")

# config.nu - Commands and settings
alias ll = ls -l
def greet [name: string] { $"Hello, ($name)!" }
```

## Custom Commands with def

### Basic Structure

```nu
def command-name [
    required_arg: type              # Required positional
    optional_arg?: type             # Optional positional (?)
    --flag (-f): type               # Named flag with short form
    --switch (-s)                   # Boolean switch (no type = bool)
    ...rest: type                   # Rest arguments (variadic)
] -> return_type {
    # Body
}
```

### Typed Parameters

```nu
def process-files [
    pattern: glob                   # Glob pattern
    --extension (-e): string = "txt" # With default
    --recursive (-r)                # Boolean flag
    --max-size: filesize            # Typed value
] {
    let files = if $recursive {
        glob $"**/*($pattern)"
    } else {
        glob $pattern
    }

    $files | where {|f| ($f | path type) == "file"}
           | if $max_size != null { where size < $max_size } else { $in }
}
```

### Wrapped Commands (--wrapped)

Use `--wrapped` to pass arguments verbatim to external commands without Nushell parsing flags:

```nu
# Without --wrapped: FAILS - Nushell parses -s as flag to wrapper
def my-wrapper [...args: string] { ^tool ...$args }
my-wrapper cmd -s value  # Error: unknown flag -s

# With --wrapped: WORKS - args passed through unparsed  
def --wrapped my-wrapper [...args: string] { ^tool ...$args }
my-wrapper cmd -s value  # Runs: tool cmd -s value
```

Common pattern for CLI wrappers:

```nu
def --wrapped git-safe [...args: string] {
    let result = (^git ...$args | complete)
    if $result.exit_code != 0 { error make { msg: $result.stderr } }
    $result.stdout
}
```

Note: Rest args are always strings with `--wrapped`. Convert types explicitly: `--timeout ($seconds | into string)`

### Documentation

```nu
# Documentation appears in help
def greet [
    name: string   # The name to greet
    --loud (-l)    # Use uppercase
] -> string {
    if $loud { $name | str upcase } else { $name }
}

# help greet shows:
# Usage: greet <name> {flags}
# Parameters:
#   name <string>: The name to greet
# Flags:
#   -l, --loud: Use uppercase
```

## Scripts with main

A script can become a CLI tool by defining `main`:

```nu
#!/usr/bin/env nu
# deploy.nu

def main [
    environment: string@environments  # Tab-completable
    --dry-run (-n)                    # Preview only
    --verbose (-v)                    # Extra output
] {
    if $verbose { print $"Deploying to ($environment)..." }

    if $dry_run {
        print "Dry run - no changes made"
        return
    }

    # Actual deployment logic
    deploy-to $environment
}

def environments [] {
    ["staging", "production", "development"]
}

def deploy-to [env: string] {
    # ...
}
```

Run with: `nu deploy.nu production --verbose`

### Subcommands

```nu
# tool.nu - Multi-command CLI

def main [] {
    help main
}

def "main build" [target?: string] {
    # nu tool.nu build [target]
}

def "main test" [--coverage (-c)] {
    # nu tool.nu test --coverage
}

def "main deploy" [env: string] {
    # nu tool.nu deploy staging
}
```

### Enriching Help with Attributes

Use attributes to add examples and metadata to commands:

```nu
# Initialize the project
@category project
@example "Basic init" { my-tool init }
@example "With path" { my-tool init --path ./custom }
def "main init" [
    --path (-p): string  # Custom project path
]: nothing -> nothing {
    # ...
}
```

Available attributes:

- `@category <name>` - Command category
- `@example "desc" { code }` - Example (with optional `--result`)
- `@search-terms <terms>` - Additional search terms
- `@deprecated "msg"` - Mark as deprecated

Type signatures improve help output:

```nu
def "main status" []: nothing -> record { ... }  # Shows: nothing -> record
def "main list" []: nothing -> table { ... }     # Shows: nothing -> table
```

## Control Flow

### Conditionals

```nu
if $condition {
    action1
} else if $other {
    action2
} else {
    action3
}

# Inline ternary-style
let result = if $x > 0 { "positive" } else { "non-positive" }
```

### Pattern Matching

```nu
match $value {
    "start" => { start-process }
    "stop" | "kill" => { stop-process }  # Multiple patterns
    $x if $x > 100 => { print "large" }  # Guards
    {name: $n, age: $a} => { print $"($n) is ($a)" }  # Destructuring
    [$first, ..$rest] => { print $"First: ($first)" }  # List patterns
    _ => { print "unknown" }              # Wildcard
}
```

### Loops

```nu
# For loop
for item in $list {
    print $item
}

# While loop
mut count = 0
while $count < 10 {
    $count += 1
}

# Loop with break
loop {
    let input = (input "Continue? (y/n): ")
    if $input == "n" { break }
}

# Functional alternatives (preferred)
$list | each {|item| process $item }
$list | where condition
$list | reduce {|it, acc| $acc + $it }
```

## Error Handling

### try/catch

```nu
try {
    risky-operation
} catch {|err|
    print $"Error: ($err.msg)"
    # Optional: re-throw
    # error make $err
}
```

### Creating Errors

```nu
def divide [a: int, b: int] {
    if $b == 0 {
        error make {
            msg: "Division by zero"
            label: {
                text: "denominator cannot be zero"
                span: (metadata $b).span
            }
        }
    }
    $a / $b
}
```

## Modules

### Creating a Module

```nu
# utils.nu
export def greet [name: string] {
    $"Hello, ($name)!"
}

export def farewell [name: string] {
    $"Goodbye, ($name)!"
}

# Private (not exported)
def internal-helper [] {
    # ...
}
```

### Using Modules

```nu
# Import all exports
use utils.nu

# Import specific items
use utils.nu [greet]

# Import with prefix
use utils.nu *

# In config.nu for persistent availability
use ~/.config/nushell/modules/utils.nu
```

### Module Directory Structure

```
~/.config/nushell/
├── env.nu
├── config.nu
└── modules/
    ├── git.nu
    ├── docker.nu
    └── project/
        ├── mod.nu      # Main module file
        ├── build.nu
        └── deploy.nu
```

## Aliases vs def

| Feature             | alias | def |
| ------------------- | ----- | --- |
| Simple substitution | ✓     | ✓   |
| Parameters          | ✗     | ✓   |
| Logic/conditionals  | ✗     | ✓   |
| Type checking       | ✗     | ✓   |
| Documentation       | ✗     | ✓   |
| Pipes in definition | ✗     | ✓   |

```nu
# alias: Simple shortcuts
alias ll = ls -l
alias gst = git status
alias dc = docker compose

# def: Anything more complex
def ll [path?: string] {
    ls -l ($path | default ".")
}
```

## Best Practices

### Naming Conventions

```nu
# Commands: kebab-case
def process-files [] {}
def build-project [] {}

# Variables: snake_case
let file_count = 10
mut total_size = 0

# Flags: --kebab-case with -short
def cmd [--output-dir (-o): string] {}
```

### Idiomatic Patterns

```nu
# Prefer pipelines over loops
# Bad
mut result = []
for item in $list {
    $result = ($result | append (transform $item))
}

# Good
$list | each {|item| transform $item }

# Use early returns for validation
def process [path: string] {
    if not ($path | path exists) {
        error make {msg: "Path not found"}
    }

    # Main logic here
}

# Use default instead of if/else for simple cases
$value | default "fallback"

# Chain with null-safe access
$config.database?.host? | default "localhost"
```

### Script Template

```nu
#!/usr/bin/env nu
# script-name.nu - Brief description
#
# Usage: nu script-name.nu [options] <args>

# Constants
const VERSION = "1.0.0"

# Main entry point
def main [
    input: string       # Input file or value
    --output (-o): string = "output.txt"  # Output path
    --verbose (-v)      # Enable verbose output
    --version           # Show version
] {
    if $version {
        print $VERSION
        return
    }

    if $verbose { print $"Processing ($input)..." }

    let result = process-input $input

    $result | save $output

    if $verbose { print $"Saved to ($output)" }
}

def process-input [input: string] {
    # Implementation
}
```
