# Migration Guide: vercel-env-sync v1 → v2

## Overview

La skill `vercel-env-sync` ha sido completamente rediseñada siguiendo el estándar [VS Code Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) y las mejores prácticas de Vercel CLI 33+.

## 🔄 What Changed

### Structure

**v1 (Old)**:

```
scripts/
├── check-vercel-env.sh     # ❌ Fuera de skill directory
├── sync-vercel-env.sh
└── audit-vercel-env.sh

.github/skills/vercel-env-sync/
└── SKILL.md                # Solo documentación
```

**v2 (New)**:

```
.github/skills/vercel-env-sync/
├── SKILL.md                # ✅ Con YAML frontmatter
├── scripts/
│   ├── env-push.sh        # ✅ Dentro de skill (renombrado)
│   ├── env-pull.sh        # ✅ Nuevo
│   └── env-audit.sh       # ✅ Renombrado
└── lib/
    └── env-functions.sh   # ✅ Funciones compartidas
```

### Scripts Renamed

| Old                           | New                                                   | Why                                         |
| ----------------------------- | ----------------------------------------------------- | ------------------------------------------- |
| `scripts/sync-vercel-env.sh`  | `.github/skills/vercel-env-sync/scripts/env-push.sh`  | Más descriptivo, sigue convención de verbos |
| `scripts/audit-vercel-env.sh` | `.github/skills/vercel-env-sync/scripts/env-audit.sh` | Nombre más corto, dentro de skill           |
| `scripts/check-vercel-env.sh` | _Removido_                                            | Funcionalidad incluida en `env-audit.sh`    |

### New Commands

```bash
# v1 (Old)
./scripts/sync-vercel-env.sh --all-envs

# v2 (New) - Must run from skill directory
cd .github/skills/vercel-env-sync
./scripts/env-push.sh --all-envs

# Or from project root
.github/skills/vercel-env-sync/scripts/env-push.sh --all-envs
```

### Vercel CLI Commands

**Deprecated (v1)**:

```bash
# ❌ Old way: rm + add
vercel env rm VAR production --yes
echo "value" | vercel env add VAR production
```

**Modern (v2)**:

```bash
# ✅ New way: update (Vercel CLI 33+)
printf "%s\n" "value" | vercel env update VAR production --yes

# ✅ With sensitive flag
printf "%s\n" "value" | vercel env update VAR production --sensitive --yes
```

## 📦 New Features in v2

### 1. Shared Function Library

```bash
# Source shared functions
source .github/skills/vercel-env-sync/lib/env-functions.sh

# Use in scripts or terminal
vercel::env::health_check
vercel::env::is_sensitive "DATABASE_URL"  # Returns 0 (true)
vercel::env::validate_value "BETTER_AUTH_SECRET" "short"  # Fails validation
```

### 2. Auto-Sensitive Detection

Variables automáticamente marcadas como `--sensitive`:

- `DATABASE_URL`, `*_SECRET`, `*_KEY`, `*_TOKEN`, `*_PASSWORD`, `PRIVATE_*`

```bash
# v1: Manual
echo "value" | vercel env add DATABASE_URL production

# v2: Auto-detected
echo "value" | vercel env add DATABASE_URL production --sensitive
```

### 3. Dry-Run Mode

```bash
# Preview changes without applying
./scripts/env-push.sh --all-envs --dry-run

# Output shows what WOULD happen:
# [DRY RUN] crear DATABASE_URL en production [SENSITIVE]
# [DRY RUN] actualizar BETTER_AUTH_SECRET en preview [SENSITIVE]
```

### 4. Automatic Backups

```bash
# v1: Manual backup
vercel env pull .env.backup.$(date +%Y%m%d)

# v2: Automatic before modifications
./scripts/env-push.sh --all-envs
# Creates:
#   .env.backup.production.20260114_153022
#   .env.backup.preview.20260114_153022
#   .env.backup.development.20260114_153022
```

### 5. Pull from Vercel (NEW)

```bash
# Download Vercel vars to local file
./scripts/env-pull.sh --env production --output .env.local

# With Git branch support
./scripts/env-pull.sh --env preview --branch feature-auth
```

### 6. JSON Output for CI/CD

```bash
# Generate machine-readable report
./scripts/env-audit.sh --json > audit.json

# Parse with jq
jq '.local_vars[] | select(.environments.production == false)' audit.json
```

### 7. Value Validation

```bash
# v1: No validation

# v2: Automatic validation
./scripts/env-push.sh
# ❌ BETTER_AUTH_SECRET debe tener al menos 32 caracteres
# ❌ DATABASE_URL debe ser una conexión PostgreSQL válida
# ⚠️  API_URL debería ser una URL válida (http:// o https://)
```

## 🚀 Migration Steps

### Step 1: Backup Old Scripts

```bash
mkdir -p scripts/backup
mv scripts/check-vercel-env.sh scripts/backup/
mv scripts/sync-vercel-env.sh scripts/backup/
mv scripts/audit-vercel-env.sh scripts/backup/
```

### Step 2: Make New Scripts Executable

```bash
chmod +x .github/skills/vercel-env-sync/scripts/*.sh
chmod +x .github/skills/vercel-env-sync/lib/*.sh
```

### Step 3: Test Health Check

```bash
cd .github/skills/vercel-env-sync
source lib/env-functions.sh
vercel::env::health_check
```

Expected output:

```
🏥 Verificación de salud...

  ✓ Vercel CLI instalado
  ✓ Autenticado como: melosdev
  ✓ Proyecto vinculado: wispy-poetry-52762475
  ✓ .env.example existe (4 variables)

✅ Configuración OK
```

### Step 4: Run Audit

```bash
./scripts/env-audit.sh
```

### Step 5: Sync Variables (Dry-Run First)

```bash
# Preview changes
./scripts/env-push.sh --all-envs --dry-run

# Apply if looks good
./scripts/env-push.sh --all-envs
```

### Step 6: Update CI/CD Pipelines

**Before**:

```yaml
- name: Sync Environment Variables
  run: ./scripts/sync-vercel-env.sh --all-envs
```

**After**:

```yaml
- name: Sync Environment Variables
  run: |
    cd .github/skills/vercel-env-sync
    chmod +x scripts/*.sh lib/*.sh
    ./scripts/env-push.sh --all-envs
```

### Step 7: Update Documentation References

Find and replace in documentation:

- `scripts/sync-vercel-env.sh` → `.github/skills/vercel-env-sync/scripts/env-push.sh`
- `scripts/audit-vercel-env.sh` → `.github/skills/vercel-env-sync/scripts/env-audit.sh`
- `scripts/check-vercel-env.sh` → `.github/skills/vercel-env-sync/scripts/env-audit.sh`

### Step 8: Clean Up (Optional)

```bash
# After verifying everything works
rm -rf scripts/backup
rm -rf scripts/  # If only had Vercel scripts
```

## 🔧 Breaking Changes

### 1. Working Directory

**v1**: Scripts could run from any directory

```bash
./scripts/sync-vercel-env.sh  # Works from project root
```

**v2**: Scripts use relative paths, recommended to run from skill directory

```bash
cd .github/skills/vercel-env-sync
./scripts/env-push.sh

# Or use absolute path
.github/skills/vercel-env-sync/scripts/env-push.sh
```

### 2. Function Names

If you imported functions from old scripts:

**v1** (if you had custom functions):

```bash
source scripts/sync-vercel-env.sh
get_env_value "DATABASE_URL"
```

**v2** (namespaced):

```bash
source .github/skills/vercel-env-sync/lib/env-functions.sh
vercel::env::get_local_value "DATABASE_URL"
```

### 3. Script Names in Shell History

Update your bash/zsh aliases:

```bash
# ~/.bashrc or ~/.zshrc

# Old
alias vercel-sync="./scripts/sync-vercel-env.sh --all-envs"

# New
alias vercel-sync="cd .github/skills/vercel-env-sync && ./scripts/env-push.sh --all-envs && cd -"
alias vercel-audit="cd .github/skills/vercel-env-sync && ./scripts/env-audit.sh && cd -"
alias vercel-pull="cd .github/skills/vercel-env-sync && ./scripts/env-pull.sh && cd -"
```

## 📊 Command Mapping

| v1 Command                      | v2 Command                         | Notes                      |
| ------------------------------- | ---------------------------------- | -------------------------- |
| `./scripts/check-vercel-env.sh` | `./scripts/env-audit.sh`           | Functionality merged       |
| `./scripts/sync-vercel-env.sh`  | `./scripts/env-push.sh`            | Renamed, added features    |
| `./scripts/audit-vercel-env.sh` | `./scripts/env-audit.sh`           | Renamed                    |
| _N/A_                           | `./scripts/env-pull.sh`            | **NEW** - Pull from Vercel |
| `vercel env add`                | `vercel env update` (for existing) | Modern Vercel CLI          |

## ✅ Verification Checklist

- [ ] Old scripts backed up
- [ ] New scripts executable (`chmod +x`)
- [ ] Health check passes
- [ ] Audit shows correct status
- [ ] Dry-run works
- [ ] Actual sync works
- [ ] CI/CD pipeline updated
- [ ] Documentation updated
- [ ] Team notified of changes
- [ ] Old scripts removed (optional)

## 🆘 Rollback Plan

If you need to rollback to v1:

```bash
# Restore old scripts
mv scripts/backup/* scripts/

# Make executable
chmod +x scripts/*.sh

# Verify
./scripts/audit-vercel-env.sh
```

## 📚 Resources

- [SKILL.md](./SKILL.md) - Complete v2 documentation
- [VS Code Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Vercel CLI Docs](https://vercel.com/docs/cli)
- [env-functions.sh](./lib/env-functions.sh) - Function reference

---

**Migration Date**: January 14, 2026  
**Version**: v2.0  
**Breaking Changes**: Yes (paths, commands)  
**Rollback Available**: Yes (backup old scripts)
