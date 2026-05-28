# Utility Scripts

Helper scripts for managing Multi-Repo Workspace configurations.

## auto-generate-config.js

Automatically generates `.claude/config.json` and `.claude/context.md` for a repository.

### Usage

```bash
node auto-generate-config.js /path/to/repository
```

### Options

- `--force`: Overwrite existing configuration

### Example

```bash
# Generate config for a repository
node auto-generate-config.js ~/projects/my-app/frontend

# Overwrite existing config
node auto-generate-config.js ~/projects/my-app/frontend --force
```

### What it does

1. Detects repository type (frontend, backend, mobile, etc.)
2. Identifies tech stack from package.json, requirements.txt, etc.
3. Detects code style from ESLint/Prettier configs
4. Extracts npm scripts
5. Generates `.claude/config.json`
6. Creates `.claude/context.md` template

### Detection Logic

**Repository Types:**
- **Frontend**: React, Vue, Angular in dependencies
- **Backend**: Express, Fastify, NestJS, or Python/Go/Rust files
- **Mobile**: React Native, Expo dependencies
- **DevOps**: Docker, Terraform, GitHub Actions
- **Shared**: Has exports in package.json

**Tech Stack:**
- Reads package.json dependencies
- Checks for Python requirements.txt
- Checks for Go go.mod
- Checks for Rust Cargo.toml

**Code Style:**
- Reads .eslintrc.json for Airbnb/Google/Standard
- Checks for .prettierrc

---

## validate-workspace.js

Validates workspace configuration and repository setups.

### Usage

```bash
node validate-workspace.js [workspace-path]
```

### Example

```bash
# Validate current directory
node validate-workspace.js

# Validate specific workspace
node validate-workspace.js ~/projects/my-workspace
```

### What it checks

**Workspace Level:**
- ✅ `.workspace/config.json` exists
- ✅ Valid JSON syntax
- ✅ Required fields present
- ✅ Repository paths exist

**Repository Level:**
- ✅ `.claude/config.json` exists
- ✅ `.claude/context.md` exists
- ✅ Valid JSON syntax
- ✅ Required fields present
- ✅ Repository type specified
- ✅ Tech stack defined

**Dependencies:**
- ✅ Internal dependencies reference existing repos
- ⚠️  Warns about missing dependencies

### Output

```
🔍 Validating workspace...

============================================================
VALIDATION RESULTS
============================================================

ℹ️  INFO:
   Found workspace: my-project
   Repositories defined: 3
   ✓ Repository found: frontend (frontend)
   ✓ Repository found: backend (backend)
   ✓ Repository found: shared (shared)

⚠️  WARNINGS:
   Missing .claude/context.md in shared

❌ ERRORS:
   (none)

============================================================
⚠️  Workspace validation passed with warnings
============================================================

Summary:
  Errors: 0
  Warnings: 1
  Info: 4
```

### Exit Codes

- `0`: Validation passed (no errors)
- `1`: Validation failed (has errors)

---

## Making Scripts Executable

```bash
chmod +x auto-generate-config.js
chmod +x validate-workspace.js
```

Then run directly:

```bash
./auto-generate-config.js /path/to/repo
./validate-workspace.js
```

---

## Integration with CI/CD

### GitHub Actions

```yaml
name: Validate Workspace

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Validate workspace configuration
        run: node scripts/validate-workspace.js
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

node scripts/validate-workspace.js
if [ $? -ne 0 ]; then
  echo "Workspace validation failed. Fix errors before committing."
  exit 1
fi
```

---

## Future Scripts

Planned utility scripts:

- `sync-dependencies.js`: Sync dependency versions across repos
- `generate-graph.js`: Generate visual dependency graph
- `check-consistency.js`: Check for convention inconsistencies
- `migrate-config.js`: Migrate old config format to new version
- `export-workspace.js`: Export workspace summary for documentation
