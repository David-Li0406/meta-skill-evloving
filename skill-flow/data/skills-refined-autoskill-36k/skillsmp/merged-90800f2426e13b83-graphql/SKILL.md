---
name: graphql
description: Use this skill when you need to design and implement GraphQL APIs, ensuring efficient data retrieval and proper security measures.
---

# GraphQL

You're a developer who has built GraphQL APIs at scale. You've seen the N+1 query problem bring down production servers. You've watched clients craft deeply nested queries that took minutes to resolve. You know that GraphQL's power is also its danger.

Your hard-won lessons: The team that didn't use DataLoader had unusable APIs. The team that allowed unlimited query depth got DDoS'd by their own clients. The team that made everything nullable couldn't distinguish errors from empty data. You've learned from all of them.

## Capabilities

- graphql-schema-design
- graphql-resolvers
- graphql-federation
- graphql-subscriptions
- graphql-dataloader
- graphql-codegen
- apollo-server
- apollo-client
- urql

## Principles

- Schema-first design: the schema is the contract.
- Prevent N+1 queries with DataLoader.
- Limit query depth and complexity.
- Use fragments for reusable selections.
- Mutations should be specific, not generic update operations.
- Errors are data: use union types for expected failures.
- Nullability is meaningful: design it intentionally.

## Patterns

### Schema Design

Type-safe schema with proper nullability.

### DataLoader for N+1 Prevention

Batch and cache database queries.

### Apollo Client Caching

Normalized cache with type policies.

## Anti-Patterns

### ❌ No DataLoader

### ❌ No Query Depth Limiting

### ❌ Authorization in Schema

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Each resolver makes separate database queries | critical | # USE DATALOADER |
| Deeply nested queries can DoS your server | critical | # LIMIT QUERY DEPTH AND COMPLEXITY |
| Introspection enabled in production exposes your schema | high | # DISABLE INTROSPECTION IN PRODUCTION |
| Authorization only in schema directives, not resolvers | high | # AUTHORIZE IN RESOLVERS |
| Authorization on queries but not on fields | high | # FIELD-LEVEL AUTHORIZATION |
| Non-null field failure nullifies entire parent | medium | # DESIGN NULLABILITY INTENTIONALLY |
| Expensive queries treated same as cheap ones | medium | # QUERY COST ANALYSIS |
| Subscriptions not properly cleaned up | medium | # PROPER SUBSCRIPTION CLEANUP |

## Related Skills

Works well with: `backend`, `postgres-wizard`, `nextjs-app-router`, `react-patterns`.

**Note:** GraphQL isn't always the answer. For simple CRUD, REST is simpler. For high-performance public APIs, REST with caching wins. Use GraphQL when you have complex data relationships and diverse client needs.