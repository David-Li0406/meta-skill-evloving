# File and Path Exclusions

## Standard Exclusions

### Version Control

```gitignore
.git/
.svn/
.hg/
.bzr/
```

Never scan VCS internal directories.

### Package Managers

```gitignore
# Node.js
node_modules/
package-lock.json
yarn.lock
pnpm-lock.yaml
.npm/
.yarn/

# Python
venv/
.venv/
env/
.env/  # Virtual env, not dotenv
__pycache__/
*.pyc
.pip/
pip-cache/
Pipfile.lock
poetry.lock

# Ruby
vendor/bundle/
Gemfile.lock
.bundle/

# Go
vendor/
go.sum

# Rust
target/
Cargo.lock

# PHP
vendor/
composer.lock

# Java/Kotlin
.gradle/
.m2/
build/
target/
*.jar
*.war
```

### Build Outputs

```gitignore
# General
dist/
build/
out/
output/
bin/
obj/

# Frontend
.next/
.nuxt/
.output/
.svelte-kit/
.vercel/
.netlify/

# Coverage
coverage/
.nyc_output/
htmlcov/
.coverage
*.lcov
```

### IDE and Editor

```gitignore
.idea/
.vscode/
*.swp
*.swo
*~
.project
.classpath
.settings/
*.sublime-*
```

### OS Files

```gitignore
.DS_Store
Thumbs.db
Desktop.ini
*.lnk
```

---

## File Type Exclusions

### Binary Files

```gitignore
# Images
*.png
*.jpg
*.jpeg
*.gif
*.ico
*.svg
*.webp
*.bmp
*.tiff

# Fonts
*.woff
*.woff2
*.ttf
*.eot
*.otf

# Documents
*.pdf
*.doc
*.docx
*.xls
*.xlsx
*.ppt
*.pptx

# Archives
*.zip
*.tar
*.gz
*.bz2
*.7z
*.rar

# Media
*.mp3
*.mp4
*.wav
*.avi
*.mov
*.webm

# Compiled
*.exe
*.dll
*.so
*.dylib
*.a
*.o
*.class
*.pyc
*.pyo
```

### Generated Files

```gitignore
# Minified
*.min.js
*.min.css
*.bundle.js
*.bundle.css

# Source maps
*.map
*.js.map
*.css.map

# Type definitions (generated)
*.d.ts.map

# Auto-generated
**/generated/
**/auto-generated/
*.generated.*
```

---

## Project-Specific Exclusions

### Documentation

```gitignore
# Usually safe to exclude from secret scanning
# but may want to verify examples don't contain real secrets

docs/
documentation/
wiki/
*.md
*.rst
*.txt
CHANGELOG*
HISTORY*
AUTHORS*
CONTRIBUTORS*
```

### Test Data

```gitignore
# Test directories (lower severity, not excluded)
# test/
# tests/
# __tests__/
# spec/

# Test fixtures (can exclude or scan with lower severity)
fixtures/
__fixtures__/
testdata/
test-data/
mocks/
__mocks__/
stubs/
```

### Vendor/Third-Party

```gitignore
# Already covered by package managers above
# Additional third-party inclusions:
third-party/
third_party/
external/
libs/
lib/  # Be careful - may contain project code
```

---

## Tool-Specific Configuration

### detect-secrets (.secrets.baseline)

```json
{
  "exclude": {
    "files": "node_modules|vendor|\\.git|package-lock\\.json|yarn\\.lock",
    "lines": null
  }
}
```

### TruffleHog

```bash
# Exclude paths via command line
trufflehog git file://. \
  --exclude-paths=node_modules \
  --exclude-paths=vendor \
  --exclude-paths=.git
```

Or create `.trufflehog.yaml`:

```yaml
exclude_paths:
  - node_modules/
  - vendor/
  - .git/
  - "*.lock"
```

---

## Size-Based Exclusions

### Large Files

Skip files over certain size (e.g., 1MB):

```bash
# Find large files
find . -type f -size +1M

# Common large files to exclude
*.sql      # Database dumps
*.sqlite   # Database files
*.log      # Log files
*.csv      # Data exports
*.json     # Large data files (check individually)
```

### Rationale

- Large files slow down scanning
- Secrets are typically in configuration, not data files
- Binary data may false-positive match patterns

---

## Performance Optimization

### Parallel Scanning

```bash
# Use multiple cores
trufflehog git file://. --concurrency=8
```

### Incremental Scanning

```bash
# Only scan changed files
git diff --name-only HEAD~1 | xargs trufflehog filesystem

# Since specific commit
trufflehog git file://. --since-commit abc123
```

### Shallow Scans

```bash
# Only scan recent history
trufflehog git file://. --max-depth=50

# Only current branch
trufflehog git file://. --branch=main
```

---

## Verification Checklist

Before adding exclusions, verify:

- [ ] Path doesn't contain configuration files
- [ ] Path doesn't contain environment setup scripts
- [ ] Exclusion won't hide secrets in custom files
- [ ] Team agrees on exclusion policy
- [ ] Exclusion is documented in project README

### Dangerous Exclusions (Avoid)

```gitignore
# DON'T exclude these entirely:
*.env*           # May have .env.production
*config*         # Contains app configuration
*settings*       # May have secrets
*.json           # Many config files are JSON
*.yaml           # Many config files are YAML
*.yml
*.xml
scripts/         # May contain deployment scripts
deploy/          # Contains deployment configuration
```

Instead, use specific exclusions:

```gitignore
# DO exclude specific safe patterns:
.env.example
config.example.json
settings.sample.yaml
```
