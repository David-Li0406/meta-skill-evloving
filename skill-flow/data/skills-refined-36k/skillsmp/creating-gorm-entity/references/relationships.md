# Relationship Examples

Detailed examples for setting up entity relationships in GORM.

## One-to-One with Cascade Delete

One-to-One relationship with cascade delete:

```go
type Symbol struct {
	ID         uint64      `gorm:"primaryKey;autoIncrement" json:"id"`
	SymbolData *SymbolData `gorm:"foreignKey:SymbolID;references:ID;constraint:OnDelete:CASCADE" json:"symbol_data,omitempty"`
	// ... other fields
}

type SymbolData struct {
	ID       uint64 `gorm:"primaryKey;autoIncrement" json:"id"`
	SymbolID uint64 `gorm:"not null;uniqueIndex" json:"symbol_id"`
	// ... other fields
}
```

Key points:
- Parent has pointer to child (`*SymbolData`)
- Child has foreign key field (`SymbolID uint64`)
- Child has foreign key field (`SymbolID uint64`)
- Foreign key field is indexed: `uniqueIndex` (one-to-one) or `index` (many-to-one)
- Relationship tag specifies: `foreignKey:ChildField;references:ParentField;constraint:OnDelete:CASCADE`
