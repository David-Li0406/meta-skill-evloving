---
name: architecture-variants
description: Use this skill when designing new integrations, choosing between monolith, service layer, or microservice architectures, or planning migration paths for applications across various platforms.
---

# Architecture Variants

## Overview
Choose and implement validated architecture blueprints for different scales across various platforms.

## Prerequisites
- Understanding of team size and daily active user (DAU) requirements
- Knowledge of deployment infrastructure
- Clear service level agreement (SLA) requirements
- Growth projections available

## Architecture Variants

### Variant A: Monolith (Simple)

**Best for:** MVPs, small teams, < 10K daily active users

```
my-app/
├── src/
│   ├── platform/
│   │   ├── client.ts          # Singleton client
│   │   ├── types.ts           # Types
│   │   └── middleware.ts      # Express middleware
│   ├── routes/
│   │   └── api/
│   │       └── platform.ts    # API routes
│   └── index.ts
├── tests/
│   └── platform.test.ts
└── package.json
```

### Key Characteristics
- Single deployment unit
- Synchronous platform calls in request path
- In-memory caching
- Simple error handling

### Code Pattern
```typescript
// Direct integration in route handler
app.post('/api/create', async (req, res) => {
  try {
    const result = await platformClient.create(req.body);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### Variant B: Service Layer (Moderate)

**Best for:** Growing startups, 10K-100K DAU, multiple integrations

```
my-app/
├── src/
│   ├── services/
│   │   ├── platform/
│   │   │   ├── client.ts      # Client wrapper
│   │   │   ├── service.ts     # Business logic
│   │   │   ├── repository.ts  # Data access
│   │   │   └── types.ts
│   │   └── index.ts           # Service exports
│   ├── controllers/
│   │   └── platform.ts
│   ├── routes/
│   ├── middleware/
│   ├── queue/
│   │   └── platform-processor.ts  # Async processing
│   └── index.ts
├── config/
│   └── platform/
└── package.json
```

### Key Characteristics
- Separation of concerns
- Background job processing
- Redis caching
- Circuit breaker pattern
- Structured error handling

### Code Pattern
```typescript
// Service layer abstraction
class PlatformService {
  constructor(
    private client: PlatformClient,
    private repository: Repository
  ) {}

  async create(data) {
    // Business logic here
  }
}
```

## Instructions

### Step 1: Assess Requirements
Use the decision matrix to identify the appropriate variant.

### Step 2: Choose Architecture
Select Monolith, Service Layer, or Microservice based on needs.

### Step 3: Implement Structure
Set up project layout following the chosen blueprint.

### Step 4: Plan Migration Path
Document upgrade path for future scaling.

## Output
- Architecture variant selected
- Project structure implemented
- Migration path documented
- Appropriate patterns applied

## Error Handling
Refer to the comprehensive error handling documentation for best practices.

## Resources
- [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html)
- [Microservices Guide](https://martinfowler.com/microservices/)
- [Architecture Guide](https://example.com/docs/architecture)