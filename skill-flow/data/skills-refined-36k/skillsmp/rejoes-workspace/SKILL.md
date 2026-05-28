---
name: rejoes-workspace
description: ReJoEs Backend – AI Skills & Responsibilities
---

# ReJoEs Backend – AI Skills & Responsibilities

This file defines what the AI agent IS ALLOWED and EXPECTED to do
when working on the ReJoEs backend.

---

## 1. Core Technical Stack Skills

The AI should confidently use and generate:

- Node.js (TypeScript)
- Express or Fastify (explicit routing)
- Prisma ORM
- SQLite (dev/test)
- PostgreSQL (production-ready schemas)
- Sharp (image processing)
- Multipart file uploads
- RESTful API design
- Transaction-safe logic

---

## 2. Backend Architecture Skills

The AI is expected to:

- Design clean controller → service → data layers
- Centralize business rules (tiers, allowances, limits)
- Use Prisma transactions for all mutations
- Keep controllers thin and logic testable
- Avoid duplication of rule logic

---

## 3. API Design Responsibilities

The AI may:
- Create REST endpoints exactly matching the spec
- Validate request payloads
- Return structured, predictable JSON errors
- Enforce idempotency and safety rules

The AI may NOT:
- Add extra endpoints
- Modify API contracts without instruction
- Add optional behavior not described

---

## 4. Subscription Sync Handling

The AI should:
- Parse Shopify subscription webhook payloads
- Map Shopify fields → internal member fields
- Normalize tier and status values
- Detect billing cycle changes
- Trigger counter resets safely

---

## 5. Image Handling Skills

The AI may:
- Accept multipart uploads
- Compress images
- Generate thumbnails
- Store local file paths
- Return URLs relative to the server

The AI must:
- Treat photos as immutable loan identifiers
- Never overwrite an existing loan photo

---

## 6. Data Integrity Skills

The AI is expected to:
- Prevent race conditions
- Prevent double-loans
- Prevent counter drift
- Handle retry-safe operations
- Use idempotency keys correctly

---

## 7. Testing & Dev Workflow

The AI may:
- Generate Prisma schemas
- Create seed data
- Write basic API tests
- Support SQLite file-based databases

The AI should:
- Keep production compatibility in mind
- Avoid SQLite-only hacks

---

## 8. Error Handling Expectations

The AI should:
- Return meaningful error messages for POS staff
- Fail fast on rule violations
- Avoid silent failures
- Never partially complete a swap

---

## 9. Security Awareness

The AI must:
- Verify Shopify webhooks
- Avoid leaking internal IDs unnecessarily
- Assume POS runs in semi-trusted environments
- Never expose admin-only logic publicly

---

## 10. Delivery Expectations

When asked to build:
- The AI should generate **complete, production-grade backend code**
- File trees must be explicit
- Functions must match the spec exactly
- No placeholder or speculative logic

---

## 11. Mental Model Alignment

The AI should always reason using this model:

- Photos = items
- Loans = circulation
- Time = velocity
- Subscriptions = funding
- Shopify = billing truth
- Backend = operational truth

If a proposed feature breaks this mental model,
the AI should reject it.

