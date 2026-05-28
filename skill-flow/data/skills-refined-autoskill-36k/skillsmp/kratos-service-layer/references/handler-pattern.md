# Handler Pattern

<basic_handler>
```go
func (s *{Entity}Service) Create{Entity}(ctx context.Context, in *pb.Create{Entity}Request) (*pb.Create{Entity}Response, error) {
	// 1. Map request → business model
	entity := {Entity}FromCreateRequest(in)

	// 2. Call use case
	result, err := s.uc.Create{Entity}(ctx, entity)
	if err != nil {
		return nil, toServiceError(err)  // Map error
	}

	// 3. Map result → response
	return &pb.Create{Entity}Response{{Entity}: toProto{Entity}(result)}, nil
}
```
</basic_handler>

<list_handler>
```go
func (s *{Entity}Service) List{Entities}(ctx context.Context, in *pb.List{Entities}Request) (*pb.List{Entities}Response, error) {
	options := NewList{Entities}Options(in)

	entities, meta, err := s.uc.List{Entities}(ctx, options)
	if err != nil {
		return nil, toServiceError(err)
	}

	return &pb.List{Entities}Response{
		{Entities}: toProto{Entities}(entities),
		Meta:     toProtoPaginationMeta(meta),
	}, nil
}
```
</list_handler>

<error_mapping>
```go
func toServiceError(err error) error {
	switch {
	case errors.Is(err, biz.Err{Entity}NotFound):
		return status.Error(codes.NotFound, err.Error())
	case errors.Is(err, biz.ErrValidationFailed):
		return status.Error(codes.InvalidArgument, err.Error())
	case errors.Is(err, biz.ErrDuplicate{Entity}):
		return status.Error(codes.AlreadyExists, err.Error())
	default:
		return status.Error(codes.Internal, "internal error")
	}
}
```
</error_mapping>