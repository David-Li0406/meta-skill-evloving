---
name: reference-architecture
description: Use this skill when designing new integrations or reviewing project structures for Exa or Supabase applications, ensuring adherence to best practices and standards.
---

# Reference Architecture

## Overview
Implement reference architecture patterns for Exa and Supabase integrations, focusing on best-practice project layouts.

## Prerequisites
- Understanding of layered architecture
- Knowledge of the respective SDK (Exa or Supabase)
- TypeScript project setup
- Testing framework configured

## Project Structure

```
my-project/
├── src/
│   ├── client.ts           # Singleton client wrapper
│   ├── config.ts           # Environment configuration
│   ├── types.ts            # TypeScript types
│   ├── errors.ts           # Custom error classes
│   ├── handlers/           # Webhook and event handlers
│   ├── services/           # Business logic and orchestration
│   ├── api/                # API endpoints
│   └── jobs/               # Background jobs
├── tests/                  # Unit and integration tests
├── config/                 # Environment-specific configurations
└── docs/                   # Documentation
```

## Layer Architecture

```
┌─────────────────────────────────────────┐
│             API Layer                    │
│   (Controllers, Routes, Webhooks)        │
├─────────────────────────────────────────┤
│           Service Layer                  │
│  (Business Logic, Orchestration)         │
├─────────────────────────────────────────┤
│          Client Layer                    │
│   (Client, Types, Error Handling)        │
├─────────────────────────────────────────┤
│         Infrastructure Layer             │
│    (Cache, Queue, Monitoring)            │
└─────────────────────────────────────────┘
```

## Key Components

### Step 1: Client Wrapper
```typescript
// src/client.ts
export class Service {
  private client: ClientType; // Replace ClientType with ExaClient or SupabaseClient
  // Additional implementation details...
}
```

### Step 2: Error Handling
Implement custom error classes for handling operations specific to Exa or Supabase.

### Step 3: Health Checks
Add health check endpoints to ensure connectivity with Exa or Supabase.

## Output
- Structured project layout
- Client wrapper with caching
- Error boundary implemented
- Health checks configured

## Resources
- [Exa SDK Documentation](https://exa.com/docs/sdk)
- [Supabase SDK Documentation](https://supabase.com/docs/sdk)
- [Best Practices](https://exa.com/docs/best-practices) / [Supabase Best Practices](https://supabase.com/docs/best-practices)