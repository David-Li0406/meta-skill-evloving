# Naming Conventions

Strict naming rules for go-kratos repository implementations.

## Structs

**Repository struct:**
- Name: `<entity>Repo` (camelCase, unexported)
- Example: `symbolRepo`, `userRepo`, `productRepo`

**Constructor:**
- Name: `New<Entity>Repo` (PascalCase, exported)
- Example: `NewSymbolRepo`, `NewUserRepo`, `NewProductRepo`
- Signature: `func New<Entity>Repo(db *gorm.DB, tx common.Transaction, logger log.Logger) biz.<Entity>Repo`

## Fields

**Database field:**
- Name: `db` (lowercase, exactly 3 characters)
- Type: `*gorm.DB`
- NOT: `database`, `gormDB`, `dbConn`, etc.

**Transaction field:**
- Name: `tx` (lowercase, exactly 2 characters)
- Type: `common.Transaction`
- NOT: `transaction`, `txManager`, `trans`, etc.

**Logger field:**
- Name: `log` (lowercase, exactly 3 characters)
- Type: `*log.Helper`
- NOT: `logger`, `l`, `logging`, etc.

## Methods

**Receiver:**
- Always use `r` (single letter, lowercase)
- NOT: `repo`, `this`, `self`, etc.

**CRUD operations:**
- Create: `Create(ctx context.Context, entity *biz.Entity) (*biz.Entity, error)`
- Update: `Update(ctx context.Context, entity *biz.Entity) (*biz.Entity, error)`
- FindByID: `FindByID(ctx context.Context, id int32) (*biz.Entity, error)`
- Delete: `Delete(ctx context.Context, id int32) error`
- List: `List<Entities>(ctx context.Context, options *biz.List<Entities>Options) ([]*biz.Entity, *pagination.PaginationMeta, error)`

## Helper Functions

**Error mapping:**
- Name: `mapGormError` (camelCase, unexported)
- Signature: `func (r *entityRepo) mapGormError(err error) error`

**Duplicate check:**
- Name: `isDuplicateKeyError` (camelCase, unexported)
- Signature: `func (r *entityRepo) isDuplicateKeyError(err error) bool`

**Data transformers:**
- To domain: `toDomain<Entity>` (camelCase with PascalCase entity, unexported)
- To entity: `toEntity<Entity>` (camelCase with PascalCase entity, unexported)
- Examples: `toDomainSymbol`, `toEntityUser`, `toDomainProduct`

## Parameter Names

**Context:**
- Always `ctx` (NOT: `context`, `c`, etc.)

**Entities:**
- Single entity parameter: Use first letter of entity name (e.g., `s` for Symbol, `u` for User)
- Result variables: Use full lowercase entity name (e.g., `symbol`, `user`)

**IDs:**
- Always `id` (NOT: `ID`, `entityId`, `recordId`)

**Errors:**
- Always `err` (NOT: `error`, `e`)

## Package Declaration

- Always `package repo`
- Repository files live in `internal/data/repo/` directory
- One file per entity: `<entity_lowercase>.go`
- Example: `symbol.go`, `user.go`, `product.go`
