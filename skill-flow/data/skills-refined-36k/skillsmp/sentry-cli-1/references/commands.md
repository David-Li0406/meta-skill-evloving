# Sentry CLI Commands Reference

## Table of Contents
- [Configuration & Authentication](#configuration--authentication)
- [Release Management](#release-management)
- [Debug Information Files (DIFs)](#debug-information-files-difs)
- [Source Maps](#source-maps)
- [Deploys](#deploys)
- [Environment Variables](#environment-variables)

## Configuration & Authentication

### Login
```bash
# Interactive login (simplest)
sentry-cli login

# For self-hosted instances
sentry-cli --url https://myserver.invalid/ login

# With auth token
sentry-cli login --auth-token ___ORG_AUTH_TOKEN___
```

### Verify Configuration
```bash
sentry-cli info
```

### Configuration File (~/.sentryclirc)
```ini
[auth]
token=___ORG_AUTH_TOKEN___

[defaults]
url=https://mysentry.invalid/
org=my-org
project=my-project
```

## Release Management

### Create Release
```bash
# Basic creation
sentry-cli releases new "$VERSION"

# With auto-determined version from git
VERSION=$(sentry-cli releases propose-version)
sentry-cli releases new "$VERSION"

# Create and finalize immediately
sentry-cli releases new "$VERSION" --finalize

# Using org and project flags
sentry-cli releases -o my-org -p my-project new "$VERSION"
```

### Finalize Release
```bash
# Finalize after build steps
sentry-cli releases finalize "$VERSION"
```

### Associate Commits
```bash
# Automatic commit association
sentry-cli releases set-commits "$VERSION" --auto

# Manual commit specification
sentry-cli releases set-commits "$VERSION" --commit "repo-owner/repo-name@deadbeef"

# Using local git (no repository integration needed)
sentry-cli releases set-commits "$VERSION" --local

# Commit range between releases
sentry-cli releases set-commits "$VERSION" --commit \
  "repo-owner/repo-name@<previous_commit>..<current_commit>"

# Ignore missing commits (for rebased/amended commits)
sentry-cli releases set-commits "$VERSION" --auto --ignore-missing
```

## Debug Information Files (DIFs)

### Validate Debug Files
```bash
sentry-cli debug-files check <file>
```

### Find Missing Debug Files
```bash
sentry-cli debug-files find <identifier>
```

### Upload Debug Symbols
```bash
# Basic upload (recursively scans folders/ZIPs)
sentry-cli debug-files upload -o <org> -p <project> /path/to/files...

# Upload with server-side processing (waits for completion)
sentry-cli debug-files upload -o <org> -p <project> --wait /path/to/files...

# iOS: Upload with BCSymbolMaps for hidden symbols
sentry-cli debug-files upload --symbol-maps path/to/symbolmaps path/to/debug/symbols

# Upload with source bundles
sentry-cli debug-files upload --include-sources /path/to/files...

# Create source bundles separately
sentry-cli debug-files bundle-sources /path/to/files...
sentry-cli debug-files upload --type sourcebundle /path/to/bundles...
```

### ProGuard Upload (Android)
```bash
sentry-cli upload-proguard --uuid A_VALID_UUID app/build/outputs/mapping/{BuildVariant}/mapping.txt
```

## Source Maps

### Upload Source Maps
```bash
# Basic upload
sentry-cli sourcemaps upload /path/to/sourcemaps

# With URL prefix (maps file paths to URLs)
sentry-cli sourcemaps upload /path/to/sourcemaps --url-prefix '~/static/js'

# Strip common prefix from paths
sentry-cli sourcemaps upload /path/to/sourcemaps --url-prefix '~/static/js' \
  --strip-common-prefix

# With ignore file
sentry-cli sourcemaps upload /path/to/sourcemaps --ignore-file .sentryignore
```

### Source Map Options
- `--dist`: Distribution identifier for build variants
- `--no-rewrite`: Disable automatic source map rewriting
- `--validate`: Enable validation when rewriting is disabled
- `--strict`: Fail if no source maps are found
- `--ext`: Override file extensions to process

## Deploys

### Create Deploy
```bash
# Basic deploy
sentry-cli deploys new --release "$VERSION" -e ENVIRONMENT

# Deploy with duration tracking
start=$(date +%s)
# ... deployment process ...
now=$(date +%s)
sentry-cli deploys new --release "$VERSION" -e ENVIRONMENT -t $((now-start))
```

### List Deploys
```bash
sentry-cli deploys list --release "$VERSION"
```

## Environment Variables

### Authentication
- `SENTRY_AUTH_TOKEN`: Primary authentication token
- `SENTRY_API_KEY`: Legacy API key option
- `SENTRY_DSN`: Direct Sentry connection DSN

### Configuration
- `SENTRY_URL`: Server endpoint (defaults to sentry.io)
- `SENTRY_ORG`: Organization ID or slug
- `SENTRY_PROJECT`: Project ID or slug

### Behavior Control
- `SENTRY_LOG_LEVEL`: Set logging verbosity (trace, debug, info, warn, error)
- `SENTRY_HTTP_MAX_RETRIES`: Maximum HTTP retry attempts (default: 5)
- `SENTRY_NO_PROGRESS_BAR`: Disable progress indicators
- `SENTRY_LOAD_DOTENV`: Control `.env` file loading
- `SENTRY_PROPERTIES`: Path to properties file (Java/React Native)

## Best Practices

### Releases
- Use unique version names across projects within your organization (e.g., `projectA-1.0`)
- Finalize releases after deployment to production for accurate issue tracking
- Use `--local` when deploying without access to configured repositories
- Apply `--ignore-missing` when commits have been rebased or amended

### Debug Files
- Use `--wait` flag when uploading debug symbols to ensure processing completes
- For iOS with BCSymbolMaps, always use `--symbol-maps` to restore hidden symbols
- Validate debug files with `check` before uploading to catch issues early

### Source Maps
- Always specify `--url-prefix` to match your deployed asset URLs
- Use `--strip-common-prefix` to simplify path mappings
- Consider using `.sentryignore` to exclude unnecessary files
