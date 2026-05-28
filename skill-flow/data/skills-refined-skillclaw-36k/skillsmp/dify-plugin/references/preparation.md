# Environment Setup

## Quick Setup (Recommended)

Run the setup script to install all dependencies:

```bash
# From skill directory
./scripts/setup_env.sh
```

This will:
1. Check Python version (3.12+ required)
2. Install `dify` CLI
3. Install `uv` (Python package manager)

## Manual Setup

If the script fails, follow these steps manually.

### 1. Install Dify CLI

**macOS (Homebrew):**
```bash
brew tap langgenius/dify
brew install dify
```

**macOS/Linux (Manual Download):**
```bash
# Download from: https://github.com/langgenius/dify-plugin-daemon/releases

# macOS ARM (M series)
curl -fsSL https://github.com/langgenius/dify-plugin-daemon/releases/latest/download/dify-plugin-darwin-arm64 -o dify
chmod +x dify
sudo mv dify /usr/local/bin/

# macOS Intel
curl -fsSL https://github.com/langgenius/dify-plugin-daemon/releases/latest/download/dify-plugin-darwin-amd64 -o dify
chmod +x dify
sudo mv dify /usr/local/bin/

# Linux AMD64
curl -fsSL https://github.com/langgenius/dify-plugin-daemon/releases/latest/download/dify-plugin-linux-amd64 -o dify
chmod +x dify
sudo mv dify /usr/local/bin/
```

Verify: `dify version`

### 2. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Add to PATH if needed: `export PATH="$HOME/.local/bin:$PATH"`

Verify: `uv --version`

### 3. Check Python

```bash
python3 --version  # Should be 3.12+
```

## Create Plugin Project

```bash
# Interactive mode
dify plugin init

# Setup Python environment
cd my-plugin
uv init --no-readme
uv add dify_plugin
```

## Verify Installation

```bash
dify version          # CLI version
uv --version          # Package manager
python3 --version     # Python 3.12+
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `dify: command not found` | Add `/usr/local/bin` to PATH or reinstall |
| `uv: command not found` | Add `~/.local/bin` to PATH |
| Python < 3.12 | Install Python 3.12+ via pyenv or system package |
| Permission denied | Use `sudo` for `/usr/local/bin` install |

## Reference Repositories (Optional)

When the reference documentation is insufficient, sync these repositories for studying real implementations:

```bash
# From skill directory
./scripts/sync_repos.sh
```

This script clones/pulls to `~/playground/dify-repo/`:

| Repository | Purpose |
|------------|---------|
| **dify** | Dify core - docker compose host for integration testing |
| **dify-plugin-daemon** | Plugin runtime & CLI - **check interface definitions here** |
| **dify-official-plugins** | Official plugin examples - study real implementations |

The script also:
- Parses `docker-compose.yaml` to detect service versions
- Switches each repo to the corresponding git tag for version consistency

**Script options:**
```bash
./scripts/sync_repos.sh --pull-only       # Only pull, don't switch tags
./scripts/sync_repos.sh --show-versions   # Show docker-compose image versions
./scripts/sync_repos.sh --base /path/to   # Custom base directory
```

**Key reference paths in dify-plugin-daemon:**
- `internal/core/plugin_daemon/` - Plugin daemon core logic
- `internal/types/` - Type definitions and interfaces
- `pkg/entities/` - Entity structures
