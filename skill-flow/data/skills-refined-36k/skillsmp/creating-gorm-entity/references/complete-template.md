# Complete Entity Template

A comprehensive template showing all common patterns in a single GORM entity.

```go
package model

import (
	"time"

	"gorm.io/gorm"
)

type EntityName struct {
	// Primary Key
	ID uint64 `gorm:"primaryKey;autoIncrement" json:"id"`

	// Foreign Keys (if any)
	ParentID uint64 `gorm:"not null;index" json:"parent_id"`

	// Business Fields
	UID         string `gorm:"not null;size:255;uniqueIndex" json:"uid"`
	Name        string `gorm:"not null;size:255" json:"name"`
	Description string `gorm:"size:500" json:"description,omitempty"`

	// Numeric Fields
	Version uint32 `gorm:"not null;default:1" json:"version"`

	// Relationships
	RelatedEntity *RelatedEntity `gorm:"foreignKey:RelatedEntityID;references:ID;constraint:OnDelete:CASCADE" json:"related_entity,omitempty"`

	// Timestamps (required)
	CreatedAt time.Time `gorm:"autoCreateTime" json:"created_at"`
	UpdatedAt time.Time `gorm:"autoUpdateTime" json:"updated_at"`

	// Soft Delete (optional)
	DeletedAt gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`
}

func (EntityName) TableName() string {
	return "entity_names"  // plural snake_case
}
```
