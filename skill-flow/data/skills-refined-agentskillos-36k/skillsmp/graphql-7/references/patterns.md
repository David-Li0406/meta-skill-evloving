# GraphQL

## Patterns


---
  #### **Name**
Schema Design
  #### **Description**
Type-safe schema with proper nullability
  #### **When**
Designing any GraphQL API
  #### **Example**
    # SCHEMA DESIGN:
    
    """
    The schema is your API contract. Design nullability
    intentionally - non-null fields must always resolve.
    """
    
    type Query {
      # Non-null - will always return user or throw
      user(id: ID!): User!
    
      # Nullable - returns null if not found
      userByEmail(email: String!): User
    
      # Non-null list with non-null items
      users(limit: Int = 10, offset: Int = 0): [User!]!
    
      # Search with pagination
      searchUsers(
        query: String!
        first: Int
        after: String
      ): UserConnection!
    }
    
    type Mutation {
      # Input types for complex mutations
      createUser(input: CreateUserInput!): CreateUserPayload!
      updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
      deleteUser(id: ID!): DeleteUserPayload!
    }
    
    type Subscription {
      userCreated: User!
      messageReceived(roomId: ID!): Message!
    }
    
    # Input types
    input CreateUserInput {
      email: String!
      name: String!
      role: Role = USER
    }
    
    input UpdateUserInput {
      email: String
      name: String
      role: Role
    }
    
    # Payload types (for errors as data)
    type CreateUserPayload {
      user: User
      errors: [Error!]!
    }
    
    union UpdateUserPayload = UpdateUserSuccess | NotFoundError | ValidationError
    
    type UpdateUserSuccess {
      user: User!
    }
    
    # Enums
    enum Role {
      USER
      ADMIN
      MODERATOR
    }
    
    # Types with relationships
    type User {
      id: ID!
      email: String!
      name: String!
      role: Role!
      posts(limit: Int = 10): [Post!]!
      createdAt: DateTime!
    }
    
    type Post {
      id: ID!
      title: String!
      content: String!
      author: User!
      comments: [Comment!]!
      published: Boolean!
    }
    
    # Pagination (Relay-style)
    type UserConnection {
      edges: [UserEdge!]!
      pageInfo: PageInfo!
      totalCount: Int!
    }
    
    type UserEdge {
      node: User!
      cursor: String!
    }
    
    type PageInfo {
      hasNextPage: Boolean!
      hasPreviousPage: Boolean!
      startCursor: String
      endCursor: String
    }
    

---
  #### **Name**
DataLoader for N+1 Prevention
  #### **Description**
Batch and cache database queries
  #### **When**
Resolving relationships
  #### **Example**
    # DATALOADER:
    
    """
    Without DataLoader, fetching 10 posts with authors
    makes 11 queries (1 for posts + 10 for each author).
    DataLoader batches into 2 queries.
    """
    
    import DataLoader from 'dataloader';
    
    // Create loaders per request
    function createLoaders(db) {
      return {
        userLoader: new DataLoader(async (ids) => {
          // Single query for all users
          const users = await db.user.findMany({
            where: { id: { in: ids } }
          });
    
          // Return in same order as ids
          const userMap = new Map(users.map(u => [u.id, u]));
          return ids.map(id => userMap.get(id) || null);
        }),
    
        postsByAuthorLoader: new DataLoader(async (authorIds) => {
          const posts = await db.post.findMany({
            where: { authorId: { in: authorIds } }
          });
    
          // Group by author
          const postsByAuthor = new Map();
          posts.forEach(post => {
            const existing = postsByAuthor.get(post.authorId) || [];
            postsByAuthor.set(post.authorId, [...existing, post]);
          });
    
          return authorIds.map(id => postsByAuthor.get(id) || []);
        })
      };
    }
    
    // Attach to context
    const server = new ApolloServer({
      typeDefs,
      resolvers,
    });
    
    app.use('/graphql', expressMiddleware(server, {
      context: async ({ req }) => ({
        db,
        loaders: createLoaders(db),
        user: req.user
      })
    }));
    
    // Use in resolvers
    const resolvers = {
      Post: {
        author: (post, _, { loaders }) => {
          return loaders.userLoader.load(post.authorId);
        }
      },
      User: {
        posts: (user, _, { loaders }) => {
          return loaders.postsByAuthorLoader.load(user.id);
        }
      }
    };
    

---
  #### **Name**
Apollo Client Caching
  #### **Description**
Normalized cache with type policies
  #### **When**
Client-side data management
  #### **Example**
    # APOLLO CLIENT CACHING:
    
    """
    Apollo Client normalizes responses into a flat cache.
    Configure type policies for custom cache behavior.
    """
    
    import { ApolloClient, InMemoryCache } from '@apollo/client';
    
    const cache = new InMemoryCache({
      typePolicies: {
        Query: {
          fields: {
            // Paginated field
            users: {
              keyArgs: ['query'],  // Cache separately per query
              merge(existing = { edges: [] }, incoming, { args }) {
                // Append for infinite scroll
                if (args?.after) {
                  return {
                    ...incoming,
                    edges: [...existing.edges, ...incoming.edges]
                  };
                }
                return incoming;
              }
            }
          }
        },
        User: {
          keyFields: ['id'],  // How to identify users
          fields: {
            fullName: {
              read(_, { readField }) {
                // Computed field
                return `${readField('firstName')} ${readField('lastName')}`;
              }
            }
          }
        }
      }
    });
    
    const client = new ApolloClient({
      uri: '/graphql',
      cache,
      defaultOptions: {
        watchQuery: {
          fetchPolicy: 'cache-and-network'
        }
      }
    });
    
    // Queries with hooks
    import { useQuery, useMutation } from '@apollo/client';
    
    const GET_USER = gql`
      query GetUser($id: ID!) {
        user(id: $id) {
          id
          name
          email
        }
      }
    `;
    
    function UserProfile({ userId }) {
      const { data, loading, error } = useQuery(GET_USER, {
        variables: { id: userId }
      });
    
      if (loading) return <Spinner />;
      if (error) return <Error message={error.message} />;
    
      return <div>{data.user.name}</div>;
    }
    
    // Mutations with cache updates
    const CREATE_USER = gql`
      mutation CreateUser($input: CreateUserInput!) {
        createUser(input: $input) {
          user {
            id
            name
            email
          }
          errors {
            field
            message
          }
        }
      }
    `;
    
    function CreateUserForm() {
      const [createUser, { loading }] = useMutation(CREATE_USER, {
        update(cache, { data: { createUser } }) {
          // Update cache after mutation
          if (createUser.user) {
            cache.modify({
              fields: {
                users(existing = []) {
                  const newRef = cache.writeFragment({
                    data: createUser.user,
                    fragment: gql`
                      fragment NewUser on User {
                        id
                        name
                        email
                      }
                    `
                  });
                  return [...existing, newRef];
                }
              }
            });
          }
        }
      });
    }
    

---
  #### **Name**
Code Generation
  #### **Description**
Type-safe operations from schema
  #### **When**
TypeScript projects
  #### **Example**
    # GRAPHQL CODEGEN:
    
    """
    Generate TypeScript types from your schema and operations.
    No more manually typing query responses.
    """
    
    # Install
    npm install -D @graphql-codegen/cli
    npm install -D @graphql-codegen/typescript
    npm install -D @graphql-codegen/typescript-operations
    npm install -D @graphql-codegen/typescript-react-apollo
    
    # codegen.ts
    import type { CodegenConfig } from '@graphql-codegen/cli';
    
    const config: CodegenConfig = {
      schema: 'http://localhost:4000/graphql',
      documents: ['src/**/*.graphql', 'src/**/*.tsx'],
      generates: {
        './src/generated/graphql.ts': {
          plugins: [
            'typescript',
            'typescript-operations',
            'typescript-react-apollo'
          ],
          config: {
            withHooks: true,
            withComponent: false
          }
        }
      }
    };
    
    export default config;
    
    # Run generation
    npx graphql-codegen
    
    # Usage - fully typed!
    import { useGetUserQuery, useCreateUserMutation } from './generated/graphql';
    
    function UserProfile({ userId }: { userId: string }) {
      const { data, loading } = useGetUserQuery({
        variables: { id: userId }  // Type-checked!
      });
    
      // data.user is fully typed
      return <div>{data?.user?.name}</div>;
    }
    

---
  #### **Name**
Error Handling with Unions
  #### **Description**
Expected errors as data, not exceptions
  #### **When**
Operations that can fail in expected ways
  #### **Example**
    # ERRORS AS DATA:
    
    """
    Use union types for expected failure cases.
    GraphQL errors are for unexpected failures.
    """
    
    # Schema
    type Mutation {
      login(email: String!, password: String!): LoginResult!
    }
    
    union LoginResult = LoginSuccess | InvalidCredentials | AccountLocked
    
    type LoginSuccess {
      user: User!
      token: String!
    }
    
    type InvalidCredentials {
      message: String!
    }
    
    type AccountLocked {
      message: String!
      unlockAt: DateTime
    }
    
    # Resolver
    const resolvers = {
      Mutation: {
        login: async (_, { email, password }, { db }) => {
          const user = await db.user.findByEmail(email);
    
          if (!user || !await verifyPassword(password, user.hash)) {
            return {
              __typename: 'InvalidCredentials',
              message: 'Invalid email or password'
            };
          }
    
          if (user.lockedUntil && user.lockedUntil > new Date()) {
            return {
              __typename: 'AccountLocked',
              message: 'Account temporarily locked',
              unlockAt: user.lockedUntil
            };
          }
    
          return {
            __typename: 'LoginSuccess',
            user,
            token: generateToken(user)
          };
        }
      },
    
      LoginResult: {
        __resolveType(obj) {
          return obj.__typename;
        }
      }
    };
    
    # Client query
    const LOGIN = gql`
      mutation Login($email: String!, $password: String!) {
        login(email: $email, password: $password) {
          ... on LoginSuccess {
            user { id name }
            token
          }
          ... on InvalidCredentials {
            message
          }
          ... on AccountLocked {
            message
            unlockAt
          }
        }
      }
    `;
    
    // Handle all cases
    const result = data.login;
    switch (result.__typename) {
      case 'LoginSuccess':
        setToken(result.token);
        redirect('/dashboard');
        break;
      case 'InvalidCredentials':
        setError(result.message);
        break;
      case 'AccountLocked':
        setError(`${result.message}. Try again at ${result.unlockAt}`);
        break;
    }
    

## Anti-Patterns


---
  #### **Name**
No DataLoader
  #### **Description**
Fetching related data without batching
  #### **Why**
    Each resolver runs independently. Fetching a user for each post
    in a list makes N separate database queries. With 100 posts,
    that's 100 queries instead of 1.
    
  #### **Instead**
    // WRONG: N+1 queries
    Post: {
      author: async (post, _, { db }) => {
        return db.user.findUnique({ where: { id: post.authorId } });
      }
    }
    
    // RIGHT: Batched with DataLoader
    Post: {
      author: (post, _, { loaders }) => {
        return loaders.userLoader.load(post.authorId);
      }
    }
    

---
  #### **Name**
No Query Depth Limiting
  #### **Description**
Allowing infinitely nested queries
  #### **Why**
    Clients can craft queries like user.posts.author.posts.author...
    going 20 levels deep. Each level multiplies the work. A malicious
    or buggy client can bring down your server.
    
  #### **Instead**
    import depthLimit from 'graphql-depth-limit';
    import { createComplexityLimitRule } from 'graphql-validation-complexity';
    
    const server = new ApolloServer({
      typeDefs,
      resolvers,
      validationRules: [
        depthLimit(10),  // Max 10 levels deep
        createComplexityLimitRule(1000)  // Max complexity score
      ]
    });
    

---
  #### **Name**
Authorization in Schema
  #### **Description**
Using directives for all authorization
  #### **Why**
    Schema directives are visible to all clients via introspection.
    Complex authorization logic doesn't fit in directives. Business
    rules change faster than schema.
    
  #### **Instead**
    // WRONG: Only directive-based
    type Mutation {
      deleteUser(id: ID!): User @auth(requires: ADMIN)
    }
    
    // RIGHT: Resolver-level authorization
    Mutation: {
      deleteUser: async (_, { id }, { user, db }) => {
        // Check authorization
        if (!user) throw new AuthenticationError('Not logged in');
        if (user.role !== 'ADMIN' && user.id !== id) {
          throw new ForbiddenError('Not authorized');
        }
    
        return db.user.delete({ where: { id } });
      }
    }
    

---
  #### **Name**
Giant Mutations
  #### **Description**
Single mutation for all updates
  #### **Why**
    A generic updateUser(id, data: JSON) mutation has no type safety,
    no validation, no clear intent. Clients can send anything.
    
  #### **Instead**
    // WRONG: Generic mutation
    type Mutation {
      updateUser(id: ID!, data: JSON!): User
    }
    
    // RIGHT: Specific mutations
    type Mutation {
      updateUserProfile(id: ID!, input: UpdateProfileInput!): UpdateProfilePayload!
      updateUserEmail(id: ID!, email: String!): UpdateEmailPayload!
      updateUserPassword(id: ID!, input: UpdatePasswordInput!): UpdatePasswordPayload!
      promoteToAdmin(userId: ID!): PromotePayload!
    }
    

---
  #### **Name**
Over-fetching in Schema
  #### **Description**
Always returning all fields
  #### **Why**
    If User always includes posts, comments, followers... every query
    fetches everything even when not needed. The benefit of GraphQL
    is fetching only what you need - design the schema to enable this.
    
  #### **Instead**
    // Let clients choose
    type User {
      id: ID!
      name: String!
      email: String!
      # These are optional - clients request if needed
      posts(limit: Int = 10): [Post!]!
      followers(limit: Int = 10): [User!]!
    }
    
    // Query only what's needed
    query {
      user(id: "1") {
        name  # Only fetches name, not posts/followers
      }
    }
    