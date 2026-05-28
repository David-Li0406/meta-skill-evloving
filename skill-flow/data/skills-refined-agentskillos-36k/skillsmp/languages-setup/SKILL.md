---
name: languages-setup
description: Language and runtime setup guide using mise for version management including Go, Node.js, npm tasks, and environment variables
---

# Languages & Runtimes

This project uses mise for language version management and task execution.

- [Tool Versions](#tool-versions)
- [Available Tasks](#available-tasks)
- [Environment Variables](#environment-variables)
- [Usage](#usage)

## Tool Versions

The following tools are configured in `.mise.toml`:

- **Go**: `1.23.4` (migrated from asdf)
- **Node.js**: `lts` (migrated from n)

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

## Usage

```sh
# Install configured tools
mise install

# Check current versions
mise current

# Run tasks
mise run npm-tools
mise run dev
```
