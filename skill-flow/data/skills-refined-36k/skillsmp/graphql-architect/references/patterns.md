# GraphQL Architect

## Patterns


---
  #### **Name**
Domain-Driven Schema Design
  #### **Description**
Schema that models the domain, not the database
  #### **When**
Designing any GraphQL schema
  #### **Example**
    # BAD - Exposing database structure
    type User {
      id: ID!
      first_name: String  # Snake case from DB
      last_name: String
      created_at: String  # Raw timestamp
      orders: [Order!]!   # All orders, no pagination
    }
    
    # GOOD - Domain-focused schema
    type User {
      id: ID!
      displayName: String!  # Computed, camelCase
      email: Email!  # Custom scalar with validation
      memberSince: DateTime!  # Semantic naming
      recentOrders(first: Int = 10): OrderConnection!  # Paginated
      orderCount: Int!  # Common aggregate
    }
    
    # Connection pattern for pagination
    type OrderConnection {
      edges: [OrderEdge!]!
      pageInfo: PageInfo!
      totalCount: Int!
    }
    
    type OrderEdge {
      cursor: String!
      node: Order!
    }
    
    type PageInfo {
      hasNextPage: Boolean!
      hasPreviousPage: Boolean!
      startCursor: String
      endCursor: String
    }
    
    # Input types for mutations
    input CreateOrderInput {
      items: [OrderItemInput!]!
      shippingAddress: AddressInput!
      notes: String
    }
    
    type CreateOrderPayload {
      order: Order
      errors: [UserError!]!
    }
    
    type UserError {
      field: [String!]!
      message: String!
    }
    

---
  #### **Name**
DataLoader Pattern
  #### **Description**
Batching and caching to solve N+1
  #### **When**
Any GraphQL server implementation
  #### **Example**
    // Without DataLoader - N+1 queries
    // Query: { users { orders { product { name } } } }
    // Result: 1 query for users + N queries for orders + M queries for products
    
    // With DataLoader - batched queries
    import DataLoader from 'dataloader';
    
    function createLoaders(db: Database) {
      return {
        userById: new DataLoader<string, User>(async (ids) => {
          const users = await db.users.findByIds(ids);
          // Must return in same order as ids
          return ids.map(id => users.find(u => u.id === id) || null);
        }),
    
        ordersByUserId: new DataLoader<string, Order[]>(async (userIds) => {
          const orders = await db.orders.findByUserIds(userIds);
          // Group by user ID
          return userIds.map(userId =>
            orders.filter(o => o.userId === userId)
          );
        }),
    
        productById: new DataLoader<string, Product>(async (ids) => {
          const products = await db.products.findByIds(ids);
          return ids.map(id => products.find(p => p.id === id) || null);
        }),
      };
    }
    
    // In resolver context
    const server = new ApolloServer({
      schema,
      context: ({ req }) => ({
        loaders: createLoaders(db),  // New loaders per request
        user: getUser(req),
      }),
    });
    
    // Resolvers use loaders
    const resolvers = {
      User: {
        orders: (user, args, { loaders }) =>
          loaders.ordersByUserId.load(user.id),
      },
      Order: {
        product: (order, args, { loaders }) =>
          loaders.productById.load(order.productId),
      },
    };
    

---
  #### **Name**
Security and Performance Limits
  #### **Description**
Protecting against malicious queries
  #### **When**
Any production GraphQL API
  #### **Example**
    import depthLimit from 'graphql-depth-limit';
    import { createComplexityLimitRule } from 'graphql-validation-complexity';
    
    const server = new ApolloServer({
      schema,
      validationRules: [
        // Limit query depth
        depthLimit(10),
    
        // Limit query complexity
        createComplexityLimitRule(1000, {
          onCost: (cost) => console.log('Query cost:', cost),
          formatErrorMessage: (cost) =>
            `Query too complex: ${cost}. Max: 1000`,
        }),
      ],
      plugins: [
        // Query timeout
        {
          requestDidStart: () => ({
            willSendResponse: ({ response }) => {
              // Add execution time header
            },
          }),
        },
        // Disable introspection in production
        ApolloServerPluginLandingPageDisabled(),
      ],
    });
    
    // Rate limiting per client
    import { rateLimitDirective } from 'graphql-rate-limit-directive';
    
    const { rateLimitDirectiveTypeDefs, rateLimitDirectiveTransformer } =
      rateLimitDirective();
    
    // In schema
    type Query {
      users: [User!]! @rateLimit(limit: 100, duration: 60)
      expensiveQuery: Data! @rateLimit(limit: 10, duration: 60)
    }
    

---
  #### **Name**
Apollo Federation
  #### **Description**
Microservices with unified GraphQL API
  #### **When**
Multiple teams, independent services
  #### **Example**
    // Users subgraph
    import { buildSubgraphSchema } from '@apollo/subgraph';
    import gql from 'graphql-tag';
    
    const typeDefs = gql`
      extend schema @link(url: "https://specs.apollo.dev/federation/v2.0",
        import: ["@key", "@shareable"])
    
      type User @key(fields: "id") {
        id: ID!
        email: String!
        name: String!
      }
    
      type Query {
        me: User
        user(id: ID!): User
      }
    `;
    
    const resolvers = {
      User: {
        __resolveReference: (user, { loaders }) =>
          loaders.userById.load(user.id),
      },
      Query: {
        me: (_, __, { user }) => user,
        user: (_, { id }, { loaders }) => loaders.userById.load(id),
      },
    };
    
    // Orders subgraph - extends User
    const ordersTypeDefs = gql`
      extend schema @link(url: "https://specs.apollo.dev/federation/v2.0",
        import: ["@key", "@external"])
    
      type User @key(fields: "id") {
        id: ID! @external
        orders: [Order!]!
      }
    
      type Order @key(fields: "id") {
        id: ID!
        total: Money!
        status: OrderStatus!
      }
    `;
    
    // Router composes subgraphs
    // rover supergraph compose --config supergraph.yaml
    

## Anti-Patterns


---
  #### **Name**
Database as Schema
  #### **Description**
Directly exposing database tables as GraphQL types
  #### **Why**
Exposes implementation details, limits flexibility, security risk
  #### **Instead**
Design domain-focused schema, transform in resolvers

---
  #### **Name**
No DataLoader
  #### **Description**
Direct database queries in resolvers
  #### **Why**
N+1 queries crush performance at scale
  #### **Instead**
Use DataLoader for all entity fetching

---
  #### **Name**
Unbounded Lists
  #### **Description**
Returning arrays without pagination
  #### **Why**
Client can fetch millions of records, OOM, slow
  #### **Instead**
Use connection pattern with cursors, enforce limits

---
  #### **Name**
No Query Protection
  #### **Description**
No depth/complexity limits on queries
  #### **Why**
Malicious clients can craft expensive queries, DoS
  #### **Instead**
Depth limit, complexity analysis, query allowlisting

---
  #### **Name**
Resolver Business Logic
  #### **Description**
All logic in resolvers instead of services
  #### **Why**
Untestable, duplicated logic, tight coupling
  #### **Instead**
Thin resolvers calling domain services