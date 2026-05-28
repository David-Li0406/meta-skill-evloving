# Gitignore Best Practices Patterns

**Category**: devops/git-history-security
**Description**: Files that should be in .gitignore and never committed to git history
**Type**: best-practice

These patterns detect files commonly found in git repositories that should have been gitignored.
When found in git history, these indicate potential data leaks or poor repository hygiene.

---

## Environment Files

### Environment Configuration Files
**Pattern**: `\.env$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- Environment files typically contain secrets, API keys, and database credentials
- These should NEVER be committed to version control
- Remediation: Add `.env` to .gitignore, use `.env.example` for templates

### Environment Variants
**Pattern**: `\.env\.(local|dev|development|prod|production|staging|test|ci)$`
**Type**: filepath
**Severity**: critical
**Languages**: [all]
- Environment-specific configuration files
- Often contain environment-specific secrets
- Remediation: Gitignore all `.env.*` files except templates

### Dotenv Backup Files
**Pattern**: `\.env\.bak$|\.env\.backup$|\.env\.old$`
**Type**: filepath
**Severity**: high
**Languages**: [all]
- Backup copies of environment files
- May contain outdated but still valid credentials
- Remediation: Remove and add to .gitignore

---

## IDE and Editor Files

### JetBrains IDE Directory
**Pattern**: `\.idea/`
**Type**: filepath
**Severity**: low
**Languages**: [all]
- JetBrains IDE configuration directory
- May contain project-specific settings or credentials
- Remediation: Add `.idea/` to .gitignore

### VS Code Directory
**Pattern**: `\.vscode/`
**Type**: filepath
**Severity**: low
**Languages**: [all]
- Visual Studio Code settings directory
- May contain local workspace settings
- Remediation: Add `.vscode/` to .gitignore (or be selective about what to commit)

### Vim Swap Files
**Pattern**: `.*\.swp$|.*\.swo$`
**Type**: filepath
**Severity**: informational
**Languages**: [all]
- Vim editor swap files
- May contain partial file contents
- Remediation: Add `*.swp` and `*.swo` to .gitignore

### Sublime Text Files
**Pattern**: `\.sublime-workspace$|\.sublime-project$`
**Type**: filepath
**Severity**: informational
**Languages**: [all]
- Sublime Text project files
- May contain local paths
- Remediation: Add `.sublime-*` to .gitignore

---

## Operating System Files

### macOS Metadata
**Pattern**: `\.DS_Store$`
**Type**: filepath
**Severity**: informational
**Languages**: [all]
- macOS Finder metadata files
- Contains folder settings, no security risk but clutters history
- Remediation: Add `.DS_Store` to global gitignore

### Windows Thumbnails
**Pattern**: `Thumbs\.db$|ehthumbs\.db$`
**Type**: filepath
**Severity**: informational
**Languages**: [all]
- Windows Explorer thumbnail cache
- Contains image previews
- Remediation: Add `Thumbs.db` to global gitignore

### Windows Desktop Config
**Pattern**: `[Dd]esktop\.ini$`
**Type**: filepath
**Severity**: informational
**Languages**: [all]
- Windows folder configuration
- Remediation: Add `Desktop.ini` to .gitignore

---

## Build Artifacts

### Node.js Dependencies
**Pattern**: `node_modules/`
**Type**: filepath
**Severity**: medium
**Languages**: [javascript, typescript]
- Node.js dependency directory
- Large, reproducible from package.json
- Remediation: Add `node_modules/` to .gitignore

### Python Virtual Environments
**Pattern**: `venv/|\.venv/|env/|\.env/|virtualenv/`
**Type**: filepath
**Severity**: medium
**Languages**: [python]
- Python virtual environment directories
- Large, reproducible from requirements.txt
- Remediation: Add `venv/` and `.venv/` to .gitignore

### Python Cache
**Pattern**: `__pycache__/|\.pyc$|\.pyo$`
**Type**: filepath
**Severity**: informational
**Languages**: [python]
- Python bytecode and cache files
- Automatically generated
- Remediation: Add `__pycache__/` and `*.pyc` to .gitignore

### Go Vendor Directory
**Pattern**: `vendor/`
**Type**: filepath
**Severity**: medium
**Languages**: [go]
- Go vendor directory (unless using vendor mode)
- Remediation: Add `vendor/` to .gitignore if not vendoring

### Java Build Output
**Pattern**: `target/|\.class$`
**Type**: filepath
**Severity**: informational
**Languages**: [java]
- Maven/Gradle build output
- Remediation: Add `target/` to .gitignore

### Rust Build Output
**Pattern**: `target/|Cargo\.lock$`
**Type**: filepath
**Severity**: informational
**Languages**: [rust]
- Rust cargo build output
- Note: Cargo.lock should be committed for binaries, ignored for libraries
- Remediation: Add `target/` to .gitignore

### General Build Directories
**Pattern**: `dist/|build/|out/|\.build/`
**Type**: filepath
**Severity**: low
**Languages**: [all]
- Common build output directories
- Generated from source code
- Remediation: Add `dist/`, `build/` to .gitignore

---

## Log Files

### General Log Files
**Pattern**: `.*\.log$`
**Type**: filepath
**Severity**: medium
**Languages**: [all]
- Log files may contain sensitive runtime data
- Example: Database queries, user data, stack traces
- Remediation: Add `*.log` to .gitignore

### npm Debug Logs
**Pattern**: `npm-debug\.log.*`
**Type**: filepath
**Severity**: low
**Languages**: [javascript, typescript]
- npm error and debug output
- May contain system paths
- Remediation: Add `npm-debug.log*` to .gitignore

### Yarn Logs
**Pattern**: `yarn-error\.log$|yarn-debug\.log$`
**Type**: filepath
**Severity**: low
**Languages**: [javascript, typescript]
- Yarn package manager logs
- Remediation: Add `yarn-*.log` to .gitignore

---

## Coverage and Test Reports

### Code Coverage Reports
**Pattern**: `coverage/|\.coverage$|htmlcov/`
**Type**: filepath
**Severity**: low
**Languages**: [all]
- Test coverage report directories
- Generated from test runs
- Remediation: Add `coverage/` to .gitignore

### Jest Cache
**Pattern**: `\.jest/`
**Type**: filepath
**Severity**: low
**Languages**: [javascript, typescript]
- Jest test framework cache
- Remediation: Add `.jest/` to .gitignore

### pytest Cache
**Pattern**: `\.pytest_cache/`
**Type**: filepath
**Severity**: low
**Languages**: [python]
- pytest cache directory
- Remediation: Add `.pytest_cache/` to .gitignore

---

## Package Manager Lock Files (Contextual)

### Composer Lock
**Pattern**: `composer\.lock$`
**Type**: filepath
**Severity**: informational
**Languages**: [php]
- PHP dependency lock file
- Should be committed for applications, often ignored for libraries
- Note: Context-dependent

### Gemfile Lock
**Pattern**: `Gemfile\.lock$`
**Type**: filepath
**Severity**: informational
**Languages**: [ruby]
- Ruby dependency lock file
- Should be committed for applications
- Note: Context-dependent

---

## Temporary and Cache Files

### Temporary Files
**Pattern**: `.*\.tmp$|.*\.temp$|tmp/|temp/`
**Type**: filepath
**Severity**: informational
**Languages**: [all]
- Temporary files and directories
- Should never be committed
- Remediation: Add `*.tmp`, `*.temp`, `tmp/` to .gitignore

### Cache Directories
**Pattern**: `\.cache/|cache/`
**Type**: filepath
**Severity**: informational
**Languages**: [all]
- Cache directories
- Remediation: Add `.cache/` to .gitignore
