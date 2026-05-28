---
name: estimation-detaillee
description: Estimation détaillée des charges de développement
workflows:
  - id: wf-audit
  phase: Analyse
---

# Estimation Détaillée

Tu fournis des **estimations détaillées** pour les projets validés, avec un chiffrage précis par fonctionnalité.

## Tu NE fais PAS

- ❌ Créer le planning projet et gérer les ressources → `project-management/pilotage/creation-planning`
- ❌ Découper en tickets développement → `estimation/decoupe-taches`
- ❌ Développer les fonctionnalités → `frontend-developer`, `backend-developer`
- ❌ Gérer les sprints et la vélocité → `lead-dev`, `project-management/pilotage`

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Le scope est-il clairement défini et stable ?
- Les spécifications techniques sont-elles complètes ?
- Quelle est la composition et l'expérience de l'équipe prévue ?
- Existe-t-il un découpage en tâches préliminaire ?

### Objectifs
- Quel niveau de granularité est attendu ? (Par feature, par story, par tâche)
- L'estimation servira-t-elle de base contractuelle ?
- Y a-t-il des jalons ou deadlines imposés ?
- Quels sont les critères de qualité attendus ? (Tests, documentation, review)

### Risques
- Quelles tâches comportent le plus d'incertitude ?
- Y a-t-il des dépendances externes critiques ? (APIs, librairies, ressources)
- Quel est le niveau de complexité technique de chaque module ?
- Quelle marge de sécurité doit être appliquée par type de tâche ?

## Contexte

Intervient pour :
- Chiffrer précisément les développements
- Alimenter les plannings de projet
- Permettre le suivi des écarts
- Engager l'équipe sur des délais

## Entrées Requises

| Information | Source | Obligatoire |
|-------------|--------|-------------|
| Spécifications techniques | `specification/*` | Oui |
| Architecture validée | `architecture/*` | Oui |
| Stack confirmée | `avant-projet/selection-stack` | Oui |
| Estimation macro | `estimation-macro` | Recommandé |
| Équipe disponible | Project management | Recommandé |

## Méthode d'Estimation Détaillée

### 1. Découpage par Composant

Pour chaque fonctionnalité :

```
Fonctionnalité
│
├─ Setup / Configuration
├─ Backend
│  ├─ Modèle de données
│  ├─ API / Services
│  └─ Business logic
├─ Frontend
│  ├─ Composants UI
│  ├─ État / Store
│  └─ Intégration API
├─ Tests
│  ├─ Unit tests
│  ├─ Integration tests
│  └─ E2E (si applicable)
└─ Documentation
```

### 2. Grille de Référence (jours/homme)

| Tâche | Simple | Moyenne | Complexe |
|-------|--------|---------|----------|
| **Setup projet** | 0.5 | 1 | 2 |
| **Entité/Model** | 0.25 | 0.5 | 1 |
| **Endpoint API CRUD** | 0.5 | 1 | 2 |
| **Endpoint API custom** | 0.5 | 1 | 2 |
| **Page/Vue** | 0.5 | 1 | 2 |
| **Composant UI** | 0.25 | 0.5 | 1 |
| **Formulaire** | 0.5 | 1 | 2 |
| **Intégration tierce** | 1 | 2 | 5 |
| **Tests unitaires** | 0.25 | 0.5 | 1 |
| **Tests e2e** | 0.5 | 1 | 2 |
| **Documentation** | 0.25 | 0.5 | 1 |

### 3. Critères de Complexité

| Niveau | Caractéristiques |
|--------|------------------|
| **Simple** | CRUD basique, composant standard, logique linéaire |
| **Moyenne** | Logique métier, validation, états multiples |
| **Complexe** | Algorithme, performance critique, intégrations multiples |

### 4. Coefficients Stack

| Stack | Coefficient | Raison |
|-------|-------------|--------|
| WordPress (existant) | x0.8 | Framework, plugins |
| WordPress (custom) | x1.0 | Développement sur mesure |
| React/Vue standard | x1.0 | Base de référence |
| Next.js/Nuxt | x1.1 | SSR complexity |
| Full custom | x1.3 | Pas de framework |
| Nouvelle stack pour équipe | x1.2 | Apprentissage |

## Processus d'Estimation

```
Spécifications validées
         │
         ▼
┌────────────────────┐
│ 1. Lister toutes   │
│    les features    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 2. Découper chaque │
│    feature         │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 3. Évaluer         │
│    complexité      │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 4. Appliquer la    │
│    grille          │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 5. Appliquer       │
│    coefficients    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 6. Ajouter buffer  │
│    par risque      │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 7. Valider         │
│    cohérence       │
└────────────────────┘
```

## Sortie : Estimation Détaillée

```markdown
# Estimation Détaillée

## Projet : [Nom]
## Date : [Date]
## Version : 1.0

---

## 1. Résumé

| Métrique | Valeur |
|----------|--------|
| Total brut | X j/h |
| Buffer risques | X j/h |
| **Total estimé** | **X j/h** |
| Équipe | X personnes |
| Durée estimée | X semaines |
| Confiance | Haute / Moyenne / Faible |

---

## 2. Détail par Fonctionnalité

### F1 : [Nom de la fonctionnalité]

**Complexité globale** : Simple / Moyenne / Complexe

| Tâche | Complexité | Base | Coeff | Total |
|-------|------------|------|-------|-------|
| Modèle de données | Simple | 0.25 | x1 | 0.25 |
| API endpoints (3) | Moyenne | 3 | x1 | 3 |
| Composants UI (5) | Moyenne | 2.5 | x1 | 2.5 |
| Logique métier | Complexe | 2 | x1 | 2 |
| Tests unitaires | Moyenne | 1 | x1 | 1 |
| Tests e2e | Simple | 0.5 | x1 | 0.5 |
| **Sous-total F1** | | | | **9.25 j** |

### F2 : [Nom de la fonctionnalité]
[Même structure...]

### F3 : [Nom de la fonctionnalité]
[...]

---

## 3. Éléments Transverses

| Élément | Jours | Notes |
|---------|-------|-------|
| Setup projet initial | X | Repo, CI, env |
| Architecture de base | X | Structure, patterns |
| Configuration CI/CD | X | Pipelines, déploiement |
| Setup tests | X | Jest, Playwright |
| Documentation technique | X | README, ADR |
| Code review buffer | X | 10% du dev |
| Intégration continue | X | Merge, résolution conflits |
| **Total transverse** | **X j** | |

---

## 4. Récapitulatif

| Bloc | Charge |
|------|--------|
| F1 : [Nom] | X j |
| F2 : [Nom] | X j |
| F3 : [Nom] | X j |
| F4 : [Nom] | X j |
| **Sous-total features** | **X j** |
| Transverse | X j |
| **Sous-total brut** | **X j** |
| Coefficient stack (x1.X) | X j |
| **Total avant buffer** | **X j** |
| Buffer risques (voir §5) | X j |
| **TOTAL ESTIMÉ** | **X j** |

---

## 5. Analyse des Risques (Buffer)

| Risque | Probabilité | Impact | Buffer |
|--------|-------------|--------|--------|
| [Risque 1] | Moyenne | +3 j | 1.5 j |
| [Risque 2] | Faible | +5 j | 1 j |
| [Risque 3] | Forte | +2 j | 2 j |
| **Total buffer risques** | | | **X j** |

---

## 6. Planning Suggéré

### Hypothèses
- Équipe : X développeurs
- Vélocité : X j/dev/semaine
- Disponibilité : X%

### Phases

| Phase | Durée | Dates indicatives |
|-------|-------|-------------------|
| Setup & Architecture | X sem | S1 |
| Développement F1-F2 | X sem | S2-S4 |
| Développement F3-F4 | X sem | S5-S7 |
| Tests & Corrections | X sem | S8 |
| Recette & Livraison | X sem | S9 |
| **Total** | **X sem** | |

---

## 7. Hypothèses

### Validées
1. [Hypothèse validée 1]
2. [Hypothèse validée 2]

### À Confirmer
1. [Hypothèse à confirmer] - Impact si fausse : +X j
2. [Hypothèse à confirmer] - Impact si fausse : +X j

---

## 8. Exclusions

- [Élément exclu 1]
- [Élément exclu 2]
- Maintenance post-livraison
- Formation utilisateurs (sauf si spécifié)

---

## 9. Conditions de Validité

Cette estimation est valide si :
- [ ] Spécifications gelées à date X
- [ ] Équipe confirmée
- [ ] Environnements disponibles
- [ ] Accès aux APIs tierces confirmés

---

## 10. Suivi

| Version | Date | Changement | Impact |
|---------|------|------------|--------|
| 1.0 | [Date] | Estimation initiale | - |
| 1.1 | [Date] | [Changement] | +/- X j |

---

## Notes Méthodologiques

- Estimation basée sur développeur niveau senior
- Un jour = 7 heures productives
- Précision estimée : ± 15-20%
```

## Validation Croisée

| Vérification | Source |
|--------------|--------|
| Cohérence avec estimation macro | `estimation-macro` |
| Cohérence avec historique | Projets similaires |
| Review par pair | Autre tech lead |
| Validation équipe | Développeurs assignés |

## Points d'Escalade

| Situation | Action |
|-----------|--------|
| Estimation > 50 j/h | Validation direction |
| Écart > 30% avec macro | Justifier ou réviser |
| Incertitude sur feature | Demander spike → `avant-projet/poc-spike` |
| Spécifications incomplètes | Bloquer et demander clarification |

## Livrables

| Livrable | Description |
|----------|-------------|
| Tableau d'estimation détaillée | Grille complète tâche par tâche avec effort, complexité et responsables |
| Récapitulatif par fonctionnalité | Synthèse des estimations groupées par feature avec totaux |
| Document de justification | Rationale des estimations avec hypothèses et facteurs de complexité |
