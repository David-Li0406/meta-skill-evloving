---
title: Keep Interfaces Small and Focused
impact: MEDIUM
impactDescription: Enables flexible implementations and easier testing
tags: oop, interfaces, solid, isp
---

## Keep Interfaces Small and Focused

Large interfaces force implementers to provide methods they don't need. Small, focused interfaces enable flexible composition and easier mocking.

**Incorrect (fat interface):**

```php
<?php
// Fat interface - too many responsibilities
interface UserServiceInterface {
    public function find(int $id): ?User;
    public function findAll(): array;
    public function create(array $data): User;
    public function update(int $id, array $data): User;
    public function delete(int $id): void;
    public function sendWelcomeEmail(User $user): void;
    public function generateReport(): string;
    public function exportToCsv(): string;
}

// Implementers must provide everything
class ReadOnlyUserService implements UserServiceInterface {
    public function find(int $id): ?User { /* ... */ }
    public function findAll(): array { /* ... */ }

    // Forced to implement unused methods
    public function create(array $data): User {
        throw new RuntimeException('Not supported');
    }
    public function update(int $id, array $data): User {
        throw new RuntimeException('Not supported');
    }
    // ... more stub methods
}
```

**Correct (segregated interfaces):**

```php
<?php
declare(strict_types=1);

// Single responsibility interfaces
interface UserFinderInterface {
    public function find(int $id): ?User;
    public function findAll(): array;
}

interface UserCreatorInterface {
    public function create(array $data): User;
}

interface UserUpdaterInterface {
    public function update(int $id, array $data): User;
}

interface UserDeleterInterface {
    public function delete(int $id): void;
}

interface UserExporterInterface {
    public function exportToCsv(): string;
}

// Combine interfaces when needed
interface UserRepositoryInterface extends
    UserFinderInterface,
    UserCreatorInterface,
    UserUpdaterInterface,
    UserDeleterInterface {}

// Implement only what's needed
final class ReadOnlyUserService implements UserFinderInterface {
    public function find(int $id): ?User { /* ... */ }
    public function findAll(): array { /* ... */ }
}

// Full implementation
final class UserService implements UserRepositoryInterface {
    // Implements all CRUD methods
}

// Easy to mock in tests
final class UserExportService {
    public function __construct(
        private UserFinderInterface $finder, // Only needs finding
        private UserExporterInterface $exporter
    ) {}
}
```

Follow Interface Segregation Principle: clients should not depend on methods they don't use.

Reference: [SOLID Principles - ISP](https://en.wikipedia.org/wiki/Interface_segregation_principle)
