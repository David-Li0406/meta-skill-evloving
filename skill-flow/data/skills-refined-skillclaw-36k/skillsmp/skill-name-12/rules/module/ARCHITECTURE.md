---
name: architecture
description: Module architecture and structure
argument-hint: N/A
---

# Architecture

- [Language/Framework](#languageframework)
  - [Frontend? (if applicable)](#frontend-if-applicable)
  - [Backend? (if applicable)](#backend-if-applicable)
    - [Database](#database)
  - [Mobile? (if applicable)](#mobile-if-applicable)
- [Full project structure](#full-project-structure)
  - [Naming Conventions](#naming-conventions)
- [Services communication](#services-communication)
  - [\<Communication 1\>](#communication-1)
  - [External Services](#external-services)
    - [\<External Service 1\>](#external-service-1)

## Language/Framework

### Frontend? (if applicable)

- **Framework**: [Framework] → @frontend/package.json
- **UI Library**: [Library] - [Brief description]
- **Routing**: [Solution] - [Brief description]
- **Data Fetching**: [Solution] - [Brief description]
- **Form Handling**: [Solution] - [Brief description]
- **Validation**: [Solution] - [Brief description]
- **State Management**: [Solution] - [Brief description]
- **Build Tool**: [Tool] - [Brief description]
- **Structure**: [Solution] - [Brief description]

### Backend? (if applicable)

- **Language/Framework**: [Language/Framework] → @backend/package.json, @composer.json etc
- **API Style**: [REST/GraphQL/tRPC] - [Brief description]
- **Architecture**: [Architecture] - [Brief description]
- **ORM**: [ORM] - [Brief description]
- **Schema path**: [Path to schema files] - [Brief description]
- **Endpoints**: [Path to endpoint files] - [Brief description]
- **Database**: [Database] - [Brief description]
- **Caching**: [Solution] - [Brief description]
- **Testing**: [Tool] - [Brief description]

#### Database

- **Type**: [PostgreSQL/MySQL/MongoDB/etc]
- **ORM/Driver**: [Prisma/TypeORM/Mongoose/etc]
- **Connection**: [Connection details] - [Brief description]
- **Migration**: [Migration tool] - [Brief description]
- **Seeding**: [Seeding tool] - [Brief description]
- **Mock**: [Mock tool] - [Brief description]

### Mobile? (if applicable)

- **Framework**: [React Native/Flutter/Native] → @mobile/package.json
- **State Management**: [Solution] - [Brief description]
- **Platform**: [iOS/Android/Both] - [Brief description]

## Full project structure

Detailed essential structure of the project, including main folders and their purposes, key files, and any important configurations.

```text
{{Important project structure}}
```

### Naming Conventions

- **Files**: [pattern - camelCase/kebab-case/PascalCase]
- **Components?**: [pattern - PascalCase]
- **Functions**: [pattern - camelCase]
- **Variables**: [pattern - camelCase]
- **Constants**: [pattern - UPPER_CASE]
- **Types/Interfaces**: [pattern - PascalCase]

## Services communication

Internal communication between services, (e.g. for frontend: React Form Component → State Management → API Service → Backend API Endpoint, but way more detailed).

### <Communication 1>

```mermaid
{{Simple schema of the communication between services}}
```

### External Services

List of external services used in the project (e.g., AWS, Firebase, Stripe), including their purpose and integration points.

#### <External Service 1>

```mermaid
{{Simple schema of the communication between services}}
```
