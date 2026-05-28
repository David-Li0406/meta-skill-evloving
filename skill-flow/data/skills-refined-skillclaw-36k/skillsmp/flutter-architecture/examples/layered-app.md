# Layered Application Example

This document demonstrates a complete Flutter application structured with Clean Architecture layers. It shows how different features work together while maintaining proper layer separation and dependencies.

## Application Overview

A task management application with the following features:
- User authentication (login/logout)
- Task list viewing and management
- Task creation and editing
- Task completion tracking
- Offline support with caching

## Project Structure

```
lib/
├── core/
│   ├── di/
│   │   ├── injection.dart
│   │   └── injection.config.dart
│   ├── errors/
│   │   ├── exceptions.dart
│   │   └── failures.dart
│   ├── network/
│   │   └── network_info.dart
│   └── utils/
│       └── validators.dart
├── features/
│   ├── authentication/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   └── tasks/
│       ├── data/
│       ├── domain/
│       └── presentation/
└── main.dart
```

## Core Layer

### Dependency Injection Setup

```dart
// core/di/injection.dart
import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:dio/dio.dart';
import 'injection.config.dart';

final getIt = GetIt.instance;

@InjectableInit()
Future<void> configureDependencies() async {
  // Register async dependencies
  final sharedPreferences = await SharedPreferences.getInstance();
  getIt.registerSingleton<SharedPreferences>(sharedPreferences);

  // Configure Dio
  final dio = Dio(
    BaseOptions(
      baseUrl: 'https://api.example.com',
      connectTimeout: const Duration(seconds: 5),
      receiveTimeout: const Duration(seconds: 3),
    ),
  );
  getIt.registerSingleton<Dio>(dio);

  // Initialize injectable
  getIt.init();
}
```

### Error Handling

```dart
// core/errors/exceptions.dart
abstract class AppException implements Exception {
  final String message;
  AppException(this.message);
}

class ServerException extends AppException {
  ServerException([String message = 'Server error occurred'])
      : super(message);
}

class NetworkException extends AppException {
  NetworkException([String message = 'Network error occurred'])
      : super(message);
}

class CacheException extends AppException {
  CacheException([String message = 'Cache error occurred'])
      : super(message);
}

class UnauthorizedException extends AppException {
  UnauthorizedException([String message = 'Unauthorized'])
      : super(message);
}

class ValidationException extends AppException {
  ValidationException(String message) : super(message);
}
```

```dart
// core/errors/failures.dart
import 'package:equatable/equatable.dart';

abstract class Failure extends Equatable {
  final String message;

  const Failure(this.message);

  @override
  List<Object> get props => [message];
}

class ServerFailure extends Failure {
  const ServerFailure(super.message);
}

class NetworkFailure extends Failure {
  const NetworkFailure(super.message);
}

class CacheFailure extends Failure {
  const CacheFailure(super.message);
}

class AuthFailure extends Failure {
  const AuthFailure(super.message);
}

class ValidationFailure extends Failure {
  const ValidationFailure(super.message);
}
```

### Network Utilities

```dart
// core/network/network_info.dart
import 'package:injectable/injectable.dart';
import 'package:connectivity_plus/connectivity_plus.dart';

abstract class NetworkInfo {
  Future<bool> get isConnected;
}

@Injectable(as: NetworkInfo)
class NetworkInfoImpl implements NetworkInfo {
  final Connectivity _connectivity;

  NetworkInfoImpl(this._connectivity);

  @override
  Future<bool> get isConnected async {
    final result = await _connectivity.checkConnectivity();
    return result != ConnectivityResult.none;
  }
}

// Module for registering third-party dependencies
@module
abstract class NetworkModule {
  @lazySingleton
  Connectivity get connectivity => Connectivity();
}
```

## Authentication Feature

### Domain Layer

```dart
// features/authentication/domain/entities/user.dart
import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String id;
  final String email;
  final String name;
  final String token;

  const User({
    required this.id,
    required this.email,
    required this.name,
    required this.token,
  });

  @override
  List<Object> get props => [id, email, name, token];
}
```

```dart
// features/authentication/domain/repositories/auth_repository.dart
import 'package:dartz/dartz.dart';
import '../../../../core/errors/failures.dart';
import '../entities/user.dart';

abstract class AuthRepository {
  Future<Either<Failure, User>> login(String email, String password);
  Future<Either<Failure, void>> logout();
  Future<Either<Failure, User?>> getCurrentUser();
}
```

```dart
// features/authentication/domain/usecases/login_user.dart
import 'package:dartz/dartz.dart';
import 'package:injectable/injectable.dart';
import '../../../../core/errors/failures.dart';
import '../entities/user.dart';
import '../repositories/auth_repository.dart';

@injectable
class LoginUser {
  final AuthRepository _repository;

  LoginUser(this._repository);

  Future<Either<Failure, User>> call(String email, String password) async {
    // Validate inputs
    if (email.isEmpty || password.isEmpty) {
      return const Left(ValidationFailure('Email and password are required'));
    }

    if (!_isValidEmail(email)) {
      return const Left(ValidationFailure('Invalid email format'));
    }

    if (password.length < 6) {
      return const Left(
        ValidationFailure('Password must be at least 6 characters'),
      );
    }

    return await _repository.login(email, password);
  }

  bool _isValidEmail(String email) {
    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    return emailRegex.hasMatch(email);
  }
}
```

### Data Layer

```dart
// features/authentication/data/models/user_dto.dart
import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/user.dart';

part 'user_dto.g.dart';

@JsonSerializable()
class UserDto {
  final String id;
  final String email;
  final String name;
  final String token;

  UserDto({
    required this.id,
    required this.email,
    required this.name,
    required this.token,
  });

  factory UserDto.fromJson(Map<String, dynamic> json) =>
      _$UserDtoFromJson(json);

  Map<String, dynamic> toJson() => _$UserDtoToJson(this);

  User toEntity() => User(
        id: id,
        email: email,
        name: name,
        token: token,
      );

  factory UserDto.fromEntity(User user) => UserDto(
        id: user.id,
        email: user.email,
        name: user.name,
        token: user.token,
      );
}
```

```dart
// features/authentication/data/datasources/auth_api_service.dart
import 'package:dio/dio.dart';
import 'package:injectable/injectable.dart';
import '../../../../core/errors/exceptions.dart';
import '../models/user_dto.dart';

@injectable
class AuthApiService {
  final Dio _dio;

  AuthApiService(this._dio);

  Future<UserDto> login(String email, String password) async {
    try {
      final response = await _dio.post(
        '/auth/login',
        data: {
          'email': email,
          'password': password,
        },
      );

      return UserDto.fromJson(response.data);
    } on DioException catch (e) {
      if (e.type == DioExceptionType.connectionTimeout ||
          e.type == DioExceptionType.connectionError) {
        throw NetworkException('Connection failed');
      } else if (e.response?.statusCode == 401) {
        throw UnauthorizedException('Invalid credentials');
      } else {
        throw ServerException('Login failed');
      }
    }
  }

  Future<void> logout(String token) async {
    try {
      await _dio.post(
        '/auth/logout',
        options: Options(
          headers: {'Authorization': 'Bearer $token'},
        ),
      );
    } on DioException {
      throw ServerException('Logout failed');
    }
  }
}
```

```dart
// features/authentication/data/datasources/auth_local_service.dart
import 'package:injectable/injectable.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import '../models/user_dto.dart';
import '../../../../core/errors/exceptions.dart';

@injectable
class AuthLocalService {
  final SharedPreferences _prefs;

  AuthLocalService(this._prefs);

  static const String _userKey = 'cached_user';

  Future<UserDto?> getCachedUser() async {
    try {
      final userJson = _prefs.getString(_userKey);
      if (userJson != null) {
        return UserDto.fromJson(jsonDecode(userJson));
      }
      return null;
    } catch (e) {
      throw CacheException('Failed to get cached user');
    }
  }

  Future<void> cacheUser(UserDto user) async {
    try {
      await _prefs.setString(_userKey, jsonEncode(user.toJson()));
    } catch (e) {
      throw CacheException('Failed to cache user');
    }
  }

  Future<void> clearUser() async {
    try {
      await _prefs.remove(_userKey);
    } catch (e) {
      throw CacheException('Failed to clear user');
    }
  }
}
```

```dart
// features/authentication/data/repositories/auth_repository_impl.dart
import 'package:dartz/dartz.dart';
import 'package:injectable/injectable.dart';
import '../../../../core/errors/exceptions.dart';
import '../../../../core/errors/failures.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_api_service.dart';
import '../datasources/auth_local_service.dart';

@Injectable(as: AuthRepository)
class AuthRepositoryImpl implements AuthRepository {
  final AuthApiService _apiService;
  final AuthLocalService _localService;

  AuthRepositoryImpl(this._apiService, this._localService);

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    try {
      final userDto = await _apiService.login(email, password);
      final user = userDto.toEntity();

      // Cache user locally
      await _localService.cacheUser(userDto);

      return Right(user);
    } on UnauthorizedException catch (e) {
      return Left(AuthFailure(e.message));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(e.message));
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    } catch (e) {
      return Left(ServerFailure('An unexpected error occurred'));
    }
  }

  @override
  Future<Either<Failure, void>> logout() async {
    try {
      final cachedUser = await _localService.getCachedUser();
      if (cachedUser != null) {
        await _apiService.logout(cachedUser.token);
      }

      await _localService.clearUser();
      return const Right(null);
    } on ServerException {
      // Still clear local cache even if API call fails
      await _localService.clearUser();
      return const Right(null);
    } catch (e) {
      return Left(ServerFailure('Logout failed'));
    }
  }

  @override
  Future<Either<Failure, User?>> getCurrentUser() async {
    try {
      final cachedUser = await _localService.getCachedUser();
      if (cachedUser != null) {
        return Right(cachedUser.toEntity());
      }
      return const Right(null);
    } on CacheException catch (e) {
      return Left(CacheFailure(e.message));
    }
  }
}
```

### Presentation Layer

```dart
// features/authentication/presentation/viewmodels/login_viewmodel.dart
import 'package:flutter/foundation.dart';
import 'package:injectable/injectable.dart';
import '../../domain/entities/user.dart';
import '../../domain/usecases/login_user.dart';

@injectable
class LoginViewModel extends ChangeNotifier {
  final LoginUser _loginUser;

  LoginViewModel(this._loginUser);

  String _email = '';
  String _password = '';
  bool _isLoading = false;
  String? _errorMessage;
  User? _user;

  String get email => _email;
  String get password => _password;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  User? get user => _user;

  bool get canSubmit =>
      _email.isNotEmpty && _password.isNotEmpty && !_isLoading;

  void updateEmail(String value) {
    _email = value;
    _errorMessage = null;
    notifyListeners();
  }

  void updatePassword(String value) {
    _password = value;
    _errorMessage = null;
    notifyListeners();
  }

  Future<bool> login() async {
    if (!canSubmit) return false;

    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    final result = await _loginUser(_email, _password);

    return result.fold(
      (failure) {
        _errorMessage = failure.message;
        _isLoading = false;
        notifyListeners();
        return false;
      },
      (user) {
        _user = user;
        _isLoading = false;
        notifyListeners();
        return true;
      },
    );
  }

  @override
  void dispose() {
    _email = '';
    _password = '';
    super.dispose();
  }
}
```

## Tasks Feature

### Domain Layer

```dart
// features/tasks/domain/entities/task.dart
import 'package:equatable/equatable.dart';

enum TaskPriority { low, medium, high }

class Task extends Equatable {
  final String id;
  final String title;
  final String? description;
  final bool isCompleted;
  final TaskPriority priority;
  final DateTime createdAt;
  final DateTime? dueDate;

  const Task({
    required this.id,
    required this.title,
    this.description,
    required this.isCompleted,
    required this.priority,
    required this.createdAt,
    this.dueDate,
  });

  Task copyWith({
    String? id,
    String? title,
    String? description,
    bool? isCompleted,
    TaskPriority? priority,
    DateTime? createdAt,
    DateTime? dueDate,
  }) {
    return Task(
      id: id ?? this.id,
      title: title ?? this.title,
      description: description ?? this.description,
      isCompleted: isCompleted ?? this.isCompleted,
      priority: priority ?? this.priority,
      createdAt: createdAt ?? this.createdAt,
      dueDate: dueDate ?? this.dueDate,
    );
  }

  @override
  List<Object?> get props => [
        id,
        title,
        description,
        isCompleted,
        priority,
        createdAt,
        dueDate,
      ];
}
```

```dart
// features/tasks/domain/usecases/get_tasks.dart
import 'package:dartz/dartz.dart';
import 'package:injectable/injectable.dart';
import '../../../../core/errors/failures.dart';
import '../entities/task.dart';
import '../repositories/task_repository.dart';

@injectable
class GetTasks {
  final TaskRepository _repository;

  GetTasks(this._repository);

  Future<Either<Failure, List<Task>>> call() async {
    return await _repository.getTasks();
  }
}
```

```dart
// features/tasks/domain/usecases/toggle_task_completion.dart
import 'package:dartz/dartz.dart';
import 'package:injectable/injectable.dart';
import '../../../../core/errors/failures.dart';
import '../entities/task.dart';
import '../repositories/task_repository.dart';

@injectable
class ToggleTaskCompletion {
  final TaskRepository _repository;

  ToggleTaskCompletion(this._repository);

  Future<Either<Failure, Task>> call(Task task) async {
    final updatedTask = task.copyWith(isCompleted: !task.isCompleted);
    return await _repository.updateTask(updatedTask);
  }
}
```

### Presentation Layer

```dart
// features/tasks/presentation/viewmodels/task_list_viewmodel.dart
import 'package:flutter/foundation.dart';
import 'package:injectable/injectable.dart';
import '../../domain/entities/task.dart';
import '../../domain/usecases/get_tasks.dart';
import '../../domain/usecases/toggle_task_completion.dart';

@injectable
class TaskListViewModel extends ChangeNotifier {
  final GetTasks _getTasks;
  final ToggleTaskCompletion _toggleTaskCompletion;

  TaskListViewModel(this._getTasks, this._toggleTaskCompletion);

  List<Task> _tasks = [];
  bool _isLoading = false;
  String? _errorMessage;

  List<Task> get tasks => _tasks;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  List<Task> get activeTasks =>
      _tasks.where((task) => !task.isCompleted).toList();

  List<Task> get completedTasks =>
      _tasks.where((task) => task.isCompleted).toList();

  int get activeTaskCount => activeTasks.length;
  int get completedTaskCount => completedTasks.length;

  Future<void> loadTasks() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    final result = await _getTasks();

    result.fold(
      (failure) {
        _errorMessage = failure.message;
        _isLoading = false;
        notifyListeners();
      },
      (tasks) {
        _tasks = tasks;
        _isLoading = false;
        notifyListeners();
      },
    );
  }

  Future<void> toggleTaskCompletion(Task task) async {
    final result = await _toggleTaskCompletion(task);

    result.fold(
      (failure) {
        _errorMessage = failure.message;
        notifyListeners();
      },
      (updatedTask) {
        final index = _tasks.indexWhere((t) => t.id == updatedTask.id);
        if (index != -1) {
          _tasks[index] = updatedTask;
          notifyListeners();
        }
      },
    );
  }
}
```

## Main Application

```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'core/di/injection.dart';
import 'features/authentication/presentation/viewmodels/login_viewmodel.dart';
import 'features/authentication/presentation/views/login_view.dart';
import 'features/tasks/presentation/viewmodels/task_list_viewmodel.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Configure dependency injection
  await configureDependencies();

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => getIt<LoginViewModel>(),
        ),
        ChangeNotifierProvider(
          create: (_) => getIt<TaskListViewModel>(),
        ),
      ],
      child: MaterialApp(
        title: 'Task Manager',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
          useMaterial3: true,
        ),
        home: const LoginView(),
      ),
    );
  }
}
```

## Key Architectural Points

### Layer Separation

**Domain Layer Independence**: The domain layer has no dependencies on Flutter, data sources, or presentation. It's pure Dart code that could run anywhere.

**Dependency Inversion**: Data and Presentation layers depend on Domain through interfaces. Domain defines what it needs, other layers provide it.

**Clear Boundaries**: Each layer has a specific responsibility and communicates through well-defined interfaces.

### Error Handling

**Exceptions in Data Layer**: Data sources throw exceptions when operations fail.

**Failures in Domain Layer**: Repositories convert exceptions to failures and return Either types.

**Messages in Presentation Layer**: ViewModels convert failures to user-friendly messages.

### Dependency Injection

**Centralized Configuration**: All dependencies registered in one place using injectable.

**Lifecycle Management**: Singletons for services, factories for ViewModels.

**Testability**: Easy to substitute mocks for testing.

### State Management

**ChangeNotifier ViewModels**: Simple, effective state management for MVVM pattern.

**Reactive UI**: Views rebuild automatically when ViewModel state changes.

**Clear Data Flow**: User actions → ViewModel methods → Use cases → Repositories → Data sources.

This layered architecture provides a solid foundation for scalable Flutter applications. Each layer can evolve independently, features can be added without breaking existing code, and the system remains testable at every level.
