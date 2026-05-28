# Exercise 08: Testing Handlers

**Time:** 15 minutes
**Goal:** Write HTTP handler tests using httptest

## The Spring Boot Version

```java
@WebMvcTest(TaskController.class)
class TaskControllerTest {

    @Autowired
    MockMvc mockMvc;

    @MockBean
    TaskService taskService;

    @Test
    void getTask_returnsTask() throws Exception {
        when(taskService.findById("123")).thenReturn(new Task("123", "Test"));

        mockMvc.perform(get("/api/tasks/123"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value("123"));
    }
}
```

## The Go Way

Use `net/http/httptest` from standard library:

```go
func TestGetTask(t *testing.T) {
    req := httptest.NewRequest("GET", "/api/tasks/123", nil)
    w := httptest.NewRecorder()

    handler.GetByID(w, req)

    if w.Code != http.StatusOK {
        t.Errorf("expected 200, got %d", w.Code)
    }
}
```

---

## Step by Step

### 1. Create a mock repository (4 min)

Create `internal/handler/task_test.go`:

```go
package handler_test

import (
    "context"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"

    "github.com/go-chi/chi/v5"

    "my-first-go-app/internal/handler"
    "my-first-go-app/internal/model"
    "my-first-go-app/internal/repository"
)

// MockTaskRepository for testing
type MockTaskRepository struct {
    tasks map[string]*model.Task
}

func NewMockTaskRepository() *MockTaskRepository {
    return &MockTaskRepository{
        tasks: make(map[string]*model.Task),
    }
}

func (m *MockTaskRepository) FindAll(ctx context.Context) ([]*model.Task, error) {
    tasks := make([]*model.Task, 0, len(m.tasks))
    for _, t := range m.tasks {
        tasks = append(tasks, t)
    }
    return tasks, nil
}

func (m *MockTaskRepository) FindByID(ctx context.Context, id string) (*model.Task, error) {
    task, ok := m.tasks[id]
    if !ok {
        return nil, repository.ErrNotFound
    }
    return task, nil
}

func (m *MockTaskRepository) Save(ctx context.Context, task *model.Task) error {
    m.tasks[task.ID] = task
    return nil
}

func (m *MockTaskRepository) Delete(ctx context.Context, id string) error {
    if _, ok := m.tasks[id]; !ok {
        return repository.ErrNotFound
    }
    delete(m.tasks, id)
    return nil
}
```

### 2. Write test for GET by ID (4 min)

```go
func TestTaskHandler_GetByID(t *testing.T) {
    tests := []struct {
        name       string
        taskID     string
        setupRepo  func(*MockTaskRepository)
        wantStatus int
        wantBody   string
    }{
        {
            name:   "returns task when found",
            taskID: "123",
            setupRepo: func(m *MockTaskRepository) {
                m.tasks["123"] = &model.Task{
                    ID:    "123",
                    Title: "Test Task",
                }
            },
            wantStatus: http.StatusOK,
            wantBody:   `"id":"123"`,
        },
        {
            name:       "returns 404 when not found",
            taskID:     "nonexistent",
            setupRepo:  func(m *MockTaskRepository) {},
            wantStatus: http.StatusNotFound,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // setup
            repo := NewMockTaskRepository()
            tt.setupRepo(repo)
            h := handler.NewTaskHandler(repo)

            // create request with chi context
            req := httptest.NewRequest("GET", "/api/tasks/"+tt.taskID, nil)

            // add chi URL params
            rctx := chi.NewRouteContext()
            rctx.URLParams.Add("id", tt.taskID)
            req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))

            w := httptest.NewRecorder()

            // execute
            h.GetByID(w, req)

            // assert
            if w.Code != tt.wantStatus {
                t.Errorf("status = %d, want %d", w.Code, tt.wantStatus)
            }

            if tt.wantBody != "" && !strings.Contains(w.Body.String(), tt.wantBody) {
                t.Errorf("body = %s, want to contain %s", w.Body.String(), tt.wantBody)
            }
        })
    }
}
```

### 3. Write test for POST create (4 min)

```go
func TestTaskHandler_Create(t *testing.T) {
    tests := []struct {
        name       string
        body       string
        wantStatus int
    }{
        {
            name:       "creates task with valid input",
            body:       `{"title":"New Task","description":"Description"}`,
            wantStatus: http.StatusCreated,
        },
        {
            name:       "returns 400 for invalid json",
            body:       `{invalid}`,
            wantStatus: http.StatusBadRequest,
        },
        {
            name:       "returns 400 for missing title",
            body:       `{"description":"No title"}`,
            wantStatus: http.StatusBadRequest,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            repo := NewMockTaskRepository()
            h := handler.NewTaskHandler(repo)

            req := httptest.NewRequest("POST", "/api/tasks", strings.NewReader(tt.body))
            req.Header.Set("Content-Type", "application/json")

            w := httptest.NewRecorder()

            h.Create(w, req)

            if w.Code != tt.wantStatus {
                t.Errorf("status = %d, want %d", w.Code, tt.wantStatus)
            }

            // if created, verify task in response
            if tt.wantStatus == http.StatusCreated {
                var task model.Task
                if err := json.NewDecoder(w.Body).Decode(&task); err != nil {
                    t.Fatalf("failed to decode response: %v", err)
                }
                if task.ID == "" {
                    t.Error("expected task to have ID")
                }
                if task.Title != "New Task" {
                    t.Errorf("title = %s, want New Task", task.Title)
                }
            }
        })
    }
}
```

### 4. Run tests (3 min)

```bash
# run all tests
go test ./...

# run with verbose output
go test -v ./internal/handler/...

# run specific test
go test -v -run TestTaskHandler_GetByID ./internal/handler/...

# with coverage
go test -cover ./...
```

## Table-Driven Tests Pattern

```go
tests := []struct {
    name       string        // test case name
    input      InputType     // test input
    setup      func()        // optional setup
    wantResult ResultType    // expected result
    wantErr    bool          // expect error?
}{
    {"case 1", input1, nil, result1, false},
    {"case 2", input2, nil, result2, true},
}

for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        // test logic
    })
}
```

## Testing with Chi Router Integration

```go
func TestTaskRoutes(t *testing.T) {
    repo := NewMockTaskRepository()
    h := handler.NewTaskHandler(repo)

    r := chi.NewRouter()
    r.Get("/api/tasks/{id}", h.GetByID)
    r.Post("/api/tasks", h.Create)

    // test through router
    req := httptest.NewRequest("GET", "/api/tasks/123", nil)
    w := httptest.NewRecorder()

    r.ServeHTTP(w, req)

    // assert...
}
```

## What Just Happened?

| Spring Boot | Go |
|-------------|-----|
| @WebMvcTest | httptest.NewRequest + NewRecorder |
| @MockBean | Manual mock implementation |
| MockMvc.perform() | handler.Method(w, req) |
| jsonPath assertions | json.Decode + field checks |

## Checkpoint

- [ ] Tests use httptest package
- [ ] Table-driven tests for multiple cases
- [ ] Chi URL params added to context
- [ ] Tests pass with `go test ./...`

**Next:** Exercise 09 - Testing Services
