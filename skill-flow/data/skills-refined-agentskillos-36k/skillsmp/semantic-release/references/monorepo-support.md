**Skill**: [semantic-release](../SKILL.md)

## Monorepo Support

> **macOS Note**: Use global `semantic-release` to avoid Gatekeeper blocking `.node` files. See [Troubleshooting](./troubleshooting.md#macos-gatekeeper-blocks-node-files).

---

## Tool Selection by Scale

| Scale                             | Recommendation           | Rationale                                 |
| --------------------------------- | ------------------------ | ----------------------------------------- |
| **< 10 packages**                 | mise + custom git script | Minimal overhead                          |
| **10-50 packages (Python-heavy)** | **Pants + mise**         | Native affected detection, auto-inference |
| **50+ packages**                  | Bazel                    | Proven scale, remote execution            |
| **JS-only monorepo**              | Turborepo or Nx          | Excellent JS tooling                      |

---

## Polyglot Monorepo with Pants + mise (Recommended)

For Python-heavy polyglot monorepos (10-50 packages), combine **mise** for runtime management with **Pants** for build orchestration and native affected detection.

### Division of Responsibility

| Tool      | Responsibility                                                         |
| --------- | ---------------------------------------------------------------------- |
| **mise**  | Runtime versions (Python, Node, Rust) + environment variables          |
| **Pants** | Build orchestration + native affected detection + dependency inference |

### Affected-Only Release Pattern

**Key insight**: Pants `--changed-since` enables releasing ONLY packages that changed, not the entire workspace.

```bash
# List affected packages
pants --changed-since=origin/main list

# Test only affected
pants --changed-since=origin/main test

# Build only affected
pants --changed-since=origin/main package
```

### mise.toml Release Tasks

```toml
# Affected-only release workflow
[tasks."release:affected"]
description = "Release only affected packages"
run = '''
#!/usr/bin/env bash
set -euo pipefail

# Get affected packages with publishable artifacts
AFFECTED=$(pants --changed-since=origin/main list --filter-target-type=python_distribution,pex_binary 2>/dev/null || true)

if [ -z "$AFFECTED" ]; then
  echo "No affected packages to release"
  exit 0
fi

echo "Affected packages:"
echo "$AFFECTED"

# For each affected package, run semantic-release in its directory
for pkg in $AFFECTED; do
  pkg_dir=$(dirname "$pkg" | sed 's|//||')
  echo "Releasing: $pkg_dir"
  (cd "$pkg_dir" && semantic-release --no-ci)
done
'''

[tasks."release:dry"]
description = "Dry-run affected release"
run = '''
pants --changed-since=origin/main list --filter-target-type=python_distribution
'''
```

### pants.toml Configuration

```toml
[GLOBAL]
pants_version = "<version>"  # See pantsbuild.org for latest
backend_packages = [
    "pants.backend.python",
    "pants.backend.python.lint.ruff",
    "pants.backend.experimental.rust",
    "pants.backend.experimental.javascript",
]

[python]
interpreter_constraints = [">=3.11"]

[source]
root_patterns = ["packages/*"]

[python-bootstrap]
# Use mise-managed Python (mise sets PATH)
search_path = ["<PATH>"]
```

### Architecture

```
monorepo/
├── mise.toml                    # Runtime versions + env vars (SSoT)
├── pants.toml                   # Pants configuration
├── BUILD                        # Root BUILD file (minimal)
├── packages/
│   ├── core-python/
│   │   ├── mise.toml           # Package-specific env (optional)
│   │   ├── BUILD               # Auto-generated: python_sources()
│   │   ├── .releaserc.yml      # Package-level release config
│   │   └── pyproject.toml
│   ├── core-rust/
│   │   ├── BUILD               # cargo-pants plugin
│   │   └── Cargo.toml          # Version SSoT for Rust
│   └── core-bun/
│       ├── BUILD               # pants-js plugin
│       └── package.json
```

> **Deep dive**: See [mise-tasks skill: polyglot-affected](../../mise-tasks/references/polyglot-affected.md) for complete Pants + mise integration guide.

> **Bootstrap**: See [mise-tasks skill: bootstrap-monorepo](../../mise-tasks/references/bootstrap-monorepo.md) for autonomous polyglot monorepo setup.

---

## JavaScript Workspaces (pnpm/npm)

### pnpm Workspaces

Install pnpm plugin:

```bash
npm install --save-dev @anolilab/semantic-release-pnpm
```

Run release across workspaces:

```bash
# macOS (global install recommended)
pnpm -r --workspace-concurrency=1 exec -- semantic-release --no-ci

# Linux/CI (npx works without Gatekeeper issues)
pnpm -r --workspace-concurrency=1 exec -- npx --no-install semantic-release
```

### npm Workspaces

Use multi-semantic-release:

```bash
npm install --save-dev @anolilab/multi-semantic-release

# macOS (global install recommended)
multi-semantic-release

# Linux/CI
npx multi-semantic-release
```

---

## Alternative Tools Comparison

| Tool           | Affected Detection         | Language Support              | Setup Time |
| -------------- | -------------------------- | ----------------------------- | ---------- |
| **Pants**      | Native (`--changed-since`) | Python, Rust, JS (native)     | 2-4 hours  |
| **Nx Release** | Native (graph-aware)       | JS native, others via plugin  | 2-4 hours  |
| **Turborepo**  | Native (`--filter`)        | JS only (wrappers for others) | 1-2 hours  |
| **Bazel**      | Via bazel-diff             | Excellent polyglot            | 1-2 weeks  |
| **Changesets** | Manual                     | JS ecosystem                  | 1 hour     |
| **Lerna-lite** | None (all or nothing)      | JS ecosystem                  | 30 min     |

### When NOT to Use Pants

- **JS-only monorepo**: Use Turborepo or Nx (better DX for JS)
- **Very small (< 5 packages)**: Use mise + git scripts (less overhead)
- **Enterprise with existing Bazel**: Extend Bazel instead

---

## Cross-Language Version Synchronization

For polyglot monorepos where packages share versions:

### Git Tags as SSoT

```bash
# Single source of truth: git tag
git tag -a v<version> -m "Release v<version>"

# All manifests read from tag, not vice versa
```

### Manifest Update Patterns

| Language | Manifest         | Update Command         |
| -------- | ---------------- | ---------------------- |
| Python   | `pyproject.toml` | `sed` or `tomlq`       |
| Rust     | `Cargo.toml`     | `cargo set-version`    |
| Node     | `package.json`   | `npm version` (no git) |
| Go       | `go.mod`         | Module path versioning |

### Example: Synchronized Release

```toml
# mise.toml - release all packages with same version
[tasks."release:sync"]
description = "Release all packages with synchronized version"
run = '''
#!/usr/bin/env bash
set -euo pipefail

# Get version from semantic-release dry-run
VERSION=$(semantic-release --dry-run 2>&1 | grep -oP 'next release version is \K[0-9.]+' || echo "")

if [ -z "$VERSION" ]; then
  echo "No new version to release"
  exit 0
fi

echo "Releasing v$VERSION across all packages"

# Update Python packages
for pkg in packages/*/pyproject.toml; do
  sed -i '' "s/^version = .*/version = \"$VERSION\"/" "$pkg"
done

# Update Rust packages
for pkg in packages/*/Cargo.toml; do
  (cd "$(dirname "$pkg")" && cargo set-version "$VERSION")
done

# Commit and release
git add -A
git commit -m "chore: bump version to $VERSION"
semantic-release --no-ci
'''
```

> **Deep dive**: See [Version Alignment](./version-alignment.md) for complete SSoT patterns.
