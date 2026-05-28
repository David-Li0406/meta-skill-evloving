# Configurations Standard

Ce dossier contient les fichiers de configuration prêts à l'emploi pour imposer les standards du process de développement.

## Utilisation

Copiez les fichiers nécessaires à la racine de votre projet :

```bash
# Copier tous les configs (depuis la racine du projet)
cp -r .web-agency/skills/web-dev-process/configs/{.prettierrc,.prettierignore,.editorconfig} .
cp .web-agency/skills/web-dev-process/configs/eslint.config.js .
cp .web-agency/skills/web-dev-process/configs/commitlint.config.js .
cp .web-agency/skills/web-dev-process/configs/lefthook.yml .
```

## Fichiers disponibles

| Fichier | Description | Dépendances |
|---------|-------------|-------------|
| `.prettierrc` | Configuration Prettier | `prettier` |
| `.prettierignore` | Fichiers ignorés par Prettier | - |
| `.editorconfig` | Configuration cross-IDE | - |
| `eslint.config.js` | ESLint flat config | `eslint`, `@eslint/js`, `globals` |
| `commitlint.config.js` | Validation des commits | `@commitlint/cli`, `@commitlint/config-conventional` |
| `lefthook.yml` | Git hooks | `lefthook` |
| `lint-staged.config.js` | Alternative aux hooks | `lint-staged`, `husky` |
| `tsconfig.base.json` | TypeScript base config | `typescript` |

## Installation des dépendances

```bash
# Core
pnpm add -D prettier eslint @eslint/js globals typescript

# Commit linting
pnpm add -D @commitlint/cli @commitlint/config-conventional

# Git hooks (choisir UNE option)
# Option A: Lefthook (recommandé)
pnpm add -D lefthook
pnpm lefthook install

# Option B: Husky + lint-staged
pnpm add -D husky lint-staged
pnpm husky init
echo "pnpm lint-staged" > .husky/pre-commit
```

## Configuration par stack

### React / Next.js

```bash
pnpm add -D eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y
```

### Vue / Nuxt

```bash
pnpm add -D eslint-plugin-vue vue-eslint-parser
```

### Node.js / Backend

```bash
pnpm add -D eslint-plugin-n eslint-plugin-security
```

## Scripts package.json

Ajoutez ces scripts à votre `package.json` :

```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "typecheck": "tsc --noEmit",
    "prepare": "lefthook install"
  }
}
```

## Personnalisation

Ces configs sont des bases recommandées. Adaptez-les selon les besoins de votre projet :

1. **ESLint** : Ajoutez les plugins spécifiques à votre framework
2. **Prettier** : Ajustez les règles de formatage selon vos préférences d'équipe
3. **TypeScript** : Étendez `tsconfig.base.json` avec vos paths spécifiques
4. **Lefthook** : Activez/désactivez les hooks selon votre workflow
