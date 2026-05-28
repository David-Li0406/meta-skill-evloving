# JSON Serialization

Complete guide to JSON serialization in Flutter using code generation with json_serializable and freezed.

## Overview

JSON is the standard data format for web APIs. Flutter applications must serialize Dart objects to JSON for API requests and deserialize JSON responses into Dart objects. While manual serialization works for small projects, code generation eliminates boilerplate, prevents runtime errors, and improves maintainability for production applications.

This reference covers three approaches: manual serialization, json_serializable, and freezed, with recommendations for when to use each.

## Approaches to JSON Serialization

### Manual Serialization

Write fromJson and toJson methods manually:

**Advantages:**
- No build step required
- Simple for trivial models
- No additional dependencies

**Disadvantages:**
- Tedious and error-prone
- Runtime errors for typos
- Difficult to maintain as models grow
- No compile-time type safety

**When to Use:** Quick prototypes, very simple models, or learning projects.

### json_serializable

Automatic code generation for serialization:

**Advantages:**
- Eliminates boilerplate
- Compile-time type safety
- Catches errors during build
- Supports custom converters
- Widely adopted and mature

**Disadvantages:**
- Requires build step
- Generated code needs to be committed or regenerated
- Learning curve for annotations

**When to Use:** Production applications, medium to large codebases, or when you need reliable serialization.

### freezed

Immutable models with integrated serialization:

**Advantages:**
- All benefits of json_serializable
- Immutable data classes
- copyWith method
- Union types (sealed classes)
- Deep equality
- Pattern matching

**Disadvantages:**
- More complex setup
- Larger generated files
- Steeper learning curve

**When to Use:** Production applications using immutable architecture, state management with BLoC/Riverpod, or complex domain models.

## Manual Serialization

### Basic Implementation

```dart
class User {
  final String id;
  final String name;
  final String email;
  final DateTime createdAt;

  User({
    required this.id,
    required this.name,
    required this.email,
    required this.createdAt,
  });

  // Deserialize from JSON
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as String,
      name: json['name'] as String,
      email: json['email'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  // Serialize to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'created_at': createdAt.toIso8601String(),
    };
  }
}

// Usage
final json = {
  'id': '123',
  'name': 'John Doe',
  'email': 'john@example.com',
  'created_at': '2024-01-01T00:00:00.000Z',
};

final user = User.fromJson(json);
print(user.name); // John Doe

final serialized = user.toJson();
print(serialized['email']); // john@example.com
```

### Nested Objects

Handle nested JSON structures:

```dart
class Address {
  final String street;
  final String city;
  final String country;

  Address({
    required this.street,
    required this.city,
    required this.country,
  });

  factory Address.fromJson(Map<String, dynamic> json) {
    return Address(
      street: json['street'],
      city: json['city'],
      country: json['country'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'street': street,
      'city': city,
      'country': country,
    };
  }
}

class User {
  final String id;
  final String name;
  final Address address;

  User({
    required this.id,
    required this.name,
    required this.address,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      name: json['name'],
      address: Address.fromJson(json['address']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'address': address.toJson(),
    };
  }
}
```

### Lists

Handle JSON arrays:

```dart
class User {
  final String id;
  final String name;
  final List<String> roles;

  User({
    required this.id,
    required this.name,
    required this.roles,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      name: json['name'],
      roles: (json['roles'] as List).cast<String>(),
      // Or more safely:
      // roles: (json['roles'] as List).map((e) => e as String).toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'roles': roles,
    };
  }
}

// List of objects
class UserList {
  final List<User> users;

  UserList({required this.users});

  factory UserList.fromJson(List<dynamic> json) {
    return UserList(
      users: json.map((e) => User.fromJson(e)).toList(),
    );
  }

  List<dynamic> toJson() {
    return users.map((user) => user.toJson()).toList();
  }
}
```

## json_serializable

### Setup

Install required packages:

```yaml
dependencies:
  json_annotation: ^4.8.1

dev_dependencies:
  build_runner: ^2.4.7
  json_serializable: ^6.7.1
```

### Basic Usage

Create a serializable model:

```dart
import 'package:json_annotation/json_annotation.dart';

// This line connects the builder to the generated code
part 'user.g.dart';

@JsonSerializable()
class User {
  final String id;
  final String name;
  final String email;

  User({
    required this.id,
    required this.name,
    required this.email,
  });

  // Connect the generated methods to the class
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

Generate code:

```bash
# One-time generation
flutter pub run build_runner build

# Watch mode (regenerates on file changes)
flutter pub run build_runner watch

# Delete conflicting outputs and rebuild
flutter pub run build_runner build --delete-conflicting-outputs
```

### Field Mapping

Map JSON keys to different Dart field names:

```dart
@JsonSerializable()
class User {
  final String id;

  @JsonKey(name: 'full_name')
  final String fullName;

  @JsonKey(name: 'email_address')
  final String email;

  @JsonKey(name: 'created_at')
  final DateTime createdAt;

  User({
    required this.id,
    required this.fullName,
    required this.email,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

### Optional and Default Values

Handle nullable and default values:

```dart
@JsonSerializable()
class User {
  final String id;
  final String name;

  // Nullable field
  final String? bio;

  // Default value
  @JsonKey(defaultValue: 'user')
  final String role;

  // Computed field (not serialized)
  @JsonKey(includeFromJson: false, includeToJson: false)
  String get displayName => '$name ($role)';

  User({
    required this.id,
    required this.name,
    this.bio,
    this.role = 'user',
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

### Nested Objects

Serialize nested structures:

```dart
@JsonSerializable()
class Address {
  final String street;
  final String city;

  Address({required this.street, required this.city});

  factory Address.fromJson(Map<String, dynamic> json) =>
      _$AddressFromJson(json);
  Map<String, dynamic> toJson() => _$AddressToJson(this);
}

@JsonSerializable(explicitToJson: true)
class User {
  final String id;
  final String name;
  final Address address;

  User({
    required this.id,
    required this.name,
    required this.address,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

Note: `explicitToJson: true` is required for nested objects to call their `toJson()` method instead of calling `toString()`.

### Lists and Collections

Handle collections:

```dart
@JsonSerializable()
class User {
  final String id;
  final List<String> tags;
  final Map<String, dynamic> metadata;

  User({
    required this.id,
    required this.tags,
    required this.metadata,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}

@JsonSerializable(explicitToJson: true)
class Organization {
  final String id;
  final String name;
  final List<User> members;

  Organization({
    required this.id,
    required this.name,
    required this.members,
  });

  factory Organization.fromJson(Map<String, dynamic> json) =>
      _$OrganizationFromJson(json);
  Map<String, dynamic> toJson() => _$OrganizationToJson(this);
}
```

### Custom Converters

Handle complex types with converters:

```dart
// DateTime converter
class DateTimeConverter implements JsonConverter<DateTime, String> {
  const DateTimeConverter();

  @override
  DateTime fromJson(String json) => DateTime.parse(json);

  @override
  String toJson(DateTime object) => object.toIso8601String();
}

// Enum converter with custom values
enum UserStatus { active, inactive, suspended }

class UserStatusConverter implements JsonConverter<UserStatus, String> {
  const UserStatusConverter();

  @override
  UserStatus fromJson(String json) {
    switch (json) {
      case 'ACTIVE':
        return UserStatus.active;
      case 'INACTIVE':
        return UserStatus.inactive;
      case 'SUSPENDED':
        return UserStatus.suspended;
      default:
        throw ArgumentError('Unknown status: $json');
    }
  }

  @override
  String toJson(UserStatus object) {
    switch (object) {
      case UserStatus.active:
        return 'ACTIVE';
      case UserStatus.inactive:
        return 'INACTIVE';
      case UserStatus.suspended:
        return 'SUSPENDED';
    }
  }
}

@JsonSerializable()
class User {
  final String id;

  @DateTimeConverter()
  final DateTime createdAt;

  @UserStatusConverter()
  final UserStatus status;

  User({
    required this.id,
    required this.createdAt,
    required this.status,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

### Configuration Options

Customize code generation globally:

```yaml
# build.yaml
targets:
  $default:
    builders:
      json_serializable:
        options:
          # Generate JSON keys in snake_case
          field_rename: snake

          # Create both fromJson and toJson
          create_factory: true
          create_to_json: true

          # Use explicit toJson for nested objects
          explicit_to_json: true

          # Check for required fields
          checked: true

          # Disallow extra keys in JSON
          disallow_unrecognized_keys: false

          # Use named constructors
          constructor: ''
```

Or configure per-class:

```dart
@JsonSerializable(
  fieldRename: FieldRename.snake,
  explicitToJson: true,
  checked: true,
  disallowUnrecognizedKeys: true,
)
class User {
  // ...
}
```

## freezed Package

### Setup

Install required packages:

```yaml
dependencies:
  freezed_annotation: ^2.4.1
  json_annotation: ^4.8.1

dev_dependencies:
  build_runner: ^2.4.7
  freezed: ^2.4.6
  json_serializable: ^6.7.1
```

### Basic Usage

Create an immutable model with freezed:

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    String? bio,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

Generate code:

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

Benefits:
- All fields are final (immutable)
- copyWith method generated automatically
- == and hashCode implemented
- toString() with all fields
- JSON serialization included

### copyWith Method

Modify immutable objects:

```dart
final user = User(
  id: '123',
  name: 'John Doe',
  email: 'john@example.com',
);

// Create modified copy
final updatedUser = user.copyWith(
  name: 'Jane Doe',
  bio: 'Flutter developer',
);

print(user.name); // John Doe
print(updatedUser.name); // Jane Doe
print(updatedUser.id); // 123 (unchanged)
```

### Union Types (Sealed Classes)

Model multiple states or variants:

```dart
@freezed
class ApiResponse<T> with _$ApiResponse<T> {
  const factory ApiResponse.loading() = _Loading<T>;
  const factory ApiResponse.success(T data) = _Success<T>;
  const factory ApiResponse.error(String message) = _Error<T>;
}

// Usage with pattern matching
Widget buildContent(ApiResponse<List<User>> response) {
  return response.when(
    loading: () => CircularProgressIndicator(),
    success: (users) => UserList(users: users),
    error: (message) => ErrorWidget(message: message),
  );
}

// Or with map
final message = response.map(
  loading: (_) => 'Loading...',
  success: (data) => 'Loaded ${data.length} users',
  error: (error) => 'Error: ${error.message}',
);

// Or with maybeWhen (default case)
Widget build(BuildContext context) {
  return response.maybeWhen(
    success: (users) => UserList(users: users),
    orElse: () => Center(child: Text('No data')),
  );
}
```

### Deep Equality

Compare objects by value:

```dart
final user1 = User(id: '123', name: 'John', email: 'john@example.com');
final user2 = User(id: '123', name: 'John', email: 'john@example.com');
final user3 = User(id: '456', name: 'Jane', email: 'jane@example.com');

print(user1 == user2); // true (same values)
print(user1 == user3); // false (different values)

// Useful in collections
final users = {user1, user2}; // Set has only one element
print(users.length); // 1
```

### Mixin Methods

Add custom methods to freezed classes:

```dart
@freezed
class User with _$User {
  const User._(); // Private constructor required for custom methods

  const factory User({
    required String id,
    required String name,
    required String email,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);

  // Custom methods
  String get displayName => name.toUpperCase();

  bool get hasValidEmail => email.contains('@');
}

// Usage
final user = User(id: '123', name: 'John', email: 'john@example.com');
print(user.displayName); // JOHN
print(user.hasValidEmail); // true
```

### Default Values

Set default values for optional fields:

```dart
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    @Default('user') String role,
    @Default([]) List<String> tags,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// Usage
final user = User(id: '123', name: 'John');
print(user.role); // 'user'
print(user.tags); // []
```

### Custom Converters with freezed

Use json_serializable converters with freezed:

```dart
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    @JsonKey(name: 'created_at')
    @DateTimeConverter()
    required DateTime createdAt,
    @UserStatusConverter()
    required UserStatus status,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

## Generic Models

Create reusable generic models:

```dart
@freezed
class ApiResponse<T> with _$ApiResponse<T> {
  const factory ApiResponse({
    required bool success,
    String? message,
    T? data,
  }) = _ApiResponse<T>;

  factory ApiResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Object?) fromJsonT,
  ) =>
      _$ApiResponseFromJson(json, fromJsonT);
}

// Usage
final response = ApiResponse<User>.fromJson(
  json,
  (data) => User.fromJson(data as Map<String, dynamic>),
);
```

## Large JSON Parsing

Parse large JSON on background isolate:

```dart
import 'dart:convert';
import 'dart:isolate';
import 'package:flutter/foundation.dart';

// Parse on background thread
Future<List<User>> parseUsersInBackground(String jsonString) async {
  return await compute(_parseUsers, jsonString);
}

List<User> _parseUsers(String jsonString) {
  final json = jsonDecode(jsonString) as List;
  return json.map((e) => User.fromJson(e)).toList();
}

// Usage
final jsonString = await response.body;
final users = await parseUsersInBackground(jsonString);
```

## Error Handling

Handle serialization errors gracefully:

```dart
class SafeUser {
  final String id;
  final String name;
  final String email;

  SafeUser({
    required this.id,
    required this.name,
    required this.email,
  });

  factory SafeUser.fromJson(Map<String, dynamic> json) {
    try {
      return SafeUser(
        id: json['id']?.toString() ?? '',
        name: json['name']?.toString() ?? 'Unknown',
        email: json['email']?.toString() ?? '',
      );
    } catch (e) {
      throw SerializationException(
        'Failed to parse User: $e',
        json: json,
      );
    }
  }

  static List<SafeUser> fromJsonList(List<dynamic> json) {
    final users = <SafeUser>[];

    for (var i = 0; i < json.length; i++) {
      try {
        users.add(SafeUser.fromJson(json[i]));
      } catch (e) {
        print('Skipping invalid user at index $i: $e');
      }
    }

    return users;
  }
}

class SerializationException implements Exception {
  final String message;
  final Map<String, dynamic>? json;

  SerializationException(this.message, {this.json});

  @override
  String toString() => message;
}
```

## Testing

Test serialization:

```dart
import 'package:test/test.dart';

void main() {
  group('User serialization', () {
    test('fromJson creates valid user', () {
      final json = {
        'id': '123',
        'name': 'John Doe',
        'email': 'john@example.com',
      };

      final user = User.fromJson(json);

      expect(user.id, '123');
      expect(user.name, 'John Doe');
      expect(user.email, 'john@example.com');
    });

    test('toJson produces correct JSON', () {
      final user = User(
        id: '123',
        name: 'John Doe',
        email: 'john@example.com',
      );

      final json = user.toJson();

      expect(json['id'], '123');
      expect(json['name'], 'John Doe');
      expect(json['email'], 'john@example.com');
    });

    test('roundtrip maintains data', () {
      final original = User(
        id: '123',
        name: 'John Doe',
        email: 'john@example.com',
      );

      final json = original.toJson();
      final restored = User.fromJson(json);

      expect(restored, original);
    });

    test('handles missing optional fields', () {
      final json = {
        'id': '123',
        'name': 'John Doe',
        'email': 'john@example.com',
        // bio is missing
      };

      final user = User.fromJson(json);

      expect(user.bio, null);
    });
  });
}
```

## Best Practices

1. **Use Code Generation**: Prefer json_serializable or freezed over manual serialization
2. **Immutability**: Use freezed for immutable models with state management
3. **Custom Converters**: Create reusable converters for complex types
4. **Field Mapping**: Use @JsonKey for API-to-Dart name mapping
5. **Null Safety**: Handle nullable fields explicitly
6. **Default Values**: Provide defaults for optional fields
7. **Error Handling**: Catch and handle serialization errors gracefully
8. **Background Parsing**: Use compute() for large JSON parsing
9. **Testing**: Test serialization roundtrips
10. **Documentation**: Document expected JSON structure in comments

## Common Pitfalls

- **Missing explicitToJson**: Nested objects serialize to toString() instead of JSON
- **Forgot build_runner**: Changes not reflected until regeneration
- **DateTime Parsing**: Not all servers use ISO8601 format
- **Enum Serialization**: Default enum serialization may not match API
- **Null vs Missing**: Distinguish between null and absent fields
- **List Casting**: Use proper casting for lists: `.cast<T>()` or `.map((e) => e as T).toList()`
- **Large JSON on UI Thread**: Blocking UI with synchronous JSON parsing
- **No Error Handling**: Crashes on malformed JSON

## Conclusion

JSON serialization is critical for Flutter apps communicating with APIs. While manual serialization works for simple cases, production applications benefit significantly from code generation. Use json_serializable for straightforward models and freezed when you need immutability, union types, and deep equality. Both eliminate boilerplate, prevent runtime errors, and improve maintainability.
