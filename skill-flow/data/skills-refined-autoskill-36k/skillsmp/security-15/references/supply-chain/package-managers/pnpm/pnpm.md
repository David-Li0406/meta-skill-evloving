# pnpm Package Manager

**Ecosystem**: JavaScript/Node.js
**Package Registry**: https://registry.npmjs.org
**Documentation**: https://pnpm.io/

---

## TIER 1: Manifest Detection

### Manifest Files

| File | Required | Description |
|------|----------|-------------|
| `package.json` | Yes | Primary manifest (shared with npm) |
| `pnpm-workspace.yaml` | No | Workspace configuration |
| `.npmrc` | No | Configuration file |

### Package.json Detection

**Pattern**: `package\.json$`
**Confidence**: 95% (HIGH)

**pnpm-Specific Indicators**:
- Presence of `pnpm-lock.yaml`
- `packageManager` field: `"pnpm@..."`
- `pnpm-workspace.yaml` file

### Dependency Types

| Field | Included in SBOM | Notes |
|-------|------------------|-------|
| `dependencies` | Yes (always) | Production runtime |
| `devDependencies` | Configurable | Development only |
| `peerDependencies` | Yes | Expected by consumer |
| `optionalDependencies` | Configurable | May fail without error |
| `pnpm.overrides` | Yes | Version overrides |

---

## TIER 2: Lock File Detection

### Lock File

| File | Format | Version |
|------|--------|---------|
| `pnpm-lock.yaml` | YAML | 5.x, 6.x, 9.x |

**Pattern**: `pnpm-lock\.yaml$`
**Confidence**: 98% (HIGH)

### Lock File Structure

```yaml
lockfileVersion: '9.0'

settings:
  autoInstallPeers: true
  excludeLinksFromLockfile: false

importers:
  .:
    dependencies:
      express:
        specifier: ^4.18.0
        version: 4.18.2

packages:
  express@4.18.2:
    resolution: {integrity: sha512-5/PsL6iGPdfQ/lKM1UuielYgv3BUoJfz1aUwU9vHZ+J7gyvwdQXFEBIEIaxeGf0GIcreATNyBExtalisDbuMqQ==}
    engines: {node: '>= 0.10.0'}
    dependencies:
      accepts: 1.3.8
      array-flatten: 1.1.1
```

### Key Lock File Fields

| Field | SBOM Use |
|-------|----------|
| `resolution.integrity` | SHA-512 hash |
| `version` | Exact package version |
| `dependencies` | Transitive dependencies |
| `engines` | Node.js version constraints |
| `peerDependencies` | Peer requirement info |

---

## TIER 3: Configuration Extraction

### Registry Configuration

**File**: `.npmrc`

**Pattern**: `registry\s*=\s*['\"]?([^\s'\"]+)`
**Pattern**: `@scope:registry\s*=\s*['\"]?([^\s'\"]+)`

### Common Configuration

```ini
# .npmrc
registry=https://npm.mycompany.com/

# Scoped packages
@mycompany:registry=https://npm.mycompany.com/

# Authentication
//npm.mycompany.com/:_authToken=${NPM_TOKEN}

# pnpm-specific settings
shamefully-hoist=true
strict-peer-dependencies=false
auto-install-peers=true
```

### Workspace Configuration

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
  - 'apps/*'
  - '!**/test/**'
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `NPM_TOKEN` | Registry authentication |
| `PNPM_HOME` | pnpm installation directory |
| `npm_config_registry` | Default registry |

---

## SBOM Generation

### Using cdxgen

```bash
# Install cdxgen
npm install -g @cyclonedx/cdxgen

# Generate SBOM
cdxgen -o sbom.json

# From pnpm-lock.yaml only
cdxgen --project-type pnpm -o sbom.json

# Exclude dev dependencies
cdxgen --no-dev -o sbom.json
```

### Using CycloneDX pnpm

```bash
# Install plugin
pnpm add -g @cyclonedx/pnpm

# Generate SBOM
cyclonedx-pnpm --output-file sbom.json

# Exclude dev dependencies
cyclonedx-pnpm --prod --output-file sbom.json
```

### Using cdxgen

```bash
# Generate from directory
cdxgen -o sbom.json

# Specify type
cdxgen -t js -o sbom.json
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--prod` | Exclude devDependencies | Include all |
| `--output-format` | json or xml | json |
| `--spec-version` | CycloneDX version | Latest |

---

## Cache Locations

| Platform | Path |
|----------|------|
| Linux | `~/.local/share/pnpm/store/` |
| macOS | `~/Library/pnpm/store/` |
| Windows | `%LocalAppData%/pnpm/store/` |

### Content-Addressable Store

pnpm uses a content-addressable store:
- One copy of each package version globally
- Hard links to project `node_modules`
- Significant disk space savings

```bash
# Find store location
pnpm store path

# Check store status
pnpm store status

# Prune unused packages
pnpm store prune
```

---

## Best Practices

1. **Always commit pnpm-lock.yaml** for reproducible builds
2. **Use `pnpm install --frozen-lockfile`** in CI/CD
3. **Enable strict-peer-dependencies** for better dependency hygiene
4. **Use workspaces** for monorepo management
5. **Leverage content-addressable store** for disk savings
6. **Run `pnpm audit`** before SBOM generation

### Strict Mode Configuration

```ini
# .npmrc
strict-peer-dependencies=true
auto-install-peers=false
```

---

## Troubleshooting

### Missing Lock File
```bash
# Generate lock file
pnpm install
```

### Lock File Out of Sync
```bash
# Regenerate lock file
rm pnpm-lock.yaml
pnpm install
```

### Peer Dependency Issues
```bash
# Auto-install peers
pnpm install --auto-install-peers

# Or configure in .npmrc
# auto-install-peers=true
```

### Private Packages
```ini
# .npmrc
@mycompany:registry=https://npm.mycompany.com/
//npm.mycompany.com/:_authToken=${NPM_TOKEN}
```

### Hoisting Issues

```ini
# .npmrc - if packages need flat node_modules
shamefully-hoist=true

# Or hoist specific packages
public-hoist-pattern[]=*eslint*
```

---

## Monorepo Support

pnpm excels at monorepo management:

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
  - 'apps/*'
```

**SBOM Considerations**:
- Generate per-workspace or root-level
- Use `--filter` to target specific packages
- Consider shared dependencies

```bash
# SBOM for specific workspace
pnpm --filter @mycompany/web cyclonedx-pnpm

# SBOM for all workspaces
pnpm -r cyclonedx-pnpm
```

---

## Best Practices Detection

### pnpm Lock File Present
**Pattern**: `pnpm-lock\.yaml`
**Type**: regex
**Severity**: info
**Languages**: [yaml]
**Context**: lock file
- Lock file ensures reproducible builds
- Required for deterministic installs

### Strict Engine Mode
**Pattern**: `engine-strict\s*=\s*true`
**Type**: regex
**Severity**: info
**Languages**: [ini]
**Context**: .npmrc
- Node.js version enforcement
- Prevents version mismatch issues

### Workspace Configuration
**Pattern**: `pnpm-workspace\.yaml`
**Type**: regex
**Severity**: info
**Languages**: [yaml]
**Context**: project root
- Monorepo properly configured
- Workspace packages defined

---

## Anti-Patterns Detection

### HTTP Registry (Insecure)
**Pattern**: `registry\s*=\s*['\"]?http://(?!localhost)`
**Type**: regex
**Severity**: critical
**Languages**: [ini]
**Context**: .npmrc
- Non-HTTPS npm registry
- CWE-319: Cleartext Transmission

### Git Dependency Without Commit
**Pattern**: `['\"]git\+[^#]+['\"](?!#[a-f0-9]{40}|#semver:)`
**Type**: regex
**Severity**: medium
**Languages**: [json]
**Context**: package.json
- Git dependency without pinned commit
- CWE-829: Unpinned git dependency

### Version Wildcard
**Pattern**: `['\"]\\*['\"]|['\"]:?\\*['\"]`
**Type**: regex
**Severity**: high
**Languages**: [json]
**Context**: package.json
- Wildcard version allows any version
- CWE-829: Dependency version not pinned

### Missing Lock File
**Pattern**: `package\.json(?![\s\S]*pnpm-lock\.yaml)`
**Type**: regex
**Severity**: medium
**Languages**: [json]
**Context**: package.json
- No pnpm-lock.yaml found
- CWE-829: Non-reproducible builds

---

## References

- [pnpm Documentation](https://pnpm.io/)
- [pnpm Lock File Format](https://pnpm.io/git#lockfiles)
- [CycloneDX pnpm](https://github.com/CycloneDX/cyclonedx-node-pnpm)
- [pnpm Workspaces](https://pnpm.io/workspaces)
