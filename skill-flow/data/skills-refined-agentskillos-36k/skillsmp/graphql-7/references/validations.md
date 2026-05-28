# Graphql - Validations

## Introspection enabled in production

### **Id**
introspection-enabled
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - introspection:\s*true
### **Message**
Introspection should be disabled in production
### **Fix Action**
Set introspection: process.env.NODE_ENV !== 'production'
### **Applies To**
  - *.ts
  - *.js

## Direct database query in resolver

### **Id**
no-dataloader
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - findUnique\s*\(\s*\{\s*where.*id
  - findOne\s*\(\s*\{\s*where.*id
  - findById\s*\(
### **Message**
Consider using DataLoader to batch and cache queries
### **Fix Action**
Create DataLoader and use .load() instead of direct query
### **Applies To**
  - **/resolvers/**
  - *.resolver.ts
  - *.resolvers.ts

## No query depth limiting

### **Id**
no-depth-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new ApolloServer\s*\(\s*\{(?![\s\S]*depthLimit)
### **Message**
Consider adding depth limiting to prevent DoS
### **Fix Action**
Add validationRules: [depthLimit(10)]
### **Applies To**
  - *.ts
  - *.js

## Resolver without try-catch

### **Id**
resolver-without-error-handling
### **Severity**
info
### **Type**
regex
### **Pattern**
  - async\s*\([^)]*\)\s*=>\s*\{(?![\s\S]*try\s*\{)
### **Message**
Consider wrapping resolver logic in try-catch
### **Fix Action**
Add error handling to provide better error messages
### **Applies To**
  - **/resolvers/**
  - *.resolver.ts

## JSON or Any type in schema

### **Id**
any-type-in-schema
### **Severity**
info
### **Type**
regex
### **Pattern**
  - scalar\s+JSON
  - scalar\s+Any
  - :\s*JSON\s*[!\]\)]
### **Message**
Avoid JSON/Any types - they bypass GraphQL's type safety
### **Fix Action**
Define proper input/output types
### **Applies To**
  - *.graphql
  - *.gql

## Mutation returns bare type instead of payload

### **Id**
mutation-no-payload
### **Severity**
info
### **Type**
regex
### **Pattern**
  - type\s+Mutation\s*\{^}]*:\s*\w+\s*!
### **Message**
Consider using payload types for mutations (includes errors)
### **Fix Action**
Create CreateUserPayload type with user and errors fields
### **Applies To**
  - *.graphql
  - *.gql

## List field without pagination arguments

### **Id**
list-without-pagination
### **Severity**
info
### **Type**
regex
### **Pattern**
  - :\s*\[\w+!?\]!?\s*$
### **Message**
List fields should have pagination (limit, first, after)
### **Fix Action**
Add arguments: field(limit: Int, offset: Int): [Type!]!
### **Applies To**
  - *.graphql
  - *.gql

## Query hook without error handling

### **Id**
no-error-handling-query
### **Severity**
info
### **Type**
regex
### **Pattern**
  - useQuery\s*\([^)]+\)(?![\s\S]{0,50}error)
### **Message**
Handle query errors in UI
### **Fix Action**
Destructure and handle error: const { error } = useQuery(...)
### **Applies To**
  - *.tsx
  - *.jsx

## Using refetch instead of cache update

### **Id**
refetch-instead-of-cache
### **Severity**
info
### **Type**
regex
### **Pattern**
  - refetchQueries:\s*\[
### **Message**
Consider cache update instead of refetch for better UX
### **Fix Action**
Use update function to modify cache directly
### **Applies To**
  - *.tsx
  - *.jsx
  - *.ts