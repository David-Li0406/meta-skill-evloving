// Package components provides reusable animated TUI components
package components

import (
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"

	"github.com/Dicklesworthstone/ntm/internal/tui/styles"
	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

// SpinnerStyle defines different spinner animations
type SpinnerStyle int

const (
	SpinnerDots SpinnerStyle = iota
	SpinnerLine
	SpinnerBounce
	SpinnerPoints
	SpinnerGlobe
	SpinnerMoon
	SpinnerMonkey
	SpinnerMeter
	SpinnerHamburger
)

var spinnerFrames = map[SpinnerStyle][]string{
	SpinnerDots:      {"⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"},
	SpinnerLine:      {"—", "\\", "|", "/"},
	SpinnerBounce:    {"⠁", "⠂", "⠄", "⡀", "⢀", "⠠", "⠐", "⠈"},
	SpinnerPoints:    {"∙∙∙", "●∙∙", "∙●∙", "∙∙●", "∙∙∙"},
	SpinnerGlobe:     {"🌍", "🌎", "🌏"},
	SpinnerMoon:      {"🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"},
	SpinnerMonkey:    {"🙈", "🙉", "🙊"},
	SpinnerMeter:     {"▱▱▱", "▰▱▱", "▰▰▱", "▰▰▰", "▰▰▱", "▰▱▱"},
	SpinnerHamburger: {"☱", "☲", "☴"},
}

// Spinner is an animated spinner component
type Spinner struct {
	Style          SpinnerStyle
	Color          lipgloss.Color
	Frame          int
	FPS            time.Duration
	Label          string
	Gradient       bool
	GradientColors []string
}

// SpinnerTickMsg is sent on each animation tick
type SpinnerTickMsg time.Time

// NewSpinner creates a new spinner with defaults
func NewSpinner() Spinner {
	t := theme.Current()
	return Spinner{
		Style:    SpinnerDots,
		Color:    t.Mauve,
		Frame:    0,
		FPS:      time.Millisecond * 80,
		Gradient: false,
		GradientColors: []string{
			string(t.Blue),
			string(t.Mauve),
			string(t.Pink),
		},
	}
}

// Init initializes the spinner
func (s Spinner) Init() tea.Cmd {
	return s.tick()
}

// Update handles spinner animation
func (s Spinner) Update(msg tea.Msg) (Spinner, tea.Cmd) {
	switch msg.(type) {
	case SpinnerTickMsg:
		frames, ok := spinnerFrames[s.Style]
		if !ok || len(frames) == 0 {
			frames = spinnerFrames[SpinnerDots]
		}
		s.Frame = (s.Frame + 1) % len(frames)
		return s, s.tick()
	}
	return s, nil
}

// View renders the spinner
func (s Spinner) View() string {
	frames, ok := spinnerFrames[s.Style]
	if !ok || len(frames) == 0 {
		frames = spinnerFrames[SpinnerDots] // fallback to default
	}
	frame := frames[s.Frame%len(frames)]

	var rendered string
	if s.Gradient && len(s.GradientColors) >= 2 {
		rendered = styles.Shimmer(frame, s.Frame*10, s.GradientColors...)
	} else {
		rendered = lipgloss.NewStyle().Foreground(s.Color).Render(frame)
	}

	if s.Label != "" {
		return rendered + " " + s.Label
	}
	return rendered
}

func (s Spinner) tick() tea.Cmd {
	return tea.Tick(s.FPS, func(t time.Time) tea.Msg {
		return SpinnerTickMsg(t)
	})
}

// TickCmd returns the tick command for external use
func (s Spinner) TickCmd() tea.Cmd {
	return s.tick()
}
