#!/usr/bin/env nu
# Shared helpers for imp bundle/skill management scripts
#
# Provides utilities for git repository detection, colored output,
# validation helpers, and directory operations.

# Find project root, escaping submodules to parent repo
export def find-project-root []: nothing -> string {
    let root = (do { git rev-parse --show-toplevel } | complete)
    if $root.exit_code != 0 {
        error make { msg: "not in a git repository" }
    }

    let superproject = (do { git rev-parse --show-superproject-working-tree } | complete)
    if $superproject.exit_code == 0 and ($superproject.stdout | str trim | is-not-empty) {
        $superproject.stdout | str trim
    } else {
        $root.stdout | str trim
    }
}

# Get the nix/bundles directory path, validating it exists
export def init-bundle-dir []: nothing -> string {
    let root = find-project-root
    let bundle_dir = $"($root)/nix/bundles"
    if not ($bundle_dir | path exists) {
        error make { msg: $"no nix/bundles directory found in ($root)" }
    }
    $bundle_dir
}

# Wrap text in ANSI red
export def color-red [
    text: string  # Text to colorize
]: nothing -> string {
    $"(ansi red)($text)(ansi reset)"
}

# Wrap text in ANSI green
export def color-green [
    text: string  # Text to colorize
]: nothing -> string {
    $"(ansi green)($text)(ansi reset)"
}

# Wrap text in ANSI yellow
export def color-yellow [
    text: string  # Text to colorize
]: nothing -> string {
    $"(ansi yellow)($text)(ansi reset)"
}

# Wrap text in ANSI cyan
export def color-cyan [
    text: string  # Text to colorize
]: nothing -> string {
    $"(ansi cyan)($text)(ansi reset)"
}

# Shorten path by replacing home directory with ~
export def shorten-path [
    path: string  # Path to shorten
]: nothing -> string {
    let home = $env.HOME
    if ($path | str starts-with $home) {
        $path | str replace $home "~"
    } else {
        $path
    }
}

# Print error message and throw (catchable in tests)
export def die [
    msg: string  # Error message to display
] {
    error make {
        msg: (color-red $"error: ($msg)")
    }
}

# Print warning to stderr
export def warn [
    msg: string  # Warning message to display
]: nothing -> nothing {
    print -e (color-yellow $"warning: ($msg)")
}

# Print success message
export def ok [
    msg: string  # Success message to display
]: nothing -> nothing {
    print (color-green $msg)
}

# Print info message
export def info [
    msg: string  # Info message to display
]: nothing -> nothing {
    print (color-cyan $msg)
}

# Assert that a required argument is not empty
export def require-arg [
    value: string  # Value to check
    name: string   # Name for error message
] {
    if ($value | is-empty) {
        error make {
            msg: $"($name) required"
            label: {
                text: "missing required argument"
                span: (metadata $value).span
            }
        }
    }
}

# Assert that a command is available in PATH
export def require-cmd [
    cmd: string    # Command name to check
    desc?: string  # Description for error message
] {
    let description = $desc | default $cmd
    if (which $cmd | is-empty) {
        error make {
            msg: $"($description) required"
            label: {
                text: "command not found"
                span: (metadata $cmd).span
            }
        }
    }
}

# Assert that a directory exists
export def require-dir [
    path: string  # Path to check
] {
    if not ($path | path exists) or (($path | path type) != "dir") {
        error make {
            msg: $"($path) does not exist"
            label: {
                text: "directory not found"
                span: (metadata $path).span
            }
        }
    }
}

# Assert that a directory does not exist
export def require-no-dir [
    path: string  # Path to check
] {
    if ($path | path exists) and (($path | path type) == "dir") {
        error make {
            msg: $"($path) already exists"
            label: {
                text: "directory already exists"
                span: (metadata $path).span
            }
        }
    }
}

# List subdirectory names in a path
export def list-subdirs [
    path: string  # Directory to list
]: nothing -> list<string> {
    if not ($path | path exists) {
        []
    } else {
        ls $path
        | where type == dir
        | get name
        | each { path basename }
    }
}

# Check if directory has subdirectories or symlinks
export def has-subdirs [
    path: string  # Directory to check
]: nothing -> bool {
    if not ($path | path exists) {
        false
    } else {
        (ls $path | where type == dir or type == symlink | length) > 0
    }
}

# Parse YAML frontmatter from a file (between --- delimiters)
export def parse-frontmatter [
    path: string  # Path to file with frontmatter
]: nothing -> record {
    if not ($path | path exists) {
        return {}
    }

    let content = open $path --raw
    let lines = $content | lines

    if ($lines | length) == 0 or ($lines | first) != "---" {
        return {}
    }

    let rest = $lines | skip 1
    let end_idx = $rest | enumerate | where item == "---" | first | get index?

    if ($end_idx | is-empty) {
        return {}
    }

    let yaml_content = $rest | take $end_idx | str join "\n"
    try {
        $yaml_content | from yaml
    } catch {
        {}
    }
}
