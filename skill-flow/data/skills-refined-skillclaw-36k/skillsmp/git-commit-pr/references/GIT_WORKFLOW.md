# Git Workflow Détaillé

Guide complet du workflow Git pour commits, push et Pull Requests.

## Vue d'Ensemble

```
┌─────────────────┐
│ 1. VÉRIFICATION │
│  - git status   │
│  - git diff     │
│  - git log      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. STAGING     │
│  - git add      │
│  - Vérification │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. COMMIT      │
│  - Message      │
│  - Validation   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. PUSH        │
│  - git push     │
│  - Retry        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. PULL        │
│     REQUEST     │
│  - gh pr create │
└─────────────────┘
```

---

## Étape 1 : Vérification Pré-Commit

### 1.1 Vérifier l'état du dépôt

```bash
git status
```

**Analyse de la sortie** :
```
On branch feature/add-dark-mode
Your branch is up to date with 'origin/feature/add-dark-mode'.

Changes not staged for commit:
  modified:   src/components/ThemeToggle.tsx
  modified:   src/styles/theme.css

Untracked files:
  src/hooks/useTheme.ts
```

✅ **Points à vérifier** :
- Branche correcte ? (pas `main` si interdite)
- Fichiers modifiés attendus ?
- Pas de fichiers sensibles ? (.env, credentials)

### 1.2 Voir les différences

```bash
# Voir tous les changements (staged + unstaged)
git diff HEAD

# Voir seulement les changements unstaged
git diff

# Voir seulement les changements staged
git diff --staged

# Voir les stats
git diff HEAD --stat
```

**Exemple de sortie** :
```diff
diff --git a/src/components/ThemeToggle.tsx b/src/components/ThemeToggle.tsx
index a1b2c3d..e4f5g6h 100644
--- a/src/components/ThemeToggle.tsx
+++ b/src/components/ThemeToggle.tsx
@@ -1,5 +1,8 @@
+import { useTheme } from '@/hooks/useTheme';
+
 export function ThemeToggle() {
-  return <button>Toggle</button>;
+  const { theme, toggleTheme } = useTheme();
+  return <button onClick={toggleTheme}>{theme}</button>;
 }
```

✅ **Points à vérifier** :
- Changements intentionnels ?
- Pas de code debug laissé ? (console.log, debugger)
- Pas de données sensibles ? (API keys, tokens)

### 1.3 Voir l'historique récent

```bash
# 10 derniers commits
git log --oneline -10

# Avec stats
git log --oneline --stat -5

# Avec graphe
git log --oneline --graph -10
```

**Pourquoi ?** Comprendre le style de commits du projet pour rester cohérent.

---

## Étape 2 : Staging des Fichiers

### 2.1 Ajouter des fichiers spécifiques (recommandé)

```bash
# Ajouter un fichier
git add src/components/ThemeToggle.tsx

# Ajouter plusieurs fichiers
git add src/components/ThemeToggle.tsx src/styles/theme.css

# Ajouter un répertoire
git add src/hooks/

# Ajouter tous les fichiers d'un type
git add *.tsx
```

### 2.2 Ajouter tous les fichiers (avec précaution)

```bash
# Ajouter tous les fichiers modifiés et nouveaux
git add .

# Ajouter tous les fichiers (y compris suppressions)
git add -A

# Mode interactif (choix fichier par fichier)
git add -i
```

⚠️ **Attention** : Toujours vérifier avec `git status` avant `git add .`

### 2.3 Vérifier ce qui est staged

```bash
git status

# Voir le diff des fichiers staged
git diff --staged
```

### 2.4 Retirer des fichiers du staging

```bash
# Retirer un fichier
git reset HEAD .env

# Retirer tous les fichiers
git reset HEAD

# Retirer un fichier et annuler les modifications
git checkout -- fichier.txt
```

### 2.5 Checklist pré-staging

- [ ] Pas de `.env` ou `.env.local`
- [ ] Pas de `credentials.json` ou `secrets.yaml`
- [ ] Pas de fichiers `*.key`, `*.pem`
- [ ] Pas de `node_modules/` (doit être dans .gitignore)
- [ ] Pas de fichiers de build (`dist/`, `build/`)
- [ ] Pas de fichiers temporaires (`.DS_Store`, `*.log`)
- [ ] Pas de code debug (`console.log`, `debugger`)

---

## Étape 3 : Création du Commit

### 3.1 Format du message

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
[session URL]
```

### 3.2 Commit simple (une ligne)

```bash
git commit -m "feat(theme): add dark mode toggle"
```

### 3.3 Commit avec body (HEREDOC)

```bash
git commit -m "$(cat <<'EOF'
feat(theme): add dark mode toggle

Users can now switch between light and dark themes.
Theme preference is saved in localStorage and persists
across sessions.

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
EOF
)"
```

### 3.4 Commit avec breaking change

```bash
git commit -m "$(cat <<'EOF'
feat(api)!: change user response format

BREAKING CHANGE: User API now returns paginated format.
Response: { data: User[], meta: { total, page, pageSize } }

Migration: Update all API calls to access response.data

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
EOF
)"
```

### 3.5 Vérifier le commit

```bash
# Voir le dernier commit
git log -1

# Voir le dernier commit avec diff
git show

# Voir le message du dernier commit
git log -1 --pretty=%B
```

### 3.6 Modifier le dernier commit (si nécessaire)

⚠️ **ATTENTION** : Seulement si le commit n'a **PAS** été pushé.

```bash
# Modifier le message
git commit --amend -m "nouveau message"

# Ajouter des fichiers oubliés
git add fichier-oublie.txt
git commit --amend --no-edit

# Modifier le message avec éditeur
git commit --amend
```

❌ **NE JAMAIS** utiliser `--amend` après un échec de hook pre-commit.

---

## Étape 4 : Push vers Origin

### 4.1 Vérifier la branche

```bash
# Voir la branche actuelle
git branch --show-current

# Voir toutes les branches
git branch -a

# Voir la branche remote trackée
git branch -vv
```

### 4.2 Push simple

```bash
# Première fois (nouvelle branche)
git push -u origin nom-branche

# Fois suivantes
git push
```

### 4.3 Push avec retry (réseau instable)

```bash
# Retry automatique (4 tentatives)
git push -u origin branch || sleep 2 && \
git push -u origin branch || sleep 4 && \
git push -u origin branch || sleep 8 && \
git push -u origin branch
```

### 4.4 Gestion des erreurs

#### Erreur : Branche divergente

```
error: failed to push some refs to 'origin'
hint: Updates were rejected because the tip of your current branch is behind
```

**Solution** :
```bash
# Récupérer les changements
git fetch origin

# Merge (si safe)
git merge origin/branch-name

# Ou rebase (si préféré)
git rebase origin/branch-name

# Puis push
git push
```

#### Erreur : Refusé (protected branch)

```
error: GH006: Protected branch update failed
```

**Solution** : Créer une PR au lieu de push direct.

#### Erreur : Taille du fichier

```
error: File large-file.bin is 150.00 MB; this exceeds GitHub's file size limit
```

**Solution** :
```bash
# Retirer du commit
git rm --cached large-file.bin

# Ajouter à .gitignore
echo "large-file.bin" >> .gitignore

# Amend le commit
git commit --amend --no-edit
```

### 4.5 Vérifier le push

```bash
# Voir les commits pushés
git log origin/branch-name..HEAD

# Si vide : tout est pushé ✅
```

---

## Étape 5 : Création de la Pull Request

### 5.1 Pré-requis

```bash
# Vérifier gh CLI installé
gh --version

# Vérifier authentification
gh auth status

# Se connecter si nécessaire
gh auth login
```

### 5.2 Analyser les changements

```bash
# Voir TOUS les commits de la branche
git log main..HEAD --oneline

# Voir TOUS les diffs depuis main
git diff main...HEAD

# Stats des fichiers modifiés
git diff main...HEAD --stat
```

⚠️ **Important** : Analyser **TOUS** les commits, pas seulement le dernier !

### 5.3 Créer la PR (format complet)

```bash
gh pr create --title "feat(theme): add dark mode support" --body "$(cat <<'EOF'
## Summary
- Add dark mode toggle component
- Implement theme persistence in localStorage
- Update all components to support theme switching

## Changes
### Added
- ThemeToggle component
- useTheme custom hook
- Dark theme CSS variables
- Theme context provider

### Changed
- Updated Button component to use theme colors
- Updated Navbar to include theme toggle

## Type of Change
- [x] New feature (non-breaking change which adds functionality)

## Testing
- [x] Tested theme toggle in Chrome, Firefox, Safari
- [x] Verified localStorage persistence
- [x] Tested with system preference detection
- [x] All existing tests pass
- [x] No console errors

## Screenshots
[Include before/after screenshots]

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
EOF
)"
```

### 5.4 Options de gh pr create

```bash
# Draft PR
gh pr create --draft --title "..." --body "..."

# Branche de base personnalisée
gh pr create --base develop --title "..." --body "..."

# Avec reviewers
gh pr create --reviewer user1,user2 --title "..." --body "..."

# Avec labels
gh pr create --label bug,urgent --title "..." --body "..."

# Avec assignees
gh pr create --assignee @me --title "..." --body "..."

# Avec milestone
gh pr create --milestone v2.0 --title "..." --body "..."
```

### 5.5 Vérifier la PR créée

```bash
# Voir la PR
gh pr view

# Voir dans le navigateur
gh pr view --web

# Lister les PRs
gh pr list
```

### 5.6 Mettre à jour la PR

```bash
# Modifier le titre
gh pr edit --title "nouveau titre"

# Modifier la description
gh pr edit --body "nouvelle description"

# Ajouter des reviewers
gh pr edit --add-reviewer user1,user2

# Passer de draft à ready
gh pr ready
```

---

## Workflow Complet (Exemple)

### Scénario : Ajouter une nouvelle fonctionnalité

```bash
# 1. Créer une branche
git checkout -b feature/user-avatar

# 2. Faire les modifications
# ... coder ...

# 3. Vérifier les changements
git status
git diff HEAD
git log --oneline -5

# 4. Ajouter les fichiers
git add src/components/Avatar.tsx
git add src/api/uploadAvatar.ts
git add src/types/user.ts

# 5. Vérifier staging
git status
git diff --staged

# 6. Commiter
git commit -m "$(cat <<'EOF'
feat(user): add avatar upload functionality

Users can now upload and update their profile avatar.
Supports JPEG, PNG, WebP formats up to 5MB.
Images are automatically resized to 256x256px.

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
EOF
)"

# 7. Vérifier le commit
git show

# 8. Pousser avec retry
git push -u origin feature/user-avatar || sleep 2 && \
git push -u origin feature/user-avatar

# 9. Analyser pour la PR
git log main..HEAD --oneline
git diff main...HEAD --stat

# 10. Créer la PR
gh pr create --title "feat(user): add avatar upload functionality" --body "$(cat <<'EOF'
## Summary
- Add user avatar upload feature
- Support multiple image formats
- Automatic image optimization

## Changes
### Added
- Avatar upload component
- Image validation and resizing
- Upload API endpoint
- User type with avatar_url field

## Type of Change
- [x] New feature (non-breaking change which adds functionality)

## Testing
- [x] Tested with JPEG, PNG, WebP
- [x] Tested file size limits
- [x] Tested image optimization
- [x] All tests pass
- [x] No console errors

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
EOF
)"

# 11. Ouvrir la PR dans le navigateur
gh pr view --web
```

---

## Bonnes Pratiques

### ✅ À FAIRE

1. **Vérifier avant commit** : `git status`, `git diff`
2. **Commits atomiques** : 1 commit = 1 changement logique
3. **Messages descriptifs** : Format Conventional Commits
4. **Fichiers spécifiques** : `git add <fichier>` plutôt que `git add .`
5. **Analyser tous les commits** : Pour la PR, pas juste le dernier
6. **Tester avant PR** : S'assurer que tout fonctionne
7. **PR bien documentée** : Summary, Changes, Testing
8. **Review avant merge** : Ne pas auto-merge sans review

### ❌ À ÉVITER

1. **Commits vagues** : "fix", "update", "WIP"
2. **Commits massifs** : 50+ fichiers en un commit
3. **Commiter des secrets** : .env, credentials, API keys
4. **Force push sur main** : `git push --force` sur branche protégée
5. **Amend après push** : Ne pas réécrire l'historique public
6. **Skip hooks** : `--no-verify` sans raison valide
7. **PRs sans contexte** : Description vide ou minimale

---

## Troubleshooting

### Problème : Pre-commit hook échoue

```bash
# ❌ NE PAS FAIRE
git commit --no-verify

# ✅ FAIRE
# 1. Corriger le problème (linting, tests)
# 2. Re-stage
git add fichier-corrige.ts
# 3. Créer un NOUVEAU commit
git commit -m "fix: resolve linting errors"
```

### Problème : Oubli d'un fichier

```bash
# Si PAS encore pushé
git add fichier-oublie.ts
git commit --amend --no-edit

# Si DÉJÀ pushé
git add fichier-oublie.ts
git commit -m "chore: add missing file"
git push
```

### Problème : Mauvais message de commit

```bash
# Si PAS encore pushé
git commit --amend -m "nouveau message correct"

# Si DÉJÀ pushé
# Ne pas modifier, créer un nouveau commit si nécessaire
```

### Problème : Commit sur mauvaise branche

```bash
# Annuler le commit (garde les changements)
git reset HEAD~1

# Changer de branche
git checkout bonne-branche

# Re-commit
git add .
git commit -m "message"
```

### Problème : Conflit lors du push

```bash
# Récupérer les changements
git fetch origin

# Merge les changements
git merge origin/branch-name

# Résoudre les conflits dans les fichiers
# Puis :
git add .
git commit -m "merge: resolve conflicts"
git push
```

---

## Ressources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Best Practices](https://github.com/git-tips/tips)
- [Oh Shit, Git!?!](https://ohshitgit.com/)
