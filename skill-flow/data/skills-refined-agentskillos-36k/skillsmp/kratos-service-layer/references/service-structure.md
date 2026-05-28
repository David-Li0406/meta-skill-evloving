# Service Structure

<service_struct>
```go
type {Entity}Service struct {
	pb.Unimplemented{Entity}ServiceServer  // Required: embed unimplemented
	uc biz.{Entity}UseCase                // Use case dependency
}
```
</service_struct>

<constructor>
```go
func New{Entity}Service(uc biz.{Entity}UseCase) *{Entity}Service {
	return &{Entity}Service{uc: uc}
}
```
</constructor>

<file_organization>
- `internal/service/{entity}.go` - Handlers
- `internal/service/mapper.go` or `{entity}_mapper.go` - Mappers
- `internal/service/service.go` - ProviderSet
</file_organization>

<imports>
```go
import (
	"context"
	"errors"

	pb "{service-name}/contracts/{proto-package}"
	"{service-name}/internal/biz"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)
```
</imports>