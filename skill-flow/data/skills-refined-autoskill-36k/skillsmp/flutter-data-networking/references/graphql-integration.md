# GraphQL Integration

Complete guide to integrating GraphQL in Flutter applications using graphql_flutter.

## Overview

GraphQL is a query language for APIs that allows clients to request exactly the data they need, nothing more and nothing less. Unlike REST, which requires multiple endpoints for different resources, GraphQL exposes a single endpoint and uses a type system to define available operations.

The `graphql_flutter` package brings full GraphQL functionality to Flutter, including queries, mutations, subscriptions, caching, and optimistic updates. This reference covers everything needed to build production-ready GraphQL integrations.

## GraphQL vs REST

### Advantages of GraphQL

**No Over-fetching**: Request only the fields you need. A REST endpoint might return 50 fields when you only need 3.

**No Under-fetching**: Get multiple related resources in a single request. REST often requires multiple round trips.

**Strong Typing**: The GraphQL schema provides compile-time type safety and excellent IDE support.

**Single Endpoint**: All operations go through one endpoint, simplifying API management.

**Real-time Updates**: Subscriptions provide WebSocket-based real-time updates built into the spec.

**Versioning**: Add new fields and types without breaking existing clients. No need for /v1, /v2 endpoints.

### When to Use GraphQL

Use GraphQL when:
- Your app needs flexible data fetching across many screens
- Mobile bandwidth is a concern (over-fetching waste)
- You need real-time updates
- The backend team controls the schema
- You're building a complex application with interconnected data

Stick with REST when:
- Your API is simple with few resources
- You need file uploads/downloads (GraphQL can do this but it's cumbersome)
- You're integrating with third-party APIs (most use REST)
- Your team is unfamiliar with GraphQL

## Installation

Add graphql_flutter to your `pubspec.yaml`:

```yaml
dependencies:
  graphql_flutter: ^5.1.0
```

The package includes everything needed: GraphQL client, cache, and Flutter widgets.

## Client Setup

### Basic Configuration

Create and configure a GraphQL client:

```dart
import 'package:graphql_flutter/graphql_flutter.dart';

class GraphQLConfig {
  static GraphQLClient createClient({
    required String endpoint,
    String? token,
  }) {
    final httpLink = HttpLink(endpoint);

    // Add authentication
    final authLink = AuthLink(
      getToken: () async => token != null ? 'Bearer $token' : null,
    );

    // Combine links
    final link = authLink.concat(httpLink);

    return GraphQLClient(
      link: link,
      cache: GraphQLCache(store: InMemoryStore()),
    );
  }

  static ValueNotifier<GraphQLClient> createClientNotifier({
    required String endpoint,
    String? token,
  }) {
    return ValueNotifier(
      createClient(endpoint: endpoint, token: token),
    );
  }
}
```

### Advanced Configuration

Configure cache policies, error handling, and more:

```dart
class GraphQLConfig {
  static GraphQLClient createAdvancedClient({
    required String endpoint,
    String? token,
  }) {
    // HTTP Link with custom headers
    final httpLink = HttpLink(
      endpoint,
      defaultHeaders: {
        'X-API-Version': '2',
      },
    );

    // Authentication Link
    final authLink = AuthLink(
      getToken: () async {
        final token = await SecureStorage().getToken();
        return token != null ? 'Bearer $token' : null;
      },
    );

    // Error Link for custom error handling
    final errorLink = ErrorLink(
      onException: (Request request, NextLink forward, Response response) {
        if (response.errors != null) {
          for (final error in response.errors!) {
            if (error.extensions?['code'] == 'UNAUTHENTICATED') {
              // Handle authentication error
              print('Authentication required');
            }
          }
        }
        return forward(request);
      },
    );

    // Combine links
    final link = Link.from([
      errorLink,
      authLink,
      httpLink,
    ]);

    // Configure cache
    final store = InMemoryStore();

    return GraphQLClient(
      link: link,
      cache: GraphQLCache(
        store: store,
        // Configure cache policies
        typePolicies: {
          'User': TypePolicy(
            // Cache users by ID
            keyFields: {'id': true},
          ),
        },
      ),
      defaultPolicies: DefaultPolicies(
        query: Policies(
          fetch: FetchPolicy.cacheFirst,
          error: ErrorPolicy.all,
        ),
        mutate: Policies(
          fetch: FetchPolicy.networkOnly,
          error: ErrorPolicy.all,
        ),
      ),
    );
  }
}
```

### GraphQLProvider

Wrap your app with GraphQLProvider to make the client available:

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize persistent cache (optional)
  await initHiveForFlutter();

  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GraphQLProvider(
      client: GraphQLConfig.createClientNotifier(
        endpoint: 'https://api.example.com/graphql',
      ),
      child: MaterialApp(
        title: 'GraphQL App',
        home: HomeScreen(),
      ),
    );
  }
}
```

## Queries

### Basic Query

Fetch data with the Query widget:

```dart
class UserProfile extends StatelessWidget {
  final String userId;

  const UserProfile({required this.userId});

  @override
  Widget build(BuildContext context) {
    return Query(
      options: QueryOptions(
        document: gql('''
          query GetUser(\$id: ID!) {
            user(id: \$id) {
              id
              name
              email
              avatarUrl
              bio
            }
          }
        '''),
        variables: {'id': userId},
      ),
      builder: (result, {fetchMore, refetch}) {
        if (result.isLoading) {
          return Center(child: CircularProgressIndicator());
        }

        if (result.hasException) {
          return Center(
            child: Text('Error: ${result.exception.toString()}'),
          );
        }

        final user = result.data?['user'];
        if (user == null) {
          return Center(child: Text('User not found'));
        }

        return Column(
          children: [
            CircleAvatar(
              backgroundImage: NetworkImage(user['avatarUrl']),
              radius: 50,
            ),
            SizedBox(height: 16),
            Text(
              user['name'],
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            Text(user['email']),
            if (user['bio'] != null)
              Padding(
                padding: EdgeInsets.all(16),
                child: Text(user['bio']),
              ),
          ],
        );
      },
    );
  }
}
```

### Query with Pagination

Implement cursor-based pagination:

```dart
class UserList extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Query(
      options: QueryOptions(
        document: gql('''
          query GetUsers(\$first: Int!, \$after: String) {
            users(first: \$first, after: \$after) {
              edges {
                node {
                  id
                  name
                  email
                }
                cursor
              }
              pageInfo {
                hasNextPage
                endCursor
              }
            }
          }
        '''),
        variables: {
          'first': 20,
        },
      ),
      builder: (result, {fetchMore, refetch}) {
        if (result.isLoading && result.data == null) {
          return Center(child: CircularProgressIndicator());
        }

        if (result.hasException) {
          return Center(child: Text('Error: ${result.exception}'));
        }

        final users = result.data?['users'];
        final edges = users['edges'] as List;
        final pageInfo = users['pageInfo'];

        return ListView.builder(
          itemCount: edges.length + (pageInfo['hasNextPage'] ? 1 : 0),
          itemBuilder: (context, index) {
            // Load more indicator
            if (index == edges.length) {
              return Padding(
                padding: EdgeInsets.all(16),
                child: Center(
                  child: ElevatedButton(
                    onPressed: () {
                      fetchMore!(
                        FetchMoreOptions(
                          variables: {
                            'after': pageInfo['endCursor'],
                          },
                          updateQuery: (previousResult, fetchMoreResult) {
                            final prevEdges =
                                previousResult?['users']['edges'] as List;
                            final newEdges =
                                fetchMoreResult?['users']['edges'] as List;

                            return {
                              'users': {
                                'edges': [...prevEdges, ...newEdges],
                                'pageInfo': fetchMoreResult?['users']
                                    ['pageInfo'],
                              }
                            };
                          },
                        ),
                      );
                    },
                    child: Text('Load More'),
                  ),
                ),
              );
            }

            final user = edges[index]['node'];
            return ListTile(
              title: Text(user['name']),
              subtitle: Text(user['email']),
            );
          },
        );
      },
    );
  }
}
```

### Fetch Policies

Control caching behavior with fetch policies:

```dart
// Cache-first (default): Return cached data if available, otherwise network
Query(
  options: QueryOptions(
    document: gql(query),
    fetchPolicy: FetchPolicy.cacheFirst,
  ),
  builder: (result, {fetchMore, refetch}) {
    // ...
  },
)

// Network-only: Always fetch from network, update cache
Query(
  options: QueryOptions(
    document: gql(query),
    fetchPolicy: FetchPolicy.networkOnly,
  ),
  builder: (result, {fetchMore, refetch}) {
    // ...
  },
)

// Cache-only: Never fetch from network, return cached data or null
Query(
  options: QueryOptions(
    document: gql(query),
    fetchPolicy: FetchPolicy.cacheOnly,
  ),
  builder: (result, {fetchMore, refetch}) {
    // ...
  },
)

// No-cache: Fetch from network, don't update cache
Query(
  options: QueryOptions(
    document: gql(query),
    fetchPolicy: FetchPolicy.noCache,
  ),
  builder: (result, {fetchMore, refetch}) {
    // ...
  },
)

// Cache-and-network: Return cached data immediately, then fetch from network
Query(
  options: QueryOptions(
    document: gql(query),
    fetchPolicy: FetchPolicy.cacheAndNetwork,
  ),
  builder: (result, {fetchMore, refetch}) {
    // Widget rebuilds twice: once with cache, once with network data
  },
)
```

### Programmatic Queries

Execute queries outside of widgets:

```dart
class UserRepository {
  final GraphQLClient _client;

  UserRepository(this._client);

  Future<User?> getUser(String id) async {
    final result = await _client.query(
      QueryOptions(
        document: gql('''
          query GetUser(\$id: ID!) {
            user(id: \$id) {
              id
              name
              email
            }
          }
        '''),
        variables: {'id': id},
      ),
    );

    if (result.hasException) {
      throw result.exception!;
    }

    final userData = result.data?['user'];
    if (userData == null) return null;

    return User.fromJson(userData);
  }

  Stream<List<User>> watchUsers() {
    return _client.watchQuery(
      WatchQueryOptions(
        document: gql('''
          query GetUsers {
            users {
              id
              name
              email
            }
          }
        '''),
        pollInterval: Duration(seconds: 10), // Poll every 10 seconds
      ),
    ).stream.map((result) {
      if (result.hasException || result.data == null) {
        return <User>[];
      }

      return (result.data!['users'] as List)
          .map((json) => User.fromJson(json))
          .toList();
    });
  }
}
```

## Mutations

### Basic Mutation

Modify data with the Mutation widget:

```dart
class CreateUserForm extends StatefulWidget {
  @override
  _CreateUserFormState createState() => _CreateUserFormState();
}

class _CreateUserFormState extends State<CreateUserForm> {
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Mutation(
      options: MutationOptions(
        document: gql('''
          mutation CreateUser(\$name: String!, \$email: String!) {
            createUser(input: {name: \$name, email: \$email}) {
              user {
                id
                name
                email
              }
            }
          }
        '''),
        onCompleted: (data) {
          final user = data?['createUser']['user'];
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('User ${user['name']} created!')),
          );
          Navigator.pop(context);
        },
        onError: (error) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error: $error')),
          );
        },
      ),
      builder: (runMutation, result) {
        return Column(
          children: [
            TextField(
              controller: _nameController,
              decoration: InputDecoration(labelText: 'Name'),
            ),
            TextField(
              controller: _emailController,
              decoration: InputDecoration(labelText: 'Email'),
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: result.isLoading
                  ? null
                  : () {
                      runMutation({
                        'name': _nameController.text,
                        'email': _emailController.text,
                      });
                    },
              child: result.isLoading
                  ? CircularProgressIndicator()
                  : Text('Create User'),
            ),
          ],
        );
      },
    );
  }

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    super.dispose();
  }
}
```

### Optimistic Updates

Update UI immediately before server response:

```dart
Mutation(
  options: MutationOptions(
    document: gql('''
      mutation LikePost(\$postId: ID!) {
        likePost(postId: \$postId) {
          post {
            id
            likes
            isLiked
          }
        }
      }
    '''),
    optimisticResult: (vars) {
      return {
        'likePost': {
          'post': {
            '__typename': 'Post',
            'id': vars['postId'],
            'likes': 0, // Will be updated from server
            'isLiked': true,
          }
        }
      };
    },
    update: (cache, result) {
      if (result.hasException || result.data == null) return;

      final postId = result.data!['likePost']['post']['id'];

      // Update cache manually if needed
      cache.writeFragment(
        Fragment(
          document: gql('''
            fragment PostLike on Post {
              id
              likes
              isLiked
            }
          '''),
        ).asRequest(idFields: {'id': postId}),
        data: result.data!['likePost']['post'],
      );
    },
  ),
  builder: (runMutation, result) {
    return IconButton(
      icon: Icon(
        result.data?['likePost']['post']['isLiked'] == true
            ? Icons.favorite
            : Icons.favorite_border,
      ),
      onPressed: () {
        runMutation({'postId': widget.postId});
      },
    );
  },
)
```

### Programmatic Mutations

Execute mutations outside of widgets:

```dart
class UserRepository {
  final GraphQLClient _client;

  UserRepository(this._client);

  Future<User> createUser({
    required String name,
    required String email,
  }) async {
    final result = await _client.mutate(
      MutationOptions(
        document: gql('''
          mutation CreateUser(\$name: String!, \$email: String!) {
            createUser(input: {name: \$name, email: \$email}) {
              user {
                id
                name
                email
              }
            }
          }
        '''),
        variables: {
          'name': name,
          'email': email,
        },
      ),
    );

    if (result.hasException) {
      throw result.exception!;
    }

    final userData = result.data!['createUser']['user'];
    return User.fromJson(userData);
  }

  Future<void> deleteUser(String id) async {
    final result = await _client.mutate(
      MutationOptions(
        document: gql('''
          mutation DeleteUser(\$id: ID!) {
            deleteUser(id: \$id) {
              success
            }
          }
        '''),
        variables: {'id': id},
        update: (cache, result) {
          // Remove from cache
          cache.evict(
            PartialKey(typename: 'User', fields: {'id': id}),
          );
        },
      ),
    );

    if (result.hasException) {
      throw result.exception!;
    }
  }
}
```

## Subscriptions

### Basic Subscription

Listen to real-time updates:

```dart
class ChatMessages extends StatelessWidget {
  final String chatId;

  const ChatMessages({required this.chatId});

  @override
  Widget build(BuildContext context) {
    return Subscription(
      options: SubscriptionOptions(
        document: gql('''
          subscription OnMessageAdded(\$chatId: ID!) {
            messageAdded(chatId: \$chatId) {
              id
              content
              author {
                id
                name
              }
              createdAt
            }
          }
        '''),
        variables: {'chatId': chatId},
      ),
      builder: (result) {
        if (result.isLoading) {
          return Center(child: CircularProgressIndicator());
        }

        if (result.hasException) {
          return Center(child: Text('Error: ${result.exception}'));
        }

        if (result.data == null) {
          return Center(child: Text('No messages yet'));
        }

        final message = result.data!['messageAdded'];

        // You'd typically combine this with a Query for existing messages
        // and append new messages from the subscription
        return MessageBubble(
          content: message['content'],
          author: message['author']['name'],
          timestamp: DateTime.parse(message['createdAt']),
        );
      },
    );
  }
}
```

### Subscription with WebSocket Link

Configure WebSocket for subscriptions:

```dart
class GraphQLConfig {
  static GraphQLClient createClientWithSubscriptions({
    required String httpEndpoint,
    required String wsEndpoint,
    String? token,
  }) {
    final httpLink = HttpLink(httpEndpoint);

    final wsLink = WebSocketLink(
      wsEndpoint,
      config: SocketClientConfig(
        autoReconnect: true,
        inactivityTimeout: Duration(seconds: 30),
        initialPayload: () async {
          return {
            'headers': {
              if (token != null) 'Authorization': 'Bearer $token',
            },
          };
        },
      ),
    );

    final authLink = AuthLink(
      getToken: () async => token != null ? 'Bearer $token' : null,
    );

    // Use WebSocket for subscriptions, HTTP for queries/mutations
    final link = Link.split(
      (request) => request.isSubscription,
      wsLink,
      authLink.concat(httpLink),
    );

    return GraphQLClient(
      link: link,
      cache: GraphQLCache(store: InMemoryStore()),
    );
  }
}
```

### Programmatic Subscriptions

Subscribe to events programmatically:

```dart
class ChatRepository {
  final GraphQLClient _client;

  ChatRepository(this._client);

  Stream<Message> subscribeToMessages(String chatId) {
    return _client.subscribe(
      SubscriptionOptions(
        document: gql('''
          subscription OnMessageAdded(\$chatId: ID!) {
            messageAdded(chatId: \$chatId) {
              id
              content
              author {
                id
                name
              }
              createdAt
            }
          }
        '''),
        variables: {'chatId': chatId},
      ),
    ).map((result) {
      if (result.hasException || result.data == null) {
        throw result.exception ?? Exception('No data');
      }

      return Message.fromJson(result.data!['messageAdded']);
    });
  }
}

// Usage
class ChatController {
  final ChatRepository _repository;
  StreamSubscription? _subscription;

  void listenToMessages(String chatId) {
    _subscription = _repository
        .subscribeToMessages(chatId)
        .listen(
          (message) {
            print('New message: ${message.content}');
            // Add to local state
          },
          onError: (error) {
            print('Subscription error: $error');
          },
        );
  }

  void dispose() {
    _subscription?.cancel();
  }
}
```

## Caching

### Cache Normalization

GraphQL normalizes cache by type and ID:

```dart
GraphQLCache(
  store: InMemoryStore(),
  typePolicies: {
    'User': TypePolicy(
      keyFields: {'id': true},
    ),
    'Post': TypePolicy(
      keyFields: {'id': true},
      fields: {
        'comments': FieldPolicy(
          // Merge new comments with existing
          merge: (existing, incoming, {args, variables}) {
            return [...?existing, ...incoming];
          },
        ),
      },
    ),
  },
)
```

### Persistent Cache

Persist cache to disk with Hive:

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Hive for persistent cache
  await initHiveForFlutter();

  final store = await HiveStore.open(
    path: await getApplicationDocumentsDirectory(),
  );

  final client = GraphQLClient(
    link: HttpLink('https://api.example.com/graphql'),
    cache: GraphQLCache(store: store),
  );

  runApp(MyApp(client: client));
}
```

### Manual Cache Updates

Update cache manually after mutations:

```dart
await _client.mutate(
  MutationOptions(
    document: gql(updateUserMutation),
    variables: {'id': userId, 'name': newName},
    update: (cache, result) {
      if (result.hasException || result.data == null) return;

      final user = result.data!['updateUser']['user'];

      // Write fragment to cache
      cache.writeFragment(
        Fragment(
          document: gql('''
            fragment UserData on User {
              id
              name
              email
            }
          '''),
        ).asRequest(idFields: {'id': userId}),
        data: user,
      );

      // Or write query to cache
      cache.writeQuery(
        Request(
          operation: Operation(
            document: gql(getUserQuery),
          ),
          variables: {'id': userId},
        ),
        data: {'user': user},
      );
    },
  ),
);
```

## Error Handling

Handle GraphQL errors:

```dart
class GraphQLErrorHandler {
  static String getErrorMessage(OperationException exception) {
    if (exception.linkException != null) {
      final linkException = exception.linkException!;

      if (linkException is NetworkException) {
        return 'Network error. Please check your connection.';
      }

      if (linkException is ServerException) {
        return 'Server error: ${linkException.parsedResponse?.errors?.first.message}';
      }
    }

    if (exception.graphqlErrors.isNotEmpty) {
      final error = exception.graphqlErrors.first;

      // Handle specific error codes
      final code = error.extensions?['code'];

      switch (code) {
        case 'UNAUTHENTICATED':
          return 'Please sign in to continue.';
        case 'FORBIDDEN':
          return 'You don\'t have permission to do that.';
        case 'VALIDATION_ERROR':
          return error.message;
        default:
          return error.message;
      }
    }

    return 'An unexpected error occurred.';
  }
}

// Usage
Query(
  options: QueryOptions(
    document: gql(query),
    errorPolicy: ErrorPolicy.all, // Don't throw, include errors in result
  ),
  builder: (result, {fetchMore, refetch}) {
    if (result.hasException) {
      return ErrorWidget(
        message: GraphQLErrorHandler.getErrorMessage(result.exception!),
        onRetry: refetch,
      );
    }
    // ...
  },
)
```

## Testing

Test GraphQL operations:

```dart
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:mockito/mockito.dart';
import 'package:test/test.dart';

class MockGraphQLClient extends Mock implements GraphQLClient {}

void main() {
  late MockGraphQLClient mockClient;
  late UserRepository repository;

  setUp(() {
    mockClient = MockGraphQLClient();
    repository = UserRepository(mockClient);
  });

  test('getUser returns user on success', () async {
    const userId = '123';
    final mockResult = QueryResult(
      data: {
        'user': {
          'id': userId,
          'name': 'John Doe',
          'email': 'john@example.com',
        },
      },
      source: QueryResultSource.network,
    );

    when(mockClient.query(any)).thenAnswer((_) async => mockResult);

    final user = await repository.getUser(userId);

    expect(user.id, userId);
    expect(user.name, 'John Doe');
  });

  test('createUser handles errors', () async {
    final mockResult = QueryResult(
      exception: OperationException(
        graphqlErrors: [
          GraphQLError(
            message: 'Email already exists',
            extensions: {'code': 'VALIDATION_ERROR'},
          ),
        ],
      ),
      source: QueryResultSource.network,
    );

    when(mockClient.mutate(any)).thenAnswer((_) async => mockResult);

    expect(
      () => repository.createUser(
        name: 'John',
        email: 'john@example.com',
      ),
      throwsA(isA<OperationException>()),
    );
  });
}
```

## Best Practices

1. **Use Fragments**: Define reusable fragments for common fields
2. **Type Policies**: Configure cache normalization for all types
3. **Error Handling**: Always handle both network and GraphQL errors
4. **Optimistic Updates**: Use for better perceived performance
5. **Pagination**: Implement cursor-based pagination for lists
6. **Batch Queries**: Combine related queries to reduce round trips
7. **Persist Cache**: Use Hive for offline access
8. **WebSocket Reconnection**: Enable auto-reconnect for subscriptions
9. **Testing**: Mock GraphQL client in tests
10. **Code Generation**: Consider graphql_codegen for type-safe operations

## Conclusion

GraphQL provides powerful data fetching capabilities that can significantly improve application performance and developer experience. The graphql_flutter package brings these benefits to Flutter with excellent caching, real-time subscriptions, and optimistic updates. Follow the patterns in this guide to build efficient, maintainable GraphQL integrations.
