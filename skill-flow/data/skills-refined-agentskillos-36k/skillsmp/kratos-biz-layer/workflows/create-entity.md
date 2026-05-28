# Workflow: Create New Entity

<required_reading>
**Read these reference files NOW:**
1. references/use-case-pattern.md
2. references/interface-pattern.md
3. references/model-pattern.md
4. references/naming-conventions.md
</required_reading>

<process>
## Step 1: Gather Requirements

Ask the user for:
- **Entity name** (PascalCase, e.g., "Product", "User", "Order")
- **Fields** for the business model with types and validation rules
- **Whether pagination is needed** for List operation
- **Whether transactions are needed** for complex operations

If user provides just entity name, infer standard CRUD needs.

## Step 2: Analyze Existing Patterns

Before generating code:

1. **Read existing biz files** to match coding style:
   ```bash
   # Check existing use case patterns
   find services/*/internal/biz -name "*.go" ! -name "*_test.go" ! -name "biz.go" ! -name "interfaces.go" ! -name "models.go"
   ```

2. **Check for naming conflicts**:
   - Read `internal/biz/interfaces.go` - verify `{Entity}Repo` doesn't exist
   - Read `internal/biz/models.go` - verify `{Entity}` model doesn't exist
   - List `internal/biz/` - verify `{entity}.go` doesn't exist

3. **Identify service name** from project structure:
   ```bash
   pwd | grep -o 'services/[^/]*' | cut -d/ -f2
   ```

## Step 3: Create Business Model

Create model in `internal/biz/models.go`:

```go
// {Entity} represents a {entity} in the business domain.
type {Entity} struct {
	ID       uint64 `validate:"omitempty,gte=0"`
	// Add fields with validation tags
	// Example: Name string `validate:"required,min=1,max=255"`
}
```

**Model Requirements**:
- Use `uint64` for ID fields
- Add `validator` struct tags for all fields
- Use pointer types for optional fields
- Add godoc comment describing the entity

If model file doesn't exist, create it with package declaration:
```go
package biz

import "brizy-go-platform/pagination"
```

## Step 4: Create Repository Interface

Add interface to `internal/biz/interfaces.go`:

```go
// {Entity}UseCase defines business operations for {Entity}.
type {Entity}UseCase interface {
	// Get{Entity} retrieves a {Entity} by its ID.
	Get{Entity}(ctx context.Context, id uint64) (*{Entity}, error)

	// Create{Entity} creates a new {Entity}.
	Create{Entity}(ctx context.Context, e *{Entity}) (*{Entity}, error)

	// Update{Entity} updates an existing {Entity} and returns the updated {Entity}.
	Update{Entity}(ctx context.Context, e *{Entity}) (*{Entity}, error)

	// Delete{Entity} deletes a {Entity} by its ID.
	Delete{Entity}(ctx context.Context, id uint64) error

	// List{Entities} lists {Entities} based on the provided options and returns pagination metadata.
	List{Entities}(ctx context.Context, options *List{Entities}Options) ([]*{Entity}, *pagination.PaginationMeta, error)
}

// {Entity}Repo defines repository operations for {Entity}.
type {Entity}Repo interface {
	// Create saves the given {Entity}.
	Create(context.Context, *{Entity}) (*{Entity}, error)

	// Update updates a {Entity} in the repository.
	Update(context.Context, *{Entity}) (*{Entity}, error)

	// FindByID returns the {Entity} with the given ID from the repository.
	FindByID(context.Context, uint64) (*{Entity}, error)

	// List{Entities} returns a list of {Entities} from the repository with pagination metadata.
	List{Entities}(context.Context, *List{Entities}Options) ([]*{Entity}, *pagination.PaginationMeta, error)

	// Delete removes a {Entity} from the repository by its ID.
	Delete(context.Context, uint64) error
}
```

**If pagination needed**, also add options struct to `models.go`:
```go
// List{Entities}Options contains parameters for listing {entities}
type List{Entities}Options struct {
	// Add filter fields as needed
	Pagination pagination.PaginationParams `validate:"required"`
}
```

## Step 5: Create Use Case Implementation

Create `internal/biz/{entity}.go`:

```go
package biz

import (
	"context"
	"errors"
	"fmt"
	"{service-name}/internal/data/common"

	"github.com/go-kratos/kratos/v2/log"
	"github.com/go-playground/validator/v10"
	"brizy-go-platform/pagination"
)

// Business errors for {Entity}
var (
	Err{Entity}NotFound    = errors.New("{entity} not found")
	ErrDuplicate{Entity}   = errors.New("{entity} already exists")
)

// {entity}UseCase implements {Entity}UseCase interface.
type {entity}UseCase struct {
	repo      {Entity}Repo
	log       *log.Helper
	validator *validator.Validate
	tm        common.Transaction
}

// New{Entity}UseCase creates a new {Entity}UseCase instance.
func New{Entity}UseCase(repo {Entity}Repo, validator *validator.Validate, tm common.Transaction, logger log.Logger) {Entity}UseCase {
	return &{entity}UseCase{
		repo:      repo,
		validator: validator,
		tm:        tm,
		log:       log.NewHelper(logger),
	}
}

// Get{Entity} retrieves a {Entity} by its ID.
func (uc *{entity}UseCase) Get{Entity}(ctx context.Context, id uint64) (*{Entity}, error) {
	{entity}, err := uc.repo.FindByID(ctx, id)
	if err != nil {
		uc.log.WithContext(ctx).Errorf("FindByID error: %v", err)

		if errors.Is(err, ErrNotFound) {
			return nil, Err{Entity}NotFound
		}

		return nil, ErrDatabaseOperation
	}

	return {entity}, nil
}

// Create{Entity} creates a new {Entity}.
func (uc *{entity}UseCase) Create{Entity}(ctx context.Context, e *{Entity}) (*{Entity}, error) {
	// Validate domain model
	if err := uc.validator.Struct(e); err != nil {
		return nil, fmt.Errorf("%w: %v", ErrValidationFailed, err)
	}

	{entity}, err := uc.repo.Create(ctx, e)
	if err != nil {
		uc.log.WithContext(ctx).Errorf("Create error: %v", err)

		if errors.Is(err, ErrDuplicateEntry) {
			return nil, ErrDuplicate{Entity}
		}

		return nil, ErrDatabaseOperation
	}

	return {entity}, nil
}

// Update{Entity} updates an existing {Entity}.
func (uc *{entity}UseCase) Update{Entity}(ctx context.Context, e *{Entity}) (*{Entity}, error) {
	// Validate domain model
	if err := uc.validator.Struct(e); err != nil {
		return nil, fmt.Errorf("%w: %v", ErrValidationFailed, err)
	}

	{entity}, err := uc.repo.Update(ctx, e)
	if err != nil {
		uc.log.WithContext(ctx).Errorf("Update error: %v", err)

		if errors.Is(err, ErrNotFound) {
			return nil, Err{Entity}NotFound
		}

		return nil, ErrDatabaseOperation
	}

	return {entity}, nil
}

// Delete{Entity} deletes a {Entity} by its ID.
func (uc *{entity}UseCase) Delete{Entity}(ctx context.Context, id uint64) error {
	err := uc.repo.Delete(ctx, id)
	if err != nil {
		uc.log.WithContext(ctx).Errorf("Delete error: %v", err)

		if errors.Is(err, ErrNotFound) {
			return Err{Entity}NotFound
		}

		return ErrDatabaseOperation
	}

	return nil
}

// List{Entities} lists {Entities} based on the provided options.
func (uc *{entity}UseCase) List{Entities}(ctx context.Context, options *List{Entities}Options) ([]*{Entity}, *pagination.PaginationMeta, error) {
	// Validate options
	if err := uc.validator.Struct(options); err != nil {
		return nil, nil, fmt.Errorf("%w: %v", ErrValidationFailed, err)
	}

	{entities}, meta, err := uc.repo.List{Entities}(ctx, options)
	if err != nil {
		uc.log.WithContext(ctx).Errorf("List{Entities} error: %v", err)
		return nil, nil, ErrDatabaseOperation
	}

	return {entities}, meta, nil
}
```

## Step 6: Update Wire ProviderSet

Read `internal/biz/biz.go` and add constructor to ProviderSet:

```go
var ProviderSet = wire.NewSet(
	// ... existing providers
	New{Entity}UseCase,  // Add this line
)
```

Maintain alphabetical order if that's the existing pattern.

## Step 7: Generate Tests (if requested)

Create `internal/biz/{entity}_test.go` with table-driven tests for each method.
Use testify/mock for repository mocking.

## Step 8: Final Reminders

Inform the user:

1. **Run Wire code generation**:
   ```bash
   cd services/{service-name}
   make generate
   ```

2. **Next steps**:
   - Create data layer: Use `kratos-repo` skill
   - Create service layer: Use `kratos-service-layer` skill
   - Write tests: Use `kratos-tests` skill

3. **Files created/modified**:
   - Created: `internal/biz/{entity}.go`
   - Modified: `internal/biz/interfaces.go`
   - Modified: `internal/biz/models.go`
   - Modified: `internal/biz/biz.go`
   - Created (if tests): `internal/biz/{entity}_test.go`
</process>

<success_criteria>
Entity creation is complete when:
- [ ] Business model added to models.go with validation tags
- [ ] UseCase and Repo interfaces added to interfaces.go
- [ ] Use case implementation created in {entity}.go
- [ ] Business errors defined (NotFound, Duplicate)
- [ ] All methods have godoc comments
- [ ] Constructor added to ProviderSet in biz.go
- [ ] Error handling wraps repository errors
- [ ] Logging uses WithContext for request tracing
- [ ] Validation happens before repository calls
- [ ] Tests generated (if requested)
- [ ] User reminded to run `make generate`
</success_criteria>