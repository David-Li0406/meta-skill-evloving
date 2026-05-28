---
title: GORM Hook Usage Guidelines
impact: MEDIUM
impactDescription: Automated data processing
tags: database, gorm, hooks
---

## GORM Hook Usage Guidelines

Use GORM Hooks appropriately for automation logic, but avoid over-reliance.

**Correct Example (common hook scenarios):**

```go
type User struct {
    ID        uint      `gorm:"primaryKey"`
    Name      string    `gorm:"size:100"`
    Email     string    `gorm:"uniqueIndex"`
    Password  string    `gorm:"-:all"` // Don't store plaintext
    PassHash  string    `gorm:"column:password"`
    CreatedAt time.Time
    UpdatedAt time.Time
}

// BeforeCreate - Hash password before creation
func (u *User) BeforeCreate(tx *gorm.DB) error {
    if u.Password != "" {
        hash, err := bcrypt.GenerateFromPassword([]byte(u.Password), bcrypt.DefaultCost)
        if err != nil {
            return err
        }
        u.PassHash = string(hash)
    }
    return nil
}

// AfterFind - Handle sensitive data after query
func (u *User) AfterFind(tx *gorm.DB) error {
    u.PassHash = "" // Don't expose password hash
    return nil
}
```

**Hook Best Practices:**
- Keep hook logic simple
- Don't put complex business logic in hooks
- Hook errors cause transaction rollback
- Avoid calling external services in hooks

**Available Hooks:**
- `BeforeSave` / `AfterSave`
- `BeforeCreate` / `AfterCreate`
- `BeforeUpdate` / `AfterUpdate`
- `BeforeDelete` / `AfterDelete`
- `AfterFind`
