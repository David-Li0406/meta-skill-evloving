---
name: daemon-send-command
description: Instructions for sending commands to the AutomateLinux daemon using the CLI.
---

# Sending Commands to the Daemon

The AutomateLinux daemon is controlled via a Unix Domain Socket (UDS). You can interact with it using the binary directly or via the `d` shorthand.

## Using the `d` Shorthand

The `d` function is the recommended way to interact with the daemon. It is designed to be smart and concise.

### 1. Direct Command Sending
You can skip the `send` keyword for most operations.

```bash
d listPorts
d ping
d publicTransportationOpenApp
```

### 2. Commands with Arguments
Use `--key` and `--value` (or other defined arguments) for commands that require parameters.

```bash
d setPort --key pt --value 3001
d simulateInput --type 1 --code 1003 --value 1
```

### 3. Explicit Modes
If you need to be explicit, or if you are starting the daemon process itself:

```bash
d send ping
```

## Internal Binary Mode

If the `d` function is not available, you must use the `daemon` binary directly from its directory:

```bash
./daemon send <command> [args...]
```

## How it Works
The `d` function (defined in `terminal/functions/daemon.sh`) checks it's first argument. If it isn't `send` or `daemon`, it prepends `send` automatically before calling the `daemon` binary. This allows for a much faster workflow while maintaining compatibility with the binary's strict `argv[1]` requirement.

> [!TIP]
> Use `d help` to see all available commands and their required arguments.
