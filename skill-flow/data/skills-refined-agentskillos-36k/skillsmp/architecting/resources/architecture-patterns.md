# Architecture Patterns (Mermaid Templates)

Use these templates to visualize the system structure before coding.

## 1. Indie App Pattern (Monolith / Simple 3-Tier)

Direct connection from Frontend to Backend API, sharing types.

```mermaid
C4Context
    title Indie App Architecture (Speed & Simplicity)

    Person(user, "User", "Uses the app web/mobile")
    
    System_Boundary(b1, "The Application") {
        Container(spa, "Single Page App", "React/Vite", "MUI v7, TanStack Query")
        Container(api, "Backend API", "Node/Express", "Layered Arch, Prisma")
        ContainerDb(db, "Database", "PostgreSQL", "Main application data")
    }

    Rel(user, spa, "Uses", "HTTPS")
    Rel(spa, api, "API Calls", "JSON/REST", "Shared Zod Types")
    Rel(api, db, "Reads/Writes", "Prisma Client")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## 2. Enterprise App Pattern (Microservices / Modular)

Introduction of API Gateway, separate services, and strict boundaries.

```mermaid
C4Context
    title Enterprise App Architecture (Scale & Stability)

    Person(user, "User", "Composite UI usage")
    
    System_Boundary(frontend, "Frontend Layer") {
        Container(mfe1, "Dashboard MFE", "React/Vite", "Feature: Analytics")
        Container(mfe2, "Admin MFE", "React/Vite", "Feature: User Mgmt")
    }

    System_Boundary(gateway, "Gateway Layer") {
        Container(bff, "API Gateway / BFF", "Node.js", "Auth, Rate Limiting, Aggregation")
    }

    System_Boundary(services, "Backend Services") {
        Container(svc_auth, "Auth Service", "Express", "Identity Mgmt")
        Container(svc_core, "Core Features", "Express", "Business Logic")
        Container(svc_rpt, "Reporting Service", "Python/Go", "Heavy Compute")
    }

    ContainerDb(db_core, "Core DB", "PostgreSQL", "Transaction Data")
    ContainerDb(db_rpt, "Analytics DB", "ClickHouse", "OLAP Data")

    Rel(user, mfe1, "Uses")
    Rel(mfe1, bff, "API Calls")
    Rel(mfe2, bff, "API Calls")
    
    Rel(bff, svc_auth, "gRPC/REST")
    Rel(bff, svc_core, "gRPC/REST")
    Rel(bff, svc_rpt, "gRPC/REST")
    
    Rel(svc_core, db_core, "SQL")
    Rel(svc_rpt, db_rpt, "SQL")
```
