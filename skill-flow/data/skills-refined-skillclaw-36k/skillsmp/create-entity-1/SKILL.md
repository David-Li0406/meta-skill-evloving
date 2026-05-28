---
name: create-entity
description: Create a new immutable domain entity following DDD patterns. Use when user needs to create a new business entity with domain logic, value objects, and behavior methods. Generates entity class with private constructor, static factory, and domain methods.
---

# Create Entity

Generate immutable domain entity following DDD patterns.

---

## When to Use

- New business entity
- Domain model in BC
- Aggregate root
- Entity with domain behavior

---

## Inputs/Outputs

| Input | Example | Output |
|-------|---------|--------|
| bc | Admin | `BC/Entities/EntityName.php` |
| entity | Article | - |
| fields | ['uuid' => 'ResourceUuid', 'name' => 'NameField'] | - |
| behaviors | ['rename', 'activate'] | - |

---

## Process

| Step | Action |
|------|--------|
| **Create** | Use template: `entity.php.tpl` |
| **Validate** | `make cs-fixer && make stan` |

---

## Structure

**Entity** (`final`, private constructor, static factory):
```php
final class EntityName {
    private function __construct(
        private ResourceUuid $uuid,
        private NameField $name,
    ) {}

    public static function create(string $name): self {
        return new self(ResourceUuid::generate(), NameField::fromString($name));
    }

    public function uuid(): ResourceUuid { return $this->uuid; }
    public function name(): NameField { return $this->name; }

    public function rename(string $name): void {
        $this->name = NameField::fromString($name);
    }
}
```

**See**: `docs/GLOSSARY.md#entity` for detailed definition

---

## Rules

**Class Structure**:
- `final` class, private constructor
- Static factory: `create()`, `createFrom*()`, `reconstitute()`
- No public properties, no setters

**Methods**:
- Getters return Value Objects: `name()` (not `getName()`)
- Behaviors modify state: `rename()`, `activate()`, `deactivate()`
- Validate in behaviors, encapsulate business rules

**Value Objects**:
- Use existing VOs: `Shared\Entities\VO\` (ResourceUuid, NameField, EmailField, PriceField)
- Create new VO if needed (skill: `create-value-object`)

---

## Templates

- `entity.php.tpl`

**Location**: `.claude/templates/`

---

## References

- Entity definition: `docs/GLOSSARY.md#entity`
- Entity pattern: `docs/QUICK_REF.md#entity-pattern`
- Architecture: `docs/architecture.md#entity`

---

## Related Skills

- `create-value-object` - Create new Value Object
- `create-use-case` - Create use case using entity
- `create-repository` - Create repository for entity
