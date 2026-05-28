# e3-cli: Command Line Interface

This document specifies the e3 command-line interface.

All commands take a repository path as the first argument (`.` for current directory).

## Path Syntax

Dataset paths in the CLI use `workspace.path.to.dataset` syntax:

```
production.inputs.sales           # Input dataset in 'production' workspace
production.tasks.train.output     # Output of 'train' task
production.tasks.predict.output   # Output of 'predict' task
```

The first segment is always the workspace name, followed by the path within that workspace.

For identifiers with special characters (spaces, dots), use backticks:
```
production.inputs.`sales data`    # Field name with space
'production.inputs.`my.field`'    # Quote the whole thing in bash
```

Internally, e3 uses keypath syntax (`#.field[index]`) for serialization and glob patterns,
but the CLI uses the simpler dot-separated format for usability.

## Repository

```bash
e3 init <repo>                              # Create new repository
e3 status <repo>                            # Show installed packages, workspaces
e3 gc <repo>                                # Remove unreferenced objects
```

## Packages

```bash
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

Dataset commands use `workspace.path` syntax to identify datasets:

```bash
e3 get <repo> <ws.path>                     # Print dataset value
e3 set <repo> <ws.path> <file>              # Set dataset from file
e3 list <repo> <ws>[.path]                  # List datasets (optionally under path)
```

Examples:
```bash
e3 get . production.inputs.sales
e3 get . production.tasks.train.output
e3 set . production.inputs.sales ./new_sales.beast2
e3 list . production                        # List all datasets
e3 list . production.inputs                 # List input datasets only
```

## Execution

```bash
e3 run <repo> <pkg>/<task> <inputs...> -o <out>  # Ad-hoc task execution
e3 start <repo> <ws> [--filter <pattern>]   # Run tasks in workspace
e3 start <repo> <ws> --watch                # Watch mode - re-run on changes
```

## Inspection

```bash
e3 logs <repo> [<task_hash>] [--follow]     # View execution logs
e3 view <repo> <ws.path>                    # TUI data viewer
e3 convert <path> [--format east|json]      # Convert between formats
```

## Examples

```bash
# Setup
$ e3 init .
$ e3 package import . ~/dev/my-pkg/dist/my-pkg-1.0.0.zip

# Create workspace and run
$ e3 workspace create . production
$ e3 workspace deploy . production my-pkg@1.0.0
$ e3 start . production
$ e3 get . production.tasks.predict.output

# Update data and rerun
$ e3 set . production.inputs.sales ./new_sales.beast2
$ e3 start . production

# Export workspace state for colleague
$ e3 workspace export . production ./handoff.zip # saves my-pkg@1.0.0-a3f8b2c1 to file

# Colleague imports and works with your exact state
$ e3 package import . ./handoff.zip # loads my-pkg@1.0.0-a3f8b2c1 from file
$ e3 workspace deploy . analysis my-pkg@1.0.0-a3f8b2c1
```
