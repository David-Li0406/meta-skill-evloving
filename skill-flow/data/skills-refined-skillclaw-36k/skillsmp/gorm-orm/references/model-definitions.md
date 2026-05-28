# GORM Model Definitions

## Basic Model

```go
import (
    "time"
    "gorm.io/gorm"
)

type User struct {
    ID        uint           `gorm:"primaryKey"`
    CreatedAt time.Time
    UpdatedAt time.Time
    DeletedAt gorm.DeletedAt `gorm:"index"`
    
    Name      string         `gorm:"size:255;not null"`
    Email     string         `gorm:"uniqueIndex;size:255"`
    Age       int            `gorm:"default:0"`
    Active    bool           `gorm:"default:true"`
}

// Or embed gorm.Model for ID, CreatedAt, UpdatedAt, DeletedAt
type Post struct {
    gorm.Model
    Title   string `gorm:"size:255;not null"`
    Content string `gorm:"type:text"`
    UserID  uint
}
```

## Field Tags

```go
type Product struct {
    // Primary key
    ID uint `gorm:"primaryKey;autoIncrement"`
    
    // Column name
    ProductName string `gorm:"column:name"`
    
    // Size and type
    Description string `gorm:"type:text"`
    Code        string `gorm:"size:50"`
    
    // Constraints
    SKU    string  `gorm:"uniqueIndex;not null"`
    Price  float64 `gorm:"not null;check:price >= 0"`
    Stock  int     `gorm:"default:0"`
    
    // Index
    Category string `gorm:"index"`
    
    // Composite index
    TenantID uint   `gorm:"uniqueIndex:idx_tenant_sku"`
    ItemSKU  string `gorm:"uniqueIndex:idx_tenant_sku"`
    
    // Ignore field
    TempData string `gorm:"-"`
    
    // Read only
    ViewCount int `gorm:"->"`
}
```

## Relationships

```go
// One-to-Many
type User struct {
    gorm.Model
    Name  string
    Posts []Post `gorm:"foreignKey:AuthorID"`
}

type Post struct {
    gorm.Model
    Title    string
    AuthorID uint
    Author   User `gorm:"foreignKey:AuthorID"`
}

// Many-to-Many
type User struct {
    gorm.Model
    Name  string
    Roles []Role `gorm:"many2many:user_roles;"`
}

type Role struct {
    gorm.Model
    Name  string
    Users []User `gorm:"many2many:user_roles;"`
}

// Has One
type User struct {
    gorm.Model
    Name    string
    Profile Profile
}

type Profile struct {
    gorm.Model
    UserID uint `gorm:"uniqueIndex"`
    Bio    string
}

// Belongs To
type Post struct {
    gorm.Model
    Title      string
    CategoryID uint
    Category   Category
}

type Category struct {
    gorm.Model
    Name string
}
```

## Polymorphic Relations

```go
type Comment struct {
    gorm.Model
    Content       string
    CommentableID uint
    CommentableType string
}

type Post struct {
    gorm.Model
    Title    string
    Comments []Comment `gorm:"polymorphic:Commentable;"`
}

type Video struct {
    gorm.Model
    URL      string
    Comments []Comment `gorm:"polymorphic:Commentable;"`
}
```

## Custom Types

```go
import "database/sql/driver"

type JSON map[string]interface{}

func (j JSON) Value() (driver.Value, error) {
    return json.Marshal(j)
}

func (j *JSON) Scan(value interface{}) error {
    bytes, _ := value.([]byte)
    return json.Unmarshal(bytes, &j)
}

type Product struct {
    gorm.Model
    Name     string
    Metadata JSON `gorm:"type:jsonb"`
}
```
