# Exercise 11: Repository Layer

**Time:** 15 minutes
**Goal:** Create clean repository interface with multiple implementations

## The Spring Boot Version

```java
public interface TaskRepository extends JpaRepository<Task, String> {
    List<Task> findByCompletedTrue();
    Optional<Task> findByTitle(String title);
}
// Spring Data implements this automatically
```

## The Go Way

Define the interface, implement it yourself:

```go
type TaskRepository interface {
    FindByID(ctx context.Context, id string) (*model.Task, error)
    FindAll(ctx context.Context) ([]*model.Task, error)
    Save(ctx context.Context, task *model.Task) error
    Delete(ctx context.Context, id string) error
}
```

---

## Step by Step

### 1. Define the repository interface (3 min)

Create `internal/repository/interface.go`:

```go
package repository

import (
    "context"
    "errors"

    "my-first-go-app/internal/model"
)

var ErrNotFound = errors.New("not found")

// TaskRepository defines the contract for task storage
type TaskRepository interface {
    FindByID(ctx context.Context, id string) (*model.Task, error)
    FindAll(ctx context.Context) ([]*model.Task, error)
    FindByCompleted(ctx context.Context, completed bool) ([]*model.Task, error)
    Save(ctx context.Context, task *model.Task) error
    Delete(ctx context.Context, id string) error
}
```

### 2. Create in-memory implementation (4 min)

Create `internal/repository/memory.go`:

```go
package repository

import (
    "context"
    "sync"
    "time"

    "my-first-go-app/internal/model"
)

type MemoryTaskRepository struct {
    mu    sync.RWMutex
    tasks map[string]*model.Task
}

func NewMemoryTaskRepository() *MemoryTaskRepository {
    return &MemoryTaskRepository{
        tasks: make(map[string]*model.Task),
    }
}

func (r *MemoryTaskRepository) FindByID(ctx context.Context, id string) (*model.Task, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()

    task, ok := r.tasks[id]
    if !ok {
        return nil, ErrNotFound
    }
    return task, nil
}

func (r *MemoryTaskRepository) FindAll(ctx context.Context) ([]*model.Task, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()

    tasks := make([]*model.Task, 0, len(r.tasks))
    for _, t := range r.tasks {
        tasks = append(tasks, t)
    }
    return tasks, nil
}

func (r *MemoryTaskRepository) FindByCompleted(ctx context.Context, completed bool) ([]*model.Task, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()

    var tasks []*model.Task
    for _, t := range r.tasks {
        if t.Completed == completed {
            tasks = append(tasks, t)
        }
    }
    return tasks, nil
}

func (r *MemoryTaskRepository) Save(ctx context.Context, task *model.Task) error {
    r.mu.Lock()
    defer r.mu.Unlock()

    now := time.Now()
    task.UpdatedAt = now
    if task.CreatedAt.IsZero() {
        task.CreatedAt = now
    }

    r.tasks[task.ID] = task
    return nil
}

func (r *MemoryTaskRepository) Delete(ctx context.Context, id string) error {
    r.mu.Lock()
    defer r.mu.Unlock()

    if _, ok := r.tasks[id]; !ok {
        return ErrNotFound
    }
    delete(r.tasks, id)
    return nil
}
```

### 3. Update Postgres implementation (4 min)

Update `internal/repository/postgres.go`:

```go
func (r *PostgresTaskRepository) FindByCompleted(ctx context.Context, completed bool) ([]*model.Task, error) {
    var tasks []*model.Task
    err := r.db.SelectContext(ctx, &tasks, `
        SELECT id, title, description, completed, created_at, updated_at
        FROM tasks
        WHERE completed = $1
        ORDER BY created_at DESC
    `, completed)

    if err != nil {
        return nil, err
    }

    return tasks, nil
}
```

### 4. Add compile-time interface check (2 min)

At the bottom of each implementation file:

```go
// verify interface compliance at compile time
var _ TaskRepository = (*MemoryTaskRepository)(nil)
var _ TaskRepository = (*PostgresTaskRepository)(nil)
```

### 5. Choose implementation at runtime (2 min)

In `cmd/server/main.go`:

```go
// choose repository based on config
var taskRepo repository.TaskRepository

if cfg.DatabaseURL != "" {
    db, err := database.Connect(dbCfg)
    if err != nil {
        logger.Error("database connection failed", "error", err)
        os.Exit(1)
    }
    defer db.Close()
    taskRepo = repository.NewPostgresTaskRepository(db)
    logger.Info("using postgres repository")
} else {
    taskRepo = repository.NewMemoryTaskRepository()
    logger.Info("using in-memory repository")
}
```

## Query Methods Pattern

```go
// filter options
type TaskFilter struct {
    Completed *bool
    Limit     int
    Offset    int
}

func (r *PostgresTaskRepository) FindWithFilter(ctx context.Context, filter TaskFilter) ([]*model.Task, error) {
    query := `SELECT * FROM tasks WHERE 1=1`
    args := []interface{}{}
    argNum := 1

    if filter.Completed != nil {
        query += fmt.Sprintf(" AND completed = $%d", argNum)
        args = append(args, *filter.Completed)
        argNum++
    }

    query += " ORDER BY created_at DESC"

    if filter.Limit > 0 {
        query += fmt.Sprintf(" LIMIT $%d", argNum)
        args = append(args, filter.Limit)
        argNum++
    }

    if filter.Offset > 0 {
        query += fmt.Sprintf(" OFFSET $%d", argNum)
        args = append(args, filter.Offset)
    }

    var tasks []*model.Task
    err := r.db.SelectContext(ctx, &tasks, query, args...)
    return tasks, err
}
```

## Transaction Support

```go
type TransactionalTaskRepository interface {
    TaskRepository
    WithTx(tx *sqlx.Tx) TaskRepository
}

func (r *PostgresTaskRepository) WithTx(tx *sqlx.Tx) TaskRepository {
    return &PostgresTaskRepository{db: tx}  // sqlx.Tx implements same interface
}

// usage
tx, _ := db.Beginx()
defer tx.Rollback()

repo := taskRepo.WithTx(tx)
repo.Save(ctx, task1)
repo.Save(ctx, task2)

tx.Commit()
```

## What Just Happened?

| Spring Boot | Go |
|-------------|-----|
| Interface auto-implemented | Manual implementation |
| findByX method names | Raw SQL or custom methods |
| @Transactional | Manual tx.Begin()/Commit() |
| JPA magic | Explicit SQL |

## Checkpoint

- [ ] Interface defined for repository
- [ ] In-memory implementation for testing
- [ ] Postgres implementation for production
- [ ] Compile-time interface verification

**Next:** Exercise 12 - Goroutines
