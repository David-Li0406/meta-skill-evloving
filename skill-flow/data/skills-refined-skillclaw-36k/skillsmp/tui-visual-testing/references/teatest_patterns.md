# teatest Patterns and API Reference

This reference provides comprehensive documentation for using `teatest` (Bubble Tea's official testing package) for TUI visual testing.

## Installation

```bash
go get github.com/charmbracelet/x/exp/teatest
```

## Core API

### TestModel

The `TestModel` wraps a Bubble Tea model for testing.

```go
// Create a new test model
tm := teatest.NewTestModel(t, model, options...)

// Options available:
teatest.WithInitialTermSize(width, height int)  // Set terminal dimensions
```

### Sending Input

```go
// Send a key message
tm.Send(tea.KeyMsg{Type: tea.KeyEnter})
tm.Send(tea.KeyMsg{Type: tea.KeyUp})
tm.Send(tea.KeyMsg{Type: tea.KeyDown})
tm.Send(tea.KeyMsg{Type: tea.KeyTab})
tm.Send(tea.KeyMsg{Type: tea.KeyEsc})

// Send a rune (character)
tm.Send(tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune{'a'}})

// Send special keys
tm.Send(tea.KeyMsg{Type: tea.KeyCtrlC})
tm.Send(tea.KeyMsg{Type: tea.KeyCtrlD})

// Type a string
for _, r := range "hello world" {
    tm.Send(tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune{r}})
}
```

### Capturing Output

```go
// Get the final rendered output
output := tm.FinalOutput(t)

// Get output with timeout
output := tm.FinalOutput(t, teatest.WithFinalTimeout(5*time.Second))
```

### Golden File Comparison

```go
// Compare output against golden file
// Creates golden file on first run
teatest.RequireEqualOutput(t, output)

// Update golden files with -update flag
// go test -v ./... -update
```

## Common Key Types

```go
// Navigation
tea.KeyUp, tea.KeyDown, tea.KeyLeft, tea.KeyRight
tea.KeyHome, tea.KeyEnd
tea.KeyPgUp, tea.KeyPgDown

// Actions
tea.KeyEnter, tea.KeySpace, tea.KeyTab, tea.KeyBacktab
tea.KeyBackspace, tea.KeyDelete
tea.KeyEsc

// Control keys
tea.KeyCtrlA through tea.KeyCtrlZ
tea.KeyCtrlSpace, tea.KeyCtrlBackslash

// Function keys
tea.KeyF1 through tea.KeyF12
```

## Advanced Patterns

### Testing with Dependencies

```go
func TestWithMockService(t *testing.T) {
    // Create mock service
    mockSvc := &MockTodoService{
        Todos: []Todo{{Title: "Test", Complete: false}},
    }

    // Create model with mock
    m := NewModelWithService(mockSvc)
    tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(80, 24))

    time.Sleep(100 * time.Millisecond)
    teatest.RequireEqualOutput(t, tm.FinalOutput(t))
}
```

### Testing Async Operations

```go
func TestAsyncLoading(t *testing.T) {
    m := NewModel()
    tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(80, 24))

    // Wait for async operation to complete
    teatest.WaitFor(t, tm.Output(), func(output []byte) bool {
        return strings.Contains(string(output), "Loaded")
    }, teatest.WithDuration(5*time.Second))

    teatest.RequireEqualOutput(t, tm.FinalOutput(t))
}
```

### Testing Window Resize

```go
func TestWindowResize(t *testing.T) {
    m := NewModel()
    tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(80, 24))

    // Initial render
    time.Sleep(100 * time.Millisecond)

    // Simulate resize
    tm.Send(tea.WindowSizeMsg{Width: 120, Height: 40})
    time.Sleep(100 * time.Millisecond)

    teatest.RequireEqualOutput(t, tm.FinalOutput(t))
}
```

### Testing Mouse Events

```go
func TestMouseClick(t *testing.T) {
    m := NewModel()
    tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(80, 24))

    // Send mouse click at position (10, 5)
    tm.Send(tea.MouseMsg{
        X:      10,
        Y:      5,
        Type:   tea.MouseLeft,
        Action: tea.MouseActionPress,
    })

    time.Sleep(100 * time.Millisecond)
    teatest.RequireEqualOutput(t, tm.FinalOutput(t))
}
```

### Snapshot Testing Multiple States

```go
func TestAllStates(t *testing.T) {
    states := []struct {
        name    string
        setup   func(*teatest.TestModel)
    }{
        {
            name:  "initial",
            setup: func(tm *teatest.TestModel) {},
        },
        {
            name: "after_navigation",
            setup: func(tm *teatest.TestModel) {
                tm.Send(tea.KeyMsg{Type: tea.KeyDown})
                tm.Send(tea.KeyMsg{Type: tea.KeyDown})
            },
        },
        {
            name: "modal_open",
            setup: func(tm *teatest.TestModel) {
                tm.Send(tea.KeyMsg{Type: tea.KeyEnter})
            },
        },
    }

    for _, state := range states {
        t.Run(state.name, func(t *testing.T) {
            m := NewModel()
            tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(80, 24))

            state.setup(tm)
            time.Sleep(100 * time.Millisecond)

            teatest.RequireEqualOutput(t, tm.FinalOutput(t))
        })
    }
}
```

## Best Practices

### 1. Use Consistent Terminal Sizes

Always specify terminal size explicitly to ensure reproducible tests:

```go
tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(80, 24))
```

### 2. Add Appropriate Wait Times

Allow time for async operations and rendering:

```go
time.Sleep(100 * time.Millisecond) // After sends
time.Sleep(500 * time.Millisecond) // After async ops
```

### 3. Use Subtests for Organization

```go
func TestFeature(t *testing.T) {
    t.Run("initial_state", func(t *testing.T) { ... })
    t.Run("after_input", func(t *testing.T) { ... })
    t.Run("error_case", func(t *testing.T) { ... })
}
```

### 4. Handle Dynamic Content

For timestamps or dynamic IDs, either:
- Mock the time provider
- Use regex matching instead of exact comparison
- Normalize output before comparison

### 5. Review Golden Files in PRs

Golden files should be reviewed in code review to catch unintended visual changes.

## Troubleshooting

### "Golden file does not exist"

Run with `-update` flag to create initial golden files:
```bash
go test -v ./... -update
```

### "Output mismatch" but visually identical

Check for:
- Trailing whitespace differences
- Different terminal sizes
- ANSI escape code variations
- Dynamic content (timestamps, IDs)

### Tests pass locally but fail in CI

Ensure CI environment has:
- `TERM=xterm-256color`
- Consistent Go version
- Same terminal dimensions in test setup
