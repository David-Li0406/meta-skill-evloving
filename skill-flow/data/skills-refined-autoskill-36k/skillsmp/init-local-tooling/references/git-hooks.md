# Git Hooks with Lefthook

## Why Lefthook?

**Lefthook** is a fast, language-agnostic Git hooks manager.

**Advantages:**
- **Language-agnostic** - Works with any language (TS, Rust, Python, etc.)
- **Fast** - Written in Go, parallel execution
- **Simple** - Single YAML config file
- **No dependencies** - Just install via Homebrew or npm
- **CI-friendly** - Can skip hooks in CI
- **Better than Husky** - Faster, works across languages, easier config

---

## Installation

### Via Homebrew (Recommended)

```bash
brew install lefthook
```

### Via npm/pnpm (Per-project)

```bash
pnpm add -D lefthook
```

### Via Script

**Use the provided setup script:**
```bash
./scripts/setup_lefthook.sh
```

The script will:
1. Check if lefthook is installed
2. Check if it's up-to-date
3. Offer to install/update if needed
4. Generate lefthook.yml config
5. Install hooks

---

## Configuration

### lefthook.yml

**Complete configuration with all hooks:**

```yaml
# Lefthook configuration
# https://github.com/evilmartians/lefthook

# Skip hooks in CI
skip_output:
  - meta
  - summary

# Commit message validation
commit-msg:
  commands:
    commitlint:
      run: npx commitlint --edit {1}

# Pre-commit: Run on staged files only
pre-commit:
  parallel: true
  commands:
    # TypeScript/JavaScript linting
    eslint:
      glob: "*.{js,ts,jsx,tsx}"
      run: npx eslint --fix {staged_files}
      stage_fixed: true

    # Formatting (if using Prettier)
    prettier:
      glob: "*.{js,ts,jsx,tsx,json,md,css,scss}"
      run: npx prettier --write {staged_files}
      stage_fixed: true

    # Formatting (if using Biome)
    biome:
      glob: "*.{js,ts,jsx,tsx,json}"
      run: npx biome check --apply {staged_files}
      stage_fixed: true

    # Rust formatting
    rustfmt:
      glob: "*.rs"
      run: cargo fmt -- {staged_files}
      stage_fixed: true

    # Rust linting (on staged files)
    clippy:
      glob: "*.rs"
      run: cargo clippy --fix --allow-dirty --allow-staged -- -D warnings
      stage_fixed: true

    # Python formatting and linting
    ruff-format:
      glob: "*.py"
      run: ruff format {staged_files}
      stage_fixed: true

    ruff-check:
      glob: "*.py"
      run: ruff check --fix {staged_files}
      stage_fixed: true

    # Python type checking (staged files only)
    mypy:
      glob: "*.py"
      run: mypy {staged_files}

# Pre-push: Full validation before pushing
pre-push:
  parallel: false  # Run sequentially to catch issues early
  commands:
    # 1. Format check
    format-check:
      run: |
        npx prettier --check . || \
        cargo fmt -- --check || \
        ruff format --check .

    # 2. Lint everything
    lint:
      run: |
        npx eslint . --max-warnings 0 || \
        cargo clippy --all-targets -- -D warnings || \
        ruff check .

    # 3. Type checking
    type-check:
      run: |
        npx tsc --noEmit || \
        mypy .

    # 4. Run all tests
    test:
      run: |
        npm test || \
        cargo test || \
        pytest

    # 5. Build everything
    build:
      run: |
        npm run build || \
        cargo build --release

    # 6. Generate docs (optional)
    docs:
      run: |
        cargo doc --no-deps || true

# Post-commit: Notify or log (optional)
post-commit:
  commands:
    notify:
      run: echo "✅ Commit created successfully"
```

---

## Conventional Commits

### commitlint Configuration

**commitlint.config.js:**
```js
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation
        'style',    // Formatting
        'refactor', // Code restructuring
        'perf',     // Performance
        'test',     // Tests
        'chore',    // Maintenance
        'ci',       // CI/CD
        'build',    // Build system
        'revert',   // Revert commit
      ],
    ],
    'type-case': [2, 'always', 'lower-case'],
    'subject-case': [0],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 100],
  },
}
```

**Install commitlint:**
```bash
pnpm add -D @commitlint/cli @commitlint/config-conventional
```

**Valid commit messages:**
```
feat: add user authentication
fix: resolve memory leak in parser
docs: update API documentation
refactor: simplify error handling
test: add unit tests for validators
```

**Invalid commit messages:**
```
Added feature  ❌ No type
FEAT: something ❌ Type not lowercase
fix ❌ No subject
fix: Fix bug. ❌ Period at end
```

---

## Language-Specific Hooks

### TypeScript/JavaScript Only

```yaml
pre-commit:
  parallel: true
  commands:
    eslint:
      glob: "*.{js,ts,jsx,tsx}"
      run: npx eslint --fix {staged_files}
      stage_fixed: true

    prettier:
      glob: "*.{js,ts,jsx,tsx,json,md}"
      run: npx prettier --write {staged_files}
      stage_fixed: true

    type-check:
      glob: "*.{ts,tsx}"
      run: npx tsc --noEmit

pre-push:
  commands:
    validate:
      run: |
        npm run lint
        npm run type-check
        npm test
        npm run build
```

### Rust Only

```yaml
pre-commit:
  parallel: true
  commands:
    fmt:
      glob: "*.rs"
      run: cargo fmt -- {staged_files}
      stage_fixed: true

    clippy:
      glob: "*.rs"
      run: cargo clippy --fix --allow-dirty --allow-staged
      stage_fixed: true

pre-push:
  commands:
    check:
      run: |
        cargo fmt -- --check
        cargo clippy --all-targets -- -D warnings
        cargo test
        cargo build --release
```

### Python Only

```yaml
pre-commit:
  parallel: true
  commands:
    ruff-format:
      glob: "*.py"
      run: ruff format {staged_files}
      stage_fixed: true

    ruff-check:
      glob: "*.py"
      run: ruff check --fix {staged_files}
      stage_fixed: true

    mypy:
      glob: "*.py"
      run: mypy {staged_files}

pre-push:
  commands:
    validate:
      run: |
        ruff format --check .
        ruff check .
        mypy .
        pytest
```

---

## Monorepo Configuration

### With Nx

```yaml
pre-commit:
  parallel: true
  commands:
    affected-lint:
      run: nx affected --target=lint --fix
      stage_fixed: true

    affected-format:
      run: nx format:write --uncommitted
      stage_fixed: true

pre-push:
  commands:
    affected-test:
      run: nx affected --target=test

    affected-build:
      run: nx affected --target=build
```

### Mixed Languages

```yaml
pre-commit:
  parallel: true
  commands:
    # TypeScript
    ts-format:
      glob: "*.{js,ts,jsx,tsx}"
      run: npx biome check --apply {staged_files}
      stage_fixed: true

    # Rust
    rs-format:
      glob: "*.rs"
      run: cargo fmt -- {staged_files}
      stage_fixed: true

    # Python
    py-format:
      glob: "*.py"
      run: ruff format {staged_files} && ruff check --fix {staged_files}
      stage_fixed: true

pre-push:
  commands:
    # Run all language validators
    validate-all:
      run: ./scripts/validate_all.sh
```

---

## Advanced Features

### Conditional Execution

**Skip hook for specific branches:**
```yaml
pre-push:
  exclude_refs:
    - refs/heads/main
    - refs/heads/develop
  commands:
    test:
      run: npm test
```

**Run only on specific branches:**
```yaml
pre-push:
  include_refs:
    - refs/heads/feature/*
  commands:
    extended-tests:
      run: npm run test:e2e
```

### Skip Patterns

**Skip hooks for specific files:**
```yaml
pre-commit:
  commands:
    eslint:
      glob: "*.{js,ts}"
      exclude: "*.config.js"
      run: npx eslint --fix {staged_files}
```

### Environment Variables

```yaml
pre-commit:
  commands:
    custom:
      run: |
        export NODE_ENV=test
        npm run custom-script
```

### Interactive Prompts

```yaml
pre-push:
  commands:
    confirm:
      run: |
        read -p "Run full test suite? (y/n) " -n 1 -r
        if [[ $REPLY =~ ^[Yy]$ ]]; then
          npm test
        fi
```

---

## Installation and Management

### Install Hooks

**After cloning repository:**
```bash
lefthook install
```

This creates `.git/hooks/` scripts that call lefthook.

### Uninstall Hooks

```bash
lefthook uninstall
```

### Update Lefthook

**Via Homebrew:**
```bash
brew upgrade lefthook
```

**Via npm:**
```bash
pnpm update lefthook
```

### Skip Hooks Temporarily

**Skip all hooks:**
```bash
LEFTHOOK=0 git commit -m "message"
```

**Skip specific hook:**
```bash
LEFTHOOK_EXCLUDE=test git push
```

**Skip in CI:**
```yaml
# .github/workflows/ci.yml
env:
  LEFTHOOK: 0
```

---

## Debugging

### Verbose Output

```bash
lefthook run pre-commit --verbose
```

### Dry Run

```bash
lefthook run pre-commit --no-tty
```

### Test Hook Manually

```bash
lefthook run pre-commit
```

### Check Configuration

```bash
lefthook dump
```

Shows parsed configuration and which commands would run.

---

## Integration with CI

### Skip in CI

**In workflow file:**
```yaml
env:
  CI: true
  LEFTHOOK: 0
```

**Or in lefthook.yml:**
```yaml
skip_output:
  - meta
  - summary

pre-commit:
  skip:
    - merge
    - rebase
  commands:
    lint:
      run: npm run lint
```

### Run Same Checks in CI

**Don't skip - run same validation:**

```yaml
# .github/workflows/ci.yml
- name: Run pre-push checks
  run: lefthook run pre-push
```

This ensures local and CI checks are identical.

---

## Best Practices

1. **Keep pre-commit fast** - Only lint/format staged files
2. **Full validation in pre-push** - Run comprehensive tests
3. **Use parallel execution** - For independent tasks
4. **Stage fixed files** - Auto-add formatted files
5. **Enforce conventional commits** - Use commitlint
6. **Document skipping** - Tell users about LEFTHOOK=0
7. **Share config** - Commit lefthook.yml to repo
8. **Test hooks** - Run `lefthook run` manually to test
9. **Match CI** - Use same commands in CI as pre-push
10. **Language-specific globs** - Only run relevant tools

---

## Migration from Husky

**Husky:**
```json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged",
      "pre-push": "npm test"
    }
  }
}
```

**Lefthook equivalent:**
```yaml
pre-commit:
  commands:
    lint-staged:
      run: npx lint-staged

pre-push:
  commands:
    test:
      run: npm test
```

**Benefits:**
- Faster execution
- YAML configuration
- Better parallel support
- Language-agnostic

---

## Quick Reference

**Installation:**
```bash
brew install lefthook
lefthook install
```

**Skip hooks:**
```bash
LEFTHOOK=0 git commit
LEFTHOOK_EXCLUDE=test git push
```

**Test hooks:**
```bash
lefthook run pre-commit
lefthook run pre-push
```

**Debug:**
```bash
lefthook dump
lefthook run pre-commit --verbose
```

**Update:**
```bash
brew upgrade lefthook
pnpm update lefthook
```
