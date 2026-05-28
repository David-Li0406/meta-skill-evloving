# Complete Repository Examples

Full, working repository implementations for reference.

## Minimal Repository (No Pagination)

A basic repository with Create and FindByID operations:

```go
package repo

import (
    "context"
    "errors"
    "strings"
    "user-service/internal/biz"
    "user-service/internal/data/common"
    "user-service/internal/data/model"

    "github.com/go-kratos/kratos/v2/log"
    "gorm.io/gorm"
)

func NewUserRepo(db *gorm.DB, tx common.Transaction, logger log.Logger) biz.UserRepo {
    return &userRepo{
        db:  db,
        tx:  tx,
        log: log.NewHelper(logger),
    }
}

type userRepo struct {
    db  *gorm.DB
    tx  common.Transaction
    log *log.Helper
}

func (r *userRepo) Create(ctx context.Context, u *biz.User) (*biz.User, error) {
    tx := r.db.WithContext(ctx).Begin()
    defer func() {
        if r := recover(); r != nil {
            tx.Rollback()
        }
    }()

    user := toEntityUser(u)

    if err := tx.Create(user).Error; err != nil {
        tx.Rollback()
        r.log.WithContext(ctx).Errorf("Failed to save user: %v", err)
        return nil, r.mapGormError(err)
    }

    if err := tx.Commit().Error; err != nil {
        r.log.WithContext(ctx).Errorf("Failed to commit transaction: %v", err)
        return nil, r.mapGormError(err)
    }

    return toDomainUser(user), nil
}

func (r *userRepo) FindByID(ctx context.Context, id int32) (*biz.User, error) {
    var user *model.User

    err := r.db.WithContext(ctx).
        Where("id = ?", id).
        First(&user).Error

    if err != nil {
        r.log.WithContext(ctx).Errorf("Failed to find user by ID %d: %v", id, err)
        return nil, r.mapGormError(err)
    }

    return toDomainUser(user), nil
}

func (r *userRepo) mapGormError(err error) error {
    if err == nil {
        return nil
    }
    if errors.Is(err, gorm.ErrRecordNotFound) {
        return biz.ErrNotFound
    }
    if r.isDuplicateKeyError(err) {
        return biz.ErrDuplicateEntry
    }
    return biz.ErrDatabase
}

func (r *userRepo) isDuplicateKeyError(err error) bool {
    errMsg := err.Error()
    return strings.Contains(errMsg, "Error 1062") ||
        strings.Contains(errMsg, "Duplicate entry")
}

func toDomainUser(u *model.User) *biz.User {
    if u == nil {
        return nil
    }
    return &biz.User{
        Id:    u.ID,
        Email: u.Email,
        Name:  u.Name,
    }
}

func toEntityUser(u *biz.User) *model.User {
    if u == nil {
        return nil
    }
    return &model.User{
        ID:    u.Id,
        Email: u.Email,
        Name:  u.Name,
    }
}
```

## Repository with Pagination and Nested Relationships

For a complete example with pagination and nested relationships, see:
- **symbol-service/internal/data/repo/symbol.go**

This example includes:
- Full CRUD operations (Create, Update, FindByID, Delete)
- Pagination support in `ListSymbols()` method
- Nested relationship handling (`SymbolData`)
- Transaction management for all write operations
- Complete error handling and mapping
- Data transformation between domain and entity models

Key features demonstrated:
- `ListSymbols()` with `PaginationMeta` calculation
- `Preload("SymbolData")` for eager loading relationships
- `Session(&gorm.Session{FullSaveAssociations: true})` for nested objects
- `RowsAffected` checks for Update and Delete
- Proper transaction rollback on errors