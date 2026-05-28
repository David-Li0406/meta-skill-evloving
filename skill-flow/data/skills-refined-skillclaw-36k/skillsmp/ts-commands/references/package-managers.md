# Package Manager Reference

Detailed information about package managers, their versions, and command syntax.

## npm

### Detection
- Lock file: `package-lock.json`
- packageManager field: `"packageManager": "npm@10.0.0"`

### Version Differences

**npm 7+:**
- Workspace support introduced
- Automatic peer dependency installation
- Lock file format v2

**npm 6 and earlier:**
- No workspace support
- Manual peer dependency management

### Commands

**Script execution:**
```bash
npm run <script>                    # Run script
npm run <script> -- --arg           # Pass arguments to script
```

**Workspace commands (npm 7+):**
```bash
npm run <script> -w <workspace>     # Run in specific workspace
npm run <script> --workspace=<name> # Alternate syntax
npm run <script> --workspaces       # Run in all workspaces
npm run <script> -ws                # Short form for all workspaces
```

**Dependency management:**
```bash
npm install                         # Install all dependencies
npm install <package>               # Add dependency
npm install <package> -D            # Add dev dependency
npm install -w <workspace>          # Install in workspace
```

**Useful flags:**
- `--if-present` - Don't error if script doesn't exist
- `--ignore-scripts` - Skip pre/post scripts
- `--workspace` / `-w` - Target specific workspace
- `--workspaces` / `-ws` - Target all workspaces

---

## Yarn

Yarn has two major versions with different architectures.

### Yarn Classic (v1.x)

**Detection:**
- Lock file: `yarn.lock` (v1 format)
- packageManager field: `"packageManager": "yarn@1.22.19"`
- `.yarnrc` file (not `.yarnrc.yml`)

**Commands:**
```bash
yarn <script>                       # Run script (no 'run' needed)
yarn run <script>                   # Also works
yarn workspace <name> <script>      # Run in workspace
yarn workspaces run <script>        # Run in all workspaces
yarn workspaces info                # Show workspace structure
```

**Workspace configuration:**
```json
{
  "private": true,
  "workspaces": ["packages/*"]
}
```

**Features:**
- Fast, deterministic installs
- Flat node_modules structure
- Workspace support (v1.0+)

### Yarn Berry (v2+, v3+, v4+)

**Detection:**
- Lock file: `yarn.lock` (v2+ format)
- packageManager field: `"packageManager": "yarn@3.6.0"` or `"packageManager": "yarn@4.0.0"`
- `.yarnrc.yml` file
- `.yarn/` directory with releases

**Commands:**
```bash
yarn <script>                       # Run script
yarn workspace <name> <script>      # Run in workspace
yarn workspaces foreach <script>    # Run in all workspaces
yarn workspaces foreach -p <script> # Parallel execution
yarn workspaces foreach -pt <script> # Parallel with topological order
```

**Advanced workspace commands:**
```bash
yarn workspaces foreach -A <script>      # Include workspaces without script
yarn workspaces foreach --since <script> # Only changed workspaces
yarn workspaces foreach -R <script>      # Reverse topological order
```

**Features:**
- Plug'n'Play (PnP) mode - no node_modules by default
- Zero-installs with committed cache
- Workspace protocol: `"workspace:*"`
- Constraints system
- Plugin architecture

**Version-specific:**
- Yarn v2: Initial berry release
- Yarn v3: Improved stability, better Windows support
- Yarn v4: Performance improvements, ESM support

---

## pnpm

### Detection
- Lock file: `pnpm-lock.yaml`
- Workspace file: `pnpm-workspace.yaml`
- packageManager field: `"packageManager": "pnpm@8.0.0"`

### Version Differences

**pnpm 7+:**
- Node.js 14.19+ required
- Improved workspace protocol
- Better monorepo support

**pnpm 8+:**
- Node.js 16.14+ required
- Catalogs feature for dependency version management
- Improved peer dependency resolution

### Commands

**Script execution:**
```bash
pnpm <script>                       # Run script (no 'run' needed)
pnpm run <script>                   # Also works
pnpm <script> -- --arg              # Pass arguments
```

**Workspace commands:**
```bash
pnpm --filter <name> <script>       # Run in specific workspace
pnpm --filter <pattern> <script>    # Run in matching workspaces
pnpm -r <script>                    # Recursive (all workspaces)
pnpm -r --parallel <script>         # Parallel execution
pnpm --filter "...<name>" <script>  # Dependents of workspace
pnpm --filter "<name>..." <script>  # Dependencies of workspace
```

**Filter patterns:**
```bash
pnpm --filter "./packages/*"        # Glob pattern
pnpm --filter "!<name>"             # Exclude workspace
pnpm --filter "[origin/main]"       # Changed since git ref
pnpm --filter "{<name>}"            # Include dependencies/dependents
```

**Useful flags:**
- `-r` / `--recursive` - Run in all workspace packages
- `--parallel` - Run in parallel (with -r)
- `--stream` - Stream output from child processes
- `--no-bail` - Continue on error
- `-w` - Run in workspace root

**Workspace configuration (pnpm-workspace.yaml):**
```yaml
packages:
  - 'packages/*'
  - 'apps/*'
  - '!**/test/**'  # Exclude pattern
```

**Workspace protocol:**
- `"workspace:*"` - Any version in workspace
- `"workspace:^"` - Semver caret range
- `"workspace:~"` - Semver tilde range
- `"workspace:^1.0.0"` - Specific range

**Features:**
- Content-addressable storage (saves disk space)
- Strict by default
- Fast, efficient installs
- Excellent monorepo support

**Catalogs (pnpm 8+):**
```json
{
  "pnpm": {
    "catalogs": {
      "default": {
        "react": "^18.2.0",
        "vite": "^5.0.0"
      }
    }
  }
}
```

Use in package.json:
```json
{
  "dependencies": {
    "react": "catalog:",
    "vite": "catalog:"
  }
}
```

---

## Bun

### Detection
- Lock file: `bun.lockb` (binary format)
- packageManager field: `"packageManager": "bun@1.0.0"`
- `bunfig.toml` configuration file

### Commands

**Script execution:**
```bash
bun run <script>                    # Run script
bun <script>                        # Also works for most scripts
bun run <script> -- --arg           # Pass arguments
```

**Workspace commands:**
```bash
bun --filter <name> run <script>    # Run in workspace
bun --filter "*" run <script>       # Run in all workspaces
```

**Dependency management:**
```bash
bun install                         # Install dependencies
bun add <package>                   # Add dependency
bun add -d <package>                # Add dev dependency
bun remove <package>                # Remove dependency
```

**Features:**
- Extremely fast package installation
- Built-in bundler and test runner
- Drop-in replacement for Node.js
- Compatible with npm registry
- Workspace support

**Workspace configuration:**
```json
{
  "workspaces": ["packages/*"]
}
```

**Note:** Bun is rapidly evolving; features may change between versions.

---

## Command Comparison Table

| Feature | npm | Yarn v1 | Yarn Berry | pnpm | Bun |
|---------|-----|---------|------------|------|-----|
| Run script | `npm run` | `yarn` | `yarn` | `pnpm` | `bun run` |
| Workspace script | `-w <name>` | `workspace` | `workspace` | `--filter` | `--filter` |
| All workspaces | `--workspaces` | `workspaces run` | `workspaces foreach` | `-r` | `--filter "*"` |
| Parallel execution | ❌ | ❌ | `-p` flag | `--parallel` | Native |
| Installation speed | Moderate | Fast | Fast | Very fast | Extremely fast |
| Disk usage | High | High | Low (PnP) | Very low | Moderate |

---

## Determining Version

### From packageManager field
```json
{
  "packageManager": "pnpm@8.6.0"
}
```
Parse the version directly.

### From lock file
- npm: Check `lockfileVersion` in package-lock.json (2 = npm 7+)
- Yarn: v1 lock files start with `# THIS IS AN AUTOGENERATED FILE`
- Yarn Berry: Lock file has different structure, check for `.yarnrc.yml`
- pnpm: Check `lockfileVersion` in pnpm-lock.yaml (6.0 = pnpm 8+)

### From CLI (if needed)
```bash
npm --version
yarn --version
pnpm --version
bun --version
```

---

## Best Practices

### Consistency
- Use one package manager per project
- Commit lock files
- Set packageManager field in package.json
- Add other lock files to .gitignore

### Performance
- pnpm: Best for monorepos, disk usage
- Yarn Berry: Good for large projects with PnP
- Bun: Fastest installation
- npm: Most compatible, widely used

### Monorepo Recommendations
1. **pnpm** - Best monorepo support, efficient, workspace protocol
2. **Yarn Berry** - Good with plugins, constraints
3. **npm** - Basic workspace support (npm 7+)
4. **Bun** - Fast but still maturing
