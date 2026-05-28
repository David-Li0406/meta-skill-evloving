# Exercise 06: CRUD Handler

**Time:** 15 minutes
**Goal:** Implement complete CRUD operations with proper HTTP semantics

## The Spring Boot Version

```java
@RestController
@RequestMapping("/api/tasks")
public class TaskController {

    @GetMapping
    public List<Task> list() { ... }

    @GetMapping("/{id}")
    public Task getById(@PathVariable String id) { ... }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Task create(@Valid @RequestBody CreateTaskRequest req) { ... }

    @PutMapping("/{id}")
    public Task update(@PathVariable String id, @Valid @RequestBody UpdateTaskRequest req) { ... }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable String id) { ... }
}
```

## Your Task

Create a complete CRUD handler for a Task resource:
- GET /api/tasks - list all tasks
- GET /api/tasks/{id} - get single task
- POST /api/tasks - create task
- PUT /api/tasks/{id} - update task
- DELETE /api/tasks/{id} - delete task

---

## Step by Step

### 1. Create the Task model (2 min)

Create `internal/model/task.go`:

```go
package model

import "time"

type Task struct {
    ID          string    `json:"id"`
    Title       string    `json:"title"`
    Description string    `json:"description"`
    Completed   bool      `json:"completed"`
    CreatedAt   time.Time `json:"created_at"`
    UpdatedAt   time.Time `json:"updated_at"`
}
```

### 2. Create the Task repository (3 min)

Create `internal/repository/task.go`:

```go
package repository

import (
    "context"
    "sync"
    "time"

    "my-first-go-app/internal/model"
)

type TaskRepository struct {
    mu    sync.RWMutex
    tasks map[string]*model.Task
}

func NewTaskRepository() *TaskRepository {
    return &TaskRepository{
        tasks: make(map[string]*model.Task),
    }
}

func (r *TaskRepository) FindAll(ctx context.Context) ([]*model.Task, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()

    tasks := make([]*model.Task, 0, len(r.tasks))
    for _, t := range r.tasks {
        tasks = append(tasks, t)
    }
    return tasks, nil
}

func (r *TaskRepository) FindByID(ctx context.Context, id string) (*model.Task, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()

    task, ok := r.tasks[id]
    if !ok {
        return nil, ErrNotFound
    }
    return task, nil
}

func (r *TaskRepository) Save(ctx context.Context, task *model.Task) error {
    r.mu.Lock()
    defer r.mu.Unlock()

    task.UpdatedAt = time.Now()
    if task.CreatedAt.IsZero() {
        task.CreatedAt = task.UpdatedAt
    }
    r.tasks[task.ID] = task
    return nil
}

func (r *TaskRepository) Delete(ctx context.Context, id string) error {
    r.mu.Lock()
    defer r.mu.Unlock()

    if _, ok := r.tasks[id]; !ok {
        return ErrNotFound
    }
    delete(r.tasks, id)
    return nil
}
```

### 3. Create the Task handler (8 min)

Create `internal/handler/task.go`:

```go
package handler

import (
    "encoding/json"
    "errors"
    "net/http"

    "github.com/go-chi/chi/v5"
    "github.com/go-playground/validator/v10"
    "github.com/google/uuid"

    "my-first-go-app/internal/model"
    "my-first-go-app/internal/repository"
)

type TaskHandler struct {
    repo     *repository.TaskRepository
    validate *validator.Validate
}

func NewTaskHandler(repo *repository.TaskRepository) *TaskHandler {
    return &TaskHandler{
        repo:     repo,
        validate: validator.New(),
    }
}

type CreateTaskRequest struct {
    Title       string `json:"title" validate:"required,min=1,max=200"`
    Description string `json:"description" validate:"max=1000"`
}

type UpdateTaskRequest struct {
    Title       string `json:"title" validate:"required,min=1,max=200"`
    Description string `json:"description" validate:"max=1000"`
    Completed   bool   `json:"completed"`
}

// List returns all tasks
func (h *TaskHandler) List(w http.ResponseWriter, r *http.Request) {
    tasks, err := h.repo.FindAll(r.Context())
    if err != nil {
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(tasks)
}

// GetByID returns a single task
func (h *TaskHandler) GetByID(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")

    task, err := h.repo.FindByID(r.Context(), id)
    if err != nil {
        if errors.Is(err, repository.ErrNotFound) {
            http.Error(w, "task not found", http.StatusNotFound)
            return
        }
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(task)
}

// Create creates a new task
func (h *TaskHandler) Create(w http.ResponseWriter, r *http.Request) {
    var req CreateTaskRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid json", http.StatusBadRequest)
        return
    }

    if err := h.validate.Struct(req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    task := &model.Task{
        ID:          uuid.New().String(),
        Title:       req.Title,
        Description: req.Description,
        Completed:   false,
    }

    if err := h.repo.Save(r.Context(), task); err != nil {
        http.Error(w, "failed to create task", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(task)
}

// Update updates an existing task
func (h *TaskHandler) Update(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")

    // check if task exists
    task, err := h.repo.FindByID(r.Context(), id)
    if err != nil {
        if errors.Is(err, repository.ErrNotFound) {
            http.Error(w, "task not found", http.StatusNotFound)
            return
        }
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }

    var req UpdateTaskRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid json", http.StatusBadRequest)
        return
    }

    if err := h.validate.Struct(req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    // update fields
    task.Title = req.Title
    task.Description = req.Description
    task.Completed = req.Completed

    if err := h.repo.Save(r.Context(), task); err != nil {
        http.Error(w, "failed to update task", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(task)
}

// Delete removes a task
func (h *TaskHandler) Delete(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")

    if err := h.repo.Delete(r.Context(), id); err != nil {
        if errors.Is(err, repository.ErrNotFound) {
            http.Error(w, "task not found", http.StatusNotFound)
            return
        }
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusNoContent)
}
```

### 4. Register routes (2 min)

In `cmd/server/main.go`:

```go
taskRepo := repository.NewTaskRepository()
taskHandler := handler.NewTaskHandler(taskRepo)

r.Route("/api/tasks", func(r chi.Router) {
    r.Get("/", taskHandler.List)
    r.Post("/", taskHandler.Create)
    r.Get("/{id}", taskHandler.GetByID)
    r.Put("/{id}", taskHandler.Update)
    r.Delete("/{id}", taskHandler.Delete)
})
```

### 5. Test it

```bash
# create
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn Go","description":"Complete all exercises"}'

# list
curl http://localhost:8080/api/tasks

# get by ID
curl http://localhost:8080/api/tasks/<id>

# update
curl -X PUT http://localhost:8080/api/tasks/<id> \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn Go","description":"All done!","completed":true}'

# delete
curl -X DELETE http://localhost:8080/api/tasks/<id>
```

## HTTP Status Codes

| Operation | Success | Not Found | Bad Request |
|-----------|---------|-----------|-------------|
| GET (list) | 200 | - | - |
| GET (single) | 200 | 404 | - |
| POST | 201 | - | 400 |
| PUT | 200 | 404 | 400 |
| DELETE | 204 | 404 | - |

## Checkpoint

- [ ] All CRUD operations work
- [ ] Proper HTTP status codes
- [ ] Validation on create/update
- [ ] 404 for missing resources

**Next:** Exercise 07 - Error Handling
