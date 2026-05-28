---
name: opensrc
description: Use this skill when you need to fetch source code for npm, PyPI, or crates.io packages and GitHub/GitLab repositories to gain deeper implementation context beyond just types and documentation.
---

# Skill body

## When to Use

- To understand how a library/package works internally (not just its interface).
- When debugging issues where types alone are insufficient.
- To explore implementation patterns in dependencies.
- When an agent needs to reference the actual source code of a package.

## Quick Start

```bash
# Install globally or use npx
npm install -g opensrc

# Fetch npm package (auto-detects installed version from lockfile)
npx opensrc zod

# Fetch from other registries
npx opensrc pypi:requests       # Python/PyPI
npx opensrc crates:serde        # Rust/crates.io

# Fetch GitHub repo directly
npx opensrc vercel/ai           # owner/repo shorthand
npx opensrc github:owner/repo   # explicit prefix
npx opensrc https://github.com/colinhacks/zod  # full URL

# Fetch specific version/ref
npx opensrc zod@3.22.0
npx opensrc owner/repo@v1.0.0
```

## Commands

| Command | Description |
|---------|-------------|
| `opensrc <packages...>` | Fetch source for packages/repos |
| `opensrc list` | List all fetched sources |
| `opensrc remove <name>` | Remove specific source |
| `opensrc clean` | Remove all sources |

## Output Structure

After fetching, sources are stored in the `opensrc/` directory:

```
opensrc/
├── settings.json           # User preferences
├── sources.json            # Index of fetched packages/repos
└── repos/
    └── github.com/
        └── owner/
            └── repo/       # Cloned source code
```

## File Modifications

On first run, opensrc prompts to modify:
- `.gitignore` - adds `opensrc/` to ignore list.
- `tsconfig.json` - excludes `opensrc/` from compilation.
- `AGENTS.md` - adds a section pointing agents to source code.

Use `--modify` or `--modify=false` to skip the prompt.

## Key Behaviors

1. **Version Detection** - For npm, auto-detects installed version from `node_modules`, `package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock`.
2. **Repository Resolution** - Resolves package to its git repo via registry API and clones at the matching tag.
3. **Monorepo Support** - Handles packages in monorepos via the `repository.directory` field.
4. **Shallow Clone** - Uses shallow cloning to minimize data transfer.