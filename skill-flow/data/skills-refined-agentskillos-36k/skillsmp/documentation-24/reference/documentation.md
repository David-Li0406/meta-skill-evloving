# Documentation Standards

## API Documentation

Provide clear documentation for all public APIs and modules.

### C++ Documentation (Doxygen)

```cpp
/**
 * @brief Manages user authentication and session handling
 *
 * The UserAuthenticator class provides methods to authenticate users
 * against various authentication providers and manage their sessions.
 *
 * @note This class is thread-safe.
 *
 * Example usage:
 * @code
 * UserAuthenticator auth(config);
 * auto result = auth.authenticate("username", "password");
 * if (result.success) {
 *     auto session = auth.createSession(result.userId);
 * }
 * @endcode
 */
class UserAuthenticator {
public:
    /**
     * @brief Authenticates a user with username and password
     *
     * @param username The user's username
     * @param password The user's password (will be hashed internally)
     * @return AuthResult containing success status and user ID if successful
     *
     * @throws AuthenticationError if authentication service is unavailable
     * @throws std::invalid_argument if username or password is empty
     *
     * @warning The password parameter is sensitive and should be handled securely
     *
     * @see createSession
     */
    AuthResult authenticate(const std::string& username,
                          const std::string& password);

    /**
     * @brief Creates a new session for an authenticated user
     *
     * @param userId The ID of the authenticated user
     * @param expiresIn Session duration in seconds (default: 3600)
     * @return Session object containing session token and expiration time
     *
     * @pre User must be successfully authenticated
     * @post A new session entry is created in the session store
     */
    Session createSession(UserId userId, int expiresIn = 3600);

private:
    /**
     * @brief Hashes a password using the configured algorithm
     * @internal
     */
    std::string hashPassword(const std::string& password);
};
```

### Kotlin Documentation (KDoc)

```kotlin
/**
 * Manages user authentication and session handling.
 *
 * This class provides methods to authenticate users against various
 * authentication providers and manage their sessions.
 *
 * Example usage:
 * ```kotlin
 * val auth = UserAuthenticator(config)
 * val result = auth.authenticate("username", "password")
 * if (result.success) {
 *     val session = auth.createSession(result.userId)
 * }
 * ```
 *
 * @property config Authentication configuration
 * @constructor Creates a new UserAuthenticator with the given configuration
 */
class UserAuthenticator(private val config: AuthConfig) {

    /**
     * Authenticates a user with username and password.
     *
     * @param username The user's username
     * @param password The user's password (will be hashed internally)
     * @return [AuthResult] containing success status and user ID if successful
     *
     * @throws AuthenticationException if authentication service is unavailable
     * @throws IllegalArgumentException if username or password is empty
     *
     * @see createSession
     */
    fun authenticate(username: String, password: String): AuthResult

    /**
     * Creates a new session for an authenticated user.
     *
     * @param userId The ID of the authenticated user
     * @param expiresIn Session duration in seconds (default: 3600)
     * @return [Session] object containing session token and expiration time
     */
    fun createSession(userId: UserId, expiresIn: Int = 3600): Session
}
```

### Python Documentation (Docstrings)

```python
class UserAuthenticator:
    """Manages user authentication and session handling.

    This class provides methods to authenticate users against various
    authentication providers and manage their sessions.

    Thread-safety: This class is thread-safe.

    Example:
        >>> auth = UserAuthenticator(config)
        >>> result = auth.authenticate("username", "password")
        >>> if result.success:
        ...     session = auth.createSession(result.user_id)

    Attributes:
        config: Authentication configuration.
    """

    def __init__(self, config: AuthConfig):
        """Initializes the authenticator with the given configuration.

        Args:
            config: Authentication configuration object.
        """
        self.config = config

    def authenticate(self, username: str, password: str) -> AuthResult:
        """Authenticates a user with username and password.

        Args:
            username: The user's username.
            password: The user's password (will be hashed internally).

        Returns:
            AuthResult containing success status and user ID if successful.

        Raises:
            AuthenticationError: If authentication service is unavailable.
            ValueError: If username or password is empty.

        Warning:
            The password parameter is sensitive and should be handled securely.

        See Also:
            create_session: Creates a session for authenticated users.
        """
        pass

    def create_session(self, user_id: UserId, expires_in: int = 3600) -> Session:
        """Creates a new session for an authenticated user.

        Args:
            user_id: The ID of the authenticated user.
            expires_in: Session duration in seconds. Defaults to 3600.

        Returns:
            Session object containing session token and expiration time.

        Note:
            User must be successfully authenticated before calling this method.
        """
        pass
```

### TypeScript Documentation (TSDoc)

```typescript
/**
 * Manages user authentication and session handling.
 *
 * This class provides methods to authenticate users against various
 * authentication providers and manage their sessions.
 *
 * @example
 * ```typescript
 * const auth = new UserAuthenticator(config);
 * const result = await auth.authenticate("username", "password");
 * if (result.success) {
 *   const session = await auth.createSession(result.userId);
 * }
 * ```
 */
export class UserAuthenticator {
  /**
   * Creates a new UserAuthenticator instance.
   *
   * @param config - Authentication configuration
   */
  constructor(private config: AuthConfig) {}

  /**
   * Authenticates a user with username and password.
   *
   * @param username - The user's username
   * @param password - The user's password (will be hashed internally)
   * @returns Promise resolving to AuthResult
   *
   * @throws {@link AuthenticationError}
   * Thrown if authentication service is unavailable
   *
   * @throws {@link Error}
   * Thrown if username or password is empty
   *
   * @see {@link createSession} for creating sessions after authentication
   */
  async authenticate(username: string, password: string): Promise<AuthResult> {
    // Implementation
  }

  /**
   * Creates a new session for an authenticated user.
   *
   * @param userId - The ID of the authenticated user
   * @param expiresIn - Session duration in seconds
   * @returns Promise resolving to Session object
   *
   * @defaultValue expiresIn defaults to 3600 (1 hour)
   */
  async createSession(userId: UserId, expiresIn: number = 3600): Promise<Session> {
    // Implementation
  }
}
```

## README Files

Every project should have a comprehensive README.

### Template

```markdown
# Project Name

Brief one-paragraph description of what this project does and who it's for.

## Features

- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description

## Prerequisites

- C++20 compatible compiler (GCC 11+, Clang 14+, MSVC 2022+)
- CMake 3.20 or higher
- vcpkg (for dependency management)

## Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/username/project.git
cd project

# Install dependencies
vcpkg install

# Build
cmake -B build -DCMAKE_TOOLCHAIN_FILE=[vcpkg-root]/scripts/buildsystems/vcpkg.cmake
cmake --build build

# Run tests
cd build && ctest
```

### Detailed Installation

[More detailed installation instructions if needed]

## Usage

### Basic Example

```cpp
#include "project/module.h"

int main() {
    auto manager = Manager();
    manager.initialize();
    manager.process();
    return 0;
}
```

### Advanced Usage

[More complex usage examples]

## Configuration

Configuration is done via `config.json`:

```json
{
  "server": {
    "port": 8080,
    "host": "0.0.0.0"
  }
}
```

## API Documentation

Full API documentation is available at [link] or can be generated:

```bash
doxygen Doxyfile
# Documentation in docs/html/index.html
```

## Development

### Building from Source

[Development-specific build instructions]

### Running Tests

```bash
cmake --build build --target test
```

### Code Style

This project follows [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/).

Format code with:

```bash
clang-format -i src/**/*.cpp include/**/*.h
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Architecture

[Brief architecture overview or link to detailed docs]

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## Authors

- Author Name (@github-username)

## Acknowledgments

- List of third-party libraries
- Contributors
- Inspiration sources

## Support

- Issue Tracker: https://github.com/username/project/issues
- Documentation: https://docs.project.com
- Contact: email@example.com
```

## CHANGELOG

Maintain a changelog following [Semantic Versioning](https://semver.org/).

### Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature in progress

### Changed
- Improvements to existing feature

### Deprecated
- Feature that will be removed in next major version

### Removed
- Removed feature

### Fixed
- Bug fix

### Security
- Security vulnerability fix

## [1.2.0] - 2025-11-02

### Added
- User authentication system with JWT tokens
- Password reset functionality via email
- Two-factor authentication support

### Changed
- Improved database query performance by 40%
- Updated user profile UI for better usability

### Fixed
- Fixed memory leak in session management
- Resolved race condition in concurrent user login

## [1.1.0] - 2025-10-15

### Added
- REST API endpoints for user management
- Swagger documentation for all API endpoints

### Changed
- Migrated from SQLite to PostgreSQL for better scalability

### Deprecated
- Old authentication endpoints (use /api/v2/auth instead)

### Fixed
- Fixed incorrect error messages in validation

## [1.0.0] - 2025-09-01

### Added
- Initial release
- Basic user registration and login
- User profile management
- Admin dashboard

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

### Version Number Guidelines

Given a version number `MAJOR.MINOR.PATCH`:

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality additions
- **PATCH**: Backward-compatible bug fixes

## Architecture Documentation

### High-Level Architecture

```markdown
# Architecture Overview

## System Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────┐
│  API Layer  │
└──────┬──────┘
       │
       ▼
┌─────────────┐       ┌─────────────┐
│  Business   │◄─────►│   Cache     │
│   Logic     │       │  (Redis)    │
└──────┬──────┘       └─────────────┘
       │
       ▼
┌─────────────┐
│  Database   │
│ (PostgreSQL)│
└─────────────┘
```

## Component Descriptions

### API Layer
- **Responsibility**: Handle HTTP requests, validate input, format responses
- **Technologies**: Express.js, JWT authentication
- **Key classes**: `ApiServer`, `AuthMiddleware`, `RequestValidator`

### Business Logic
- **Responsibility**: Core business rules and data processing
- **Technologies**: TypeScript, Clean Architecture pattern
- **Key classes**: `UserService`, `PaymentProcessor`, `NotificationManager`

### Database
- **Responsibility**: Persistent data storage
- **Technologies**: PostgreSQL 14, Knex.js query builder
- **Key schemas**: `users`, `transactions`, `sessions`
```

## Inline Documentation

### When to Write Comments

**Do comment**:
- Complex algorithms or business logic
- Non-obvious design decisions
- Workarounds for bugs or limitations
- Public API interfaces

**Don't comment**:
- Obvious code that explains itself
- What the code does (code should be self-explanatory)
- Redundant information

### Example

```cpp
// ❌ Bad: Obvious comment
// Increment the counter
counter++;

// ❌ Bad: Redundant with function name
// Gets the user's name
std::string getName() const { return name_; }

// ✅ Good: Explains why, not what
// Cache results for 5 minutes to reduce database load during peak hours
constexpr int CACHE_DURATION_SECONDS = 300;

// ✅ Good: Explains non-obvious logic
// Use binary search instead of hash map here because the overhead
// of hash computation exceeds lookup time for small datasets (< 100 items)
auto it = std::lower_bound(data.begin(), data.end(), key);

// ✅ Good: Documents workaround
// WORKAROUND: Older versions of library X have a bug where method Y
// returns null instead of empty string. Remove this check after
// upgrading to version 2.0+
if (result == nullptr) result = "";
```
