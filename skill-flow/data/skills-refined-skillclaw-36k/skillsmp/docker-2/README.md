# Docker Development Skill for Claude Code

A Claude Code skill for container-based development with Docker. Ensures all package installations and code execution happen inside containers, keeping your host machine clean.

## Installation

```bash
git clone https://github.com/wrsmith108/docker-claude-skill.git ~/.claude/skills/docker
```

## Key Principle

**Never run `npm`, `node`, `npx`, `tsx`, or project scripts directly on the host machine.**

Always use `docker exec <container-name> <command>` instead.

## What's Included

- **First-Time Setup Guide**: Step-by-step configuration for new projects
- **Native Module Compatibility**: Alpine vs Slim decision guide (glibc requirements)
- **Enforcement Rules**: Block npm/node commands from running on host
- **Pre-Flight Checks**: Verify container status before commands
- **Command Reference**: docker exec, docker-compose patterns
- **Troubleshooting**: Common issues including `ERR_DLOPEN_FAILED` fixes
- **Project Configuration**: `.claude/docker-config.json` for per-project settings

## Quick Start

### 1. Configure for Your Project

Create `.claude/docker-config.json`:

```json
{
  "containerName": "my-project-dev-1",
  "baseImage": "node:20-slim",
  "port": 3000,
  "hasNativeModules": true
}
```

### 2. Choose Base Image

| Your Project Has | Use |
|------------------|-----|
| Native modules (sqlite, sharp, bcrypt) | `node:20-slim` |
| Pure JavaScript/TypeScript only | `node:20-alpine` |
| Unsure | `node:20-slim` (safe default) |

### 3. Start Container

```bash
docker compose --profile dev up -d
docker exec my-project-dev-1 npm install
```

### 4. Run Commands in Container

```bash
docker exec my-project-dev-1 npm test
docker exec my-project-dev-1 npm run build
docker exec my-project-dev-1 npm run lint
```

## Why Docker?

- **Clean Host**: No node_modules pollution on your machine
- **Reproducible**: Same environment for all developers
- **Isolated**: Project dependencies don't conflict
- **Secure**: No global package installations

## License

MIT - See [LICENSE](LICENSE)
