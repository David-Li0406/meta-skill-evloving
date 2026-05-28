---
name: go-database
description: >
  Database patterns including repository, query building, and pagination.
  Use when working with SQL, repositories, or database operations.
  Triggers: repository.go, *sql.DB, *sql.Tx, ProjectionMap, query.Builder,
  PageRequest, PageResult, ScanFunc, WithTx, QueryOne, QueryMany, migrations,
  mapping.go, scanProvider, cross-domain dependencies.
  File patterns: internal/*/repository.go, internal/*/mapping.go,
  pkg/query/*.go, pkg/pagination/*.go, pkg/repository/*.go
---

# Go Database Patterns

## When This Skill Applies

- Implementing repository methods
- Building SQL queries with filters/pagination
- Creating domain scanners
- Managing transactions
- Setting up cross-domain dependencies

## Principles

### 1. Three-Layer Query Architecture

**Layer 1: ProjectionMap** (Structure Definition)
```go
var providerProjection = query.NewProjectionMap("public", "providers", "p").
    Project("id", "ID").
    Project("name", "Name").
    Project("config", "Config").
    Project("created_at", "CreatedAt").
    Project("updated_at", "UpdatedAt")
```

**Layer 2: Builder** (Operations)
```go
qb := query.NewBuilder(providerProjection, query.SortField{Field: "Name"}).
    WhereContains("Name", req.Name).
    WhereSearch(req.Search, "Name", "Config")

if len(req.Sort) > 0 {
    qb.OrderByFields(req.Sort)
}

countSQL, countArgs := qb.BuildCount()
pageSQL, pageArgs := qb.BuildPage(req.Page, req.PageSize)
```

**Layer 3: Execution**
```go
var total int
err := db.QueryRowContext(ctx, countSQL, countArgs...).Scan(&total)

rows, err := db.QueryContext(ctx, pageSQL, pageArgs...)
```

### 2. Domain Scanner Pattern

Each domain defines a scanner function in `mapping.go`:

```go
// internal/providers/mapping.go
func scanProvider(s repository.Scanner) (Provider, error) {
    var p Provider
    err := s.Scan(&p.ID, &p.Name, &p.Config, &p.CreatedAt, &p.UpdatedAt)
    return p, err
}
```

### 3. Transaction Pattern

Commands use `repository.WithTx` for automatic transaction management:

```go
func (r *repo) Create(ctx context.Context, cmd CreateCommand) (*Provider, error) {
    q := `INSERT INTO providers (name, config) VALUES ($1, $2)
          RETURNING id, name, config, created_at, updated_at`

    p, err := repository.WithTx(ctx, r.db, func(tx *sql.Tx) (Provider, error) {
        return repository.QueryOne(ctx, tx, q, []any{cmd.Name, cmd.Config}, scanProvider)
    })

    if err != nil {
        return nil, repository.MapError(err, ErrNotFound, ErrDuplicate)
    }

    return &p, nil
}
```

### 4. Query Pattern (No Transaction)

Read operations use repository helpers without transactions:

```go
func (r *repo) FindByID(ctx context.Context, id uuid.UUID) (*Provider, error) {
    q, args := query.NewBuilder(projection).BuildSingle("ID", id)

    p, err := repository.QueryOne(ctx, r.db, q, args, scanProvider)
    if err != nil {
        return nil, repository.MapError(err, ErrNotFound, ErrDuplicate)
    }

    return &p, nil
}
```

### 5. Pagination

**Request/Response Types**:
```go
type PageRequest struct {
    Page     int               `json:"page"`
    PageSize int               `json:"page_size"`
    Search   *string           `json:"search,omitempty"`
    Sort     []query.SortField `json:"sort,omitempty"`
}

type PageResult[T any] struct {
    Data       []T `json:"data"`
    Total      int `json:"total"`
    Page       int `json:"page"`
    PageSize   int `json:"page_size"`
    TotalPages int `json:"total_pages"`
}
```

**Parse from URL**:
```go
// Supports: page, page_size, search, sort (comma-separated, "-" prefix for desc)
pageReq := pagination.PageRequestFromQuery(r.URL.Query(), h.pagination)
```

### 6. Repository Helpers

```go
// QueryOne executes a query expecting a single row
func QueryOne[T any](ctx context.Context, q Querier, query string, args []any, scan ScanFunc[T]) (T, error)

// QueryMany executes a query expecting multiple rows
func QueryMany[T any](ctx context.Context, q Querier, query string, args []any, scan ScanFunc[T]) ([]T, error)

// WithTx executes fn within a transaction, handling Begin/Commit/Rollback
func WithTx[T any](ctx context.Context, db *sql.DB, fn func(tx *sql.Tx) (T, error)) (T, error)

// MapError translates database errors to domain errors
func MapError(err error, notFoundErr, duplicateErr error) error
```

### 7. Cross-Domain Dependencies

Domain systems can depend on other domains. Dependencies must be unidirectional.

```go
// images depends on documents (unidirectional)
func New(
    docs documents.System,  // Domain dependencies first
    db *sql.DB,             // Then runtime dependencies
    storage storage.System,
    logger *slog.Logger,
    pagination pagination.Config,
) System {
    return &repo{...}
}
```

**Rules**:
- Domain dependencies listed before runtime dependencies
- Dependencies flow one direction only (A → B, never B → A)
- Inject via constructor, not method parameters
- Use interface types to avoid import cycles
- Wire at server startup in `cmd/server/domain.go`

## Patterns

### List with Pagination

```go
func (r *repo) List(ctx context.Context, page pagination.PageRequest, filters Filters) (*pagination.PageResult[Provider], error) {
    qb := query.NewBuilder(projection, query.SortField{Field: "Name"})
    filters.Apply(qb)

    if len(page.Sort) > 0 {
        qb.OrderByFields(page.Sort)
    }

    countSQL, countArgs := qb.BuildCount()
    var total int
    if err := r.db.QueryRowContext(ctx, countSQL, countArgs...).Scan(&total); err != nil {
        return nil, fmt.Errorf("count: %w", err)
    }

    pageSQL, pageArgs := qb.BuildPage(page.Page, page.PageSize)
    items, err := repository.QueryMany(ctx, r.db, pageSQL, pageArgs, scanProvider)
    if err != nil {
        return nil, fmt.Errorf("query: %w", err)
    }

    result := pagination.NewPageResult(items, total, page.Page, page.PageSize)
    return &result, nil
}
```

### Domain Filters

```go
type Filters struct {
    Name   *string
    Search *string
}

func (f *Filters) Apply(qb *query.Builder) {
    qb.WhereContains("Name", f.Name)
    qb.WhereSearch(f.Search, "Name", "Config")
}
```

## Anti-Patterns

### Manual Transaction Management

```go
// Bad: Manual begin/commit/rollback
tx, _ := db.Begin()
_, err := tx.Exec(...)
if err != nil {
    tx.Rollback()
    return err
}
tx.Commit()

// Good: Use repository.WithTx
result, err := repository.WithTx(ctx, db, func(tx *sql.Tx) (T, error) {
    return tx.Exec(...)
})
```

### Inline SQL Building

```go
// Bad: String concatenation
sql := "SELECT * FROM providers WHERE name = '" + name + "'"

// Good: Parameterized queries via Builder
q, args := query.NewBuilder(projection).
    WhereEquals("Name", name).
    BuildSingle("Name", name)
```
