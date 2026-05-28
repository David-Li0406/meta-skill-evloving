# Use Case Pattern

<overview>
Use cases are the heart of the business layer. They orchestrate business logic, coordinate between repositories, handle validation, and manage errors.
</overview>

<struct_pattern>
## Use Case Struct

**Standard structure**:
```go
type {entity}UseCase struct {
	repo      {Entity}Repo          // Repository interface
	log       *log.Helper            // Structured logger
	validator *validator.Validate    // Validator instance
	tm        common.Transaction     // Transaction manager
}
```

**Field naming**:
- `repo` - single repository (lowercase)
- `repos` - multiple repositories (rare, prefer composition)
- `log` - always `*log.Helper`
- `validator` - always `*validator.Validate`
- `tm` - transaction manager

**Struct naming**: `{entity}UseCase` (camelCase, unexported)
</struct_pattern>

<constructor_pattern>
## Constructor Function

**Standard signature**:
```go
func New{Entity}UseCase(
	repo {Entity}Repo,
	validator *validator.Validate,
	tm common.Transaction,
	logger log.Logger,
) {Entity}UseCase {  // Returns interface, not struct
	return &{entity}UseCase{
		repo:      repo,
		validator: validator,
		tm:        tm,
		log:       log.NewHelper(logger),
	}
}
```

**Key patterns**:
- Accept `log.Logger`, wrap as `log.NewHelper(logger)`
- Return **interface type**, not pointer to struct
- Parameters in order: repo, validator, tm, logger
- Function name: `New{Entity}UseCase` (PascalCase)
</constructor_pattern>

<method_pattern>
## Use Case Methods

**Method signature**:
```go
func (uc *{entity}UseCase) Create{Entity}(ctx context.Context, e *{Entity}) (*{Entity}, error)
```

**Standard flow**:
1. Validate input with validator
2. Call repository method
3. Handle errors with logging
4. Map repository errors to business errors
5. Return result

**Example**:
```go
func (uc *{entity}UseCase) Create{Entity}(ctx context.Context, e *{Entity}) (*{Entity}, error) {
	// 1. Validate
	if err := uc.validator.Struct(e); err != nil {
		return nil, fmt.Errorf("%w: %v", ErrValidationFailed, err)
	}

	// 2. Call repository
	{entity}, err := uc.repo.Create(ctx, e)
	if err != nil {
		// 3. Log error
		uc.log.WithContext(ctx).Errorf("Create error: %v", err)

		// 4. Map to business error
		if errors.Is(err, ErrDuplicateEntry) {
			return nil, ErrDuplicate{Entity}
		}

		return nil, ErrDatabaseOperation
	}

	// 5. Return result
	return {entity}, nil
}
```
</method_pattern>

<error_handling>
## Error Handling Pattern

**Define business errors** at top of file:
```go
var (
	Err{Entity}NotFound    = errors.New("{entity} not found")
	ErrDuplicate{Entity}   = errors.New("{entity} already exists")
)
```

**Map repository errors to business errors**:
```go
if err != nil {
	uc.log.WithContext(ctx).Errorf("Operation error: %v", err)

	// Specific error mapping
	if errors.Is(err, ErrNotFound) {
		return nil, Err{Entity}NotFound
	}

	if errors.Is(err, ErrDuplicateEntry) {
		return nil, ErrDuplicate{Entity}
	}

	// Generic fallback
	return nil, ErrDatabaseOperation
}
```

**Never expose repository errors directly** - always wrap or map them.
</error_handling>

<logging_pattern>
## Logging Pattern

**Use WithContext** for request tracing:
```go
uc.log.WithContext(ctx).Errorf("Create error: %v", err)
uc.log.WithContext(ctx).Infof("Created {entity} %d", {entity}.ID)
```

**Log levels**:
- `Errorf` - Errors that prevent operation completion
- `Warnf` - Recoverable issues or unexpected states
- `Infof` - Important business events
- `Debugf` - Detailed debugging information

**What to log**:
- ✅ Repository errors with context
- ✅ Validation failures (at debug level)
- ✅ Business rule violations
- ❌ Successful operations (creates noise)
- ❌ Sensitive data (passwords, tokens)
</logging_pattern>

<validation_pattern>
## Validation Pattern

**Validate before repository calls**:
```go
// Validate domain model
if err := uc.validator.Struct(e); err != nil {
	return nil, fmt.Errorf("%w: %v", ErrValidationFailed, err)
}
```

**Validate options/parameters**:
```go
// Validate list options
if err := uc.validator.Struct(options); err != nil {
	return nil, nil, fmt.Errorf("%w: %v", ErrValidationFailed, err)
}
```

**Don't re-validate** if data comes from trusted source (e.g., Get after Create).
</validation_pattern>

<transaction_pattern>
## Transaction Pattern

**For multi-repository operations**:
```go
func (uc *{entity}UseCase) ComplexOperation(ctx context.Context, data *Data) error {
	return uc.tm.InTx(ctx, func(ctx context.Context) error {
		// Multiple repository calls
		if err := uc.repo1.Create(ctx, item1); err != nil {
			return err  // Transaction will rollback
		}

		if err := uc.repo2.Update(ctx, item2); err != nil {
			return err  // Transaction will rollback
		}

		return nil  // Transaction will commit
	})
}
```

**When to use transactions**:
- Multiple related repository operations
- Operations that must succeed or fail together
- Complex business workflows

**When NOT to use transactions**:
- Single repository call
- Read-only operations
- Independent operations
</transaction_pattern>

<godoc_pattern>
## Documentation Pattern

**Constructor**:
```go
// New{Entity}UseCase creates a new {Entity}UseCase instance.
func New{Entity}UseCase(...) {Entity}UseCase
```

**Methods** (match interface comments):
```go
// Create{Entity} creates a new {Entity}.
func (uc *{entity}UseCase) Create{Entity}(ctx context.Context, e *{Entity}) (*{Entity}, error)
```

**Struct** (optional but recommended):
```go
// {entity}UseCase implements {Entity}UseCase interface.
type {entity}UseCase struct {
	...
}
```
</godoc_pattern>

<complete_example>
## Complete Use Case Example

```go
package biz

import (
	"context"
	"errors"
	"fmt"
	"symbol-service/internal/data/common"

	"github.com/go-kratos/kratos/v2/log"
	"github.com/go-playground/validator/v10"
	"brizy-go-platform/pagination"
)

// Business errors
var (
	ErrProductNotFound    = errors.New("product not found")
	ErrDuplicateProduct   = errors.New("product already exists")
)

// productUseCase implements ProductUseCase interface.
type productUseCase struct {
	repo      ProductRepo
	log       *log.Helper
	validator *validator.Validate
	tm        common.Transaction
}

// NewProductUseCase creates a new ProductUseCase instance.
func NewProductUseCase(repo ProductRepo, validator *validator.Validate, tm common.Transaction, logger log.Logger) ProductUseCase {
	return &productUseCase{
		repo:      repo,
		validator: validator,
		tm:        tm,
		log:       log.NewHelper(logger),
	}
}

// GetProduct retrieves a Product by its ID.
func (uc *productUseCase) GetProduct(ctx context.Context, id uint64) (*Product, error) {
	product, err := uc.repo.FindByID(ctx, id)
	if err != nil {
		uc.log.WithContext(ctx).Errorf("FindByID error: %v", err)

		if errors.Is(err, ErrNotFound) {
			return nil, ErrProductNotFound
		}

		return nil, ErrDatabaseOperation
	}

	return product, nil
}

// CreateProduct creates a new Product.
func (uc *productUseCase) CreateProduct(ctx context.Context, p *Product) (*Product, error) {
	// Validate domain model
	if err := uc.validator.Struct(p); err != nil {
		return nil, fmt.Errorf("%w: %v", ErrValidationFailed, err)
	}

	product, err := uc.repo.Create(ctx, p)
	if err != nil {
		uc.log.WithContext(ctx).Errorf("Create error: %v", err)

		if errors.Is(err, ErrDuplicateEntry) {
			return nil, ErrDuplicateProduct
		}

		return nil, ErrDatabaseOperation
	}

	return product, nil
}

// Additional methods: UpdateProduct, DeleteProduct, ListProducts...
```
</complete_example>