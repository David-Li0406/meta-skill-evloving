---
name: quality-tools-orchestrator
description: Orchestrateur pour la configuration des outils de qualité de code
workflows:
  - name: wf-creation
    step: Brief
---

# Orchestrateur Outils de Qualité

Ce module coordonne la mise en place des outils de qualité de code.

## Agents Spécialisés

| Agent | Responsabilité |
|-------|----------------|
| `linting.md` | ESLint, Stylelint |
| `formatting.md` | Prettier, EditorConfig |
| `git-hooks.md` | Husky, Lefthook, lint-staged |
| `commit-conventions.md` | Commitlint, conventional commits |

## Tu NE fais PAS

- ❌ Installer les outils → devops
- ❌ Configurer les pipelines → devops
- ❌ Définir les standards → direction-technique, lead-dev
- ❌ Écrire du code applicatif → frontend-developer, backend-developer

## Stack Recommandée

```
┌─────────────────────────────────────────────────────────┐
│                    GIT HOOKS                            │
│                   (Husky/Lefthook)                      │
├─────────────────────────────────────────────────────────┤
│  pre-commit         │  commit-msg         │  pre-push   │
│  ├── lint-staged    │  └── commitlint     │  └── tests  │
│  │   ├── ESLint     │                     │             │
│  │   ├── Prettier   │                     │             │
│  │   └── Stylelint  │                     │             │
└─────────────────────────────────────────────────────────┘
```

## Installation Rapide

```bash
# Linting & Formatting
npm install -D eslint @eslint/js typescript-eslint prettier eslint-config-prettier

# CSS
npm install -D stylelint stylelint-config-standard

# Git Hooks
npm install -D husky lint-staged @commitlint/cli @commitlint/config-conventional

# Setup
npx husky init
```

## Scripts Recommandés

```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "check": "npm run lint && npm run format:check",
    "fix": "npm run lint:fix && npm run format",
    "prepare": "husky"
  }
}
```

## Workflow d'Utilisation

1. **Développeur modifie du code**
2. **`git commit`** → pre-commit hook
   - lint-staged exécute ESLint + Prettier sur fichiers modifiés
3. **Message de commit** → commit-msg hook
   - Commitlint valide le format
4. **`git push`** → pre-push hook (optionnel)
   - Tests et typecheck

## Exemples de Configuration

### ESLint (Flat Config)

```javascript
// eslint.config.js
import js from '@eslint/js';
import typescript from 'typescript-eslint';
import prettier from 'eslint-config-prettier';

export default [
  js.configs.recommended,
  ...typescript.configs.recommended,
  prettier,
  {
    rules: {
      'no-console': 'warn',
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': 'error',
    },
    ignores: ['dist/', 'node_modules/', '.next/'],
  },
];
```

### Prettier

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

### lint-staged

```javascript
// lint-staged.config.js
export default {
  '*.{js,jsx,ts,tsx}': ['eslint --fix', 'prettier --write'],
  '*.{css,scss}': ['stylelint --fix', 'prettier --write'],
  '*.{json,md}': ['prettier --write'],
};
```

### Lefthook (Alternative à Husky)

```yaml
# lefthook.yml
pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{js,ts,tsx}"
      run: npx eslint --fix {staged_files}
    format:
      glob: "*.{js,ts,tsx,json,md}"
      run: npx prettier --write {staged_files}

commit-msg:
  commands:
    validate:
      run: npx commitlint --edit {1}
```

## Bonnes Pratiques

| Pratique | Raison |
|----------|--------|
| Utiliser lint-staged | Ne linter que les fichiers modifiés (rapidité) |
| Parallel hooks | Exécuter ESLint et Prettier en parallèle |
| Auto-fix en pre-commit | Corriger automatiquement les erreurs simples |
| Commitlint obligatoire | Garantir un historique git propre |
| EditorConfig | Assurer la cohérence entre éditeurs |
| CI/CD backup | Vérifier aussi en CI (au cas où hooks contournés) |

## Erreurs Courantes

| Erreur | Solution |
|--------|----------|
| Hooks pas exécutés | `npx husky init` ou `npx lefthook install` |
| Conflits ESLint/Prettier | Utiliser `eslint-config-prettier` |
| Lint trop lent | Utiliser lint-staged (fichiers staged uniquement) |
| Commits bloqués | `git commit --no-verify` (à éviter) |

## Agents à Consulter

- Pour le détail ESLint/Stylelint → `linting.md`
- Pour Prettier/EditorConfig → `formatting.md`
- Pour Husky/Lefthook → `git-hooks.md`
- Pour Commitlint → `commit-conventions.md`

## Livrables

| Livrable | Description |
|----------|-------------|
| Quality Tools Configuration | Configuration complète de tous les outils de qualité |
| Pre-commit Setup | Setup complet des checks pre-commit |
| Quality Scripts | Scripts npm pour vérifier la qualité du code |
| CI Quality Check | Job CI pour backup des vérifications locales |
