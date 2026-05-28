---
name: apex
description: >
  Workflow autonome de développement complet en 10 étapes. Orchestre l'exploration,
  la planification et l'implémentation pour développer une feature de A à Z.
  Utiliser avec /apex [feature] pour mode interactif ou /apex --auto [feature]
  pour mode autonome. Triggers: "apex", "workflow complet", "feature to PR",
  "développement autonome", "implement feature end to end".
---

# /apex - Autonomous Development Workflow

---

## INSTRUCTIONS D'EXÉCUTION

**Quand ce skill est invoqué, suivre ces étapes dans l'ordre :**

### Étape 0 : Parser les arguments et initialiser

1. **Parser la commande** pour extraire :
   - Flags : `--auto`, `--review`, `--tests`, `--resume`
   - Feature description : tout le reste après les flags

   ```
   Exemple : "/apex --auto --tests Ajouter un dark mode"
   → flags: { auto: true, review: false, tests: true, resume: false }
   → feature: "Ajouter un dark mode"
   ```

2. **Déterminer le mode** :
   - Si `--auto` : mode autonome (pas de confirmation entre étapes)
   - Sinon : mode interactif (confirmation avec AskUserQuestion avant chaque étape)
   - En mode autonome : `--review` et `--tests` contrôlent si ces étapes sont exécutées
   - En mode interactif : toutes les étapes sont proposées

3. **Créer la todo list** avec TodoWrite :
   ```
   1. [pending] Vérifications git et création branche
   2. [pending] Analyse du codebase
   3. [pending] Planification de l'implémentation
   4. [pending] Implémentation du code
   5. [pending] Validation (build/lint/types)
   6. [pending] Code review (si activé)
   7. [pending] Correction des issues (si nécessaire)
   8. [pending] Écriture des tests (si activé)
   9. [pending] Vérification des tests (si activé)
   10. [pending] Création de la Pull Request
   ```

4. **Afficher le header** :
   ```
   🚀 APEX - Autonomous Development Workflow
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Feature: {feature_description}
   Mode: {Interactif | Autonome} {flags actifs}
   ```

### Étape 1 : Init Branch

**Marquer todo 1 comme in_progress**

1. Vérifier qu'on est dans un repo git : `git rev-parse --git-dir`
2. Vérifier le working tree : `git status --porcelain`
   - Si non vide → demander à l'utilisateur : commit/stash/abort
3. Identifier la branche principale : chercher `main`, `master`, ou `develop`
4. Pull les dernières modifications : `git checkout {main} && git pull`
5. Générer le nom de branche :
   - Extraire mots-clés de la feature → kebab-case
   - Préfixer avec `feature/`
   - Limiter à 50 caractères
6. Créer la branche : `git checkout -b feature/{nom}`
7. Créer le dossier `.apex/` pour les artefacts du workflow

**Marquer todo 1 comme completed**

### Étape 2 : Analyze Code (Agent Explore)

**Marquer todo 2 comme in_progress**

En mode interactif : demander confirmation avec AskUserQuestion avant de lancer

Utiliser l'outil **Task** avec `subagent_type: "Explore"` :

```
Prompt: Explore ce codebase pour comprendre comment implémenter la feature suivante :
"{feature_description}"

Analyse demandée :
1. Structure générale du projet (dossiers, architecture)
2. Patterns utilisés (state management, routing, styling, etc.)
3. Fichiers pertinents pour cette feature (avec chemins)
4. Conventions de code observées (naming, structure)
5. Technologies et frameworks détectés

Retourne un rapport structuré avec ces informations.
```

Stocker le résultat pour l'étape suivante.

**Marquer todo 2 comme completed**

### Étape 3 : Plan Feature (Agent Plan)

**Marquer todo 3 comme in_progress**

En mode interactif : demander confirmation avec AskUserQuestion

Utiliser l'outil **Task** avec `subagent_type: "Plan"` :

```
Prompt: En te basant sur l'analyse ci-dessous, crée un plan d'implémentation pour :
"{feature_description}"

Analyse du codebase :
{résultat_étape_2}

Le plan doit inclure :
1. Stratégie d'implémentation
2. Liste des fichiers à créer (avec chemins complets)
3. Liste des fichiers à modifier (avec changements spécifiques)
4. Séquence d'implémentation ordonnée
5. Points d'attention et risques
```

Écrire le plan dans `.apex/plan.md`

**Marquer todo 3 comme completed**

### Étape 4 : Execute (Implémentation)

**Marquer todo 4 comme in_progress**

En mode interactif : demander confirmation avec AskUserQuestion

Lire `.apex/plan.md` et pour chaque tâche du plan :

1. Lire le fichier concerné (si modification)
2. Implémenter le changement
3. Commit atomique avec message conventionnel :
   ```
   git commit -m "type(scope): description

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

Types de commit :
- `feat`: nouvelle fonctionnalité
- `fix`: correction de bug
- `refactor`: refactoring
- `test`: tests
- `docs`: documentation

**Marquer todo 4 comme completed**

### Étape 5 : Validate

**Marquer todo 5 comme in_progress**

1. **Détecter le type de projet** en cherchant :
   - `package.json` → Node.js
   - `Cargo.toml` → Rust
   - `go.mod` → Go
   - `pyproject.toml` / `requirements.txt` → Python

2. **Pour Node.js**, lire `package.json` et identifier :
   - Package manager : pnpm-lock.yaml → pnpm, yarn.lock → yarn, sinon npm
   - Scripts disponibles : `build`, `lint`, `typecheck`, `type-check`, `tsc`

3. **Exécuter les validations disponibles** :

   | Projet | Build | Lint | Types |
   |--------|-------|------|-------|
   | Node.js | `{pm} run build` | `{pm} run lint` | `{pm} run typecheck` ou `tsc --noEmit` |
   | Rust | `cargo build` | `cargo clippy` | (inclus) |
   | Go | `go build ./...` | `go vet ./...` | (inclus) |
   | Python | - | `ruff check .` | `mypy .` |

4. **Si erreur** :
   - Parser le message d'erreur
   - Corriger le fichier concerné
   - Commit : `fix(scope): resolve {type} error`
   - Retry (max 3 fois)

5. **Si pas de scripts de validation** : noter et continuer

**Marquer todo 5 comme completed**

### Étape 6 : Review (si activé)

**Skip si mode `--auto` sans `--review`**

**Marquer todo 6 comme in_progress**

En mode interactif : demander confirmation avec AskUserQuestion

1. Obtenir le diff complet : `git diff main...HEAD`

2. Effectuer une code review en analysant :
   - **Bugs** : erreurs logiques, edge cases
   - **Security** : injections, XSS, données exposées
   - **Performance** : N+1, renders inutiles
   - **Conventions** : respect des patterns du projet

3. Catégoriser les issues :
   - 🔴 **Critical** : doit être corrigé (bloquant)
   - 🟡 **Warning** : devrait être corrigé
   - 🔵 **Suggestion** : amélioration optionnelle

4. Écrire le rapport dans `.apex/review.md`

**Marquer todo 6 comme completed**

### Étape 7 : Fix Issues (si nécessaire)

**Skip si pas d'issues Critical/Warning dans review.md**

**Marquer todo 7 comme in_progress**

1. Lire `.apex/review.md`
2. Pour chaque issue Critical et Warning :
   - Localiser le fichier et la ligne
   - Appliquer la correction
   - Commit : `fix(scope): resolve review issue {id}`
3. Re-exécuter l'étape 5 (Validate)

**Marquer todo 7 comme completed**

### Étape 8 : Add Tests (si activé)

**Skip si mode `--auto` sans `--tests`**

**Marquer todo 8 comme in_progress**

En mode interactif : demander confirmation avec AskUserQuestion

1. **Détecter le framework de test** :
   - `jest.config.*` ou `"jest"` dans package.json → Jest
   - `vitest.config.*` → Vitest
   - `pytest.ini` ou `pyproject.toml` avec pytest → Pytest
   - `*_test.go` existants → Go testing
   - `Cargo.toml` → Rust tests

2. **Trouver des exemples de tests existants** pour référence de style

3. **Écrire les tests** :
   - Tests unitaires pour les nouvelles fonctions
   - Tests des edge cases (null, empty, erreurs)
   - Placer dans le bon dossier selon les conventions du projet

4. **Commit** : `test(scope): add tests for {feature}`

**Marquer todo 8 comme completed**

### Étape 9 : Verify Tests (si activé)

**Skip si étape 8 skippée**

**Marquer todo 9 comme in_progress**

1. **Exécuter les tests** :
   - Jest/Vitest : `{pm} test` ou `npx jest`
   - Pytest : `pytest`
   - Go : `go test ./...`
   - Rust : `cargo test`

2. **Si échec** :
   - Analyser si le bug est dans le code ou le test
   - Corriger
   - Commit : `fix(test): correct {test_name}`
   - Retry (max 3 fois)

**Marquer todo 9 comme completed**

### Étape 10 : Create PR

**Marquer todo 10 comme in_progress**

1. **Push la branche** :
   ```bash
   git push -u origin feature/{nom}
   ```

2. **Générer le titre** : `{type}: {description courte en anglais}`

3. **Générer le body** :
   ```markdown
   ## Summary
   {Description de la feature}

   ## Changes
   {Liste des changements extraite des commits}

   ## Testing
   - [x] Build passes
   - [x] Lint passes
   - [x] Type check passes
   - [x] Unit tests pass

   ---
   🤖 Generated with [Claude Code](https://claude.ai/claude-code) using /apex
   ```

4. **Créer la PR** :
   ```bash
   gh pr create --title "{titre}" --body "{body}"
   ```

5. **Afficher le résultat** :
   ```
   🎉 Pipeline complete!
   PR: {url}
   ```

**Marquer todo 10 comme completed**

---

## GESTION DES ERREURS

### Mode interactif
À chaque erreur, utiliser AskUserQuestion :
```
options: ["Retry", "Skip cette étape", "Abort le workflow"]
```

### Mode autonome
1. Retry automatique (max 2 fois)
2. Si échec persistant → demander à l'utilisateur avec AskUserQuestion

### Erreurs bloquantes (toujours abort)
- Pas un repo git
- Pas de remote origin
- Push échoue (permissions)

---

## GESTION DU FLAG --resume

Si `--resume` est présent :

1. Vérifier si une branche `feature/*` existe localement
2. Checkout cette branche
3. Analyser l'état :
   - `.apex/plan.md` existe → étape 3 complétée
   - `.apex/review.md` existe → étape 6 complétée
   - Compter les commits depuis main → estimer progression
4. Reprendre à l'étape suivante

---

## CONVENTIONS

### Structure des artefacts
```
.apex/
├── plan.md      # Plan d'implémentation (étape 3)
└── review.md    # Rapport de review (étape 6)
```

### Nommage des branches
`feature/{mots-clés-kebab-case}` (max 50 chars)

### Format des commits
```
type(scope): description en anglais

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## QUICK REFERENCE

| Mode | Commande | Review | Tests |
|------|----------|:------:|:-----:|
| Interactif complet | `/apex {feature}` | ✓ | ✓ |
| Autonome minimal | `/apex --auto {feature}` | ✗ | ✗ |
| Autonome + review | `/apex --auto --review {feature}` | ✓ | ✗ |
| Autonome + tests | `/apex --auto --tests {feature}` | ✗ | ✓ |
| Autonome complet | `/apex --auto --review --tests {feature}` | ✓ | ✓ |
| Reprendre | `/apex --resume` | - | - |

---

## Référence détaillée

Pour plus de détails sur chaque étape : [references/workflow.md](./references/workflow.md)
