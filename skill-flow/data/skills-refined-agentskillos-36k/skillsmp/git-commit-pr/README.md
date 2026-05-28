# Skill : Git Commit & Pull Request

Ce skill guide la création de commits bien formatés, le push vers origin et la création de Pull Requests documentées.

## Description

Le skill `git-commit-pr` fournit un workflow complet pour :
- Créer des commits selon les **Conventional Commits**
- Gérer le staging de fichiers de manière sécurisée
- Pousser vers origin avec retry automatique
- Créer des Pull Requests bien documentées via `gh` CLI
- Suivre les bonnes pratiques Git

## Requirements

### Git
- **Git** : Version 2.x ou supérieur
- Dépôt Git initialisé
- Remote `origin` configuré

### GitHub CLI (pour PRs)
- **gh CLI** : Latest version
- Authentification GitHub configurée (`gh auth login -h github.com --web`)
  - Utilise le device flow avec code à 6 caractères
  - Ouvrir https://github.com/login/device pour autoriser

### Optionnel
- **Pre-commit hooks** : Pour validation automatique
- **Conventional Commits linter** : commitlint (optionnel)

### Compatibilité
- Linux, macOS, Windows (avec Git Bash)
- Fonctionne avec GitHub, GitLab, Bitbucket (gh CLI requis pour GitHub)

## Structure

```
git-commit-pr/
├── SKILL.md                    # Instructions principales du skill
├── README.md                   # Ce fichier
├── CHANGELOG.md                # Historique des versions
└── references/                 # Documentation de référence
    ├── PR_TEMPLATE.md          # Template de Pull Request
    ├── COMMIT_EXAMPLES.md      # Exemples de commits
    └── GIT_WORKFLOW.md         # Workflow Git détaillé
```

## Utilisation

### Pour l'agent

L'agent peut utiliser ce skill automatiquement lorsqu'il détecte :
- Une demande de commit
- Une demande de push
- Une demande de création de PR
- "Commit et push ces changements"
- "Créer une PR pour..."

Le skill fournit :
- Format de commit Conventional Commits
- Validation pré-commit
- Templates de PR documentés
- Gestion automatique des retries réseau

### Pour l'utilisateur

#### Workflow simple

```bash
# L'agent exécutera automatiquement :
1. git status && git diff HEAD
2. git add <fichiers-spécifiques>
3. git commit -m "type(scope): description"
4. git push -u origin branch
5. gh pr create --title "..." --body "..."
```

#### Demandes typiques

**Créer un commit** :
> "Commit ces changements avec un message approprié"

**Commit et push** :
> "Commit et push sur origin"

**Créer une PR** :
> "Crée une PR bien documentée pour ces changements"

**Workflow complet** :
> "Commit, push et crée une PR"

## Workflow en 5 Étapes

### 1. Vérification pré-commit
- `git status` : État des fichiers
- `git diff HEAD` : Changements à commiter
- `git log --oneline -10` : Historique récent

### 2. Staging sécurisé
- Préférer `git add <fichier>` plutôt que `git add .`
- Vérifier qu'aucun fichier sensible n'est staged (.env, credentials)

### 3. Commit formaté
Format Conventional Commits :
```
type(scope): description

[body optionnel]

[footer optionnel]
[session URL]
```

Types : `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### 4. Push avec retry
```bash
git push -u origin branch-name
# Retry automatique sur échec réseau (4 tentatives max)
```

### 5. Pull Request documentée
Template complet avec :
- **Summary** : Résumé en bullets
- **Changes** : Added, Changed, Fixed, Removed
- **Type of Change** : Checklist
- **Testing** : Tests effectués
- **Session URL** : Lien Claude

## Exemples de Commits

### Feature
```bash
git commit -m "feat(auth): add OAuth2 login support"
```

### Bug Fix
```bash
git commit -m "fix(api): handle null response in user endpoint"
```

### Documentation
```bash
git commit -m "docs(readme): update installation instructions"
```

### Breaking Change
```bash
git commit -m "$(cat <<'EOF'
feat(api)!: change user endpoint response format

BREAKING CHANGE: Response now returns { data: User[] }
instead of User[] directly.

https://claude.ai/code/session_XXX
EOF
)"
```

## Exemples de PRs

### Feature PR
```markdown
## Summary
- Add OAuth2 authentication
- Support Google and GitHub providers
- Include token refresh mechanism

## Changes
### Added
- OAuth2Service class
- Google/GitHub provider configs
- Token refresh endpoint

## Type of Change
- [x] New feature

## Testing
- [x] Unit tests pass
- [x] Integration tests with Google
- [x] Manual testing completed
```

### Bug Fix PR
```markdown
## Summary
- Fix null pointer exception in user endpoint
- Add defensive null checks

## Changes
### Fixed
- Null handling in /api/users/:id
- Added validation for empty responses

## Type of Change
- [x] Bug fix

## Testing
- [x] Regression tests added
- [x] All tests pass
```

## Bonnes Pratiques

### ✅ À FAIRE
1. Vérifier avec `git status` avant commit
2. Commits atomiques (1 changement logique = 1 commit)
3. Messages descriptifs suivant Conventional Commits
4. Ajouter fichiers spécifiques (pas `git add .` sans vérification)
5. Inclure session URL Claude dans commits et PRs
6. Analyser TOUS les commits de la branche pour la PR
7. Tester avant de créer la PR

### ❌ À ÉVITER
1. Messages vagues : "fix", "update", "WIP"
2. Commits massifs (50+ fichiers)
3. Commiter des secrets (.env, credentials)
4. `git push --force` sur main/master
5. PRs sans description
6. Oublier de vérifier `git diff` avant commit

## Gestion des Erreurs

### Hook pre-commit échoue
1. Corriger le problème (linting, tests)
2. Re-stage les fichiers
3. Créer un **nouveau commit** (pas `--amend`)

### Push échoue (réseau)
- Retry automatique : 4 tentatives avec backoff (2s, 4s, 8s, 16s)

### gh CLI non authentifié ou token invalide

**Symptômes** :
- `HTTP 401: Bad credentials`
- `Failed to log in to github.com`
- `The token in /root/.config/gh/hosts.yml is invalid`

**Solution** :
```bash
# Vérifier le statut
gh auth status

# Ré-authentifier avec device flow
gh auth login -h github.com --web

# Le CLI affichera un code à 6 caractères (ex: 523C-8D88)
# Ouvrir https://github.com/login/device
# Entrer le code et autoriser
```

### Remote Git non reconnu par gh

**Symptôme** :
- `none of the git remotes configured for this repository point to a known GitHub host`

**Solution** : Utiliser `--repo` explicitement
```bash
gh pr create --repo owner/repo --head branch --base main --title "..." --body "..."
```

### API GitHub temporairement indisponible

**Symptôme** :
- `HTTP 503: Service Unavailable`

**Solution** : Attendre et réessayer
```bash
sleep 3
gh pr create --repo owner/repo --head branch --base main --title "..." --body "..."
```

### Branche de base incorrecte
```bash
gh pr create --base develop --title "..." --body "..."
```

## Références

### Documentation externe
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [Keep a Changelog](https://keepachangelog.com/)

### Documentation interne
- `references/PR_TEMPLATE.md` : Template complet de PR
- `references/COMMIT_EXAMPLES.md` : Exemples de commits variés
- `references/GIT_WORKFLOW.md` : Workflow détaillé

### Skills connexes
- `build-chatwindow` : Pour commits de widgets
- `configure-mcp-server` : Pour commits de configuration MCP

## Auteur

somtech-pack

## Version

1.0.0 — Voir [CHANGELOG.md](./CHANGELOG.md) pour l'historique des versions
