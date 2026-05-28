---
name: bun-runtime
description: Master Bun runtime workflows for full-stack development. Monorepos, bunx, lockfiles, performance optimization, and integration patterns.
triggers:
  - bun runtime
  - bunx
  - monorepo
  - bun workflows
  - bun performance
  - fast startup
---

# Bun Runtime Workflows

Leverage Bun's integrated toolkit for faster development. From one-off commands with bunx to optimizing monorepos, master the workflows that keep full-stack teams moving.

## Why Bun?

Bun is a **complete toolkit** in a single binary:
- **Runtime** — JavaScript/TypeScript execution (4x faster Node startup)
- **Package Manager** — Replaces npm/yarn (faster installs)
- **Bundler** — Built-in code bundling
- **Test Runner** — Native test framework (no external runners)

All in one. No configuration. No separate tools.

---

## 1. bunx: No Global Installs

Replace globally installed CLI tools with `bunx`. Each command runs the latest version without cluttering your environment.

### Pattern: Use bunx Instead of Global npm

```bash
# ❌ Old way (npm)
npm install -g eslint
npx eslint .

# ✅ New way (Bun)
bunx eslint .
bunx eslint --fix .

# Always uses latest version, no global pollution
```

### Common bunx Commands

```bash
# Create projects
bunx create-vite@latest my-app --template react-ts
bunx create-next-app@latest my-blog

# Run tools
bunx eslint . --fix
bunx prettier . --write
bunx tsc --noEmit

# Utilities
bunx tsx script.ts          # Run TypeScript directly
bunx esbuild app.ts         # Bundle app
bunx http-server .          # Quick HTTP server
```

### Why bunx?

- **No global cluttering** — Each tool installs to temp directory
- **Version consistency** — Everyone uses the latest (or pinned) version
- **Faster** — No global npm cache to manage
- **Reproducible** — Same versions across developers and CI

---

## 2. Bun Workspaces: Monorepo Management

Define workspaces in root `package.json` for seamless monorepo management.

### Setup

```json
{
  "name": "my-workspace",
  "private": true,
  "workspaces": [
    "packages/*",
    "apps/*",
    "plugins/*"
  ]
}
```

### Directory Structure

```
my-workspace/
├── package.json              # Root (defines workspaces)
├── packages/
│   ├── core/                # Shared library
│   │   ├── package.json
│   │   └── src/
│   └── utils/
│       ├── package.json
│       └── src/
├── apps/
│   ├── web/                 # Next.js app
│   │   ├── package.json
│   │   └── src/
│   └── mobile/              # React Native
│       ├── package.json
│       └── src/
└── plugins/                 # Claude Code plugins
    ├── my-plugin/
    │   ├── package.json
    │   └── src/
```

### Cross-Workspace Dependencies

Use `workspace:*` protocol for local dependencies:

```json
{
  "name": "@myapp/web",
  "dependencies": {
    "@myapp/core": "workspace:*",
    "@myapp/utils": "workspace:*"
  }
}
```

**Benefits:**
- Automatic linking (no npm install needed)
- Changes to packages/* update immediately
- Single `bun install` in root
- No node_modules duplication

### Workspace Commands

```bash
# Install all dependencies
bun install

# Run script in specific workspace
bun --filter web run dev

# Run test in all workspaces with changes
bun test --recursive

# List workspaces
bun workspaces list
```

---

## 3. Lockfile Management: Reproducibility

Bun creates a binary lockfile (`bun.lockb`) for fast, reliable builds.

### Key Practices

```bash
# Generate lockfile
bun install

# Commit bun.lockb to git
git add bun.lockb
git commit -m "chore: update dependencies"

# CI: Install with frozen lockfile
bun install --frozen-lockfile

# Production: Skip dev dependencies
bun install --production
```

### Why bun.lockb?

- **Fast to parse** — Binary format (faster than JSON)
- **Reliable** — Exact versions always reproduced
- **Smaller** — More compact than package-lock.json
- **Deterministic** — Same install on every machine

### Dependency Pinning

```json
{
  "dependencies": {
    "react": "^18.2.0",      // Patch updates ok
    "typescript": "5.7.2"    // Exact version (no updates)
  }
}
```

---

## 4. Bun Built-In Tools: Bundling & Testing

### Bundling with Bun

```bash
# Bundle with default settings
bun build ./src/index.ts --outdir=./dist

# Minify and split chunks
bun build ./src/index.ts --minify --splitting

# Watch mode
bun build ./src/index.ts --watch
```

### Testing with Bun's Test Runner

```bash
# Run all tests
bun test

# Run specific test file
bun test src/math.test.ts

# Watch mode (rerun on changes)
bun test --watch

# Coverage
bun test --coverage
```

**No separate test runner needed.** It's built in.

---

## 5. Performance Optimization

### Startup Time

Bun has **4x faster startup** than Node:

```bash
# Node.js
time node script.js
# real    0m0.345s

# Bun
time bun script.ts
# real    0m0.085s
```

### Why?

- Written in Rust (not C++)
- JavaScriptCore engine (Apple's, highly optimized)
- Single binary (no bootstrapping overhead)
- Native TypeScript support (no transpile step)

### Optimization Tips

1. **Use bunfig.toml for config:**
```toml
[run]
logLevel = "error"
```

2. **Minimize imports** — Each import has a cost
3. **Use native modules** — Bun's fs, path, etc.
4. **Avoid transpilation** — Bun handles TypeScript natively

---

## 6. Practical Workflows

### Workflow 1: Monorepo Development

```bash
# Install all dependencies
bun install

# Run dev server for web app
bun --filter web run dev

# Run tests for changed packages
bun test --recursive

# Build everything
bun --filter "*" run build
```

### Workflow 2: Creating CLI Tools

```bash
# Create new CLI package
mkdir packages/my-cli
cd packages/my-cli

# Create package.json with bin entry
cat > package.json << EOF
{
  "name": "@myapp/my-cli",
  "bin": {
    "my-cli": "./src/cli.ts"
  },
  "scripts": {
    "test": "bun test"
  }
}
EOF

# Back in root
bun install

# Test CLI from anywhere
bun my-cli --help
```

### Workflow 3: Scripts and Utilities

```bash
# scripts/deploy.ts (executable)
#!/usr/bin/env bun
import { $ } from "bun";

const env = process.env.NODE_ENV || "staging";
console.log(`Deploying to ${env}...`);

await $`git push origin main`;
await $`bun --filter web run build`;
await $`vercel deploy --prod`;

console.log("✅ Deployed!");
```

```bash
# Run it
chmod +x scripts/deploy.ts
./scripts/deploy.ts
```

---

## 7. Integration Patterns

### With Next.js

```bash
# bunx create-next-app + Bun
bunx create-next-app@latest my-app --bun
cd my-app

# Next.js + Bun
bun run dev
bun run build
bun start
```

### With Vite

```bash
# Create Vite project
bunx create-vite@latest my-app --template react

cd my-app

# Use Bun
bun install
bun run dev
bun run build
```

### With TypeScript

```bash
# No configuration needed
bun run my-script.ts

# Watch mode
bun --watch src/index.ts

# Type checking (in CI)
bunx tsc --noEmit
```

---

## Common Pitfalls

### ❌ Don't

- **Use `npm` inside a Bun project** — Use `bun` instead
- **Ignore bun.lockb** — It's critical for reproducibility
- **Forget workspace protocol** — Use `workspace:*` for local deps
- **Mix package managers** — Stick to Bun (no npm, yarn, pnpm)
- **Assume Node.js compatibility** — Most packages work, but test edge cases

### ✅ Do

- **Use `bun install`** — Faster, lockb is optimized
- **Commit bun.lockb** — It's tiny, git-friendly
- **Use `bunx`** — For one-off commands
- **Leverage workspaces** — For monorepos
- **Test with `bun test`** — Native, no config needed

---

## Checklist: Setting Up a Bun Project

- [ ] Use `bun create` or `bunx` to scaffold
- [ ] Run `bun install` (creates bun.lockb)
- [ ] Add `.bunfig.toml` if custom config needed
- [ ] Add `bun.lockb` to git
- [ ] Use `bun run` for scripts
- [ ] Use `bun test` for testing
- [ ] Use `bunx` for one-off tools
- [ ] Document Bun setup in README
- [ ] Test on target Node version (if needed)

---

## Performance Comparison

| Task | Node.js | Bun |
|------|---------|-----|
| Startup | 0.3s | 0.08s |
| Install (100 packages) | 45s | 8s |
| Test run | 2.3s | 1.1s |
| Build (esbuild equiv.) | 1.5s | 0.4s |

**Bun is 4-10x faster for typical full-stack workflows.**

---

## Resources

### Official Docs
- [Bun Documentation](https://bun.sh/docs)
- [Package Manager](https://bun.sh/docs/pm)
- [Bundler](https://bun.sh/docs/bundler)
- [Test Runner](https://bun.sh/docs/test/writing)

### Useful Commands
```bash
bun --help                 # All commands
bun install --help         # Install options
bun run --help             # Run options
bun test --help            # Test options
```

---

## Related Skills

- **Bun CLI Development** — Building CLIs with Bun
- **Monorepo Management** — Advanced workspace patterns
- **Performance Optimization** — Profiling and tuning
- **Git Workflows** — Committing lockfiles reliably

---

## FAQ

**Q: Is Bun production-ready?**
A: Yes, for most use cases. Check Bun's compatibility for your specific packages.

**Q: Should I switch from Node.js?**
A: For new projects, yes. For existing, evaluate package compatibility first.

**Q: Will my npm packages work?**
A: Most do. Bun is npm-compatible. Test critical dependencies first.

**Q: How do I handle CI/CD with Bun?**
A: Install Bun in CI, use `bun install --frozen-lockfile`, then `bun run`.

**Q: Can I use Bun with monorepos?**
A: Absolutely. Workspaces make monorepos effortless.

---

**Last Updated:** 2025-12-05
**Status:** Reference Implementation
**Related:** BUN_CLI_STANDARD.md, Bun Documentation
