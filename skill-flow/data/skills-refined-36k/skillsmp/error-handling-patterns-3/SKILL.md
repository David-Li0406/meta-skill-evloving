---
name: "Error Handling Patterns"
description: "Exception classes, failure classes, Either type, and error handling strategies"
version: "1.0.0"
---

# Error Handling Patterns

## Exception Classes (Data Layer)

```dart
abstract class AppException implements Exception {
  final String message;
  final String? code;
  
  const AppException({required this.message, this.code});
}

class ServerException extends AppException {
  final int? statusCode;
  
  const ServerException({
    required super.message,
    super.code,
    this.statusCode,
  });
}

class CacheException extends AppException {
  const CacheException({required super.message, super.code});
}

class NetworkException extends AppException {
  const NetworkException({
    super.message = 'No internet connection',
    super.code,
  });
}
```

## Failure Classes (Domain Layer)

```dart
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

class CacheFailure extends Failure {
  const CacheFailure(super.message);
}

class NetworkFailure extends Failure {
  const NetworkFailure([super.message = 'No internet connection']);
}
```

## Either Type Usage

```dart
import 'package:dartz/dartz.dart';

// Repository returns Either<Failure, Entity>
Future<Either<Failure, User>> getUser(String id) async {
  try {
    final model = await provider.fetchUser(id);
    return Right(model.toEntity());
  } on ServerException catch (e) {
    return Left(ServerFailure(e.message));
  } on NetworkException {
    return Left(NetworkFailure());
  }
}

// Controller handles Either result
final result = await getUserUseCase('123');
result.fold(
  (failure) => _handleError(failure),
  (user) => _user.value = user,
);
```
