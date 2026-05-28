---
title: Use ?Type for Nullable Parameters
impact: MEDIUM-HIGH
impactDescription: Clearly indicates when null is acceptable
tags: types, nullable, parameters, safety
---

## Use ?Type for Nullable Parameters

Not distinguishing nullable from required parameters leads to null pointer exceptions. Use ?Type or union types to explicitly indicate when null is valid.

**Incorrect (ambiguous null handling):**

```php
<?php
// Unclear if null is valid
function setParent($parent) {
    $this->parent = $parent;
}

// Default null without type - anything goes
function findUsers($status = null) {
    // Is $status optional or can it be explicitly null?
}

// Mixed type - no null safety
function process(mixed $data) {
    $data->doSomething(); // May be null!
}
```

**Correct (explicit nullable types):**

```php
<?php
declare(strict_types=1);

// Nullable parameter - null explicitly allowed
function setParent(?Category $parent): void {
    $this->parent = $parent;
}

// Required vs optional
function findUsers(?string $status = null): array {
    // null means "no filter" which is intentional
    if ($status !== null) {
        return $this->repository->findByStatus($status);
    }
    return $this->repository->findAll();
}

// Nullable return - may not find result
function findUser(int $id): ?User {
    return $this->repository->find($id);
}

// Non-nullable - guaranteed to exist
function findUserOrFail(int $id): User {
    return $this->repository->find($id)
        ?? throw new NotFoundException(User::class, $id);
}

// Union types for multiple possibilities
function getValue(string $key): string|int|null {
    return $this->config[$key] ?? null;
}

// Null-safe operator usage
function getParentName(?Category $category): ?string {
    return $category?->getParent()?->getName();
}

// Explicit null checks
function processUser(?User $user): void {
    if ($user === null) {
        return; // Early return for null
    }
    // $user is guaranteed non-null here
    $this->notify($user);
}
```

Use ?Type (PHP 7.1+) or Type|null union (PHP 8.0+) to document null expectations.
