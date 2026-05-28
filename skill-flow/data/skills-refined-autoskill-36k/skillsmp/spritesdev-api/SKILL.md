---
name: Sprites.dev API
description: |
  This skill should be used when the user asks about "sprites", "sprite API",
  "Sprites.dev", "cloud sandbox", "remote execution with sprites", "sprite CLI",
  "sprite filesystem API", "sprite sessions", or needs guidance on working with
  Sprites.dev cloud development environments.
version: 1.0.0
---

# Sprites.dev API Knowledge

## Overview

Sprites.dev provides persistent cloud sandboxes (called "sprites") for running code remotely. Key features:
- Persistent ext4 filesystems that survive hibernation
- Auto-hibernation after 30 seconds of inactivity (no compute cost when idle)
- Instant wake on any request
- Session management for long-running processes
- Filesystem API for direct file operations

## CLI Reference

### Sprite Management
```bash
sprite create <name>          # Create new sprite
sprite list                   # List all sprites
sprite use <name>             # Set active sprite for directory
sprite use                    # Show current active sprite
sprite destroy <name>         # Delete sprite (permanent)
```

### Command Execution
```bash
sprite exec "command"                    # One-off execution
sprite exec -detachable "command"        # Detachable session
sprite exec -env KEY=VAL "command"       # With environment variables
sprite exec -dir /path "command"         # With working directory
sprite exec -file local:/remote "cmd"    # Upload file before exec
```

### Session Management
```bash
sprite sessions list          # List running sessions
sprite sessions attach <id>   # Reattach to session
sprite sessions kill <id>     # Terminate session
```
**Detach from session**: Press `Ctrl+\` (keeps running in background)

### Port Forwarding
```bash
sprite proxy <port>           # Forward sprite port to localhost
```

## Filesystem API

Base URL: `https://api.sprites.dev/v1`
Auth: `Authorization: Bearer <token>`

### Write File
```bash
curl -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@localfile.txt" \
  "https://api.sprites.dev/v1/sprites/NAME/fs/write?path=remote.txt&workingDir=/home/sprite&mkdir=true"
```

### Read File
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.sprites.dev/v1/sprites/NAME/fs/read?path=file.txt&workingDir=/home/sprite"
```

### List Directory
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.sprites.dev/v1/sprites/NAME/fs/list?path=.&workingDir=/home/sprite"
```

### Delete
```bash
curl -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"path":"file.txt","workingDir":"/home/sprite","recursive":false,"asRoot":false}' \
  "https://api.sprites.dev/v1/sprites/NAME/fs/delete"
```

## Authentication

Token stored in `~/.sprites/sprites.json` after running `sprite org auth`.

Extract token:
```bash
jq -r '.token' ~/.sprites/sprites.json
```

## Best Practices

1. **Use detachable sessions** for long-running processes (dev servers, builds, tests)
2. **Sync git-tracked files** rather than entire directories to avoid bloat
3. **Port forward** for accessing web UIs running in sprites
4. **Check sessions** before creating new ones to avoid orphaned processes
5. **Sprites hibernate automatically** - no need to manually stop them
6. **Use checkpoints** for creating clean restore points (filesystem snapshots)

## Common Patterns

### Development Server
```bash
sprite create my-dev
sprite use my-dev
# sync files
sprite exec -detachable "npm run dev"
sprite proxy 3000
# Access at localhost:3000
```

### CI-style Execution
```bash
sprite exec "npm install && npm test && npm run build"
```

### Background Build
```bash
sprite exec -detachable "npm run build:watch"
sprite sessions list  # to monitor
```
