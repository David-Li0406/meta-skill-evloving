---
name: api-design
description: Use this when reasoning about API surfaces, packages, protobuf schema, versioning, compatibility adapters or domain action handlers.
---
## The Meaning of "API"

An **API** (Application Programming Interface)...

- provides a pathway for users to perform actions within a domain
- is always versioned (so client contracts are kept)
- adapts protobuf-generated request/response messages to domain command/query objects

The API surface is a compatibility membrane between external clients and the evolving domain.

## Data Flow

HTTP JSON
    ↓
Authentication (no DB access)
    - verify token
    - extract identity
    ↓
Parse JSON
    ↓
Hydrate protobuf request (v1/v2/v3)
    ↓
Optional early Authorization
    - must use only read‑only or cached data
    - no domain DB access
    ↓
Compat layer (adapt versioned request to canonical action)
    - normalize
    - validate
    - coerce
    - convert to domain types
    - map fields
    - pure logic only (no DB access)
    ↓
Domain command dataclass
    ↓
Domain handler
    - hydrate identifiers to domain objects
    - domain-dependent authorization
    - DB access and side effects are fine
    ↓
Domain result
    ↓
Compat layer:
    - map domain to versioned protobuf response
    ↓
Serialize protobuf to JSON
    ↓
HTTP response

Nothing before the domain handler should hit the domain DB; compat layer can only use pure domain logic.
