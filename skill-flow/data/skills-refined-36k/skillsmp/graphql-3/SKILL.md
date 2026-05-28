---
name: graphql
description: Read when modifying *.graphql files
---

# GraphQL Rules


## Scalars
- For numbers, use the right scalar. We have `PositiveX`, `NonNegativeX`, etc. Where "X" can be `Float`, `Integer`
- In almost all cases, we use `NonEmptyString` for strings, can be null but not empty string
- **Use `Email` scalar for email fields, `Phone` scalar for phone fields** (not `NonEmptyString`)
- We have various custom scalars, you can find them in codegen.yml

## Codegen
- If you change .graphql files, you need to run `npm run gql:codegen` to update them. Needs a running local API server
- If you get an error about the server being down, stop and ask the developer to start it, don't keep going

## Don'ts
- Don't leave properties as nullable when they shouldn't be
- Array types NEVER support a nullable type inside
- All inputs to queries and mutations should be wrapped in an `input` unless it's, by design, a single value (like an ID)

## Naming
- Queries: Noun for one, plural for many (e.g., `user`, `tasks`)
- Mutations: Verb+Noun (e.g., `updateOrganization`)

## Schema Structure Patterns
- Entity types implement `Node` interface
- Input types: `CreateEntityInput`, `UpdateEntityInput`, `EntitiesInput` (for filtering)
- Payload types: `EntitiesPayload implements PagePayload` for paginated lists
- ID fields in inputs: `entityId` (e.g., `productId`, `receiptId`)

## Standard Entity Fields
- All entities: `id`, `createdAt`, `updatedAt`
- Status field: `status: EntityStatus`
- Collections: `tags: [NonEmptyString!]!` (non-nullable array, nullable elements not allowed)

## Input Patterns
- Create inputs: all required fields except optional ones
- Update inputs: entity ID + all optional fields (make everything nullable except ID)
- Filter inputs: support `page`, `order`, `search`, plus entity-specific filters
- Date ranges: `createdAt`/`updatedAt`/etc. are a `DateTimeFilter` or `DateFilter` (depending on the field type)

## Query/Mutation Structure
- Single entity query: `entity(entityId: ID!): Entity!`
- List query: `entities(input: EntitiesInput): EntitiesPayload!` (usually paginated and superadmin only)
- Create mutation: `createEntity(input: CreateEntityInput!): Entity!`
- Update mutation: `updateEntity(input: UpdateEntityInput!): Entity!`
