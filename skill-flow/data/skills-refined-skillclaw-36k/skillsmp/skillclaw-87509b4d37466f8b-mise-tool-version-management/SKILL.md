---
name: mise-tool-version-management
description: Use this skill when you need to manage multiple programming languages and tools using mise, including installation, configuration, and troubleshooting.
---

# Skill body

## Overview

This skill provides guidance on managing multiple runtimes and tools using the mise tool. It covers installation, configuration, and troubleshooting for programming languages like Node.js and Go, as well as npm package management.

## Configuration Files

- **Home-manager configuration**: `home-manager/mise/default.nix`
- **Generated configuration**: `~/.config/mise/config.toml`

## Managed Tools

### Programming Languages

- **Node.js**: `lts`
- **Go**: `1.23.4`

### NPM Packages

Packages managed by mise include:

- `@redocly/cli` - CLI tool for OpenAPI/Swagger
- `corepack` - Node.js package manager management
- `@anthropic-ai/claude-code` - CLI tool for Claude AI
- `@google/gemini-cli` - CLI tool for Google Gemini

### NPM Global Packages (via Tasks)

Installed via tasks due to complex dependencies:

- `commitizen` - Git commit convention tool
- `cz-git` - commitizen adapter

## Commands

### Basic Operations

```sh
# List installed tools
make mise-list

# Check mise configuration
make mise-config

# Install all tools
make mise-install-all
```

### Individual Tool Operations

```sh
# Install specific tools
mise install go@1.23.4
mise install node@lts

# Use specific tools
mise use go@1.23.4
mise use node@lts
```

### NPM Packages

```sh
# Install commitizen + cz-git
make mise-install-npm-commitizen

# Direct execution
mise run npm-commitizen
```

## Available Tasks

### npm-tools

Installs global npm packages required for development:

```sh
mise run npm-tools
# or
make npm-tools
```

Installs:
- npm (latest)
- commitizen
- cz-git
- @redocly/cli
- corepack
- @anthropic-ai/claude-code
- @google/gemini-cli

### dev

Development environment setup:

```sh
mise run dev
```

## Environment Variables

Configured environment variables:

- `NODE_ENV`: Set to "development"
- `GOPATH`: Set to "$XDG_DATA_HOME/go"

## Troubleshooting

### When PATH is not recognized

```sh
# Restart shell
exec zsh

# Or manually initialize mise
eval "$(mise activate zsh)"
```

### When tools are not found

```sh
# Check mise status
mise doctor

# Reload configuration
mise config
```

## Related Documents

- [npm tools](50_npm_tools.md) - NPM package management
- [Languages](30_languages.md) - Programming language environments