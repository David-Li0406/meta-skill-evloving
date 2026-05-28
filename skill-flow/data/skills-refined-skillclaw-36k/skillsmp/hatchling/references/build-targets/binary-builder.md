---
name: "Hatchling Binary Builder"
description: "Create standalone executables from Python applications: PyApp integration, cross-compilation, multi-version binaries, and distribution strategies"
---

# Binary Builder

The binary builder creates standalone executable applications using [PyApp](https://github.com/ofek/pyapp), allowing Python applications to bootstrap themselves at runtime without requiring Python to be pre-installed. This is ideal for CLI tools and applications that need zero-installation deployment.

## Requirements

- [Rust](https://www.rust-lang.org) toolchain installed
- PyApp (installed automatically or can be built locally)

## Configuration

The binary builder is configured in the `pyproject.toml` file:

```toml
[tool.hatch.build.targets.binary]
# Configuration options here
```

## Options

| Option           | Default           | Description                    |
| ---------------- | ----------------- | ------------------------------ |
| `scripts`        | all defined       | Array of script names to build |
| `python-version` | latest compatible | The Python version ID to embed |
| `pyapp-version`  | latest            | The version of PyApp to use    |

### Example Configuration

```toml
[tool.hatch.build.targets.binary]
scripts = ["myapp-cli", "myapp-admin"]
python-version = "3.11"
pyapp-version = "0.22.0"
```

## Build Behavior

### Script-Based Building

If scripts are defined in your project:

```toml
[project.scripts]
myapp = "myapp.cli:main"
myapp-admin = "myapp.admin:main"

[tool.hatch.build.targets.binary]
# Builds both scripts as separate executables
```

### Module-Based Building

If no scripts are defined, builds a single executable based on the project name:

```toml
[project]
name = "myapp"
# Assumes myapp/__main__.py exists

[tool.hatch.build.targets.binary]
# Builds single "myapp" executable
```

## Output Structure

Binary executables are built in the `app` subdirectory of the output directory:

```text
dist/
└── app/
    ├── myapp         # Unix executable
    ├── myapp.exe     # Windows executable
    └── myapp-admin   # Additional script
```

## Environment Variables

### Build Configuration

| Variable             | Description                            |
| -------------------- | -------------------------------------- |
| `CARGO`              | Path to Rust cargo executable          |
| `CARGO_BUILD_TARGET` | Target triple (appended to filename)   |
| `PYAPP_REPO`         | Local PyApp repository for development |

### Runtime Configuration

PyApp executables support various runtime environment variables:

| Variable               | Description                      |
| ---------------------- | -------------------------------- |
| `PYAPP_PYTHON_VERSION` | Override embedded Python version |
| `PYAPP_UPGRADE`        | Auto-upgrade the application     |
| `PYAPP_SKIP_INSTALL`   | Skip installation step           |

## Platform Support

### Cross-Compilation

Set the target platform using Rust's standard target triple:

```bash
# Build for Windows from Linux/macOS
export CARGO_BUILD_TARGET=x86_64-pc-windows-gnu
hatch build -t binary

# Build for Linux from macOS
export CARGO_BUILD_TARGET=x86_64-unknown-linux-gnu
hatch build -t binary
```

### Architecture Support

Common target triples:

- `x86_64-pc-windows-msvc` - Windows 64-bit
- `x86_64-apple-darwin` - macOS Intel
- `aarch64-apple-darwin` - macOS Apple Silicon
- `x86_64-unknown-linux-gnu` - Linux 64-bit
- `aarch64-unknown-linux-gnu` - Linux ARM64

## PyApp Configuration

### Embedding Python Version

```toml
[tool.hatch.build.targets.binary]
python-version = "3.11"  # Uses Python 3.11.x
# or
python-version = "3.11.5"  # Specific version
```

### Custom PyApp Options

Configure PyApp behavior through environment variables during build:

```bash
# Use specific Python distribution
export PYAPP_PYTHON_VERSION="3.11"

# Enable additional features
export PYAPP_FULL_ISOLATION="1"
export PYAPP_UPGRADE_VIRTUALENV="1"

hatch build -t binary
```

## Advanced Usage

### Local PyApp Development

Use a local PyApp repository for development:

```bash
# Clone PyApp locally
git clone https://github.com/ofek/pyapp.git

# Set environment variable
export PYAPP_REPO=/path/to/pyapp

# Build using local PyApp
hatch build -t binary
```

### Multiple Binary Configurations

Create different binary variants using build versions:

```toml
[tool.hatch.build.targets.binary]
scripts = ["myapp"]

[[tool.hatch.build.targets.binary.versions]]
name = "minimal"
python-version = "3.10"

[[tool.hatch.build.targets.binary.versions]]
name = "full"
python-version = "3.11"
```

Build specific versions:

```bash
hatch build -t binary:minimal
hatch build -t binary:full
```

## Application Distribution

### Single-File Executable

The binary builder produces a single executable file that includes:

- PyApp runtime
- Python interpreter (downloaded on first run)
- Your application code
- All dependencies

### First-Run Behavior

On first execution:

1. PyApp downloads the specified Python version
2. Creates a virtual environment
3. Installs your application and dependencies
4. Runs your application

Subsequent runs use the cached environment.

## Common Patterns

### CLI Application

```toml
[project]
name = "mytool"
version = "1.0.0"

[project.scripts]
mytool = "mytool.cli:main"

[tool.hatch.build.targets.binary]
scripts = ["mytool"]
python-version = "3.11"
```

### Multiple Entry Points

```toml
[project.scripts]
server = "myapp.server:run"
worker = "myapp.worker:start"
admin = "myapp.admin:cli"

[tool.hatch.build.targets.binary]
scripts = ["server", "worker", "admin"]
```

### GUI Application

```toml
[project]
name = "myguiapp"
dependencies = ["tkinter", "pyqt5"]

[tool.hatch.build.targets.binary]
python-version = "3.11"

# Configure PyApp for GUI
# Set via environment variables during build
# PYAPP_IS_GUI=1
```

## Build Optimization

### Release Builds

Enable optimizations for production:

```bash
# Enable Rust optimizations
export CARGO_PROFILE_RELEASE_LTO=true
export CARGO_PROFILE_RELEASE_CODEGEN_UNITS=1
export CARGO_PROFILE_RELEASE_STRIP=symbols

hatch build -t binary
```

### Binary Size Reduction

Strategies to reduce executable size:

1. Use UPX compression (post-build)
2. Strip debug symbols
3. Minimize dependencies

```bash
# Build with stripping
export CARGO_PROFILE_RELEASE_STRIP=symbols
hatch build -t binary

# Compress with UPX (if installed)
upx --best dist/app/myapp
```

## Troubleshooting

### Rust Not Found

Ensure Rust is installed:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

### Build Failures

Check Rust toolchain:

```bash
rustc --version
cargo --version
```

Update toolchain:

```bash
rustup update
```

### Cross-Compilation Issues

Install required targets:

```bash
# For Windows target
rustup target add x86_64-pc-windows-gnu

# For Linux target
rustup target add x86_64-unknown-linux-gnu
```

### PyApp Version Issues

Explicitly specify PyApp version:

```toml
[tool.hatch.build.targets.binary]
pyapp-version = "0.22.0"  # Use specific version
```

## Performance Considerations

### Startup Time

First run is slower due to:

- Python download
- Virtual environment creation
- Dependency installation

Subsequent runs are fast (near-native Python speed).

### Cache Location

PyApp caches Python and environments in:

- Windows: `%LOCALAPPDATA%\pyapp`
- Unix: `~/.local/share/pyapp`

### Memory Usage

Binary executables have similar memory footprint to regular Python applications after initial setup.

## Quick Decision Guide

**Use binary builder when:**

- Creating a CLI tool that needs zero Python installation dependencies
- Distributing to end users who don't have Python installed
- Building a cross-platform application (can build Windows binaries from Linux/macOS)
- You want automatic Python version embedding

**Don't use binary builder for:**

- Libraries (use wheel instead)
- GUI applications requiring complex system integration
- Packages that need source distribution

## Security Considerations

### Code Signing

Sign executables for distribution:

**Windows:**

```bash
signtool sign /a /t http://timestamp.digicert.com dist/app/myapp.exe
```

**macOS:**

```bash
codesign --sign "Developer ID" dist/app/myapp
```

### Distribution Verification

Include checksums with releases:

```bash
sha256sum dist/app/* > dist/app/checksums.txt
```

## Comparison with Other Solutions

| Feature              | Binary Builder | PyInstaller | Nuitka    | cx_Freeze |
| -------------------- | -------------- | ----------- | --------- | --------- |
| Single File          | ✓              | ✓           | ✓         | ✗         |
| No Python Required   | ✓              | ✓           | ✓         | ✓         |
| Cross-Platform Build | ✓              | ✗           | Limited   | ✗         |
| Size                 | Small\*        | Large       | Medium    | Large     |
| Startup Speed        | Fast\*\*       | Slow        | Fast      | Medium    |
| Build Speed          | Fast           | Slow        | Very Slow | Medium    |

\* Initial download required \*\* After first run

## See Also

- [PyApp Documentation](https://github.com/ofek/pyapp)
- [Rust Installation](https://www.rust-lang.org/tools/install)
- [Cargo Build Documentation](https://doc.rust-lang.org/cargo/commands/cargo-build.html)
- [Python Packaging - Binary Extensions](https://packaging.python.org/guides/packaging-binary-extensions/)
