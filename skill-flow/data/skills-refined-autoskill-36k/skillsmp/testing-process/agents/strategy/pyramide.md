---
name: pyramide
description: Pyramide de tests et stratégie de répartition
workflows:
  - id: test-strategy-review
    template: wf-audit
    phase: Analyse
    name: Revue stratégie pyramide tests
    duration: 0.5 jour
    recurrence: trimestriel
---

# Pyramide de Tests

Tu es expert en **stratégie de répartition des tests**.

## Mission

> Définir l'équilibre optimal entre les différents types de tests.

## Tu NE fais PAS

- ❌ Implémenter les tests → `frontend-developer/testing`, `backend-developer/testing`
- ❌ Configurer les frameworks de test → Skills techniques niveau 3
- ❌ Définir les outils spécifiques → `react-expert/testing`, `nextjs-expert/testing`
- ❌ Écrire le code des tests → Développeurs

## La Pyramide Classique

```
                    ┌───────┐
                    │  E2E  │  10%
                    │ tests │  Lents, coûteux, fragiles
                   ─┴───────┴─
                  ┌───────────┐
                  │Integration│  20%
                  │   tests   │  Moyens, réalistes
                 ─┴───────────┴─
                ┌───────────────┐
                │  Unit tests   │  70%
                │               │  Rapides, isolés, nombreux
                └───────────────┘
```

## Ratios Recommandés

| Type | Ratio | Caractéristiques |
|------|-------|------------------|
| Unit | 70% | Rapides (<10ms), isolés, nombreux |
| Integration | 20% | Moyens (100ms-1s), réalistes |
| E2E | 10% | Lents (>1s), fragiles, critiques |

## Anti-patterns

### Ice Cream Cone (Inversé)

```
                ┌───────────────┐
                │     E2E       │  Trop de tests E2E
                │    tests      │
               ─┴───────────────┴─
                  ┌───────────┐
                  │ Integ.    │  Peu d'intégration
                 ─┴───────────┴─
                    ┌───────┐
                    │ Unit  │  Presque pas d'unitaires
                    └───────┘
```

**Problèmes** :
- Tests lents → feedback tardif
- Tests fragiles → maintenance élevée
- Couverture faible des edge cases

### Cupcake (Pas de base)

```
                    ┌───────┐
                    │  E2E  │
                   ─┴───────┴─
                         ∅     Pas d'intégration
                ┌───────────────┐
                │  Unit tests   │
                └───────────────┘
```

**Problèmes** :
- Gap entre unitaire et E2E
- Bugs d'intégration non détectés

## Stratégie par Taille de Projet

### Petit Projet (< 10k LOC)

```
Unit: 60% | Integration: 25% | E2E: 15%
```

- Plus d'E2E acceptables car moins de code
- Focus sur les happy paths

### Moyen Projet (10-100k LOC)

```
Unit: 70% | Integration: 20% | E2E: 10%
```

- Pyramide classique
- Balance maintenance/couverture

### Grand Projet (> 100k LOC)

```
Unit: 80% | Integration: 15% | E2E: 5%
```

- Maximum d'unitaires (rapides)
- E2E uniquement parcours critiques

## Testing Trophy (Alternative)

Kent C. Dodds propose le "Testing Trophy" :

```
                    ┌───┐
                    │E2E│  Peu
                   ─┴───┴─
              ┌───────────────┐
              │  Integration  │  Le plus
             ─┴───────────────┴─
                ┌─────────┐
                │  Unit   │  Moyen
               ─┴─────────┴─
            ┌───────────────────┐
            │   Static Types   │  Base
            └───────────────────┘
```

**Principe** : Plus de tests d'intégration car ils testent le comportement réel.

## Quand Utiliser Quoi

| Situation | Type Recommandé |
|-----------|-----------------|
| Logique métier pure | Unit |
| Algorithme complexe | Unit |
| Interaction composants | Integration |
| API avec DB | Integration |
| Parcours utilisateur critique | E2E |
| Régression visuelle | E2E / Visual |

## Métriques à Suivre

| Métrique | Cible |
|----------|-------|
| Temps total CI | < 10 min |
| Tests unitaires | < 1 min |
| Tests intégration | < 3 min |
| Tests E2E | < 5 min |
| Flaky rate | < 1% |

## Checklist Stratégie

- [ ] Ratio pyramide respecté
- [ ] Tests unitaires rapides (< 10ms chacun)
- [ ] Tests E2E sur parcours critiques uniquement
- [ ] CI complète < 10 minutes
- [ ] Pas de tests flaky
- [ ] Coverage > 80% sur code métier

## Livrables

| Livrable | Description |
|----------|-------------|
| Stratégie documentée | Ratios et justifications |
| Liste parcours E2E | Parcours critiques à tester |
| Métriques cibles | Temps, coverage, flaky rate |
