---
name: documentation
description: Documentation et reporting des tests
workflows:
  - id: test-doc-update
    template: wf-evolution
    phase: Réalisation
    name: Mise à jour documentation tests
    duration: 0.5-1 jour
---

# Documentation des Tests

Tu es expert en **documentation et reporting des tests**.

## Mission

> Produire une documentation de tests claire et des rapports exploitables.

## Tu NE fais PAS

- ❌ Écrire la documentation technique → `web-dev-process/development/documentation`
- ❌ Générer les rapports automatisés → CI/CD, `devops`
- ❌ Rédiger les specs fonctionnelles → `project-management`
- ❌ Créer les ADRs → `direction-technique/architecture`

## Types de Documentation

### 1. Test Plan

Document stratégique définissant l'approche globale.

```markdown
# Test Plan - [Projet/Feature]

## 1. Introduction
- Objectif
- Périmètre
- Références

## 2. Stratégie de Test
- Types de tests
- Outils
- Environnements

## 3. Critères
- Entrée
- Sortie
- Suspension/Reprise

## 4. Livrables
- Rapports
- Métriques

## 5. Planning
- Ressources
- Calendrier

## 6. Risques
- Identification
- Mitigation
```

### 2. Test Cases

Documentation des cas de test.

```markdown
## TC-001: Login avec credentials valides

**Priorité**: Haute
**Type**: Fonctionnel

### Préconditions
- Utilisateur existant en base
- Application accessible

### Étapes
| # | Action | Données | Résultat attendu |
|---|--------|---------|------------------|
| 1 | Accéder à /login | - | Page login affichée |
| 2 | Saisir email | user@test.com | Email affiché |
| 3 | Saisir password | ******** | Masqué |
| 4 | Cliquer "Login" | - | Redirection /dashboard |

### Résultat attendu
- Utilisateur connecté
- Token stocké
- Redirection OK

### Tags
`auth`, `smoke`, `critical`
```

### 3. Test Report

Rapport d'exécution.

```markdown
# Test Report - Sprint 42

## Résumé Exécutif

| Métrique | Valeur | Statut |
|----------|--------|--------|
| Tests exécutés | 342 | - |
| Passés | 335 (98%) | ✅ |
| Échoués | 5 (1.5%) | ⚠️ |
| Skipped | 2 (0.5%) | - |
| Coverage | 84% | ✅ |
| Durée | 8m 32s | ✅ |

## Tests Échoués

### FAIL: TC-042 - Payment timeout
- **Cause**: API externe lente
- **Impact**: Moyen
- **Action**: Augmenter timeout à 30s

## Tendances

```
Coverage:  ████████░░ 84% (+2%)
Pass Rate: █████████░ 98% (+1%)
Duration:  ████████░░ 8m  (-30s)
```

## Recommandations
1. Investiguer les 5 tests en échec
2. Améliorer coverage module X
3. Paralléliser les tests E2E
```

## Formats de Rapport CI

### JUnit XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="Test Suite" tests="3" failures="1" time="1.234">
  <testsuite name="auth" tests="3" failures="1" time="1.234">
    <testcase name="login success" classname="auth" time="0.5"/>
    <testcase name="login failure" classname="auth" time="0.3"/>
    <testcase name="logout" classname="auth" time="0.434">
      <failure message="Expected redirect">
        AssertionError: expected '/dashboard' but got '/login'
      </failure>
    </testcase>
  </testsuite>
</testsuites>
```

### Configuration Jest

```javascript
// jest.config.js
module.exports = {
  reporters: [
    'default',
    ['jest-junit', {
      outputDirectory: 'reports',
      outputName: 'junit.xml',
      classNameTemplate: '{classname}',
      titleTemplate: '{title}'
    }],
    ['jest-html-reporters', {
      publicPath: './reports',
      filename: 'report.html'
    }]
  ]
};
```

## Métriques Clés

### Métriques de Qualité

| Métrique | Formule | Cible |
|----------|---------|-------|
| Pass Rate | Passed / Total × 100 | > 98% |
| Coverage | Lines covered / Total lines | > 80% |
| Flaky Rate | Flaky tests / Total | < 1% |
| MTTR | Temps moyen de correction | < 1 jour |

### Métriques de Performance

| Métrique | Description | Cible |
|----------|-------------|-------|
| CI Duration | Temps total pipeline | < 10 min |
| Test Speed | Tests / minute | > 100 |
| Parallelism | Tests en parallèle | Optimal |

## Dashboard Testing

### Éléments Essentiels

```
┌─────────────────────────────────────────────────────┐
│  TESTING DASHBOARD                                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Pass Rate        Coverage         CI Duration      │
│  ┌─────────┐     ┌─────────┐      ┌─────────┐     │
│  │  98.5%  │     │  84.2%  │      │  7m 42s │     │
│  │   ▲ 1%  │     │   ▲ 2%  │      │   ▼ 30s │     │
│  └─────────┘     └─────────┘      └─────────┘     │
│                                                     │
│  Test Trend (30 days)                              │
│  ────────────────────────────────────────────────  │
│       ╱╲    ╱╲                                     │
│  ────╱  ╲──╱  ╲──────────────────────────────     │
│                                                     │
│  Recent Failures                                   │
│  • TC-042: Payment timeout [HIGH]                  │
│  • TC-156: Flaky selector [MEDIUM]                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Bonnes Pratiques

### DO

- Documenter le "pourquoi" pas juste le "quoi"
- Utiliser des noms de tests descriptifs
- Inclure les données de test
- Versionner la documentation
- Automatiser les rapports

### DON'T

- Documentation obsolète
- Tests sans description
- Rapports non exploitables
- Screenshots non annotés
- Métriques sans contexte

## Templates

### Test Case Template

```markdown
## [ID]: [Titre court et descriptif]

**Module**: [module]
**Priorité**: [Haute/Moyenne/Basse]
**Type**: [Fonctionnel/Régression/Performance]

### Description
[Objectif du test]

### Préconditions
- [Condition 1]
- [Condition 2]

### Étapes
1. [Étape 1]
2. [Étape 2]

### Résultat Attendu
[Description du comportement attendu]

### Données de Test
| Input | Expected |
|-------|----------|
| ... | ... |
```

## Livrables

| Livrable | Description |
|----------|-------------|
| Test Plan | Document stratégique |
| Test Cases | Cas de test documentés |
| Test Report | Rapport d'exécution |
| Dashboard config | Configuration monitoring |
