# Changelog

Toutes les modifications notables de ce skill sont documentées ici.

Format basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

## [1.0.0] - 2026-01-17

### Ajouté

#### Strategic (8 agents)
- **orchestrator** : Routage vers les agents strategic
- **bounded-contexts** : Identification et délimitation des contextes
- **context-mapping** : Relations entre contextes (Shared Kernel, ACL, etc.)
- **ubiquitous-language** : Construction du vocabulaire partagé
- **core-domain-identification** : Classification Core/Supporting/Generic
- **event-storming** : Facilitation d'ateliers de découverte
- **domain-storytelling** : Narration visuelle des processus
- **example-mapping** : Découverte par exemples (Given-When-Then)

#### Tactical (17 agents)
- **orchestrator** : Routage vers les agents tactical
- **entities** : Modélisation des entités
- **value-objects** : Objets valeur immuables
- **aggregates** : Agrégats et racines d'agrégat
- **repositories** : Interfaces de persistance
- **domain-services** : Logique métier transverse
- **domain-events** : Événements du domaine
- **domain-errors** : Gestion des erreurs métier typées (Result/Either patterns)
- **factories** : Création complexe d'agrégats
- **specifications** : Règles métier composables
- **domain-primitives** : Types primitifs typés
- **application-services** : Use Cases et orchestration
- **clean-architecture** : Structure en couches concentriques
- **anti-corruption-layer** : Protection du domaine, patterns ACL
- **cqrs** : Séparation Command/Query, Read Models, Projections
- **event-sourcing** : Events comme source de vérité, snapshots, RGPD
- **saga-process-manager** : Orchestration processus longs, compensations

#### Tooling (3 agents)
- **model-validator** : Audit de modèles, détection anti-patterns
- **pattern-selector** : Aide à la décision avec arbres de décision
- **performance-guide** : Optimisation (aggregate sizing, snapshots, projections)

#### Templates (3 agents)
- **aggregate-template** : Template complet Aggregate avec TS/Java
- **value-object-template** : Templates VO (Money, Email, Address, DateRange)
- **repository-template** : Interface domaine + implémentation infra

#### Case Studies (2 agents)
- **e-commerce-domain** : Cas end-to-end (Event Storming → Bounded Contexts → Aggregates)
- **anemic-to-rich-migration** : Guide migration Strangler Fig étape par étape

#### Integrations (1 agent)
- **nextjs-integration** : DDD avec Next.js App Router, Server Actions, API Routes

### Infrastructure

- SKILL.md avec philosophie, routage et workflow
- Organisation en 6 domaines (strategic, tactical, tooling, templates, case-studies, integrations)
- Tables de routage par mots-clés et par phase de projet
- Suite de tests complète avec 4 suites (813 tests)
- Test runner avec timing détaillé, sortie JSON, sélection de suites
- ADR-008 : Standard Mermaid pour diagrammes
