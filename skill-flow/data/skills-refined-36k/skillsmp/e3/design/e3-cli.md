# e3-cli: Command Line Interface

This document specifies the e3 command-line interface.

All commands take a repository path as the first argument (`.` for current directory).

## Repository

```bash
e3 init <repo>                              # Create new repository
e3 status <repo>                            # Show installed packages, workspaces
e3 gc <repo>                                # Remove unreferenced objects
```

## Packages

```bash
e3 package add <repo> <name>[@<ver>]        # Fetch from registry + import
e3 package import <repo> <path.zip>         # Import from local .zip
e3 package export <repo> <pkg>[@<ver>] <path.zip>  # Export to .zip
e3 package remove <repo> <pkg>[@<ver>]      # Remove package
e3 package list <repo>                      # List installed packages
```

## Workspaces

```bash
e3 workspace create <repo> <name>           # Create empty workspace
e3 workspace deploy <repo> <ws> <pkg>[@<ver>]  # Deploy package to workspace
e3 workspace export <repo> <ws> <path.zip>  # Export workspace as package
    [--name <pkg>] [--version <ver>]        # Default: <pkg>@<ver>-<hash>
e3 workspace list <repo>                    # List workspaces
e3 workspace remove <repo> <ws>             # Remove workspace
```

## Datasets

```bash
e3 dataset get <repo> <ws> <path>           # Print dataset value
e3 dataset set <repo> <ws> <path> <file>    # Set dataset from file
e3 dataset list <repo> <ws>                 # List datasets in workspace
```

## Execution

```bash
e3 run <repo> <task> <inputs...> -o <out>   # Ad-hoc task execution
e3 start <repo> <ws> [--filter <pattern>]   # Run dataflows in workspace
e3 start <repo> <ws> --watch                # Watch mode - re-run on changes
```

## Inspection

```bash
e3 logs <repo> [<task_hash>] [--follow]     # View execution logs
e3 view <repo> <path>                       # TUI data viewer
e3 convert <path> [--format east|json]      # Convert between formats
```

## Registry

```bash
e3 registry add <repo> <url>                # Add registry
e3 registry remove <repo> <url>             # Remove registry
e3 registry list <repo>                     # List registries
e3 publish <repo> <pkg>[@<ver>]             # Publish to registry
e3 search <repo> <query>                    # Search registries
```

## Examples

```bash
# Setup
$ e3 init .
$ e3 package add . east-python
$ e3 package import . ~/dev/my-pkg/dist/my-pkg-1.0.0.zip

# Create workspace and run
$ e3 workspace create . production
$ e3 workspace deploy . production my-pkg@1.0.0
$ e3 start . production
$ e3 dataset get . production outputs/predict

# Update data and rerun
$ e3 dataset set . production inputs/sales ./new_sales.beast2
$ e3 start . production

# Export workspace state for colleague
$ e3 workspace export . production ./handoff.zip
# Creates my-pkg-1.0.0-a3f8b2c1.zip (includes package + current data)

# Colleague imports and works with your exact state
$ e3 package import . ./handoff.zip
$ e3 workspace deploy . analysis my-pkg@1.0.0-a3f8b2c1
```
