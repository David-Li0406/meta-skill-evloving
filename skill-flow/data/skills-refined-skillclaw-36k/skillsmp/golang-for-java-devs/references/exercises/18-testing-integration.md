# Exercise 18: Integration Testing

**Time:** 15 minutes
**Goal:** Test against real dependencies using testcontainers

## The Spring Boot Version

```java
@SpringBootTest
@Testcontainers
class TaskIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
    }

    @Test
    void createTask_persistsToDatabase() {
        // test with real postgres
    }
}
```

## The Go Way

Use testcontainers-go to spin up real dependencies:

```go
func TestWithPostgres(t *testing.T) {
    ctx := context.Background()

    container, _ := postgres.RunContainer(ctx)
    defer container.Terminate(ctx)

    connStr, _ := container.ConnectionString(ctx)
    db, _ := sqlx.Connect("postgres", connStr)

    // test with real database
}
```

---

## Step by Step

### 1. Add testcontainers dependency (1 min)

```bash
go get github.com/testcontainers/testcontainers-go
go get github.com/testcontainers/testcontainers-go/modules/postgres
```

### 2. Create test helper for Postgres (5 min)

Create `internal/testutil/postgres.go`:

```go
package testutil

import (
    "context"
    "testing"
    "time"

    "github.com/jmoiron/sqlx"
    _ "github.com/lib/pq"
    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/modules/postgres"
    "github.com/testcontainers/testcontainers-go/wait"
)

type PostgresContainer struct {
    *postgres.PostgresContainer
    ConnectionString string
}

func SetupPostgres(t *testing.T) *PostgresContainer {
    t.Helper()

    ctx := context.Background()

    container, err := postgres.RunContainer(ctx,
        testcontainers.WithImage("postgres:15-alpine"),
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("test"),
        postgres.WithPassword("test"),
        testcontainers.WithWaitStrategy(
            wait.ForLog("database system is ready to accept connections").
                WithOccurrence(2).
                WithStartupTimeout(5*time.Second),
        ),
    )
    if err != nil {
        t.Fatalf("failed to start postgres: %v", err)
    }

    connStr, err := container.ConnectionString(ctx, "sslmode=disable")
    if err != nil {
        t.Fatalf("failed to get connection string: %v", err)
    }

    // cleanup on test end
    t.Cleanup(func() {
        if err := container.Terminate(ctx); err != nil {
            t.Logf("failed to terminate container: %v", err)
        }
    })

    return &PostgresContainer{
        PostgresContainer: container,
        ConnectionString:  connStr,
    }
}

func SetupDB(t *testing.T, connStr string) *sqlx.DB {
    t.Helper()

    db, err := sqlx.Connect("postgres", connStr)
    if err != nil {
        t.Fatalf("failed to connect to database: %v", err)
    }

    // run migrations
    _, err = db.Exec(`
        CREATE TABLE IF NOT EXISTS tasks (
            id VARCHAR(36) PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    `)
    if err != nil {
        t.Fatalf("failed to run migrations: %v", err)
    }

    t.Cleanup(func() {
        db.Close()
    })

    return db
}
```

### 3. Write integration test (5 min)

Create `internal/repository/task_integration_test.go`:

```go
//go:build integration

package repository_test

import (
    "context"
    "testing"

    "github.com/google/uuid"

    "my-first-go-app/internal/model"
    "my-first-go-app/internal/repository"
    "my-first-go-app/internal/testutil"
)

func TestPostgresTaskRepository_Integration(t *testing.T) {
    // skip if short tests
    if testing.Short() {
        t.Skip("skipping integration test")
    }

    // setup postgres container
    pg := testutil.SetupPostgres(t)
    db := testutil.SetupDB(t, pg.ConnectionString)

    repo := repository.NewPostgresTaskRepository(db)
    ctx := context.Background()

    t.Run("Save and FindByID", func(t *testing.T) {
        task := &model.Task{
            ID:          uuid.New().String(),
            Title:       "Integration Test Task",
            Description: "Testing with real database",
        }

        // save
        err := repo.Save(ctx, task)
        if err != nil {
            t.Fatalf("Save failed: %v", err)
        }

        // retrieve
        found, err := repo.FindByID(ctx, task.ID)
        if err != nil {
            t.Fatalf("FindByID failed: %v", err)
        }

        if found.Title != task.Title {
            t.Errorf("Title = %s, want %s", found.Title, task.Title)
        }
    })

    t.Run("FindAll", func(t *testing.T) {
        // create multiple tasks
        for i := 0; i < 3; i++ {
            task := &model.Task{
                ID:    uuid.New().String(),
                Title: "Task " + uuid.New().String()[:8],
            }
            repo.Save(ctx, task)
        }

        tasks, err := repo.FindAll(ctx)
        if err != nil {
            t.Fatalf("FindAll failed: %v", err)
        }

        if len(tasks) < 3 {
            t.Errorf("expected at least 3 tasks, got %d", len(tasks))
        }
    })

    t.Run("Delete", func(t *testing.T) {
        task := &model.Task{
            ID:    uuid.New().String(),
            Title: "To be deleted",
        }
        repo.Save(ctx, task)

        err := repo.Delete(ctx, task.ID)
        if err != nil {
            t.Fatalf("Delete failed: %v", err)
        }

        _, err = repo.FindByID(ctx, task.ID)
        if err != repository.ErrNotFound {
            t.Error("expected ErrNotFound after delete")
        }
    })
}
```

### 4. Run integration tests (2 min)

```bash
# run all tests
go test ./...

# run only integration tests
go test -tags=integration ./...

# skip integration tests
go test -short ./...
```

### 5. End-to-end API test (2 min)

Create `internal/handler/task_e2e_test.go`:

```go
//go:build integration

package handler_test

import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/go-chi/chi/v5"

    "my-first-go-app/internal/handler"
    "my-first-go-app/internal/model"
    "my-first-go-app/internal/repository"
    "my-first-go-app/internal/testutil"
)

func TestTaskAPI_E2E(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping e2e test")
    }

    pg := testutil.SetupPostgres(t)
    db := testutil.SetupDB(t, pg.ConnectionString)

    repo := repository.NewPostgresTaskRepository(db)
    h := handler.NewTaskHandler(repo)

    r := chi.NewRouter()
    r.Post("/api/tasks", h.Create)
    r.Get("/api/tasks/{id}", h.GetByID)

    t.Run("create and get task", func(t *testing.T) {
        // create
        body := `{"title":"E2E Test","description":"Testing full flow"}`
        req := httptest.NewRequest("POST", "/api/tasks", bytes.NewReader([]byte(body)))
        req.Header.Set("Content-Type", "application/json")
        w := httptest.NewRecorder()

        r.ServeHTTP(w, req)

        if w.Code != http.StatusCreated {
            t.Fatalf("Create status = %d, want %d", w.Code, http.StatusCreated)
        }

        var created model.Task
        json.NewDecoder(w.Body).Decode(&created)

        // get
        req = httptest.NewRequest("GET", "/api/tasks/"+created.ID, nil)
        w = httptest.NewRecorder()

        r.ServeHTTP(w, req)

        if w.Code != http.StatusOK {
            t.Fatalf("Get status = %d, want %d", w.Code, http.StatusOK)
        }

        var found model.Task
        json.NewDecoder(w.Body).Decode(&found)

        if found.Title != "E2E Test" {
            t.Errorf("Title = %s, want E2E Test", found.Title)
        }
    })
}
```

## Build Tags

Use build tags to separate test types:

```go
//go:build integration
```

Run with: `go test -tags=integration ./...`

## What Just Happened?

| Spring Boot | Go |
|-------------|-----|
| @Testcontainers | testcontainers-go |
| @Container | postgres.RunContainer |
| @DynamicPropertySource | Get ConnectionString |
| @SpringBootTest | Manual setup |

## Checkpoint

- [ ] Testcontainers starts real Postgres
- [ ] Repository tests against real DB
- [ ] Build tags separate unit/integration
- [ ] Cleanup happens via t.Cleanup

**Next:** Exercise 19 - Project Structure
