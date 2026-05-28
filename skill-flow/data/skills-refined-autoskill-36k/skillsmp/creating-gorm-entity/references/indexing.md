# Indexing Patterns

Detailed reference for creating single and composite indexes in GORM entities.

## Composite Indexes

When you need multiple fields indexed together:

```go
ProjectID uint64 `gorm:"not null;uniqueIndex:idx_project_uid,priority:1;index:idx_project_id,priority:1"`
UID       string `gorm:"not null;size:255;uniqueIndex:idx_project_uid,priority:2"`
```

Same index name with different priorities creates composite index. Can have both unique and non-unique composite indexes on same field.

## Single Indexes

```go
ID        uint64         `gorm:"primaryKey;autoIncrement;index:idx_project_id,priority:2"`
DeletedAt gorm.DeletedAt `gorm:"index"`
```

Simple index tag without priority for single-column indexes.

## Unique Indexes

**Single field**: `uniqueIndex`
**Composite**: `uniqueIndex:idx_name,priority:N`

Examples:
```go
Email string `gorm:"not null;size:255;uniqueIndex" json:"email"`
UID   string `gorm:"not null;size:255;uniqueIndex:idx_project_uid,priority:2" json:"uid"`
```
