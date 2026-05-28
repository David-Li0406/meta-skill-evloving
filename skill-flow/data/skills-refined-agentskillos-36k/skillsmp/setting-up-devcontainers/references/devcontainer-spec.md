# Devcontainer Specification Reference

Quick reference for devcontainer.json configuration relevant to Claude Code setups.

## Contents

- [Key Fields](#key-fields) - build, mounts, remoteUser
- [Lifecycle Commands](#lifecycle-commands) - postCreateCommand, postStartCommand
- [Volume Naming](#volume-naming) - marketplace-specific volumes
- [Dockerfile Requirements](#dockerfile-requirements) - packages, user creation, PATH

## Key Fields

### build

Defines how to build the container:

```json
{
  "build": {
    "dockerfile": "Dockerfile",
    "context": "."
  }
}
```

### mounts

Mount volumes or directories:

```json
{
  "mounts": [
    "source=volume-name,target=/path/in/container,type=volume",
    "source=${localWorkspaceFolder},target=/workspaces/project,type=bind"
  ]
}
```

**Mount types**:
- `volume` - Named Docker volume (persistent across rebuilds)
- `bind` - Bind mount from host filesystem

### remoteUser

Non-root user to use:

```json
{
  "remoteUser": "vscode"
}
```

### Lifecycle Commands

```json
{
  "postCreateCommand": "bash setup.sh",
  "postStartCommand": "bash sync.sh",
  "postAttachCommand": "echo 'attached'"
}
```

| Command | When | Use Case |
|---------|------|----------|
| `postCreateCommand` | After container first created | Install tools, one-time setup |
| `postStartCommand` | Every container start | Sync files, refresh caches |
| `postAttachCommand` | When user attaches | User notifications |

## Volume Naming

For Claude Code, use marketplace-specific volume names:

```
claude-config-{marketplace-name}   → ~/.claude
claude-data-{marketplace-name}     → ~/.local/share/claude
```

This allows multiple marketplaces to have independent credential stores.

## Dockerfile Requirements

Required packages for Claude Code:
```dockerfile
RUN apt-get update && apt-get install -y \
    curl git jq ca-certificates sudo zsh python3 ripgrep \
    && rm -rf /var/lib/apt/lists/*
```

User creation with UID/GID 1000 handling (ubuntu image has existing user):
```dockerfile
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN if getent group $USER_GID > /dev/null 2>&1; then \
        groupmod -n $USERNAME $(getent group $USER_GID | cut -d: -f1); \
    else \
        groupadd --gid $USER_GID $USERNAME; \
    fi \
    && if getent passwd $USER_UID > /dev/null 2>&1; then \
        usermod -l $USERNAME -d /home/$USERNAME -m -s /bin/zsh $(getent passwd $USER_UID | cut -d: -f1); \
    else \
        useradd --uid $USER_UID --gid $USER_GID -m -s /bin/zsh $USERNAME; \
    fi \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
```

PATH configuration (binary installed to ~/.local/bin):
```dockerfile
ENV PATH="/home/vscode/.local/bin:$PATH"
```

## Example: Complete devcontainer.json

```json
{
  "name": "my-marketplace-devcontainer",
  "build": {
    "dockerfile": "Dockerfile"
  },
  "mounts": [
    "source=claude-config-my-marketplace,target=/home/vscode/.claude,type=volume",
    "source=claude-data-my-marketplace,target=/home/vscode/.local/share/claude,type=volume"
  ],
  "remoteUser": "vscode",
  "postCreateCommand": "bash .devcontainer/post-create.sh",
  "postStartCommand": "bash .devcontainer/reinstall-marketplace.sh"
}
```
