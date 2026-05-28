---
name: fetch-source-code
description: Use this skill to fetch source code for npm, PyPI, or crates.io packages and GitHub/GitLab repositories, providing AI agents with deeper implementation context for understanding libraries and debugging.
---

# Fetch Source Code

CLI tool to fetch source code for packages and repositories, giving AI coding agents deeper implementation context.

## When to Use

- Need to understand how a library/package works internally (not just its interface)
- Debugging issues where types alone are insufficient
- Exploring implementation patterns in dependencies
- Agent needs to reference actual source code of a package

## Quick Start

```bash
# Install globally or use npx
npm install -g fetch-source-code

# Fetch npm package (auto-detects installed version from lockfile)
npx fetch-source-code zod

# Fetch from other registries
npx fetch-source-code pypi:requests       # Python/PyPI
npx fetch-source-code crates:serde        # Rust/crates.io

# Fetch GitHub repo directly
npx fetch-source-code vercel/ai           # owner/repo shorthand
npx fetch-source-code github:owner/repo   # explicit prefix
npx fetch-source-code https://github.com/colinhacks/zod  # full URL

# Fetch specific version/ref
npx fetch-source-code zod@3.22.0
npx fetch-source-code owner/repo@v1.0.0
```

## Commands

| Command | Description |
|---------|-------------|
| `fetch-source-code <packages...>` | Fetch source for packages/repos |
| `fetch-source-code list` | List all fetched sources |
| `fetch-source-code remove <name>` | Remove specific source |
| `fetch-source-code clean` | Remove all sources |

## Output Structure

After fetching, sources are stored in the `fetch-source-code/` directory:

```
fetch-source-code/
├── settings.json           # User preferences
├── sources.json            # Index of fetched packages/repos
└── repos/
    └── github.com/
        └── owner/
            └── repo/       # Cloned source code
```

## File Modifications

On first run, the tool prompts to modify:
- `.gitignore` - adds `fetch-source-code/` to ignore list
- `tsconfig.json` - excludes `fetch-source-code/` from compilation
- `AGENTS.md` - adds section pointing agents to source code

Use `--modify` or `--modify=false` to skip the prompt.

## Key Behaviors

1. **Version Detection** - For npm, auto-detects installed version from `node_modules`, `package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock`
2. **Repository Resolution** - Resolves package to its git repo via registry API, clones at matching tag
3. **Monorepo Support** - Handles packages in monorepos via `repository.directory` field
4. **Shallow Clone** - Uses `--depth 1` for efficient cloning, removes `.git` after clone
5. **Tag Fallback** - Tries `v{version}`, `{version}`, then default branch if tag not found

## Common Workflows

### Fetching a Package

```bash
# Agent needs to understand zod's implementation
npx fetch-source-code zod
# → Detects version from lockfile
# → Finds repo URL from npm registry
# → Clones at matching git tag
# → Source available at fetch-source-code/repos/github.com/colinhacks/zod/
```

### Updating Sources

```bash
# Re-run same command to update to currently installed version
npx fetch-source-code zod
# → Checks if version changed
# → Re-clones if needed
```

### Multiple Sources

```bash
# Fetch multiple at once
npx fetch-source-code react react-dom next
npx fetch-source-code zod pypi:pydantic vercel/ai
```

## References

For detailed information:
- [CLI Usage & Options](references/cli-usage.md) - Full command reference
- [Architecture](references/architecture.md) - Code structure and extension
- [Registry Support](references/registry-support.md) - npm, PyPI, crates.io details