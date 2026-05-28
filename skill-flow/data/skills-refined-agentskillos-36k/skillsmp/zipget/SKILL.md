---
name: zipget
description: Download and install tools from GitHub releases, URLs, or S3. Use when user needs to download binaries, install CLI tools, create tool recipes, or set up Java JAR applications.
---

# Zipget - Tool Downloader & Installer

Downloads and installs executables from GitHub releases, URLs, and S3 with caching. See https://github.com/vivainio/zipget-rs

## Commands

```bash
# Install from GitHub (auto-detects platform)
zipget install sharkdp/bat                    # Install with shim (Windows)
zipget install sharkdp/bat --no-shim          # Install directly (cross-platform)
zipget install google/go-jsonnet --exe jsonnet

# Download from GitHub
zipget github sharkdp/bat --unzip-to ./tools
zipget github BurntSushi/ripgrep --tag 14.1.0 --save-as ./rg.tar.gz

# Download and run without installing
zipget run BurntSushi/ripgrep -- --version
zipget run sharkdp/bat --exe bat -- README.md

# Process recipe file
zipget recipe tools.toml
zipget recipe tools.toml ripgrep bat          # Only specific items
zipget recipe tools.toml --upgrade            # Update to latest versions
zipget recipe tools.toml --lock               # Generate SHA-256 hashes

# Create launcher for JAR or executable
zipget shim ./plantuml.jar                    # Creates ~/.local/bin/plantuml
zipget shim ./app.jar --name myapp            # Custom launcher name
zipget shim ./app.jar --java-opts="-Xmx1g"    # With JVM options

# Fetch direct URL
zipget fetch https://example.com/tool.zip --unzip-to ./tools

# Self-update
zipget update
```

## Recipe Format

TOML file with download items:

```toml
[vars]
tools_dir = "./tools"

[ripgrep]
github = { repo = "BurntSushi/ripgrep" }
unzip_to = "${tools_dir}"
files = "*/rg"
install_exes = ["rg"]

[bat]
github = { repo = "sharkdp/bat", tag = "v0.24.0" }
unzip_to = "${tools_dir}"
files = "*.exe"

[plantuml]
github = { repo = "plantuml/plantuml", asset = "plantuml.jar" }
save_as = "${tools_dir}/plantuml.jar"
install_exes = ["plantuml.jar"]

[internal-tool]
url = "s3://company-bucket/tool.tar.gz"
profile = "company-profile"
unzip_to = "${tools_dir}"
```

## Recipe Fields

| Field | Description |
|-------|-------------|
| `url` | Direct URL (HTTP/HTTPS/S3/local path) |
| `github` | `{ repo = "owner/repo", asset = "pattern", tag = "v1.0" }` |
| `unzip_to` | Extract archives to this directory |
| `save_as` | Save downloaded file to this path |
| `files` | Glob pattern for selective extraction (flattens structure) |
| `install_exes` | List of executables/JARs to install to ~/.local/bin |
| `no_shim` | `true` to copy directly instead of creating launchers |
| `profile` | AWS profile for S3 downloads |
| `executable` | `true` to set executable permission (Unix) |
| `lock` | `{ sha = "...", download_url = "..." }` for verification |

## Variables

Built-in variables for recipes:

| Variable | Value |
|----------|-------|
| `${os}` | `linux`, `macos`, `windows` |
| `${arch}` | `x86_64`, `aarch64`, etc. |
| `${home}` | User's home directory |
| `${recipe_dir}` | Directory containing the recipe |
| `${env.VAR}` | Environment variable |
| `~/path` | Expands to home directory |

## Common Patterns

### Install multiple tools from recipe

```toml
[vars]
bin = "${home}/.local/bin"

[ripgrep]
github = { repo = "BurntSushi/ripgrep" }
unzip_to = "/tmp/rg"
files = "*/rg"
install_exes = ["rg"]
no_shim = true

[fd]
github = { repo = "sharkdp/fd" }
unzip_to = "/tmp/fd"
files = "*/fd"
install_exes = ["fd"]
no_shim = true
```

### Java JAR application

```toml
[plantuml]
github = { repo = "plantuml/plantuml", asset = "plantuml.jar" }
save_as = "./tools/plantuml.jar"
install_exes = ["plantuml.jar"]
```

Creates launcher script:
```bash
#!/bin/sh
exec java -jar "/path/to/plantuml.jar" "$@"
```

### S3 with AWS profiles

```toml
[prod-tool]
url = "s3://prod-bucket/tool.tar.gz"
profile = "production"
unzip_to = "./tools"

[dev-tool]
url = "s3://dev-bucket/tool.tar.gz"
profile = "development"
unzip_to = "./tools"
```

### Pin versions with lock file

```bash
zipget recipe tools.toml --lock
```

Adds SHA-256 hashes and pins GitHub tags:

```toml
[ripgrep]
github = { repo = "BurntSushi/ripgrep", tag = "14.1.1" }
lock = { sha = "abc123...", download_url = "https://..." }
```

## Output Locations

- Cache: `/tmp/zipget-cache` (Unix) or `%TEMP%\zipget-cache` (Windows)
- Install: `~/.local/bin`
- Shims: `~/.local/bin/*.shim` + `*.exe` (Windows)

## Tips

- Use `--no-shim` on Unix for direct installation
- Use `files = "*/binary"` to extract single file from nested archive
- Use `--upgrade` to update all GitHub releases to latest
- JAR files in `install_exes` automatically get Java launchers
- Recipe URLs can be remote: `zipget recipe https://example.com/tools.toml`
