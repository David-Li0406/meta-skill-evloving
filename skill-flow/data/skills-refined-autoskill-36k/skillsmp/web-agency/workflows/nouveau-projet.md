---
name: nouveau-projet
description: Workflow complet pour un nouveau projet client
---

# Workflow : Nouveau Projet Client

Ce workflow guide la composition des skills pour un nouveau projet de A à Z.

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        WORKFLOW NOUVEAU PROJET                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Phase 1        Phase 2         Phase 3         Phase 4        Phase 5      │
│  AVANT-PROJET   CONCEPTION      SETUP           DEV/TEST       LIVRAISON    │
│                                                                              │
│  ┌─────────┐   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐   │
│  │ Brief   │──►│ Specs   │───►│ Repo    │───►│ Code    │───►│ Recette │   │
│  │ Devis   │   │ Archi   │    │ CI/CD   │    │ Tests   │    │ Deploy  │   │
│  │ Contrat │   │ Design  │    │ Envs    │    │ Review  │    │ PV      │   │
│  └─────────┘   └─────────┘    └─────────┘    └─────────┘    └─────────┘   │
│                                                                              │
│  Skills:        Skills:        Skills:        Skills:        Skills:        │
│  • proj-mgmt    • dir-tech     • web-dev      • wordpress    • proj-mgmt   │
│  • dir-tech     • design-sys   • wordpress    • web-dev      • dir-tech    │
│                 • content                                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Phase 1 : Avant-Projet

**Objectif** : Comprendre le besoin, estimer, proposer

### Étapes

| # | Action | Skill | Agent | Output |
|---|--------|-------|-------|--------|
| 1 | Collecter le besoin | project-management | avant-projet/collecte-besoin | Extraction brute |
| 2 | Formaliser le brief | project-management | avant-projet/formalisation-brief | Brief structuré |
| 3 | Clarifier (si besoin) | project-management | avant-projet/questions-clarification | Questions client |
| 4 | Estimer commercialement | project-management | avant-projet/chiffrage | Estimation €/jours |
| 5 | Valider faisabilité | direction-technique | avant-projet/etude-faisabilite | Go/NoGo technique |
| 6 | Estimer techniquement | direction-technique | estimation/estimation-macro | Estimation j/h |
| 7 | Rédiger proposition | project-management | avant-projet/redaction-proposition | Proposition commerciale |

### Livrables Phase 1

- [ ] Brief client validé
- [ ] Estimation commerciale
- [ ] Estimation technique
- [ ] Proposition commerciale
- [ ] Contrat signé (hors skill)

### Point d'Escalade

Si estimation > 50 j/h ou budget > 50k€ → Validation direction

---

## Phase 2 : Conception

**Objectif** : Définir l'architecture, le design, les specs

### Étapes Séquentielles

| # | Action | Skill | Agent | Output |
|---|--------|-------|-------|--------|
| 1 | Choisir la stack | direction-technique | avant-projet/selection-stack | ADR stack |
| 2 | Définir l'architecture | direction-technique | architecture/architecture-applicative | Schéma archi |
| 3 | Spécifier techniquement | direction-technique | specification/specification-technique | Specs techniques |

### Étapes Parallèles (après specs)

| Action | Skill | Agent | Output |
|--------|-------|-------|--------|
| Design tokens | design-system-foundations | foundations/* | theme.json / tokens |
| Contenus | content (si disponible) | - | Arborescence, textes |
| Maquettes | design (si disponible) | - | Figma |

### Livrables Phase 2

- [ ] ADR choix de stack
- [ ] Architecture documentée
- [ ] Specs techniques
- [ ] Design tokens
- [ ] Maquettes (si applicable)

---

## Phase 3 : Setup

**Objectif** : Préparer l'environnement de développement

### Étapes

| # | Action | Skill | Agent | Output |
|---|--------|-------|-------|--------|
| 1 | Créer le repository | web-dev-process | setup/repository | Repo Git |
| 2 | Configurer Git | web-dev-process | setup/git-config | .gitignore, branches |
| 3 | Setup environnements | wordpress-* | tooling/local-dev | wp-env.json |
| 4 | Configurer CI/CD | web-dev-process | setup/cicd | GitHub Actions |
| 5 | Configurer qualité | web-dev-process | setup/quality-tools | ESLint, PHPCS |

### Livrables Phase 3

- [ ] Repository créé et configuré
- [ ] Environnements local/staging/prod
- [ ] Pipeline CI/CD fonctionnel
- [ ] Outils qualité configurés

---

## Phase 4 : Développement & Tests

**Objectif** : Implémenter et valider

### Boucle de Développement

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│    ┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐    │
│    │  Code  │────►│  Test  │────►│ Review │────►│ Merge  │    │
│    └────────┘     └────────┘     └────────┘     └────────┘    │
│         │                              │                        │
│         └──────────────────────────────┘                        │
│                   (si refus)                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Skills par Activité

| Activité | Skill | Agents |
|----------|-------|--------|
| Développement WP | wordpress-* | wp-core/*, gutenberg-blocks/*, theme/* |
| Tests unitaires | wordpress-* | testing/php-unit-tests, testing/js-unit-tests |
| Tests e2e | wordpress-* | testing/e2e-tests |
| Code review | web-dev-process | development/code-review |

### Livrables Phase 4

- [ ] Code complet et fonctionnel
- [ ] Tests passants (couverture selon standards)
- [ ] Code reviews approuvées
- [ ] Déploiement staging

---

## Phase 5 : Livraison

**Objectif** : Recetter, déployer, clôturer

### Étapes

| # | Action | Skill | Agent | Output |
|---|--------|-------|-------|--------|
| 1 | Préparer recette | project-management | livraison/plan-recette | Plan de recette |
| 2 | Créer grille tests | project-management | livraison/grille-recette | Grille de recette |
| 3 | Suivre anomalies | project-management | livraison/suivi-anomalies | Suivi bugs |
| 4 | Déployer prod | web-dev-process | deployment/production | Site en production |
| 5 | Rédiger PV | project-management | livraison/pv-recette | PV signé |
| 6 | Facturer | project-management | facturation/* | Facture |

### Livrables Phase 5

- [ ] Site en production
- [ ] PV de recette signé
- [ ] Documentation technique
- [ ] Facture envoyée

---

## Timeline Indicative

| Phase | Durée typique | Dépend de |
|-------|---------------|-----------|
| Avant-projet | 1-2 semaines | Réactivité client |
| Conception | 1-3 semaines | Complexité |
| Setup | 1-2 jours | Stack connue ou non |
| Développement | Variable | Scope |
| Livraison | 1 semaine | Bugs recette |

## Références

- [Composition des skills](../orchestration/composition.md)
- [Points d'escalade](../orchestration/escalation.md)
