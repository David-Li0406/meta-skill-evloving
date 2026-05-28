---
title: Connection Pool Configuration
impact: HIGH
impactDescription: Balance performance and resources
tags: database, connection-pool, performance
---

## Connection Pool Configuration

Properly configure database connection pool to balance performance and resource consumption.

**Incorrect (default config not suitable for production):**

```go
db, _ := gorm.Open(mysql.Open(dsn), &gorm.Config{})
// Default config: unlimited connections, may exhaust database resources
```

**Correct (production environment configuration):**

```go
func ConfigureConnectionPool(db *gorm.DB, cfg PoolConfig) error {
    sqlDB, err := db.DB()
    if err != nil {
        return err
    }

    // Maximum idle connections
    // Recommended: 10-25% of MaxOpenConns
    sqlDB.SetMaxIdleConns(cfg.MaxIdleConns)

    // Maximum open connections
    // Calculate based on database limits and application instances
    sqlDB.SetMaxOpenConns(cfg.MaxOpenConns)

    // Maximum idle time for connections
    // Recommended: 5-10 minutes
    sqlDB.SetConnMaxIdleTime(cfg.ConnMaxIdleTime)

    // Maximum connection lifetime
    // Recommended: less than database wait_timeout
    sqlDB.SetConnMaxLifetime(cfg.ConnMaxLifetime)

    return nil
}

// Configuration example
type PoolConfig struct {
    MaxIdleConns    int           // Recommended: 10
    MaxOpenConns    int           // Recommended: 100
    ConnMaxIdleTime time.Duration // Recommended: 5 * time.Minute
    ConnMaxLifetime time.Duration // Recommended: 1 * time.Hour
}
```

**Configuration Guide:**

| Parameter | Development | Production | Description |
|-----------|-------------|------------|-------------|
| MaxIdleConns | 2 | 10-25 | Keep warm connections, reduce connection overhead |
| MaxOpenConns | 10 | 50-200 | Calculate based on total DB connections and instances |
| ConnMaxIdleTime | 5min | 5-10min | Release long-idle connections |
| ConnMaxLifetime | 1h | 30min-1h | Must be less than DB wait_timeout |
