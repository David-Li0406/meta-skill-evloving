# Graphql Architect - Validations

## Resolver Without DataLoader

### **Id**
no-dataloader
### **Severity**
error
### **Type**
regex
### **Pattern**
  - resolver.*findOne
  - resolver.*findUnique
  - Query:.*\{(?!.*loaders)
### **Message**
Resolver without DataLoader causes N+1 queries.
### **Fix Action**
Use DataLoader for all entity fetching
### **Applies To**
  - **/resolvers/**/*.ts
  - **/schema/**/*.ts

## Unbounded List Return

### **Id**
unbounded-list
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \[.*\!?\](?!.*Connection)
  - findMany\(\)(?!.*take)
### **Message**
Unbounded list can return millions of records.
### **Fix Action**
Use pagination with Connection pattern
### **Applies To**
  - **/*.graphql
  - **/schema/**/*.ts

## No Query Depth Limit

### **Id**
no-depth-limit
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ApolloServer\(\{(?!.*depthLimit)
  - new GraphQLServer(?!.*validationRules)
### **Message**
No depth limit allows DoS attacks.
### **Fix Action**
Add depthLimit validation rule
### **Applies To**
  - **/server.ts
  - **/index.ts
  - **/apollo.ts

## Introspection Enabled in Production

### **Id**
introspection-production
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - introspection.*true
  - ApolloServer\(\{(?!.*introspection.*false)
### **Message**
Introspection exposes schema to attackers.
### **Fix Action**
Disable introspection in production
### **Applies To**
  - **/server.ts
  - **/apollo.ts

## Error Message Leaking Details

### **Id**
error-leak
### **Severity**
error
### **Type**
regex
### **Pattern**
  - throw new Error.*\$\{
  - throw.*error\.message
  - throw.*err\.stack
### **Message**
Error may expose internal details to clients.
### **Fix Action**
Use GraphQLError with sanitized message
### **Applies To**
  - **/resolvers/**/*.ts

## No Query Complexity Limit

### **Id**
no-complexity-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ApolloServer\(\{(?!.*complexity)
### **Message**
No complexity limit allows expensive queries.
### **Fix Action**
Add complexity analysis validation
### **Applies To**
  - **/server.ts
  - **/apollo.ts

## Direct Database Return

### **Id**
direct-db-return
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - return.*findUnique\(
  - return.*findOne\(
  - return.*findFirst\(
### **Message**
Returning DB object directly may expose sensitive fields.
### **Fix Action**
Select specific fields or use transformation
### **Applies To**
  - **/resolvers/**/*.ts

## No Rate Limiting

### **Id**
no-rate-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Query:.*\{(?!.*@rateLimit)
### **Message**
No rate limiting allows API abuse.
### **Fix Action**
Add rate limiting directive or middleware
### **Applies To**
  - **/*.graphql

## Subscription Without Connection Limit

### **Id**
subscription-no-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Subscription:.*\{(?!.*limit)
  - pubsub\.asyncIterator
### **Message**
Unlimited subscriptions exhaust resources.
### **Fix Action**
Limit subscriptions per client
### **Applies To**
  - **/resolvers/**/*.ts

## N+1 Query Pattern

### **Id**
n-plus-one-pattern
### **Severity**
error
### **Type**
regex
### **Pattern**
  - parent\s*=>\s*.*find
  - \(parent\).*prisma\.
### **Message**
Pattern suggests N+1 query problem.
### **Fix Action**
Use DataLoader to batch fetches
### **Applies To**
  - **/resolvers/**/*.ts

## Mutation Without Input Validation

### **Id**
mutation-no-validation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Mutation:.*args\.
### **Message**
Mutation should validate input before processing.
### **Fix Action**
Add input validation with zod or similar
### **Applies To**
  - **/resolvers/**/*.ts

## Schema Matches Database Names

### **Id**
schema-db-mismatch
### **Severity**
info
### **Type**
regex
### **Pattern**
  - _id:
  - created_at:
  - updated_at:
### **Message**
Schema uses database naming (snake_case).
### **Fix Action**
Use camelCase in GraphQL schema
### **Applies To**
  - **/*.graphql