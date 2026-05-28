# Complete Feature Structure Example

This document provides a complete, production-ready example of a feature module following Clean Architecture and MVVM patterns. The example implements a user profile feature with view, edit, and update capabilities.

## Feature Overview

The user profile feature allows users to:
- View their profile information
- Edit profile details (name, bio, avatar)
- Update their profile
- Handle loading and error states

## Directory Structure

```
features/user_profile/
├── data/
│   ├── datasources/
│   │   ├── user_api_service.dart
│   │   └── user_cache_service.dart
│   ├── models/
│   │   └── user_profile_dto.dart
│   └── repositories/
│       └── user_profile_repository_impl.dart
├── domain/
│   ├── entities/
│   │   └── user_profile.dart
│   ├── repositories/
│   │   └── user_profile_repository.dart
│   └── usecases/
│       ├── get_user_profile.dart
│       └── update_user_profile.dart
└── presentation/
    ├── viewmodels/
    │   └── user_profile_viewmodel.dart
    ├── views/
    │   ├── user_profile_view.dart
    │   └── edit_profile_view.dart
    └── widgets/
        ├── profile_avatar.dart
        └── profile_info_card.dart
```

## Domain Layer

### Entity

```dart
// domain/entities/user_profile.dart
import 'package:equatable/equatable.dart';

class UserProfile extends Equatable {
  final String id;
  final String email;
  final String name;
  final String? bio;
  final String? avatarUrl;
  final DateTime createdAt;
  final DateTime updatedAt;

  const UserProfile({
    required this.id,
    required this.email,
    required this.name,
    this.bio,
    this.avatarUrl,
    required this.createdAt,
    required this.updatedAt,
  });

  UserProfile copyWith({
    String? id,
    String? email,
    String? name,
    String? bio,
    String? avatarUrl,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return UserProfile(
      id: id ?? this.id,
      email: email ?? this.email,
      name: name ?? this.name,
      bio: bio ?? this.bio,
      avatarUrl: avatarUrl ?? this.avatarUrl,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  @override
  List<Object?> get props => [
        id,
        email,
        name,
        bio,
        avatarUrl,
        createdAt,
        updatedAt,
      ];
}
```

### Repository Interface

```dart
// domain/repositories/user_profile_repository.dart
import 'package:dartz/dartz.dart';
import '../entities/user_profile.dart';

abstract class UserProfileRepository {
  Future<Either<Failure, UserProfile>> getUserProfile(String userId);
  Future<Either<Failure, UserProfile>> updateUserProfile(
    String userId,
    UpdateProfileParams params,
  );
  Future<Either<Failure, String>> uploadAvatar(File image);
}

class UpdateProfileParams {
  final String? name;
  final String? bio;
  final String? avatarUrl;

  UpdateProfileParams({
    this.name,
    this.bio,
    this.avatarUrl,
  });
}
```

### Use Cases

```dart
// domain/usecases/get_user_profile.dart
import 'package:dartz/dartz.dart';
import 'package:injectable/injectable.dart';
import '../entities/user_profile.dart';
import '../repositories/user_profile_repository.dart';

@injectable
class GetUserProfile {
  final UserProfileRepository _repository;

  GetUserProfile(this._repository);

  Future<Either<Failure, UserProfile>> call(String userId) async {
    return await _repository.getUserProfile(userId);
  }
}
```

```dart
// domain/usecases/update_user_profile.dart
import 'package:dartz/dartz.dart';
import 'package:injectable/injectable.dart';
import '../entities/user_profile.dart';
import '../repositories/user_profile_repository.dart';

@injectable
class UpdateUserProfile {
  final UserProfileRepository _repository;

  UpdateUserProfile(this._repository);

  Future<Either<Failure, UserProfile>> call(
    String userId,
    UpdateProfileParams params,
  ) async {
    // Business logic validation
    if (params.name != null && params.name!.trim().isEmpty) {
      return Left(ValidationFailure('Name cannot be empty'));
    }

    if (params.bio != null && params.bio!.length > 500) {
      return Left(ValidationFailure('Bio must be 500 characters or less'));
    }

    return await _repository.updateUserProfile(userId, params);
  }
}
```

## Data Layer

### DTO (Data Transfer Object)

```dart
// data/models/user_profile_dto.dart
import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/user_profile.dart';

part 'user_profile_dto.g.dart';

@JsonSerializable()
class UserProfileDto {
  final String id;
  final String email;
  final String name;
  final String? bio;
  @JsonKey(name: 'avatar_url')
  final String? avatarUrl;
  @JsonKey(name: 'created_at')
  final String createdAt;
  @JsonKey(name: 'updated_at')
  final String updatedAt;

  UserProfileDto({
    required this.id,
    required this.email,
    required this.name,
    this.bio,
    this.avatarUrl,
    required this.createdAt,
    required this.updatedAt,
  });

  factory UserProfileDto.fromJson(Map<String, dynamic> json) =>
      _$UserProfileDtoFromJson(json);

  Map<String, dynamic> toJson() => _$UserProfileDtoToJson(this);

  UserProfile toEntity() {
    return UserProfile(
      id: id,
      email: email,
      name: name,
      bio: bio,
      avatarUrl: avatarUrl,
      createdAt: DateTime.parse(createdAt),
      updatedAt: DateTime.parse(updatedAt),
    );
  }

  factory UserProfileDto.fromEntity(UserProfile entity) {
    return UserProfileDto(
      id: entity.id,
      email: entity.email,
      name: entity.name,
      bio: entity.bio,
      avatarUrl: entity.avatarUrl,
      createdAt: entity.createdAt.toIso8601String(),
      updatedAt: entity.updatedAt.toIso8601String(),
    );
  }
}
```

### Data Sources

```dart
// data/datasources/user_api_service.dart
import 'package:dio/dio.dart';
import 'package:injectable/injectable.dart';
import '../models/user_profile_dto.dart';

@injectable
class UserApiService {
  final Dio _dio;

  UserApiService(this._dio);

  Future<UserProfileDto> getUserProfile(String userId) async {
    try {
      final response = await _dio.get('/users/$userId/profile');
      return UserProfileDto.fromJson(response.data);
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) {
        throw NotFoundException('User profile not found');
      } else if (e.response?.statusCode == 401) {
        throw UnauthorizedException();
      } else {
        throw ServerException('Failed to fetch user profile');
      }
    }
  }

  Future<UserProfileDto> updateUserProfile(
    String userId,
    Map<String, dynamic> data,
  ) async {
    try {
      final response = await _dio.patch(
        '/users/$userId/profile',
        data: data,
      );
      return UserProfileDto.fromJson(response.data);
    } on DioException catch (e) {
      if (e.response?.statusCode == 400) {
        throw ValidationException(
          e.response?.data['message'] ?? 'Invalid data',
        );
      } else if (e.response?.statusCode == 401) {
        throw UnauthorizedException();
      } else {
        throw ServerException('Failed to update user profile');
      }
    }
  }

  Future<String> uploadAvatar(File image) async {
    try {
      final formData = FormData.fromMap({
        'avatar': await MultipartFile.fromFile(image.path),
      });

      final response = await _dio.post(
        '/users/avatar',
        data: formData,
      );

      return response.data['avatar_url'];
    } on DioException {
      throw ServerException('Failed to upload avatar');
    }
  }
}
```

```dart
// data/datasources/user_cache_service.dart
import 'package:injectable/injectable.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import '../models/user_profile_dto.dart';

@injectable
class UserCacheService {
  final SharedPreferences _prefs;

  UserCacheService(this._prefs);

  Future<UserProfileDto?> getCachedProfile(String userId) async {
    try {
      final cached = _prefs.getString('user_profile_$userId');
      if (cached != null) {
        return UserProfileDto.fromJson(jsonDecode(cached));
      }
      return null;
    } catch (e) {
      return null;
    }
  }

  Future<void> cacheProfile(UserProfileDto profile) async {
    await _prefs.setString(
      'user_profile_${profile.id}',
      jsonEncode(profile.toJson()),
    );
  }

  Future<void> clearCache(String userId) async {
    await _prefs.remove('user_profile_$userId');
  }
}
```

### Repository Implementation

```dart
// data/repositories/user_profile_repository_impl.dart
import 'package:dartz/dartz.dart';
import 'package:injectable/injectable.dart';
import '../../domain/entities/user_profile.dart';
import '../../domain/repositories/user_profile_repository.dart';
import '../datasources/user_api_service.dart';
import '../datasources/user_cache_service.dart';

@Injectable(as: UserProfileRepository)
class UserProfileRepositoryImpl implements UserProfileRepository {
  final UserApiService _apiService;
  final UserCacheService _cacheService;
  final NetworkInfo _networkInfo;

  UserProfileRepositoryImpl(
    this._apiService,
    this._cacheService,
    this._networkInfo,
  );

  @override
  Future<Either<Failure, UserProfile>> getUserProfile(String userId) async {
    try {
      if (await _networkInfo.isConnected) {
        final profileDto = await _apiService.getUserProfile(userId);
        final profile = profileDto.toEntity();

        // Cache the profile
        await _cacheService.cacheProfile(profileDto);

        return Right(profile);
      } else {
        // Return cached data when offline
        final cached = await _cacheService.getCachedProfile(userId);
        if (cached != null) {
          return Right(cached.toEntity());
        } else {
          return Left(CacheFailure('No cached data available'));
        }
      }
    } on NotFoundException {
      return Left(NotFoundFailure('User profile not found'));
    } on UnauthorizedException {
      return Left(AuthFailure('Unauthorized'));
    } on ServerException catch (e) {
      // Try cache as fallback
      final cached = await _cacheService.getCachedProfile(userId);
      if (cached != null) {
        return Right(cached.toEntity());
      }
      return Left(ServerFailure(e.message));
    } catch (e) {
      return Left(UnexpectedFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, UserProfile>> updateUserProfile(
    String userId,
    UpdateProfileParams params,
  ) async {
    try {
      if (!await _networkInfo.isConnected) {
        return Left(NetworkFailure('No internet connection'));
      }

      final data = <String, dynamic>{};
      if (params.name != null) data['name'] = params.name;
      if (params.bio != null) data['bio'] = params.bio;
      if (params.avatarUrl != null) data['avatar_url'] = params.avatarUrl;

      final profileDto = await _apiService.updateUserProfile(userId, data);
      final profile = profileDto.toEntity();

      // Update cache
      await _cacheService.cacheProfile(profileDto);

      return Right(profile);
    } on ValidationException catch (e) {
      return Left(ValidationFailure(e.message));
    } on UnauthorizedException {
      return Left(AuthFailure('Unauthorized'));
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    } catch (e) {
      return Left(UnexpectedFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, String>> uploadAvatar(File image) async {
    try {
      if (!await _networkInfo.isConnected) {
        return Left(NetworkFailure('No internet connection'));
      }

      final avatarUrl = await _apiService.uploadAvatar(image);
      return Right(avatarUrl);
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    } catch (e) {
      return Left(UnexpectedFailure(e.toString()));
    }
  }
}
```

## Presentation Layer

### ViewModel

```dart
// presentation/viewmodels/user_profile_viewmodel.dart
import 'package:flutter/foundation.dart';
import 'package:injectable/injectable.dart';
import '../../domain/entities/user_profile.dart';
import '../../domain/usecases/get_user_profile.dart';
import '../../domain/usecases/update_user_profile.dart';

@injectable
class UserProfileViewModel extends ChangeNotifier {
  final GetUserProfile _getUserProfile;
  final UpdateUserProfile _updateUserProfile;

  UserProfileViewModel(
    this._getUserProfile,
    this._updateUserProfile,
  );

  UserProfile? _profile;
  bool _isLoading = false;
  bool _isUpdating = false;
  String? _errorMessage;

  UserProfile? get profile => _profile;
  bool get isLoading => _isLoading;
  bool get isUpdating => _isUpdating;
  String? get errorMessage => _errorMessage;

  Future<void> loadProfile(String userId) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    final result = await _getUserProfile(userId);

    result.fold(
      (failure) {
        _errorMessage = _mapFailureToMessage(failure);
        _isLoading = false;
        notifyListeners();
      },
      (profile) {
        _profile = profile;
        _isLoading = false;
        notifyListeners();
      },
    );
  }

  Future<bool> updateProfile({
    String? name,
    String? bio,
    String? avatarUrl,
  }) async {
    if (_profile == null) return false;

    _isUpdating = true;
    _errorMessage = null;
    notifyListeners();

    final params = UpdateProfileParams(
      name: name,
      bio: bio,
      avatarUrl: avatarUrl,
    );

    final result = await _updateUserProfile(_profile!.id, params);

    return result.fold(
      (failure) {
        _errorMessage = _mapFailureToMessage(failure);
        _isUpdating = false;
        notifyListeners();
        return false;
      },
      (profile) {
        _profile = profile;
        _isUpdating = false;
        notifyListeners();
        return true;
      },
    );
  }

  String _mapFailureToMessage(Failure failure) {
    if (failure is ServerFailure) {
      return 'Server error. Please try again later.';
    } else if (failure is NetworkFailure) {
      return 'No internet connection.';
    } else if (failure is ValidationFailure) {
      return failure.message;
    } else if (failure is AuthFailure) {
      return 'You are not authorized to perform this action.';
    } else if (failure is NotFoundFailure) {
      return 'Profile not found.';
    } else {
      return 'An unexpected error occurred.';
    }
  }
}
```

### Views

```dart
// presentation/views/user_profile_view.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../viewmodels/user_profile_viewmodel.dart';
import '../widgets/profile_avatar.dart';
import '../widgets/profile_info_card.dart';
import 'edit_profile_view.dart';

class UserProfileView extends StatefulWidget {
  final String userId;

  const UserProfileView({
    super.key,
    required this.userId,
  });

  @override
  State<UserProfileView> createState() => _UserProfileViewState();
}

class _UserProfileViewState extends State<UserProfileView> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<UserProfileViewModel>().loadProfile(widget.userId);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        actions: [
          IconButton(
            icon: const Icon(Icons.edit),
            onPressed: () => _navigateToEditProfile(context),
          ),
        ],
      ),
      body: Consumer<UserProfileViewModel>(
        builder: (context, viewModel, child) {
          if (viewModel.isLoading) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }

          if (viewModel.errorMessage != null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(
                    Icons.error_outline,
                    size: 48,
                    color: Colors.red,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    viewModel.errorMessage!,
                    style: const TextStyle(color: Colors.red),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () => viewModel.loadProfile(widget.userId),
                    child: const Text('Retry'),
                  ),
                ],
              ),
            );
          }

          final profile = viewModel.profile;
          if (profile == null) {
            return const Center(
              child: Text('No profile data'),
            );
          }

          return RefreshIndicator(
            onRefresh: () => viewModel.loadProfile(widget.userId),
            child: SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  ProfileAvatar(
                    avatarUrl: profile.avatarUrl,
                    radius: 60,
                  ),
                  const SizedBox(height: 24),
                  ProfileInfoCard(profile: profile),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  Future<void> _navigateToEditProfile(BuildContext context) async {
    final updated = await Navigator.push<bool>(
      context,
      MaterialPageRoute(
        builder: (_) => ChangeNotifierProvider.value(
          value: context.read<UserProfileViewModel>(),
          child: EditProfileView(userId: widget.userId),
        ),
      ),
    );

    if (updated == true && mounted) {
      context.read<UserProfileViewModel>().loadProfile(widget.userId);
    }
  }
}
```

### Widgets

```dart
// presentation/widgets/profile_avatar.dart
import 'package:flutter/material.dart';

class ProfileAvatar extends StatelessWidget {
  final String? avatarUrl;
  final double radius;

  const ProfileAvatar({
    super.key,
    this.avatarUrl,
    this.radius = 40,
  });

  @override
  Widget build(BuildContext context) {
    return CircleAvatar(
      radius: radius,
      backgroundColor: Theme.of(context).colorScheme.primaryContainer,
      backgroundImage: avatarUrl != null ? NetworkImage(avatarUrl!) : null,
      child: avatarUrl == null
          ? Icon(
              Icons.person,
              size: radius,
              color: Theme.of(context).colorScheme.onPrimaryContainer,
            )
          : null,
    );
  }
}
```

This example demonstrates a complete, production-ready feature following Clean Architecture and MVVM patterns. It includes proper error handling, caching, loading states, and separation of concerns across all layers.
