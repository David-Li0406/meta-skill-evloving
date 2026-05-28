---
name: charm-ui
description: Knowledge about the Charm ecosystem (Bubbletea, Lipgloss, Bubbles) used for the Drime Shell UI. Use when creating or modifying UI components, styling output, or handling user interaction.
---

# Charm UI Ecosystem

Drime Shell uses the Charm ecosystem for all UI rendering.

## Libraries

- **Lipgloss**: Styling and layout (`github.com/charmbracelet/lipgloss`)
- **Bubbletea**: The Elm Architecture (TEA) for TUI (`github.com/charmbracelet/bubbletea`)
- **Bubbles**: Common components (`github.com/charmbracelet/bubbles`)
- **Glamour**: Markdown rendering (`github.com/charmbracelet/glamour`)

## Styling Guidelines (Lipgloss)

- Use the `internal/ui` package for shared styles and theme detection.
- Support both Dark and Light themes (Catppuccin Mocha/Latte).
- Use semantic color names defined in `ui/colors.go` (e.g., `ColorPrimary`, `ColorError`).

### Catppuccin Color Palette Reference

| Color | Mocha (Dark) | Latte (Light) | Use For |
|-------|--------------|---------------|---------|
| Rosewater | `#f5e0dc` | `#dc8a78` | Subtle highlights |
| Red | `#f38ba8` | `#d20f39` | Errors, deletions |
| Green | `#a6e3a1` | `#40a02b` | Success, additions |
| Yellow | `#f9e2af` | `#df8e1d` | Warnings |
| Blue | `#89b4fa` | `#1e66f5` | Links, info |
| Mauve | `#cba6f7` | `#8839ef` | Folders |
| Text | `#cdd6f4` | `#4c4f69` | Primary text |
| Subtext | `#a6adc8` | `#6c6f85` | Secondary text |
| Surface | `#313244` | `#ccd0da` | Backgrounds |

```go
// Example: Styled error message
var errorStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("9")). // Red
    Bold(true)

fmt.Println(errorStyle.Render("Error: " + err.Error()))
```

## Components (Bubbles)

### Spinner (Async Operations)

Use `ui.WithSpinner` for operations taking >100ms.

```go
// Signature: WithSpinner[T any](w io.Writer, message string, immediate bool, action func() (T, error)) (T, error)
result, err := ui.WithSpinner(env.Stdout, "Loading...", false, func() (Result, error) {
    return client.DoSomething(ctx)
})

// For startup/immediate display, set immediate=true
data, err := ui.WithSpinner(os.Stderr, "Initializing...", true, func() (*Data, error) {
    return loadData(ctx)
})
```

### Progress Bar (Transfers)

Use `bubbles/progress` for file uploads/downloads.

```go
// Update progress in a loop
prog := progress.New(progress.WithDefaultGradient())
// ... inside loop ...
fmt.Print("\r" + prog.ViewAs(percent))
```

### Tables (Listings)

Use `ui.NewTable` (custom implementation) for structured data like `ls -l` or `ws members`.

```go
// internal/ui/table.go - custom ANSI-aware table
t := ui.NewTable(env.Stdout)
t.SetHeaders("NAME", "SIZE", "MODIFIED")
t.AddRow(name, size, modified)
t.AddRow(name2, size2, modified2)
t.Render()
```

### Pager (File Viewing)

Use `bubbles/viewport` for viewing large content (`less` command).

- Small files (<100KB): Print inline with syntax highlighting.
- Medium files (<10MB): Use Bubbletea viewport.
- Large files (>10MB): Use system pager (`less`).


## Bubbletea Model Pattern

For interactive components (prompts, pagers), implement the `tea.Model` interface:

```go
type Model struct {
    // State
}

func (m Model) Init() tea.Cmd {
    return nil
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "q", "ctrl+c":
            return m, tea.Quit
        }
    }
    return m, nil
}

func (m Model) View() string {
    return "Rendered view"
}
```
