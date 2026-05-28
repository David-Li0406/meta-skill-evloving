# Bundler Package Manager

**Ecosystem**: Ruby
**Package Registry**: https://rubygems.org
**Documentation**: https://bundler.io/

---

## TIER 1: Manifest Detection

### Manifest Files

| File | Required | Description |
|------|----------|-------------|
| `Gemfile` | Yes | Dependency specification |
| `.bundle/config` | No | Bundler configuration |

### Gemfile Detection

**Pattern**: `Gemfile$`
**Confidence**: 98% (HIGH)

### Required Sections for SBOM

```ruby
# Gemfile
source 'https://rubygems.org'

ruby '3.2.0'

gem 'rails', '~> 7.0.0'
gem 'pg', '~> 1.5'
gem 'puma', '~> 6.0'

group :development, :test do
  gem 'rspec-rails', '~> 6.0'
  gem 'factory_bot_rails'
end

group :development do
  gem 'rubocop', require: false
end

group :test do
  gem 'capybara'
  gem 'selenium-webdriver'
end
```

### Dependency Types

| Group | Included in SBOM | Notes |
|-------|------------------|-------|
| Default (no group) | Yes (always) | Production runtime |
| `:development` | Configurable | Development tools |
| `:test` | Configurable | Testing frameworks |
| `:production` | Yes (always) | Production-specific |
| Custom groups | Configurable | User-defined |

---

## TIER 2: Lock File Detection

### Lock File

| File | Format | Version |
|------|--------|---------|
| `Gemfile.lock` | Text | Bundler 1.x/2.x |

**Pattern**: `Gemfile\.lock$`
**Confidence**: 98% (HIGH)

### Lock File Structure

```
GEM
  remote: https://rubygems.org/
  specs:
    actioncable (7.0.8)
      actionpack (= 7.0.8)
      activesupport (= 7.0.8)
      nio4r (~> 2.0)
      websocket-driver (>= 0.6.1)
    actionmailbox (7.0.8)
      actionpack (= 7.0.8)
      activejob (= 7.0.8)
      activerecord (= 7.0.8)

PLATFORMS
  arm64-darwin-22
  x86_64-linux

DEPENDENCIES
  rails (~> 7.0.0)
  pg (~> 1.5)

RUBY VERSION
   ruby 3.2.0p0

BUNDLED WITH
   2.4.21
```

### Key Lock File Fields

| Section | SBOM Use |
|---------|----------|
| `GEM specs` | Package versions and dependencies |
| `remote` | Source registry URL |
| `DEPENDENCIES` | Direct dependencies |
| `PLATFORMS` | Platform constraints |
| `BUNDLED WITH` | Bundler version |

---

## TIER 3: Configuration Extraction

### Registry Configuration

**File**: `.bundle/config` or `Gemfile`

**Pattern (Gemfile)**: `source\s+['\"]([^'\"]+)['\"]`
**Pattern (config)**: `BUNDLE_MIRROR__RUBYGEMS__ORG:\s*['\"]?([^\s'\"]+)`

### Common Configuration

```yaml
# .bundle/config
---
BUNDLE_MIRROR__RUBYGEMS__ORG: "https://gems.mycompany.com/"
BUNDLE_GEM__MYCOMPANY__COM: "username:password"
BUNDLE_PATH: "vendor/bundle"
BUNDLE_WITHOUT: "development:test"
BUNDLE_JOBS: "4"
```

### Gemfile Sources

```ruby
# Gemfile
source 'https://rubygems.org'

# Private gem server
source 'https://gems.mycompany.com/' do
  gem 'my_private_gem'
end

# Git source
gem 'my_gem', git: 'https://github.com/myorg/my_gem.git', tag: 'v1.0.0'

# Path source (local gem)
gem 'local_gem', path: '../local_gem'
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `BUNDLE_RUBYGEMS__MYCOMPANY__COM` | Private registry credentials |
| `BUNDLE_PATH` | Installation path |
| `BUNDLE_WITHOUT` | Groups to exclude |
| `BUNDLE_DEPLOYMENT` | Deployment mode |
| `GEM_HOME` | Gem installation directory |

---

## SBOM Generation

### Using cdxgen

```bash
# Install cdxgen
npm install -g @cyclonedx/cdxgen

# Generate SBOM
cdxgen -o sbom.json

# Specify project type
cdxgen --project-type ruby -o sbom.json

# Exclude dev dependencies
cdxgen --no-dev -o sbom.json
```

### Using cyclonedx-ruby

```bash
# Install gem
gem install cyclonedx-ruby

# Generate SBOM
cyclonedx-ruby -o sbom.json

# Exclude groups
cyclonedx-ruby --exclude-group development --exclude-group test -o sbom.json
```

### Using cdxgen

```bash
# Generate from directory
cdxgen -o sbom.json

# Specify type
cdxgen -t ruby -o sbom.json
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--exclude-group` | Exclude dependency group | Include all |
| `--output-format` | json or xml | json |
| `--spec-version` | CycloneDX version | Latest |

---

## Cache Locations

| Location | Path |
|----------|------|
| System Gems | `/usr/local/lib/ruby/gems/` |
| User Gems | `~/.gem/ruby/<version>/` |
| Bundler Cache | `~/.bundle/cache/` |
| Vendor Bundle | `./vendor/bundle/` |

```bash
# Find gem paths
gem env

# Show bundle path
bundle config path

# List installed gems
bundle list
```

---

## Best Practices

1. **Always commit Gemfile.lock** for reproducible builds
2. **Use `bundle install --deployment`** in CI/CD
3. **Vendor gems** for air-gapped deployments with `bundle package`
4. **Use `bundle exec`** to ensure correct gem versions
5. **Run `bundle audit`** for vulnerability scanning
6. **Use `bundle outdated`** to check for updates

### Deployment Mode

```bash
# CI/CD install (strict, deployment mode)
bundle config set --local deployment true
bundle config set --local without 'development test'
bundle install

# Or single command
bundle install --deployment --without development test
```

### Vendoring Gems

```bash
# Package gems for offline use
bundle package --all

# Creates vendor/cache/ with .gem files
```

---

## Troubleshooting

### Missing Lock File
```bash
# Generate lock file
bundle lock
```

### Lock File Out of Sync
```bash
# Update lock file
bundle lock --update

# Full reinstall
rm Gemfile.lock
bundle install
```

### Version Conflicts
```bash
# Show dependency tree
bundle viz

# Or text format
bundle list --verbose
```

### Private Gems
```bash
# Configure credentials
bundle config set gems.mycompany.com username:password

# Or environment variable
export BUNDLE_GEMS__MYCOMPANY__COM="username:password"
```

### Platform Issues
```bash
# Add platform to lock file
bundle lock --add-platform x86_64-linux

# Remove platform
bundle lock --remove-platform ruby
```

---

## Security Scanning

### Bundle Audit

```bash
# Install
gem install bundler-audit

# Scan for vulnerabilities
bundle audit check

# Update vulnerability database
bundle audit update

# Check and update
bundle audit check --update
```

---

## Best Practices Detection

### Gemfile.lock Present
**Pattern**: `Gemfile\.lock`
**Type**: regex
**Severity**: info
**Languages**: [ruby]
**Context**: lock file
- Lock file ensures reproducible builds
- Recommended for all Bundler projects

### Ruby Version Specified
**Pattern**: `ruby\s+['\"][0-9]+\.[0-9]+`
**Type**: regex
**Severity**: info
**Languages**: [ruby]
**Context**: Gemfile
- Ruby version pinned in Gemfile
- Best practice for environment consistency

### HTTPS Source
**Pattern**: `source\s+['\"]https://rubygems\.org['\"]`
**Type**: regex
**Severity**: info
**Languages**: [ruby]
**Context**: Gemfile
- Using HTTPS for RubyGems source
- Secure registry connection

### Bundle Audit Integration
**Pattern**: `bundler-audit|bundle audit`
**Type**: regex
**Severity**: info
**Languages**: [ruby, yaml]
**Context**: CI/CD
- Security scanning integrated
- Vulnerability detection enabled

---

## Anti-Patterns Detection

### HTTP Source (Insecure)
**Pattern**: `source\s+['\"]http://(?!localhost)`
**Type**: regex
**Severity**: critical
**Languages**: [ruby]
**Context**: Gemfile
- Non-HTTPS gem source
- CWE-319: Cleartext Transmission

### Git Dependency Without Tag/Ref
**Pattern**: `git:\s*['\"][^'\"]+['\"](?!.*tag:|ref:|branch:.*v[0-9])`
**Type**: regex
**Severity**: medium
**Languages**: [ruby]
**Context**: Gemfile
- Git dependency without pinned version
- CWE-829: Unpinned git dependency

### Path Dependency
**Pattern**: `path:\s*['\"][^'\"]+['\"]`
**Type**: regex
**Severity**: medium
**Languages**: [ruby]
**Context**: Gemfile
- Local path dependency (not portable)
- May cause reproducibility issues

### Missing Ruby Version
**Pattern**: `^source.*rubygems(?![\s\S]*^ruby\s)`
**Type**: regex
**Severity**: low
**Languages**: [ruby]
**Context**: Gemfile
- No Ruby version specified
- May cause version mismatch issues

### Wildcard Version
**Pattern**: `gem\s+['\"][^'\"]+['\"]\s*$`
**Type**: regex
**Severity**: medium
**Languages**: [ruby]
**Context**: Gemfile
- Gem without version constraint
- CWE-829: Dependency version not pinned

---

## References

- [Bundler Documentation](https://bundler.io/)
- [Gemfile Manual](https://bundler.io/man/gemfile.5.html)
- [CycloneDX Ruby](https://github.com/CycloneDX/cyclonedx-ruby-gem)
- [bundler-audit](https://github.com/rubysec/bundler-audit)
- [RubyGems Guides](https://guides.rubygems.org/)
