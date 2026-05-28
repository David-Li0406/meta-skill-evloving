---
name: mise-guide
description: Mise tool version management guide including runtime management (Node.js, Go), NPM package installation, home-manager configuration, and troubleshooting
---

# mise

[mise](https://mise.jdx.dev/) is a tool for managing multiple runtimes and tools.

## Overview

mise is configured and managed through home-manager.

## Configuration Files

- **home-manager configuration**: `home-manager/mise/default.nix`
- **Generated configuration**: `~/.config/mise/config.toml`

## Managed Tools

### Programming Languages

- **Node.js**: `lts`
- **Go**: `1.23.4`

### NPM Packages

Packages directly managed by mise:

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

## Configuration Editing

Edit home-manager configuration:

```nix
# home-manager/mise/default.nix
programs.mise = {
  enable = true;
  enableZshIntegration = true;

  globalConfig = {
    tools = {
      node = "lts";
      go = "1.23.4";
      "npm:@redocly/cli" = "latest";
      # ... other tools
    };

    tasks = {
      npm-commitizen = {
        description = "Install commitizen and cz-git globally";
        run = [
          "npm install -g commitizen cz-git"
        ];
      };
    };
  };
};
```

Apply configuration changes:

```sh
make home-manager-apply
```

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
