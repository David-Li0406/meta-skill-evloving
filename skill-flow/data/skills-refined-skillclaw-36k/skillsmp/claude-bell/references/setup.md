# Installation and Setup

Guide for installing and configuring claude-bell.

## Prerequisites

- macOS (10.14 Mojave or later)
- Notification permissions enabled for Terminal/iTerm2

## Installation

### From Release Binary

1. Download the appropriate binary for your architecture:
   - Apple Silicon (M1/M2/M3): `cb-macos-arm64`
   - Intel: `cb-macos-x64`

2. Make executable and move to PATH:
   ```bash
   chmod +x cb-macos-arm64
   sudo mv cb-macos-arm64 /usr/local/bin/cb
   ```

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/aaronbassett/claude-bell.git
   cd claude-bell
   ```

2. Build with Cargo:
   ```bash
   cargo build --release
   ```

3. Install:
   ```bash
   sudo cp target/release/cb /usr/local/bin/
   ```

## First-Time Setup

Run the setup wizard:

```bash
cb setup
```

This will:
1. Create the configuration directory (`~/.claude-bell/`)
2. Create default configuration file
3. Set up template and alias directories
4. Verify notification permissions

## Configuration Directory

Default location: `~/.claude-bell/`

Structure:
```
~/.claude-bell/
├── config.json        # Main configuration
├── templates/         # Custom templates
│   └── templates.json
├── sounds/            # Sound aliases and cached files
│   ├── aliases.json
│   └── files/         # Cached sound files
└── icons/             # Icon aliases
    └── aliases.json
```

## Configuration Options

Edit `~/.claude-bell/config.json` or use `cb config set`:

```json
{
  "version": 1,
  "defaults": {
    "sound": "Glass",
    "icon": null,
    "json": false,
    "log_level": "warn",
    "persistent": false
  },
  "json_targets": ["stdout"],
  "timeout": null,
  "on_dismiss": null,
  "on_timeout": null
}
```

### Setting Defaults

```bash
# Set default sound
cb config set defaults.sound Glass

# Set default timeout
cb config set timeout 5m

# Set default dismiss value
cb config set on_dismiss "cancelled"

# Enable JSON output by default
cb config set defaults.json true
```

## Notification Permissions

macOS requires permission to send notifications. If notifications aren't appearing:

1. Open System Preferences > Notifications
2. Find your terminal app (Terminal, iTerm2, etc.)
3. Enable "Allow Notifications"
4. Set alert style to "Alerts" (not "Banners") for interactive notifications

## Creating Templates

### Via CLI

```bash
cb template create
```

Follow the interactive prompts to define your template.

### Manually

Create or edit `~/.claude-bell/templates/templates.json`:

```json
{
  "templates": [
    {
      "name": "build-done",
      "description": "Build completion notification",
      "title": "Build Complete",
      "subtitle": "{{ project }}",
      "message": "Built in {{ duration | default('unknown') }}",
      "sound": "Glass",
      "defaults": {
        "project": "unnamed"
      }
    }
  ]
}
```

### Template Syntax

Templates use Tera templating:

- `{{ variable }}` - Insert variable
- `{{ variable | default("fallback") }}` - With default value
- `{{ variable | upper }}` - Uppercase filter
- `{{ variable | lower }}` - Lowercase filter
- `{{ variable | title }}` - Title case filter

## Sound Aliases

Add custom sounds for easy reference:

```bash
# Add local sound file (copies to cache)
cb sound add success /path/to/success.aiff --cache

# Add reference to existing sound
cb sound add chime /System/Library/Sounds/Chime.aiff

# Use in notifications
cb -t "Done" --sound @success
```

### Built-in macOS Sounds

Available system sounds:
- Basso
- Blow
- Bottle
- Frog
- Funk
- Glass
- Hero
- Morse
- Ping
- Pop
- Purr
- Sosumi
- Submarine
- Tink

## Icon Aliases

Add custom icons:

```bash
# Add app icon
cb icon add vscode /Applications/Visual\ Studio\ Code.app

# Use in notifications
cb -t "Build Done" --icon @vscode
```

## Verify Installation

Run diagnostics:

```bash
cb doctor
```

This checks:
- Configuration directory exists
- Configuration file is valid
- Sound aliases are valid
- Icon aliases are valid

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAUDE_BELL_CONFIG` | Override config file path |
| `CLAUDE_BELL_LOG` | Override log level |

## Updating

### From Binary

Download new binary and replace existing:

```bash
sudo mv cb-macos-arm64 /usr/local/bin/cb
```

### From Source

```bash
git pull
cargo build --release
sudo cp target/release/cb /usr/local/bin/
```

## Uninstalling

```bash
# Remove binary
sudo rm /usr/local/bin/cb

# Remove configuration (optional)
rm -rf ~/.claude-bell
```
