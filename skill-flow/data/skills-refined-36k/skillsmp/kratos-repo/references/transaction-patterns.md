# Transaction Patterns

Detailed reference for handling transactions in go-kratos repositories.

## Write Operations (Create/Update/Delete)

All write operations MUST use explicit transactions with panic recovery:

```go
func (r *entityRepo) Create(ctx context.Context, entity *biz.Entity) (*biz.Entity, error) {
    // Begin transaction
    tx := r.db.WithContext(ctx).Begin()
    defer func() {
        if r := recover(); r != nil {
            tx.Rollback()
        }
    }()

    // ... perform operation ...

    // Commit transaction
    if err := tx.Commit().Error; err != nil {
        r.log.WithContext(ctx).Errorf("Failed to commit transaction: %v", err)
        return nil, r.mapGormError(err)
    }

    return result, nil
}
```

**Key points:**
- Use `r.db.WithContext(ctx).Begin()` to start explicit transaction
- Defer panic recovery with rollback
- Rollback on any error
- Commit at the end
- Always map errors through `r.mapGormError(err)`

## Read Operations (FindByID/List)

Read operations NEVER use transactions:

```go
func (r *entityRepo) FindByID(ctx context.Context, id int32) (*biz.Entity, error) {
    var entity *model.Entity

    err := r.db.WithContext(ctx).
        Where("id = ?", id).
        First(&entity).Error

    if err != nil {
        r.log.WithContext(ctx).Errorf("Failed to find entity by ID %d: %v", id, err)
        return nil, r.mapGormError(err)
    }

    return toDomainEntity(entity), nil
}
```

**Key points:**
- Use `r.db.WithContext(ctx)` directly (no Begin/Commit)
- Use `Preload()` for eager loading relationships
- Always map errors through `r.mapGormError(err)`

## Session Options for Nested Objects

When creating or updating entities with relationships:

```go
tx.Session(&gorm.Session{FullSaveAssociations: true}).Create(entity)
tx.Session(&gorm.Session{FullSaveAssociations: true}).Updates(entity)
```

**When to use:**
- Entity has nested relationships (one-to-one, one-to-many)
- You want GORM to automatically save/update associated entities
- Ensures referential integrity

## Preloading Relationships

For queries that need to eagerly load relationships:

```go
r.db.WithContext(ctx).
    Preload("RelationshipName").
    Preload("AnotherRelationship").
    Where("id = ?", id).
    First(&entity)
```

**Best practices:**
- Only preload what you need (avoid N+1 queries)
- Chain multiple `Preload()` calls for multiple relationships
- Use in both FindByID and List operations
