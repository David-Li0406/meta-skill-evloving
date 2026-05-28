---
name: optimisation-backend
description: Objectifs et politiques d'optimisation des performances backend (Niveau POURQUOI)
workflows:
  - template: wf-evolution
    phase: Réalisation
---
# Politique de Performance Backend

Tu définis les **objectifs et standards** de performance backend et API.

## Rôle de cet Agent (Niveau POURQUOI)

> **Ce que tu fais** : Définir les OBJECTIFS de performance et les standards à atteindre
> **Ce que tu ne fais pas** : Implémenter les optimisations (code, requêtes, cache)
>
> → Process d'optimisation : `web-dev-process/agents/testing/performance`
> → Implémentation Node.js : Skills backend spécialisés
> → Implémentation WordPress : `wordpress-gutenberg-expert/agents/performance/*`

```
┌─────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : POURQUOI (direction-technique) ← ICI                │
│  → "Pourquoi ces cibles ? Scalabilité et UX"                    │
│  → "Standards : p95 < 200ms, throughput > 1000 RPS"             │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : QUOI (web-dev-process)                              │
│  → "Quoi optimiser ? Requêtes, cache, pooling"                  │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : COMMENT (frameworks spécifiques)                    │
│  → "Code : Redis, query optimization, batch processing..."      │
└─────────────────────────────────────────────────────────────────┘
```
---
## Objectifs de Performance

### Latence API - Cibles

| Percentile | Cible | Acceptable | Alerte |
|------------|-------|------------|--------|
| **p50** (médiane) | < 50ms | < 100ms | > 200ms |
| **p95** | < 200ms | < 500ms | > 1s |
| **p99** | < 500ms | < 1s | > 2s |
| **p99.9** | < 2s | < 5s | > 10s |

### Throughput - Cibles

| Contexte | Cible | Justification |
|----------|-------|---------------|
| **API standard** | > 1000 RPS | Charge normale |
| **API lecture** | > 5000 RPS | Endpoints GET simples |
| **API écriture** | > 500 RPS | Endpoints mutants |
| **Batch/Import** | > 10000 items/min | Traitements bulk |

### Base de Données - Cibles

| Métrique | Cible | Alerte | Action |
|----------|-------|--------|--------|
| Query time (p95) | < 50ms | > 200ms | Optimisation index |
| Connection pool usage | < 70% | > 90% | Scaling pool |
| Slow queries (> 1s) | 0 | > 5/min | Investigation urgente |
| N+1 queries | 0 | > 0 | Refactoring |
---
## Politiques de Performance

### 1. Politique de Requêtes DB

| Aspect | Politique |
|--------|-----------|
| **N+1 queries** | Interdit (eager loading obligatoire) |
| **Index** | Obligatoire sur colonnes filtrées/triées |
| **Pagination** | Cursor-based pour collections > 100 items |
| **Timeout** | Max 5s pour requêtes normales |
| **Query logging** | Activé en dev, slow-log en prod |

### 2. Politique de Cache

| Donnée | Stratégie | TTL Recommandé |
|--------|-----------|----------------|
| **Données statiques** | Cache-aside | 24h |
| **Sessions** | Write-through | 1h |
| **Résultats API** | Cache-aside + SWR | 5min |
| **Compteurs/Stats** | Write-behind | 1min |
| **Full-page** | CDN edge | Variable |

### Invalidation

| Stratégie | Quand Utiliser |
|-----------|----------------|
| **TTL-based** | Données peu sensibles à la fraîcheur |
| **Event-driven** | Données critiques, cohérence requise |
| **Versioned keys** | Déploiements, changements de schéma |

### 3. Politique de Connection Pooling

| Ressource | Min Pool | Max Pool | Idle Timeout |
|-----------|----------|----------|--------------|
| **Database** | 5 | 20 | 30s |
| **Redis** | 5 | 50 | 60s |
| **External APIs** | 2 | 10 | 30s |

### 4. Politique de Traitement Asynchrone

| Opération | Stratégie |
|-----------|-----------|
| **Emails** | Queue obligatoire |
| **Notifications** | Queue obligatoire |
| **Imports > 100 items** | Background job |
| **Rapports** | Background job + notification |
| **Webhooks** | Queue avec retry |

### 5. Politique de Rate Limiting

| Endpoint | Limite | Fenêtre | Action dépassement |
|----------|--------|---------|-------------------|
| **Auth/login** | 5 | 15 min | Block IP |
| **API standard** | 1000 | 1 min | 429 + Retry-After |
| **API heavy** | 100 | 1 min | 429 + Retry-After |
| **Webhooks incoming** | 10000 | 1 min | Queue overflow |
---
## Questions de Clarification

Avant d'optimiser :

### Contexte
- ❓ Quel est le profil de charge ? (lecture/écriture ratio)
- ❓ Quels sont les endpoints les plus utilisés ?
- ❓ Y a-t-il des SLA contractuels ?

### État Actuel
- ❓ Quelles sont les latences actuelles (p50, p95, p99) ?
- ❓ Y a-t-il un APM en place ?
- ❓ Quelles sont les requêtes les plus lentes ?

### Contraintes
- ❓ Budget infrastructure ? (instances, Redis, CDN)
- ❓ Contraintes de cohérence des données ?
- ❓ Legacy systems à intégrer ?
---
## Checklist par Phase

### Phase Conception

- [ ] SLA définis
- [ ] Profil de charge estimé
- [ ] Stratégie de cache définie
- [ ] Architecture async identifiée

### Phase Développement

- [ ] N+1 queries éliminées
- [ ] Index créés sur colonnes requises
- [ ] Cache implémenté pour données fréquentes
- [ ] Jobs async pour opérations longues

### Phase Review

- [ ] Load tests passés
- [ ] Aucune requête > 1s
- [ ] Rate limiting configuré
- [ ] Timeouts configurés

### Phase Production

- [ ] APM configuré
- [ ] Slow query log activé
- [ ] Alertes latence configurées
- [ ] Dashboard métriques
---
## Anti-Patterns à Éviter

| Anti-Pattern | Problème | Solution |
|--------------|----------|----------|
| **N+1 queries** | O(n) requêtes au lieu de O(1) | Eager loading |
| **SELECT *** | Données inutiles transférées | Sélection explicite |
| **OFFSET pagination** | Lent pour grandes pages | Cursor pagination |
| **Sync processing** | Blocage de l'API | Async/queue |
| **Cache sans TTL** | Stale data indéfinie | TTL obligatoire |
| **No connection pool** | Overhead connexions | Pooling |
---
## Métriques de Suivi

| Métrique | Cible | Alerte | Action |
|----------|-------|--------|--------|
| API latency p95 | < 200ms | > 500ms | Optimisation urgente |
| DB query p95 | < 50ms | > 200ms | Index/query review |
| Error rate | < 0.1% | > 1% | Investigation |
| Cache hit ratio | > 90% | < 70% | Stratégie cache |
| Queue backlog | < 100 | > 1000 | Scale workers |
---
## Outils de Diagnostic (Recommandés)

| Type | Outil | Usage |
|------|-------|-------|
| **APM** | Datadog, New Relic, Sentry | Tracing distribué |
| **Profiling** | Flamegraph, pprof | Hotspots |
| **DB Analysis** | EXPLAIN ANALYZE, pg_stat_statements | Requêtes |
| **Load Testing** | k6, Artillery, JMeter | Validation |
---
## Points d'Escalade

| Situation | Action | Responsable |
|-----------|--------|-------------|
| p95 > 1s | War room optimisation | Tech Lead |
| DB CPU > 80% | Scaling vertical/horizontal | DevOps |
| Queue backlog croissant | Scale workers | DevOps |
| Cache miss > 50% | Review stratégie cache | Tech Lead |
---
## Références

| Aspect | Agent de Référence |
|--------|-------------------|
| Process performance | `web-dev-process/agents/testing/performance` |
| Architecture | `architecture/architecture-systeme` |
| Implémentation cache | Skills backend spécialisés |
| Performance WordPress | `wordpress-gutenberg-expert/agents/performance/*` |

### Ressources Externes

- [High Scalability](http://highscalability.com/) - Patterns à grande échelle
- [Martin Fowler - Patterns](https://martinfowler.com/) - Architecture patterns

## Livrables

| Livrable | Description |
|----------|-------------|
| Stratégie de cache backend | Document définissant les niveaux de cache et stratégies d'invalidation |
| Plan d'optimisation requêtes | Analyse des requêtes N+1, index manquants avec plan de correction |
| Architecture de scalabilité | Stratégies load balancing, sharding, réplication pour montée en charge |
