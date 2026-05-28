---
name: jikime-lang-flutter
description: Flutter 3.24+ / Dart 3.5+ development specialist covering Riverpod, go_router, and cross-platform patterns. Use when building cross-platform mobile apps, desktop apps, or web applications with Flutter.
version: 1.0.0
tags: ["language", "dart", "flutter", "mobile", "cross-platform", "riverpod"]
triggers:
  keywords: ["flutter", "dart", "riverpod", "widget", "플러터", "모바일"]
  phases: ["run"]
  agents: ["frontend"]
  languages: ["dart"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2000
user-invocable: false
---

# Flutter Development Guide

Flutter 3.24+ / Dart 3.5+ 개발을 위한 간결한 가이드.

## Quick Reference

| 용도 | 도구 | 특징 |
|------|------|------|
| State | **Riverpod** | 타입 안전, 테스트 용이 |
| Router | **go_router** | 선언적 라우팅 |
| HTTP | **Dio** | 인터셉터, 취소 |
| Storage | **Hive** | 로컬 NoSQL |

## Project Setup

```bash
flutter create project
cd project

# 주요 패키지
flutter pub add flutter_riverpod go_router dio freezed_annotation
flutter pub add -d build_runner freezed json_serializable
```

## Widget Patterns

### Stateless Widget

```dart
class UserCard extends StatelessWidget {
  final User user;
  final VoidCallback? onTap;

  const UserCard({
    super.key,
    required this.user,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(child: Text(user.name[0])),
        title: Text(user.name),
        subtitle: Text(user.email),
        onTap: onTap,
      ),
    );
  }
}
```

### Consumer Widget (Riverpod)

```dart
class UserListPage extends ConsumerWidget {
  const UserListPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(usersProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Users')),
      body: usersAsync.when(
        data: (users) => ListView.builder(
          itemCount: users.length,
          itemBuilder: (context, index) => UserCard(user: users[index]),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('Error: $e')),
      ),
    );
  }
}
```

## Riverpod Patterns

### Providers

```dart
// Simple provider
final greetingProvider = Provider<String>((ref) => 'Hello');

// State provider
final counterProvider = StateProvider<int>((ref) => 0);

// Future provider
final usersProvider = FutureProvider<List<User>>((ref) async {
  final api = ref.watch(apiClientProvider);
  return api.getUsers();
});

// Notifier provider
final authProvider = NotifierProvider<AuthNotifier, AuthState>(AuthNotifier.new);

class AuthNotifier extends Notifier<AuthState> {
  @override
  AuthState build() => const AuthState.initial();

  Future<void> login(String email, String password) async {
    state = const AuthState.loading();
    try {
      final user = await ref.read(authServiceProvider).login(email, password);
      state = AuthState.authenticated(user);
    } catch (e) {
      state = AuthState.error(e.toString());
    }
  }

  void logout() {
    state = const AuthState.initial();
  }
}
```

## go_router Patterns

```dart
final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const HomePage(),
      ),
      GoRoute(
        path: '/users',
        builder: (context, state) => const UserListPage(),
        routes: [
          GoRoute(
            path: ':id',
            builder: (context, state) {
              final id = state.pathParameters['id']!;
              return UserDetailPage(userId: id);
            },
          ),
        ],
      ),
    ],
    redirect: (context, state) {
      final isAuthenticated = ref.read(authProvider).isAuthenticated;
      if (!isAuthenticated && state.matchedLocation != '/login') {
        return '/login';
      }
      return null;
    },
  );
});
```

## Data Models (Freezed)

```dart
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    @Default(false) bool isActive,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

@freezed
class AuthState with _$AuthState {
  const factory AuthState.initial() = _Initial;
  const factory AuthState.loading() = _Loading;
  const factory AuthState.authenticated(User user) = _Authenticated;
  const factory AuthState.error(String message) = _Error;
}
```

## API Client (Dio)

```dart
final apiClientProvider = Provider<ApiClient>((ref) {
  final dio = Dio(BaseOptions(
    baseUrl: 'https://api.example.com',
    connectTimeout: const Duration(seconds: 10),
  ));

  dio.interceptors.add(InterceptorsWrapper(
    onRequest: (options, handler) {
      final token = ref.read(authTokenProvider);
      if (token != null) {
        options.headers['Authorization'] = 'Bearer $token';
      }
      handler.next(options);
    },
  ));

  return ApiClient(dio);
});

class ApiClient {
  final Dio _dio;

  ApiClient(this._dio);

  Future<List<User>> getUsers() async {
    final response = await _dio.get('/users');
    return (response.data as List)
        .map((json) => User.fromJson(json))
        .toList();
  }
}
```

## Project Structure

```
lib/
├── main.dart
├── app/
│   ├── router.dart
│   └── theme.dart
├── features/
│   ├── auth/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   └── users/
├── shared/
│   ├── widgets/
│   └── utils/
└── core/
    ├── api/
    └── providers/
```

## Best Practices

- **Riverpod**: Provider로 상태 관리
- **Freezed**: 불변 데이터 모델
- **const**: 위젯에 const 사용
- **Feature-first**: 기능별 폴더 구조
- **Extension**: 유틸리티에 extension 사용

---

Last Updated: 2026-01-21
Version: 2.0.0
