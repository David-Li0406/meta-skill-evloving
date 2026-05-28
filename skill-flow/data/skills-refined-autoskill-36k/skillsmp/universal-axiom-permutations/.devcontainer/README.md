# DevContainer for The Universal Axiom

This DevContainer provides a complete, one-click development environment for The Universal Axiom with all languages and tools pre-configured.

## Features

- **Multi-Language Support**: Node.js, Python, Rust, and Julia pre-installed
- **Pre-configured Tools**: ESLint, Prettier, Black, Clippy, and more
- **Automatic Setup**: All dependencies installed on container creation
- **Git Integration**: Git hooks and workflow tools ready to use
- **VS Code Extensions**: Language servers and formatters for all supported languages

## Usage

### GitHub Codespaces

1. Click the "Code" button on GitHub
2. Select "Codespaces"
3. Click "Create codespace on main"
4. Wait for the container to build (first time takes ~5 minutes)
5. Start coding! All tools are ready.

### VS Code Remote - Containers

1. Install the "Remote - Containers" extension in VS Code
2. Open the repository folder
3. Click "Reopen in Container" when prompted
4. Wait for the container to build
5. Start coding!

### Manual Docker

```bash
# Clone the repository
git clone https://github.com/TheUniversalAxiom/pointy-stick.git
cd pointy-stick

# Build and run the container
docker build -t universal-axiom-dev .devcontainer
docker run -it -v $(pwd):/workspace universal-axiom-dev
```

## What's Included

### Languages & Runtimes
- **Node.js** (LTS): For JavaScript/TypeScript development
- **Python 3.11**: For Python development
- **Rust** (latest): For Rust development
- **Julia** (latest): For Julia development

### Development Tools
- Git (with hooks configured)
- Make
- npm, pip, cargo, Julia package manager
- Code formatters (Prettier, Black, rustfmt)
- Linters (ESLint, Pylint, Clippy)

### VS Code Extensions
- Language servers for all languages
- Code formatters
- Git tools
- Markdown support
- Spell checker

## Post-Creation Setup

The DevContainer automatically:
1. Installs all dependencies (Node, Python, Rust, Julia)
2. Builds TypeScript and MCP server
3. Sets up Git hooks
4. Runs verification tests
5. Displays helpful commands

## Quick Commands

After the container is ready:

```bash
# Show all available commands
make help

# Run tests for all languages
make test

# Verify all implementations
make verify

# Run examples
npm run example:js
python examples/python/basic_usage.py
cargo run --example basic_usage --manifest-path src/rust/Cargo.toml
julia examples/julia/basic_usage.jl
```

## Customization

Edit `.devcontainer/devcontainer.json` to:
- Add more VS Code extensions
- Change language versions
- Modify environment settings
- Add custom ports

Edit `.devcontainer/setup.sh` to:
- Add custom installation steps
- Configure additional tools
- Set up project-specific requirements

## Troubleshooting

### Container fails to build
- Check Docker is running and up to date
- Ensure you have enough disk space
- Try rebuilding: `Cmd/Ctrl + Shift + P` → "Rebuild Container"

### Git hooks not working
- Run `npm run prepare` manually
- Check file permissions in `.husky/`

### Python imports not working
- Run `pip install -e ".[dev]"` to install package in editable mode
- Reload VS Code window

## Resources

- [VS Code DevContainers Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)
- [The Universal Axiom Website](https://www.epiphanyengine.ai)
