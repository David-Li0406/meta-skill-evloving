# Index des Templates de Workflows

> 5 templates réutilisables couvrant tous les types de missions d'une agence web.

## Vue d'Ensemble

| Template | ID | Phases | Durée | Usage |
|----------|-----|--------|-------|-------|
| [Création](./creation.md) | `wf-creation` | 4 | 5-15j | Nouveau projet from scratch |
| [Refonte](./refonte.md) | `wf-refonte` | 5 | 8-20j | Migration, modernisation |
| [Évolution](./evolution.md) | `wf-evolution` | 4 | 2-8j | Feature, amélioration |
| [Audit](./audit.md) | `wf-audit` | 4 | 3-10j | Diagnostic, analyse |
| [Support](./support.md) | `wf-support` | 4 | 1h-5j | Tickets, incidents |

---

## Mapping Template → Cas d'Usage

### Création (`wf-creation`)

```
BRIEF → CONCEPTION → PRODUCTION → LIVRAISON
```

**Quand l'utiliser:**
- Nouveau site web
- Nouvelle application
- Nouvelle identité visuelle
- Nouveau composant/feature majeure
- Nouveau design system

**Rôles concernés:**
- UX/UI Designer
- Développeurs (front, back)
- Chef de projet
- Directeur artistique

---

### Refonte (`wf-refonte`)

```
AUDIT → ANALYSE → CONCEPTION → MIGRATION → BASCULE
```

**Quand l'utiliser:**
- Refonte de site existant
- Migration technologique
- Changement d'identité
- Modernisation legacy
- Fusion de plateformes

**Rôles concernés:**
- Architecte technique
- DevOps
- UX Designer
- Développeurs

---

### Évolution (`wf-evolution`)

```
DEMANDE → SPECIFICATION → REALISATION → DEPLOIEMENT
```

**Quand l'utiliser:**
- Nouvelle fonctionnalité
- Amélioration existante
- Optimisation performance
- Correction de bug
- Petite évolution design

**Rôles concernés:**
- Développeurs
- QA/Testeurs
- Chef de projet
- Product Owner

---

### Audit (`wf-audit`)

```
CADRAGE → COLLECTE → ANALYSE → RESTITUTION
```

**Quand l'utiliser:**
- Audit technique
- Audit UX/UI
- Audit SEO
- Audit sécurité
- Audit accessibilité
- Benchmark concurrentiel

**Rôles concernés:**
- Experts spécialisés
- Consultants
- Analystes
- Direction technique

---

### Support (`wf-support`)

```
RECEPTION → DIAGNOSTIC → RESOLUTION → CLOTURE
```

**Quand l'utiliser:**
- Ticket client
- Incident production
- Demande d'information
- Bug report
- Réclamation

**Rôles concernés:**
- Support N1/N2/N3
- Développeurs (escalade)
- Account manager
- Responsable support

---

## Usage dans les Agents

### Référencer un workflow dans un agent

```yaml
---
name: mon-agent
description: Description de l'agent
workflows:
  - id: creation
    template: wf-creation
    name: Création Nouveau Projet
    duration: 10-15 jours
  - id: refonte
    template: wf-refonte
    name: Refonte Existant
    duration: 15-20 jours
---
```

### Étendre un template

Les agents peuvent étendre un template en ajoutant des étapes spécifiques:

```yaml
workflows:
  - id: creation-ux
    template: wf-creation
    extensions:
      - phase: CONCEPTION
        add_activities:
          - Tests utilisateurs
          - A/B testing
```

---

## Métriques de Couverture

| Skill | Templates Applicables | Couverture Actuelle |
|-------|----------------------|---------------------|
| project-management | creation, refonte, evolution | 0% |
| ux-ui-design | creation, refonte, audit | 7.4% |
| marketing | creation, evolution, audit | 0.85% |
| frontend-developer | creation, refonte, evolution | 0% |
| backend-developer | creation, refonte, evolution | 0% |
| devops | evolution, audit, support | 0% |
| support-client | support | 0% |

**Objectif:** 80% des agents avec workflows référencés

---

## Prochaines Étapes

1. [ ] Appliquer les templates au skill pilote (project-management)
2. [ ] Valider l'approche avec 2-3 agents
3. [ ] Industrialiser l'ajout de workflows
4. [ ] Créer un script d'aide à l'ajout de workflows
5. [ ] Définir les métriques de suivi

---

## Références

- [WORKFLOW-GAP-ANALYSIS.md](../docs/analysis/WORKFLOW-GAP-ANALYSIS.md)
- [ADR-003: Format Markdown](../docs/adr/003-markdown-agent-format.md)
- [ADR-006: Learning Loop](../docs/adr/006-learning-loop-system.md)
