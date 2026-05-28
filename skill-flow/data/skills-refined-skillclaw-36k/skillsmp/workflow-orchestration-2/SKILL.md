---
name: workflow-orchestration
description: >
  Workflow patterns from go-agents-orchestration library. Use when implementing
  workflows, state management, checkpoints, or parallel processing.
  Triggers: StateGraph, workflows.Register, WorkflowFactory, state.State,
  Observer, CheckpointStore, ProcessParallel, MultiObserver, StreamingObserver,
  graph.Execute, graph.Resume, OnEvent, workflow_runs, stages, decisions.
  File patterns: internal/workflows/*.go, workflows/**/*.go
---

# Workflow Orchestration Patterns

## When This Skill Applies

- Implementing workflow state graphs
- Creating workflow factories
- Handling checkpoints and resumption
- Observing workflow execution events
- Parallel processing within workflows

## Principles

### 1. WorkflowFactory Pattern

Workflows are registered via factories that create both graph structure and initial state:

```go
type WorkflowFactory func(
    ctx context.Context,
    graph state.StateGraph,
    runtime *Runtime,
    params map[string]any,
) (state.State, error)

func init() {
    workflows.Register("classify", Factory, "Document security marking classification")
}

func Factory(ctx context.Context, graph state.StateGraph, runtime *Runtime, params map[string]any) (state.State, error) {
    docID, err := workflows.ExtractDocumentID(params)
    if err != nil {
        return state.State{}, err
    }

    // Add nodes
    graph.AddNode("detect", detectNode(runtime, config))
    graph.AddNode("classify", classifyNode(runtime, agentID))
    graph.AddNode("assess", assessNode(runtime, agentID))

    // Add edges
    graph.AddEdge(state.START, "detect")
    graph.AddEdge("detect", "classify")
    graph.AddEdge("classify", "assess")
    graph.AddEdge("assess", state.END)

    return state.New(map[string]any{"document_id": docID.String()}), nil
}
```

### 2. Global Registry

Thread-safe workflow registration:

```go
var registry = &workflowRegistry{
    factories: make(map[string]WorkflowFactory),
    info:      make(map[string]WorkflowInfo),
}

func Register(name string, factory WorkflowFactory, description string) {
    registry.mu.Lock()
    defer registry.mu.Unlock()
    registry.factories[name] = factory
    registry.info[name] = WorkflowInfo{Name: name, Description: description}
}

func Get(name string) (WorkflowFactory, bool) {
    registry.mu.RLock()
    defer registry.mu.RUnlock()
    factory, exists := registry.factories[name]
    return factory, exists
}
```

### 3. Executor Pattern

Manages execution lifecycle with cancellation tracking:

```go
type executor struct {
    repo       *repo
    runtime    *Runtime
    db         *sql.DB
    logger     *slog.Logger
    activeRuns map[uuid.UUID]context.CancelFunc
    mu         sync.RWMutex
}

func (e *executor) Execute(name string, params map[string]any, token string) (<-chan ExecutionEvent, *Run, error) {
    factory, exists := Get(name)
    if !exists {
        return nil, nil, ErrWorkflowNotFound
    }

    ctx := e.runtime.Lifecycle().Context()
    run, err := e.repo.CreateRun(ctx, name, params)
    if err != nil {
        return nil, nil, fmt.Errorf("create run: %w", err)
    }

    streamingObs := NewStreamingObserver(defaultStreamBufferSize)
    go e.executeAsync(ctx, run.ID, factory, params, token, streamingObs)

    return streamingObs.Events(), run, nil
}
```

### 4. Observer Pattern

PostgreSQL-backed observer for auditing:

```go
type PostgresObserver struct {
    db         *sql.DB
    runID      uuid.UUID
    logger     *slog.Logger
    mu         sync.Mutex
    startTimes map[string]time.Time
}

func (o *PostgresObserver) OnEvent(ctx context.Context, event observability.Event) {
    o.mu.Lock()
    defer o.mu.Unlock()

    switch event.Type {
    case observability.EventNodeStart:
        o.handleNodeStart(ctx, event)
    case observability.EventNodeComplete:
        o.handleNodeComplete(ctx, event)
    case observability.EventEdgeTransition:
        o.handleEdgeTransition(ctx, event)
    }
}
```

**MultiObserver** for combining observers:
```go
postgresObs := NewPostgresObserver(e.db, runID, e.logger)
multiObs := observability.NewMultiObserver(postgresObs, streamingObs)
```

### 5. CheckpointStore Pattern

PostgreSQL-backed checkpoint persistence:

```go
type PostgresCheckpointStore struct {
    db     *sql.DB
    logger *slog.Logger
}

func (s *PostgresCheckpointStore) Save(ctx context.Context, checkpoint checkpoints.Checkpoint) error {
    data, err := json.Marshal(checkpoint)
    if err != nil {
        return err
    }

    const query = `
        INSERT INTO checkpoints (run_id, data, created_at)
        VALUES ($1, $2, $3)
        ON CONFLICT (run_id) DO UPDATE SET data = $2, created_at = $3
    `
    _, err = s.db.ExecContext(ctx, query, checkpoint.RunID, data, time.Now())
    return err
}
```

### 6. Graph Configuration

Checkpoint settings for workflow graphs:

```go
func workflowGraphConfig(name string) config.GraphConfig {
    cfg := config.DefaultGraphConfig(name)
    cfg.Checkpoint.Interval = 1   // Checkpoint every node
    cfg.Checkpoint.Preserve = true // Keep for resumption
    return cfg
}

graph, err := state.NewGraphWithDeps(cfg, observer, checkpointStore)
```

### 7. Secure Token Handling

Tokens stored as secrets, never checkpointed:

```go
initialState, err := factory(execCtx, graph, e.runtime, params)
if err != nil {
    return err
}

initialState.RunID = runID.String()
if token != "" {
    initialState = initialState.SetSecret("token", token)
}

finalState, err := graph.Execute(execCtx, initialState)
```

### 8. Streaming Events

Real-time event streaming via SSE:

```go
type StreamingObserver struct {
    events chan ExecutionEvent
    closed bool
    mu     sync.Mutex
}

func (o *StreamingObserver) OnEvent(ctx context.Context, event observability.Event) {
    o.mu.Lock()
    defer o.mu.Unlock()

    if o.closed {
        return
    }

    select {
    case o.events <- mapToExecutionEvent(event):
    default:
        // Buffer full, drop event
    }
}

func (o *StreamingObserver) Events() <-chan ExecutionEvent {
    return o.events
}
```

### 9. Parallel Processing

Worker pool for domain-level parallelism:

```go
func processParallel(ctx context.Context, items []Item) ([]Result, error) {
    workerCount := max(min(runtime.NumCPU(), len(items)), 1)
    tasks := make(chan int, len(items))
    results := make(chan task, len(items))

    var wg sync.WaitGroup
    for range workerCount {
        wg.Go(func() {
            processWorker(ctx, items, tasks, results)
        })
    }

    for i := range items {
        tasks <- i
    }
    close(tasks)

    go func() {
        wg.Wait()
        close(results)
    }()

    // Collect with order preservation
    resultMap := make(map[int]*Result)
    for t := range results {
        if t.err != nil {
            return nil, t.err
        }
        resultMap[t.item] = t.result
    }
    // ...
}
```

**Library ProcessParallel** for workflow stages:
```go
cfg := config.DefaultParallelConfig()
result, err := workflows.ProcessParallel(ctx, cfg, items, processor, nil)
```

## Patterns

### Node Implementation

```go
func detectNode(runtime *workflows.Runtime, opts DetectOptions) state.NodeFunc {
    return func(ctx context.Context, s state.State) (state.State, error) {
        start := time.Now()
        defer logNodeTiming(runtime.Logger(), "detect", start)

        docID, err := workflows.ExtractDocumentID(s)
        if err != nil {
            return s, err
        }

        // Get token from secrets (not checkpointed)
        token, _ := s.GetSecret("token")

        // ... process document

        return s.Set("detections", detections), nil
    }
}
```

### Conditional Edges

```go
graph.AddConditionalEdge("detect", func(s state.State) string {
    detections, _ := s.Get("detections").([]PageDetection)
    if needsEnhancement(detections) {
        return "enhance"
    }
    return "classify"
}, []string{"enhance", "classify"})
```

### Resume from Checkpoint

```go
func (e *executor) Resume(ctx context.Context, runID uuid.UUID) (*Run, error) {
    run, err := e.repo.FindRun(ctx, runID)
    if err != nil {
        return nil, err
    }

    if run.Status != StatusFailed && run.Status != StatusCancelled {
        return nil, ErrInvalidStatus
    }

    // Reconstruct graph with same configuration
    graph, err := state.NewGraphWithDeps(cfg, observer, checkpointStore)
    if err != nil {
        return nil, err
    }

    factory(execCtx, graph, e.runtime, params)

    // Resume from last checkpoint
    finalState, err := graph.Resume(execCtx, run.ID.String())
    // ...
}
```

## Database Tables

| Table | Purpose |
|-------|---------|
| workflow_runs | Execution metadata and status |
| stages | Node execution records (start, complete, timing) |
| decisions | Edge transitions and predicate results |
| checkpoints | State snapshots for resumption |

## Anti-Patterns

### Token in Regular State

```go
// Bad: Token gets checkpointed
initialState = initialState.Set("token", token)

// Good: Token stored as secret
initialState = initialState.SetSecret("token", token)
```

### Blocking Observer

```go
// Bad: Slow operation blocks workflow
func (o *Observer) OnEvent(ctx context.Context, event Event) {
    time.Sleep(5 * time.Second) // Blocks execution
}

// Good: Non-blocking with buffered channel
func (o *StreamingObserver) OnEvent(ctx context.Context, event Event) {
    select {
    case o.events <- event:
    default:
        // Drop if buffer full
    }
}
```

### Missing Error Handling in Nodes

```go
// Bad: Swallowing errors
func nodeFunc(ctx context.Context, s state.State) (state.State, error) {
    result, _ := doWork()  // Ignoring error
    return s.Set("result", result), nil
}

// Good: Propagate errors for proper status tracking
func nodeFunc(ctx context.Context, s state.State) (state.State, error) {
    result, err := doWork()
    if err != nil {
        return s, fmt.Errorf("do work: %w", err)
    }
    return s.Set("result", result), nil
}
```
