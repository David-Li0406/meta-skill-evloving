# Installation

## Quick Install

```bash
# Via pip
pip install mcp-b

# Via uv
uvx mcp-b demo

# With full dependencies
pip install mcp-b[full]

# Development install
pip install mcp-b[dev]
```

## From Source

```bash
git clone https://github.com/bjoernbethge/mcp-b.git
cd mcp-b
pip install -e ".[dev,full]"
```

## Requirements

- Python 3.11+
- Node.js 20+ (for MCP servers)

## MCP Server Setup

### Serena (Semantic Code Analysis)

```bash
pip install uvx
```

Configuration is in `.github/copilot/mcp.json`.

### Context7 (Documentation)

Get your API key from [context7.com](https://context7.com/dashboard).

Set environment variable:
```bash
export CONTEXT7_API_KEY="your-api-key"
```

## Dev Container

For VS Code/GitHub Codespaces, the `.devcontainer/devcontainer.json` provides a pre-configured environment with all tools installed.
