---
name: ddd
description: |
  Redirection vers le skill DDD complet.
  Pour tout ce qui concerne le Domain-Driven Design, utilise le skill `ddd`.
workflows:
  - id: redirect-to-ddd-skill
    template: redirect
    name: Redirection vers skill DDD
---

# DDD (Redirection)

> **Ce fichier redirige vers le skill DDD complet.**
>
> **→ Voir : `.web-agency/skills/ddd/`**

## Ta Responsabilité Unique

> Rediriger toutes les demandes DDD vers le skill `ddd` spécialisé.

Tu NE fais PAS :
- L'implémentation DDD directe (→ `ddd/*`)
- Le modeling de domaine (→ `ddd/strategic/*`)
- Les patterns tactiques (→ `ddd/tactical/*`)

## Pourquoi cette redirection ?

Le skill `ddd` est le **skill de référence** pour tout ce qui concerne le Domain-Driven Design. Il offre une couverture complète avec **34 agents spécialisés** :

### Strategic (8 agents)
- Event Storming, Domain Storytelling, Example Mapping
- Bounded Contexts, Context Mapping, Ubiquitous Language
- Core Domain Identification

### Tactical (17 agents)
- Entities, Value Objects, Aggregates
- Repositories, Domain Services, Domain Events, Domain Errors
- Factories, Specifications, Domain Primitives
- Application Services, Clean Architecture
- CQRS, Event Sourcing, Saga/Process Manager
- Anti-Corruption Layer

### Tooling (3 agents)
- Model Validator (audit anti-patterns)
- Pattern Selector (aide à la décision)
- Performance Guide (aggregate sizing, snapshots)

### Templates (3 agents)
- Aggregate Template, Value Object Template, Repository Template

### Case Studies (2 agents)
- E-commerce Domain, Anemic-to-Rich Migration

### Integrations (1 agent)
- Next.js Integration

## Quand utiliser le skill DDD ?

1. Comprendre un domaine métier complexe
2. Identifier les bounded contexts
3. Créer un ubiquitous language
4. Modéliser des entités et agrégats
5. Structurer du code selon Clean Architecture
6. Choisir entre CQRS, Event Sourcing, Sagas

## Ce qui reste dans backend-developer

| Responsabilité | Agent |
|----------------|-------|
| Implémentation API REST/GraphQL | `api/*` |
| Bases de données, queries | `data/*` |
| Architecture microservices | `architecture/microservices` |
| Architecture event-driven | `architecture/event-driven` |

## Mots-clés de routage

`ddd`, `domain driven design`, `bounded context`, `aggregate`, `entity`, `value object`, `ubiquitous language`, `event storming`

→ **Tous ces mots-clés doivent router vers le skill `ddd`**
