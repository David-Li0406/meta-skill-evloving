---
name: cicd-orchestrator
description: Orchestrateur pour les principes CI/CD et automatisation (Niveau QUOI)
workflows:
  - id: wdp-setup-cicd
    template: wf-creation
    phase: Production
    name: Pipelines CI/CD
    duration: 0.5 jour
---

# Orchestrateur CI/CD

Ce module coordonne la mise en place de l'intégration et du déploiement continus.

## Rôle de cet Agent (Niveau QUOI)

> **Ce que tu fais** : Définir QUOI mettre en place (stages, workflows, process)
> **Ce que tu ne fais pas** :
> - Décisions stratégiques → `direction-technique/infrastructure/strategie-cicd`
> - Code YAML spécifique → Skills technologiques (`wordpress-*/tooling/cicd-pipelines`)

```
┌─────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : POURQUOI (direction-technique/infrastructure)       │
│  → Politiques, quality gates, seuils, critères de succès       │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : QUOI (web-dev-process/setup/cicd) ← ICI            │
│  → Stages, workflows, bonnes pratiques génériques              │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : COMMENT (wordpress-*/tooling/cicd-pipelines)       │
│  → YAML GitHub Actions/GitLab CI, scripts, configurations      │
└─────────────────────────────────────────────────────────────────┘
```

## Agents Spécialisés

| Agent | Responsabilité |
|-------|----------------|
| `ci-principles.md` | Pipelines de validation, tests, qualité |
| `cd-principles.md` | Déploiement, environnements, rollback |
| `deployment-strategies.md` | Rolling, Blue-Green, Canary, Feature Flags |

## Contextualisation ADR-005

### Couche Métier (Global)
> Pratique standard de l'industrie pour CI/CD.

Les pipelines CI/CD suivent des standards universels : stages (setup, build, test, quality, deploy), parallélisation pour performance, fail-fast principle, caching des dépendances, artifacts pour traçabilité, et stratégies de déploiement (rolling, blue-green, canary). Les outils (GitHub Actions, GitLab CI, Jenkins) partagent ces concepts fondamentaux.

### Couche Agence (Spécifique)
> Adaptations selon plateforme et processus agence.

**Questions à poser :**
- Quelle plateforme CI/CD utiliser ? (GitHub Actions, GitLab CI, Jenkins)
- Y a-t-il des workflows agence réutilisables ? (templates, actions custom)
- Quels sont les quality gates standards ? (couverture min, lint obligatoire)
- Comment sont gérés les secrets en CI ? (GitHub Secrets, GitLab Variables)
- Y a-t-il un pipeline de référence ? (starter template agence)

### Couche Projet (Exception)
> Exceptions selon infrastructure et besoins projet.

**Questions à poser :**
- Y a-t-il des contraintes de déploiement ? (approbations manuelles, horaires)
- Des tests spécifiques sont-ils requis ? (E2E, performance, sécurité)
- Faut-il adapter les stages ? (étapes supplémentaires, audits)
- Y a-t-il des environnements multiples ? (multi-région, A/B testing)
- Des notifications spécifiques ? (Slack, email, outils client)

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTINUOUS INTEGRATION (CI)                  │
│                                                                 │
│   Code Push ──▶ Build ──▶ Tests ──▶ Quality Checks ──▶ Artifact│
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    CONTINUOUS DELIVERY (CD)                     │
│                                                                 │
│   Artifact ──▶ Deploy Staging ──▶ Tests E2E ──▶ Approval ──▶  │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    CONTINUOUS DEPLOYMENT                        │
│                                                                 │
│   ──▶ Deploy Production (automatique, sans approval manuelle)  │
└─────────────────────────────────────────────────────────────────┘
```

## Stages Recommandés

| Stage | Objectif | Contenu |
|-------|----------|---------|
| `setup` | Préparation | Install deps, restore cache |
| `build` | Compilation | Transpile, bundle |
| `test` | Validation | Unit, integration (parallel) |
| `quality` | Qualité | Lint, typecheck, coverage |
| `security` | Sécurité | Audit deps, SAST |
| `deploy` | Livraison | Staging → Prod |

## Bonnes Pratiques

### DO ✅

1. **Fail Fast** : Exécuter les tests rapides en premier
2. **Paralléliser** : Maximiser l'utilisation des runners
3. **Cacher** : Réutiliser node_modules, build cache
4. **Rollback** : Toujours pouvoir revenir en arrière

### DON'T ❌

1. **Skipper les tests** : `git push --no-verify`
2. **Merge sans CI** : Bypass de la validation
3. **Secrets en clair** : Dans le code ou les logs
4. **Déployer le vendredi** : Sans capacité de réaction

## Références

| Aspect | Où trouver |
|--------|------------|
| Seuils qualité, politiques | `direction-technique/infrastructure/strategie-cicd` |
| YAML GitHub Actions WordPress | `wordpress-gutenberg-expert/agents/tooling/cicd-pipelines` |
| YAML GitLab CI WordPress | `wordpress-gutenberg-expert/agents/tooling/gitlab-ci` |
| Principes CI détaillés | `ci-principles.md` |
| Principes CD détaillés | `cd-principles.md` |
| Stratégies de déploiement | `deployment-strategies.md` |

## Livrables

| Livrable | Description |
|----------|-------------|
| CI/CD Configuration Files | Fichiers de configuration GitHub Actions/GitLab CI/Jenkins |
| Pipeline Documentation | Documentation complète des pipelines CI/CD |
| Environment Setup Guide | Guide de configuration des environnements et secrets |
