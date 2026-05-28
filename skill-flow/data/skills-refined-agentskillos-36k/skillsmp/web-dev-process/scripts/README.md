# Scripts de Validation

Ce dossier contient des scripts pour automatiser la vérification et l'initialisation de projets selon le process de développement.

## Scripts Disponibles

### `check-process.js`

Vérifie qu'un projet respecte les standards du process.

```bash
node .web-agency/skills/web-dev-process/scripts/check-process.js

# Options
--fix     # Tente de corriger automatiquement
--strict  # Échoue aussi sur les warnings
--quiet   # Affiche uniquement les erreurs
```

**Vérifie :**
- Présence des fichiers requis (README, package.json, .gitignore)
- Configuration des outils (ESLint, Prettier, TypeScript)
- Git hooks
- Scripts dans package.json

### `init-project.js`

Initialise un projet avec tous les standards du process.

```bash
node .web-agency/skills/web-dev-process/scripts/init-project.js

# Options
--force      # Écrase les fichiers existants
--minimal    # Installe uniquement l'essentiel
--skip-deps  # Ne pas installer les dépendances npm
```

**Actions :**
1. Copie les fichiers de configuration
2. Copie les templates GitHub
3. Ajoute les scripts npm
4. Installe les dépendances de dev
5. Configure les hooks Git

### `audit-project.js`

Effectue un audit complet du projet.

```bash
node .web-agency/skills/web-dev-process/scripts/audit-project.js

# Options
--json     # Sortie au format JSON
--ci       # Mode CI (exit codes stricts)
--no-deps  # Ignorer l'audit des dépendances
```

**Catégories auditées :**
- Conformité au process (30%)
- Qualité du code (30%)
- Tests (20%)
- Documentation (10%)
- Sécurité (10%)

## Utilisation en CI

Ajoutez à votre workflow GitHub Actions :

```yaml
name: Audit

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install

      - name: Check process compliance
        run: node .web-agency/skills/web-dev-process/scripts/check-process.js --strict

      - name: Run full audit
        run: node .web-agency/skills/web-dev-process/scripts/audit-project.js --ci
```

## Intégration NPM

Ajoutez ces scripts à votre `package.json` :

```json
{
  "scripts": {
    "process:check": "node .web-agency/skills/web-dev-process/scripts/check-process.js",
    "process:init": "node .web-agency/skills/web-dev-process/scripts/init-project.js",
    "process:audit": "node .web-agency/skills/web-dev-process/scripts/audit-project.js"
  }
}
```

## Exit Codes

| Code | Signification |
|------|---------------|
| 0 | Succès |
| 1 | Échec de validation |
| 2 | Vulnérabilités critiques (audit) |
