# External Command Interoperability

## Execution Basics

Any unrecognized command is executed as an external program:

```nu
git status                    # Runs external git
cargo build                   # Runs external cargo
```

Output is captured as text (byte stream interpreted as UTF-8).

## The Caret Escape Hatch (^)

Nushell provides internal implementations of common commands (`ls`, `ps`, `cp`, `rm`, etc.) that produce structured output. To explicitly run the system version:

```nu
ls                            # Nushell's ls (structured table)
^ls                           # System /bin/ls (text output)

^ls -la                       # System ls with flags
^ps aux                       # System ps (text, not table)
```

Use `^` when:

- You need system-specific flags not supported by Nushell
- A script requires exact POSIX behavior
- You're piping to another external command expecting text

## Capturing Output with complete

For robust error handling, use `complete` to capture stdout, stderr, and exit code as a structured record:

```nu
let result = (git push | complete)

# result is a record:
# {
#   stdout: "..."
#   stderr: "..."
#   exit_code: 0
# }

if $result.exit_code != 0 {
    print $"Push failed: ($result.stderr)"
    exit 1
}

print $result.stdout
```

### Pattern: Safe External Command Wrapper

```nu
def git-safe [...args: string] {
    let result = (^git ...$args | complete)
    if $result.exit_code != 0 {
        error make {msg: $"git ($args | str join ' ') failed: ($result.stderr)"}
    }
    $result.stdout
}
```

## Parsing External Output

External commands output text. Transform to structured data:

### Lines → List

```nu
# Split text into list of strings
^find . -name "*.txt" | lines
```

### Split Columns

```nu
# Delimited data
^cat /etc/passwd | lines | split column ":" user x uid gid info home shell
```

### Parse with Patterns

```nu
# Regex-like extraction
^uptime | parse "load average: {one}, {five}, {fifteen}"

# Result: [{one: "1.23", five: "0.89", fifteen: "0.72"}]
```

### From Structured Formats

```nu
# JSON output (many modern tools support this)
docker ps --format json | from json
kubectl get pods -o json | from json | get items
gh pr list --json number,title | from json

# Other formats
curl -s https://api.example.com/data.yaml | from yaml
```

## Defining Typed Signatures with extern

For frequently used external commands, define a full typed signature to get:

- Parse-time type checking
- Context-aware completions
- Proper syntax highlighting

```nu
# Basic extern
extern "git" [
    subcommand: string
    ...args: string
]

# Detailed extern with flags
extern "docker run" [
    --detach (-d)                    # Run in background
    --interactive (-i)               # Keep STDIN open
    --tty (-t)                       # Allocate pseudo-TTY
    --rm                             # Remove container on exit
    --name: string                   # Container name
    --volume (-v): string            # Bind mount
    --env (-e): string               # Environment variable
    --publish (-p): string           # Port mapping
    image: string                    # Image name
    ...cmd: string                   # Command to run
]

# Now get completions and type checking for docker run!
docker run -it --rm -v (pwd):/app node:latest npm test
```

### extern with Custom Completions

```nu
# Define completion function
def git-branches [] {
    ^git branch --format='%(refname:short)' | lines
}

# Use in extern
extern "git checkout" [
    branch: string@git-branches      # Tab-completes branch names!
]
```

## Sourcing Foreign Shell Scripts

Some tools require sourcing bash scripts (e.g., Python venvs, nvm, direnv).

### Pattern: Capture Environment Changes

```nu
# Activate Python venv and capture env changes
def activate-venv [path: string] {
    let before = (^env | lines | sort)
    let after = (bash -c $"source ($path)/bin/activate && env" | lines | sort)

    # Parse and apply new/changed variables
    $after | each {|line|
        let parts = ($line | split row "=" | first 2)
        if ($parts | length) == 2 {
            let key = $parts.0
            let value = $parts.1
            # Skip readonly vars
            if $key not-in ["BASH_FUNC_*", "_"] {
                load-env {($key): $value}
            }
        }
    }
}
```

### Using overlay for Temporary Environments

```nu
# Run command in modified environment
with-env {RUST_BACKTRACE: "1"} { cargo test }

# Or use overlay for scope
overlay use custom-env.nu
# ... work in modified environment ...
overlay hide custom-env
```

## Interop Patterns Summary

| Scenario                | Approach                       |
| ----------------------- | ------------------------------ |
| Run external command    | Just type it: `git status`     |
| Force system version    | Use `^`: `^ls -la`             |
| Capture errors          | `cmd \| complete`              |
| Parse delimited text    | `lines \| split column`        |
| Parse structured format | `from json`, `from yaml`, etc. |
| Extract with pattern    | `parse "{field}: {value}"`     |
| Add types to external   | `extern "cmd" [args...]`       |
| Source bash script      | Capture env diff pattern       |

## Common External Command Recipes

```nu
# Git: files changed in last commit
^git diff --name-only HEAD~1 | lines

# Docker: running containers with memory
docker ps --format json | from json | select Names State.Status | rename name status

# Kubernetes: pods not running
kubectl get pods -o json | from json | get items | where status.phase != "Running"

# AWS: list S3 buckets with size
aws s3 ls --output json | from json | each {|b| {name: $b.Name, created: $b.CreationDate}}

# jq alternative (nu can replace most jq usage)
curl -s https://api.github.com/users/nushell | from json | select login name public_repos
```
