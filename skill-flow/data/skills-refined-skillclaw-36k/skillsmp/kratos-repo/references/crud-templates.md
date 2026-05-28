# CRUD Operation Templates

Complete code templates for all CRUD operations in go-kratos repositories.

## Create Template

```go
func (r *<entity>Repo) Create(ctx context.Context, s *biz.<Entity>) (*biz.<Entity>, error) {
    // Begin transaction
    tx := r.db.WithContext(ctx).Begin()
    defer func() {
        if r := recover(); r != nil {
            tx.Rollback()
        }
    }()

    entity := toEntity<Entity>(s)

    // Create entity
    if err := tx.Session(&gorm.Session{FullSaveAssociations: true}).Create(entity).Error; err != nil {
        tx.Rollback()
        r.log.WithContext(ctx).Errorf("Failed to save <entity>: %v", err)
        return nil, r.mapGormError(err)
    }

    // Commit transaction
    if err := tx.Commit().Error; err != nil {
        r.log.WithContext(ctx).Errorf("Failed to commit transaction: %v", err)
        return nil, r.mapGormError(err)
    }

    return toDomain<Entity>(entity), nil
}
```

## Update Template

```go
func (r *<entity>Repo) Update(ctx context.Context, entity *biz.<Entity>) (*biz.<Entity>, error) {
    // Begin transaction
    tx := r.db.WithContext(ctx).Begin()
    defer func() {
        if r := recover(); r != nil {
            tx.Rollback()
        }
    }()

    // Transform to entity
    e := toEntity<Entity>(entity)

    // Update entity
    result := tx.Session(&gorm.Session{FullSaveAssociations: true}).Model(&model.<Entity>{}).Where("id = ?", entity.Id).Updates(e)
    if result.Error != nil {
        tx.Rollback()
        r.log.WithContext(ctx).Errorf("Failed to update <entity>: %v", result.Error)
        return nil, r.mapGormError(result.Error)
    }
    if result.RowsAffected == 0 {
        r.log.WithContext(ctx).Errorf("Failed to update <entity>: 0 rows affected")
        tx.Rollback()
        return biz.ErrNotFound
    }

    // Commit transaction
    if err := tx.Commit().Error; err != nil {
        r.log.WithContext(ctx).Errorf("Failed to commit transaction: %v", err)
        return nil, r.mapGormError(err)
    }

    // Fetch updated entity with preloaded data
    return r.FindByID(ctx, entity.Id)
}
```

## FindByID Template

```go
func (r *<entity>Repo) FindByID(ctx context.Context, id int32) (*biz.<Entity>, error) {
    var entity *model.<Entity>

    err := r.db.WithContext(ctx).
        Preload("<RelationshipName>").  // Add for each relationship
        Where("id = ?", id).
        First(&entity).Error

    if err != nil {
        r.log.WithContext(ctx).Errorf("Failed to find <entity> by ID %d: %v", id, err)
        return nil, r.mapGormError(err)
    }

    return toDomain<Entity>(entity), nil
}
```

## Delete Template

```go
func (r *<entity>Repo) Delete(ctx context.Context, id int32) error {
    // Begin transaction
    tx := r.db.WithContext(ctx).Begin()
    defer func() {
        if r := recover(); r != nil {
            tx.Rollback()
        }
    }()

    // Delete entity
    result := tx.Where("id = ?", id).Delete(&model.<Entity>{})
    if err := result.Error; err != nil {
        tx.Rollback()
        r.log.WithContext(ctx).Errorf("Failed to delete <entity>: %v", err)
        return r.mapGormError(err)
    }

    if result.RowsAffected == 0 {
        r.log.WithContext(ctx).Errorf("Failed to delete <entity>: 0 rows affected")
        tx.Rollback()
        return biz.ErrNotFound
    }

    // Commit transaction
    if err := tx.Commit().Error; err != nil {
        r.log.WithContext(ctx).Errorf("Failed to commit delete transaction: %v", err)
        return r.mapGormError(err)
    }

    return nil
}
```

## List with Pagination Template

```go
func (r *<entity>Repo) List<Entities>(ctx context.Context, options *biz.List<Entities>Options) ([]*biz.<Entity>, *pagination.PaginationMeta, error) {
    var entities []*model.<Entity>
    var totalCount int64

    // Base query with filters
    baseQuery := r.db.WithContext(ctx).Model(&model.<Entity>{}).Where("<filter_field> = ?", options.FilterValue)

    // Execute count query for total_count
    if err := baseQuery.Count(&totalCount).Error; err != nil {
        r.log.WithContext(ctx).Errorf("Failed to count <entities>: %v", err)
        return nil, nil, r.mapGormError(err)
    }

    // Execute data query with pagination
    query := baseQuery.
        Order("id ASC").                        // Default ordering by ID
        Limit(int(options.Pagination.Limit)).   // Limit results
        Offset(int(options.Pagination.Offset)). // Skip offset records
        Preload("<RelationshipName>")           // Eagerly load relationships if needed

    if err := query.Find(&entities).Error; err != nil {
        r.log.WithContext(ctx).Errorf("Failed to list <entities>: %v", err)
        return nil, nil, r.mapGormError(err)
    }

    // Transform entities to domain objects
    domainEntities := make([]*biz.<Entity>, 0, len(entities))
    for _, entity := range entities {
        domainEntities = append(domainEntities, toDomain<Entity>(entity))
    }

    // Calculate pagination metadata
    meta := &pagination.PaginationMeta{
        TotalCount:      int32(totalCount),
        Offset:          options.Pagination.Offset,
        Limit:           options.Pagination.Limit,
        HasNextPage:     options.Pagination.Offset+int32(len(entities)) < int32(totalCount),
        HasPreviousPage: options.Pagination.Offset > 0,
    }

    return domainEntities, meta, nil
}
```

## Data Transformation Templates

```go
func toDomain<Entity>(e *model.<Entity>) *biz.<Entity> {
    if e == nil {
        return nil
    }

    d := &biz.<Entity>{
        Id:      e.ID,
        Field1:  e.Field1,
        Field2:  e.Field2,
        // ... map all fields
    }

    // Handle nested relationships
    if e.RelatedEntity != nil {
        d.RelatedEntity = &biz.RelatedEntity{
            Id:    e.RelatedEntity.ID,
            Field: e.RelatedEntity.Field,
        }
    }

    return d
}

func toEntity<Entity>(d *biz.<Entity>) *model.<Entity> {
    if d == nil {
        return nil
    }

    e := &model.<Entity>{
        ID:     d.Id,
        Field1: d.Field1,
        Field2: d.Field2,
        // ... map all fields
    }

    // Handle nested relationships
    if d.RelatedEntity != nil {
        e.RelatedEntity = &model.RelatedEntity{
            ID:    d.RelatedEntity.Id,
            Field: d.RelatedEntity.Field,
        }
    }

    return e
}
```
