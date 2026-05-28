# APEX Workflow - Detailed Reference

Ce document complète le SKILL.md avec des détails supplémentaires sur chaque étape.

**Note** : Les instructions d'exécution principales sont dans SKILL.md. Ce fichier fournit du contexte additionnel.

---

## Artefacts du workflow

Tous les artefacts sont stockés dans le dossier `.apex/` à la racine du projet :

```
.apex/
├── plan.md      # Plan d'implémentation (créé à l'étape 3)
└── review.md    # Rapport de code review (créé à l'étape 6)
```

Ce dossier est créé à l'étape 1 et peut être ajouté au `.gitignore` ou commité selon les préférences.

---

## Étape 1: Init Branch

### Objectif
Créer une branche de travail propre pour la feature.

### Vérifications préalables

```bash
# 1. Vérifier qu'on est dans un repo git
git rev-parse --git-dir

# 2. Vérifier le working tree
git status --porcelain
# Si non vide → demander commit ou stash

# 3. Identifier la branche principale
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'
# Fallback: main > master > develop
```

### Génération du nom de branche

1. Extraire les mots-clés de la description de feature
2. Convertir en kebab-case
3. Préfixer avec `feature/`
4. Limiter à 50 caractères

Exemples :
- "Ajouter un bouton de partage" → `feature/add-share-button`
- "Fix le bug de pagination sur mobile" → `feature/fix-pagination-bug-mobile`

### Actions

```bash
# Checkout branche principale et pull
git checkout main && git pull origin main

# Créer et checkout la nouvelle branche
git checkout -b feature/nom-feature
```

### Gestion des conflits

Si la branche existe déjà :
1. Proposer de checkout la branche existante
2. Ou générer un nom alternatif avec suffixe (`-v2`, `-alt`)

### Critère de succès
- Branche créée et checkoutée
- Working tree propre
- Synchronisé avec remote

---

## Étape 2: Analyze Code (Analyst)

### Objectif
Comprendre l'architecture et identifier les fichiers pertinents.

### Agent utilisé
`Task` avec `subagent_type: "Explore"`

### Prompt pour l'agent Analyst

```
Explore ce codebase pour comprendre comment implémenter la feature suivante :
"{description_feature}"

Analyse demandée :
1. Structure générale du projet
2. Patterns utilisés (state management, routing, components, etc.)
3. Fichiers qui semblent pertinents pour cette feature
4. Conventions de code observées
5. Dépendances et contraintes techniques

Focus sur les éléments nécessaires à l'implémentation, pas une analyse exhaustive.
```

### Output attendu

Rapport structuré incluant :
- **Architecture** : Organisation des dossiers, layers
- **Patterns** : State management, routing, styling
- **Fichiers pertinents** : Liste avec justification
- **Conventions** : Naming, structure des composants
- **Risques** : Points d'attention pour l'implémentation

### Critère de succès
- Au moins 3 fichiers pertinents identifiés
- Patterns principaux compris
- Pas de zone d'ombre critique

---

## Étape 3: Plan Feature (Architect)

### Objectif
Concevoir le plan d'implémentation détaillé.

### Agent utilisé
`Task` avec `subagent_type: "Plan"`

### Prompt pour l'agent Architect

```
En te basant sur l'analyse précédente, crée un plan d'implémentation pour :
"{description_feature}"

Contexte du codebase :
{rapport_analyse_étape_2}

Le plan doit inclure :
1. Stratégie d'implémentation (approche choisie)
2. Liste ordonnée des fichiers à créer/modifier
3. Pour chaque fichier : changements spécifiques à effectuer
4. Dépendances entre les changements
5. Points de validation intermédiaires
```

### Output : plan.md

```markdown
# Plan d'implémentation : {feature}

## Stratégie
{Description de l'approche choisie et pourquoi}

## Fichiers concernés

### À créer
- `path/to/new/file.ts` - {description}

### À modifier
- `path/to/existing/file.ts` - {changements}

## Séquence d'implémentation

1. **{Tâche 1}**
   - Fichier: `path/file.ts`
   - Action: {description}
   - Validation: {comment vérifier}

2. **{Tâche 2}**
   ...

## Points d'attention
- {Risque 1 et mitigation}
- {Risque 2 et mitigation}

## Estimation
Complexité: {Low/Medium/High}
```

### Critère de succès
- Plan validé et réalisable
- Tous les fichiers identifiés
- Séquence logique sans dépendances circulaires

---

## Étape 4: Execute (Developer)

### Objectif
Implémenter la feature selon le plan.

### Processus

Pour chaque tâche du plan :

1. **Lire le fichier** (si modification)
2. **Implémenter le changement**
   - Respecter les patterns existants
   - Suivre les conventions du codebase
3. **Valider localement** (syntax check)
4. **Commit atomique**

### Convention de commits

```bash
# Format
git commit -m "type(scope): description

Co-Authored-By: Claude <noreply@anthropic.com>"

# Exemples par tâche
git commit -m "feat(share): add ShareButton component"
git commit -m "feat(share): integrate ShareButton in ArticlePage"
git commit -m "feat(share): add share analytics tracking"
```

### Règles d'implémentation

1. **Un commit par changement logique** - Pas de commits géants
2. **Respect du style existant** - Ne pas reformater tout le fichier
3. **Pas de sur-ingénierie** - Implémenter ce qui est demandé
4. **Tests inline** - Vérifier que le code compile/parse

### Critère de succès
- Tous les fichiers du plan traités
- Commits atomiques créés
- Code syntaxiquement valide

---

## Étape 5: Validate

### Objectif
Vérifier que le build, lint et types passent.

### Détection des commandes

| Fichier | Commande build | Commande lint | Commande types |
|---------|---------------|---------------|----------------|
| `package.json` | `npm run build` | `npm run lint` | `npm run typecheck` ou `tsc --noEmit` |
| `Cargo.toml` | `cargo build` | `cargo clippy` | (inclus dans build) |
| `go.mod` | `go build ./...` | `go vet ./...` | (inclus dans build) |
| `pyproject.toml` | - | `ruff check .` | `mypy .` |

### Processus

```bash
# 1. Build
{build_command}
# Si échec → identifier erreur → fix → retry

# 2. Lint
{lint_command}
# Si warnings → évaluer si fix nécessaire

# 3. Type check
{typecheck_command}
# Si erreur → fix → retry
```

### Gestion des erreurs

Pour chaque erreur :
1. Parser le message d'erreur
2. Localiser le fichier et la ligne
3. Appliquer le fix
4. Commit de fix : `fix(scope): resolve {type} error`
5. Re-run la validation

### Critère de succès
- Build: exit code 0
- Lint: pas d'erreurs (warnings acceptables)
- Types: pas d'erreurs

---

## Étape 6: Review

### Objectif
Effectuer une code review automatique de qualité.

### Exécution
Cette étape est effectuée directement (pas de sub-agent). Claude analyse le diff et produit le rapport de review.

### Checklist de review

1. **Bugs** : Erreurs logiques, edge cases non gérés
2. **Security** : Injections, XSS, données sensibles exposées
3. **Performance** : N+1 queries, renders inutiles, memory leaks
4. **Maintenabilité** : Code dupliqué, complexité excessive
5. **Conventions** : Respect des patterns du projet

### Catégorisation des issues

- 🔴 **CRITICAL** : Blocage, doit être fixé avant merge
- 🟡 **WARNING** : Important mais non bloquant
- 🔵 **SUGGESTION** : Amélioration optionnelle

### Output : review.md

```markdown
# Code Review : {feature}

## Résumé
- Critical: {n}
- Warnings: {n}
- Suggestions: {n}

## Issues

### 🔴 Critical

#### [C1] {Titre}
- **Fichier**: `path/file.ts:42`
- **Description**: {description du problème}
- **Fix suggéré**: {comment corriger}

### 🟡 Warning

#### [W1] {Titre}
...

### 🔵 Suggestion

#### [S1] {Titre}
...
```

### Critère de succès
- Review complétée
- Issues catégorisées
- Fixes suggérés pour les criticals

---

## Étape 7: Fix Issues

### Objectif
Corriger les issues critiques et warnings de la review.

### Processus

1. **Parser review.md**
2. **Pour chaque Critical** :
   - Localiser le fichier et la ligne
   - Appliquer le fix suggéré
   - Commit : `fix(scope): resolve review issue C{n}`
3. **Pour chaque Warning** :
   - Évaluer si fix nécessaire
   - Appliquer si oui
   - Commit : `fix(scope): address review warning W{n}`
4. **Re-run validation** (Étape 5)

### Priorité des fixes

1. Security issues (toujours fixer)
2. Bugs critiques (toujours fixer)
3. Performance issues (fixer si impact significatif)
4. Maintenabilité (fixer si temps le permet)
5. Suggestions (skip en mode autonome)

### Critère de succès
- Tous les Critical résolus
- Warnings évalués et traités
- Validation repasse

---

## Étape 8: Add Tests

### Objectif
Écrire des tests pour les nouveaux chemins de code.

### Exécution
Cette étape est effectuée directement. Claude écrit les tests en suivant les conventions du projet.

### Détection du framework de test

| Fichier | Framework | Pattern de test |
|---------|-----------|-----------------|
| `jest.config.*` | Jest | `*.test.ts`, `*.spec.ts` |
| `vitest.config.*` | Vitest | `*.test.ts`, `*.spec.ts` |
| `pytest.ini` | Pytest | `test_*.py` |
| `Cargo.toml` | Rust tests | `#[cfg(test)]` inline |
| `*_test.go` | Go testing | `*_test.go` |

### Tests à écrire

1. **Tests unitaires** pour chaque nouvelle fonction
2. **Tests des edge cases** : null, empty, invalid input
3. **Tests d'intégration** si composants interconnectés

### Processus

1. Identifier les fichiers modifiés avec `git diff --name-only main...HEAD`
2. Trouver des exemples de tests existants pour référence de style
3. Créer les fichiers de test selon les conventions du projet

### Output

Fichiers de test créés suivant les conventions du projet.

### Critère de succès
- Tests créés pour tous les nouveaux chemins de code
- Tests suivent le pattern du projet
- Tests sont syntaxiquement valides

---

## Étape 9: Verify Tests

### Objectif
Exécuter les tests et s'assurer qu'ils passent.

### Commandes de test

| Framework | Commande |
|-----------|----------|
| Jest | `npm test` ou `npx jest` |
| Vitest | `npm test` ou `npx vitest run` |
| Pytest | `pytest` |
| Cargo | `cargo test` |
| Go | `go test ./...` |

### Processus

```bash
# Run tests
{test_command}

# Si échec :
# 1. Parser les erreurs
# 2. Identifier le test qui fail
# 3. Analyser si bug dans le code ou dans le test
# 4. Fix approprié
# 5. Commit : fix(test): correct {test_name}
# 6. Retry
```

### Gestion des flaky tests

Si un test fail de manière intermittente :
1. Re-run 2 fois
2. Si toujours flaky → isoler le test
3. Marquer comme `skip` avec TODO si nécessaire

### Critère de succès
- Tous les tests passent
- Pas de tests skipped (sauf justification)
- Coverage acceptable

---

## Étape 10: Create PR

### Objectif
Créer une Pull Request complète et bien documentée.

### Processus

```bash
# 1. Push la branche
git push -u origin feature/nom-feature

# 2. Créer la PR via gh CLI
gh pr create --title "{titre}" --body "{body}"
```

### Génération du titre

Format : `{type}: {description courte}`

Exemples :
- `feat: add share button to article page`
- `fix: resolve pagination bug on mobile`

### Génération du body

```markdown
## Summary
{Description de la feature en 2-3 phrases, extraite de la description initiale}

## Changes
{Liste des changements principaux, extraite des commits}
- Add ShareButton component
- Integrate share functionality in ArticlePage
- Add analytics tracking for shares

## Testing
- [x] Build passes
- [x] Lint passes
- [x] Type check passes
- [x] Unit tests pass
- [x] Manual testing done

## Review Notes
{Notes issues de la code review si pertinent}

---
🤖 Generated with [Claude Code](https://claude.ai/claude-code) using /apex
```

### Critère de succès
- PR créée avec succès
- Titre et description appropriés
- URL de la PR retournée

---

## Diagramme de flux complet

```
                    ┌─────────────┐
                    │   START     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Parse args  │
                    │ & flags     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Git checks  │◄──────┐
                    └──────┬──────┘       │
                           │              │
                    ┌──────▼──────┐       │
                    │ 1. Init     │       │
                    │    Branch   │       │
                    └──────┬──────┘       │
                           │              │
                    ┌──────▼──────┐       │
                    │ 2. Analyze  │       │
                    │   (Analyst) │       │
                    └──────┬──────┘       │
                           │              │
                    ┌──────▼──────┐       │
                    │ 3. Plan     │       │
                    │ (Architect) │       │
                    └──────┬──────┘       │
                           │              │
                    ┌──────▼──────┐       │
                    │ 4. Execute  │       │
                    │ (Developer) │       │
                    └──────┬──────┘       │
                           │              │
                    ┌──────▼──────┐       │
              ┌─────│ 5. Validate │       │
              │     └──────┬──────┘       │
              │            │              │
         fail │     ┌──────▼──────┐       │
              │     │  --review?  │       │
              │     └──────┬──────┘       │
              │            │yes           │
              │     ┌──────▼──────┐       │
              │     │ 6. Review   │       │
              │     │ (Reviewer)  │       │
              │     └──────┬──────┘       │
              │            │              │
              │     ┌──────▼──────┐       │
              └────►│ 7. Fix      │───────┘
                    │   Issues    │  (retry validation)
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  --tests?   │
                    └──────┬──────┘
                           │yes
                    ┌──────▼──────┐
                    │ 8. Add      │
                    │   Tests (QA)│
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
              ┌─────│ 9. Verify   │
              │     │    Tests    │
              │     └──────┬──────┘
              │            │
         fail │     ┌──────▼──────┐
              └────►│ Fix & Retry │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ 10. Create  │
                    │     PR      │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    END      │
                    │  (PR URL)   │
                    └─────────────┘
```

---

## Récupération et reprise

### Sauvegarde d'état

À chaque étape complétée, l'état est implicitement sauvegardé via :
- Les commits git
- Les fichiers générés dans `.apex/` (`plan.md`, `review.md`)

### Reprise après interruption

Si le workflow est interrompu :
1. Checkout la branche existante
2. Analyser les commits existants
3. Déterminer la dernière étape complétée
4. Reprendre à l'étape suivante

### Commande de reprise

```
/apex --resume
```

Détecte automatiquement où reprendre basé sur :
- Existence de la branche `feature/*`
- Présence de `.apex/plan.md` → étape 3 complétée
- Présence de `.apex/review.md` → étape 6 complétée
- Nombre de commits depuis main → estimation de la progression
