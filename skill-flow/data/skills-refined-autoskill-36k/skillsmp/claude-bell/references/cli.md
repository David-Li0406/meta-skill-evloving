# CLI Reference

Complete command-line interface documentation for claude-bell (`cb`).

## Synopsis

```bash
cb [OPTIONS] [COMMAND]
```

## Global Options

### Content Options

| Flag | Short | Description |
|------|-------|-------------|
| `--title <TEXT>` | `-t` | Notification title |
| `--subtitle <TEXT>` | `-s` | Notification subtitle |
| `--message <TEXT>` | `-m` | Notification message body |
| `--image <PATH>` | `-i` | Thumbnail image path or URL |
| `--icon <PATH>` | | App icon (path or @alias) |
| `--sound <NAME>` | | Sound (system name, path, or @alias) |

### Interaction Options

| Flag | Short | Description |
|------|-------|-------------|
| `--actions <A,B,C>` | `-a` | Comma-separated action buttons |
| `--reply <PLACEHOLDER>` | `-r` | Enable reply input with placeholder text |
| `--url <URL>` | | URL to open when notification clicked |

### Behavior Options

| Flag | Description |
|------|-------------|
| `--persistent` | Keep notification on screen until dismissed |
| `--not-persistent` | Override implicit persistence |
| `--timeout <DURATION>` | Timeout duration (e.g., 30s, 5m, 1h) |
| `--default <VALUE>` | Default value on dismiss/timeout |
| `--on-dismiss <VALUE>` | Value to return on dismiss |
| `--on-timeout <VALUE>` | Value to return on timeout |

### Input Options

| Flag | Description |
|------|-------------|
| `--batch` | Process newline-delimited JSON from stdin |

### Output Options

| Flag | Description |
|------|-------------|
| `--json <TARGETS>` | JSON output targets (stdout, stderr, logs, response) |
| `--pretty` | Pretty-print JSON output |
| `--quiet` | Suppress stdout |
| `--silent` | Suppress all output |
| `--log-level <LEVEL>` | Log level: error, warn, info, debug, trace (default: warn) |

### Template Options

| Flag | Description |
|------|-------------|
| `--template <NAME>` | Use named template |
| `--var <KEY:VALUE>` | Template variables (repeatable, comma-separated) |

## Subcommands

### `cb setup`

Run first-time setup wizard. Creates configuration directory and walks through initial settings.

```bash
cb setup
```

### `cb doctor`

Check system health and configuration. Reports status of:
- Configuration directory and file
- Sound aliases
- Icon aliases

```bash
cb doctor
```

### `cb template <ACTION>`

Manage notification templates.

| Action | Description |
|--------|-------------|
| `list` | List all templates |
| `show <name>` | Show a template definition |
| `create` | Create a new template interactively |
| `update <name>` | Update an existing template |
| `delete <name>` | Delete a template |
| `validate [name] [--all]` | Validate template(s) |

Examples:
```bash
cb template list
cb template show build-done
cb template create
cb template validate --all
```

### `cb sound <ACTION>`

Manage sound aliases.

| Action | Description |
|--------|-------------|
| `list` | List sound aliases |
| `add <alias> <path> [--cache]` | Add a sound alias (--cache copies to local storage) |
| `remove <alias> [--with-file]` | Remove alias (--with-file also deletes cached file) |
| `prune [target]` | Prune orphaned items: files, aliases, or both |
| `doctor` | Check sound alias health |

Examples:
```bash
cb sound list
cb sound add success /path/to/sound.aiff --cache
cb sound remove success --with-file
cb sound prune both
```

### `cb icon <ACTION>`

Manage icon aliases.

| Action | Description |
|--------|-------------|
| `list` | List icon aliases |
| `add <alias> <path>` | Add an icon alias |
| `remove <alias> [--with-bundle]` | Remove alias (--with-bundle also deletes bundle) |
| `prune [target]` | Prune orphaned items: bundles, aliases, or both |
| `doctor` | Check icon alias health |

Examples:
```bash
cb icon list
cb icon add myapp /Applications/MyApp.app
cb icon remove myapp
```

### `cb config <ACTION>`

Manage configuration.

| Action | Description |
|--------|-------------|
| `show [--pretty]` | Show current configuration |
| `set <key> <value>` | Set a configuration value |
| `unset <key>` | Unset a configuration value |
| `reset` | Reset configuration to defaults |
| `validate [--path <path>]` | Validate configuration file |

Examples:
```bash
cb config show --pretty
cb config set defaults.sound Glass
cb config unset timeout
cb config validate
```

## Configuration Keys

Available configuration keys for `cb config set`:

| Key | Type | Description |
|-----|------|-------------|
| `defaults.sound` | string | Default notification sound |
| `defaults.icon` | string | Default app icon |
| `defaults.json` | boolean | Default to JSON output |
| `defaults.log_level` | string | Default log level |
| `defaults.persistent` | boolean | Default persistent mode |
| `json_targets` | array | JSON output targets |
| `timeout` | string | Default timeout duration |
| `on_dismiss` | string | Default dismiss value |
| `on_timeout` | string | Default timeout value |

## Timeout Format

Timeouts use duration syntax:

| Format | Example | Description |
|--------|---------|-------------|
| `Ns` | `30s` | N seconds |
| `Nm` | `5m` | N minutes |
| `Nh` | `1h` | N hours |

## Template Variables

Templates use Tera syntax for interpolation:

```bash
# Single variable
cb --template deploy --var 'env:production'

# Multiple variables
cb --template build-done --var 'project:myapp' --var 'duration:45s'

# Variables with special characters
cb --template release --var 'version:1.2.3' --var 'notes:Bug fixes and improvements'
```

Template syntax in template files:
- `{{ variable }}` - Insert variable value
- `{{ variable | default("fallback") }}` - With default
- `{{ variable | upper }}` - With filter

## Persistence Behavior

Notifications become persistent automatically when:
- `--actions` is specified
- `--reply` is specified

Use `--not-persistent` to override implicit persistence.

## JSON Output

The `--json` flag controls where JSON output is written:

```bash
# Output to stdout
cb -t "Test" --json stdout

# Output to multiple targets
cb -t "Test" --json stdout,logs

# Pretty-printed JSON
cb -t "Test" --json stdout --pretty
```

JSON response structure:
```json
{
  "action": "clicked",
  "value": "Yes",
  "exit_code": 0
}
```

## Batch Mode

Process multiple notifications from stdin:

```bash
echo '{"title":"A"}
{"title":"B"}' | cb --batch
```

Each line must be valid JSON with notification parameters.
