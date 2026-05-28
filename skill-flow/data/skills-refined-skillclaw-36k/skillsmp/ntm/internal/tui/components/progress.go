package components

import (
	"fmt"
	"strings"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"

	"github.com/Dicklesworthstone/ntm/internal/tui/styles"
	"github.com/Dicklesworthstone/ntm/internal/tui/terminal"
	"github.com/Dicklesworthstone/ntm/internal/tui/theme"
)

// Animation tick interval. Higher values reduce visual jitter but make
// animations less smooth. 150ms is a good balance.
const progressTickInterval = 150 * time.Millisecond

// ASCII fallback characters for terminals without Unicode block support
const (
	FilledASCII = "="
	EmptyASCII  = "-"
)

// ProgressBar is an animated progress bar with gradient support
type ProgressBar struct {
	Width          int
	Percent        float64
	ShowPercent    bool
	ShowLabel      bool
	Label          string
	GradientColors []string
	EmptyColor     lipgloss.Color
	FilledChar     string
	EmptyChar      string
	Animated       bool
	AnimationTick  int
}

// ProgressTickMsg is sent for animation updates
type ProgressTickMsg time.Time

// NewProgressBar creates a new progress bar with defaults
func NewProgressBar(width int) ProgressBar {
	t := theme.Current()
	return ProgressBar{
		Width:       width,
		Percent:     0,
		ShowPercent: true,
		ShowLabel:   false,
		GradientColors: []string{
			string(t.Blue),
			string(t.Teal),
			string(t.Green),
		},
		EmptyColor:    t.Surface0,
		FilledChar:    "█",
		EmptyChar:     "░",
		Animated:      true,
		AnimationTick: 0,
	}
}

// Init initializes the progress bar
func (p ProgressBar) Init() tea.Cmd {
	if p.Animated {
		return p.tick()
	}
	return nil
}

// Update handles progress bar updates
func (p ProgressBar) Update(msg tea.Msg) (ProgressBar, tea.Cmd) {
	switch msg.(type) {
	case ProgressTickMsg:
		p.AnimationTick++
		return p, p.tick()
	}
	return p, nil
}

// View renders the progress bar
func (p ProgressBar) View() string {
	// Calculate filled width
	filledWidth := int(p.Percent * float64(p.Width))
	emptyWidth := p.Width - filledWidth

	// Determine characters to use (ASCII fallback for limited terminals)
	filledChar, emptyChar := p.FilledChar, p.EmptyChar
	if !terminal.SupportsUnicodeBlocks() {
		filledChar, emptyChar = FilledASCII, EmptyASCII
	}

	// Create filled portion with gradient (or solid color for limited terminals)
	var filledStr string
	if filledWidth > 0 {
		barText := strings.Repeat(filledChar, filledWidth)
		if terminal.SupportsTrueColor() {
			if p.Animated {
				// Animated shimmer effect
				filledStr = styles.Shimmer(barText, p.AnimationTick, p.GradientColors...)
			} else {
				filledStr = styles.GradientText(barText, p.GradientColors...)
			}
		} else {
			// Fallback to solid primary color for terminals without true color
			filledStr = lipgloss.NewStyle().
				Foreground(theme.Current().Primary).
				Render(barText)
		}
	}

	// Create empty portion
	emptyStr := lipgloss.NewStyle().
		Foreground(p.EmptyColor).
		Render(strings.Repeat(emptyChar, emptyWidth))

	// Build result
	bar := filledStr + emptyStr

	if p.ShowPercent {
		percentStr := fmt.Sprintf(" %3.0f%%", p.Percent*100)
		bar += lipgloss.NewStyle().
			Foreground(theme.Current().Text).
			Render(percentStr)
	}

	if p.ShowLabel && p.Label != "" {
		bar = lipgloss.NewStyle().
			Foreground(theme.Current().Subtext).
			Render(p.Label+" ") + bar
	}

	return bar
}

// SetPercent updates the progress percentage
func (p *ProgressBar) SetPercent(percent float64) {
	if percent < 0 {
		p.Percent = 0
	} else if percent > 1 {
		p.Percent = 1
	} else {
		p.Percent = percent
	}
}

func (p ProgressBar) tick() tea.Cmd {
	return tea.Tick(progressTickInterval, func(t time.Time) tea.Msg {
		return ProgressTickMsg(t)
	})
}

// IndeterminateBar is a progress bar for unknown duration
type IndeterminateBar struct {
	Width     int
	Tick      int
	BarWidth  int
	Colors    []string
	Label     string
	ShowLabel bool
}

// NewIndeterminateBar creates a new indeterminate progress bar
func NewIndeterminateBar(width int) IndeterminateBar {
	t := theme.Current()
	return IndeterminateBar{
		Width:    width,
		BarWidth: 10,
		Colors: []string{
			string(t.Blue),
			string(t.Mauve),
			string(t.Pink),
		},
	}
}

// Update handles indeterminate bar animation
func (b IndeterminateBar) Update(msg tea.Msg) (IndeterminateBar, tea.Cmd) {
	switch msg.(type) {
	case ProgressTickMsg:
		b.Tick++
		return b, tea.Tick(progressTickInterval, func(t time.Time) tea.Msg {
			return ProgressTickMsg(t)
		})
	}
	return b, nil
}

// View renders the indeterminate bar
func (b IndeterminateBar) View() string {
	// Ensure bar width is smaller than total width
	barWidth := b.BarWidth
	if barWidth >= b.Width {
		barWidth = b.Width - 1
	}
	if barWidth < 1 {
		barWidth = 1
	}

	// Determine characters to use (ASCII fallback for limited terminals)
	filledChar, emptyChar := "█", "░"
	if !terminal.SupportsUnicodeBlocks() {
		filledChar, emptyChar = FilledASCII, EmptyASCII
	}

	// Calculate position (bouncing back and forth)
	period := (b.Width - barWidth) * 2
	if period < 1 {
		period = 1
	}
	pos := b.Tick % period
	if pos >= b.Width-barWidth {
		pos = period - pos
	}

	// Build bar
	var result strings.Builder
	bgStyle := lipgloss.NewStyle().Foreground(theme.Current().Surface0)

	// Empty before
	result.WriteString(bgStyle.Render(strings.Repeat(emptyChar, pos)))

	// Moving bar with gradient (or solid color for limited terminals)
	var bar string
	if terminal.SupportsTrueColor() {
		bar = styles.GradientText(strings.Repeat(filledChar, barWidth), b.Colors...)
	} else {
		bar = lipgloss.NewStyle().
			Foreground(theme.Current().Primary).
			Render(strings.Repeat(filledChar, barWidth))
	}
	result.WriteString(bar)

	// Empty after
	remaining := b.Width - pos - barWidth
	if remaining > 0 {
		result.WriteString(bgStyle.Render(strings.Repeat(emptyChar, remaining)))
	}

	output := result.String()

	if b.ShowLabel && b.Label != "" {
		output = lipgloss.NewStyle().
			Foreground(theme.Current().Subtext).
			Render(b.Label+" ") + output
	}

	return output
}

// Init initializes the indeterminate bar
func (b IndeterminateBar) Init() tea.Cmd {
	return tea.Tick(progressTickInterval, func(t time.Time) tea.Msg {
		return ProgressTickMsg(t)
	})
}
