# Error Handling Patterns

Comprehensive error handling reference for go-kratos repositories.

## Error Mapping Function

Every repository MUST implement `mapGormError()` to translate database errors to business errors:

```go
// mapGormError translates GORM errors to data layer errors
func (r *entityRepo) mapGormError(err error) error {
    if err == nil {
        return nil
    }

    // Check for GORM-specific errors
    if errors.Is(err, gorm.ErrRecordNotFound) {
        return biz.ErrNotFound
    }

    // Check for duplicate key constraint violations
    if r.isDuplicateKeyError(err) {
        return biz.ErrDuplicateEntry
    }

    // Wrap other database errors
    return biz.ErrDatabase
}

// isDuplicateKeyError checks if error is a duplicate key violation
func (r *entityRepo) isDuplicateKeyError(err error) bool {
    errMsg := err.Error()
    return strings.Contains(errMsg, "Error 1062") ||
        strings.Contains(errMsg, "Duplicate entry")
}
```

## Error Mapping Rules

**GORM Errors:**
- `gorm.ErrRecordNotFound` → `biz.ErrNotFound`
- Always use `errors.Is()` for GORM error checks

**MySQL Errors:**
- "Error 1062" (Duplicate entry) → `biz.ErrDuplicateEntry`
- Use string matching for MySQL-specific errors

**Other Errors:**
- All other errors → `biz.ErrDatabase`

## Error Logging Pattern

Every error MUST be logged before returning:

```go
if err != nil {
    r.log.WithContext(ctx).Errorf("Failed to <operation> <entity>: %v", err)
    return nil, r.mapGormError(err)
}
```

**Key points:**
- Use `r.log.WithContext(ctx)` to include request context
- Use `Errorf()` with formatted message
- Include operation name and entity type
- Include error value with `%v`
- Always map through `mapGormError()` before returning

## RowsAffected Checks

Update and Delete operations MUST check for zero rows affected:

```go
result := tx.Where("id = ?", id).Delete(&model.Entity{})
if err := result.Error; err != nil {
    tx.Rollback()
    r.log.WithContext(ctx).Errorf("Failed to delete entity: %v", err)
    return r.mapGormError(err)
}

if result.RowsAffected == 0 {
    r.log.WithContext(ctx).Errorf("Failed to delete entity: 0 rows affected")
    tx.Rollback()
    return biz.ErrNotFound
}
```

**When to check:**
- Update operations: Return `biz.ErrNotFound` if no rows updated
- Delete operations: Return `biz.ErrNotFound` if no rows deleted
- Create operations: No check needed (would error if failed)

## Transaction Rollback on Error

All write operations must rollback on error:

```go
if err := tx.Create(entity).Error; err != nil {
    tx.Rollback()  // Rollback transaction
    r.log.WithContext(ctx).Errorf("Failed to save entity: %v", err)
    return nil, r.mapGormError(err)
}
```

**Pattern:**
1. Check for error
2. Rollback transaction
3. Log error with context
4. Return mapped error
