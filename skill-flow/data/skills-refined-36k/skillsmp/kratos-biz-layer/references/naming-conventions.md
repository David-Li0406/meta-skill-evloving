# Naming Conventions

<file_naming>
## File Names

- Use case: `internal/biz/{entity}.go` (singular, lowercase)
- Tests: `internal/biz/{entity}_test.go`
- Interfaces: `internal/biz/interfaces.go` (shared file)
- Models: `internal/biz/models.go` (shared file)
- Provider: `internal/biz/biz.go` (Wire ProviderSet)

**Examples**:
- `symbol.go`, `product.go`, `user.go`
- `symbol_test.go`, `product_test.go`
</file_naming>

<type_naming>
## Type Names

**Interfaces** (exported):
- UseCase: `{Entity}UseCase` (e.g., `SymbolUseCase`)
- Repo: `{Entity}Repo` (e.g., `SymbolRepo`)

**Structs** (unexported):
- UseCase impl: `{entity}UseCase` (e.g., `symbolUseCase`)

**Models** (exported):
- Entity: `{Entity}` (e.g., `Symbol`)
- Options: `List{Entities}Options` (e.g., `ListSymbolsOptions`)

**Errors** (exported):
- `Err{Entity}NotFound` (e.g., `ErrSymbolNotFound`)
- `ErrDuplicate{Entity}` (e.g., `ErrDuplicateSymbol`)
</type_naming>

<function_naming>
## Function Names

**Constructors**:
- `New{Entity}UseCase` (returns interface)

**Methods** (UseCase):
- `Get{Entity}` - Retrieve by ID
- `Create{Entity}` - Create new
- `Update{Entity}` - Update existing
- `Delete{Entity}` - Delete by ID
- `List{Entities}` - List with pagination (plural!)

**Methods** (Repo):
- `Create` - No entity prefix
- `FindByID` - Not `Get`
- `Update` - No entity prefix
- `Delete` - No entity prefix
- `List{Entities}` - With entity prefix (plural!)
</function_naming>

<variable_naming>
## Variable Names

**Receiver**: `uc` (use case)

**Parameters**:
```go
ctx        context.Context
id         uint64
e, p, u    *Entity (first letter of entity)
options    *ListOptions
```

**Return values**:
```go
symbol, err := ...
symbols, meta, err := ...  // For list operations
```
</variable_naming>

<import_ordering>
## Import Ordering

```go
import (
	"context"
	"errors"
	"fmt"
	"{service-name}/internal/data/common"

	"github.com/go-kratos/kratos/v2/log"
	"github.com/go-playground/validator/v10"
	"brizy-go-platform/pagination"
)
```

**Order**:
1. Standard library
2. Internal packages
3. Third-party packages
</import_ordering>