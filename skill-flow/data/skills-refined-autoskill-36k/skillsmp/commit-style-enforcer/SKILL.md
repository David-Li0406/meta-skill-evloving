---
name: commit-style-enforcer
description: >-
  Generates properly formatted commit messages following project conventions.
  Use when creating commits or when users need help writing commit messages.
  Inspects staged changes and creates messages with component tags, concise
  summaries, and detailed descriptions.
allowed-tools: 'Bash, Read, Grep, Glob, Bash(git commit:*)'
metadata:
  sync:
    version: 2
    files: {}
    hash: sha256-e41a30e1a79737a14305e71b3ed7824aec7dcce3620fb812d2cddc9db23ee804
---
# Commit Style Enforcer

## Instructions

This skill enforces commit message conventions for the TypeScript SDK project. It analyzes staged changes and generates commit messages that follow the established patterns.

### Commit Message Format

Based on the project's commit history, follow this format:

1. **Component/Area Tag** (optional, in square brackets):
   - `[api]` - API changes
   - `[docs]` - Documentation updates
   - `[spec]` - Specification changes
   - `[examples]` - Example code changes
   - `[test]` - Test additions/modifications
   - `[types]` - TypeScript type definitions
   - `[validation]` - Schema validation changes
   - `[client]` - Client-side changes
   - `[server]` - Server-side changes
   - `[transport]` - Transport layer changes
   - `[auth]` - Authentication/OAuth changes
   - `[experimental]` - Experimental features
   - `[chore]` - Maintenance tasks, version bumps
   - `[build]` - Build system changes
   - `[ci]` - CI/CD configurations

2. **Concise Summary** (under 50 characters):
   - Use present tense ("add" not "added")
   - Use imperative mood ("fix" not "fixes")
   - No period at the end
   - Start with capital letter

3. **PR Reference** (optional, in parentheses):
   - `(#1234)` - Reference to pull request number

### Step-by-Step Process

1. **Check staged changes**:
   ```bash
   git diff --staged --stat
   git diff --staged
   ```

2. **Analyze affected components**:
   - Identify main directories and files changed
   - Determine appropriate component tags
   - Assess scope of changes (single component vs multiple)

3. **Generate commit message**:
   - Start with component tag(s) if applicable
   - Write concise summary under 50 characters
   - Add detailed description explaining:
     - What changed
     - Why the change was necessary
     - Any breaking changes or migration notes
     - References to related issues or specs

4. **Validate the message**:
   - Summary line under 50 characters
   - Proper tag format: `[tag]`
   - Clear description that explains the change

### Examples

**Good examples from project history**:
```
Add create-skill command
Update server examples and docs (#1285)
SPEC COMPLIANCE: Remove loose/passthrough types not allowed/defined by MCP spec + Task types (#1242)
[Docs] Fix typo (#1067)
fix: Support updating output schema (#1048)
chore: bump version for patch release (#1235)
```

**Generated examples**:
```
[client] Add OAuth authentication helper for token management

- Implement new OAuth client with PKCE flow
- Add token refresh logic
- Support for multiple auth providers
- Breaking: OAuthConfiguration interface updated

This addresses the need for standardized OAuth authentication
across all client implementations, replacing the previous
ad-hoc token management approach.

[types] Update Resource and Tool schemas for MCP spec v2025-11-25

- Add new optional fields for resource metadata
- Update Tool input validation to support recursive schemas
- Deprecate legacy fields in Resource schema
- Add JSON schema examples in type comments

Aligns with latest MCP specification changes and ensures
compatibility with upcoming server implementations.

[transport] Fix memory leak in StreamableHTTP transport

- Properly close EventSource connections on cleanup
- Add connection pool management
- Fix timeout handling for long-running requests
- Add unit tests for edge cases

Resolves issue where HTTP connections were not properly
closed, leading to memory exhaustion in long-running
processes.

[docs] Update authentication examples with OAuth flows

- Add complete OAuth 2.0 client credentials example
- Document PKCE flow implementation
- Include refresh token handling
- Update troubleshooting section

Authentication documentation was outdated and didn't
reflect the new OAuth capabilities introduced in v1.20.0.
```

### Common Patterns

**Type definitions changes**:
```
[types] Add new union types for experimental features
```

**Bug fixes**:
```
[validation] Fix schema validation for nested objects
```

**Documentation**:
```
[docs] Update API reference with new methods
```

**Multiple components**:
```
[client][server] Add bidirectional streaming support
```

**Breaking changes** (include breaking in summary):
```
[api] BREAKING: Change request/response format for v2
```

### Special Cases

1. **PR commits**: Include PR number in parentheses
2. **Reverts**: Start with `revert:`
3. **Dependencies**: Use `chore(deps):` prefix
4. **Performance**: Add `[perf]` tag when relevant

## Configuration

The skill automatically detects the project context and adapts the commit style based on:
- Project type (TypeScript SDK)
- Existing commit patterns
- Affected components
- Scope of changes

## Usage

Simply ask the skill to help with commit messages:
- "Help me write a commit message for these changes"
- "What's a good commit message for the staged changes?"
- "Review and improve my commit message"
