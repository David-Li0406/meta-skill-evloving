# GitHub Packages

**Category**: package-registries
**Description**: GitHub's package hosting service for npm, Docker, Maven, NuGet, and RubyGems
**Homepage**: https://github.com/features/packages

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

No specific SDK packages - GitHub Packages is a registry, not a library.

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate GitHub Packages usage*

- `.npmrc` - NPM config with GitHub registry
- `nuget.config` - NuGet config with GitHub source
- `settings.xml` - Maven settings with GitHub Packages
- `Gemfile` - Ruby Gemfile with GitHub source
- `.docker/config.json` - Docker config with ghcr.io

### Code Patterns

**Pattern**: `npm\.pkg\.github\.com|ghcr\.io|maven\.pkg\.github\.com|nuget\.pkg\.github\.com|rubygems\.pkg\.github\.com`
- GitHub Packages registry URLs
- Example: `https://npm.pkg.github.com`

**Pattern**: `@[a-z0-9-]+:registry=https://npm\.pkg\.github\.com`
- NPM scoped registry configuration
- Example: `@myorg:registry=https://npm.pkg.github.com`

**Pattern**: `GITHUB_TOKEN|GH_TOKEN|GITHUB_PACKAGES_TOKEN`
- GitHub token environment variables
- Example: `GITHUB_TOKEN=ghp_...`

**Pattern**: `docker\.pkg\.github\.com|ghcr\.io/[a-z0-9-]+/`
- GitHub Container Registry URLs
- Example: `ghcr.io/myorg/myimage:latest`

**Pattern**: `publishConfig.*registry.*npm\.pkg\.github\.com`
- NPM publish configuration for GitHub
- Example: `"publishConfig": {"registry": "https://npm.pkg.github.com"}`

---

## Environment Variables

- `GITHUB_TOKEN` - GitHub personal access token
- `GH_TOKEN` - Alternative GitHub token variable
- `GITHUB_PACKAGES_TOKEN` - Specific token for packages
- `NPM_TOKEN` - NPM token (often GitHub token)
- `NODE_AUTH_TOKEN` - Node.js auth token
- `NUGET_AUTH_TOKEN` - NuGet auth token
- `MAVEN_USERNAME` - Maven username (github)
- `MAVEN_CENTRAL_TOKEN` - Maven token (GitHub token)

## Detection Notes

- ghcr.io is the GitHub Container Registry
- npm.pkg.github.com hosts NPM packages
- maven.pkg.github.com hosts Maven/Gradle packages
- nuget.pkg.github.com hosts NuGet packages
- rubygems.pkg.github.com hosts RubyGems
- Tokens require appropriate scopes (read:packages, write:packages)

---

## Secrets Detection

### Tokens

#### GitHub Personal Access Token (Classic)
**Pattern**: `ghp_[a-zA-Z0-9]{36}`
**Severity**: critical
**Description**: GitHub personal access token (classic format)
**Example**: `ghp_abc123def456ghi789jkl012mno345pqr678`

#### GitHub Personal Access Token (Fine-grained)
**Pattern**: `github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}`
**Severity**: critical
**Description**: GitHub fine-grained personal access token
**Example**: `github_pat_11ABC...`

#### GitHub OAuth Access Token
**Pattern**: `gho_[a-zA-Z0-9]{36}`
**Severity**: critical
**Description**: GitHub OAuth access token
**Example**: `gho_abc123def456...`

#### GitHub App Token
**Pattern**: `ghu_[a-zA-Z0-9]{36}|ghs_[a-zA-Z0-9]{36}`
**Severity**: critical
**Description**: GitHub App user or server token
**Example**: `ghu_abc123...` or `ghs_abc123...`

#### GitHub Refresh Token
**Pattern**: `ghr_[a-zA-Z0-9]{36}`
**Severity**: critical
**Description**: GitHub refresh token
**Example**: `ghr_abc123...`

#### NPM Auth Token for GitHub
**Pattern**: `//npm\.pkg\.github\.com/:_authToken=([a-zA-Z0-9_]+)`
**Severity**: critical
**Description**: NPM auth token in .npmrc for GitHub Packages
**Example**: `//npm.pkg.github.com/:_authToken=ghp_...`

### Validation

#### API Documentation
- **GitHub Packages**: https://docs.github.com/en/packages
- **Container Registry**: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry

#### Validation Endpoint
**API**: Get authenticated user
**Endpoint**: `https://api.github.com/user`
**Method**: GET
**Headers**: `Authorization: Bearer {token}`
**Purpose**: Validates token and returns user info

```bash
# Validate GitHub token
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
     "https://api.github.com/user"
```

---

## TIER 3: Configuration Extraction

### Registry URL Extraction

**Pattern**: `registry\s*=\s*https://npm\.pkg\.github\.com/?([a-z0-9-]*)`
- GitHub NPM registry from .npmrc
- Extracts: `org_name` (optional)
- Example: `registry=https://npm.pkg.github.com/myorg`

### Container Image Extraction

**Pattern**: `ghcr\.io/([a-z0-9-]+)/([a-z0-9._-]+)(?::([a-z0-9._-]+))?`
- GitHub Container Registry image
- Extracts: `owner`, `image_name`, `tag`
- Example: `ghcr.io/myorg/myapp:v1.2.3`
