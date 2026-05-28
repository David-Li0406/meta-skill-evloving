# Composer Package Manager

**Ecosystem**: PHP
**Package Registry**: https://packagist.org
**Documentation**: https://getcomposer.org/doc/

---

## TIER 1: Manifest Detection

### Manifest Files

| File | Required | Description |
|------|----------|-------------|
| `composer.json` | Yes | Project dependencies and metadata |
| `auth.json` | No | Authentication credentials |

### composer.json Detection

**Pattern**: `composer\.json$`
**Confidence**: 98% (HIGH)

### Required Sections for SBOM

```json
{
    "name": "myvendor/my-project",
    "description": "Project description",
    "type": "project",
    "require": {
        "php": "^8.1",
        "laravel/framework": "^10.0",
        "guzzlehttp/guzzle": "^7.0"
    },
    "require-dev": {
        "phpunit/phpunit": "^10.0",
        "mockery/mockery": "^1.6"
    },
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

### Dependency Types

| Field | Included in SBOM | Notes |
|-------|------------------|-------|
| `require` | Yes (always) | Production dependencies |
| `require-dev` | Configurable | Development dependencies |
| `provide` | Metadata | Virtual packages provided |
| `replace` | Metadata | Packages replaced |
| `conflict` | Metadata | Incompatible packages |
| `suggest` | No | Optional recommendations |

---

## TIER 2: Lock File Detection

### Lock File

| File | Format | Version |
|------|--------|---------|
| `composer.lock` | JSON | Composer 1.x/2.x |

**Pattern**: `composer\.lock$`
**Confidence**: 98% (HIGH)

### Lock File Structure

```json
{
    "_readme": [
        "This file locks the dependencies of your project to a known state"
    ],
    "content-hash": "abc123...",
    "packages": [
        {
            "name": "laravel/framework",
            "version": "v10.30.1",
            "source": {
                "type": "git",
                "url": "https://github.com/laravel/framework.git",
                "reference": "abc123..."
            },
            "dist": {
                "type": "zip",
                "url": "https://api.github.com/repos/laravel/framework/zipball/abc123",
                "reference": "abc123...",
                "shasum": ""
            },
            "require": {
                "php": "^8.1"
            },
            "type": "library",
            "license": ["MIT"]
        }
    ],
    "packages-dev": [],
    "aliases": [],
    "minimum-stability": "stable",
    "prefer-stable": true,
    "prefer-lowest": false,
    "platform": {
        "php": "8.1.0"
    }
}
```

### Key Lock File Fields

| Field | SBOM Use |
|-------|----------|
| `name` | Package identifier |
| `version` | Exact version |
| `dist.reference` | Git commit hash |
| `dist.shasum` | SHA-1 hash (if available) |
| `require` | Dependencies |
| `license` | License information |

---

## TIER 3: Configuration Extraction

### Registry Configuration

**File**: `composer.json` or `auth.json`

**Pattern**: `"url":\s*"([^"]+)"`
**Context**: Inside `repositories` array

### Common Configuration

```json
{
    "repositories": [
        {
            "type": "composer",
            "url": "https://packages.mycompany.com/"
        },
        {
            "type": "vcs",
            "url": "https://github.com/mycompany/private-package"
        },
        {
            "packagist.org": false
        }
    ],
    "config": {
        "secure-http": true,
        "preferred-install": "dist",
        "sort-packages": true
    }
}
```

### Authentication (auth.json)

```json
{
    "http-basic": {
        "packages.mycompany.com": {
            "username": "user",
            "password": "secret"
        }
    },
    "github-oauth": {
        "github.com": "token123..."
    },
    "gitlab-token": {
        "gitlab.com": "token456..."
    }
}
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `COMPOSER_HOME` | Composer home directory |
| `COMPOSER_CACHE_DIR` | Cache directory |
| `COMPOSER_AUTH` | JSON authentication string |
| `COMPOSER_NO_DEV` | Skip dev dependencies |

---

## SBOM Generation

### Using CycloneDX PHP Composer

```bash
# Install globally
composer global require cyclonedx/cyclonedx-php-composer

# Generate SBOM
composer make-bom

# Output to specific file
composer make-bom --output-file=sbom.json

# Exclude dev dependencies
composer make-bom --no-dev --output-file=sbom.json

# Specify format
composer make-bom --spec-version=1.5 --output-format=JSON
```

### Using cdxgen

```bash
# Install cdxgen
npm install -g @cyclonedx/cdxgen

# Generate SBOM
cdxgen -o sbom.json

# Specify project type
cdxgen --project-type php -o sbom.json

# Exclude dev dependencies
cdxgen --no-dev -o sbom.json
```

### Using cdxgen (alternative)

```bash
# Generate from directory
cdxgen -o sbom.json

# Specify type
cdxgen -t php -o sbom.json
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--no-dev` | Exclude require-dev | Include all |
| `--output-format` | JSON or XML | JSON |
| `--spec-version` | CycloneDX version | 1.5 |
| `--output-file` | Output file path | bom.json |

---

## Cache Locations

| Platform | Path |
|----------|------|
| Linux | `~/.cache/composer/` |
| macOS | `~/Library/Caches/composer/` |
| Windows | `%LocalAppData%\Composer\` |

### Cache Structure

| Directory | Content |
|-----------|---------|
| `files/` | Downloaded packages |
| `repo/` | Repository metadata |
| `vcs/` | VCS clones |

```bash
# Find cache directory
composer config cache-dir

# Clear cache
composer clear-cache

# Show global config
composer global config --list
```

---

## Best Practices

1. **Always commit composer.lock** for reproducible builds
2. **Use `composer install`** in CI/CD (not `composer update`)
3. **Run `composer audit`** for vulnerability scanning
4. **Use `--no-dev`** in production deployments
5. **Prefer `dist` over `source`** for faster installs
6. **Use platform config** to ensure PHP version compatibility

### Production Install

```bash
# CI/CD install (optimized)
composer install --no-dev --prefer-dist --optimize-autoloader --no-interaction

# With audit
composer install --no-dev --prefer-dist && composer audit
```

### Platform Requirements

```json
{
    "config": {
        "platform": {
            "php": "8.1.0"
        }
    }
}
```

---

## Troubleshooting

### Missing Lock File
```bash
# Generate lock file
composer update --lock
```

### Lock File Out of Sync
```bash
# Regenerate lock file
rm composer.lock
composer update
```

### Version Conflicts
```bash
# Show why package was installed
composer why vendor/package

# Show conflicts
composer why-not vendor/package 2.0

# Show dependency tree
composer show --tree
```

### Private Repository Issues
```bash
# Configure authentication
composer config http-basic.packages.mycompany.com username password

# Or use auth.json
# Or environment variable
export COMPOSER_AUTH='{"http-basic":{"packages.mycompany.com":{"username":"user","password":"pass"}}}'
```

### Memory Issues
```bash
# Increase memory limit
COMPOSER_MEMORY_LIMIT=-1 composer update
```

---

## Security Scanning

### Composer Audit

```bash
# Built-in audit (Composer 2.4+)
composer audit

# Output as JSON
composer audit --format=json

# Exit with error code on vulnerabilities
composer audit --locked
```

### Local PHP Security Checker

```bash
# Install
composer global require enlightn/security-checker

# Scan
security-checker security:check composer.lock
```

---

## Plugin System

Composer plugins can affect SBOM:

```json
{
    "require": {
        "composer/installers": "^2.0"
    },
    "config": {
        "allow-plugins": {
            "composer/installers": true
        }
    }
}
```

**SBOM Considerations**:
- Plugin dependencies should be included
- Custom installers may place files in non-standard locations

---

## Best Practices Detection

### Composer Lock File Present
**Pattern**: `composer\.lock`
**Type**: regex
**Severity**: info
**Languages**: [json]
**Context**: lock file
- Lock file ensures reproducible builds
- Required for deterministic installs

### PHP Version Constraint
**Pattern**: `['\"]php['\"]\s*:\s*['\"][^'\"]+['\"]`
**Type**: regex
**Severity**: info
**Languages**: [json]
**Context**: composer.json
- PHP version specified
- Best practice for compatibility

### Composer Audit Integration
**Pattern**: `composer audit|composer-audit`
**Type**: regex
**Severity**: info
**Languages**: [yaml, json]
**Context**: CI/CD
- Security scanning enabled
- Vulnerability detection integrated

---

## Anti-Patterns Detection

### HTTP Repository (Insecure)
**Pattern**: `['\"]url['\"]\s*:\s*['\"]http://(?!localhost)`
**Type**: regex
**Severity**: critical
**Languages**: [json]
**Context**: composer.json
- Non-HTTPS package repository
- CWE-319: Cleartext Transmission

### VCS Dependency Without Reference
**Pattern**: `['\"]type['\"]\s*:\s*['\"]vcs['\"](?![\s\S]*['\"]reference['\"])`
**Type**: regex
**Severity**: medium
**Languages**: [json]
**Context**: composer.json
- VCS dependency without pinned reference
- CWE-829: Unpinned dependency

### Dev Branch Dependency
**Pattern**: `['\"]dev-master['\"]|['\"]dev-main['\"]`
**Type**: regex
**Severity**: high
**Languages**: [json]
**Context**: composer.json
- Development branch as dependency
- CWE-829: Unstable dependency version

### Wildcard Version
**Pattern**: `['\"]\\*['\"]|['\"]:?\\*['\"]`
**Type**: regex
**Severity**: high
**Languages**: [json]
**Context**: composer.json
- Wildcard version constraint
- CWE-829: Dependency version not pinned

### Unsafe Plugin Allowlist
**Pattern**: `['\"]allow-plugins['\"]\s*:\s*true`
**Type**: regex
**Severity**: medium
**Languages**: [json]
**Context**: composer.json
- All plugins allowed without restriction
- CWE-829: Unrestricted plugin execution

---

## References

- [Composer Documentation](https://getcomposer.org/doc/)
- [composer.json Schema](https://getcomposer.org/doc/04-schema.md)
- [CycloneDX PHP Composer](https://github.com/CycloneDX/cyclonedx-php-composer)
- [Packagist](https://packagist.org/)
- [Composer Audit](https://getcomposer.org/doc/03-cli.md#audit)
