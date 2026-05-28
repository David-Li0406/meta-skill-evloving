---
name: Sandbox Config Management
description: This skill should be used when reading or writing Sandbox.toml configuration files, cloning sandbox configurations from existing projects, merging user preferences with detected settings, validating sandbox configuration compatibility, or managing sandbox metadata and settings. Provides knowledge for Sandbox.toml structure and configuration management.
version: 0.1.0
---

# Sandbox Config Management

Read, write, and manage Sandbox.toml configuration files that define sandbox setup and preferences.

## Purpose

This skill provides knowledge for working with `Sandbox.toml` files - the configuration format used to define and share sandbox setups. Handle reading existing configurations, creating new ones, cloning and customizing configurations, and validating compatibility.

## Sandbox.toml Structure

### Complete Example

```toml
[sandbox]
name = "myproject"
location = "/Users/aaronbassett/Sandboxes/aaronbassett/myproject"
created = "2026-01-24T01:30:00Z"
base_image = "ubuntu:24.04"

[source]
type = "github"  # or "local" or "new"
repository = "aaronbassett/myproject"
branch = "main"  # optional

[languages]
rust = "1.93.0"  # or "stable", "nightly"
python = "3.14.2"  # or "current"
nodejs = "current"  # or "lts", "nightly", "18.20.0"

[languages.tools]
rust = ["clippy", "rustfmt", "cargo-dist", "cargo-deny", "cargo-release", "cocogitto"]
python = ["uv", "ruff", "mypy", "black", "pytest"]
nodejs = ["pnpm", "typescript", "ts-node"]

[claude]
marketplaces = [
    "anthropics/claude-plugins-official",
    "aaronbassett/aaronbassett-marketplace"
]

[claude.plugins]
plugins = [
    "rust-analyzer-lsp@claude-plugins-official",
    "pyright-lsp@claude-plugins-official",
    "typescript-lsp@claude-plugins-official",
    "devs@aaronbassett-marketplace",
    "git-lovely@aaronbassett-marketplace",
    "settings-presets@aaronbassett-marketplace"
]

[network]
ports = [3000, 3001, 3002]  # specific ports
# or
port_range = "3000-3999"  # range

[environment]
# Non-secret environment variables
NODE_ENV = "development"
RUST_BACKTRACE = "1"

[shell]
aliases = true  # use standard eza/git aliases
starship_theme = "red_container"
oh_my_zsh_plugins = ["git", "docker", "rust", "python", "node"]

[tools]
# Additional CLI tools beyond defaults
extra = ["bat", "delta", "hyperfine"]
```

### Field Descriptions

**[sandbox] section:**
- `name`: Project name (required)
- `location`: Absolute path to sandbox directory (required)
- `created`: ISO 8601 timestamp of creation
- `base_image`: Docker base image (default: "ubuntu:24.04")

**[source] section:**
- `type`: "github", "local", or "new" (required)
- `repository`: GitHub repo (owner/name) if type="github"
- `branch`: Git branch (default: "main")

**[languages] section:**
- `rust`, `python`, `nodejs`: Version strings or keywords
- Keywords: "stable"/"current", "lts", "nightly"
- Specific versions: "1.93.0", "3.14.2", "18.20.0"

**[languages.tools] section:**
- Arrays of tool names to install for each language
- Empty array = no additional tools

**[claude] section:**
- `marketplaces`: List of marketplace repos
- `plugins`: List of plugins in "name@marketplace" format

**[network] section:**
- `ports`: Array of specific ports to forward
- `port_range`: String range like "3000-3999"
- Use one or the other, not both

**[environment] section:**
- Key-value pairs for environment variables
- Do not include secrets (use .env file instead)

**[shell] section:**
- `aliases`: Boolean to include standard aliases
- `starship_theme`: Theme identifier
- `oh_my_zsh_plugins`: List of plugin names

**[tools] section:**
- `extra`: Additional tools beyond standard set

## Reading Configurations

### Parse Sandbox.toml

Use `scripts/parse_config.py`:

```bash
python3 scripts/parse_config.py /path/to/sandbox/Sandbox.toml
```

Output: JSON representation of configuration

```python
# In Python code
import tomli

with open("Sandbox.toml", "rb") as f:
    config = tomli.load(f)

# Access fields
project_name = config["sandbox"]["name"]
languages = config.get("languages", {})
rust_version = languages.get("rust")
```

### Validate Configuration

Check for required fields and valid values:

```python
def validate_config(config: dict) -> List[str]:
    """
    Validate Sandbox.toml structure.

    Returns list of validation errors (empty if valid).
    """
    errors = []

    # Required sections
    if "sandbox" not in config:
        errors.append("Missing [sandbox] section")
    else:
        sandbox = config["sandbox"]
        if "name" not in sandbox:
            errors.append("Missing sandbox.name")
        if "location" not in sandbox:
            errors.append("Missing sandbox.location")

    if "source" not in config:
        errors.append("Missing [source] section")
    else:
        source = config["source"]
        if "type" not in source:
            errors.append("Missing source.type")
        elif source["type"] not in ["github", "local", "new"]:
            errors.append(f"Invalid source.type: {source['type']}")

        if source.get("type") == "github" and "repository" not in source:
            errors.append("GitHub source requires repository field")

    # Warn about unknown fields (lenient)
    # Just log warnings, don't error

    return errors
```

Use `scripts/validate_config.py` for validation.

### Read from Existing Sandbox

When user references an existing sandbox:

```
User: "Base this on ~/Sandboxes/aaronbassett/project1"
```

Process:
1. Check if directory exists
2. Look for `Sandbox.toml` in directory root
3. Parse configuration
4. Present configuration to user for customization

```python
existing_config_path = Path("~/Sandboxes/aaronbassett/project1/Sandbox.toml").expanduser()

if not existing_config_path.exists():
    print("No Sandbox.toml found in that directory")
    # Offer to create from scratch
else:
    with open(existing_config_path, "rb") as f:
        existing_config = tomli.load(f)

    # Show user what's in existing config
    print(f"Found sandbox config for: {existing_config['sandbox']['name']}")
    print(f"Languages: {', '.join(existing_config.get('languages', {}).keys())}")
    # etc.
```

## Writing Configurations

### Create New Sandbox.toml

Build configuration from user answers and detected settings:

```python
from datetime import datetime, timezone

config = {
    "sandbox": {
        "name": project_name,
        "location": str(sandbox_location),
        "created": datetime.now(timezone.utc).isoformat(),
        "base_image": base_image or "ubuntu:24.04",
    },
    "source": {
        "type": source_type,  # "github", "local", or "new"
    },
}

# Add repository if GitHub source
if source_type == "github":
    config["source"]["repository"] = repo_name
    config["source"]["branch"] = branch or "main"

# Add detected/specified languages
if languages:
    config["languages"] = languages
    config["languages"]["tools"] = tools_by_language

# Add Claude configuration
if marketplaces or plugins:
    config["claude"] = {}
    if marketplaces:
        config["claude"]["marketplaces"] = marketplaces
    if plugins:
        config["claude"]["plugins"] = plugins

# Add network config
if ports:
    config["network"] = {"ports": ports}
elif port_range:
    config["network"] = {"port_range": port_range}

# Add environment variables (non-secrets only)
if env_vars:
    config["environment"] = env_vars

# Shell configuration
config["shell"] = {
    "aliases": True,
    "starship_theme": "red_container",
    "oh_my_zsh_plugins": ["git", "docker", "rust", "python", "node"],
}
```

### Write to File

```python
import tomli_w  # or toml for writing

output_path = Path(sandbox_location) / "Sandbox.toml"

with open(output_path, "wb") as f:
    tomli_w.dump(config, f)

print(f"Configuration saved to {output_path}")
```

Use `scripts/write_config.py` helper script.

## Cloning Configurations

### Clone and Customize Workflow

When user wants to clone an existing sandbox for a new project:

```
User: "Create a duplicate of ~/Sandboxes/aaronbassett/project1 for myproject2"
```

Workflow:
1. **Read existing config**
2. **Detect new project languages** (if repository provided)
3. **Compare and identify differences**
4. **Ask user about discrepancies**
5. **Merge preferences**
6. **Write new config**

Example:

```python
# Read existing
existing = read_config("~/Sandboxes/aaronbassett/project1/Sandbox.toml")

# Detect new project (if applicable)
if new_project_repo:
    detected_languages = detect_languages(new_project_repo)

# Compare
existing_langs = set(existing.get("languages", {}).keys())
detected_langs = set(detected_languages.keys())

if existing_langs != detected_langs:
    # Ask user
    print(f"Original sandbox configured for: {', '.join(existing_langs)}")
    print(f"New project uses: {', '.join(detected_langs)}")
    print("Should I configure for new project languages, or keep original?")

    # Wait for user response
    # Then merge accordingly

# Clone base config
new_config = existing.copy()

# Update with new values
new_config["sandbox"]["name"] = "myproject2"
new_config["sandbox"]["location"] = new_location
new_config["sandbox"]["created"] = datetime.now(timezone.utc).isoformat()

# Update languages if changed
if user_wants_new_languages:
    new_config["languages"] = detected_languages_with_versions

# Keep other settings (tools, plugins, etc.)
# unless user specifies changes
```

### Partial Cloning

User may want only specific parts:

```
User: "Use the same Claude plugins as project1, but different languages"
```

```python
new_config = {
    "sandbox": {...},  # New sandbox details
    "source": {...},   # New source
    "languages": {...},  # New languages
    "claude": existing_config["claude"],  # Cloned from existing
    "network": existing_config.get("network", default_network),  # Cloned
    "shell": existing_config.get("shell", default_shell),  # Cloned
}
```

## User Preference Merging

### Override Priority

When conflicts occur, resolution order:

1. **Explicit user request** (highest priority)
2. **Detected from project files**
3. **Cloned from existing sandbox**
4. **User's default preferences** (from `.claude/sandbox.local.md`)
5. **Plugin defaults** (lowest priority)

Example:

```
Detected: Python 3.12 (from pyproject.toml)
User says: "use current stable" (3.14.2)

Resolution: Use 3.14.2 (user request overrides detection)
Action: Warn user about mismatch, suggest updating pyproject.toml
```

### Merge Algorithm

```python
def merge_preferences(
    detected: dict,
    user_requested: dict,
    cloned: dict,
    user_defaults: dict,
    plugin_defaults: dict,
) -> dict:
    """Merge preferences with priority."""
    result = plugin_defaults.copy()

    # Layer in each level (lowest to highest priority)
    for source in [user_defaults, cloned, detected, user_requested]:
        for key, value in source.items():
            if value is not None:  # Only override if value provided
                result[key] = value

    return result
```

## Validation

### Compatibility Checks

Validate configuration before using:

**Language version compatibility:**
```python
def check_language_compatibility(config: dict) -> List[str]:
    warnings = []

    # Check if versions are too old
    rust_version = config.get("languages", {}).get("rust")
    if rust_version and rust_version < "1.70":
        warnings.append(f"Rust {rust_version} is quite old, consider updating")

    # Check for known incompatibilities
    # e.g., certain tool combinations

    return warnings
```

**Port conflicts:**
```python
def check_port_availability(ports: List[int]) -> List[int]:
    """Return list of ports that are already in use."""
    import socket

    in_use = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) == 0:
                in_use.append(port)
    return in_use
```

### Lenient Validation

Be lenient with unknown fields (warn, don't error):

```python
KNOWN_SECTIONS = {"sandbox", "source", "languages", "claude", "network", "environment", "shell", "tools"}

def check_unknown_fields(config: dict):
    unknown = set(config.keys()) - KNOWN_SECTIONS
    if unknown:
        print(f"Warning: Unknown sections in config: {', '.join(unknown)}")
        print("These will be ignored but won't cause errors")
```

## SANDBOX.md Generation

### Create Documentation File

Alongside `Sandbox.toml`, create `SANDBOX.md` describing the setup:

```markdown
# Sandbox: {project_name}

Created: {created_timestamp}
Location: {sandbox_location}

## Configuration

**Languages:**
- Rust: {rust_version}
- Python: {python_version}
- Node.js: {nodejs_version}

**Source:**
- Type: {source_type}
- Repository: {repository} (if applicable)

**Claude Code:**
- Marketplaces: {marketplaces}
- Plugins: {plugins}

## Setup

This sandbox was automatically configured based on:
{what influenced the config - detection, cloning, user preferences}

{Any version mismatches or warnings}

## Usage

### Starting the Sandbox

```bash
./sandbox/up.sh
```

The sandbox will build and start. First run may take 10-15 minutes.

### Interactive Shell

```bash
./sandbox/shell.sh
```

### Running Commands

```bash
./sandbox/run.sh <command>

# Examples:
./sandbox/run.sh cargo test
./sandbox/run.sh npm run dev
./sandbox/run.sh python -m pytest
```

### Stopping

```bash
./sandbox/stop.sh
```

## First Run

On first run in the container:

1. Authenticate Claude Code:
   ```bash
   ./sandbox/shell.sh
   cc auth
   # Follow authentication flow
   ```

2. Verify plugins loaded:
   ```bash
   cc plugin list
   ```

3. Exit shell:
   ```bash
   exit
   ```

Authentication persists across container restarts.

## Network

Ports forwarded: {ports or port_range}

Access applications:
- http://localhost:{port}

## Notes

{Any special notes, warnings, or instructions}
```

Generate this file automatically when creating sandbox.

## Integration with Other Skills

**With docker-sandbox-setup:**
- This skill defines WHAT to configure
- docker-sandbox-setup implements HOW (Dockerfile, scripts)

**With language-environment-config:**
- This skill stores language preferences
- language-environment-config implements installation

## Scripts

### Available Utilities

- **`scripts/parse_config.py`** - Parse Sandbox.toml to JSON
- **`scripts/validate_config.py`** - Validate configuration
- **`scripts/write_config.py`** - Create Sandbox.toml from dict
- **`scripts/merge_configs.py`** - Merge multiple configs with priority

### Example Usage

```bash
# Parse existing config
python3 scripts/parse_config.py ~/sandbox/Sandbox.toml

# Validate
python3 scripts/validate_config.py ~/sandbox/Sandbox.toml

# Create new config
python3 scripts/write_config.py \
  --name myproject \
  --location ~/Sandboxes/myproject \
  --rust stable \
  --python current \
  --output ~/Sandboxes/myproject/Sandbox.toml
```

## Examples

See `examples/` directory for:
- **`Sandbox.toml.rust`** - Rust-only project
- **`Sandbox.toml.python`** - Python project
- **`Sandbox.toml.fullstack`** - Multi-language monorepo

## Quick Reference

**Read config:**
```python
import tomli
with open("Sandbox.toml", "rb") as f:
    config = tomli.load(f)
```

**Write config:**
```python
import tomli_w
with open("Sandbox.toml", "wb") as f:
    tomli_w.dump(config, f)
```

**Priority order (highest first):**
1. User explicit request
2. Project detection
3. Cloned config
4. User defaults
5. Plugin defaults

**Validation:** Lenient - warn on unknown fields, error only on critical issues
