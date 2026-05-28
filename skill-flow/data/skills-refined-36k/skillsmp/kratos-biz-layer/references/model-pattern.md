# Business Model Pattern

<overview>
Business models represent domain entities with validation rules. They're independent of database schema and use validator tags for validation.
</overview>

<basic_model>
## Basic Model Pattern

```go
// {Entity} represents a {entity} in the business domain.
type {Entity} struct {
	ID   uint64 `validate:"omitempty,gte=0"`
	Name string `validate:"required,min=1,max=255"`
	// Additional fields...
}
```

**Field Rules**:
- Use `uint64` for all ID fields
- Required fields: `validate:"required,..."`
- Optional fields: use pointer types + `validate:"omitempty,..."`
- String lengths: always specify `min` and `max`
</basic_model>

<validation_tags>
## Validation Tags

**Common patterns**:
```go
ID        uint64  `validate:"omitempty,gte=0"`              // Optional ID (create)
ProjectID uint64  `validate:"required,gt=0"`                // Required foreign key
Name      string  `validate:"required,min=1,max=255"`       // Required string
Email     *string `validate:"omitempty,email,max=255"`      // Optional email
Status    string  `validate:"required,oneof=active paused"` // Enum
Count     uint32  `validate:"omitempty,gte=0,lte=1000"`     // Bounded number
```

**Validation keywords**:
- `required` - Field must be present
- `omitempty` - Skip validation if empty
- `min`, `max` - String length or numeric bounds
- `gte`, `lte`, `gt`, `lt` - Numeric comparisons
- `email`, `uuid4`, `url` - Format validation
- `oneof` - Enum validation
</validation_tags>

<nested_models>
## Nested Models

```go
type Symbol struct {
	ID     uint64       `validate:"omitempty,gte=0"`
	Data   *SymbolData  `validate:"required"`  // Nested struct
}

type SymbolData struct {
	Project uint64  `validate:"required,gt=0"`
	Content *[]byte `validate:"omitempty"`
}
```

Use pointers for optional nested structs.
</nested_models>

<list_options>
## List Options Pattern

**With pagination**:
```go
// List{Entities}Options contains parameters for listing {entities}
type List{Entities}Options struct {
	ProjectID  uint64                      `validate:"required,gt=0"`
	Status     string                      `validate:"omitempty,oneof=active inactive"`
	Pagination pagination.PaginationParams `validate:"required"`
}
```

**Pagination import**:
```go
import "brizy-go-platform/pagination"
```
</list_options>

<godoc>
## Documentation

```go
// {Entity} represents a {entity} in the business domain.
// It contains... [brief description of purpose and usage]
type {Entity} struct {
	...
}

// List{Entities}Options contains parameters for listing {entities}.
type List{Entities}Options struct {
	...
}
```
</godoc>
