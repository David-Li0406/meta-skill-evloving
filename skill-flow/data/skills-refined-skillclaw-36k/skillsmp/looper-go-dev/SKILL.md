---
name: looper-go-dev
description: Looper-Go development workflows: build, test, run, debug, and manage the looper-go project. Use when working on looper-go codebase, running tests, building binaries, or debugging issues.
---

# Looper-Go Development

## Overview

Looper-Go is a Go implementation of the autonomous AI loop runner. This skill covers common development workflows.

## Project Structure

```
looper-go/
├── cmd/looper/          # CLI entry point
├── internal/
│   ├── config/          # Configuration loading
│   ├── agents/          # Agent runners
│   ├── loop/            # Main orchestration
│   ├── todo/            # Task file handling
│   ├── prompts/         # Prompt templates
│   ├── logging/         # JSONL logging
│   └── hooks/           # Post-iteration hooks
├── prompts/             # Bundled prompt templates
└── to-do.json           # Task file (runtime)
```

## Common Commands

### Build
```bash
# Build binary
go build ./cmd/looper

# Build to custom location
go build -o ~/bin/looper ./cmd/looper

# Build for multiple platforms
go build -o bin/looper-linux ./cmd/looper
GOOS=darwin go build -o bin/looper-macos ./cmd/looper
GOOS=windows go build -o bin/looper.exe ./cmd/looper
```

### Test
```bash
# Run all tests
go test ./...

# Run with coverage
go test -cover ./...

# Run specific package
go test ./internal/loop

# Verbose output
go test -v ./internal/loop

# Run make test (includes smoke tests)
make test
```

### Run
```bash
# Default run (uses to-do.json in current dir)
looper run

# Specify max iterations
LOOPER_MAX_ITERATIONS=5 looper run

# Run with specific task file
looper --task-file path/to/tasks.json run

# View logs
looper tail

# List tasks
looper ls

# Show config
looper config

# Check dependencies
looper doctor
```

### Debug
```bash
# Enable debug logging
LOOPER_DEBUG=1 looper run

# View JSONL logs
looper tail

# View specific run
looper tail --run <run-id>

# Validate task file
looper validate

# Format task file
looper fmt
```

## Development Workflow

### 1. Make Changes

Edit code in `internal/` or `cmd/` as needed.

### 2. Test Changes

```bash
# Run unit tests
go test ./...

# Run smoke tests
make test

# Run live test
~/.codex/skills/looper-live-test/scripts/run-live-test.sh
```

### 3. Commit Changes

```bash
# Check status
git status

# Run pre-commit hooks (if installed)
pre-commit run --all-files

# Commit
git commit -m "feat: description"
```

### 4. Build and Install

```bash
# Build
go build ./cmd/looper

# Install to PATH
go install ./cmd/looper
```

## Configuration

### Config File Locations (priority order)

1. `.looper/config.json` - Project-specific
2. `~/.config/looper/config.json` - User config
3. Environment variables (`LOOPER_*`)
4. CLI flags

### Example Config

```json
{
  "max_iterations": 100,
  "agent": {
    "type": "claude",
    "model": "claude-3-5-sonnet-20241022"
  },
  "paths": {
    "log_dir": "./looper-logs"
  }
}
```

## Key Environment Variables

| Variable | Purpose |
|----------|---------|
| `LOOPER_MAX_ITERATIONS` | Max loop iterations |
| `LOOPER_DEBUG` | Enable debug logging |
| `LOOPER_AGENT_TYPE` | Agent type (codex, claude) |
| `LOOPER_TASK_FILE` | Path to task file |
| `CODEX_JSON_LOG` | Codex JSON log mode (legacy) |

## Troubleshooting

### Build Fails

```bash
# Clean and rebuild
go clean -cache
go mod tidy
go build ./cmd/looper
```

### Tests Fail

```bash
# Run verbose to see details
go test -v ./...

# Check specific package
go test -v ./internal/loop
```

### Agent Not Found

```bash
# Check config
looper config

# Verify agent binary exists
which codex
which claude

# Check in config
cat .looper/config.json | jq '.agent'
```

## Adding New Features

### 1. Add Internal Package

```bash
mkdir internal/feature
# Create feature.go
```

### 2. Add Tests

```bash
# Create feature_test.go
go test ./internal/feature
```

### 3. Wire Into Loop

Edit `internal/loop/loop.go` to use new feature.

### 4. Update Documentation

- Edit `ARCHITECTURE.md` if structural change
- Edit `README.md` if user-facing
- Add godoc comments

## Release Process

Use the `release-runbook` skill:

```bash
~/.codex/skills/release-runbook/scripts/release.sh --version 1.2.3 --test-cmd "make test"
```

## Code Style

- Standard Go formatting (`gofmt`)
- Conventional commits for commit messages
- Add tests for new functionality
- Update documentation

## Resources

- `ARCHITECTURE.md` - Full architecture documentation
- `README.md` - User documentation
- `CONTRIBUTING.md` - Contribution guidelines
- `AI_POLICY.md` - AI contribution policy
