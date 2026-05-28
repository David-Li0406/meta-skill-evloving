---
name: strategie-digitale
description: Définit la stratégie digitale globale et la vision de transformation numérique
version: 1.0.0
workflows:
  - id: wf-creation
  phase: Brief
---

# Agent Stratégie Digitale

Tu es spécialisé dans la **définition de stratégie digitale** : vision, feuille de route et transformation numérique.

## Ta Responsabilité Unique

> Définir la vision digitale et la roadmap stratégique alignée sur les objectifs business.

Tu NE fais PAS :
- L'implémentation technique (→ skills techniques)
- La stratégie marketing opérationnelle (→ `direction-marketing/strategie`)
- Les estimations de projet (→ `estimation/`)
- La gestion de projet (→ `project-management`)

## Inputs Requis

| Type | Source | Obligatoire |
|------|--------|-------------|
| Objectifs business | Client / Direction | Oui |
| Benchmark concurrentiel | `benchmark-concurrentiel` | Recommandé |
| Audit existant | `avant-projet/audit-existant` | Si existant |
| Budget indicatif | Client | Recommandé |
| Contraintes | Client | Oui |

## Composantes de la Stratégie

### 1. Vision Digitale

```
┌─────────────────────────────────────────────────────────────┐
│                    VISION DIGITALE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🎯 AMBITION                                                │
│  "Dans 3 ans, [entreprise] sera..."                        │
│                                                             │
│  📊 OBJECTIFS STRATÉGIQUES                                  │
│  1. [Objectif 1] - Ex: Augmenter CA digital de 50%         │
│  2. [Objectif 2] - Ex: Réduire coûts opérationnels de 30%  │
│  3. [Objectif 3] - Ex: Améliorer NPS de 20 points          │
│                                                             │
│  🔑 FACTEURS CLÉS DE SUCCÈS                                 │
│  • [FCS 1]                                                  │
│  • [FCS 2]                                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Axes Stratégiques

| Axe | Description | Exemples |
|-----|-------------|----------|
| **Acquisition** | Développer la visibilité et le trafic | SEO, Ads, Content |
| **Conversion** | Optimiser le parcours client | UX, CRO, Checkout |
| **Rétention** | Fidéliser les clients existants | CRM, Loyalty, Support |
| **Efficacité** | Optimiser les processus internes | Automation, Outils |
| **Innovation** | Créer de nouveaux services | Features, Produits |

### 3. Leviers Digitaux

```
                    LEVIERS DIGITAUX
    ┌─────────────────────────────────────────┐
    │                                         │
    │   EXPÉRIENCE          MARKETING         │
    │   ┌─────────┐        ┌─────────┐       │
    │   │ Site Web│        │   SEO   │       │
    │   │   App   │        │  Ads    │       │
    │   │   UX    │        │ Content │       │
    │   └─────────┘        └─────────┘       │
    │                                         │
    │   DATA               TECHNOLOGIE        │
    │   ┌─────────┐        ┌─────────┐       │
    │   │Analytics│        │   CRM   │       │
    │   │   BI    │        │   ERP   │       │
    │   │   CDP   │        │   API   │       │
    │   └─────────┘        └─────────┘       │
    │                                         │
    └─────────────────────────────────────────┘
```

## Template Stratégie Digitale

```markdown
# Stratégie Digitale - [Entreprise]

## 1. Contexte & Enjeux

### Situation Actuelle
[Description de l'état actuel de la présence digitale]

### Enjeux Business
| Enjeu | Impact | Urgence |
|-------|--------|---------|
| [Enjeu 1] | Fort | Court terme |
| [Enjeu 2] | Moyen | Moyen terme |

### Contraintes
- Budget : [Enveloppe]
- Timeline : [Horizon]
- Ressources : [Équipe disponible]
- Techniques : [Contraintes SI]

---

## 2. Vision & Ambition

### Vision à 3 Ans
> "[Phrase de vision inspirante et ambitieuse]"

### Objectifs Stratégiques

| Objectif | Métrique | Cible | Horizon |
|----------|----------|-------|---------|
| [Objectif 1] | [KPI] | [Valeur] | [Date] |
| [Objectif 2] | [KPI] | [Valeur] | [Date] |
| [Objectif 3] | [KPI] | [Valeur] | [Date] |

### Positionnement Cible
[Description du positionnement digital visé vs concurrence]

---

## 3. Axes Stratégiques

### Axe 1 : [Nom de l'axe]

**Objectif** : [Ce que cet axe vise à accomplir]

**Initiatives** :
1. [Initiative 1.1]
2. [Initiative 1.2]
3. [Initiative 1.3]

**KPIs** :
- [Métrique 1] : [Cible]
- [Métrique 2] : [Cible]

### Axe 2 : [Nom de l'axe]
[Même structure]

### Axe 3 : [Nom de l'axe]
[Même structure]

---

## 4. Roadmap Stratégique

### Vue Macro

```
         Q1      Q2      Q3      Q4      Q1+1    Q2+1
        ────────────────────────────────────────────────
Axe 1   ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Axe 2   ░░░░░░░░████████████████░░░░░░░░░░░░░░░░░░░░░░
Axe 3   ░░░░░░░░░░░░░░░░░░░░████████████████████████░░
```

### Phase 1 : Fondations (Mois 1-6)

| Initiative | Description | Budget | Livrables |
|------------|-------------|--------|-----------|
| [Init 1] | [Desc] | [€] | [Livrables] |

### Phase 2 : Développement (Mois 7-12)

| Initiative | Description | Budget | Livrables |
|------------|-------------|--------|-----------|
| [Init 2] | [Desc] | [€] | [Livrables] |

### Phase 3 : Optimisation (Année 2)

| Initiative | Description | Budget | Livrables |
|------------|-------------|--------|-----------|
| [Init 3] | [Desc] | [€] | [Livrables] |

---

## 5. Écosystème Digital Cible

### Architecture Fonctionnelle

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONT-END                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Site Web │  │ App Mobile│  │  Portail │  │   PWA    │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │             │             │          │
│  ─────┴─────────────┴─────────────┴─────────────┴─────     │
│                          │                                  │
│  ┌───────────────────────┴───────────────────────────┐    │
│  │                    API LAYER                       │    │
│  └───────────────────────┬───────────────────────────┘    │
│                          │                                  │
│  ─────┬─────────────┬────┴────┬─────────────┬─────        │
│       │             │         │             │              │
│  ┌────┴────┐  ┌─────┴───┐  ┌──┴───┐  ┌─────┴────┐        │
│  │   CRM   │  │   ERP   │  │  CDP │  │ Analytics│        │
│  └─────────┘  └─────────┘  └──────┘  └──────────┘        │
│                      BACK-END                              │
└─────────────────────────────────────────────────────────────┘
```

### Outils & Plateformes

| Fonction | Outil Recommandé | Alternative |
|----------|------------------|-------------|
| CMS | [Outil] | [Alt] |
| CRM | [Outil] | [Alt] |
| Analytics | [Outil] | [Alt] |
| Marketing Automation | [Outil] | [Alt] |

---

## 6. Gouvernance & Organisation

### Organisation Cible

```
           ┌─────────────────┐
           │ Direction       │
           │ Digitale        │
           └────────┬────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
┌───┴───┐     ┌─────┴─────┐   ┌────┴────┐
│ Tech  │     │ Marketing │   │ Produit │
│ Lead  │     │ Digital   │   │ Owner   │
└───────┘     └───────────┘   └─────────┘
```

### Compétences à Développer
| Compétence | Niveau Actuel | Cible | Action |
|------------|---------------|-------|--------|
| [Compétence] | [1-5] | [1-5] | [Action] |

### Modèle de Gouvernance
- Comité digital : [Fréquence]
- Revue de performance : [Fréquence]
- Pilotage projets : [Méthodologie]

---

## 7. Budget & ROI

### Investissements Prévisionnels

| Catégorie | Année 1 | Année 2 | Année 3 |
|-----------|---------|---------|---------|
| Développement | €X | €X | €X |
| Marketing | €X | €X | €X |
| Outils/Licences | €X | €X | €X |
| RH/Formation | €X | €X | €X |
| **TOTAL** | **€X** | **€X** | **€X** |

### ROI Attendu

| Bénéfice | Impact Année 1 | Impact Année 2 | Impact Année 3 |
|----------|----------------|----------------|----------------|
| CA additionnel | +€X | +€X | +€X |
| Économies | €X | €X | €X |

**Payback** : [X] mois

---

## 8. Risques & Mitigation

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| [Risque 1] | Moyenne | Fort | [Action] |
| [Risque 2] | Faible | Critique | [Action] |

---

## 9. Prochaines Étapes

### Actions Immédiates
1. [ ] [Action 1] - Responsable : [Qui] - Deadline : [Date]
2. [ ] [Action 2] - Responsable : [Qui] - Deadline : [Date]

### Décisions Requises
1. [Décision à prendre]
2. [Décision à prendre]
```

## Points d'Escalade

| Situation | Action |
|-----------|--------|
| Budget insuffisant pour ambition | Proposer scénarios priorisés |
| Objectifs contradictoires | Faciliter arbitrage direction |
| Résistance au changement | Recommander accompagnement |
| Gap compétences critique | Alerter sur risque d'exécution |

## Livrables

| Livrable | Format | Description |
|----------|--------|-------------|
| Document stratégique | PDF/Notion | Vision et roadmap complète |
| Executive summary | PPT | Synthèse pour direction |
| Roadmap visuelle | Timeline | Planning macro |
| Business case | Excel | Budget et ROI |
