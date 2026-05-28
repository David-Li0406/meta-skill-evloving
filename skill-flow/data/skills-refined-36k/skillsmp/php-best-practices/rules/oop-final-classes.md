---
title: Prefer final Classes, Extend Explicitly
impact: MEDIUM
impactDescription: Prevents unintended inheritance and simplifies reasoning
tags: oop, final, inheritance, design
---

## Prefer final Classes, Extend Explicitly

Open classes invite uncontrolled extension, leading to fragile base class problems. Default to final; only open classes explicitly designed for inheritance.

**Incorrect (open by default):**

```php
<?php
// Open class - can be extended unpredictably
class UserService {
    public function createUser(array $data): User {
        $user = new User($data);
        $this->repository->save($user);
        $this->eventDispatcher->dispatch(new UserCreated($user));
        return $user;
    }
}

// Subclass breaks parent assumptions
class ExtendedUserService extends UserService {
    public function createUser(array $data): User {
        // Skips event dispatch - breaks system!
        return $this->repository->save(new User($data));
    }
}
```

**Correct (final by default, explicit extension points):**

```php
<?php
declare(strict_types=1);

// Final - cannot be extended
final class UserService {
    public function __construct(
        private UserRepository $repository,
        private EventDispatcher $eventDispatcher
    ) {}

    public function createUser(array $data): User {
        $user = new User($data);
        $this->repository->save($user);
        $this->eventDispatcher->dispatch(new UserCreated($user));
        return $user;
    }
}

// Need customization? Use composition
final class AuditedUserService implements UserServiceInterface {
    public function __construct(
        private UserService $userService,
        private AuditLogger $auditLogger
    ) {}

    public function createUser(array $data): User {
        $user = $this->userService->createUser($data);
        $this->auditLogger->log('user_created', $user->id);
        return $user;
    }
}

// Or use interfaces for polymorphism
interface UserServiceInterface {
    public function createUser(array $data): User;
}

// When inheritance IS needed, design for it
abstract class AbstractRepository {
    abstract protected function getEntityClass(): string;

    final public function find(int $id): ?object {
        return $this->doFind($id);
    }

    protected function doFind(int $id): ?object {
        // Default implementation, can be overridden
    }
}
```

Final classes are easier to understand, test, and maintain.

Reference: [When to declare classes final](https://ocramius.github.io/blog/when-to-declare-classes-final/)
