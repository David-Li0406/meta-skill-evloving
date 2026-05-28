---
name: composition
description: Comment composer et combiner les skills
version: 2.0.0
---

# Composition des Skills

Ce document définit comment combiner plusieurs skills pour des requêtes complexes.

## Principe

> Les skills sont des LEGO : composables, indépendants, réutilisables.

## Skills Disponibles (12 skills, 409 agents)

| Skill | Niveau | Agents | Domaine |
|-------|--------|--------|---------|
| direction-technique | 1-STRATÉGIE | 52 | Décisions, politiques |
| web-dev-process | 2-PROCESSUS | 61 | Méthodologie dev |
| testing-process | 2-PROCESSUS | 25 | Méthodologie tests |
| lead-dev | 2-OPÉRATIONS | 27 | Coordination équipe |
| frontend-developer | 3-IMPLÉMENTATION | 33 | Code frontend |
| backend-developer | 3-IMPLÉMENTATION | 32 | Code backend |
| devops | 3-IMPLÉMENTATION | 30 | CI/CD, infrastructure |
| react-expert | 3-IMPLÉMENTATION | 28 | Spécialisation React |
| nextjs-expert | 3-IMPLÉMENTATION | 35 | Spécialisation Next.js |
| wordpress-gutenberg | 3-IMPLÉMENTATION | 41 | WordPress/Gutenberg |
| design-system | 3-IMPLÉMENTATION | 21 | Tokens, composants |
| project-management | TRANSVERSE | 24 | Gestion projet |

## Types de Composition

### 1. Composition Séquentielle

Un skill dépend de l'output d'un autre.

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ project-mgmt     │ ──► │ direction-tech   │ ──► │ frontend-dev     │
│ (Brief client)   │     │ (Specs techniques)│     │ (Implémentation) │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

**Exemple** : "Créer un devis pour site e-commerce"
1. `project-management` → Brief & estimation commerciale
2. `direction-technique` → Choix stack (Next.js + API)
3. `nextjs-expert` → Estimation technique App Router

### 2. Composition Parallèle

Skills indépendants travaillant en même temps.

```
                    ┌──────────────────┐
               ┌───►│ design-system    │
               │    └──────────────────┘
┌──────────┐   │    ┌──────────────────┐
│ Specs    │───┼───►│ frontend-dev     │
└──────────┘   │    └──────────────────┘
               │    ┌──────────────────┐
               └───►│ backend-dev      │
                    └──────────────────┘
```

**Exemple** : Après validation des specs, frontend/backend/design-system peuvent avancer en parallèle.

### 3. Composition Hiérarchique (3 niveaux)

Selon ADR-005 et ADR-006, les skills s'empilent :

```
NIVEAU 1 : POURQUOI (direction-technique)
        │
        ▼
NIVEAU 2 : QUOI/QUI
        ├── web-dev-process (méthodologie)
        ├── testing-process (tests)
        └── lead-dev (coordination)
        │
        ▼
NIVEAU 3 : COMMENT (implémentation)
        ├── frontend-developer / react-expert / nextjs-expert
        ├── backend-developer
        ├── devops
        ├── wordpress-gutenberg-expert
        └── design-system-foundations
```

**Exemple** : "Mettre en place la stratégie de tests"
1. `direction-technique` → POURQUOI : "Qualité, non-régression, CI/CD"
2. `testing-process` → QUOI : "Pyramide 70/20/10, TDD, coverage > 80%"
3. `frontend-developer` → COMMENT : "Vitest + RTL + Playwright"

## Patterns de Composition Courants

### Pattern : Nouveau Projet React/Next.js

```
1. project-management/avant-projet
   → Collecte brief, estimation commerciale

2. direction-technique/avant-projet
   → Choix stack: Next.js 14 + App Router
   → Standards: TypeScript, TDD, accessibilité AA

3. [PARALLÈLE - Setup]
   ├─ devops/cicd
   │  → GitHub Actions, environnements
   ├─ design-system-foundations
   │  → Tokens, primitives
   └─ testing-process/strategy
      → Pyramide tests, outils

4. web-dev-process/setup
   → Structure projet, conventions

5. [PARALLÈLE - Développement]
   ├─ frontend-developer + react-expert
   │  → Composants, hooks
   ├─ nextjs-expert
   │  → Server Components, routing
   └─ backend-developer
      → API Routes, données

6. lead-dev
   → Code review, coordination

7. testing-process + devops
   → Tests, déploiement staging

8. project-management/livraison
   → Recette, PV, mise en production
```

### Pattern : Migration WordPress vers Next.js

```
1. direction-technique/audit-existant
   → Analyse WordPress actuel
   → Décision: Headless avec WP comme CMS

2. project-management
   → Planning migration, risques

3. [PHASE 1 - Infrastructure]
   ├─ devops
   │  → Setup Next.js + WP headless
   └─ wordpress-gutenberg-expert
      → API REST, ACF, Custom Post Types

4. [PHASE 2 - Frontend]
   ├─ nextjs-expert
   │  → App Router, ISR, Server Components
   ├─ frontend-developer
   │  → Composants, styles
   └─ design-system-foundations
      → Nouveau design system

5. testing-process
   → Tests de non-régression
   → Tests performance

6. devops/deployment
   → Stratégie blue-green
   → Rollback plan

7. project-management/livraison
   → Go-live progressif
```

### Pattern : Bug Fix Urgent

```
1. project-management/communication
   → Accusé réception client

2. direction-technique/support
   → Diagnostic, impact

3. lead-dev
   → Assignation, coordination

4. testing-process/types
   → Test reproduisant le bug

5. [frontend-developer ou backend-developer]
   → Fix

6. lead-dev/code-review
   → Validation rapide

7. devops
   → Hotfix deployment

8. project-management/communication
   → Notification client
```

### Pattern : Amélioration Performance

```
1. testing-process/performance
   → Audit: load testing, profiling, Core Web Vitals

2. direction-technique
   → Priorisation des optimisations

3. [PARALLÈLE selon les bottlenecks]
   ├─ nextjs-expert/optimization
   │  → SSR, ISR, edge functions
   ├─ frontend-developer/performance
   │  → Bundle size, lazy loading
   ├─ backend-developer/performance
   │  → Query optimization, caching
   └─ devops/monitoring
      → APM, alerting

4. testing-process/performance
   → Validation des gains
```

### Pattern : Audit Sécurité

```
1. direction-technique/securite
   → Définition scope, standards

2. testing-process/security
   → OWASP scan, dependencies audit, headers

3. [PARALLÈLE selon les findings]
   ├─ backend-developer/auth-security
   │  → Fix vulnérabilités API
   ├─ frontend-developer
   │  → XSS prevention
   └─ devops
      → Headers, secrets rotation

4. lead-dev/security-review
   → Validation fixes

5. testing-process/security
   → Re-test
```

## Règles de Composition

### 1. Toujours Respecter la Hiérarchie

```
❌ MAUVAIS : Aller directement en implémentation
   "Crée un composant Button" → react-expert

✅ BON : Respecter les niveaux
   direction-technique (si nouveau) → web-dev-process → react-expert
```

### 2. Un Orchestrateur Principal

Pour chaque workflow, un skill "lead" coordonne :
- Nouveau projet → `project-management`
- Migration technique → `direction-technique`
- Feature development → `lead-dev`
- Bug fix → `lead-dev` ou `direction-technique/support`
- Performance → `testing-process/performance`

### 3. Handoffs Explicites

Chaque transition entre skills produit un artefact :

| Transition | Artefact |
|------------|----------|
| Brief → Specs | Document de spécifications |
| Specs → Code | Tickets, critères d'acceptance |
| Code → Tests | Tests automatisés |
| Tests → Review | PR, coverage report |
| Review → Deploy | Changelog, tag release |

### 4. Points de Synchronisation

Valider humainement avant de passer au skill suivant :
- Fin de phase (setup, dev, test)
- Changement de niveau hiérarchique
- Décisions d'architecture

## Combinaisons Fréquentes

| Cas d'usage | Skills combinés |
|-------------|-----------------|
| App React complète | frontend-developer + react-expert + design-system |
| App Next.js fullstack | nextjs-expert + backend-developer + devops |
| Site WordPress moderne | wordpress-gutenberg + design-system |
| API Node.js | backend-developer + devops + testing-process |
| CI/CD complet | devops + testing-process + lead-dev |

## Anti-Patterns

### À Éviter

- **Skill soup** : Invoquer 5+ skills en parallèle sans coordination
- **Boucle infinie** : A → B → A → B...
- **Skip de niveau** : Aller directement en implémentation sans processus
- **Over-engineering** : Invoquer direction-technique pour un simple bug fix
- **Sous-utilisation** : Ne pas utiliser testing-process pour définir la stratégie tests

## Références

- [Graphe des dépendances](./dependency-graph.md)
- [Règles de routage](./routing.md)
- [Points d'escalade](./escalation.md)
- [ADR-005 : Frontières de responsabilités](../docs/adr/005-skill-responsibility-boundaries.md)
- [ADR-006 : Hiérarchie lead-dev/web-dev-process](../docs/adr/006-hierarchy-clarification.md)
