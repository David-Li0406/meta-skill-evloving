# npm Registry

**Category**: package-registries
**Description**: Official package registry for Node.js/JavaScript packages
**Homepage**: https://www.npmjs.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*npm CLI and related packages*

- `npm` - npm CLI
- `npm-registry-fetch` - Fetch from npm registry
- `libnpm` - Programmatic npm access
- `npm-profile` - npm profile management
- `npm-check-updates` - Update checker

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate npm registry usage*

- `.npmrc` - npm configuration file
- `package.json` - Node.js package manifest
- `package-lock.json` - npm lock file
- `.npm/` - npm cache directory
- `npm-shrinkwrap.json` - npm shrinkwrap file

### Code Patterns

**Pattern**: `registry\.npmjs\.org|registry\.npmmirror\.com`
- npm registry URLs
- Example: `https://registry.npmjs.org`

**Pattern**: `NPM_TOKEN|NPM_AUTH_TOKEN|npm_token`
- npm token environment variables
- Example: `NPM_TOKEN=npm_...`

**Pattern**: `//registry\.npmjs\.org/:_authToken`
- npm auth configuration in .npmrc
- Example: `//registry.npmjs.org/:_authToken=npm_abc123...`

**Pattern**: `npm publish|npm login|npm adduser`
- npm publishing commands
- Example: `npm publish --access public`

---

## Environment Variables

- `NPM_TOKEN` - npm authentication token
- `NPM_AUTH_TOKEN` - Alternative token variable
- `NPM_CONFIG_REGISTRY` - Custom registry URL
- `NPM_CONFIG_USERCONFIG` - Custom .npmrc path
- `NPM_CONFIG_CACHE` - npm cache directory
- `NODE_AUTH_TOKEN` - Node.js auth token (GitHub Actions)

## Detection Notes

- .npmrc in project root or home directory
- package-lock.json indicates npm (vs yarn.lock or pnpm-lock.yaml)
- Scoped packages (@org/package) may use different registries
- npm tokens start with "npm_" for granular access tokens
- Legacy tokens are UUIDs

---

## Secrets Detection

### Tokens

#### npm Granular Access Token
**Pattern**: `npm_[a-zA-Z0-9]{36}`
**Severity**: critical
**Description**: npm granular access token (new format)
**Example**: `npm_abc123def456ghi789jkl012mno345pqr`

#### npm Legacy Token (UUID)
**Pattern**: `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}`
**Severity**: critical
**Description**: npm legacy authentication token (UUID format)
**Context Required**: Near npm, npmrc, or registry references
**Example**: `12345678-1234-1234-1234-123456789012`

#### npm Auth Token in .npmrc
**Pattern**: `//:_authToken=([a-zA-Z0-9_-]+)`
**Severity**: critical
**Description**: Authentication token in .npmrc file
**Example**: `//registry.npmjs.org/:_authToken=npm_abc123...`

#### npm Base64 Auth
**Pattern**: `_auth\s*=\s*([A-Za-z0-9+/=]{20,})`
**Severity**: critical
**Description**: Base64-encoded credentials in .npmrc
**Example**: `_auth=dXNlcjpwYXNz...`

### Validation

#### API Documentation
- **npm Registry API**: https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md
- **npm CLI**: https://docs.npmjs.com/cli

#### Validation Endpoint
**API**: Whoami
**Endpoint**: `https://registry.npmjs.org/-/whoami`
**Method**: GET
**Headers**: `Authorization: Bearer {token}`
**Purpose**: Validates token and returns username

```bash
# Validate npm token
curl -H "Authorization: Bearer $NPM_TOKEN" \
     "https://registry.npmjs.org/-/whoami"
```

---

## TIER 3: Configuration Extraction

### Registry URL Extraction

**Pattern**: `registry\s*=\s*['"]?(https?://[^\s'"]+)['"]?`
- npm registry URL from .npmrc
- Extracts: `registry_url`
- Example: `registry=https://registry.npmjs.org/`

### Scoped Registry Extraction

**Pattern**: `(@[a-z0-9-]+):registry\s*=\s*['"]?(https?://[^\s'"]+)['"]?`
- Scoped package registry
- Extracts: `scope`, `registry_url`
- Example: `@myorg:registry=https://npm.pkg.github.com`

### Package Scope Extraction

**Pattern**: `"name"\s*:\s*"(@[a-z0-9-]+)/([a-z0-9._-]+)"`
- Scoped package name from package.json
- Extracts: `scope`, `package_name`
- Example: `"name": "@myorg/mypackage"`
