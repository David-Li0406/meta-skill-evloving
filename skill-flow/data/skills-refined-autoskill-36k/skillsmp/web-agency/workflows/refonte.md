---
name: refonte
description: Workflow pour une refonte de site existant
---

# Workflow : Refonte Site Existant

Ce workflow guide la composition des skills pour une refonte de site.

## Spécificités Refonte

Une refonte diffère d'un nouveau projet car :
- Il existe un historique à analyser
- Des données à migrer
- Des utilisateurs existants à gérer
- Des risques de régression

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        WORKFLOW REFONTE                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Phase 0        Phase 1         Phase 2         Phase 3        Phase 4      │
│  AUDIT          AVANT-PROJET    CONCEPTION      DEV/MIGRATION  BASCULE      │
│                                                                              │
│  ┌─────────┐   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │
│  │ Audit   │──►│ Brief   │───►│ Specs   │───►│ Code    │───►│ Go-Live │   │
│  │ existant│   │ Refonte │    │ Migrat° │    │ Tests   │    │ Bascule │   │
│  │ Risques │   │ Devis   │    │ Design  │    │ Import  │    │ Redirect│   │
│  └─────────┘   └─────────┘    └─────────┘    └─────────┘    └─────────┘   │
│                                                                              │
│  Skills:        Skills:        Skills:        Skills:        Skills:        │
│  • dir-tech     • proj-mgmt    • dir-tech     • wordpress    • dir-tech    │
│  • strategy     • dir-tech     • design-sys   • web-dev      • proj-mgmt   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Phase 0 : Audit (Spécifique Refonte)

**Objectif** : Comprendre l'existant avant de proposer

### Étapes

| # | Action | Skill | Agent | Output |
|---|--------|-------|-------|--------|
| 1 | Audit technique | direction-technique | avant-projet/audit-existant | Rapport technique |
| 2 | Audit performance | direction-technique | performance/audit-performance | Métriques actuelles |
| 3 | Audit sécurité | direction-technique | securite/audit-securite | Vulnérabilités |
| 4 | Audit UX/contenu | strategy (si dispo) | - | Recommandations UX |
| 5 | Analyse risques | direction-technique | estimation/analyse-risques | Matrice risques |

### Livrables Phase 0

- [ ] Rapport d'audit technique
- [ ] Inventaire des fonctionnalités existantes
- [ ] Liste des données à migrer
- [ ] Matrice des risques
- [ ] Recommandations (refonte partielle vs totale)

### Points d'Escalade

- Si dette technique > 40% du budget refonte → Repenser le périmètre
- Si données non-exportables → Étude migration manuelle

---

## Phase 1 : Avant-Projet

**Objectif** : Cadrer la refonte avec les enseignements de l'audit

### Différences avec Nouveau Projet

| Aspect | Nouveau Projet | Refonte |
|--------|----------------|---------|
| Brief | Partir de zéro | Partir de l'audit |
| Estimation | Standard | + 20-30% pour migration |
| Risques | Standards | Migration, régression, SEO |

### Étapes

| # | Action | Skill | Agent | Output |
|---|--------|-------|-------|--------|
| 1 | Brief enrichi | project-management | avant-projet/formalisation-brief | Brief + audit |
| 2 | Chiffrage migration | direction-technique | estimation/estimation-detaillee | J/H migration |
| 3 | Plan de migration | direction-technique | specification/specification-technique | Plan migration |
| 4 | Proposition refonte | project-management | avant-projet/redaction-proposition | Proposition |

### Livrables Phase 1

- [ ] Brief refonte (incluant périmètre vs existant)
- [ ] Estimation avec ligne "migration"
- [ ] Plan de migration des données
- [ ] Stratégie de bascule (big bang vs progressive)

---

## Phase 2 : Conception

**Objectif** : Concevoir en tenant compte de l'existant

### Spécificités

- **SEO** : Mapping des URLs anciennes → nouvelles
- **Données** : Schéma de migration
- **Fonctionnel** : Comparatif existant vs nouveau

### Étapes Additionnelles

| # | Action | Skill | Agent | Output |
|---|--------|-------|-------|--------|
| 1 | Mapping URLs | wordpress-* | seo-expert | Redirections 301 |
| 2 | Schéma migration | direction-technique | specification/modelisation-donnees | Scripts migration |
| 3 | Gap analysis | direction-technique | specification/specification-technique | Delta fonctionnel |

---

## Phase 3 : Développement & Migration

**Objectif** : Développer + migrer en parallèle

### Workflow Parallèle

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   DÉVELOPPEMENT                    MIGRATION                     │
│   (nouveau site)                   (données)                     │
│                                                                  │
│   ┌────────────┐                  ┌────────────┐                │
│   │ Thème      │                  │ Export     │                │
│   │ Plugins    │                  │ données    │                │
│   │ Blocks     │                  │ existantes │                │
│   └─────┬──────┘                  └─────┬──────┘                │
│         │                               │                        │
│         │         ┌────────────┐        │                        │
│         └────────►│  STAGING   │◄───────┘                        │
│                   │ (fusion)   │                                 │
│                   └─────┬──────┘                                 │
│                         │                                        │
│                   ┌─────▼──────┐                                 │
│                   │   TESTS    │                                 │
│                   │ régression │                                 │
│                   └────────────┘                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Tests Spécifiques Refonte

| Type | Objectif | Skill |
|------|----------|-------|
| Migration | Données correctement importées | wordpress-*/testing |
| Régression | Fonctionnalités existantes OK | web-dev-process/testing |
| SEO | Redirections fonctionnelles | wordpress-*/seo-expert |
| Performance | Égale ou meilleure | direction-technique/performance |

---

## Phase 4 : Bascule (Spécifique Refonte)

**Objectif** : Basculer sans perdre de trafic ni de données

### Checklist Pré-Bascule

- [ ] Backup complet ancien site
- [ ] DNS TTL réduit à 5 min (48h avant)
- [ ] Redirections 301 configurées
- [ ] Migration finale des données (J-1)
- [ ] Tests smoke sur staging
- [ ] Monitoring en place
- [ ] Rollback plan documenté

### Stratégies de Bascule

#### Option 1 : Big Bang

```
22h00 : Backup final
22h30 : Migration données delta
23h00 : Switch DNS
23h30 : Tests smoke
00h00 : Surveillance renforcée
```

**Quand** : Petit site, faible trafic, peu de données

#### Option 2 : Progressive (Blue/Green)

```
Jour J   : Nouveau site sur nouveau domaine
Jour J+7 : 10% du trafic routé vers nouveau
Jour J+14: 50% du trafic
Jour J+21: 100% du trafic + redirections
```

**Quand** : Site critique, fort trafic

### Post-Bascule

| # | Action | Skill | Agent | Délai |
|---|--------|-------|-------|-------|
| 1 | Monitoring intensif | web-dev-process | maintenance/monitoring | 48h |
| 2 | Vérif SEO | wordpress-* | seo-expert | J+3 |
| 3 | Correction bugs | direction-technique | support/troubleshooting | J+7 |
| 4 | Désactivation ancien | - | - | J+30 |
| 5 | Bilan | project-management | - | J+30 |

### Points d'Escalade Bascule

| Situation | Action |
|-----------|--------|
| Erreurs 500 > 1% | Pause, diagnostic |
| Trafic chute > 20% | Vérifier redirections |
| Performance dégradée > 50% | Rollback potentiel |
| Données manquantes critiques | Rollback |

---

## Différences Clés vs Nouveau Projet

| Aspect | Nouveau Projet | Refonte |
|--------|----------------|---------|
| Phase 0 | Non | Audit obligatoire |
| Estimation | Standard | +20-30% migration |
| Tests | Standard | + régression + SEO |
| Livraison | Simple | Bascule planifiée |
| Rollback | Rare | Plan obligatoire |
| Durée totale | X | X + 30-50% |

## Références

- [Workflow nouveau projet](./nouveau-projet.md)
- [Points d'escalade](../orchestration/escalation.md)
