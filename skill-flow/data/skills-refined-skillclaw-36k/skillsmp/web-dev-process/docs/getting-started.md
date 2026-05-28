# Guide de Démarrage - Web Dev Process

Ce guide vous aide à utiliser le skill `web-dev-process` pour structurer vos projets web.

## Introduction

Le skill `web-dev-process` définit un processus de développement web en **7 phases**, applicable à toutes les technologies (React, Vue, WordPress, Node.js, etc.).

```
Discovery → Design → Setup → Development → Testing → Deployment → Maintenance
```

## Installation

Ce skill est automatiquement disponible si vous l'avez dans votre répertoire `.web-agency/skills/`.

## Comment Utiliser ce Skill

### 1. Poser des Questions Générales

Le skill répond aux questions sur le processus de développement :

```
"Comment structurer mon projet ?"
"Quelles sont les bonnes pratiques de code review ?"
"Comment définir le MVP de mon projet ?"
```

### 2. Demander de l'Aide sur une Phase Spécifique

Chaque phase a ses propres agents spécialisés :

```
"Aide-moi à rédiger les user stories pour mon projet"
→ Utilise discovery/user-stories

"Comment designer mon API REST ?"
→ Utilise design/api-design

"Comment configurer ESLint pour mon projet ?"
→ Utilise setup/quality-tools
```

### 3. Combiner avec un Skill Technologique

Pour une implémentation concrète, combinez avec le skill de votre technologie :

```
"Comment mettre en place CI/CD pour mon projet WordPress ?"
→ web-dev-process/setup/cicd (principes)
→ wordpress-gutenberg-expert/tooling/cicd (implémentation)
```

## Les 7 Phases en Détail

### Phase 1: Discovery (Analyse)

**Objectif** : Comprendre le besoin avant de coder

**Agents disponibles** :
- `requirements` - Collecte des exigences
- `user-stories` - Rédaction des user stories
- `scope-definition` - Définition du périmètre

**Questions typiques** :
- "Comment rédiger des user stories efficaces ?"
- "Comment définir le MVP ?"
- "Comment prioriser le backlog ?"

---

### Phase 2: Design (Conception)

**Objectif** : Concevoir avant d'implémenter

**Agents disponibles** :
- `architecture` - Architecture technique
- `data-modeling` - Modélisation des données
- `api-design` - Design d'API REST/GraphQL
- `ui-ux` - Principes UI/UX et accessibilité

**Questions typiques** :
- "Quelle architecture choisir pour mon projet ?"
- "Comment modéliser ma base de données ?"
- "Quelles sont les bonnes pratiques REST ?"

---

### Phase 3: Setup (Initialisation)

**Objectif** : Préparer l'environnement de travail

**Agents disponibles** :
- `repository` - Configuration Git
- `environment` - Variables d'environnement
- `cicd` - Principes CI/CD
- `quality-tools` - Linting, formatting

**Questions typiques** :
- "Quelle stratégie de branches utiliser ?"
- "Comment configurer les pre-commit hooks ?"
- "Comment gérer mes variables d'environnement ?"

---

### Phase 4: Development (Développement)

**Objectif** : Écrire du code maintenable

**Agents disponibles** :
- `coding-standards` - Conventions de code
- `code-review` - Pratiques de revue
- `git-workflow` - Commits, PRs
- `documentation` - ADRs, README

**Questions typiques** :
- "Comment nommer mes variables ?"
- "Comment faire une bonne code review ?"
- "Comment écrire des commits clairs ?"

---

### Phase 5: Testing (Tests)

**Objectif** : Valider la qualité

**Agents disponibles** :
- `unit-tests` - Tests unitaires
- `integration-tests` - Tests d'intégration
- `e2e-tests` - Tests end-to-end
- `performance` - Tests de charge
- `accessibility` - Tests WCAG
- `security` - Tests OWASP

**Questions typiques** :
- "Comment structurer mes tests ?"
- "Quelle couverture de code viser ?"
- "Comment tester l'accessibilité ?"

---

### Phase 6: Deployment (Déploiement)

**Objectif** : Livrer en production

**Agents disponibles** :
- `staging` - Environnement de pré-production
- `production` - Mise en production
- `rollback` - Stratégies de retour arrière

**Questions typiques** :
- "Comment configurer le staging ?"
- "Quelle stratégie de déploiement utiliser ?"
- "Comment faire un rollback ?"

---

### Phase 7: Maintenance

**Objectif** : Maintenir et améliorer

**Agents disponibles** :
- `monitoring` - Observabilité et alertes
- `bug-tracking` - Gestion des incidents
- `updates` - Mises à jour et dette technique

**Questions typiques** :
- "Comment surveiller mon application ?"
- "Comment gérer la dette technique ?"
- "Comment mettre à jour mes dépendances ?"

## Exemples d'Utilisation

### Exemple 1: Démarrer un nouveau projet

```
1. "Aide-moi à définir les requirements de mon projet e-commerce"
2. "Quels sont les user stories essentiels pour un MVP ?"
3. "Quelle architecture recommandes-tu ?"
4. "Comment configurer mon repo Git ?"
```

### Exemple 2: Améliorer un projet existant

```
1. "Comment mettre en place une stratégie de tests ?"
2. "Comment réduire ma dette technique ?"
3. "Comment améliorer mon monitoring ?"
```

### Exemple 3: Résoudre un problème spécifique

```
1. "J'ai un bug en production, que faire ?"
   → Utilise deployment/rollback et maintenance/bug-tracking

2. "Mon site est lent, comment l'optimiser ?"
   → Utilise testing/performance

3. "Comment rendre mon site accessible ?"
   → Utilise design/ui-ux et testing/accessibility
```

## Ressources Complémentaires

- [Phase Checklist](./phase-checklist.md) - Checklists par phase
- [SKILL.md](../SKILL.md) - Documentation complète du skill

## Support

Pour toute question sur l'utilisation de ce skill, consultez le fichier SKILL.md ou demandez directement assistance.
