# Dependency Management

## Health Indicators

| Indicator | Healthy | Warning | Critical |
|-----------|---------|---------|----------|
| Outdated deps | < 10% | 10-30% | > 30% |
| Known CVEs | 0 | Low severity | High/Critical |
| Unmaintained | 0 | < 5% | > 5% |
| Major versions behind | 0-1 | 2 | 3+ |

## Audit Commands by Language

### Node.js

```bash
# List outdated packages
npm outdated
# or with more detail
npx npm-check -u

# Security audit
npm audit
npm audit fix              # Auto-fix
npm audit fix --force      # Breaking changes

# Find unused dependencies
npx depcheck

# Check for duplicate packages
npm dedupe

# Analyze bundle size
npx bundle-phobia <package>
```

### Python

```bash
# List outdated
pip list --outdated
pip list --outdated --format=json | jq

# Security audit
pip-audit
safety check

# Find unused
pip-autoremove --list

# Dependency tree
pipdeptree
pipdeptree --reverse <package>

# Update within constraints
pip install --upgrade-strategy eager -r requirements.txt
```

### Go

```bash
# List outdated
go list -m -u all

# Security audit
govulncheck ./...

# Tidy dependencies
go mod tidy

# Why is this dependency included?
go mod why <package>

# Dependency graph
go mod graph
```

### Rust

```bash
# List outdated
cargo outdated

# Security audit
cargo audit

# Update within semver
cargo update

# Unused dependencies
cargo +nightly udeps
```

## Lock Files

| Language | Lock File | Commit? |
|----------|-----------|---------|
| Node.js | `package-lock.json` | Yes |
| Python | `requirements.txt` / `poetry.lock` | Yes |
| Go | `go.sum` | Yes |
| Rust | `Cargo.lock` | Apps: Yes, Libs: No |
| Ruby | `Gemfile.lock` | Yes |

### Why Lock Files Matter

```bash
# Without lock file
npm install  # Gets latest within semver range

# With lock file
npm ci       # Gets exact versions from lock

# Reproducible builds require lock files!
```

## Update Strategies

### Conservative (Recommended for Production)

```yaml
# Dependabot config
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    versioning-strategy: increase
    groups:
      production-dependencies:
        dependency-type: "production"
      development-dependencies:
        dependency-type: "development"
```

### Automated Security Updates Only

```yaml
# GitHub Dependabot security updates
# Enabled by default for public repos
# Check: Settings > Security > Dependabot
```

### Manual Updates with Testing

```bash
# 1. Create update branch
git checkout -b deps/update-$(date +%Y%m)

# 2. Update all deps
npm update            # Minor/patch only
npm update --save     # Update package.json too

# 3. Run full test suite
npm test
npm run lint
npm run build

# 4. Check for breaking changes
npm outdated          # Review what's still outdated

# 5. Update major versions one at a time
npm install package@latest
# Test after each major update
```

## Handling Vulnerabilities

### Triage Process

```markdown
1. **Assess Impact**
   - Is the vulnerable code path used?
   - Is it in prod dependencies or dev only?
   - What's the attack vector?

2. **Check for Fix**
   - Is there a patched version?
   - Can we update without breaking?
   - Are there workarounds?

3. **Mitigate**
   - Update if possible
   - Override transitive dependency
   - Apply workaround
   - Accept risk (document why)
```

### Override Transitive Dependencies

```json
// package.json - npm 8.3+
{
  "overrides": {
    "vulnerable-package": "2.0.1"
  }
}

// pnpm
{
  "pnpm": {
    "overrides": {
      "vulnerable-package": "2.0.1"
    }
  }
}
```

```toml
# Python - pip-tools
# requirements.in
package==1.0
vulnerable-package==2.0.1  # Override

# Go - go.mod
replace vulnerable/package => vulnerable/package v2.0.1
```

## Dependency Policies

### Evaluation Criteria

| Criterion | Check |
|-----------|-------|
| Maintenance | Last commit < 1 year |
| Popularity | > 1000 weekly downloads |
| Security | No unpatched CVEs |
| License | Compatible with project |
| Size | Reasonable bundle impact |

### Adding New Dependencies

```markdown
Before adding a dependency, ask:

1. **Is it necessary?**
   - Can we implement it ourselves simply?
   - Is it a one-liner we can inline?

2. **Is it maintained?**
   - When was last release?
   - Are issues being addressed?

3. **Is it secure?**
   - Any known vulnerabilities?
   - Does it have many dependencies?

4. **Is the license compatible?**
   - MIT, Apache 2.0: Generally safe
   - GPL: May require your code to be GPL
   - No license: Don't use
```

## Monitoring

### GitHub Dependabot Alerts

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

### CI Integration

```yaml
# .github/workflows/deps.yml
name: Dependency Check
on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly
  push:
    paths:
      - 'package-lock.json'

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
```

## Red Flags

| Red Flag | Risk | Action |
|----------|------|--------|
| No lock file | Unreproducible builds | Add and commit |
| 100+ direct deps | Maintenance burden | Review necessity |
| Deps > 2 years old | Security risk | Update or replace |
| Abandoned deps | Won't get fixes | Fork or replace |
| CVE not addressed | Active vulnerability | Patch or mitigate |
| Massive dep tree | Supply chain risk | Audit dependencies |
