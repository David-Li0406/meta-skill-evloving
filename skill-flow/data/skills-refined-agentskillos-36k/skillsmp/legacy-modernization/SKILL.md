---
name: legacy-modernization
description: |-
  Expert modernisation de systèmes legacy - Strangler Fig, refactoring progressif, migration. Utilise ce skill quand: (1) moderniser une application legacy, (2) migration progressive, (3) refactoring à grande échelle, (4) dette technique critique, (5) réécriture partielle, (6) cohabitation ancien/nouveau système.
metadata:
  version: 1.0.0
  status: active
---

# Legacy Modernization Expert Skill

## Quick Start

```bash
# 1. Navigation rapide vers un agent
legacy-modernization/agents/assessment/audit        # Audit du legacy
legacy-modernization/agents/strategies/strangler    # Pattern Strangler Fig
legacy-modernization/agents/migration/data          # Migration de données
legacy-modernization/agents/refactoring/incremental # Refactoring progressif

# 2. Questions fréquentes
"Comment évaluer mon legacy ?"             → assessment/audit
"Quelle stratégie de migration ?"          → strategies/orchestrator
"Strangler Fig pattern ?"                  → strategies/strangler
"Migrer les données progressivement ?"     → migration/data
"Refactorer sans tout casser ?"            → refactoring/incremental
```

## Position dans l'Architecture

Ce skill est au **NIVEAU 3 : IMPLÉMENTATION**. Il implémente les stratégies de modernisation.

```
┌─────────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : STRATÉGIE (direction-technique)                         │
│  → POURQUOI : Décision de moderniser, budget, timeline              │
├─────────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : OPÉRATIONS                                              │
│  ┌────────────────────────────┐  ┌────────────────────────────┐    │
│  │     web-dev-process        │  │       lead-dev             │    │
│  │  QUOI : Phases du projet   │  │  QUI : Coordination        │    │
│  └────────────────────────────┘  └────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : IMPLÉMENTATION                                          │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │          legacy-modernization ← CE SKILL                    │    │
│  │  COMMENT : Strangler, migration, refactoring, testing       │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## Philosophie

> Moderniser progressivement, sans interrompre le business.

Ce skill :
- ✅ Évalue et audite les systèmes legacy
- ✅ Définit les stratégies de modernisation
- ✅ Implémente les patterns de migration
- ✅ Guide le refactoring progressif
- ✅ Assure la cohabitation ancien/nouveau

Il ne fait PAS :
- ❌ Les décisions stratégiques → `direction-technique`
- ❌ La gestion de projet → `project-management`
- ❌ L'implémentation techno spécifique → skills techniques

## Domaines et Agents (30 agents)

### 1. assessment/ - Évaluation du Legacy (6 agents)

Audit et analyse des systèmes existants.

| Agent | Responsabilité | Livrables |
|-------|----------------|-----------|
| `orchestrator` | Coordination évaluation | - |
| `audit` | Audit technique complet | Rapport d'audit |
| `debt-analysis` | Analyse dette technique | Matrice de dette |
| `risk-assessment` | Évaluation des risques | Risk register |
| `cost-estimation` | Estimation des coûts | Business case |
| `dependencies` | Cartographie dépendances | Dependency graph |

### 2. strategies/ - Stratégies de Modernisation (6 agents)

Patterns et approches de modernisation.

| Agent | Responsabilité | Pattern |
|-------|----------------|---------|
| `orchestrator` | Coordination stratégies | - |
| `strangler` | Strangler Fig Pattern | Remplacement progressif |
| `bubble-context` | Bubble Context | DDD bounded context |
| `branch-by-abstraction` | Branch by Abstraction | Abstraction layer |
| `parallel-run` | Parallel Run | Double exécution |
| `feature-flags` | Feature Flags | Bascule progressive |

### 3. migration/ - Migration de Données et APIs (6 agents)

Migration des données et interfaces.

| Agent | Responsabilité | Focus |
|-------|----------------|-------|
| `orchestrator` | Coordination migration | - |
| `data` | Migration de données | ETL, sync, validation |
| `api` | Migration d'APIs | Versioning, compatibility |
| `database` | Migration de schémas | Schema evolution |
| `sync` | Synchronisation bidirectionnelle | CDC, events |
| `rollback` | Stratégies de rollback | Réversibilité |

### 4. refactoring/ - Refactoring Progressif (6 agents)

Techniques de refactoring à grande échelle.

| Agent | Responsabilité | Techniques |
|-------|----------------|------------|
| `orchestrator` | Coordination refactoring | - |
| `incremental` | Refactoring incrémental | Small steps |
| `extract-service` | Extraction de services | Microservices |
| `seams` | Identification des seams | Points d'injection |
| `contracts` | Contrats d'interface | API contracts |
| `cleanup` | Nettoyage du code | Dead code, duplications |

### 5. testing/ - Tests pour Legacy (6 agents)

Stratégies de test spécifiques au legacy.

| Agent | Responsabilité | Techniques |
|-------|----------------|------------|
| `orchestrator` | Coordination testing | - |
| `characterization` | Tests de caractérisation | Golden master |
| `approval` | Approval testing | Snapshot |
| `coverage` | Couverture legacy | Seams coverage |
| `regression` | Tests de régression | Before/after |
| `integration` | Tests d'intégration | Contract testing |

**Total : 30 agents spécialisés**

## Règles de Routage

### Par Type de Question

| Question | Domaine |
|----------|---------|
| Évaluer, auditer le legacy | `assessment/` |
| Quelle stratégie adopter | `strategies/` |
| Migrer données, APIs | `migration/` |
| Refactorer progressivement | `refactoring/` |
| Tester le legacy | `testing/` |

### Par Mots-Clés

| Mots-clés | Agent |
|-----------|-------|
| audit, évaluation, état des lieux | `assessment/audit` |
| dette technique, technical debt | `assessment/debt-analysis` |
| strangler, fig, remplacement | `strategies/strangler` |
| bubble, bounded context, DDD | `strategies/bubble-context` |
| abstraction, interface, layer | `strategies/branch-by-abstraction` |
| feature flag, toggle, bascule | `strategies/feature-flags` |
| migration données, ETL, sync | `migration/data` |
| API versioning, breaking changes | `migration/api` |
| schema, database migration | `migration/database` |
| refactoring, extract, seams | `refactoring/incremental` |
| microservice, extract service | `refactoring/extract-service` |
| characterization test, golden master | `testing/characterization` |

## Arbre de Décision

```
Requête Legacy Modernization
│
├─ Phase d'évaluation ?
│  ├─ Audit technique → assessment/audit
│  ├─ Dette technique → assessment/debt-analysis
│  ├─ Risques → assessment/risk-assessment
│  ├─ Business case → assessment/cost-estimation
│  └─ Dépendances → assessment/dependencies
│
├─ Choix de stratégie ?
│  ├─ Remplacement progressif → strategies/strangler
│  ├─ Nouveau contexte isolé → strategies/bubble-context
│  ├─ Couche d'abstraction → strategies/branch-by-abstraction
│  ├─ Double exécution → strategies/parallel-run
│  └─ Bascule progressive → strategies/feature-flags
│
├─ Migration ?
│  ├─ Données → migration/data
│  ├─ APIs → migration/api
│  ├─ Schéma DB → migration/database
│  ├─ Synchronisation → migration/sync
│  └─ Plan de rollback → migration/rollback
│
├─ Refactoring ?
│  ├─ Approche incrémentale → refactoring/incremental
│  ├─ Extraire un service → refactoring/extract-service
│  ├─ Identifier les seams → refactoring/seams
│  ├─ Définir les contrats → refactoring/contracts
│  └─ Nettoyer → refactoring/cleanup
│
└─ Testing ?
   ├─ Caractériser le comportement → testing/characterization
   ├─ Approval testing → testing/approval
   ├─ Couverture → testing/coverage
   ├─ Régression → testing/regression
   └─ Intégration → testing/integration
```

## Patterns Clés

### 1. Strangler Fig Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                         FACADE/PROXY                            │
├─────────────────────────────────────────────────────────────────┤
│   ┌─────────────┐                     ┌─────────────┐          │
│   │   LEGACY    │ ──── routing ────▶  │    NEW      │          │
│   │   SYSTEM    │     progressif      │   SYSTEM    │          │
│   └─────────────┘                     └─────────────┘          │
│        │                                    │                   │
│        ▼                                    ▼                   │
│   Fonctionnalités                    Fonctionnalités           │
│   à migrer                           migrées                   │
└─────────────────────────────────────────────────────────────────┘

Phase 1: 100% legacy, 0% nouveau
Phase 2: 70% legacy, 30% nouveau
Phase 3: 30% legacy, 70% nouveau
Phase 4: 0% legacy, 100% nouveau
```

### 2. Branch by Abstraction

```
Étape 1: Créer l'abstraction
┌──────────┐     ┌──────────┐
│  Client  │────▶│  Legacy  │
└──────────┘     └──────────┘

Étape 2: Insérer l'interface
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │────▶│Interface │────▶│  Legacy  │
└──────────┘     └──────────┘     └──────────┘

Étape 3: Implémenter nouveau
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │────▶│Interface │──┬─▶│  Legacy  │
└──────────┘     └──────────┘  │  └──────────┘
                               │  ┌──────────┐
                               └─▶│   New    │
                                  └──────────┘

Étape 4: Basculer
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │────▶│Interface │────▶│   New    │
└──────────┘     └──────────┘     └──────────┘
```

### 3. Parallel Run

```typescript
async function processOrder(order: Order) {
  // Exécuter les deux systèmes en parallèle
  const [legacyResult, newResult] = await Promise.all([
    legacySystem.process(order),
    newSystem.process(order),
  ]);

  // Comparer les résultats
  const diff = compareResults(legacyResult, newResult);
  if (diff.hasDifferences) {
    logger.warn('Parallel run discrepancy', { diff, order });
    metrics.increment('parallel_run.discrepancy');
  }

  // Retourner le résultat du système de confiance
  return featureFlags.isEnabled('use_new_system')
    ? newResult
    : legacyResult;
}
```

## Interaction avec les Autres Skills

### Flux Entrants

```
direction-technique ──► legacy-modernization (décision → implémentation)
ddd ──► legacy-modernization (bounded contexts → extraction)
```

### Flux Sortants

```
legacy-modernization ──► backend-developer (implémentation nouveau système)
legacy-modernization ──► devops (infra, déploiement)
legacy-modernization ──► testing-process (stratégie de tests)
```

## Points d'Escalade

### Vers direction-technique

| Situation | Raison |
|-----------|--------|
| Choix stratégie (strangler vs rewrite) | Impact budget/timeline |
| Périmètre de migration | Décision business |
| Risques identifiés critiques | Validation |

### Vers l'humain

| Situation | Raison |
|-----------|--------|
| Logique métier non documentée | Connaissance tacite |
| Validation des données migrées | Responsabilité |
| Go/no-go bascule production | Décision business |

## Anti-Patterns à Éviter

| Anti-Pattern | Problème | Alternative |
|--------------|----------|-------------|
| Big Bang Rewrite | Risque élevé, long | Strangler Fig |
| Pas de tests avant refactoring | Régression | Characterization tests |
| Migration données en une fois | Downtime | Sync bidirectionnelle |
| Ignorer le legacy | Dette croissante | Bubble context |
| Copier-coller le legacy | Bugs copiés | Repenser le design |

## Skills Associés

| Skill | Niveau | Relation |
|-------|--------|----------|
| `direction-technique` | STRATÉGIE | Reçoit les directives |
| `ddd` | TRANSVERSAL | Bounded contexts |
| `backend-developer` | IMPLÉMENTATION | Nouveau système |
| `devops` | IMPLÉMENTATION | Infra, déploiement |
| `testing-process` | PROCESSUS | Stratégie de tests |

## Changelog

### v1.0.0
- Création initiale avec 5 domaines et 30 agents
- Couverture : assessment, strategies, migration, refactoring, testing
- Position : NIVEAU 3 IMPLÉMENTATION
- Patterns : Strangler Fig, Branch by Abstraction, Parallel Run
