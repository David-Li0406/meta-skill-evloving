---
title: Create Domain-Specific Exception Classes
impact: HIGH
impactDescription: Enables precise error handling and better debugging
tags: exceptions, errors, domain, classes
---

## Create Domain-Specific Exception Classes

Generic exceptions make it impossible to handle different error types appropriately. Domain-specific exceptions enable precise catching and better error messages.

**Incorrect (generic exceptions):**

```php
<?php
// Generic exceptions - can't distinguish error types
function findUser(int $id): User {
    if ($id <= 0) {
        throw new Exception('Invalid ID');
    }
    $user = $this->repository->find($id);
    if (!$user) {
        throw new Exception('Not found');
    }
    return $user;
}

// Caller can't handle specifically
try {
    $user = findUser($id);
} catch (Exception $e) {
    // Was it validation? Not found? Database error?
}
```

**Correct (domain-specific exceptions):**

```php
<?php
// Base domain exception
abstract class DomainException extends Exception {
    public function __construct(
        string $message,
        public readonly array $context = [],
        int $code = 0,
        ?Throwable $previous = null
    ) {
        parent::__construct($message, $code, $previous);
    }
}

// Specific exceptions
class ValidationException extends DomainException {
    public function __construct(
        public readonly string $field,
        string $message,
        array $context = []
    ) {
        parent::__construct($message, $context);
    }
}

class NotFoundException extends DomainException {
    public function __construct(
        public readonly string $resource,
        public readonly mixed $identifier
    ) {
        parent::__construct("{$resource} with ID {$identifier} not found", [
            'resource' => $resource,
            'identifier' => $identifier
        ]);
    }
}

class AuthorizationException extends DomainException {}
class InsufficientFundsException extends DomainException {}

// Usage
function findUser(int $id): User {
    if ($id <= 0) {
        throw new ValidationException('id', 'User ID must be positive');
    }
    $user = $this->repository->find($id);
    if (!$user) {
        throw new NotFoundException('User', $id);
    }
    return $user;
}

// Precise handling
try {
    $user = findUser($id);
} catch (ValidationException $e) {
    return response()->badRequest($e->field, $e->getMessage());
} catch (NotFoundException $e) {
    return response()->notFound($e->getMessage());
}
```

Organize exceptions in an Exceptions directory mirroring your domain.
