---
name: tui-visual-testing
description: Visual regression testing for Bubble Tea TUI applications. This skill should be used when testing terminal UI appearance, capturing TUI screenshots, comparing visual output against golden files, or detecting UI regressions after code changes. Supports both static screen capture and interactive flow testing with simulated key sequences.
---

# TUI Visual Testing

This skill enables visual regression testing for Bubble Tea terminal applications. It provides tools to capture TUI output, convert it to screenshots, and compare against golden files to detect visual regressions.

## When to Use

- After modifying UI rendering code to verify appearance
- Testing that keyboard interactions produce expected visual results
- Capturing baseline screenshots for new UI states
- Comparing current output against approved golden files
- Debugging visual discrepancies in terminal output

## Core Workflow

```
1. Write test using teatest    →  Capture TUI output as text
2. Run capture script          →  Convert ANSI output to PNG
3. Compare against golden      →  Detect visual differences
4. Update golden if approved   →  Store new baseline
```

## Testing Approaches

### Approach 1: Go Test with teatest (Recommended)

Use Bubble Tea's official `teatest` package for programmatic testing.

**Setup test file** (e.g., `ui_test.go`):

```go
package main

import (
    "testing"
    "time"

    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/x/exp/teatest"
)

func TestMainView(t *testing.T) {
    // Create model
    m := NewModel()

    // Create test model with terminal size
    tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(80, 24))

    // Wait for initial render
    time.Sleep(100 * time.Millisecond)

    // Capture output
    out := tm.FinalOutput(t)

    // Compare against golden file
    teatest.RequireEqualOutput(t, out)
}

func TestKeyboardNavigation(t *testing.T) {
    m := NewModel()
    tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(80, 24))

    // Simulate key presses
    tm.Send(tea.KeyMsg{Type: tea.KeyDown})
    tm.Send(tea.KeyMsg{Type: tea.KeyDown})
    tm.Send(tea.KeyMsg{Type: tea.KeyEnter})

    time.Sleep(100 * time.Millisecond)

    out := tm.FinalOutput(t)
    teatest.RequireEqualOutput(t, out)
}
```

**Run tests**:
```bash
# Run tests and create golden files
go test -v ./...

# Update golden files after approved changes
go test -v ./... -update
```

### Approach 2: Screenshot Comparison

For pixel-perfect visual testing, convert ANSI output to images.

**Step 1: Capture TUI output**

```bash
# Run the capture script to get ANSI output
python scripts/capture_tui.py ./your-app --keys "jjk" --output /tmp/tui_output.txt
```

**Step 2: Convert to screenshot**

```bash
# Convert ANSI to PNG image
python scripts/ansi_to_image.py /tmp/tui_output.txt --output /tmp/screenshot.png
```

**Step 3: Compare screenshots**

```bash
# Compare against golden screenshot
python scripts/compare_screenshots.py golden/main_view.png /tmp/screenshot.png
```

## Scripts Reference

### scripts/capture_tui.py

Captures terminal output from a Bubble Tea application.

```bash
python scripts/capture_tui.py <app-binary> [options]

Options:
  --keys KEY_SEQUENCE    Keys to send (e.g., "jjk<enter>")
  --width WIDTH          Terminal width (default: 80)
  --height HEIGHT        Terminal height (default: 24)
  --output FILE          Output file (default: stdout)
  --timeout SECONDS      Max wait time (default: 5)
```

### scripts/ansi_to_image.py

Converts ANSI terminal output to a PNG image.

```bash
python scripts/ansi_to_image.py <input-file> [options]

Options:
  --output FILE          Output PNG file
  --font-size SIZE       Font size in pixels (default: 14)
  --theme THEME          Color theme: dark, light (default: dark)
```

### scripts/compare_screenshots.py

Compares two screenshots and reports differences.

```bash
python scripts/compare_screenshots.py <golden-file> <actual-file> [options]

Options:
  --threshold PERCENT    Acceptable difference percentage (default: 0.1)
  --output FILE          Save diff image to file
  --fail-on-diff         Exit with code 1 if different
```

## Directory Structure for Tests

Recommended project structure for visual tests:

```
your-project/
├── cmd/app/
│   ├── main.go
│   └── ui_test.go           # teatest-based tests
├── testdata/
│   └── TestMainView.golden  # Golden files (auto-generated)
└── visual-tests/
    ├── golden/              # Screenshot golden files
    │   ├── main_view.png
    │   └── edit_modal.png
    └── run_visual_tests.sh  # Test runner script
```

## 結合設計檢查

建議在進行視覺回歸測試時，同步使用 `tui-design-inspector` skill 進行人工設計審查。
你可以將自動化產生的截圖或 ANSI 輸出，交由設計檢查 skill 進行人工審查與設計建議，確保 UI 不僅外觀穩定，也符合最佳 UX 標準。

---


## Workflow: Adding a New Visual Test

1. **Write the test case**
   ```go
   func TestNewFeature(t *testing.T) {
       m := NewModel()
       tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(80, 24))
       // ... setup and interactions
       teatest.RequireEqualOutput(t, tm.FinalOutput(t))
   }
   ```

2. **Run test to generate golden file**
   ```bash
   go test -v -run TestNewFeature -update
   ```

3. **Review the golden file**
   - Check `testdata/TestNewFeature.golden`
   - Verify it looks correct

4. **Commit the golden file**
   ```bash
   git add testdata/TestNewFeature.golden
   ```

## Workflow: Updating Golden Files After UI Changes

1. **Make UI changes** in source code

2. **Run tests** to see failures
   ```bash
   go test -v ./...
   ```

3. **Review the diff** - Verify changes are intentional

4. **Update golden files**
   ```bash
   go test -v ./... -update
   ```

5. **Verify and commit**
   ```bash
   git diff testdata/
   git add testdata/
   git commit -m "Update golden files for UI changes"
   ```

## Common Patterns

### Testing Different Terminal Sizes

```go
func TestResponsiveLayout(t *testing.T) {
    sizes := []struct {
        name   string
        width  int
        height int
    }{
        {"small", 80, 24},
        {"medium", 120, 40},
        {"large", 200, 60},
    }

    for _, size := range sizes {
        t.Run(size.name, func(t *testing.T) {
            m := NewModel()
            tm := teatest.NewTestModel(t, m,
                teatest.WithInitialTermSize(size.width, size.height))
            teatest.RequireEqualOutput(t, tm.FinalOutput(t))
        })
    }
}
```

### Testing State Transitions

```go
func TestStateTransitions(t *testing.T) {
    m := NewModel()
    tm := teatest.NewTestModel(t, m, teatest.WithInitialTermSize(80, 24))

    // Initial state
    t.Run("initial", func(t *testing.T) {
        teatest.RequireEqualOutput(t, tm.FinalOutput(t))
    })

    // After navigation
    tm.Send(tea.KeyMsg{Type: tea.KeyTab})
    t.Run("after_tab", func(t *testing.T) {
        teatest.RequireEqualOutput(t, tm.FinalOutput(t))
    })

    // After action
    tm.Send(tea.KeyMsg{Type: tea.KeyEnter})
    t.Run("after_enter", func(t *testing.T) {
        teatest.RequireEqualOutput(t, tm.FinalOutput(t))
    })
}
```

## Troubleshooting

### Golden file mismatch but looks the same
- Check for trailing whitespace differences
- Verify terminal size matches between runs
- Check for timestamp or dynamic content in output

### ANSI codes in golden files look garbled
- Golden files contain raw ANSI - this is expected
- Use `cat testdata/Test.golden` to render properly
- Or use `scripts/ansi_to_image.py` to visualize

### Tests pass locally but fail in CI
- Ensure consistent terminal size in CI
- Set `TERM=xterm-256color` in CI environment
- Use fixed dimensions in test setup

## References

See `references/teatest_patterns.md` for advanced testing patterns and API documentation.
