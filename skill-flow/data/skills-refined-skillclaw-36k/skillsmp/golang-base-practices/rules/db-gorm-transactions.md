---
title: Transaction Handling Patterns
impact: CRITICAL
impactDescription: Data consistency guarantee
tags: database, gorm, transaction
---

## Transaction Handling Patterns

Use GORM transactions to ensure data consistency.

**Incorrect (no transaction, data inconsistency):**

```go
func Transfer(fromID, toID uint, amount int) error {
    db.Model(&Account{}).Where("id = ?", fromID).Update("balance", gorm.Expr("balance - ?", amount))
    // If this fails, money is deducted but not added
    db.Model(&Account{}).Where("id = ?", toID).Update("balance", gorm.Expr("balance + ?", amount))
    return nil
}
```

**Correct (using transaction):**

```go
func Transfer(db *gorm.DB, fromID, toID uint, amount int) error {
    return db.Transaction(func(tx *gorm.DB) error {
        // Deduct
        result := tx.Model(&Account{}).
            Where("id = ? AND balance >= ?", fromID, amount).
            Update("balance", gorm.Expr("balance - ?", amount))

        if result.Error != nil {
            return result.Error
        }
        if result.RowsAffected == 0 {
            return errors.New("insufficient balance or account not found")
        }

        // Add
        result = tx.Model(&Account{}).
            Where("id = ?", toID).
            Update("balance", gorm.Expr("balance + ?", amount))

        if result.Error != nil {
            return result.Error
        }
        if result.RowsAffected == 0 {
            return errors.New("target account not found")
        }

        return nil // Return nil to commit transaction
    })
}
```

**Nested Transactions (SavePoint):**

```go
db.Transaction(func(tx *gorm.DB) error {
    tx.Create(&user1)

    tx.Transaction(func(tx2 *gorm.DB) error {
        tx2.Create(&user2)
        return errors.New("rollback user2 only")
    })

    return nil // user1 will be committed
})
```
