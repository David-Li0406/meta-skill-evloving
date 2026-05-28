---
name: dependency-graph
description: Graphe des dépendances entre skills
version: 1.0.0
---

# Skill Dependency Graph

Ce document visualise les relations et dépendances entre les 12 skills de web-agency.

## Vue d'Ensemble

```mermaid
flowchart TB
    WA["WEB-AGENCY<br/>Méta-Orchestrateur<br/>(409 agents total)"]

    GP["GESTION<br/>PROJET"]
    TECH["TECHNIQUE<br/>(Dev)"]
    DESIGN["DESIGN<br/>(Futur)"]

    WA --> GP
    WA --> TECH
    WA --> DESIGN

    classDef meta fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef domain fill:#fff3e0,stroke:#e65100

    class WA meta
    class GP,TECH,DESIGN domain
```

## Hiérarchie des Skills (3 Niveaux)

```mermaid
flowchart TB
    subgraph N1["NIVEAU 1 : STRATÉGIE<br/>(POURQUOI - Décisions, politiques, standards)"]
        DT["direction-technique (52)<br/>Architecture • Choix technologiques<br/>Standards • Estimation"]
    end

    subgraph N2["NIVEAU 2 : OPÉRATIONS / PROCESSUS<br/>(QUOI/QUI - Méthodologie, process, coordination)"]
        WDP["web-dev-process (61)<br/>──────────────<br/>QUOI: Méthodo<br/>• 7 phases<br/>• Checklists<br/>• Workflows"]
        TP["testing-process (25)<br/>──────────────<br/>QUOI: Tests<br/>• Stratégie<br/>• Types tests<br/>• Qualité/Perf"]
        LD["lead-dev (27)<br/>──────────────<br/>QUI: Coordination<br/>• Code review<br/>• Mentoring<br/>• Delivery"]
    end

    subgraph N3["NIVEAU 3 : IMPLÉMENTATION<br/>(COMMENT - Code, configuration, patterns)"]
        FD["frontend-developer<br/>(33)"]
        BD["backend-developer<br/>(32)"]
        DO["devops<br/>(30)"]
        WG["wordpress-gutenberg<br/>(41)"]
        DS["design-system<br/>(21)"]
        RE["react-expert<br/>(28)"]
        NE["nextjs-expert<br/>(35)"]
    end

    subgraph PM["SÉPARÉ : GESTION PROJET"]
        PMG["project-management (24)<br/>Brief • Estimation • Planning<br/>Communication • Livraison • Facturation"]
    end

    DT --> WDP
    DT --> TP
    DT --> LD

    WDP --> FD
    WDP --> BD
    WDP --> DO
    WDP --> WG
    WDP --> DS
    TP --> FD
    TP --> BD
    LD --> FD
    LD --> BD

    BD --> RE
    BD --> NE
    FD --> RE

    classDef niveau1 fill:#e1f5fe,stroke:#01579b
    classDef niveau2 fill:#fff3e0,stroke:#e65100
    classDef niveau3 fill:#e8f5e9,stroke:#2e7d32
    classDef gestion fill:#fce4ec,stroke:#c2185b

    class N1,DT niveau1
    class N2,WDP,TP,LD niveau2
    class N3,FD,BD,DO,WG,DS,RE,NE niveau3
    class PM,PMG gestion
```

## Graphe des Dépendances

### Dépendances Directes

```
direction-technique
├── web-dev-process       [suit les politiques tech]
├── testing-process       [suit les standards qualité]
├── lead-dev              [applique les décisions]
├── frontend-developer    [implémente les specs]
├── backend-developer     [implémente les specs]
├── devops                [déploie selon les standards]
├── wordpress-gutenberg   [implémente les specs WP]
└── design-system         [applique les guidelines]

web-dev-process
├── testing-process       [s'intègre dans les phases]
├── frontend-developer    [phase implementation]
├── backend-developer     [phase implementation]
├── devops                [phase setup/deployment]
└── wordpress-gutenberg   [phase implementation]

lead-dev
├── frontend-developer    [code review, mentoring]
├── backend-developer     [code review, mentoring]
├── devops                [review infra]
└── wordpress-gutenberg   [code review]

frontend-developer
├── react-expert          [spécialisation React]
├── nextjs-expert         [spécialisation Next.js]
└── design-system         [consomme les tokens/composants]

backend-developer
├── devops                [collaboration déploiement]
└── nextjs-expert         [Server Components, API Routes]

project-management
├── direction-technique   [estimation technique]
└── [tous les skills]     [coordination projet]
```

### Relations par Domaine Technique

```mermaid
flowchart TB
    subgraph TESTING["DOMAINE: TESTING"]
        direction TB
        TP2["testing-process (STRATÉGIE - 25 agents)<br/>• Définit QUOI/QUAND tester<br/>• Pyramide, TDD/BDD, planning<br/>• Qualité, performance, sécurité"]

        subgraph IMPL_TEST["Skills d'IMPLÉMENTATION (COMMENT tester)"]
            FDT["frontend-developer/testing/<br/>vitest, RTL, playwright"]
            BDT["backend-developer/testing/<br/>jest, supertest, db tests"]
            RET["react-expert/testing/<br/>hooks, components, mocks"]
            NET["nextjs-expert/testing/<br/>server components, e2e"]
            WGT["wordpress-gutenberg/testing/<br/>wp-env, jest for blocks"]
        end

        TP2 --> IMPL_TEST
    end

    subgraph SECURITE["DOMAINE: SÉCURITÉ"]
        direction TB
        DTS["direction-technique/securite (POLITIQUE - 5 agents)<br/>• Définit les politiques sécurité<br/>• RGPD, audit, gestion secrets"]
        TPS["testing-process/security (TESTS - 4 agents)<br/>• Tests OWASP, dépendances, headers"]

        subgraph IMPL_SEC["Skills d'IMPLÉMENTATION"]
            BDS["backend-developer/auth-security/<br/>JWT, OAuth, crypto"]
            DOS["devops/security/<br/>container security"]
            WGS["wordpress-gutenberg/security/<br/>nonces, sanitization"]
        end

        DTS --> TPS --> IMPL_SEC
    end

    subgraph DEVOPS["DOMAINE: DEVOPS"]
        direction TB
        DTD["direction-technique/devops (POLITIQUE)<br/>• Standards CI/CD, environnements"]
        WDPD["web-dev-process/setup (PROCESS)<br/>• Checklists setup, workflows"]
        DOD["devops (IMPLÉMENTATION - 30 agents)<br/>• CI/CD, containers, K8s, IaC, monitoring"]

        DTD --> WDPD --> DOD
    end

    classDef strategy fill:#e1f5fe,stroke:#01579b
    classDef process fill:#fff3e0,stroke:#e65100
    classDef impl fill:#e8f5e9,stroke:#2e7d32

    class TP2,DTS,DTD strategy
    class TPS,WDPD process
    class IMPL_TEST,IMPL_SEC,FDT,BDT,RET,NET,WGT,BDS,DOS,WGS,DOD impl
```

## Matrice de Collaboration

| Skill Source | → Collabore avec | Type de Relation |
|--------------|------------------|------------------|
| direction-technique | tous | dépendance descendante |
| web-dev-process | testing-process | complémentaire |
| web-dev-process | lead-dev | synchronisation |
| lead-dev | frontend-developer | review, mentoring |
| lead-dev | backend-developer | review, mentoring |
| frontend-developer | react-expert | spécialisation |
| frontend-developer | nextjs-expert | spécialisation |
| frontend-developer | design-system | consommation |
| backend-developer | devops | déploiement |
| backend-developer | nextjs-expert | Server Components |
| testing-process | tous skills techniques | méthodologie |
| project-management | tous | coordination |

## Flux de Travail Typiques

### Nouveau Projet Web

```mermaid
flowchart TB
    PM1["project-management"]
    DT["direction-technique"]
    WDP["web-dev-process"]
    LD["lead-dev"]
    TP["testing-process"]
    DO["devops"]
    INFRA(["infra ready"])
    FD["frontend-developer"]
    BD["backend-developer"]
    RE["react-expert"]
    DS["design-system"]
    APP(["application"])
    PM2["project-management<br/>(livraison)"]

    PM1 -->|"brief"| DT
    DT --> WDP
    DT --> LD
    WDP --> TP
    WDP --> DO
    LD -->|"coordination"| FD
    LD -->|"coordination"| BD
    DO --> INFRA
    TP --> FD
    TP --> BD
    INFRA --> FD
    INFRA --> BD
    FD --> RE
    FD --> DS
    RE --> APP
    DS --> APP
    BD --> APP
    APP --> PM2

    classDef management fill:#fce4ec,stroke:#c2185b
    classDef strategy fill:#e1f5fe,stroke:#01579b
    classDef process fill:#fff3e0,stroke:#e65100
    classDef impl fill:#e8f5e9,stroke:#2e7d32
    classDef milestone fill:#f5f5f5,stroke:#9e9e9e

    class PM1,PM2 management
    class DT strategy
    class WDP,TP,LD,DO process
    class FD,BD,RE,DS impl
    class INFRA,APP milestone
```

### Bug Fix Critique

```mermaid
flowchart TB
    PM1["project-management<br/>(notification client)"]
    DTS["direction-technique/support<br/>(diagnostic)"]
    LD["lead-dev<br/>(coordination)"]
    TP["testing-process<br/>(reproduction)"]
    DEV["frontend/backend-developer"]
    DO["devops<br/>(hotfix deploy)"]
    PM2["project-management<br/>(notification client)"]

    PM1 --> DTS
    DTS --> LD
    DTS --> TP
    LD --> DEV
    TP --> DEV
    DEV --> DO
    DO --> PM2

    classDef management fill:#fce4ec,stroke:#c2185b
    classDef strategy fill:#e1f5fe,stroke:#01579b
    classDef process fill:#fff3e0,stroke:#e65100
    classDef impl fill:#e8f5e9,stroke:#2e7d32

    class PM1,PM2 management
    class DTS strategy
    class LD,TP,DO process
    class DEV impl
```

## Bonnes Pratiques

### Composition Verticale (Haut → Bas)

```mermaid
flowchart TB
    subgraph HIERARCHIE["TOUJOURS respecter la hiérarchie"]
        direction TB
        P1["1. POURQUOI<br/>(direction-technique)"]
        P2["2. QUOI<br/>(web-dev-process, testing-process)"]
        P3["3. QUI<br/>(lead-dev)"]
        P4["4. COMMENT<br/>(skills implémentation)"]
        P1 --> P2 --> P3 --> P4
    end

    classDef n1 fill:#e1f5fe,stroke:#01579b
    classDef n2 fill:#fff3e0,stroke:#e65100
    classDef n3 fill:#fce4ec,stroke:#c2185b
    classDef n4 fill:#e8f5e9,stroke:#2e7d32

    class P1 n1
    class P2 n2
    class P3 n3
    class P4 n4
```

### Composition Horizontale (Parallèle)

```mermaid
flowchart LR
    subgraph OK["✅ OK pour paralléliser"]
        direction TB
        A1["frontend-developer"] ~~~ A2["backend-developer"]
        B1["react-expert"] ~~~ B2["design-system"]
        C1["testing-process"] ~~~ C2["devops (setup)"]
    end

    subgraph NOPE["❌ NE PAS paralléliser"]
        direction TB
        D1["direction-technique"] -.-x D2["implémentation<br/>(sans validation)"]
        E1["lead-dev review"] -.-x E2["merge<br/>(avant approbation)"]
    end

    classDef ok fill:#e8f5e9,stroke:#2e7d32
    classDef nope fill:#ffebee,stroke:#c62828

    class OK,A1,A2,B1,B2,C1,C2 ok
    class NOPE,D1,D2,E1,E2 nope
```

## Références

- [ADR-005 : Frontières de responsabilités](../docs/adr/005-skill-responsibility-boundaries.md)
- [ADR-006 : Hiérarchie lead-dev/web-dev-process](../docs/adr/006-hierarchy-clarification.md)
- [Règles de routage](./routing.md)
- [Composition des skills](./composition.md)
