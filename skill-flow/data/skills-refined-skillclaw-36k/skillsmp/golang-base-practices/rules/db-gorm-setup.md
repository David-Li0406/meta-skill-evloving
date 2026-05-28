---
title: GORM Initialization and Configuration
impact: CRITICAL
impactDescription: Database operation foundation
tags: database, gorm, orm, setup
---

## GORM Initialization and Configuration

Properly initialize GORM with connection pool and logging configuration.

**Incorrect (missing configuration):**

```go
func main() {
    db, _ := gorm.Open(mysql.Open(dsn), &gorm.Config{})
    // Ignoring error, no connection pool config, no logging
}
```

**Correct (complete configuration):**

```go
package data

import (
    "log"
    "os"
    "time"

    "gorm.io/driver/mysql"
    "gorm.io/gorm"
    "gorm.io/gorm/logger"
)

func NewDB(dsn string) (*gorm.DB, func(), error) {
    // Configure logger
    gormLogger := logger.New(
        log.New(os.Stdout, "\r\n", log.LstdFlags),
        logger.Config{
            SlowThreshold:             200 * time.Millisecond,
            LogLevel:                  logger.Warn,
            IgnoreRecordNotFoundError: true,
            Colorful:                  true,
        },
    )

    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{
        Logger:                                   gormLogger,
        DisableForeignKeyConstraintWhenMigrating: true,
        PrepareStmt:                              true,
    })
    if err != nil {
        return nil, nil, err
    }

    // Configure connection pool
    sqlDB, err := db.DB()
    if err != nil {
        return nil, nil, err
    }

    sqlDB.SetMaxIdleConns(10)
    sqlDB.SetMaxOpenConns(100)
    sqlDB.SetConnMaxLifetime(time.Hour)

    cleanup := func() {
        sqlDB.Close()
    }

    return db, cleanup, nil
}
```

**Key Configuration:**
- `MaxIdleConns`: Number of idle connections
- `MaxOpenConns`: Maximum open connections
- `ConnMaxLifetime`: Maximum connection lifetime
- `PrepareStmt`: Prepared statement cache
