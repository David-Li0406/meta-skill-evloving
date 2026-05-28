---
name: build
description: Build the project. Use when compiling code, creating artifacts, or preparing for deployment.
allowed-tools: Bash, Read, Glob
---

# Build - argus

Build the project.

## Command

```bash
go build ./...
```

## Description

Build all packages

## Entry Point

Main: `cmd/argus/main.go`

## On Failure

- Check for syntax errors in the output
- Verify all dependencies are installed
- Check for type errors (if applicable)
- Review recent changes that might have broken the build

## Success Criteria

- Build completes without errors
- Output artifacts are generated correctly
