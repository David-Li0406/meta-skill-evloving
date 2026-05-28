# Exercise 09: Testing Services

**Time:** 15 minutes
**Goal:** Test service layer with interfaces and mocks

## The Spring Boot Version

```java
@ExtendWith(MockitoExtension.class)
class TaskServiceTest {

    @Mock
    TaskRepository repository;

    @InjectMocks
    TaskService service;

    @Test
    void createTask_savesToRepository() {
        when(repository.save(any())).thenAnswer(inv -> inv.getArgument(0));

        Task result = service.create(new CreateTaskRequest("Test"));

        verify(repository).save(any());
        assertThat(result.getTitle()).isEqualTo("Test");
    }
}
```

## The Go Way

Define interfaces at the consumer side, implement mocks manually or generate them:

```go
// interface defined where it's needed
type TaskRepository interface {
    FindByID(ctx context.Context, id string) (*model.Task, error)
    Save(ctx context.Context, task *model.Task) error
}

// mock implementation
type MockTaskRepository struct {
    FindByIDFn func(ctx context.Context, id string) (*model.Task, error)
    SaveFn     func(ctx context.Context, task *model.Task) error
}
```

---

## Step by Step

### 1. Define interface for repository (3 min)

Update `internal/service/task.go`:

```go
package service

import (
    "context"
    "errors"

    "github.com/google/uuid"

    "my-first-go-app/internal/model"
)

var ErrTaskNotFound = errors.New("task not found")

// TaskRepository defines what the service needs
type TaskRepository interface {
    FindByID(ctx context.Context, id string) (*model.Task, error)
    FindAll(ctx context.Context) ([]*model.Task, error)
    Save(ctx context.Context, task *model.Task) error
    Delete(ctx context.Context, id string) error
}

type TaskService struct {
    repo TaskRepository
}

func NewTaskService(repo TaskRepository) *TaskService {
    return &TaskService{repo: repo}
}

type CreateTaskInput struct {
    Title       string
    Description string
}

func (s *TaskService) Create(ctx context.Context, input CreateTaskInput) (*model.Task, error) {
    task := &model.Task{
        ID:          uuid.New().String(),
        Title:       input.Title,
        Description: input.Description,
        Completed:   false,
    }

    if err := s.repo.Save(ctx, task); err != nil {
        return nil, err
    }

    return task, nil
}

func (s *TaskService) GetByID(ctx context.Context, id string) (*model.Task, error) {
    task, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, ErrTaskNotFound
    }
    return task, nil
}

func (s *TaskService) Complete(ctx context.Context, id string) (*model.Task, error) {
    task, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, ErrTaskNotFound
    }

    task.Completed = true

    if err := s.repo.Save(ctx, task); err != nil {
        return nil, err
    }

    return task, nil
}
```

### 2. Create mock repository (4 min)

Create `internal/service/task_test.go`:

```go
package service_test

import (
    "context"
    "errors"
    "testing"

    "my-first-go-app/internal/model"
    "my-first-go-app/internal/service"
)

// MockTaskRepository implements service.TaskRepository
type MockTaskRepository struct {
    FindByIDFn func(ctx context.Context, id string) (*model.Task, error)
    FindAllFn  func(ctx context.Context) ([]*model.Task, error)
    SaveFn     func(ctx context.Context, task *model.Task) error
    DeleteFn   func(ctx context.Context, id string) error

    // track calls
    SaveCalls []*model.Task
}

func (m *MockTaskRepository) FindByID(ctx context.Context, id string) (*model.Task, error) {
    if m.FindByIDFn != nil {
        return m.FindByIDFn(ctx, id)
    }
    return nil, errors.New("not implemented")
}

func (m *MockTaskRepository) FindAll(ctx context.Context) ([]*model.Task, error) {
    if m.FindAllFn != nil {
        return m.FindAllFn(ctx)
    }
    return nil, errors.New("not implemented")
}

func (m *MockTaskRepository) Save(ctx context.Context, task *model.Task) error {
    m.SaveCalls = append(m.SaveCalls, task)
    if m.SaveFn != nil {
        return m.SaveFn(ctx, task)
    }
    return nil
}

func (m *MockTaskRepository) Delete(ctx context.Context, id string) error {
    if m.DeleteFn != nil {
        return m.DeleteFn(ctx, id)
    }
    return nil
}
```

### 3. Write service tests (5 min)

```go
func TestTaskService_Create(t *testing.T) {
    tests := []struct {
        name    string
        input   service.CreateTaskInput
        saveFn  func(ctx context.Context, task *model.Task) error
        wantErr bool
    }{
        {
            name: "creates task successfully",
            input: service.CreateTaskInput{
                Title:       "Test Task",
                Description: "Description",
            },
            saveFn:  func(ctx context.Context, task *model.Task) error { return nil },
            wantErr: false,
        },
        {
            name: "returns error when save fails",
            input: service.CreateTaskInput{
                Title: "Test",
            },
            saveFn: func(ctx context.Context, task *model.Task) error {
                return errors.New("db error")
            },
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            repo := &MockTaskRepository{SaveFn: tt.saveFn}
            svc := service.NewTaskService(repo)

            task, err := svc.Create(context.Background(), tt.input)

            if tt.wantErr {
                if err == nil {
                    t.Error("expected error, got nil")
                }
                return
            }

            if err != nil {
                t.Fatalf("unexpected error: %v", err)
            }

            if task.Title != tt.input.Title {
                t.Errorf("title = %s, want %s", task.Title, tt.input.Title)
            }

            if task.ID == "" {
                t.Error("expected task to have ID")
            }

            // verify save was called
            if len(repo.SaveCalls) != 1 {
                t.Errorf("Save called %d times, want 1", len(repo.SaveCalls))
            }
        })
    }
}

func TestTaskService_Complete(t *testing.T) {
    tests := []struct {
        name     string
        taskID   string
        findFn   func(ctx context.Context, id string) (*model.Task, error)
        wantErr  bool
        wantDone bool
    }{
        {
            name:   "completes existing task",
            taskID: "123",
            findFn: func(ctx context.Context, id string) (*model.Task, error) {
                return &model.Task{ID: id, Title: "Test", Completed: false}, nil
            },
            wantErr:  false,
            wantDone: true,
        },
        {
            name:   "returns error for missing task",
            taskID: "nonexistent",
            findFn: func(ctx context.Context, id string) (*model.Task, error) {
                return nil, errors.New("not found")
            },
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            repo := &MockTaskRepository{FindByIDFn: tt.findFn}
            svc := service.NewTaskService(repo)

            task, err := svc.Complete(context.Background(), tt.taskID)

            if tt.wantErr {
                if err == nil {
                    t.Error("expected error, got nil")
                }
                return
            }

            if err != nil {
                t.Fatalf("unexpected error: %v", err)
            }

            if task.Completed != tt.wantDone {
                t.Errorf("completed = %v, want %v", task.Completed, tt.wantDone)
            }
        })
    }
}
```

### 4. Run tests (3 min)

```bash
go test -v ./internal/service/...
```

## Using mockgen (Optional)

Generate mocks automatically:

```bash
go install go.uber.org/mock/mockgen@latest

# generate mock
mockgen -source=internal/service/task.go -destination=internal/service/mock_task_test.go -package=service_test
```

## Interface Segregation

Define small interfaces where you need them:

```go
// service only needs these
type TaskFinder interface {
    FindByID(ctx context.Context, id string) (*model.Task, error)
}

type TaskSaver interface {
    Save(ctx context.Context, task *model.Task) error
}

// function that only needs to find
func GetTaskTitle(finder TaskFinder, id string) (string, error) {
    task, err := finder.FindByID(context.Background(), id)
    if err != nil {
        return "", err
    }
    return task.Title, nil
}
```

## What Just Happened?

| Spring Boot | Go |
|-------------|-----|
| @Mock annotation | Manual mock struct |
| @InjectMocks | Pass mock to constructor |
| Mockito.when() | Set function field on mock |
| verify() | Check calls array |

## Checkpoint

- [ ] Interface defined for repository
- [ ] Mock implements interface
- [ ] Tests use table-driven pattern
- [ ] Service behavior is verified

**Next:** Exercise 10 - Database Setup
