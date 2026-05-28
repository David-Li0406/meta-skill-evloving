---
name: read-external
description: Read-only access to external repositories for cross-repo context. Use when you need to reference code, patterns, or documentation from the iOS UnaMentis repository.
allowed-tools: Read, Grep, Glob, Task
---

# Cross-Repository Read Access

This skill provides constrained read-only access to external repositories configured in `additionalDirectories`.

## Available External Repos

| Repo | Path | Purpose |
|------|------|---------|
| unamentis-ios | /Users/cygoerdt/unamentis | iOS companion app - reference for feature parity, Swift patterns, and shared architecture |

## Usage

Access is always active via `additionalDirectories` in settings.json. When you need external context:

1. **Find files**: Use `Glob` with the repo's absolute path
   ```
   Glob: /Users/cygoerdt/unamentis/**/*.swift
   ```

2. **Search content**: Use `Grep` with pattern in the repo path
   ```
   Grep: "SessionManager" in /Users/cygoerdt/unamentis/
   ```

3. **Read files**: Use `Read` with absolute path
   ```
   Read: /Users/cygoerdt/unamentis/UnaMentis/Core/Session/SessionManager.swift
   ```

## Common Cross-Reference Tasks

When working on UnaMentis Android, use this skill to:

- **Feature parity checks**: Compare iOS implementation before building Android equivalent
- **Architecture patterns**: Reference how iOS handles audio, VAD, curriculum, etc.
- **API contracts**: Verify shared server API usage between platforms
- **UI/UX reference**: Check iOS UI patterns for consistency

## Constraints

When this skill is explicitly invoked with `/read-external`:
- ONLY Read, Grep, Glob, and Task tools are available
- No modifications to external repos (Edit/Write blocked)
- Reference and adapt code, don't copy wholesale

## Adding New Repositories

See [TEMPLATE.md](TEMPLATE.md) for step-by-step instructions on adding new external repositories.
