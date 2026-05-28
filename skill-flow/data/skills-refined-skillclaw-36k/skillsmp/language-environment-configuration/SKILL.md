---
name: Language Environment Configuration
description: This skill should be used when detecting programming languages in projects, determining language versions from config files, installing development environments (Rust, Python, Node.js), setting up LSP servers, installing CLI development tools, or configuring shell environments (oh-my-zsh, starship). Provides knowledge for language detection and environment setup in sandboxes.
version: 0.1.0
---

# Language Environment Configuration

Detect programming languages, parse version requirements, and install complete development environments for Rust, Python, and Node.js in Docker-based sandboxes.

## Purpose

This skill provides knowledge for setting up language-specific development environments inside sandbox containers. Focus on the three primary languages (Rust, Python, Node.js) and their associated tooling, LSP servers, and development utilities.

## Language Detection

### Detection Strategy

Identify languages by scanning for configuration and dependency files:

**Rust indicators:**
- `Cargo.toml` - Rust project manifest
- `Cargo.lock` - Dependency lock file
- `rust-toolchain.toml` - Rust version specification
- `.rs` files in `src/` directory

**Python indicators:**
- `pyproject.toml` - Modern Python project config
- `requirements.txt` - Dependency list
- `setup.py` - Package setup script
- `Pipfile` - Pipenv config
- `.python-version` - Python version file
- `.py` files

**Node.js indicators:**
- `package.json` - npm project manifest
- `package-lock.json` - npm lock file
- `pnpm-lock.yaml` - pnpm lock file
- `.nvmrc` - Node version specification
- `.node-version` - Alternative version file
- `.js`, `.ts`, `.jsx`, `.tsx` files

### Detection Script

Use the `scripts/detect_languages.py` script to analyze a project:

```python
# Returns detected languages and their config files
python3 scripts/detect_languages.py /path/to/project
```

Output format:
```json
{
  "rust": {
    "detected": true,
    "indicators": ["Cargo.toml", "src/main.rs"]
  },
  "python": {
    "detected": true,
    "indicators": ["pyproject.toml", "requirements.txt"]
  },
  "nodejs": {
    "detected": true,
    "indicators": ["package.json", ".nvmrc"]
  }
}
```

## Version Detection

### Version Files and Parsing

Each language has standard files for version specification:

#### Rust Version Detection

**Primary: `rust-toolchain.toml`**
```toml
[toolchain]
channel = "1.93.0"
# or
channel = "stable"
# or
channel = "nightly"
```

Parse with:
```python
import toml
config = toml.load("rust-toolchain.toml")
version = config["toolchain"]["channel"]
```

**Legacy: `rust-toolchain` (plain text)**
```
1.93.0
```

#### Python Version Detection

**Primary: `pyproject.toml`**
```toml
[project]
requires-python = ">=3.14.2"
```

Parse with:
```python
import toml
config = toml.load("pyproject.toml")
version_spec = config["project"]["requires-python"]
# Extract version: ">=3.14.2" → "3.14.2"
```

**Alternative: `.python-version`**
```
3.14.2
```

**requirements.txt (less precise)**
```
python>=3.14
```

#### Node.js Version Detection

**Primary: `.nvmrc`**
```
18.20.0
```

Or semantic versions:
```
lts/*
node
v18
```

**Alternative: `.node-version`**
```
18.20.0
```

**package.json engines field**
```json
{
  "engines": {
    "node": ">=18.0.0"
  }
}
```

### Version Parsing Script

Use `scripts/parse_versions.py`:

```python
# Extract version requirements from project files
python3 scripts/parse_versions.py /path/to/project
```

Output:
```json
{
  "rust": "1.93.0",
  "python": "3.14.2",
  "nodejs": "18.20.0"
}
```

## Language Installation

### Rust Installation

**Install via rustup** (preferred for version flexibility):

```dockerfile
# Install specific version
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | \
    sh -s -- -y --default-toolchain 1.93.0

# Install stable (current)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | \
    sh -s -- -y --default-toolchain stable

# Install nightly
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | \
    sh -s -- -y --default-toolchain nightly
```

**Critical: Version keywords vs numbers**

✅ **GOOD - Always current:**
```dockerfile
RUN rustup install stable
RUN rustup install nightly
RUN rustup default stable
```

❌ **BAD - Becomes outdated:**
```dockerfile
RUN rustup install 1.93.0  # Fixed version, will be old
```

**When to use specific versions:**
- Project requires exact version (from rust-toolchain.toml)
- User explicitly requests specific version

**Components to install:**
```dockerfile
RUN rustup component add clippy rustfmt rust-analyzer
```

**Standard tools:**
```dockerfile
# After Rust is installed
RUN cargo install cargo-dist cargo-deny cargo-release cocogitto
```

### Python Installation

**Install via apt** (system Python):

```dockerfile
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*
```

**Install via uv** (for specific versions):

```dockerfile
# Install uv first
RUN pip3 install --no-cache-dir uv

# Install specific Python version
RUN uv python install 3.14.2

# Install current stable
RUN uv python install

# Python doesn't have official LTS - use current stable
# When user asks for LTS, install current stable instead
```

**Critical: Version keywords**

✅ **GOOD - Always current:**
```dockerfile
RUN uv python install  # Latest stable
RUN pip3 install --upgrade pip  # Latest pip
```

❌ **BAD - Becomes outdated:**
```dockerfile
RUN uv python install 3.14  # Major version, but not latest patch
RUN uv python install 3.14.2  # Specific version, will be old
```

**Standard tools:**
```dockerfile
RUN pip3 install --no-cache-dir uv ruff mypy black pytest
```

### Node.js Installation

**Install via nvm** (preferred for version flexibility):

```dockerfile
ENV NVM_DIR="/root/.nvm"

# Install nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# Install current stable
RUN . "$NVM_DIR/nvm.sh" && nvm install node && nvm alias default node

# Install LTS
RUN . "$NVM_DIR/nvm.sh" && nvm install --lts && nvm alias default lts/*

# Install nightly (latest, including pre-release)
RUN . "$NVM_DIR/nvm.sh" && nvm install node --latest-npm

# Install specific version (when required)
RUN . "$NVM_DIR/nvm.sh" && nvm install 18.20.0
```

**Critical: Version keywords**

✅ **GOOD - Always current:**
```dockerfile
RUN nvm install node  # Current stable
RUN nvm install --lts  # Current LTS
RUN nvm install node --latest-npm  # Nightly/latest
```

❌ **BAD - Becomes outdated:**
```dockerfile
RUN nvm install 18.20.0  # Specific version, will be old
RUN nvm install 18  # Major version, not latest
```

**Standard tools:**
```dockerfile
RUN npm install -g pnpm typescript ts-node
```

## LSP Server Installation

### rust-analyzer

**Install via rustup:**
```dockerfile
RUN rustup component add rust-analyzer
```

**Or via cargo (latest):**
```dockerfile
RUN cargo install rust-analyzer
```

### pyright (Python)

**Install via npm:**
```dockerfile
RUN npm install -g pyright
```

**Or via pip:**
```dockerfile
RUN pip3 install pyright
```

### typescript-language-server

**Install via npm:**
```dockerfile
RUN npm install -g typescript-language-server typescript
```

### Claude Code LSP Plugins

When user requests LSP plugins from marketplace:

```markdown
Add these plugins in Sandbox.toml:

[claude.plugins]
plugins = [
  "rust-analyzer-lsp@claude-plugins-official",
  "pyright-lsp@claude-plugins-official",
  "typescript-lsp@claude-plugins-official"
]
```

Note: LSP servers must be installed in container. Plugins just configure Claude Code to use them.

## CLI Tools Installation

### Tools List

**Standard tools to install:**
- ripgrep, fd, eza, jq, just
- repomix, scc, sg (ast-grep)
- bfs, xan, rga, pdfgrep, fq
- shellcheck, zizmor, git-cliff, has

### Installation Methods

**Via apt (if available):**
```dockerfile
RUN apt-get update && apt-get install -y \
    ripgrep \
    fd-find \
    jq \
    pdfgrep \
    shellcheck \
    && rm -rf /var/lib/apt/lists/*

# Create symlinks where needed
RUN ln -s $(which fdfind) /usr/local/bin/fd
```

**Via cargo:**
```dockerfile
RUN cargo install \
    eza \
    just \
    repomix \
    scc \
    bfs \
    xan \
    git-cliff \
    ast-grep \
    ripgrep_all \
    zizmor \
    has
```

**Via download (for binaries like fq):**
```dockerfile
RUN wget https://github.com/wader/fq/releases/latest/download/fq_linux_amd64.tar.gz && \
    tar xzf fq_linux_amd64.tar.gz && \
    mv fq /usr/local/bin/ && \
    rm fq_linux_amd64.tar.gz
```

### Installation Order

1. **System packages first** (apt) - fastest, most reliable
2. **Cargo tools** - compile from source, takes time
3. **Binary downloads** - fast, but version management needed

See `references/tool-installation.md` for complete installation commands and alternatives.

## Shell Configuration

### oh-my-zsh Installation

```dockerfile
# Install zsh first
RUN apt-get update && apt-get install -y zsh && rm -rf /var/lib/apt/lists/*

# Install oh-my-zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Set zsh as default shell
RUN chsh -s $(which zsh)
```

### Recommended Plugins

```bash
# In .zshrc
plugins=(
  git
  docker
  rust
  python
  node
  npm
  command-not-found
  colored-man-pages
  zsh-autosuggestions
  zsh-syntax-highlighting
)
```

**Install additional plugins:**
```dockerfile
RUN git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

### Custom Aliases

Add to `.zshrc`:

```bash
# eza aliases
alias l='eza -ao --sort=old -F=always --icons=auto --color=always --color-scale=size --color-scale-mode=gradient --group-directories-first --git --git-ignore --no-quotes --time-style=relative --no-permissions --no-user'
alias ll='l -l'
alias lk='eza -a -F=never --icons=never --group-directories-first'

# eza tree function
lt() {
  eza -alT --icons=always --color=always --color-scale=all --color-scale-mode=gradient --group-directories-first --git --git-ignore --no-quotes --level=${1:-2}
}
```

### Starship Installation and Configuration

**Install:**
```dockerfile
RUN curl -sS https://starship.rs/install.sh | sh -s -- -y
```

**Enable in .zshrc:**
```bash
eval "$(starship init zsh)"
```

**Configuration (starship.toml):**

Create `/root/.config/starship.toml`:

```toml
add_newline = true

# Container indicator - highly visible
[container]
disabled = false
symbol = "🐳 "
style = "bold red"
format = "[$symbol]($style)"

# Hostname in red to indicate sandbox
[hostname]
ssh_only = false
format = "[$hostname]($style) "
style = "bold red"

# Directory
[directory]
style = "cyan"
truncation_length = 3
fish_style_pwd_dir_length = 1

# Prompt character
[character]
success_symbol = "[❯](bold red)"
error_symbol = "[❯](bold red)"

# Git
[git_branch]
format = "[$symbol$branch]($style) "
style = "bold purple"

[git_status]
style = "bold yellow"

# Language versions (show when relevant)
[rust]
symbol = "🦀 "
format = "[$symbol($version )]($style)"

[python]
symbol = "🐍 "
format = "[$symbol($version )]($style)"

[nodejs]
symbol = "⬢ "
format = "[$symbol($version )]($style)"

# Disable slow modules
[gcloud]
disabled = true

[kubernetes]
disabled = true
```

**Themes:** See `references/starship-themes.md` for alternative configurations.

## Environment Variables

### Language-Specific Environment Setup

**Rust:**
```dockerfile
ENV PATH="/root/.cargo/bin:${PATH}"
ENV RUSTUP_HOME="/root/.rustup"
ENV CARGO_HOME="/root/.cargo"
```

**Python:**
```dockerfile
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
```

**Node.js:**
```dockerfile
ENV NVM_DIR="/root/.nvm"
ENV NODE_PATH="$NVM_DIR/versions/node/$(cat $NVM_DIR/alias/default)/lib/node_modules"
ENV PATH="$NVM_DIR/versions/node/$(cat $NVM_DIR/alias/default)/bin:$PATH"
```

### Shell RC Files

Ensure language tools available in shell:

```bash
# .zshrc additions
export PATH="/root/.cargo/bin:$PATH"

export NVM_DIR="/root/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

eval "$(starship init zsh)"
```

## Version Conflict Resolution

### User Override vs Detected Version

**Scenario:** Project has Python 3.12 in `pyproject.toml`, user says "use current stable" (3.14.2)

**Resolution:**
1. **User preference takes precedence** - install what user requested
2. **Warn about mismatch:**

```
⚠️  Warning: Project specifies Python 3.12 in pyproject.toml, but you requested current stable (3.14.2).
Installing Python 3.14.2 as requested.

Note: You may need to update pyproject.toml to match:
  requires-python = ">=3.14.2"
```

3. **Install user's version**
4. **Add note to SANDBOX.md** about the version mismatch

### Missing Version Specification

**Scenario:** Language detected but no version file

**Resolution:**
1. **Prompt user** with suggested version:

```
Detected Node.js project, but no .nvmrc or .node-version file found.

What version should I install?
- current (latest stable - recommended)
- lts (long-term support)
- nightly (bleeding edge)
- specific version (e.g., 18.20.0)
```

2. **Default to current stable** if user says "whatever works"

## Additional Resources

### Reference Files

Detailed installation instructions and troubleshooting:
- **`references/tool-installation.md`** - Complete installation commands for all tools
- **`references/version-management.md`** - Advanced version detection and management
- **`references/starship-themes.md`** - Starship configuration examples

### Scripts

Utility scripts for automation:
- **`scripts/detect_languages.py`** - Language detection
- **`scripts/parse_versions.py`** - Version extraction from config files
- **`scripts/install_tools.sh`** - Batch tool installation

### Examples

Working configuration examples:
- **`examples/.zshrc`** - Complete zsh configuration
- **`examples/starship.toml`** - Starship config with container theme

## Integration with Other Skills

**With docker-sandbox-setup:**
- This skill provides the Dockerfile commands for language installation
- docker-sandbox-setup provides the container structure

**With sandbox-config-management:**
- Read language versions from Sandbox.toml
- Update Sandbox.toml with detected or installed versions

## Quick Reference

**Detect languages:** `python3 scripts/detect_languages.py /project`

**Parse versions:** `python3 scripts/parse_versions.py /project`

**Version keywords (ALWAYS use for "current/latest"):**
- Rust: `stable` (not version numbers)
- Python: `uv python install` (not 3.x)
- Node.js: `nvm install node` (not version numbers)

**Version keywords (LTS):**
- Rust: `stable` (no official LTS)
- Python: current stable (no official LTS)
- Node.js: `nvm install --lts`

**Version keywords (nightly/bleeding edge):**
- Rust: `nightly`
- Python: `uv python install nightly`
- Node.js: `nvm install node --latest-npm`

**LSP servers:**
- rust-analyzer: `rustup component add rust-analyzer`
- pyright: `npm install -g pyright`
- typescript-language-server: `npm install -g typescript-language-server`

**Shell setup:**
- oh-my-zsh: Auto-installed via script
- starship: `curl -sS https://starship.rs/install.sh | sh`
- Aliases: Add to `.zshrc`
