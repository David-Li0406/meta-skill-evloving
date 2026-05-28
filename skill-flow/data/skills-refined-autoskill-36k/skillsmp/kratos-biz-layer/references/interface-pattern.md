# Interface Pattern

<use_case_interface>
## UseCase Interface

**Purpose**: Defines business operations exposed to service layer.

**Pattern**:
```go
type {Entity}UseCase interface {
	// Get{Entity} retrieves a {Entity} by its ID.
	Get{Entity}(ctx context.Context, id uint64) (*{Entity}, error)

	// Create{Entity} creates a new {Entity}.
	Create{Entity}(ctx context.Context, e *{Entity}) (*{Entity}, error)

	// Update{Entity} updates an existing {Entity}.
	Update{Entity}(ctx context.Context, e *{Entity}) (*{Entity}, error)

	// Delete{Entity} deletes a {Entity} by its ID.
	Delete{Entity}(ctx context.Context, id uint64) error

	// List{Entities} lists {Entities} with pagination.
	List{Entities}(ctx context.Context, options *List{Entities}Options) ([]*{Entity}, *pagination.PaginationMeta, error)
}
```

**Rules**:
- One interface per entity
- Methods match use case implementation
- First parameter always `context.Context`
- Return errors as last return value
- Use pointer types for structs
</use_case_interface>

<repo_interface>
## Repository Interface

**Purpose**: Defines data access contract implemented by data layer.

**Pattern**:
```go
type {Entity}Repo interface {
	// Create saves the given {Entity}.
	Create(context.Context, *{Entity}) (*{Entity}, error)

	// Update updates a {Entity}.
	Update(context.Context, *{Entity}) (*{Entity}, error)

	// FindByID returns the {Entity} with the given ID.
	FindByID(context.Context, uint64) (*{Entity}, error)

	// List{Entities} returns a list of {Entities}.
	List{Entities}(context.Context, *List{Entities}Options) ([]*{Entity}, *pagination.PaginationMeta, error)

	// Delete removes a {Entity} by its ID.
	Delete(context.Context, uint64) error
}
```

**Rules**:
- Repo methods use short names (Create vs Create{Entity})
- Accept/return business models, not ORM entities
- First parameter always `context.Context`
- No business logic in repo interface
</repo_interface>

<naming_rules>
## Naming Rules

**UseCase Interface**: `{Entity}UseCase` (exported)
**Repo Interface**: `{Entity}Repo` (exported)

**Method Naming**:
- UseCase: `Create{Entity}`, `Get{Entity}`, `Update{Entity}`
- Repo: `Create`, `FindByID`, `Update`

**Why Different?**:
- UseCase methods are entity-specific (exported to service layer)
- Repo methods are generic (internal to biz layer)
</naming_rules>
