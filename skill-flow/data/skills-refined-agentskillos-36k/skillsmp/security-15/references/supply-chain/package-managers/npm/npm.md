# npm Package Manager

**Ecosystem**: JavaScript/Node.js
**Package Registry**: https://registry.npmjs.org
**Documentation**: https://docs.npmjs.com

---

## TIER 1: Manifest Detection

### Manifest Files

| File | Required | Description |
|------|----------|-------------|
| `package.json` | Yes | Primary manifest with dependencies |
| `.npmrc` | No | Configuration file |
| `.nvmrc` | No | Node version specification |

### Package.json Detection

**Pattern**: `package\.json$`
**Confidence**: 95% (HIGH)

**Required Fields for SBOM:**
```json
{
  "name": "package-name",
  "version": "1.0.0",
  "dependencies": {},
  "devDependencies": {}
}
```

### Dependency Types

| Field | Included in SBOM | Notes |
|-------|------------------|-------|
| `dependencies` | Yes (always) | Production runtime |
| `devDependencies` | Configurable | Development only |
| `peerDependencies` | Yes | Expected by consumer |
| `optionalDependencies` | Configurable | May fail without error |
| `bundledDependencies` | Yes | Bundled in package |

---

## TIER 2: Lock File Detection

### Lock File

| File | Format | Version |
|------|--------|---------|
| `package-lock.json` | JSON | v1, v2, v3 |

**Pattern**: `package-lock\.json$`
**Confidence**: 98% (HIGH)

### Lock File Structure (v3)

```json
{
  "name": "project",
  "version": "1.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "project",
      "dependencies": {}
    },
    "node_modules/express": {
      "version": "4.18.2",
      "resolved": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
      "integrity": "sha512-...",
      "engines": {"node": ">= 0.10.0"}
    }
  }
}
```

### Key Lock File Fields

| Field | SBOM Use |
|-------|----------|
| `version` | Exact package version |
| `resolved` | Download URL |
| `integrity` | SHA-512 hash |
| `dependencies` | Transitive dependencies |
| `dev` | Development dependency flag |
| `optional` | Optional dependency flag |
| `peer` | Peer dependency flag |

---

## TIER 3: Configuration Extraction

### Registry Configuration

**File**: `.npmrc`

**Pattern**: `registry\s*=\s*['"]?([^\s'"]+)`
**Extracts**: Custom registry URL

**Pattern**: `@scope:registry\s*=\s*['"]?([^\s'"]+)`
**Extracts**: Scoped registry URL

### Common Configuration

```ini
# Private registry
registry=https://npm.mycompany.com/

# Scoped packages
@mycompany:registry=https://npm.mycompany.com/

# Authentication
//npm.mycompany.com/:_authToken=${NPM_TOKEN}

# Cache settings
cache=/path/to/cache
prefer-offline=true
```

---

## SBOM Generation

### Native npm SBOM (v9+)

```bash
# Generate CycloneDX SBOM
npm sbom --sbom-format=cyclonedx

# Generate SPDX SBOM
npm sbom --sbom-format=spdx

# Exclude dev dependencies
npm sbom --sbom-format=cyclonedx --omit=dev

# Output to file
npm sbom --sbom-format=cyclonedx > sbom.json

# From package-lock.json only
npm sbom --package-lock-only
```

### CycloneDX npm Plugin

```bash
# Install globally
npm install -g @cyclonedx/cyclonedx-npm

# Generate SBOM
cyclonedx-npm --output-file sbom.json

# Exclude dev dependencies
cyclonedx-npm --omit=dev --output-file sbom.json

# Specific output format
cyclonedx-npm --output-format json --spec-version 1.5
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--omit=dev` | Exclude devDependencies | Include all |
| `--omit=optional` | Exclude optionalDependencies | Include |
| `--omit=peer` | Exclude peerDependencies | Include |
| `--package-lock-only` | Use lock file without node_modules | false |
| `--workspace` | Target specific workspace | All |

---

## Cache Locations

| Platform | Path |
|----------|------|
| Linux/macOS | `~/.npm/_cacache/` |
| Windows | `%AppData%/npm-cache/_cacache/` |
| Custom | `npm config get cache` |

---

## Best Practices Detection

Patterns to detect good dependency management practices in CI/CD, Makefiles, and scripts.

### npm ci
**Pattern**: `npm\s+ci`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Clean install from lock file
- Ensures reproducible builds in CI/CD

### npm audit
**Pattern**: `npm\s+audit`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Vulnerability scanning
- Should run in CI/CD pipelines

### npm audit with enforcement
**Pattern**: `npm\s+audit\s+--audit-level`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Enforcing audit results in CI/CD
- Fails build on specified severity level

### package-lock-only
**Pattern**: `--package-lock-only`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Generate lock file without node_modules
- Useful for SBOM generation

### npm sbom generation
**Pattern**: `npm\s+sbom`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Native SBOM generation (npm 9+)
- Supply chain transparency

### npm prune production
**Pattern**: `npm\s+prune\s+--production|npm\s+prune\s+--omit=dev`
**Type**: regex
**Severity**: info
**Context**: CI/CD, Makefile, scripts
- Removing dev dependencies before deployment
- Reduces attack surface

---

## Anti-Patterns Detection

Patterns that indicate potential issues.

### Missing package-lock in git
**Pattern**: `package-lock\.json` in `.gitignore`
**Type**: regex
**Severity**: high
**Context**: .gitignore
- package-lock.json should be committed for reproducible builds

### Ignoring scripts globally
**Pattern**: `ignore-scripts\s*=\s*true`
**Type**: regex
**Severity**: medium
**Context**: .npmrc
- Disabling scripts globally may indicate security concern but breaks legitimate scripts

### Wildcard versions
**Pattern**: `"[^"]+"\s*:\s*"\*"`
**Type**: regex
**Severity**: high
**Context**: package.json
- Using `*` versions is dangerous for supply chain security

### Latest tag in dependencies
**Pattern**: `"[^"]+"\s*:\s*"latest"`
**Type**: regex
**Severity**: medium
**Context**: package.json
- Using `latest` tag prevents reproducible builds

### Skipping npm audit in CI
**Pattern**: `npm\s+audit\s+--audit-level=none`
**Type**: regex
**Severity**: medium
**Context**: CI/CD
- Disabling audit checks weakens supply chain security

---

## Best Practices Summary

1. **Always commit package-lock.json** for reproducible builds
2. **Use `npm ci`** in CI/CD for clean installs from lock file
3. **Exclude dev dependencies** in production SBOMs
4. **Use lockfileVersion 3** for best SBOM compatibility
5. **Run `npm audit`** before SBOM generation for vulnerability awareness
6. **Sign SBOMs** with Sigstore for provenance

---

## Troubleshooting

### Missing Lock File
```bash
# Generate lock file
npm install --package-lock-only
```

### Lock File Out of Sync
```bash
# Regenerate lock file
rm package-lock.json
npm install
```

### Private Packages
Ensure `.npmrc` has authentication configured for private registries.

---

## References

- [npm Documentation](https://docs.npmjs.com/)
- [package-lock.json Specification](https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json)
- [npm sbom Command](https://docs.npmjs.com/cli/v10/commands/npm-sbom)
- [CycloneDX npm Plugin](https://github.com/CycloneDX/cyclonedx-node-npm)
