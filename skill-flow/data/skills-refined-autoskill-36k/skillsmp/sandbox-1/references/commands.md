# Command Reference

## Table of Contents
- [Lifecycle Commands](#lifecycle-commands)
- [Execution Commands](#execution-commands)
- [File Transfer](#file-transfer)
- [Endpoint Management](#endpoint-management)
- [Snapshot Management](#snapshot-management)
- [Command Management](#command-management)

## Lifecycle Commands

```bash
bdy sandbox create -i <identifier>             # Create sandbox
bdy sandbox list                               # List sandboxes (alias: ls)
bdy sandbox get <identifier>                   # Get details
bdy sandbox status <identifier>                # Get status
bdy sandbox start <identifier>                 # Start stopped sandbox
bdy sandbox start <identifier> --wait          # Start and wait
bdy sandbox stop <identifier>                  # Stop running sandbox
bdy sandbox stop <identifier> --wait           # Stop and wait
bdy sandbox restart <identifier>               # Restart sandbox
bdy sandbox restart <identifier> --wait        # Restart and wait
bdy sandbox destroy <identifier>               # Delete sandbox (alias: rm)
```

### Create Options

| Option | Description |
|--------|-------------|
| `-i, --identifier <id>` | Unique identifier |
| `-n, --name <name>` | Display name |
| `--os <image>` | OS image (default: ubuntu:24.04) |
| `--resources <spec>` | Resources: 1x2, 2x4, 4x8, 8x16, 12x24 (CPUxRAM) |
| `--install-command <cmd>` | Setup commands (repeatable) |
| `--run-command <cmd>` | Command to run on startup |
| `--snapshot <snapshot-name>` | Create from snapshot name (instead of OS) |
| `--app-dir <directory>` | Application directory |
| `--app-type <type>` | Application type (CMD, SERVICE) |
| `--tag <tags...>` | Tags (repeatable) |
| `--wait-for-running` | Wait until sandbox is running |
| `--wait-for-configured` | Wait until setup commands complete |
| `--wait-for-app` | Wait until app commands complete |

## Execution Commands

```bash
bdy sandbox exec command <identifier> "<command>"                  # Execute (background)
bdy sandbox exec command <identifier> "<command>" --wait           # Execute and wait
bdy sandbox exec command <identifier> "<code>" --runtime PYTHON    # Different runtime
bdy sandbox exec list <identifier>                                 # List commands (alias: ls)
bdy sandbox exec status <identifier> <command-id>                  # Get command status
bdy sandbox exec logs <identifier> <command-id>                    # View logs
bdy sandbox exec logs <identifier> <command-id> --wait             # Wait for completion and get logs
bdy sandbox exec kill <identifier> <command-id>                    # Kill command
```

### Exec Options

| Option | Description |
|--------|-------------|
| `--runtime <type>` | BASH (default), JAVASCRIPT, TYPESCRIPT, PYTHON |
| `--wait` | Block until command completes (default: background) |

## File Transfer

```bash
bdy sandbox cp <source> <identifier>:<dest>         # Copy to sandbox
bdy sandbox cp ./src my-app:/app/src                # Copy directory
bdy sandbox cp --silent ./file my-app:/app/file     # Silent mode (recommended)
```

**Important:** Always use `--silent` to suppress progress output.

## Endpoint Management

```bash
bdy sandbox endpoint list <identifier>                             # List (alias: ep list)
bdy sandbox endpoint get <identifier> <endpoint-name>              # Get details
bdy sandbox endpoint add <identifier> -n <name> -e <port>          # Add
bdy sandbox endpoint delete <identifier> <endpoint-name>           # Delete
```

### Endpoint Options

| Option | Description |
|--------|-------------|
| `-n, --name <name>` | Endpoint name |
| `-e, --endpoint <port>` | [ip:]port |
| `-t, --type <type>` | HTTP, TLS, or TCP (default: HTTP) |
| `-a, --auth <user:pass>` | HTTP basic authorization |
| `-b, --buddy` | Buddy authorization |
| `--whitelist <cidrs...>` | Whitelist IP CIDRs (use "*" for all) |
| `-s, --serve <directory>` | Serve files from directory |
| `-l, --log` | Log HTTP requests |
| `-c, --compression` | Enable HTTP response compression |
| `--timeout <seconds>` | Connection timeout |

## Snapshot Management

```bash
bdy sandbox snapshot list <identifier>                        # List (alias: snap list)
bdy sandbox snapshot get <identifier> <snapshot-name>         # Get details
bdy sandbox snapshot create <identifier> -n <name>            # Create
bdy sandbox snapshot create <identifier> -n <name> --wait     # Create and wait
bdy sandbox snapshot delete <identifier> <snapshot-name>      # Delete
```

## Command Management

Commands are managed via `bdy sandbox exec` subcommands (see [Execution Commands](#execution-commands)):

```bash
bdy sandbox exec list <identifier>                  # List all commands
bdy sandbox exec logs <identifier> <cmd-id>         # View logs
bdy sandbox exec logs <identifier> <cmd-id> --wait  # Wait and get logs
bdy sandbox exec kill <identifier> <cmd-id>         # Kill command
```

**Tip:** Use `exec list` to discover command IDs, then `exec logs` to check output.
