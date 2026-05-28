/// Base class for all application failures.
abstract class Failure {
  final String message;
  final dynamic cause;

  const Failure(this.message, [this.cause]);

  @override
  String toString() =>
      '$runtimeType: $message${cause != null ? ' (Cause: $cause)' : ''}';
}

/// Represents failure during server communication.
class ServerFailure extends Failure {
  const ServerFailure(super.message, [super.cause]);
}

/// Represents failure during cache/local storage operations.
class CacheFailure extends Failure {
  const CacheFailure(super.message, [super.cause]);
}

/// Represents authentication failures.
class AuthFailure extends Failure {
  const AuthFailure(super.message, [super.cause]);
}

/// Represents generic or unknown failures.
class UnknownFailure extends Failure {
  const UnknownFailure(super.message, [super.cause]);
}
