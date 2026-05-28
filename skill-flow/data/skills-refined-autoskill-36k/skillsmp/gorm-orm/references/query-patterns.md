# GORM Query Patterns

## Basic CRUD

```go
// Create
user := User{Name: "John", Email: "john@example.com"}
result := db.Create(&user) // user.ID populated after insert
if result.Error != nil {
    return result.Error
}

// Batch create
users := []User{{Name: "A"}, {Name: "B"}, {Name: "C"}}
db.Create(&users)

// Read
var user User
db.First(&user, 1) // by primary key
db.First(&user, "id = ?", 1)
db.Find(&users) // all records

// Update
db.Model(&user).Update("Name", "Jane")
db.Model(&user).Updates(User{Name: "Jane", Age: 30})
db.Model(&user).Updates(map[string]interface{}{"name": "Jane", "age": 30})

// Delete
db.Delete(&user, 1)
db.Where("name = ?", "John").Delete(&User{})
```

## Conditions

```go
// Where
db.Where("name = ?", "John").First(&user)
db.Where("name = ? AND age >= ?", "John", 18).Find(&users)
db.Where("name IN ?", []string{"John", "Jane"}).Find(&users)
db.Where("name LIKE ?", "%john%").Find(&users)

// Struct condition
db.Where(&User{Name: "John", Age: 30}).Find(&users)

// Map condition
db.Where(map[string]interface{}{"name": "John", "age": 30}).Find(&users)

// Or
db.Where("name = ?", "John").Or("name = ?", "Jane").Find(&users)

// Not
db.Not("name = ?", "John").Find(&users)

// Select specific fields
db.Select("name", "age").Find(&users)
db.Select("COALESCE(age, 0) as age").Find(&users)

// Order
db.Order("age desc, name").Find(&users)

// Limit & Offset
db.Limit(10).Offset(20).Find(&users)
```

## Preloading (Eager Loading)

```go
// Preload associations
db.Preload("Posts").Find(&users)
db.Preload("Posts.Comments").Find(&users)

// Preload with conditions
db.Preload("Posts", "published = ?", true).Find(&users)

// Preload with custom query
db.Preload("Posts", func(db *gorm.DB) *gorm.DB {
    return db.Order("posts.created_at DESC").Limit(5)
}).Find(&users)

// Preload all
db.Preload(clause.Associations).Find(&users)

// Joins
db.Joins("Profile").Find(&users)
db.Joins("JOIN posts ON posts.user_id = users.id").
    Where("posts.title = ?", "Hello").
    Find(&users)
```

## Transactions

```go
// Automatic transaction
err := db.Transaction(func(tx *gorm.DB) error {
    if err := tx.Create(&user).Error; err != nil {
        return err // rollback
    }

    if err := tx.Create(&post).Error; err != nil {
        return err // rollback
    }

    return nil // commit
})

// Manual transaction
tx := db.Begin()
if err := tx.Create(&user).Error; err != nil {
    tx.Rollback()
    return err
}
if err := tx.Create(&post).Error; err != nil {
    tx.Rollback()
    return err
}
tx.Commit()

// Nested transactions (savepoints)
db.Transaction(func(tx *gorm.DB) error {
    tx.Create(&user)
    
    tx.Transaction(func(tx2 *gorm.DB) error {
        tx2.Create(&post)
        return errors.New("rollback post only")
    })
    
    return nil // user is committed
})
```

## Scopes

```go
// Define reusable scopes
func Active(db *gorm.DB) *gorm.DB {
    return db.Where("active = ?", true)
}

func Paginate(page, size int) func(db *gorm.DB) *gorm.DB {
    return func(db *gorm.DB) *gorm.DB {
        offset := (page - 1) * size
        return db.Offset(offset).Limit(size)
    }
}

// Usage
db.Scopes(Active, Paginate(1, 10)).Find(&users)
```

## Raw SQL

```go
// Raw query
db.Raw("SELECT * FROM users WHERE name = ?", "John").Scan(&users)

// Exec
db.Exec("UPDATE users SET age = ? WHERE name = ?", 30, "John")

// Named arguments
db.Where("name = @name OR age = @age", sql.Named("name", "John"), sql.Named("age", 30)).Find(&users)
```
