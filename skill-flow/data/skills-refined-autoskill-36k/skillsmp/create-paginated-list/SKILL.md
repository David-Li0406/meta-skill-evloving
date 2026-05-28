---
name: create-paginated-list
description: Create paginated list UseCase (Request + UseCase + Response + Test). Use when listing entities with pagination. Generates Get{EntityPlural} pattern with page/itemsPerPage.
---

# Create Paginated List

Generate complete pagination pattern: Request interface, UseCase, Response, and Test.

**IMPORTANT**: Always uses `tdd-workflow` skill (MANDATORY)

---

## When to Use

- Listing entities with pagination
- Adding page/itemsPerPage to existing entity queries
- Creating Get{EntityPlural} endpoints

---

## Inputs/Outputs

| Input | Example | Output |
|-------|---------|--------|
| bc | Inventory | `{BC}/UseCases/{Entity}/Get{EntityPlural}/` |
| entity | StockMovement | `Get{EntityPlural}Request.php` |
| entityPlural | StockMovements | `Get{EntityPlural}.php` (UseCase) |
| | | `Get{EntityPlural}Response.php` |
| | | Test in `{BC}/Tests/UseCases/...` |

---

## Process

**Follow**: `.claude/skills/tdd-workflow/` (MANDATORY)

| Phase | File | Template |
|-------|------|----------|
| **RED** | Test.php | `.claude/templates/paginated-test.php.tpl` |
| **GREEN** | Request + UseCase + Response | `paginated-request.php.tpl`, `paginated-use-case.php.tpl`, `paginated-response.php.tpl` |
| **REFACTOR** | - | `make cs-fixer && make stan && make ta` |
| **VALIDATE** | - | `make qa` |

---

## Structures

**Request** (interface):
```php
namespace {BC}\UseCases\{Entity}\Get{EntityPlural};

interface Get{EntityPlural}Request
{
    public function page(): int;
    public function itemsPerPage(): int;
}
```

**UseCase** (readonly):
```php
namespace {BC}\UseCases\{Entity}\Get{EntityPlural};

use {BC}\Entities\Repository\{Entity}Repository;

final readonly class Get{EntityPlural}
{
    public function __construct(private {Entity}Repository $repository)
    {
    }

    public function execute(Get{EntityPlural}Request $request): Get{EntityPlural}Response
    {
        $collection = $this->repository->getAll{EntityPlural}Paginated(
            $request->page(),
            $request->itemsPerPage()
        );

        return new Get{EntityPlural}Response($collection);
    }
}
```

**Response**:
```php
namespace {BC}\UseCases\{Entity}\Get{EntityPlural};

use {BC}\Entities\{Entity}\{Entity}Collection;

final readonly class Get{EntityPlural}Response
{
    public function __construct(public {Entity}Collection $collection)
    {
    }
}
```

**See**: `docs/QUICK_REF.md#usecase-pattern`

---

## Rules

**Collection Pattern**:
- UseCase returns `{Entity}Collection` (NOT array)
- Collection implements `Iterator` + `Countable`
- `count()` returns **total items** (for pagination), not page size

**Collection Constructor**:
- Signature: `__construct(private readonly int $totalItems)`
- `totalItems` = nombre total en BDD (pas la taille de la page)
- Utilisé par `count()` pour le calcul de pagination

**Repository Method**:
- Add `getAll{EntityPlural}Paginated(int $page, int $itemsPerPage): {Entity}Collection`
- Convention projet : `getAll` + pluriel entité + `Paginated`
- Exemples existants : `getAllArticlesPaginated()`, `getAllSuppliersPaginated()`

**Tests**:
- Mock repository with `expects()->once()`
- Test with collection containing 2+ items
- Verify page/itemsPerPage passed to repository

**See**: `docs/GLOSSARY.md#collection`

---

## Prerequisites

Before using this skill, ensure:
1. Entity exists (`{BC}/Entities/{Entity}/{Entity}.php`)
2. Collection exists (`{BC}/Entities/{Entity}/{Entity}Collection.php`)
3. Repository interface exists (`{BC}/Entities/Repository/{Entity}Repository.php`)

If missing, use skills:
- `create-entity` for entity
- `create-repository` for repository

---

## Templates

- `paginated-request.php.tpl`
- `paginated-use-case.php.tpl`
- `paginated-response.php.tpl`
- `paginated-test.php.tpl`

**Location**: `.claude/templates/`

---

## References

- TDD workflow: `.claude/skills/tdd-workflow/`
- UseCase pattern: `docs/QUICK_REF.md#usecase-pattern`
- Collection: `docs/GLOSSARY.md#collection`
- Existing impl: `src/Admin/UseCases/Article/GetArticles/`