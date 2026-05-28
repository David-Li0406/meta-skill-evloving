# Flutter Project Structure

Project structure significantly impacts the maintainability and scalability of Flutter applications. A well-organized codebase makes it easy to find files, understand relationships between components, and work collaboratively with other developers.

## The Importance of Structure

As Flutter applications grow, poor organization becomes increasingly painful:

- **Finding files takes too long**: Developers waste time searching for the right file
- **Unclear where new code belongs**: Team members put files in inconsistent locations
- **Merge conflicts increase**: Multiple developers modify the same files
- **Coupling increases**: Related files scattered across directories encourage poor dependencies
- **Onboarding slows down**: New developers struggle to understand the codebase layout

Good project structure addresses these issues by providing clear, consistent organization that scales with your application.

## Two Main Approaches

There are two primary approaches to organizing Flutter projects: feature-based and layer-based. Each has advantages and works better in different contexts.

### Feature-Based Structure

Feature-based structure organizes code by features first, with architectural layers as subdirectories within each feature. All code related to a specific feature lives together.

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
│   │   ├── api_client.dart
│   │   └── network_info.dart
│   ├── theme/
│   │   ├── app_theme.dart
│   │   └── app_colors.dart
│   └── utils/
│       ├── validators.dart
│       └── formatters.dart
├── features/
│   ├── authentication/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   │   ├── auth_api_service.dart
│   │   │   │   └── auth_local_service.dart
│   │   │   ├── models/
│   │   │   │   ├── user_dto.dart
│   │   │   │   └── login_response_dto.dart
│   │   │   └── repositories/
│   │   │       └── auth_repository_impl.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── user.dart
│   │   │   ├── repositories/
│   │   │   │   └── auth_repository.dart
│   │   │   └── usecases/
│   │   │       ├── login_user.dart
│   │   │       ├── logout_user.dart
│   │   │       └── get_current_user.dart
│   │   └── presentation/
│   │       ├── viewmodels/
│   │       │   ├── login_viewmodel.dart
│   │       │   └── register_viewmodel.dart
│   │       ├── views/
│   │       │   ├── login_view.dart
│   │       │   └── register_view.dart
│   │       └── widgets/
│   │           ├── email_input_field.dart
│   │           └── password_input_field.dart
│   ├── products/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   └── orders/
│       ├── data/
│       ├── domain/
│       └── presentation/
└── main.dart
```

**Advantages**:

- **Feature Encapsulation**: All code for a feature is in one place, making it easy to find and modify
- **Team Scalability**: Different developers can work on different features with minimal conflicts
- **Feature Deletion**: Can remove an entire feature by deleting one directory
- **Clear Ownership**: Teams can own specific features and directories
- **Easier Navigation**: Related files are physically close together

**Best For**:
- Medium to large applications with distinct features
- Teams with multiple developers
- Applications expected to grow significantly
- Projects where features are relatively independent

### Layer-Based Structure

Layer-based structure organizes code by architectural layers first, with features nested inside each layer. This emphasizes the layered architecture.

```
lib/
├── core/
│   ├── di/
│   ├── errors/
│   ├── network/
│   └── utils/
├── data/
│   ├── datasources/
│   │   ├── auth/
│   │   │   ├── auth_api_service.dart
│   │   │   └── auth_local_service.dart
│   │   ├── products/
│   │   │   ├── product_api_service.dart
│   │   │   └── product_database_service.dart
│   │   └── orders/
│   ├── models/
│   │   ├── auth/
│   │   ├── products/
│   │   └── orders/
│   └── repositories/
│       ├── auth_repository_impl.dart
│       ├── product_repository_impl.dart
│       └── order_repository_impl.dart
├── domain/
│   ├── entities/
│   │   ├── user.dart
│   │   ├── product.dart
│   │   └── order.dart
│   ├── repositories/
│   │   ├── auth_repository.dart
│   │   ├── product_repository.dart
│   │   └── order_repository.dart
│   └── usecases/
│       ├── auth/
│       ├── products/
│       └── orders/
├── presentation/
│   ├── viewmodels/
│   │   ├── login_viewmodel.dart
│   │   ├── product_list_viewmodel.dart
│   │   └── order_detail_viewmodel.dart
│   ├── views/
│   │   ├── auth/
│   │   ├── products/
│   │   └── orders/
│   └── widgets/
│       ├── common/
│       ├── auth/
│       ├── products/
│       └── orders/
└── main.dart
```

**Advantages**:

- **Clear Layering**: Architectural layers are immediately visible
- **Easy Layer Navigation**: Find all repositories, all entities, etc. in one place
- **Enforces Architecture**: Layer separation is explicit in directory structure
- **Good for Learning**: New developers can easily understand the layered architecture

**Disadvantages**:

- **Feature Scattering**: Files for a single feature are spread across multiple directories
- **More Navigation**: Frequently jumping between directories when working on features
- **Merge Conflicts**: More likely when multiple developers work on similar features
- **Harder to Remove Features**: Need to delete files from multiple directories

**Best For**:
- Small to medium applications
- Solo developers or small teams
- Applications where emphasizing layers is important for team understanding
- Educational contexts where architecture clarity is prioritized

## Recommended Structure: Feature-Based

For most Flutter applications, especially those expected to grow, feature-based structure is recommended. It scales better and reduces friction as teams and codebases expand.

The official Flutter documentation (updated 2026) recommends feature-based organization for medium to large applications, stating that "the folders by feature pattern is the way to go as it scales well and organizes files in its feature folder."

## Core Directory

Both approaches include a `core/` directory for shared code that doesn't belong to specific features. This directory contains foundational code used throughout the application.

### Common Core Subdirectories

```
core/
├── di/                 # Dependency injection configuration
├── errors/             # Error handling and exceptions
├── network/            # Network configuration and utilities
├── theme/              # App theme and styling
├── utils/              # Utility functions and helpers
├── constants/          # App-wide constants
├── extensions/         # Dart extension methods
└── config/             # App configuration
```

**Dependency Injection** (`di/`):
- Service locator setup (get_it configuration)
- Injectable configuration
- Dependency registration code

**Errors** (`errors/`):
- Custom exception classes
- Failure classes for error handling
- Error message constants

**Network** (`network/`):
- HTTP client configuration (Dio, http)
- Network connectivity checking
- API endpoints and base URLs
- Interceptors and middleware

**Theme** (`theme/`):
- App theme definitions
- Color schemes
- Text styles
- Custom theme extensions

**Utils** (`utils/`):
- Validators (email, password, etc.)
- Formatters (date, currency, etc.)
- Helper functions
- Extension methods on built-in types

**Constants** (`constants/`):
- App-wide constant values
- String constants
- Configuration values
- Magic numbers with semantic names

## Feature Structure

Each feature in a feature-based structure follows the same pattern, making the codebase predictable and easy to navigate.

### Standard Feature Layout

```
features/feature_name/
├── data/
│   ├── datasources/
│   │   ├── feature_api_service.dart
│   │   └── feature_local_service.dart
│   ├── models/
│   │   └── feature_dto.dart
│   └── repositories/
│       └── feature_repository_impl.dart
├── domain/
│   ├── entities/
│   │   └── feature_entity.dart
│   ├── repositories/
│   │   └── feature_repository.dart
│   └── usecases/
│       ├── get_feature.dart
│       └── create_feature.dart
└── presentation/
    ├── viewmodels/
    │   └── feature_viewmodel.dart
    ├── views/
    │   └── feature_view.dart
    └── widgets/
        └── feature_widget.dart
```

### Data Layer Organization

**Datasources**: Classes that interact with specific data sources
- API services for remote data
- Database services for local data
- Cache services for temporary storage
- Platform channel services for native code

**Models**: DTOs for serialization/deserialization
- One DTO per API response structure
- Conversion methods to domain entities
- JSON serialization annotations

**Repositories**: Implementations of domain repository interfaces
- Coordinate between data sources
- Handle caching logic
- Transform DTOs to entities
- Implement error handling

### Domain Layer Organization

**Entities**: Core business objects
- Immutable domain models
- Business logic methods
- Value equality (Equatable)
- No serialization logic

**Repositories**: Abstract interfaces
- Define data access contracts
- No implementation details
- Return domain entities
- Declare exceptions that can be thrown

**Use Cases**: Business operations
- One class per operation
- Orchestrate repository calls
- Apply business rules
- Return domain entities

### Presentation Layer Organization

**ViewModels** (or BLoCs/Controllers): Presentation logic
- Manage UI state
- Call use cases
- Transform entities to UI models
- Handle user interactions
- Notify views of state changes

**Views**: Screen-level widgets
- StatelessWidget or StatefulWidget
- Observe ViewModel state
- Build UI based on state
- Trigger ViewModel methods
- Handle navigation

**Widgets**: Reusable UI components
- Feature-specific widgets
- Stateless when possible
- Accept data via parameters
- Trigger callbacks for interactions

## File Naming Conventions

Consistent file naming is crucial for navigating and understanding the codebase.

### General Rules

- Use **snake_case** for all file names
- Name files after the primary class they contain
- Include suffixes that indicate the file's purpose
- Keep names descriptive but concise

### Common Suffixes

**Data Layer**:
- `*_api_service.dart` - API data source
- `*_database_service.dart` - Database data source
- `*_local_service.dart` - Local storage data source
- `*_dto.dart` - Data transfer object
- `*_repository_impl.dart` - Repository implementation

**Domain Layer**:
- `*_repository.dart` - Repository interface (abstract class)
- No suffix for entities (e.g., `user.dart`, `product.dart`)
- Descriptive use case names (e.g., `login_user.dart`, `create_order.dart`)

**Presentation Layer**:
- `*_viewmodel.dart` - ViewModel
- `*_bloc.dart` - BLoC
- `*_controller.dart` - Controller
- `*_view.dart` or `*_screen.dart` or `*_page.dart` - Screen-level widget
- Descriptive widget names (e.g., `email_input_field.dart`)

**Core**:
- `*_exception.dart` - Exception class
- `*_failure.dart` - Failure class
- `*_validator.dart` - Validator
- `*_formatter.dart` - Formatter
- `*_extension.dart` - Extension methods

### Examples

```
user_repository.dart          # Interface
user_repository_impl.dart     # Implementation
user_dto.dart                 # DTO
user.dart                     # Entity
login_user.dart               # Use case
user_profile_viewmodel.dart   # ViewModel
user_profile_view.dart        # View
profile_avatar_widget.dart    # Widget
```

## Barrel Files (Index Files)

Barrel files re-export multiple files from a directory, simplifying imports. They're named `feature_name.dart` or use a generic name.

### Example Barrel File

```dart
// features/authentication/authentication.dart
export 'domain/entities/user.dart';
export 'domain/repositories/auth_repository.dart';
export 'domain/usecases/login_user.dart';
export 'domain/usecases/logout_user.dart';
export 'domain/usecases/get_current_user.dart';

export 'presentation/viewmodels/login_viewmodel.dart';
export 'presentation/views/login_view.dart';
```

**Benefits**:
- Simplify imports (single import instead of multiple)
- Hide internal directory structure
- Make refactoring easier (change internal structure without updating imports)

**Usage**:

```dart
// Instead of:
import 'package:myapp/features/authentication/domain/entities/user.dart';
import 'package:myapp/features/authentication/domain/usecases/login_user.dart';

// Use:
import 'package:myapp/features/authentication/authentication.dart';
```

**Caution**: Don't export everything. Only export public APIs that other features should use. Keep internal implementation details private.

## Shared Code Between Features

Sometimes multiple features need to share code. There are several approaches to handling shared code.

### Shared in Core

For truly app-wide code, put it in `core/`:

```
core/
└── widgets/
    ├── app_button.dart
    ├── app_text_field.dart
    └── loading_indicator.dart
```

### Shared Feature

For code shared by multiple features but not the entire app, create a shared feature:

```
features/
├── shared/
│   ├── domain/
│   │   ├── entities/
│   │   │   └── address.dart
│   │   └── value_objects/
│   │       └── email.dart
│   └── presentation/
│       └── widgets/
│           └── address_form.dart
├── authentication/
├── products/
└── orders/
```

### Feature Dependencies

Features can depend on other features' domain layers (entities and repositories), but should avoid depending on presentation or data layers:

```dart
// OK: products feature depends on auth feature's domain layer
import 'package:myapp/features/authentication/domain/entities/user.dart';

// Bad: products feature depends on auth feature's presentation
import 'package:myapp/features/authentication/presentation/views/login_view.dart';
```

## Test Structure

Mirror your source structure in tests:

```
test/
├── core/
│   ├── network/
│   │   └── network_info_test.dart
│   └── utils/
│       └── validators_test.dart
├── features/
│   ├── authentication/
│   │   ├── data/
│   │   │   └── repositories/
│   │   │       └── auth_repository_impl_test.dart
│   │   ├── domain/
│   │   │   └── usecases/
│   │   │       └── login_user_test.dart
│   │   └── presentation/
│   │       └── viewmodels/
│   │           └── login_viewmodel_test.dart
│   └── products/
└── helpers/
    ├── test_data.dart
    └── mock_factories.dart
```

**Test Naming**: Use `*_test.dart` suffix for all test files.

**Test Organization**:
- Mirror source directory structure
- Keep test files next to tested code (in test/ directory)
- Use `helpers/` or `fixtures/` for shared test utilities

## Large Applications: Modular Structure

For very large applications, consider organizing features into modules:

```
lib/
├── core/
├── modules/
│   ├── user_management/
│   │   └── features/
│   │       ├── authentication/
│   │       ├── profile/
│   │       └── settings/
│   ├── commerce/
│   │   └── features/
│   │       ├── products/
│   │       ├── cart/
│   │       └── checkout/
│   └── content/
│       └── features/
│           ├── articles/
│           ├── videos/
│           └── comments/
└── main.dart
```

This adds another level of organization for applications with dozens of features that naturally group into larger modules.

## Assets Structure

Organize assets similarly to code:

```
assets/
├── images/
│   ├── logos/
│   │   ├── logo.png
│   │   └── logo@2x.png
│   ├── icons/
│   │   └── custom_icons.png
│   └── illustrations/
│       └── onboarding.png
├── fonts/
│   ├── Roboto-Regular.ttf
│   └── Roboto-Bold.ttf
└── data/
    └── mock_data.json
```

**Best Practices**:
- Group by asset type (images, fonts, data)
- Use subdirectories for different image categories
- Include multiple resolutions for images (@2x, @3x)
- Use consistent naming conventions

## Migration Strategy

If you have an existing app with poor structure, migrate incrementally:

1. **Create New Structure**: Set up the new directory structure alongside existing code
2. **Identify Features**: List distinct features in your application
3. **Migrate One Feature**: Move one feature to the new structure
4. **Update Imports**: Update import statements
5. **Test Thoroughly**: Ensure the feature still works
6. **Repeat**: Migrate remaining features one at a time

Don't try to restructure everything at once. Incremental migration reduces risk and allows for course correction.

## Structure Best Practices

### Keep Related Files Together

Files that change together should live together. If you find yourself frequently modifying files in different directories for the same feature, they're probably in the wrong places.

### Avoid Deep Nesting

Limit directory depth to 4-5 levels. Deeper nesting makes navigation difficult and indicates over-organization.

```
// Too deep
lib/features/authentication/presentation/viewmodels/login/mobile/login_viewmodel.dart

// Better
lib/features/authentication/presentation/viewmodels/login_viewmodel.dart
```

### Use Consistent Patterns

Once you establish a pattern, follow it consistently across all features. Consistency reduces cognitive load and makes the codebase predictable.

### Don't Over-Organize

Not everything needs its own directory. If a directory only contains one file, it's probably unnecessary.

### Document Structure Decisions

Create a `STRUCTURE.md` or include structure documentation in your README:

```markdown
## Project Structure

This project uses feature-based organization with Clean Architecture layers.

Each feature contains:
- `data/` - Data layer (repositories, data sources, DTOs)
- `domain/` - Domain layer (entities, use cases, repository interfaces)
- `presentation/` - Presentation layer (ViewModels, Views, Widgets)

See `features/authentication/` for a reference implementation.
```

## Tooling Support

Several tools can help enforce and navigate project structure:

**IDE Plugins**:
- Flutter Enhancement Suite: Provides templates for creating feature structure
- Dart Data Class Generator: Generate boilerplate for entities and DTOs
- Flutter Riverpod Snippets: Code snippets for common patterns

**VS Code Snippets**: Create custom snippets for your structure:

```json
{
  "Create Feature": {
    "prefix": "feature",
    "body": [
      "class ${1:Feature}Repository {",
      "  $0",
      "}"
    ]
  }
}
```

**CLI Tools**: Create scripts to scaffold new features:

```bash
# scripts/create_feature.sh
#!/bin/bash
FEATURE_NAME=$1
mkdir -p lib/features/$FEATURE_NAME/{data,domain,presentation}
mkdir -p lib/features/$FEATURE_NAME/data/{datasources,models,repositories}
mkdir -p lib/features/$FEATURE_NAME/domain/{entities,repositories,usecases}
mkdir -p lib/features/$FEATURE_NAME/presentation/{viewmodels,views,widgets}
```

## Structure in Practice

Project structure is not about rigid rules but about organizing code to support your team's workflow. The best structure is one that:

- Makes it easy to find files
- Clearly indicates where new code belongs
- Minimizes merge conflicts
- Supports your team's development process
- Scales with your application

Start with feature-based structure for most applications. Adjust based on your specific needs, but maintain consistency once you establish patterns. Good structure reduces friction and lets developers focus on building features rather than navigating the codebase.
