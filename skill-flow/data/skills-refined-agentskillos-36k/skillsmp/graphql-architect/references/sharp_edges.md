# Graphql Architect - Sharp Edges

## N Plus One Queries

### **Id**
n-plus-one-queries
### **Summary**
Resolver per item causes N+1 database queries
### **Severity**
critical
### **Situation**
Nested queries in GraphQL
### **Why**
  Query: { users { orders { items } } }
  Without batching: 1 query for users, N queries for orders (one per user),
  M queries for items (one per order). 100 users = potentially 10,000+ queries.
  Database drowns, API times out.
  
### **Solution**
  1. ALWAYS use DataLoader:
     import DataLoader from 'dataloader';
  
     const ordersByUserId = new DataLoader(async (userIds) => {
       const orders = await db.orders.findMany({
         where: { userId: { in: userIds } }
       });
       return userIds.map(id =>
         orders.filter(o => o.userId === id)
       );
     });
  
     // Resolver
     User: {
       orders: (user, args, { loaders }) =>
         loaders.ordersByUserId.load(user.id)
     }
  
  2. Create new DataLoader per request:
     context: () => ({
       loaders: {
         ordersByUserId: new DataLoader(...),
         userById: new DataLoader(...),
       }
     })
  
  3. Batch correctly - return in same order as input IDs
  
  4. Monitor query counts in production
  
### **Symptoms**
  - Exponentially slow nested queries
  - Database connection exhaustion
  - Timeouts on deep queries
### **Detection Pattern**
Query:.*\{(?!.*DataLoader)|resolver.*findOne

## Denial Of Service Queries

### **Id**
denial-of-service-queries
### **Summary**
Malicious queries exhaust server resources
### **Severity**
critical
### **Situation**
Public GraphQL API
### **Why**
  Query: { user { friends { friends { friends { friends { ... } } } } } }
  Exponential expansion. Or: { users(first: 1000000) { ... } }
  No limits = trivial DoS. Attackers can craft queries that consume
  all CPU, memory, or database connections.
  
### **Solution**
  1. Depth limiting:
     import depthLimit from 'graphql-depth-limit';
  
     new ApolloServer({
       validationRules: [depthLimit(10)],
     });
  
  2. Complexity analysis:
     import { createComplexityLimitRule } from 'graphql-validation-complexity';
  
     validationRules: [
       createComplexityLimitRule(1000, {
         scalarCost: 1,
         objectCost: 10,
         listFactor: 10,
       }),
     ]
  
  3. Pagination limits:
     type Query {
       users(first: Int = 20): [User!]!
     }
  
     // Resolver enforces max
     const first = Math.min(args.first || 20, 100);
  
  4. Query timeout:
     const controller = new AbortController();
     setTimeout(() => controller.abort(), 30000);
  
  5. Rate limiting per client
  
### **Symptoms**
  - Server CPU/memory spikes
  - Timeouts for all users
  - Database connection exhaustion
### **Detection Pattern**
first:.*Int(?!.*max)|Query.*\{(?!.*depthLimit)

## Introspection In Production

### **Id**
introspection-in-production
### **Summary**
Introspection exposes entire schema to attackers
### **Severity**
high
### **Situation**
Production GraphQL endpoint
### **Why**
  Introspection query returns complete schema: all types, fields,
  arguments, descriptions. Attackers map your entire API surface,
  find hidden admin fields, sensitive data types. Information goldmine.
  
### **Solution**
  1. Disable introspection in production:
     new ApolloServer({
       introspection: process.env.NODE_ENV !== 'production',
     });
  
  2. Or use Apollo's plugin:
     import { ApolloServerPluginLandingPageDisabled } from '@apollo/server/plugin/disabled';
  
     plugins: [
       process.env.NODE_ENV === 'production'
         ? ApolloServerPluginLandingPageDisabled()
         : ApolloServerPluginLandingPageLocalDefault(),
     ]
  
  3. For legitimate schema consumers, use schema registry
  
  4. Consider persisted queries (allowlist only)
  
  5. Monitor for introspection attempts in logs
  
### **Symptoms**
  - Schema visible at /graphql
  - Documentation exposed to public
  - Security audit failure
### **Detection Pattern**
introspection.*true|ApolloServer\(\{(?!.*introspection.*false)

## Overfetching Exposure

### **Id**
overfetching-exposure
### **Summary**
Returning more data than requested exposes sensitive fields
### **Severity**
high
### **Situation**
Resolvers returning database objects directly
### **Why**
  Resolver: return await db.user.findUnique({ where: { id } });
  This returns ALL user fields including password_hash, internal_notes,
  ssn. GraphQL filters at response time, but data is still fetched,
  logged, and vulnerable to bugs that skip filtering.
  
### **Solution**
  1. Select only needed fields:
     const user = await db.user.findUnique({
       where: { id },
       select: { id: true, name: true, email: true }
     });
  
  2. Use field-level resolvers for sensitive data:
     User: {
       email: (user, args, { currentUser }) => {
         if (currentUser.id === user.id || currentUser.isAdmin) {
           return user.email;
         }
         return null;
       }
     }
  
  3. Create presentation layer:
     function toPublicUser(dbUser: DbUser): PublicUser {
       return {
         id: dbUser.id,
         name: dbUser.name,
         // Explicitly omit sensitive fields
       };
     }
  
  4. Use GraphQL Shield for field authorization:
     const permissions = shield({
       User: {
         email: isAuthenticated,
         adminNotes: isAdmin,
       }
     });
  
### **Symptoms**
  - Sensitive data in response
  - Data exposed in error messages
  - Logs contain sensitive information
### **Detection Pattern**
return.*findOne|return.*findUnique(?!.*select)

## Resolver Error Leakage

### **Id**
resolver-error-leakage
### **Summary**
Errors expose stack traces and internal details
### **Severity**
high
### **Situation**
Error handling in resolvers
### **Why**
  throw new Error('Database query failed: SELECT * FROM users WHERE...');
  This error goes to client. They see your SQL, table names, database
  structure. Stack traces reveal file paths, framework versions, internal logic.
  
### **Solution**
  1. Use custom error types:
     import { GraphQLError } from 'graphql';
  
     throw new GraphQLError('User not found', {
       extensions: {
         code: 'USER_NOT_FOUND',
         userMessage: 'The requested user does not exist',
       },
     });
  
  2. Format errors before sending:
     new ApolloServer({
       formatError: (error) => {
         // Log full error internally
         logger.error(error);
  
         // Return sanitized error to client
         if (error.extensions?.code === 'INTERNAL_SERVER_ERROR') {
           return { message: 'Internal server error' };
         }
         return error;
       },
     });
  
  3. Never include original error in response:
     // BAD
     throw new Error(`DB error: ${dbError.message}`);
  
     // GOOD
     logger.error('DB error', dbError);
     throw new GraphQLError('Service unavailable');
  
  4. Use error codes, not messages for client logic
  
### **Symptoms**
  - Stack traces in API responses
  - SQL queries visible in errors
  - Internal paths exposed
### **Detection Pattern**
throw new Error.*\$\{|throw.*error\.message

## Subscription Resource Exhaustion

### **Id**
subscription-resource-exhaustion
### **Summary**
GraphQL subscriptions consume server resources per connection
### **Severity**
high
### **Situation**
Real-time features with subscriptions
### **Why**
  Each subscription is a persistent WebSocket connection. 10,000 users
  with 3 subscriptions each = 30,000 open connections. Each holds memory,
  needs heartbeats, consumes file descriptors. Subscriptions don't scale
  like request/response.
  
### **Solution**
  1. Limit subscriptions per client:
     const connectionCount = new Map<string, number>();
  
     onConnect: (params, socket) => {
       const clientId = getClientId(socket);
       const count = connectionCount.get(clientId) || 0;
       if (count >= 5) {
         throw new Error('Too many subscriptions');
       }
       connectionCount.set(clientId, count + 1);
     }
  
  2. Use connection timeouts:
     subscriptions: {
       keepAlive: 30000,  // 30 second heartbeat
       onConnect: (params) => {
         setTimeout(() => socket.close(), 3600000);  // 1 hour max
       }
     }
  
  3. Consider polling for low-frequency updates:
     // Instead of subscription for data that changes hourly
     useQuery(GET_DATA, { pollInterval: 60000 });
  
  4. Use pub/sub with Redis for horizontal scaling:
     import { RedisPubSub } from 'graphql-redis-subscriptions';
  
  5. Monitor active connections, set alerts
  
### **Symptoms**
  - Server runs out of memory
  - File descriptor exhaustion
  - WebSocket connection failures
### **Detection Pattern**
Subscription:.*\{(?!.*limit)|pubsub\.asyncIterator

## Batching Attack

### **Id**
batching-attack
### **Summary**
Query batching allows amplified attacks
### **Severity**
medium
### **Situation**
GraphQL endpoint accepting batched queries
### **Why**
  [{ query: "{ user(id: 1) }" }, { query: "{ user(id: 2) }" }, ...]
  Batch of 1000 queries in one HTTP request. Bypasses rate limiting
  that counts requests. Single request triggers 1000 resolver executions.
  
### **Solution**
  1. Limit batch size:
     new ApolloServer({
       allowBatchedHttpRequests: true,
       maxBatchSize: 10,  // Max 10 queries per batch
     });
  
  2. Count operations, not requests:
     // Rate limit by operation count
     function rateLimitMiddleware(req, res, next) {
       const operationCount = Array.isArray(req.body)
         ? req.body.length
         : 1;
       if (!rateLimit.check(req.ip, operationCount)) {
         return res.status(429).send('Rate limited');
       }
       next();
     }
  
  3. Consider disabling batching if not needed:
     allowBatchedHttpRequests: false
  
  4. Apply complexity limits per batch, not per query:
     // Total complexity of all queries in batch
     const totalComplexity = queries.reduce(
       (sum, q) => sum + getComplexity(q),
       0
     );
  
### **Symptoms**
  - Rate limits bypassed
  - Spiky resource usage
  - Single requests causing high load
### **Detection Pattern**
allowBatchedHttpRequests.*true(?!.*maxBatchSize)

## Enum Mismatch

### **Id**
enum-mismatch
### **Summary**
Schema enum and code enum out of sync
### **Severity**
medium
### **Situation**
Using enums in GraphQL schema
### **Why**
  Schema: enum Status { PENDING, ACTIVE, COMPLETED }
  Code: enum Status { Pending = 'pending', Active = 'active' }
  Values don't match. Resolvers return 'pending', schema expects 'PENDING'.
  Client gets null or error. Hard to debug because types look correct.
  
### **Solution**
  1. Generate types from schema (single source of truth):
     npx graphql-codegen --config codegen.yml
  
     // codegen.yml
     generates:
       ./src/types.ts:
         plugins:
           - typescript
           - typescript-resolvers
  
  2. Use consistent naming:
     // Schema
     enum OrderStatus {
       PENDING
       PROCESSING
       SHIPPED
     }
  
     // Resolver - use same values
     return order.status.toUpperCase();
  
  3. Or use custom scalar for mapping:
     const OrderStatusType = new GraphQLEnumType({
       name: 'OrderStatus',
       values: {
         PENDING: { value: 'pending' },
         PROCESSING: { value: 'processing' },
       }
     });
  
  4. Add tests that verify enum alignment
  
### **Symptoms**
  - Fields return null unexpectedly
  - "Enum value not found" errors
  - Type mismatches in responses
### **Detection Pattern**
enum.*\{(?!.*values)|resolver.*return.*\.toLowerCase