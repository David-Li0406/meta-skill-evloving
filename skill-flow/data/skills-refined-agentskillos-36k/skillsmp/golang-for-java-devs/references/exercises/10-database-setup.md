# Exercise 10: Database Setup

**Time:** 15 minutes
**Goal:** Connect to PostgreSQL using database/sql and sqlx

## The Spring Boot Version

```java
// application.yml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/myapp
    username: user
    password: pass

// entity
@Entity
public class Task {
    @Id
    @GeneratedValue
    private UUID id;
    private String title;
}

// repository (auto-implemented!)
public interface TaskRepository extends JpaRepository<Task, UUID> {}
```

## The Go Way

No ORM magic. Use `database/sql` directly or with `sqlx` for convenience:

```go
db, err := sql.Open("postgres", "postgres://localhost:5432/myapp")
if err != nil {
    log.Fatal(err)
}

rows, err := db.QueryContext(ctx, "SELECT id, title FROM tasks WHERE id = $1", id)
```

---

## Step by Step

### 1. Add dependencies (1 min)

```bash
go get github.com/jmoiron/sqlx
go get github.com/lib/pq
```

### 2. Create database connection (4 min)

Create `internal/database/postgres.go`:

```go
package database

import (
    "context"
    "fmt"
    "time"

    "github.com/jmoiron/sqlx"
    _ "github.com/lib/pq"
)

type Config struct {
    URL             string
    MaxOpenConns    int
    MaxIdleConns    int
    ConnMaxLifetime time.Duration
}

func Connect(cfg Config) (*sqlx.DB, error) {
    db, err := sqlx.Connect("postgres", cfg.URL)
    if err != nil {
        return nil, fmt.Errorf("connecting to database: %w", err)
    }

    db.SetMaxOpenConns(cfg.MaxOpenConns)
    db.SetMaxIdleConns(cfg.MaxIdleConns)
    db.SetConnMaxLifetime(cfg.ConnMaxLifetime)

    return db, nil
}

func Ping(ctx context.Context, db *sqlx.DB) error {
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    return db.PingContext(ctx)
}
```

### 3. Create the Task model with DB tags (3 min)

Update `internal/model/task.go`:

```go
package model

import "time"

type Task struct {
    ID          string    `json:"id" db:"id"`
    Title       string    `json:"title" db:"title"`
    Description string    `json:"description" db:"description"`
    Completed   bool      `json:"completed" db:"completed"`
    CreatedAt   time.Time `json:"created_at" db:"created_at"`
    UpdatedAt   time.Time `json:"updated_at" db:"updated_at"`
}
```

### 4. Create repository with SQL (5 min)

Create `internal/repository/task_postgres.go`:

```go
package repository

import (
    "context"
    "database/sql"
    "errors"
    "time"

    "github.com/jmoiron/sqlx"

    "my-first-go-app/internal/model"
)

type PostgresTaskRepository struct {
    db *sqlx.DB
}

func NewPostgresTaskRepository(db *sqlx.DB) *PostgresTaskRepository {
    return &PostgresTaskRepository{db: db}
}

func (r *PostgresTaskRepository) FindByID(ctx context.Context, id string) (*model.Task, error) {
    var task model.Task
    err := r.db.GetContext(ctx, &task, `
        SELECT id, title, description, completed, created_at, updated_at
        FROM tasks
        WHERE id = $1
    `, id)

    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, ErrNotFound
        }
        return nil, err
    }

    return &task, nil
}

func (r *PostgresTaskRepository) FindAll(ctx context.Context) ([]*model.Task, error) {
    var tasks []*model.Task
    err := r.db.SelectContext(ctx, &tasks, `
        SELECT id, title, description, completed, created_at, updated_at
        FROM tasks
        ORDER BY created_at DESC
    `)

    if err != nil {
        return nil, err
    }

    return tasks, nil
}

func (r *PostgresTaskRepository) Save(ctx context.Context, task *model.Task) error {
    now := time.Now()
    task.UpdatedAt = now

    if task.CreatedAt.IsZero() {
        task.CreatedAt = now
    }

    _, err := r.db.NamedExecContext(ctx, `
        INSERT INTO tasks (id, title, description, completed, created_at, updated_at)
        VALUES (:id, :title, :description, :completed, :created_at, :updated_at)
        ON CONFLICT (id) DO UPDATE SET
            title = EXCLUDED.title,
            description = EXCLUDED.description,
            completed = EXCLUDED.completed,
            updated_at = EXCLUDED.updated_at
    `, task)

    return err
}

func (r *PostgresTaskRepository) Delete(ctx context.Context, id string) error {
    result, err := r.db.ExecContext(ctx, `DELETE FROM tasks WHERE id = $1`, id)
    if err != nil {
        return err
    }

    rows, err := result.RowsAffected()
    if err != nil {
        return err
    }

    if rows == 0 {
        return ErrNotFound
    }

    return nil
}
```

### 5. Database migration (2 min)

Create `migrations/001_create_tasks.sql`:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```

## Wire It Together

In `cmd/server/main.go`:

```go
// connect to database
dbCfg := database.Config{
    URL:             cfg.DatabaseURL,
    MaxOpenConns:    cfg.DBMaxConns,
    MaxIdleConns:    cfg.DBMaxConns / 2,
    ConnMaxLifetime: time.Hour,
}

db, err := database.Connect(dbCfg)
if err != nil {
    logger.Error("database connection failed", "error", err)
    os.Exit(1)
}
defer db.Close()

// verify connection
if err := database.Ping(context.Background(), db); err != nil {
    logger.Error("database ping failed", "error", err)
    os.Exit(1)
}

// use postgres repository
taskRepo := repository.NewPostgresTaskRepository(db)
```

## sqlx vs database/sql

| Feature | database/sql | sqlx |
|---------|--------------|------|
| Query to struct | Manual scanning | `db.Get()`, `db.Select()` |
| Named parameters | Not supported | `:name` syntax |
| Null handling | sql.NullString | Same, but easier |
| Learning curve | Lower | Slightly higher |

## What Just Happened?

| Spring Boot | Go |
|-------------|-----|
| Auto-config datasource | Manual connection setup |
| JPA entity mapping | Struct tags (db:"field") |
| Spring Data queries | Raw SQL or sqlx |
| Connection pool magic | Explicit pool config |

## Checkpoint

- [ ] Database connection works
- [ ] CRUD operations use SQL
- [ ] Connection pool configured
- [ ] Struct tags map to columns

**Next:** Exercise 11 - Repository Layer
