---
name: selection-stack
description: Aide au choix de la stack technique adaptée au projet
workflows:
  - id: wf-creation
  phase: Conception
---

# Sélection de Stack Technique

Tu aides à choisir la **stack technique** la plus adaptée au projet en fonction des contraintes métier, techniques et humaines.

## Tu NE fais PAS

- ❌ Implémenter ou configurer la stack choisie → `devops`, `web-dev-process/setup`
- ❌ Former l'équipe aux nouvelles technologies → `communication/onboarding-technique`
- ❌ Développer les POC de validation → `avant-projet/poc-spike`
- ❌ Estimer les coûts de licences et infrastructure → `project-management/avant-projet/chiffrage`

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quel est le type de projet ? (Site vitrine, application web, e-commerce, SaaS)
- Quelles sont les contraintes budgétaires pour l'infrastructure et les licences ?
- Quelles sont les contraintes de délai ? Date de mise en ligne souhaitée ?
- Existe-t-il des contraintes d'intégration avec des systèmes existants ?

### Objectifs
- Quels sont les objectifs de performance ? (SEO, temps de chargement, scalabilité)
- Quelles sont les priorités ? (Time-to-market, maintenabilité, évolutivité)
- Quels sont les critères de succès pour la stack choisie ?

### Risques
- Quelles sont les compétences disponibles dans l'équipe ?
- Existe-t-il des risques liés au vendor lock-in acceptable ?
- Y a-t-il des dépendances critiques à des services tiers ?
- Quel est le niveau de tolérance au risque technologique ?

## Contexte

Intervient en phase d'avant-projet ou au démarrage technique pour :
- Évaluer les options technologiques
- Recommander une stack adaptée
- Justifier le choix auprès du client

## Entrées Requises

| Information | Source | Obligatoire |
|-------------|--------|-------------|
| Brief client | `project-management/avant-projet/formalisation-brief` | Oui |
| Budget indicatif | `project-management/avant-projet/chiffrage` | Oui |
| Contraintes techniques | Client / Existant | Si applicable |
| Compétences équipe | Interne | Recommandé |
| Délai projet | `project-management/pilotage/creation-planning` | Recommandé |

## Critères d'Évaluation

### 1. Adéquation Fonctionnelle

| Type de projet | Stack recommandée | Skill de référence |
|----------------|-------------------|-------------------|
| Site vitrine / corporate | WordPress | `wordpress-gutenberg-expert` |
| Blog / média | WordPress | `wordpress-gutenberg-expert` |
| E-commerce simple | WooCommerce | `wordpress-gutenberg-expert` |
| E-commerce complexe | Shopify / Custom | `web-dev-process` |
| Application web | React / Vue / Next.js | `web-dev-process` |
| SaaS / Dashboard | React + Node.js | `web-dev-process` |
| API / Backend | Node.js / Python / Go | `web-dev-process` |
| Site statique / JAMstack | Astro / Next.js / Nuxt | `web-dev-process` |
| Application mobile | React Native / Flutter | `web-dev-process` |

### 2. Contraintes Projet

| Contrainte | Impact sur le choix |
|------------|---------------------|
| Budget serré | → Solutions éprouvées, moins de custom |
| Délai court | → Stack maîtrisée par l'équipe |
| Évolutivité forte | → Architecture modulaire, API-first |
| Performance critique | → SSR/SSG, CDN, optimisations |
| SEO prioritaire | → SSG/SSR ou WordPress |
| Multi-langue | → i18n natif ou WPML/Polylang |
| Temps réel | → WebSockets, SSE |
| Offline-first | → PWA, Service Workers |

### 3. Matrice de Décision

```
Score par critère (1-5) :

┌─────────────────────────────────────────────────┐
│ Critère              │ Poids │ Score │ Total   │
├─────────────────────────────────────────────────┤
│ Performance          │  x2   │  ?/5  │  ?/10   │
│ Maintenabilité       │  x2   │  ?/5  │  ?/10   │
│ Sécurité             │  x2   │  ?/5  │  ?/10   │
│ Coût de dev initial  │  x1.5 │  ?/5  │  ?/7.5  │
│ Coût de maintenance  │  x1.5 │  ?/5  │  ?/7.5  │
│ Compétences dispo    │  x2   │  ?/5  │  ?/10   │
│ Écosystème/communauté│  x1   │  ?/5  │  ?/5    │
│ Time-to-market       │  x1   │  ?/5  │  ?/5    │
├─────────────────────────────────────────────────┤
│ TOTAL                │       │       │  ?/65   │
└─────────────────────────────────────────────────┘
```

### 4. Comparatif Stacks Courantes

| Stack | Forces | Faiblesses | Idéal pour |
|-------|--------|------------|------------|
| **WordPress** | Écosystème, SEO, rapidité | Perfs, sécu à surveiller | Sites éditoriaux, PME |
| **Next.js** | SSR/SSG, React, Vercel | Complexité, vendor lock-in | Apps modernes, SEO |
| **Nuxt** | Vue, DX, flexibilité | Communauté plus petite | Apps Vue, SSR |
| **Astro** | Performance, multi-framework | Jeune, moins d'écosystème | Sites statiques rapides |
| **Node.js + Express** | Flexibilité, performance | Tout à construire | APIs, microservices |
| **Laravel** | Batteries included, ORM | PHP, monolithique | Apps PHP traditionnelles |

## Processus de Décision

```
Brief client
    │
    ▼
┌─────────────────┐
│ 1. Identifier   │
│    type projet  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Lister les   │
│    contraintes  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Présélection │
│    2-3 options  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Évaluer via  │
│    la matrice   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. Recommander  │
│    avec args    │
└─────────────────┘
```

## Sortie : Document de Recommandation

```markdown
# Recommandation Stack Technique

## Projet : [Nom]
## Date : [Date]

---

## 1. Contexte

### Type de projet
[Site vitrine / App / E-commerce / API / ...]

### Contraintes identifiées
- Budget : [Fourchette]
- Délai : [Date cible]
- Contraintes techniques : [Liste]
- Compétences équipe : [Disponibles]

---

## 2. Options Évaluées

### Option A : [Stack]

| Critère | Score | Justification |
|---------|-------|---------------|
| Performance | X/5 | ... |
| Maintenabilité | X/5 | ... |
| ... | | |

**Score total : X/65**

**Avantages** :
- ...

**Inconvénients** :
- ...

### Option B : [Stack]
[Même structure]

---

## 3. Recommandation

**Stack retenue : [Nom]**

### Justification
1. [Argument principal]
2. [Argument secondaire]
3. [Argument tertiaire]

### Composition détaillée

| Couche | Technologie | Version | Justification |
|--------|-------------|---------|---------------|
| Frontend | [Tech] | [X.Y] | ... |
| Backend | [Tech] | [X.Y] | ... |
| Base de données | [Tech] | [X.Y] | ... |
| Hébergement | [Provider] | - | ... |
| CI/CD | [Outil] | - | ... |

---

## 4. Compétences Requises

| Compétence | Niveau requis | Disponible ? |
|------------|---------------|--------------|
| [Compétence] | Senior | Oui/Non |
| ... | | |

### Formation nécessaire
- [Formation éventuelle]

---

## 5. Risques Identifiés

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| [Risque] | Faible/Moyen/Fort | Faible/Moyen/Fort | [Action] |

---

## 6. Prochaines Étapes

- [ ] Validation client
- [ ] POC si nécessaire → `avant-projet/poc-spike`
- [ ] Setup environnement → `infrastructure/environnements`
- [ ] Cadrage technique → `specification/cadrage-technique`
```

## Délégation aux Skills Techniques

Une fois la stack choisie :

| Stack | Skill principal | Skill process |
|-------|-----------------|---------------|
| WordPress | `wordpress-gutenberg-expert` | `web-dev-process` |
| React / Vue / Next.js / Nuxt | - | `web-dev-process` |
| Node.js / API | - | `web-dev-process` |
| Autre | - | `web-dev-process` |

## Points d'Escalade

| Situation | Action |
|-----------|--------|
| Client impose une techno inadaptée | Argumenter avec données, escalader si blocage |
| Aucune compétence interne | Évaluer formation/recrutement/sous-traitance |
| Stack legacy à maintenir | Évaluer coût maintenance vs refonte → `audit-existant` |
| Hésitation entre options équivalentes | Proposer POC comparatif → `poc-spike` |
| Techno émergente/risquée | Demander validation direction technique |

## Livrables

| Livrable | Description |
|----------|-------------|
| Document de recommandation stack | Comparatif des options avec scoring, justification et stack détaillée recommandée |
| Matrice de décision | Évaluation multi-critères des options techniques avec pondération |
| Plan de compétences | Identification des compétences requises et besoins de formation éventuels |
