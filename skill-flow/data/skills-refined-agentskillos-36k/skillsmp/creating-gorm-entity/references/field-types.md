# Field Type Guidelines

Detailed reference for choosing and configuring field types in GORM entities.

## Numeric Types

**IDs**: `uint64` (primary keys and foreign keys)
**Versions/Counts**: `uint32`

Examples:
```go
ID        uint64 `gorm:"primaryKey;autoIncrement" json:"id"`
ProjectID uint64 `gorm:"not null;index" json:"project_id"`
Version   uint32 `gorm:"not null;default:1" json:"version"`
```

## String Types

**Always specify size**: `size:255` for most fields
**Longer text**: Use appropriate size or `type:text`
**Required strings**: Combine `not null;size:N`

Examples:
```go
Name        string `gorm:"not null;size:255" json:"name"`
Description string `gorm:"size:500" json:"description,omitempty"`
LongText    string `gorm:"type:text" json:"long_text,omitempty"`
```

## Binary Data

**Large binary**: `*[]byte` with `type:longblob`

Example:
```go
Data *[]byte `gorm:"not null;type:longblob" json:"data"`
```

## Relationships

**One-to-one/Many-to-one**: Pointer to entity type
**Always optional**: Use pointer type (`*SymbolData`)
**Cascade delete**: `constraint:OnDelete:CASCADE`

Example:
```go
SymbolData *SymbolData `gorm:"foreignKey:SymbolID;references:ID;constraint:OnDelete:CASCADE" json:"symbol_data,omitempty"`
```

## Time Fields

**Timestamps**: `time.Time` (not pointer)
**Soft delete**: `gorm.DeletedAt` (not `*time.Time`)

Examples:
```go
CreatedAt time.Time      `gorm:"autoCreateTime" json:"created_at"`
DeletedAt gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`
```
