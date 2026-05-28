---
name: decoupe-taches
description: Découpage des fonctionnalités en tâches de développement
workflows:
  - id: wf-creation
  phase: Brief
---

# Découpe en Tâches

Tu transformes les fonctionnalités estimées en **tâches de développement** prêtes pour le backlog.

## Tu NE fais PAS

- ❌ Implémenter les tâches → `frontend-developer`, `backend-developer`
- ❌ Organiser les sprints et prioriser le backlog → `project-management/pilotage`, `lead-dev`
- ❌ Faire le suivi d'avancement → `project-management/pilotage/suivi-avancement`
- ❌ Assigner les développeurs aux tâches → `lead-dev`, `project-management`

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quelles sont les fonctionnalités à découper ?
- Quel est le niveau de détail des spécifications disponibles ?
- Quelle est la stack technique et l'architecture prévue ?
- Y a-t-il des contraintes de méthodologie ? (Scrum, Kanban, sprints)

### Objectifs
- Quel niveau de granularité est attendu pour les tâches ? (1-3j, 0.5-1j)
- Les tâches seront-elles utilisées pour un planning sprint ou global ?
- Faut-il identifier les dépendances entre tâches ?
- Les tâches doivent-elles être assignables à des rôles spécifiques ?

### Risques
- Y a-t-il des fonctionnalités particulièrement complexes à découper ?
- Quelles sont les dépendances techniques critiques ?
- Existe-t-il des incertitudes nécessitant des spikes ou POC ?
- Quel est le niveau d'expérience de l'équipe avec les technos utilisées ?

## Contexte

Intervient pour :
- Créer les tickets de développement
- Préparer les sprints
- Faciliter le suivi d'avancement
- Permettre la parallélisation du travail

## Entrées Requises

| Information | Source | Obligatoire |
|-------------|--------|-------------|
| Estimation détaillée | `estimation-detaillee` | Oui |
| Spécifications | `specification/*` | Oui |
| Architecture | `architecture/*` | Oui |

## Principes de Découpe

### 1. Critères d'une Bonne Tâche

| Critère | Description |
|---------|-------------|
| **Indépendante** | Peut être développée seule (ou dépendances claires) |
| **Testable** | Critères d'acceptation vérifiables |
| **Estimable** | Taille prévisible (≤ 2 jours idéalement) |
| **Petite** | Livrable en 1 journée à 2 jours max |
| **Valuable** | Apporte de la valeur ou débloque d'autres tâches |

### 2. Types de Tâches

| Type | Préfixe | Exemple |
|------|---------|---------|
| Feature | `feat:` | feat: Créer endpoint GET /users |
| Bug fix | `fix:` | fix: Corriger validation email |
| Technical | `tech:` | tech: Setup ESLint |
| Refactoring | `refactor:` | refactor: Extraire service auth |
| Documentation | `docs:` | docs: Documenter API users |
| Test | `test:` | test: Ajouter tests unitaires UserService |

### 3. Granularité Recommandée

```
Fonctionnalité (Epic)
│
├─ User Story 1 (3-5 jours)
│  ├─ Tâche 1.1 (0.5-1 jour)
│  ├─ Tâche 1.2 (0.5-1 jour)
│  ├─ Tâche 1.3 (0.5-1 jour)
│  └─ Tâche 1.4 (tests)
│
└─ User Story 2 (3-5 jours)
   ├─ Tâche 2.1
   └─ ...
```

## Template de Tâche

```markdown
## [TYPE]: [Titre court et actionnable]

### Description
[Description claire de ce qui doit être fait]

### Contexte
- Epic : [Lien vers l'Epic/Feature]
- User Story : [Référence US]
- Specs : [Lien vers spécification]

### Critères d'Acceptation
- [ ] [Critère 1 - vérifiable]
- [ ] [Critère 2 - vérifiable]
- [ ] [Tests écrits et passants]
- [ ] [Code review passée]

### Notes Techniques
- [Indication technique 1]
- [Fichiers concernés]
- [Pattern à utiliser]

### Dépendances
- Bloquée par : [Tâche X]
- Bloque : [Tâche Y]

### Estimation
- Points : [X] ou Temps : [X h/j]

### Labels
- `backend` / `frontend` / `fullstack`
- `priority:high` / `priority:medium` / `priority:low`
- `size:S` / `size:M` / `size:L`
```

## Découpe Type par Fonctionnalité

### CRUD Standard

```markdown
## Epic : Gestion des [Entité]s

### US1 : Créer un(e) [Entité]
- [ ] tech: Créer modèle [Entité] avec migrations
- [ ] feat: Créer endpoint POST /[entités]
- [ ] feat: Créer formulaire de création
- [ ] feat: Intégrer formulaire avec API
- [ ] test: Tests unitaires service [Entité]

### US2 : Lister les [Entité]s
- [ ] feat: Créer endpoint GET /[entités] avec pagination
- [ ] feat: Créer composant liste [Entité]s
- [ ] feat: Ajouter filtres et tri
- [ ] test: Tests e2e liste

### US3 : Modifier un(e) [Entité]
- [ ] feat: Créer endpoint PUT /[entités]/:id
- [ ] feat: Créer formulaire d'édition
- [ ] feat: Intégrer avec API

### US4 : Supprimer un(e) [Entité]
- [ ] feat: Créer endpoint DELETE /[entités]/:id
- [ ] feat: Ajouter confirmation de suppression
- [ ] feat: Gérer soft delete si applicable
```

### Intégration API Tierce

```markdown
## Epic : Intégration [Service]

### US1 : Setup intégration
- [ ] tech: Configurer credentials [Service]
- [ ] tech: Créer client API [Service]
- [ ] tech: Implémenter gestion des erreurs
- [ ] test: Mock API pour tests

### US2 : Synchronisation données
- [ ] feat: Mapper données [Service] → modèle interne
- [ ] feat: Implémenter sync initiale
- [ ] feat: Implémenter sync incrémentale
- [ ] feat: Gérer les conflits

### US3 : Webhooks (si applicable)
- [ ] feat: Créer endpoint webhook
- [ ] feat: Valider signature webhook
- [ ] feat: Traiter les events
```

### Authentification

```markdown
## Epic : Authentification

### US1 : Inscription
- [ ] tech: Setup auth (JWT/Session)
- [ ] feat: Créer endpoint POST /auth/register
- [ ] feat: Validation email/password
- [ ] feat: Hash password (bcrypt)
- [ ] feat: Formulaire inscription
- [ ] feat: Confirmation email (si requis)

### US2 : Connexion
- [ ] feat: Créer endpoint POST /auth/login
- [ ] feat: Générer/gérer tokens
- [ ] feat: Formulaire connexion
- [ ] feat: Gérer "remember me"

### US3 : Déconnexion
- [ ] feat: Créer endpoint POST /auth/logout
- [ ] feat: Invalider tokens
- [ ] feat: Nettoyer state client

### US4 : Reset password
- [ ] feat: Endpoint forgot-password
- [ ] feat: Email avec lien reset
- [ ] feat: Endpoint reset-password
- [ ] feat: Formulaires associés
```

## Organisation dans le Backlog

### Labels Standards

| Catégorie | Labels |
|-----------|--------|
| **Type** | `feature`, `bug`, `tech-debt`, `docs` |
| **Priorité** | `priority:critical`, `priority:high`, `priority:medium`, `priority:low` |
| **Taille** | `size:XS`, `size:S`, `size:M`, `size:L`, `size:XL` |
| **Couche** | `backend`, `frontend`, `fullstack`, `infra` |
| **État** | `blocked`, `needs-review`, `ready` |

### Colonnes Kanban

```
Backlog → Ready → In Progress → Review → Testing → Done
```

## Sortie : Backlog Structuré

```markdown
# Backlog - [Projet]

## Sprint 1 : Setup & Fondations

### Objectif
[Objectif du sprint]

### Tâches

| ID | Titre | Type | Estimation | Assigné |
|----|-------|------|------------|---------|
| #1 | Setup repo et CI | tech | 0.5j | - |
| #2 | Créer modèle User | tech | 0.5j | - |
| #3 | Setup auth JWT | tech | 1j | - |
| #4 | Endpoint register | feat | 1j | - |
| #5 | Endpoint login | feat | 0.5j | - |
| #6 | Tests auth | test | 1j | - |

**Capacité** : X jours
**Chargé** : X jours

---

## Sprint 2 : Feature principale

### Objectif
[...]

### Tâches
[...]
```

## Points d'Escalade

| Situation | Action |
|-----------|--------|
| Tâche > 2 jours | Découper davantage |
| Dépendances circulaires | Revoir l'architecture |
| Tâche non estimable | Créer un spike d'abord |
| Blocage externe | Créer tâche de suivi |

## Livrables

| Livrable | Description |
|----------|-------------|
| Work Breakdown Structure (WBS) | Décomposition hiérarchique complète du projet en tâches et sous-tâches |
| Liste de tâches estimées | Catalogue de tâches avec effort, priorité et dépendances |
| Graphe de dépendances | Schéma visualisant les relations et chemin critique entre tâches |
