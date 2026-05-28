---
name: GitHub Actions Debugging
description: Debug and troubleshoot GitHub Actions CI/CD workflows for the SOMA project
---

# GitHub Actions Debugging Skill

This skill guides debugging and troubleshooting GitHub Actions workflows in the SOMA project.

## When to Use This Skill

Use this skill when you need to:
- Debug failing CI/CD workflows
- Troubleshoot deployment issues
- Analyze workflow execution logs
- Fix race conditions in pipelines
- Resolve SFTP/deployment failures
- Debug PHPUnit test failures in CI

## SOMA Workflow Architecture

### Workflow Files

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci-cd.yml` | Push to `main`, `week-*`, PRs, tags | Unified CI/CD pipeline |

### CI/CD Pipeline Stages

```
Tag Push (v*)
    ↓
Stage 1: Quality Gates (parallel)
├── code-quality: PHPCS + PHPStan
├── php-tests: PHPUnit 108 tests
└── frontend-build: npm prod
    ↓
Stage 2: Build & Release
├── Create production ZIP
├── Generate release notes
└── Create GitHub Release
    ↓
Stage 3: Deploy to Production
├── SFTP upload to server
├── Backup existing theme
└── Extract new theme
    ↓
Stage 4: Summary
└── Report all stage results
```

## Common Workflow Failures

### 1. PHPCS Failures

**Symptom**: `code-quality` job fails

**Check Logs**:
```bash
gh run view RUN_ID --log | grep -A 20 "PHPCS"
```

**Common Causes**:
- Unsanitized `$_GET`/`$_POST` input
- Missing escaping on output
- Incorrect spacing/indentation
- Missing file docblocks

**Fix Locally**:
```bash
cd wp-content/themes/soma
composer phpcs        # Check errors
composer phpcbf       # Auto-fix what's possible
```

**Example Fix**:
```php
// ❌ WRONG
$value = $_GET['param'];
echo $title;

// ✅ CORRECT
$value = isset( $_GET['param'] ) ? sanitize_text_field( wp_unslash( $_GET['param'] ) ) : '';
echo esc_html( $title );
```

### 2. PHPStan Failures

**Symptom**: `code-quality` job fails at PHPStan step

**Check Logs**:
```bash
gh run view RUN_ID --log | grep -A 50 "PHPStan"
```

**Common Causes**:
- Missing return type hints
- Incompatible parameter types
- Undefined variables/methods
- Wrong PHPDoc annotations

**Fix Locally**:
```bash
cd wp-content/themes/soma
composer phpstan
```

**Example Fixes**:
```php
// ❌ Missing return type
public function get_name() { return 'soma-widget'; }

// ✅ With return type
public function get_name(): string { return 'soma-widget'; }

// ❌ Wrong PHPDoc
/** @param string $value */
public function process( $value ) {} // $value is actually array

// ✅ Correct PHPDoc
/** @param array $value */
public function process( array $value ): void {}
```

### 3. PHPUnit Test Failures

**Symptom**: `php-tests` job fails

**Check Logs**:
```bash
gh run view RUN_ID --log | grep -A 100 "PHPUnit"
```

**Common Causes**:
- Missing Elementor dependencies in CI
- Singleton state not reset between tests
- Database state issues
- Assertion failures

**Fix: Skip Elementor Tests in CI**:
```php
public function setUp(): void {
    parent::setUp();
    
    // Skip if Elementor not loaded (CI environment)
    if ( ! did_action( 'elementor/loaded' ) ) {
        $this->markTestSkipped( 'Elementor not loaded' );
        return; // IMPORTANT: Always return after markTestSkipped
    }
    
    $this->widget = new MyWidget();
}
```

**Fix: Reset Singleton**:
```php
public function tearDown(): void {
    // Reset singleton for clean state
    $reflection = new \ReflectionClass( MyClass::class );
    $property = $reflection->getProperty( 'instance' );
    $property->setValue( null, null );
    
    parent::tearDown();
}
```

### 4. Frontend Build Failures

**Symptom**: `frontend-build` job fails

**Check Logs**:
```bash
gh run view RUN_ID --log | grep -A 50 "npm"
```

**Common Causes**:
- Node.js version mismatch
- Missing dependencies
- Webpack configuration errors
- OpenSSL legacy provider issue

**Fix Locally**:
```bash
cd wp-content/themes/soma
rm -rf node_modules package-lock.json
npm install
npm run prod
```

**OpenSSL Fix** (already in package.json):
```json
{
  "scripts": {
    "dev": "NODE_OPTIONS=--openssl-legacy-provider ...",
    "prod": "NODE_OPTIONS=--openssl-legacy-provider ..."
  }
}
```

### 5. Release Creation Failures

**Symptom**: Stage 2 fails to create GitHub Release

**Common Causes**:
- Tag created from wrong branch (not `main`)
- Missing CHANGELOG.md entry
- GitHub API rate limits
- Token permissions issue

**Verify Tag Origin**:
```bash
# Check if tag is reachable from main
git log main --oneline | grep $(git rev-list -n 1 v3.1.16)

# If empty, tag is orphaned - recreate from main
git tag -d v3.1.16
git checkout main && git pull
git tag -a v3.1.16 -m "Release v3.1.16"
git push origin v3.1.16
```

### 6. SFTP Deployment Failures

**Symptom**: Stage 3 Deploy fails

**Check Logs**:
```bash
gh run view RUN_ID --log | grep -A 30 "SFTP"
```

**Common Causes**:
- SFTP credentials expired/invalid
- Server disk full
- SSH key issues
- Network timeouts

**Verify Secrets**:
1. Go to **GitHub Repo** → **Settings** → **Secrets and variables** → **Actions**
2. Check these secrets exist:
   - `FTP_HOST`
   - `FTP_USERNAME`
   - `FTP_PASSWORD` (or SSH key)
   - `FTP_PORT`

**Test SFTP Manually**:
```bash
sftp -P $PORT $USER@$HOST
# If fails, credentials need updating in GitHub Secrets
```

## Debugging Commands

### View Workflow Runs

```bash
# List recent runs
gh run list --limit 10 | cat

# List runs for specific workflow
gh run list --workflow=ci-cd.yml --limit 5 | cat

# Filter by status
gh run list --status=failure --limit 5 | cat

# Filter by branch
gh run list --branch=week-4 --limit 5 | cat
```

### View Run Details

```bash
# View run summary
gh run view RUN_ID | cat

# View run logs
gh run view RUN_ID --log | cat

# View specific job logs
gh run view RUN_ID --log --job=JOB_ID | cat

# View failed job only
gh run view RUN_ID --log-failed | cat
```

### Re-run Workflows

```bash
# Re-run all jobs
gh run rerun RUN_ID

# Re-run failed jobs only
gh run rerun RUN_ID --failed
```

### Watch Running Workflow

```bash
# Watch in real-time
gh run watch

# Watch specific run
gh run watch RUN_ID
```

### Cancel Workflow

```bash
gh run cancel RUN_ID
```

## Log Analysis Patterns

### Find Specific Errors

```bash
# Search for PHP errors
gh run view RUN_ID --log | grep -i "error\|fatal\|failed" | cat

# Find PHPCS violations
gh run view RUN_ID --log | grep "FOUND\|ERROR" | cat

# Find PHPUnit failures
gh run view RUN_ID --log | grep -A 5 "FAILURES\|Error:" | cat

# Find npm errors
gh run view RUN_ID --log | grep -i "npm ERR\|error" | cat
```

### Extract Step Output

```bash
# Get specific step output (adjust step name)
gh run view RUN_ID --log | awk '/Run vendor\/bin\/phpcs/,/::endgroup::/' | cat
```

## Environment Variables

### Check Workflow Environment

The CI environment has these differences from local:

| Aspect | Local | CI |
|--------|-------|-----|
| PHP | 8.1+ (configured) | 8.1 (GitHub Actions) |
| MySQL | Local server | Service container |
| Elementor | Loaded | NOT loaded |
| ACF PRO | Loaded | Mock/stub |
| WordPress | Full install | Test suite |

### CI-Specific Conditionals

```php
// Check if running in CI
if ( defined( 'SOMA_TESTING' ) && SOMA_TESTING ) {
    // CI-specific behavior
}

// Check for GitHub Actions specifically
if ( getenv( 'GITHUB_ACTIONS' ) ) {
    // GitHub Actions specific
}
```

## Workflow Syntax Issues

### YAML Validation

```bash
# Install yamllint
brew install yamllint

# Validate workflow file
yamllint .github/workflows/ci-cd.yml
```

### Common YAML Errors

```yaml
# ❌ WRONG - Tab character
jobs:
	build:  # Tab instead of spaces

# ✅ CORRECT - Spaces only
jobs:
  build:  # 2 spaces

# ❌ WRONG - Missing quotes on special characters
run: echo ${{ secrets.TOKEN }}  # May fail

# ✅ CORRECT - Properly quoted
run: echo "${{ secrets.TOKEN }}"

# ❌ WRONG - Multiline without proper syntax
run: |
  command1
    command2  # Wrong indentation in block

# ✅ CORRECT - Consistent indentation
run: |
  command1
  command2
```

## Race Conditions

### Symptoms
- Intermittent failures
- "Resource not found" errors
- Timing-related issues

### Prevention (Already Implemented)
The unified `ci-cd.yml` uses `needs:` to enforce sequential stages:

```yaml
jobs:
  code-quality:
    # Runs first (parallel with php-tests, frontend-build)
    
  build-release:
    needs: [code-quality, php-tests, frontend-build]
    # Only runs after ALL quality gates pass
    
  deploy:
    needs: [build-release]
    # Only runs after release is created
```

## Debugging Checklist

### Pre-Debug

- [ ] Note the Run ID from GitHub
- [ ] Check which job failed (Stage 1, 2, or 3)
- [ ] Review the error message

### During Debug

- [ ] View full logs: `gh run view RUN_ID --log-failed | cat`
- [ ] Identify error category (PHPCS, PHPStan, Tests, Build, Deploy)
- [ ] Reproduce locally if possible
- [ ] Check if error is environment-specific (CI vs local)

### Post-Fix

- [ ] Run local quality checks: `composer phpcs && composer phpstan && composer test`
- [ ] Push fix and monitor workflow
- [ ] Verify all stages pass

## Emergency: Manual Release

If CI/CD completely fails and you need emergency release:

```bash
# Build locally
cd wp-content/themes/soma
composer install --no-dev --optimize-autoloader
npm install && npm run prod

# Create ZIP manually
cd ..
zip -r soma-v3.1.16.zip soma/ \
  -x "soma/node_modules/*" \
  -x "soma/tests/*" \
  -x "soma/.git/*" \
  -x "soma/vendor/bin/*"

# Upload via cPanel or SFTP directly
# Then create GitHub release manually
gh release create v3.1.16 soma-v3.1.16.zip \
  --title "v3.1.16" \
  --notes "Emergency manual release" | cat
```

## Useful Links

- **Workflow File**: `.github/workflows/ci-cd.yml`
- **Workflow Runs**: `https://github.com/sanruiz/fibra/actions`
- **Workflow Documentation**: `docs/workflows/CI_CD.md`
- **GitHub CLI Manual**: https://cli.github.com/manual/
