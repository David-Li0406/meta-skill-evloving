# Architecture

This file is an example placeholder referenced by the Skill Creator skill.

## System Overview

- **Purpose**: [What the system/service does]
- **Primary users**: [Who uses it]
- **Key constraints**: [Latency, compliance, cost, etc.]

## High-Level Diagram

Describe the major components and their interactions:

- **Clients** → **API** → **Services** → **Datastores**
- **Async processing**: queues, workers, scheduled jobs

## Key Components

- **Service A**: [Responsibilities, inputs/outputs]
- **Service B**: [Responsibilities, dependencies]
- **Datastore**: [Schema ownership, migrations]

## Data Flow

1. [Request enters system]
2. [Validation/auth]
3. [Core logic]
4. [Persistence]
5. [Response]

## Cross-Cutting Concerns

- **Authentication/Authorization**: [Mechanism, roles]
- **Observability**: logs/metrics/traces conventions
- **Error handling**: retry/backoff, idempotency
- **Performance**: hot paths and known bottlenecks

## Change Guide

- Where to add new endpoints
- Where domain logic lives
- How to add a new data model or migration
