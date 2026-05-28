---
name: create-repository
description: Create Repository interface and Finder interface for domain entity persistence. Use when entity needs persistence layer with commands (save, delete) and queries (find, findAll). Generates both Repository (commands) and Finder (queries) following CQRS pattern.
---

# Create Repository

Generate Repository (commands) and Finder (queries) interfaces.

---

## When to Use

- Entity needs persistence
- Implementing CQRS pattern
- Creating persistence layer ports

---

## Inputs/Outputs

| Input | Example | Output |
|-------|---------|--------|
| bc | Admin | `BC/Entities/Repository/EntityRepository.php` |
| entity | Article | `BC/UseCases/Gateway/Finder/EntityFinder.php` |
| entityPlural | Articles | Used in `findAll{EntityPlural}()` method |
| commands | ['save', 'delete'] | - |
| queries | ['find', 'findAll'] | - |

> **Note**: `entityPlural` handles irregular plurals (Category→Categories, Entity→Entities).

---

## Process

| Step | Action |
|------|--------|
| **Repository** | Create interface in `BC/Entities/Repository/` (template: `repository.php.tpl`) |
| **Finder** | Create interface in `BC/UseCases/Gateway/Finder/` (template: `finder.php.tpl`) |
| **Validate** | `make cs-fixer && make stan` |

---

## Structures

**Repository** (commands - throws exceptions):
```php
interface EntityRepository {
    public function getByUuid(ResourceUuid $uuid): Entity; // throws EntityNotFound
    public function save(Entity $entity): void;
    public function delete(Entity $entity): void;
}
```

**Finder** (queries - returns null/array):
```php
interface EntityFinder {
    public function find(ResourceUuid|string $uuid): ?Entity;
    public function findAll(): array; // @return Entity[]
    public function findByName(string $name): ?Entity;
}
```

**See**: `docs/GLOSSARY.md#repository-vs-finder` for detailed comparison

---

## Rules

**Repository** (commands):
- Location: `BC/Entities/Repository/`
- Methods: `get*()` MUST throw exception if not found
- Common: `getByUuid()`, `save()`, `delete()`
- Used in: Use cases that MODIFY state (Create, Update, Delete)

**Finder** (queries):
- Location: `BC/UseCases/Gateway/Finder/`
- Methods: `find*()` MAY return null or empty array
- Common: `find()`, `findAll()`, `findBy*()`
- Used in: Use cases that READ state (List, Search, Find)

**CRITICAL**: Repository for writes (throws), Finder for reads (returns null/array)

---

## Templates

- `repository.php.tpl` - Repository interface
- `finder.php.tpl` - Finder interface

**Location**: `.claude/templates/`

---

## References

- Repository vs Finder: `docs/GLOSSARY.md#repository-vs-finder`
- Repository pattern: `docs/QUICK_REF.md#repository-pattern`
- Finder pattern: `docs/QUICK_REF.md#finder-pattern`

---

## Related Skills

- `create-entity` - Create entity first
- `create-use-case` - Use repository/finder in use case
