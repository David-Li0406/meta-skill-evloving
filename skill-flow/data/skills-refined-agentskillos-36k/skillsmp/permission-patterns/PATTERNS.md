# Permission Patterns

Comprehensive guide to permission pattern syntax for all tool types.

## Pattern Syntax Overview

Permission rules use the format: `Tool` or `Tool(specifier)`

```json
{
  "permissions": {
    "allow": ["Tool", "Tool(specifier)"],
    "ask": ["Tool(specifier)"],
    "deny": ["Tool(specifier)"]
  }
}
```

## Bash Command Patterns

### Basic Syntax

| Pattern | Matches | Example |
|---------|---------|---------|
| `Bash(command)` | Exact command | `Bash(npm test)` |
| `Bash(prefix:*)` | Commands starting with prefix | `Bash(git log:*)` |
| `Bash(prefix *)` | Commands with prefix (space variant) | `Bash(npm run *)` |
| `Bash(* suffix)` | Commands ending with suffix | `Bash(* --help)` |
| `Bash(part * part)` | Commands with wildcards | `Bash(git * main)` |

### Git Commands

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git branch:*)",
      "Bash(git show:*)",
      "Bash(git stash:*)"
    ],
    "ask": [
      "Bash(git push:*)",
      "Bash(git commit:*)",
      "Bash(git merge:*)",
      "Bash(git rebase:*)",
      "Bash(git reset:*)"
    ],
    "deny": [
      "Bash(git push --force:*)",
      "Bash(git push -f:*)"
    ]
  }
}
```

### Package Manager Commands

#### npm
```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(npm test:*)",
      "Bash(npm run build:*)",
      "Bash(npm run lint:*)",
      "Bash(npx *)"
    ],
    "ask": [
      "Bash(npm install:*)",
      "Bash(npm publish:*)"
    ]
  }
}
```

#### Bun
```json
{
  "permissions": {
    "allow": [
      "Bash(bun run *)",
      "Bash(bun test:*)",
      "Bash(bun build:*)",
      "Bash(bunx *)"
    ],
    "ask": [
      "Bash(bun install:*)",
      "Bash(bun add:*)"
    ]
  }
}
```

#### Yarn
```json
{
  "permissions": {
    "allow": [
      "Bash(yarn *)",
      "Bash(yarn test:*)",
      "Bash(yarn build:*)"
    ],
    "ask": [
      "Bash(yarn add:*)",
      "Bash(yarn publish:*)"
    ]
  }
}
```

### Build Tools

```json
{
  "permissions": {
    "allow": [
      "Bash(make *)",
      "Bash(cmake *)",
      "Bash(cargo build:*)",
      "Bash(cargo test:*)",
      "Bash(go build:*)",
      "Bash(go test:*)"
    ]
  }
}
```

### Docker Commands

```json
{
  "permissions": {
    "allow": [
      "Bash(docker ps:*)",
      "Bash(docker logs:*)",
      "Bash(docker images:*)"
    ],
    "ask": [
      "Bash(docker build:*)",
      "Bash(docker run:*)",
      "Bash(docker compose:*)"
    ],
    "deny": [
      "Bash(docker rm -f *)",
      "Bash(docker system prune:*)"
    ]
  }
}
```

### Pattern Limitations

Be aware of pattern bypass possibilities:

| Pattern | Intended | Could Match |
|---------|----------|-------------|
| `Bash(npm run build)` | `npm run build` | Only exact match |
| `Bash(git push:*)` | `git push origin main` | Also `git push --force` |
| `Bash(curl *)` | Block curl | Can be bypassed with options |

For critical security, use `deny` rules and consider hooks for validation.

## File Path Patterns

### Path Types

| Pattern Prefix | Meaning | Example |
|----------------|---------|---------|
| `//path` | Absolute filesystem path | `Read(//Users/alice/secrets/**)` |
| `~/path` | Home directory relative | `Read(~/Documents/*.pdf)` |
| `/path` | Settings file relative | `Edit(/src/**/*.ts)` |
| `path` or `./path` | Current directory relative | `Read(*.env)` |

### Glob Syntax (gitignore-style)

| Pattern | Matches |
|---------|---------|
| `*` | Any file in directory |
| `**` | Any files recursively |
| `*.ts` | All .ts files |
| `**/*.ts` | All .ts files recursively |
| `src/**` | Everything in src/ |

### Read Patterns

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Read(/docs/**)",
      "Read(~/.zshrc)",
      "Read(//etc/hosts)"
    ],
    "deny": [
      "Read(/.env)",
      "Read(/.env.*)",
      "Read(/secrets/**)",
      "Read(~/.ssh/**)"
    ]
  }
}
```

### Edit/Write Patterns

```json
{
  "permissions": {
    "allow": [
      "Edit(/src/**/*.ts)",
      "Edit(/src/**/*.tsx)",
      "Edit(/tests/**)",
      "Write(/dist/**)"
    ],
    "ask": [
      "Edit(/package.json)",
      "Edit(/tsconfig.json)"
    ],
    "deny": [
      "Edit(/.env)",
      "Edit(/credentials/**)",
      "Write(//etc/**)"
    ]
  }
}
```

### Common File Patterns

```json
{
  "permissions": {
    "allow": [
      "Edit(/src/**)",
      "Edit(/lib/**)",
      "Edit(/tests/**)",
      "Edit(/docs/**)"
    ],
    "deny": [
      "Edit(/.env*)",
      "Edit(/secrets/**)",
      "Edit(/*.key)",
      "Edit(/*.pem)",
      "Edit(/credentials.*)"
    ]
  }
}
```

## WebFetch Patterns

### Domain-Based Rules

```json
{
  "permissions": {
    "allow": [
      "WebFetch(domain:github.com)",
      "WebFetch(domain:docs.example.com)",
      "WebFetch(domain:api.internal.com)"
    ],
    "deny": [
      "WebFetch(domain:malicious-site.com)"
    ]
  }
}
```

### Full URL Patterns

```json
{
  "permissions": {
    "allow": [
      "WebFetch"
    ],
    "ask": [
      "WebFetch(domain:*)"
    ]
  }
}
```

## MCP Tool Patterns

### Server-Level Rules

```json
{
  "permissions": {
    "allow": [
      "mcp__github",
      "mcp__memory",
      "mcp__filesystem"
    ]
  }
}
```

### Tool-Level Rules

```json
{
  "permissions": {
    "allow": [
      "mcp__github__search_repositories",
      "mcp__github__get_file_contents",
      "mcp__memory__store",
      "mcp__memory__retrieve"
    ],
    "deny": [
      "mcp__github__delete_repository"
    ]
  }
}
```

### Wildcard Patterns

```json
{
  "permissions": {
    "allow": [
      "mcp__puppeteer__*"
    ]
  }
}
```

## Task (Subagent) Patterns

Control which subagent types Claude can spawn:

```json
{
  "permissions": {
    "allow": [
      "Task(Verify)"
    ],
    "deny": [
      "Task(Explore)",
      "Task(Plan)"
    ]
  }
}
```

### Task Types

| Task Type | Purpose |
|-----------|---------|
| `Task(Explore)` | Exploring codebase |
| `Task(Plan)` | Planning changes |
| `Task(Verify)` | Verifying implementations |

## Combined Patterns

### TypeScript Project

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Edit(/src/**/*.ts)",
      "Edit(/src/**/*.tsx)",
      "Edit(/tests/**)",
      "Bash(npm run *)",
      "Bash(npm test:*)",
      "Bash(npx *)",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(git log:*)"
    ],
    "ask": [
      "Edit(/package.json)",
      "Edit(/tsconfig.json)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(npm install:*)"
    ],
    "deny": [
      "Edit(/.env*)",
      "Bash(rm -rf *)"
    ]
  }
}
```

### Python Project

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Edit(/src/**/*.py)",
      "Edit(/tests/**/*.py)",
      "Bash(python *)",
      "Bash(pytest:*)",
      "Bash(pip list)",
      "Bash(git:*)"
    ],
    "ask": [
      "Edit(/requirements.txt)",
      "Edit(/pyproject.toml)",
      "Bash(pip install:*)"
    ],
    "deny": [
      "Edit(/.env*)",
      "Bash(rm -rf *)"
    ]
  }
}
```

### Rust Project

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Edit(/src/**/*.rs)",
      "Edit(/tests/**)",
      "Bash(cargo build:*)",
      "Bash(cargo test:*)",
      "Bash(cargo check:*)",
      "Bash(cargo clippy:*)",
      "Bash(cargo fmt:*)"
    ],
    "ask": [
      "Edit(/Cargo.toml)",
      "Bash(cargo publish:*)"
    ]
  }
}
```

## Pattern Debugging

### Testing Patterns

Use `/permissions` to see active rules and test matches:

```bash
/permissions
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Pattern too broad | Add more specific deny rules |
| Pattern not matching | Check exact command syntax |
| Unexpected prompts | Add to allow list |
| Can't execute | Check deny rules |

### Debug Mode

```bash
claude --debug
```

Shows which permission rules are being evaluated.

## Pattern Best Practices

1. **Start restrictive** - Add permissions as needed
2. **Use deny for critical** - Always explicitly deny dangerous operations
3. **Be specific with Bash** - Broad patterns can be bypassed
4. **Test patterns** - Verify with `/permissions`
5. **Document patterns** - Comment your settings.json
