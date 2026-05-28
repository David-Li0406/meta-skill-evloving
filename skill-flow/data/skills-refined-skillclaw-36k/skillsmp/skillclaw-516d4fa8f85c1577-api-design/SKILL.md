---
name: api-design
description: Use this skill when reasoning about API surfaces, packages, protobuf schema, versioning, compatibility adapters, or domain action handlers.
---

# Skill body

## The Meaning of "API"

An **API** (Application Programming Interface) provides a pathway for users to perform actions within a domain. It is always versioned to maintain client contracts and adapts protobuf-generated request/response messages to domain command/query objects. The API surface acts as a compatibility membrane between external clients and the evolving domain.

## Data Flow

1. **HTTP JSON**
    - ↓
2. **Authentication (no DB access)**
    - Verify token
    - Extract identity
    - ↓
3. **Parse JSON**
    - ↓
4. **Hydrate protobuf request (v1/v2/v3)**
    - ↓
5. **Optional early Authorization**
    - Must use only read-only or cached data
    - No domain DB access
    - ↓
6. **Compat layer (adapt versioned request to canonical action)**
    - Normalize
    - Validate
    - Coerce
    - Convert to domain types
    - Map fields
    - Pure logic only (no DB access)
    - ↓
7. **Domain command dataclass**
    - ↓
8. **Domain handler**
    - Hydrate identifiers to domain objects
    - Domain-dependent authorization
    - DB access and side effects are fine
    - ↓
9. **Domain result**
    - ↓
10. **Compat layer:**
    - Map domain to versioned protobuf response
    - ↓
11. **Serialize protobuf to JSON**
    - ↓
12. **HTTP response**

> Note: Nothing before the domain handler should hit the domain DB; the compat layer can only use pure domain logic.