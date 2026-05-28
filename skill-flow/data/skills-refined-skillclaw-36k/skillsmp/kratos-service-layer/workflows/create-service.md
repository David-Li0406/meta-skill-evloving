# Workflow: Create Service Handlers

<required_reading>
**Read NOW:**
1. references/handler-pattern.md
2. references/service-structure.md
</required_reading>

<process>
## Step 1: Gather Requirements

Ask user for:
- **Entity name** (must match proto service name)
- **Proto package** (e.g., "symbolsv1", "v1")
- Confirm use case exists in biz layer

## Step 2: Create Service File

Create `internal/service/{entity}.go`:

```go
package service

import (
	"context"
	pb "{service-name}/contracts/{proto-package}"
	"{service-name}/internal/biz"
)

// {Entity}Service implements {Entity}ServiceServer.
type {Entity}Service struct {
	pb.Unimplemented{Entity}ServiceServer
	uc biz.{Entity}UseCase
}

// New{Entity}Service creates a new {Entity}Service.
func New{Entity}Service(uc biz.{Entity}UseCase) *{Entity}Service {
	return &{Entity}Service{uc: uc}
}

// Create{Entity} handles creation requests.
func (s *{Entity}Service) Create{Entity}(ctx context.Context, in *pb.Create{Entity}Request) (*pb.Create{Entity}Response, error) {
	entity := {Entity}FromCreateRequest(in)
	result, err := s.uc.Create{Entity}(ctx, entity)
	if err != nil {
		return nil, toServiceError(err)
	}
	return &pb.Create{Entity}Response{{Entity}: toProto{Entity}(result)}, nil
}

// Get{Entity}, Update{Entity}, Delete{Entity}, List{Entities} - similar pattern
```

## Step 3: Create Mapper Functions

Add to `internal/service/mapper.go` or create `internal/service/{entity}_mapper.go`:

```go
// {Entity}FromCreateRequest maps proto request to business model.
func {Entity}FromCreateRequest(req *pb.Create{Entity}Request) *biz.{Entity} {
	return &biz.{Entity}{
		// Map fields from req to business model
	}
}

// toProto{Entity} maps business model to proto response.
func toProto{Entity}(e *biz.{Entity}) *pb.{Entity} {
	return &pb.{Entity}{
		Id: e.ID,
		// Map other fields
	}
}
```

## Step 4: Update ProviderSet

Add constructor to `internal/service/service.go`:

```go
var ProviderSet = wire.NewSet(
	// ... existing
	New{Entity}Service,
)
```

## Step 5: Register Service

Add to `internal/server/grpc.go`:

```go
pb.Register{Entity}ServiceServer(srv, service.New{Entity}Service(...))
```

## Step 6: Remind User

- Run `make generate`
- Implement mapper functions for all fields
- Add error mapping in toServiceError
</process>

<success_criteria>
- [ ] Service file created with all handlers
- [ ] Mapper functions defined
- [ ] Constructor added to ProviderSet
- [ ] Handlers use mappers (not direct proto access)
- [ ] Errors mapped with toServiceError
- [ ] Godoc comments on all exports
</success_criteria>