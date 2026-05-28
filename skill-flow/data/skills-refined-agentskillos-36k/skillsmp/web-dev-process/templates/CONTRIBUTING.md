# Guide de Contribution

Merci de votre intérêt pour contribuer à ce projet ! Ce guide vous aidera à démarrer.

## Table des Matières

- [Code de Conduite](#code-de-conduite)
- [Comment Contribuer](#comment-contribuer)
- [Processus de Développement](#processus-de-développement)
- [Standards de Code](#standards-de-code)
- [Commits](#commits)
- [Pull Requests](#pull-requests)
- [Review](#review)

## Code de Conduite

En contribuant, vous acceptez de respecter notre code de conduite :

- Soyez respectueux et inclusif
- Acceptez les critiques constructives
- Concentrez-vous sur ce qui est le mieux pour la communauté

## Comment Contribuer

### Signaler un Bug

1. Vérifiez que le bug n'a pas déjà été signalé dans les [Issues](../../issues)
2. Créez une nouvelle issue en utilisant le template "Bug Report"
3. Fournissez le maximum d'informations pour reproduire le problème

### Proposer une Fonctionnalité

1. Vérifiez que la fonctionnalité n'a pas déjà été proposée
2. Créez une issue en utilisant le template "Feature Request"
3. Décrivez le problème que vous cherchez à résoudre

### Soumettre du Code

1. Forkez le repository
2. Créez une branche pour votre modification
3. Développez et testez vos changements
4. Soumettez une Pull Request

## Processus de Développement

### 1. Configuration de l'Environnement

```bash
# Cloner votre fork
git clone https://github.com/VOTRE-USERNAME/REPO.git
cd REPO

# Ajouter le repo original comme remote
git remote add upstream https://github.com/ORG/REPO.git

# Installer les dépendances
pnpm install

# Configurer les hooks
pnpm prepare
```

### 2. Créer une Branche

```bash
# Mettre à jour main
git checkout main
git pull upstream main

# Créer une branche
git checkout -b type/description-courte

# Exemples :
# feat/user-authentication
# fix/login-validation
# docs/api-examples
```

### Conventions de Nommage des Branches

| Préfixe | Usage |
|---------|-------|
| `feat/` | Nouvelle fonctionnalité |
| `fix/` | Correction de bug |
| `docs/` | Documentation |
| `refactor/` | Refactoring |
| `test/` | Ajout de tests |
| `chore/` | Maintenance |

### 3. Développer

```bash
# Lancer en mode développement
pnpm dev

# Vérifier le code
pnpm lint
pnpm typecheck
pnpm test
```

### 4. Commiter

Suivez les [Conventional Commits](https://www.conventionalcommits.org/) :

```bash
git commit -m "feat(auth): add password reset functionality"
git commit -m "fix(cart): resolve quantity update bug"
git commit -m "docs(api): update authentication examples"
```

### 5. Pousser et Créer une PR

```bash
# Pousser votre branche
git push origin feat/ma-feature

# Créer une PR via GitHub
```

## Standards de Code

### Formatage

Le code est automatiquement formaté via pre-commit hooks. Vous pouvez aussi lancer manuellement :

```bash
pnpm format      # Formater tout le code
pnpm lint:fix    # Corriger les erreurs de lint
```

### TypeScript

- Utilisez des types explicites (pas de `any` sauf cas justifié)
- Préférez les interfaces aux types pour les objets
- Documentez les fonctions complexes avec JSDoc

### Tests

- Écrivez des tests pour toute nouvelle fonctionnalité
- Maintenez la couverture au-dessus du seuil défini
- Nommez vos tests de manière descriptive

```typescript
// ✅ Bon
test('should return empty array when no items match filter', () => {})

// ❌ Mauvais
test('filter test', () => {})
```

### Structure des Fichiers

```
src/
├── components/
│   └── Button/
│       ├── Button.tsx          # Composant
│       ├── Button.test.tsx     # Tests
│       ├── Button.styles.ts    # Styles (si applicable)
│       └── index.ts            # Export
```

## Commits

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `docs` | Documentation |
| `style` | Formatage (pas de changement de logique) |
| `refactor` | Refactoring |
| `perf` | Amélioration de performance |
| `test` | Ajout/modification de tests |
| `chore` | Maintenance |
| `ci` | Configuration CI/CD |

### Exemples

```bash
feat(auth): add OAuth2 login with Google

Implements OAuth2 authentication flow with Google provider.
Users can now log in using their Google account.

Closes #123
```

```bash
fix(cart): resolve race condition on quantity update

Multiple rapid clicks caused incorrect totals due to
concurrent state updates. Added debounce and optimistic
locking.

Fixes #456
```

## Pull Requests

### Checklist Avant Soumission

- [ ] Le code compile sans erreur
- [ ] Tous les tests passent
- [ ] Le linter ne signale rien
- [ ] La documentation est à jour
- [ ] Les commits suivent les conventions
- [ ] La PR a une description claire

### Template de PR

Utilisez le template fourni et remplissez toutes les sections :

1. **Description** : Expliquez vos changements
2. **Type de changement** : Cochez la case appropriée
3. **Comment tester** : Étapes pour vérifier
4. **Checklist** : Confirmez les vérifications

### Taille des PRs

- Préférez les petites PRs focalisées
- Une PR = une fonctionnalité ou un fix
- Si la PR est grande, expliquez pourquoi

## Review

### Pour l'Auteur

- Répondez aux commentaires de manière constructive
- Expliquez vos choix si vous n'êtes pas d'accord
- Mettez à jour votre PR selon les retours
- Relancez la review une fois les corrections faites

### Pour le Reviewer

- Soyez constructif et bienveillant
- Distinguez les blocages des suggestions
- Approuvez quand les critères sont remplis

### Étiquettes de Commentaires

| Préfixe | Signification |
|---------|---------------|
| `blocker:` | Doit être corrigé avant merge |
| `suggestion:` | Amélioration optionnelle |
| `question:` | Besoin de clarification |
| `nit:` | Détail mineur |

## Questions ?

Si vous avez des questions :

1. Consultez la documentation
2. Recherchez dans les issues existantes
3. Créez une discussion si besoin

Merci de contribuer ! 🎉
